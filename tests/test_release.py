"""forgejo_release.py and github_release.py against local stand-ins of the Forgejo and GitHub APIs.

The stand-ins answer only the requests documented in each script's docstring, with the status codes
given there, and refuse a request without the right Authorization header or with Python's default
User-Agent (as a Cloudflare in front of Forgejo does).
"""

import http.server
import json
import os
import re
import subprocess
import sys
import threading
import unittest
import urllib.parse

from support import ROOT

from hecate_volume import __version__

TAG = f"v{__version__}"
SCRIPTS = ROOT / "scripts"


class Forge(http.server.BaseHTTPRequestHandler):
    """Shared state lives on the server: releases, uploads, the tag's commit and the expected token."""

    def log_message(self, *args):
        pass

    def reply(self, status, payload=None):
        data = json.dumps(payload).encode() if payload is not None else b""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def body(self):
        return self.rfile.read(int(self.headers.get("Content-Length") or 0))

    def allowed(self):
        state = self.server.state
        if self.headers.get("User-Agent", "").startswith("Python-urllib"):
            self.reply(403, {"message": "error code: 1010"})
            return False
        if self.headers.get("Authorization") != state["auth"]:
            self.reply(401, {"message": "bad token"})
            return False
        state["log"].append((self.command, self.path))
        return True

    def do_GET(self):
        if self.allowed():
            self.route("GET")

    def do_POST(self):
        if self.allowed():
            self.route("POST")

    def do_DELETE(self):
        if self.allowed():
            self.route("DELETE")

    def do_PATCH(self):
        if self.allowed():
            self.route("PATCH")


class ForgejoApi(Forge):
    def route(self, method):
        state, path = self.server.state, urllib.parse.urlsplit(self.path).path
        base = "/api/v1/repos/owner/repo"
        if method == "GET" and path == f"{base}/tags/{TAG}":
            return self.reply(200, {"commit": {"sha": state["commit"]}})
        if method == "DELETE" and path == f"{base}/releases/tags/{TAG}":
            had = bool(state["releases"])
            state["releases"].clear()
            return self.reply(204 if had else 404)
        if method == "POST" and path == f"{base}/releases":
            release = {**json.loads(self.body()), "id": 7, "assets": []}
            state["releases"].append(release)
            return self.reply(201, release)
        match = re.fullmatch(rf"{base}/releases/7/assets", path)
        if method == "POST" and match:
            data = self.body()
            name = re.search(rb'name="attachment"; filename="([^"]+)"', data)[1].decode()
            state["releases"][0]["assets"].append(name)
            return self.reply(201, {"browser_download_url": f"http://x/{name}"})
        return self.reply(404, {"message": f"no route {method} {path}"})


class GitHubApi(Forge):
    def route(self, method):
        state, path = self.server.state, urllib.parse.urlsplit(self.path).path
        base = "/repos/owner/repo"
        if method == "GET" and path == f"{base}/git/ref/tags/{TAG}":
            return self.reply(200, {"object": {"type": "tag", "sha": "t1"}})
        if method == "GET" and path == f"{base}/git/tags/t1":
            return self.reply(200, {"object": {"type": "commit", "sha": state["commit"]}})
        if method == "GET" and path == f"{base}/releases":
            return self.reply(200, state["releases"])
        if method == "DELETE" and path.startswith(f"{base}/releases/"):
            state["releases"] = [r for r in state["releases"] if str(r["id"]) != path.rsplit("/", 1)[1]]
            return self.reply(204)
        if method == "POST" and path == f"{base}/releases":
            port = self.server.server_address[1]
            release = {**json.loads(self.body()), "id": 9, "assets": []}
            release["upload_url"] = f"http://127.0.0.1:{port}/uploads/9/assets{{?name,label}}"
            state["releases"].append(release)
            return self.reply(201, release)
        if method == "POST" and path == "/uploads/9/assets":
            release = next(r for r in state["releases"] if r["id"] == 9)
            if not release["draft"]:
                return self.reply(422, {"message": "immutable: cannot add assets to a published release"})
            name = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)["name"][0]
            release["assets"].append((name, self.headers["Content-Type"], len(self.body())))
            return self.reply(201, {"browser_download_url": f"http://x/{name}"})
        if method == "PATCH" and path == f"{base}/releases/9":
            release = next(r for r in state["releases"] if r["id"] == 9)
            release.update(json.loads(self.body()))
            return self.reply(200, release)
        return self.reply(404, {"message": f"no route {method} {path}"})


class Release(unittest.TestCase):
    def setUp(self):
        dist = ROOT / "dist"
        dist.mkdir(exist_ok=True)
        self.created = []
        for name in (f"hecate-g2000-pro-volume_{__version__}_all.deb", f"hecate-g2000-pro-volume-{__version__}.tar.gz",
                     f"Hecate-G2000-PRO-Volume-{__version__}-Manual.pdf"):  # fmt: skip
            path = dist / name
            if not path.exists():
                path.write_bytes(b"test data " + name.encode())
                self.created.append(path)
        self.addCleanup(lambda: [path.unlink() for path in self.created])

    def serve(self, handler, auth, releases=()):
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        server.state = {"auth": auth, "releases": list(releases), "commit": "c0ffee", "log": []}
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server

    def run_script(self, script, env):
        environment = {key: value for key, value in os.environ.items() if not key.startswith(("GITHUB_", "FORGEJO_"))}
        environment.update(env)
        return subprocess.run([sys.executable, "-B", SCRIPTS / script], env=environment, capture_output=True, text=True)

    def forgejo_env(self, server, **extra):
        url = f"http://127.0.0.1:{server.server_address[1]}"
        return {"GITHUB_SERVER_URL": url, "GITHUB_REPOSITORY": "owner/repo", "GITHUB_REF_NAME": TAG,
                "FORGEJO_TOKEN": "secret-token", **extra}  # fmt: skip

    def github_env(self, server, **extra):
        url = f"http://127.0.0.1:{server.server_address[1]}"
        return {"GITHUB_API_URL": url, "GITHUB_REPOSITORY": "owner/repo", "GITHUB_REF_NAME": TAG,
                "GITHUB_TOKEN": "secret-token", **extra}  # fmt: skip

    def test_forgejo_replaces_the_release_and_attaches_every_file(self):
        server = self.serve(ForgejoApi, "token secret-token", releases=[{"id": 1}])
        result = self.run_script("forgejo_release.py", self.forgejo_env(server, BUILD_COMMIT="c0ffee"))
        self.assertEqual(result.returncode, 0, result.stderr)
        release = server.state["releases"][0]
        self.assertEqual(len(release["assets"]), 3)
        self.assertIn("| Arquivo | SHA-256 |", release["body"])
        self.assertIn("Earlier", result.stdout)
        self.assertNotIn("secret-token", result.stdout + result.stderr)

    def test_forgejo_does_not_publish_when_the_tag_moved(self):
        server = self.serve(ForgejoApi, "token secret-token")
        result = self.run_script("forgejo_release.py", self.forgejo_env(server, BUILD_COMMIT="old"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(server.state["releases"], [])
        self.assertIn("Nothing published", result.stdout)

    def test_github_drafts_attaches_then_publishes(self):
        earlier = [{"id": 3, "tag_name": TAG, "draft": True}, {"id": 4, "tag_name": "v0.9.0", "draft": False}]
        server = self.serve(GitHubApi, "Bearer secret-token", releases=earlier)
        result = self.run_script("github_release.py", self.github_env(server, BUILD_COMMIT="c0ffee"))
        self.assertEqual(result.returncode, 0, result.stderr)
        ids = sorted(release["id"] for release in server.state["releases"])
        self.assertEqual(ids, [4, 9], "the earlier draft of this tag goes, other versions stay")
        published = next(r for r in server.state["releases"] if r["id"] == 9)
        self.assertFalse(published["draft"])
        kinds = {name: kind for name, kind, _ in published["assets"]}
        deb = f"hecate-g2000-pro-volume_{__version__}_all.deb"
        self.assertEqual(kinds[deb], "application/vnd.debian.binary-package")
        self.assertEqual(len(kinds), 3)

    def test_wrong_tag_missing_token_and_plain_http_are_refused_before_any_request(self):
        server = self.serve(GitHubApi, "Bearer secret-token")
        cases = {
            "wrong tag": self.github_env(server, GITHUB_REF_NAME="v0.0.1"),
            "no token": {**self.github_env(server), "GITHUB_TOKEN": ""},
            "plain http": self.github_env(server, GITHUB_API_URL="http://example.com"),
        }
        for name, env in cases.items():
            with self.subTest(case=name):
                result = self.run_script("github_release.py", env)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(result.stderr.startswith("release: "), result.stderr)
        self.assertEqual(server.state["log"], [])

    def test_missing_file_is_refused(self):
        for path in self.created:
            path.unlink()
        self.created = []
        if (ROOT / "dist" / f"Hecate-G2000-PRO-Volume-{__version__}-Manual.pdf").exists():
            self.skipTest("a real manual is in dist/")
        server = self.serve(ForgejoApi, "token secret-token")
        result = self.run_script("forgejo_release.py", self.forgejo_env(server))
        self.assertIn("is missing", result.stderr)
        self.assertEqual(server.state["log"], [])


if __name__ == "__main__":
    unittest.main()
