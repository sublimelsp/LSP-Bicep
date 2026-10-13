from __future__ import annotations

from LSP.plugin import ClientConfig
from LSP.plugin import LspPlugin
from LSP.plugin import OnPreStartContext
from LSP.plugin import PluginStartError
from typing import final
from urllib.request import urlretrieve
from zipfile import ZipFile
import re
import shutil
import subprocess

VERSION = "v0.48.1"
URL = "https://github.com/Azure/bicep/releases/download/{0}/bicep-langserver.zip"
DOTNET_MIN_MAJOR = 10


@final
class Bicep(LspPlugin):
    @classmethod
    def installed_version_str(cls) -> str:
        with (cls.plugin_storage_path / "VERSION").open("r") as f:
            return f.readline().strip()

    @classmethod
    def needs_update_or_installation(cls) -> bool:
        try:
            if VERSION == cls.installed_version_str():
                return False
        except Exception:
            pass
        return True

    @classmethod
    def install_or_update(cls) -> None:
        basedir = cls.plugin_storage_path
        shutil.rmtree(basedir, ignore_errors=True)
        basedir.mkdir(parents=True, exist_ok=True)
        zipfile = basedir / "biceplangserver.zip"
        try:
            urlretrieve(URL.format(VERSION), zipfile)
            with ZipFile(zipfile, "r") as f:
                f.extractall(basedir)
            zipfile.unlink()
            (basedir / "VERSION").write_text(VERSION)
        except Exception:
            shutil.rmtree(basedir, ignore_errors=True)
            raise

    @classmethod
    def check_dotnet(cls, configuration: ClientConfig) -> str:
        """Return the dotnet executable to use. Raise PluginStartError when it is missing or too old."""
        dotnet = configuration.root_settings.get("dotnet_executable") or "dotnet"
        resolved = shutil.which(dotnet)
        if not resolved:
            raise PluginStartError(
                'dotnet not found. Install .NET {} or set "dotnet_executable" in the LSP-Bicep settings.'.format(
                    DOTNET_MIN_MAJOR
                )
            )
        try:
            result = subprocess.run(
                [resolved, "--list-runtimes"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                universal_newlines=True,
                timeout=15,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except Exception:
            return dotnet  # Could not ask. Let the server try to start.
        if result.returncode != 0:
            return dotnet
        runtimes = re.finditer(r"^Microsoft\.NETCore\.App (\d+)\.", result.stdout, re.MULTILINE)
        majors = [int(m.group(1)) for m in runtimes]
        if not majors:
            raise PluginStartError(
                'No .NET runtime found by "dotnet --list-runtimes". Install .NET {}.'.format(DOTNET_MIN_MAJOR)
            )
        if max(majors) < DOTNET_MIN_MAJOR:
            raise PluginStartError(
                ".NET runtime {} found, but Bicep needs {} or newer. Install .NET {}.".format(
                    max(majors), DOTNET_MIN_MAJOR, DOTNET_MIN_MAJOR
                )
            )
        return dotnet

    @classmethod
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        # Check dotnet first, so that a missing or old .NET is reported before the 65 MB server is downloaded.
        context.variables["dotnet_executable"] = cls.check_dotnet(context.configuration)
        if cls.needs_update_or_installation():
            try:
                cls.install_or_update()
            except Exception as ex:
                raise PluginStartError("Failed to install the Bicep language server: {}".format(ex))


def plugin_loaded() -> None:
    Bicep.register()


def plugin_unloaded() -> None:
    Bicep.unregister()
