run_script = "pipenv run python scripts/build.py"

.PHONY: build

init:
	$(info [INIT PROJECT FOR DEV])
	pipenv --python 3.6
	"$(run_script)" init

build-wheel:
	$(info [BUILD])
	"$(run_script)" build-wheel

bump-git:
	$(info [BUMP GIT])
	"$(run_script)" bump-git

bump-version:
	$(info [BUMP VERSION NUMBER])
	"$(run_script)" bump-version

push-registry:
	$(info [PUSH TO PACKAGE REGISTRY])
	"$(run_script)" push-registry

bump:
	$(info [BUMP])
	"$(run_script)" bump



