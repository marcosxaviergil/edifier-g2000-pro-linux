"""Publish the built packages and the manual as the GitHub release of the pushed version tag (Actions step).

The GitHub counterpart of forgejo_release.py, with the same rules (see forge.py). The release is created
as a draft, gets its files and is published last: with immutable releases on, GitHub refuses files
added after publishing, and a run that fails halfway leaves a draft instead of a public release
without its files. The next run of the same version deletes that draft.

API (GitHub REST, docs.github.com/rest: releases, release assets, git references, git tags):
GET /repos/{owner}/{repo}/git/ref/tags/{tag} (object: the commit, or an annotated tag that
GET /repos/{owner}/{repo}/git/tags/{sha} follows to its commit), GET /repos/{owner}/{repo}/releases
(drafts are listed for a token that can push), DELETE /repos/{owner}/{repo}/releases/{id} (204),
POST /repos/{owner}/{repo}/releases (201), POST to the release's upload_url with ?name= and the raw
file as the body (201), PATCH /repos/{owner}/{repo}/releases/{id} (200).
Auth: the job's GITHUB_TOKEN, which the workflow passes in env with `permissions: contents: write`.

    python3 -B scripts/github_release.py   # env: GITHUB_API_URL, GITHUB_REPOSITORY, GITHUB_REF_NAME, GITHUB_TOKEN
"""

import os
import urllib.parse

from forge import NAME, __version__, body, check_inputs, fail, github, is_safe


def tag_commit(request, base, tag):
    """The commit a tag points to; an annotated tag (git tag -a) is followed to its commit."""
    status, answer = request("GET", f"{base}/git/ref/tags/{urllib.parse.quote(tag)}")
    target = answer.get("object") if status == 200 else None
    if target and target.get("type") == "tag":
        status, answer = request("GET", f"{base}/git/tags/{urllib.parse.quote(str(target.get('sha')))}")
        target = answer.get("object") if status == 200 else None
    if not target or target.get("type") != "commit":
        fail(f"could not read the commit of the {tag} tag (HTTP {status}): {answer}")
    return target.get("sha")


def main():
    env = os.environ
    token, api = env.get("GITHUB_TOKEN"), env.get("GITHUB_API_URL")
    repository, tag = env.get("GITHUB_REPOSITORY"), env.get("GITHUB_REF_NAME")
    if not (token and api and repository and tag):
        fail("run it in GitHub Actions with GITHUB_TOKEN in env: token, API URL, repository or tag is missing")
    if not is_safe(api):
        fail("GITHUB_API_URL must be https (http only for localhost)")
    files = check_inputs(tag)
    request = github(api, token)
    base = f"/repos/{repository}"

    # A tag moved to a newer commit starts a newer build: an older run that ends later never replaces it.
    built = env.get("BUILD_COMMIT")
    if built and tag_commit(request, base, tag) != built:
        print(f"{tag} now points to another commit; its own run publishes the release. Nothing published here.")
        return

    # Only the first page is read (up to 100 releases).
    status, releases = request("GET", f"{base}/releases?per_page=100")
    if status != 200:
        fail(f"could not list the releases (HTTP {status}): {releases}")
    earlier = [old for old in releases if old.get("tag_name") == tag]
    for old in earlier:
        status, answer = request("DELETE", f"{base}/releases/{old['id']}")
        if status not in (204, 404):
            fail(f"could not delete the earlier {tag} release (HTTP {status}): {answer}")
        print(f"Earlier {tag} {'draft' if old.get('draft') else 'release'} deleted.")
    if not earlier:
        print(f"No earlier {tag} release.")

    draft = {"tag_name": tag, "name": f"{NAME} {__version__}", "body": body(files), "draft": True, "prerelease": False}
    status, release = request("POST", f"{base}/releases", draft)
    if status != 201:
        fail(f"could not create the {tag} draft (HTTP {status}): {release}")
    upload = str(release.get("upload_url") or "").split("{", 1)[0]  # hypermedia template: ...assets{?name,label}
    if not is_safe(upload):
        fail(f"the upload URL of the {tag} draft must be https (http only for localhost)")
    for path, kind in files:
        name = urllib.parse.quote(path.name)
        status, asset = request("POST", f"{upload}?name={name}", path.read_bytes(), kind)
        if status != 201:
            fail(f"could not attach {path.name} (HTTP {status}): {asset}. The draft stays until the next run.")
        print(f"File: {asset.get('browser_download_url', path.name)}")
    status, answer = request("PATCH", f"{base}/releases/{release['id']}", {"draft": False})
    if status != 200:
        fail(f"could not publish the {tag} draft (HTTP {status}): {answer}")
    print(f"Release {tag}: {answer.get('html_url', '')}")


if __name__ == "__main__":
    main()
