"""What forgejo_release.py and github_release.py share: the release files, the notes, the API clients.

Adapted from the release scripts of opendeck-uno-overlays (same author, MIT), with the same rules:
the tag must be v<version>, the notes are the CHANGELOG section of the version plus the SHA-256 of
every file, and requests carry their own User-Agent (a Cloudflare in front of Forgejo can refuse
Python's default one with HTTP 403, error 1010).
"""

import hashlib
import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from hecate_volume import __version__  # noqa: E402 - the version of the code itself

USER_AGENT = "hecate-g2000-pro-volume-release"
NAME = "Hecate G2000 PRO Volume"
LOOPBACK = ("127.0.0.1", "localhost", "::1")  # plain http only here (the tests' stand-in); the token needs TLS


def fail(message):
    sys.exit(f"release: {message}")


def release_files(version=__version__):
    """(path, media type) of everything a release carries, in upload order."""
    dist = ROOT / "dist"
    return [
        (dist / f"hecate-g2000-pro-volume_{version}_all.deb", "application/vnd.debian.binary-package"),
        (dist / f"hecate-g2000-pro-volume-{version}.tar.gz", "application/gzip"),
        (dist / f"{NAME.replace(' ', '-')}-{version}-Manual.pdf", "application/pdf"),
    ]


def check_inputs(tag, version=__version__):
    """The files for `tag`, or exit when the tag is not v<version> or a file is missing."""
    if tag != f"v{version}":
        fail(f"tag {tag} does not match the version {version}: tag the commit v{version}")
    files = release_files(version)
    for path, _ in files:
        if not path.is_file():
            fail(f"{path.relative_to(ROOT)} is missing: run scripts/build.py and scripts/build_manual.py first")
    return files


def notes(version=__version__):
    """The CHANGELOG section of this version (Keep a Changelog)."""
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(rf"^## \[{re.escape(version)}\].*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match.group(1).strip() if match else ""


def body(files, version=__version__):
    sums = "\n".join(f"| `{path.name}` | `{hashlib.sha256(path.read_bytes()).hexdigest()}` |" for path, _ in files)
    return f"{notes(version)}\n\n| Arquivo | SHA-256 |\n| --- | --- |\n{sums}".strip()


def is_safe(url):
    """https, or http to this machine only: the token goes in every request."""
    parts = urllib.parse.urlsplit(url)
    return parts.scheme == "https" or (parts.scheme == "http" and parts.hostname in LOOPBACK)


class Api:
    """A JSON API with a token. Paths are relative to `base`; an absolute URL is used as it is."""

    def __init__(self, base, headers):
        self.base, self.headers = base.rstrip("/"), headers

    def __call__(self, method, path, payload=None, kind="application/json"):
        """(HTTP status, answer). A dict payload goes as JSON; bytes go as they are, with `kind`."""
        url = path if path.startswith(("https://", "http://")) else self.base + path
        data = payload if isinstance(payload, bytes) or payload is None else json.dumps(payload).encode()
        headers = {**self.headers, "User-Agent": USER_AGENT}
        if data:
            headers["Content-Type"] = kind
        request = urllib.request.Request(url, data, headers, method=method)  # noqa: S310 - is_safe() checked by main()
        try:
            with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
                return response.status, json.loads(response.read() or b"null")
        except urllib.error.HTTPError as error:
            return error.code, error.read(2000).decode("utf-8", "replace")


def forgejo(server, token):
    """Forgejo /api/v1 with an access token."""
    return Api(server.rstrip("/") + "/api/v1", {"Authorization": f"token {token}", "Accept": "application/json"})


def github(api, token):
    """GitHub REST API with the job's GITHUB_TOKEN."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    return Api(api, headers)
