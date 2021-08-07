# LSP-Bicep

This is a helper package that automatically installs and updates
[Bicep.LangServer](https://github.com/Azure/bicep) for you.

To use this package, you must have:

- The [Bicep syntax](https://packagecontrol.io/packages/Bicep) package.
- The [LSP](https://packagecontrol.io/packages/LSP) package.
- The [.NET SDK](https://dotnet.microsoft.com/download). **Minimum version is v5**.
- Either make sure that the `dotnet` executable is in your $PATH, or configure the path to the `dotnet` executable via the package settings (see below).

## Applicable Selectors

This language server operates on views with the `source.bicep` base scope.

## Installation Location

The server is installed in the $CACHE/Package Storage/LSP-Bicep directory, where $CACHE is the base cache path of Sublime Text. For instance, $CACHE is `~/.cache/sublime-text` on a Linux system. If you want to force a re-installation of the server, you can delete the entire $CACHE/Package Storage/LSP-Bicep directory.

Like any helper package, installation starts when you open a view that is suitable for this language server. In this case, that means that when you open a view with the `source.bicep` base scope, installation commences.

## Configuration

_Optionally_ configure Bicep.LangServer by accessing `Preferences > Package Settings > LSP > Servers > LSP-Bicep`. However, by default things should work out of the box.
