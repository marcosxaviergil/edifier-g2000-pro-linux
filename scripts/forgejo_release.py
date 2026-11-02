"""Publish the built packages and the manual as the Forgejo release of the pushed version tag (Actions step).

Same version again: the earlier release of that tag and its files are deleted first, so only the
newest build remains; the git tag itself is kept. The files must already be in dist/ (scripts/build.py,
scripts/build_manual.py). With BUILD_COMMIT (the commit the run built), nothing is published when the
tag already points elsewhere: a moved tag never gets an older build.

API (Forgejo /api/v1; paths from the Forgejo release docs and the Gitea 1.21 spec Forgejo forked):
DELETE /repos/{owner}/{repo}/releases/tags/{tag} (204, or 404 when there is none),
POST /repos/{owner}/{repo}/releases (201), POST .../releases/{id}/assets, multipart field "attachment",
GET /repos/{owner}/{repo}/tags/{tag} (commit.sha: the commit the tag points to).
Auth: the job's automatic token (FORGEJO_TOKEN or GITHUB_TOKEN), which can write to its own repository.

    python3 -B scripts/forgejo_release.py   # env: GITHUB_SERVER_URL, GITHUB_REPOSITORY, GITHUB_REF_NAME, FORGEJO_TOKEN
"""

import os
import secrets
import urllib.parse

from forge import NAME, __version__, body, check_inputs, fail, forgejo, is_safe


def multipart(name, data, kind):
    boundary = secrets.token_hex(16)
    head = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="attachment"; filename="{name}"\r\n'
        f"Content-Type: {kind}\r\n\r\n"
    )
    return head.encode() + data + f"\r\n--{boundary}--\r\n".encode(), f"multipart/form-data; boundary={boundary}"


def main():
    env = os.environ
    token = env.get("FORGEJO_TOKEN") or env.get("GITHUB_TOKEN")
    server, repository, tag = env.get("GITHUB_SERVER_URL"), env.get("GITHUB_REPOSITORY"), env.get("GITHUB_REF_NAME")
    if not (token and server and repository and tag):
        fail("run it in Forgejo Actions: token, server, repository or tag is missing")
    if not is_safe(server):
        fail("GITHUB_SERVER_URL must be https (http only for localhost)")
    files = check_inputs(tag)
    request = forgejo(server, token)
    base = f"/repos/{repository}"
    api = f"{base}/releases"

    # A tag moved to a newer commit starts a newer build: an older run that ends later never replaces it.
    built = env.get("BUILD_COMMIT")
    if built:
        status, answer = request("GET", f"{base}/tags/{urllib.parse.quote(tag)}")
        if status != 200:
            fail(f"could not read the {tag} tag (HTTP {status}): {answer}")
        if (answer.get("commit") or {}).get("sha") != built:
            print(f"{tag} now points to another commit; its own run publishes the release. Nothing published here.")
            return

    status, answer = request("DELETE", f"{api}/tags/{urllib.parse.quote(tag)}")
    if status not in (204, 404):
        fail(f"could not delete the earlier {tag} release (HTTP {status}): {answer}")
    print(f"Earlier {tag} release deleted." if status == 204 else f"No earlier {tag} release.")

    release = {"tag_name": tag, "name": f"{NAME} {__version__}", "body": body(files), "draft": False}
    status, answer = request("POST", api, release)
    if status != 201:
        fail(f"could not create the {tag} release (HTTP {status}): {answer}")
    print(f"Release {tag}: {answer.get('html_url', '')}")
    for path, kind in files:
        upload, form = multipart(path.name, path.read_bytes(), kind)
        name = urllib.parse.quote(path.name)
        status, asset = request("POST", f"{api}/{answer['id']}/assets?name={name}", upload, form)
        if status != 201:
            fail(f"could not attach {path.name} (HTTP {status}): {asset}")
        print(f"File: {asset.get('browser_download_url', path.name)}")


if __name__ == "__main__":
    main()
