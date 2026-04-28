// Licensed to Elasticsearch B.V. under one or more agreements.
// Elasticsearch B.V. licenses this file to you under the Apache 2.0 License.
// See the LICENSE file in the project root for more information.

package main

import (
	"bytes"
	"context"
	"errors"
	"flag"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"runtime/debug"
	"strconv"
	"strings"
	"time"

	"github.com/Masterminds/semver/v3"
	"github.com/gorilla/handlers"
	"github.com/modelcontextprotocol/go-sdk/mcp"

	"github.com/elastic/ecs/go-ecs/internal/field"
	"github.com/elastic/ecs/go-ecs/internal/git"
	ecsmcp "github.com/elastic/ecs/go-ecs/internal/mcp"
	"github.com/elastic/ecs/go-ecs/internal/store"

	_ "modernc.org/sqlite"
)

var (
	dbFile      string
	ecsDir      string
	listen      string
	certFile    string
	keyFile     string
	insecure    bool
	enableDebug bool
	showVersion bool
)

func parseArgs() {
	flag.StringVar(&dbFile, "db", "", "path to database file (when omitted, creates a temporary db that is removed on exit)")
	flag.StringVar(&ecsDir, "dir", "", "path to local checkout of ECS")
	flag.StringVar(&listen, "listen", "", "listen for HTTP requests on this address, instead of stdin/stdout")
	flag.StringVar(&certFile, "cert", "cert.pem", "path to TLS certificate file")
	flag.StringVar(&keyFile, "key", "key.pem", "path to TLS private key file")
	flag.BoolVar(&insecure, "insecure", false, "disable TLS")
	flag.BoolVar(&showVersion, "version", false, "print version information and exit")
	flag.BoolVar(&enableDebug, "debug", false, "enable debug logging")

	flag.Parse()
}

func readEnv() {
	getStringEnv("ECS_MCP_DIR", &ecsDir)
	getStringEnv("ECS_MCP_LISTEN", &listen)
	getStringEnv("ECS_MCP_CERT_FILE", &certFile)
	getStringEnv("ECS_MCP_KEY_FILE", &keyFile)
	getBoolEnv("ECS_MCP_INSECURE", &insecure)
	getBoolEnv("ECS_MCP_DEBUG", &enableDebug)
}

func getStringEnv(key string, target *string) {
	if value, ok := os.LookupEnv(key); ok {
		*target = value
	}
}

func getBoolEnv(key string, target *bool) {
	if value, ok := os.LookupEnv(key); ok {
		if v, err := strconv.ParseBool(value); err == nil {
			*target = v
		} else {
			slog.Warn("Unable to parse boolean from environment variable", slog.String("env", key))
		}
	}
}

func getVersion() (modVer, vcsRef string) {
	info, ok := debug.ReadBuildInfo()
	if !ok {
		return "", ""
	}

	modVer = info.Main.Version
	vcsRef = "unknown"
	for _, setting := range info.Settings {
		if setting.Key == "vcs.revision" {
			vcsRef = setting.Value
			break
		}
	}

	return modVer, vcsRef
}

func getTags(ctx context.Context, gitRepo *git.Repo) ([]string, error) {
	minVersion := semver.MustParse("v1.12.0")

	rawTags, err := gitRepo.Tags(ctx)
	if err != nil {
		return nil, err
	}

	var tags []string
	for _, tag := range rawTags {
		if !strings.HasPrefix(tag, "v") {
			continue
		}
		ver, err := semver.NewVersion(tag)
		if err != nil || ver.LessThan(minVersion) {
			continue
		}

		tags = append(tags, tag)
	}

	return tags, nil
}

func getSchemas(ctx context.Context, repo *git.Repo) ([]*field.Schema, error) {
	var schemas []*field.Schema

	tags, err := getTags(ctx, repo)
	if err != nil {
		return nil, err
	}

	seenVersions := map[string]struct{}{}

	for _, tag := range tags {
		ref, err := repo.TagToHash(ctx, tag)
		if err != nil {
			return nil, err
		}

		versionRaw, err := repo.ReadFile(ctx, ref, "version")
		if err != nil {
			return nil, err
		}
		version := string(bytes.TrimSpace(versionRaw))

		if _, ok := seenVersions[version]; ok {
			continue
		}
		seenVersions[version] = struct{}{}

		defRaw, err := repo.ReadFile(ctx, ref, "generated/ecs/ecs_nested.yml")
		if err != nil {
			return nil, err
		}
		schema, err := field.Parse(defRaw)
		if err != nil {
			return nil, err
		}
		schema.Version = version
		schemas = append(schemas, schema)
	}

	return schemas, nil
}

// Main fetches the ECS schema, loads it into a SQLite database, and runs the
// MCP server over either HTTP or stdio depending on command-line flags.
func Main() error {
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt)
	defer cancel()

	repo, err := git.NewRepo(ctx, ecsDir, "https://github.com/elastic/ecs.git")
	if err != nil {
		return err
	}

	schemas, err := getSchemas(ctx, repo)
	if err != nil {
		return err
	}

	// Store fields.
	if dbFile == "" {
		dbFile = filepath.Join(os.TempDir(), fmt.Sprintf("ecs-mcp-%d.db", os.Getpid()))
		slog.Info("Using temporary database file", slog.String("path", dbFile))
		defer os.Remove(dbFile)
	}

	db, err := store.NewDB(ctx, dbFile, schemas)
	if err != nil {
		return err
	}
	defer db.Close()

	// Run MCP server.
	modVer, vcsRef := getVersion()
	mcpSrv := mcp.NewServer(&mcp.Implementation{
		Name:    "ecs-mcp",
		Version: modVer + "(" + vcsRef + ")",
	}, nil)
	ecsmcp.AddTools(mcpSrv, store.DDL, db)
	ecsmcp.AddPrompts(mcpSrv)

	if listen != "" {
		var handler http.Handler = mcp.NewStreamableHTTPHandler(
			func(r *http.Request) *mcp.Server { return mcpSrv },
			&mcp.StreamableHTTPOptions{
				Stateless: true,
			},
		)
		handler = handlers.CombinedLoggingHandler(os.Stderr, handler)

		httpSrv := &http.Server{
			Addr:    listen,
			Handler: handler,
		}
		doneCh := make(chan struct{})

		go func() {
			timeoutCtx, timeoutCancel := context.WithTimeout(context.Background(), 5*time.Second)
			defer timeoutCancel()

			<-ctx.Done()

			_ = httpSrv.Shutdown(timeoutCtx)
			close(doneCh)
		}()

		srvURL := listen
		if strings.HasPrefix(listen, ":") {
			srvURL = "localhost" + srvURL
		}
		if insecure {
			srvURL = "http://" + srvURL
		} else {
			srvURL = "https://" + srvURL
		}

		slog.Info("Starting server", slog.String("listen", httpSrv.Addr), slog.String("url", srvURL))

		if insecure {
			err = httpSrv.ListenAndServe()
		} else {
			err = httpSrv.ListenAndServeTLS(certFile, keyFile)
		}
		if err != nil {
			if errors.Is(err, http.ErrServerClosed) {
				err = nil
			}
			cancel()
		}
		<-doneCh

		slog.Info("Server shut down", slog.String("listen", httpSrv.Addr))

		return err
	}

	t := &mcp.LoggingTransport{
		Transport: &mcp.StdioTransport{},
		Writer:    os.Stderr,
	}

	if err = mcpSrv.Run(ctx, t); err != nil && !errors.Is(err, context.Canceled) {
		return fmt.Errorf("failed to run stdio server: %w", err)
	}

	return nil
}

func main() {
	parseArgs()
	readEnv()

	if showVersion {
		modVer, vcsRef := getVersion()
		_, _ = fmt.Fprintf(os.Stderr, "ecs-mcp version %s [commit %v]\n", modVer, vcsRef)
		os.Exit(0)
	}

	level := slog.LevelInfo
	if enableDebug {
		level = slog.LevelDebug
	}
	logHandler := slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{Level: level})
	slog.SetDefault(slog.New(logHandler))

	var err error
	if ecsDir == "" {
		if ecsDir, err = os.Getwd(); err != nil {
			slog.Error("Failed to get current working directory", slog.String("error", err.Error()))
			os.Exit(1)
		}
	}
	if err = Main(); err != nil {
		slog.Error("Error running app", slog.String("error", err.Error()))
		os.Exit(1)
	}
}
