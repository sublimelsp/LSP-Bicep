# Releasing LSP-Bicep

## How updates arrive

[Renovate](https://docs.renovatebot.com/) monitors the
[Azure/bicep](https://github.com/Azure/bicep) GitHub releases and opens a PR
when a new version is available. The PR updates the `VERSION` variable in
`plugin.py`, which controls which language server binary the plugin downloads.

Renovate automerges patch updates once the smoke test passes. Bicep is still
0.x, so minor updates (e.g., v0.41.2 -> v0.42.0) need a manual merge.

Every merge to `main` runs the [release workflow](https://github.com/sublimelsp/lsp_release_workflow),
which releases according to the [conventional commits](https://www.conventionalcommits.org/)
since the latest tag: `feat` makes a minor release, and `fix`, `perf` and
`revert` make a patch release. Renovate's commits are `fix(deps): ...`, so each
language server update makes a patch release.

## Routine release (language server update only)

Most Renovate PRs are routine version bumps with no breaking changes. Patch
updates are merged and released automatically. For a minor update:

### 1. Verify the update works

The smoke test checks that the server starts and reports diagnostics on all
platforms. To also check that the new language server version starts and lints
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
- Deprecations, removed or added features.

### 3. Merge the PR

Merge the Renovate PR on GitHub. The release workflow then makes a patch
release, and Package Control picks it up from the tag.

To release a minor or major version instead, merge the PR with a commit
message that needs one, such as `feat: ...` for a minor release, or run the
[release workflow](../../actions/workflows/release.yml) manually with the
`bump` input.

## Breaking change release

When a Bicep update introduces breaking changes (such as a new .NET SDK
requirement), additional files need updating before merging.

### Additional steps

1. **Update documentation** if the .NET version requirement changes:
   - `README.md` — update the required .NET SDK version.
   - `LSP-Bicep.sublime-settings` — update the minimum version comment.

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

3. Commit these changes to the Renovate PR branch before merging it. A new
   version in `messages.json` makes the release workflow release that version,
   with the message as the release notes.

## Version numbering

This project has two independent version numbers:

| Version                  | Where           | What it tracks                                        |
| ------------------------ | --------------- | ----------------------------------------------------- |
| `VERSION` in `plugin.py` | e.g., `v0.41.2` | The Azure/bicep language server release being bundled |
| Git tag / GitHub release | e.g., `v2.0.1`  | The LSP-Bicep plugin release for Package Control      |

Renovate manages the first. The release workflow manages the second.
