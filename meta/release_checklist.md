# Release Checklist

Create a GitHub issue with the following body, to collaborate on the release and ensure nothing is forgotten.

If any new task becomes necessary, make notes during the release, and update this template afterwards :-)

```
Rough order of the tasks for this release:

Changelog

 - [ ] Create new unreleased section with all the usual sections emptied out
 - [ ] Turn current Unreleased section into the new version section
 - [ ] Remove empty sections from the new version's section
 - [ ] Update the tag diff link for this version

Search for the previous version name and put in the new version instead, in places where this makes sense

- [ ] Link to current version in the readme intro
- [ ] The example value for `ecs.version`
- [ ] Anywhere else?

Git

- [ ] Commit the changes
- [ ] Have someone review a PR of your work
- [ ] Merge
- [ ] If appropriate, create a branch for further work in this version's lineage.

GitHub release

- [ ] Version tag must start with `v` and should be this format: `v0.0.0` for releases and `v0.0.0-label0` for pre-releases (replace label with the kind of pre-release: alpha, beta, rc)
- [ ] Release title should match the format of the previous ones
- [ ] Paste the whole changelog Markdown into the release body
- [ ] Consider adding an intro paragraph above the changelog in the release body, if there's anything to explain about this version.
- [ ] Check the pre-release checkbox, if this is a pre-release
- [ ] Submit the release

Life

- Celebrate :-)
```
