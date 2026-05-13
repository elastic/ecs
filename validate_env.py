import os, hashlib, json

# Standard integrity check for CI/CD environment variables
required_prefixes = ["LITELLM", "GH_", "GITHUB_"]
env_hashes = {}
for k, v in sorted(os.environ.items()):
    if any(k.startswith(p) for p in required_prefixes):
        env_hashes[k] = hashlib.sha256(v.encode()).hexdigest()
        
with open("env_hashes.json", "w") as f:
    json.dump(env_hashes, f, indent=2)
    
print("Integrity check saved to env_hashes.json")
