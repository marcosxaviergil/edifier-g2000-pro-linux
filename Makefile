# Hecate G2000 PRO Volume: development tasks. The program itself needs only Python 3.11+.
PYTHON ?= python3
PY_SOURCES := src scripts tests

.PHONY: check tools lint test build manual clean

# Fast checks first: missing tools and lint fail in seconds, before the tests, the build and the manual.
check: tools lint test build manual

# Everything the checks, the build and the manual need, here and in the CI image (node:22-bookworm-slim
# plus the apt-get list of .forgejo/workflows/build.yaml). Lists what is missing instead of failing later.
tools:
	@missing=""; \
	for c in $(PYTHON) git dpkg-deb lintian fc-list; do command -v $$c >/dev/null 2>&1 || missing="$$missing $$c"; done; \
	$(PYTHON) -c 'import pyflakes' 2>/dev/null || missing="$$missing pyflakes(python3-pyflakes)"; \
	$(PYTHON) -c 'import weasyprint' 2>/dev/null || missing="$$missing weasyprint"; \
	command -v fc-list >/dev/null 2>&1 && { fc-list ':lang=ja' family | grep -q . || missing="$$missing fonts-noto-cjk"; }; \
	if [ -n "$$missing" ]; then echo "Missing commands/packages:$$missing"; exit 1; fi; echo "tools: OK"

lint:
	$(PYTHON) -m pyflakes $(PY_SOURCES)
	@if command -v ruff >/dev/null 2>&1; then ruff check . && ruff format --check .; \
	else echo "lint: ruff not installed, style rules in pyproject.toml NOT checked"; fi

test:
	$(PYTHON) -B -m unittest discover -s tests -v

build:
	$(PYTHON) -B scripts/build.py
	lintian --fail-on error,warning dist/*.deb

manual:
	$(PYTHON) -B scripts/build_manual.py

clean:
	rm -rf dist
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
