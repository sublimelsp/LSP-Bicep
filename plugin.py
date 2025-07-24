from urllib.request import urlretrieve
from zipfile import ZipFile
import os
import shutil

from LSP.plugin import AbstractPlugin
from LSP.plugin import register_plugin
from LSP.plugin import unregister_plugin
from LSP.plugin.core.typing import Optional, Dict
import sublime


VERSION = "v0.36.177"
URL = "https://github.com/Azure/bicep/releases/download/{0}/bicep-langserver.zip"  # noqa: E501


class Bicep(AbstractPlugin):
    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @classmethod
    def additional_variables(cls) -> Optional[Dict[str, str]]:
        filename = "LSP-{}.sublime-settings".format(cls.name())
        settings = sublime.load_settings(filename)
        dotnet_executable = settings.get("dotnet_executable")
        if not dotnet_executable:
            dotnet_executable = "dotnet"
        return {"dotnet_executable": dotnet_executable}

    @classmethod
    def installed_version_str(cls) -> str:
        filename = os.path.join(cls.basedir(), "VERSION")
        with open(filename, "r") as f:
            return f.readline().strip()

    @classmethod
    def basedir(cls) -> str:
        return os.path.join(cls.storage_path(), "LSP-{}".format(cls.name()))

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
        shutil.rmtree(cls.basedir(), ignore_errors=True)
        os.makedirs(cls.basedir(), exist_ok=True)
        zipfile = os.path.join(cls.basedir(), "biceplangserver.zip")
        try:
            urlretrieve(URL.format(VERSION), zipfile)
            with ZipFile(zipfile, "r") as f:
                f.extractall(cls.basedir())
            os.unlink(zipfile)
            with open(os.path.join(cls.basedir(), "VERSION"), "w") as fp:
                fp.write(VERSION)
        except Exception:
            shutil.rmtree(cls.basedir(), ignore_errors=True)
            raise


def plugin_loaded() -> None:
    register_plugin(Bicep)


def plugin_unloaded() -> None:
    unregister_plugin(Bicep)
