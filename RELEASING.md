# Releasing LSP-Bicep

## How updates arrive

[Renovate](https://docs.renovatebot.com/) monitors the
[Azure/bicep](https://github.com/Azure/bicep) GitHub releases and opens a PR
when a new version is available. The PR updates the `VERSION` variable in
`plugin.py`, which controls which language server binary the plugin downloads.

## Routine release (language server update only)

Most Renovate PRs are routine version bumps with no breaking changes.

### 1. Verify the update works

Before merging, check that the new language server version starts and lints
correctly in Sublime Text:

1. Check out the Renovate branch locally.
2. Restart Sublime Text (or run `LSP: Restart All Servers`).
3. Open a `.bicep` file and confirm the server starts without errors.
4. Introduce a deliberate error to verify diagnostics are working, for example:
   ```bicep
   output test string = nonExistentVariable
   ```
   You should see an error diagnostic on `nonExistentVariable`.
5. Remove the test error.

### 2. Check upstream release notes

Skim the [Azure/bicep release notes](https://github.com/Azure/bicep/releases)
for the new version. Look for:

- Changes to the .NET SDK version requirement.
- Breaking changes in language server behavior.
- Deprecations or removed features.

### 3. Merge the PR

Merge the Renovate PR on GitHub.

### 4. Create a release

Choose the new plugin version number:

- **Patch** (e.g., v2.0.0 -> v2.0.1): Routine language server update, no
  breaking changes.
- **Minor** (e.g., v2.0.1 -> v2.1.0): New language server features worth
  highlighting, but no breaking changes.
- **Major** (e.g., v2.1.0 -> v3.0.0): Breaking changes (e.g., new .NET SDK
  version required).

Create the release on the upstream repo:

```sh
gh release create vX.Y.Z --repo sublimelsp/LSP-Bicep \
  --title "vX.Y.Z" \
  --notes "Update Bicep language server to vA.B.C"
```

Package Control picks up new releases automatically from the tag.

## Breaking change release

When a Bicep update introduces breaking changes (such as a new .NET SDK
requirement), additional files need updating before merging.

### Additional steps

1. **Update documentation** if the .NET version requirement changes:
   - `README.md` — update the required .NET SDK version.
   - `LSP-Bicep.sublime-settings` — update the version comment.

2. **Add an upgrade message** so users see a notice in Sublime Text:
   - Create `messages/<version>.txt` with the upgrade notice. See
     `messages/2.0.0.txt` for an example.
   - Add an entry to `messages.json` mapping the version to the new file:
     ```json
     {
       "2.0.0": "messages/2.0.0.txt",
       "3.0.0": "messages/3.0.0.txt"
     }
     ```

3. Commit these changes to the Renovate PR branch (or as a follow-up commit on
   `main`) before tagging the release.

## Version numbering

This project has two independent version numbers:

| Version                  | Where           | What it tracks                                        |
| ------------------------ | --------------- | ----------------------------------------------------- |
| `VERSION` in `plugin.py` | e.g., `v0.41.2` | The Azure/bicep language server release being bundled |
| Git tag / GitHub release | e.g., `v2.0.1`  | The LSP-Bicep plugin release for Package Control      |

Renovate manages the first. You manage the second.
