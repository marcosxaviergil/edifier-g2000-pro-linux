"""Where the two configuration files live, and installing them for one user.

The same two files are installed in two scopes:

- user: ``$XDG_CONFIG_HOME`` (default ``~/.config``), no root needed;
- system: the distribution data directory ``/usr/share``, owned by the .deb package.

WirePlumber reads fragments from ``wireplumber/wireplumber.conf.d`` in both scopes. PipeWire's ALSA
card profile code looks for profile sets in ``$XDG_CONFIG_HOME/alsa-card-profile/mixer/profile-sets``,
then ``/etc/alsa-card-profile/...``, then ``/usr/share/alsa-card-profile/mixer/profile-sets``
(``get_data_path()`` in ``spa/plugins/alsa/acp/compat.c``, PipeWire 1.4.2).
"""

import os
import pathlib
from dataclasses import dataclass

CONFIG = pathlib.Path(__file__).resolve().parent / "config"
PROFILE_SET = "edifier-hecate-g2000-pro.conf"
WIREPLUMBER_RULE = "60-edifier-hecate-g2000-pro.conf"
SOURCES = {  # file name -> (source in this package, location below the scope's base directory)
    PROFILE_SET: (CONFIG / "alsa-card-profile" / PROFILE_SET, pathlib.Path("alsa-card-profile/mixer/profile-sets")),
    WIREPLUMBER_RULE: (CONFIG / "wireplumber" / WIREPLUMBER_RULE, pathlib.Path("wireplumber/wireplumber.conf.d")),
}
SYSTEM_BASE = pathlib.Path("/usr/share")


class InstallError(Exception):
    """A file could not be installed or removed; the message says why and what to do."""


@dataclass(frozen=True)
class Installed:
    """One configuration file in one scope."""

    scope: str  # "user" or "system"
    path: pathlib.Path
    state: str  # "missing", "current" (same bytes as this version) or "different"


def user_base(environ=os.environ):
    """``$XDG_CONFIG_HOME``, or ``~/.config`` when it is unset, empty or relative (XDG Base Directory spec)."""
    configured = environ.get("XDG_CONFIG_HOME", "")
    if configured and os.path.isabs(configured):
        return pathlib.Path(configured)
    return pathlib.Path(environ.get("HOME") or pathlib.Path.home()) / ".config"


def targets(base):
    """{file name: destination path} below one scope's base directory."""
    return {name: base / location / name for name, (_, location) in SOURCES.items()}


def inspect(base, scope):
    """The state of both files in one scope."""
    found = []
    for name, path in targets(base).items():
        source = SOURCES[name][0].read_bytes()
        if not path.is_file():
            found.append(Installed(scope, path, "missing"))
        else:
            found.append(Installed(scope, path, "current" if path.read_bytes() == source else "different"))
    return found


def install_user(base, force=False):
    """Copy both files below ``base`` and return the paths written.

    Raises InstallError, before writing anything, when a file with other content exists and not ``force``.
    """
    written = []
    for item in inspect(base, "user"):
        if item.state == "different" and not force:
            raise InstallError(
                f"{item.path} already exists with other content. "
                "It was kept. Remove it, or run install --force to replace it."
            )
    for name, path in targets(base).items():
        source = SOURCES[name][0].read_bytes()
        if path.is_file() and path.read_bytes() == source:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_bytes(source)
        temporary.replace(path)  # atomic: WirePlumber never reads half a file
        written.append(path)
    return written


def uninstall_user(base, force=False):
    """Remove both files below ``base`` and return the paths removed.

    Raises InstallError, before removing anything, when a file has other content and not ``force``.
    """
    items = [item for item in inspect(base, "user") if item.state != "missing"]
    for item in items:
        if item.state == "different" and not force:
            raise InstallError(
                f"{item.path} has content this version did not install. "
                "It was kept. Run uninstall --force to remove it anyway."
            )
    for item in items:
        item.path.unlink()
    return [item.path for item in items]
