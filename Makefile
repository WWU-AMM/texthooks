PKG_VERSION=$(shell grep '^version' setup.cfg | cut -d '=' -f2 | tr -d ' ')

.PHONY: lint test release showvars
lint:
	tox -e lint
test:
	tox
showvars:
	@echo "PKG_VERSION=$(PKG_VERSION)"
release:
	git tag -s "$(PKG_VERSION)" -m "v$(PKG_VERSION)"
	-git push $(shell git rev-parse --abbrev-ref @{push} | cut -d '/' -f1) refs/tags/$(PKG_VERSION)
	tox -e publish-release

.PHONY: clean
clean:
	rm -rf dist build *.egg-info .tox .venv
	find . -name '*.pyc' -delete
	find . -name "__pycache__" -type d -exec rm -rf '{}' +
