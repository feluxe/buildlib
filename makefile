run_script = "pipenv run python scripts/build.py"


bump-build:
	$(info [BUMP BUILD])
	"$(run_script)" bump-build

bump-git:
	$(info [BUMP GIT])
	"$(run_script)" bump-git

bump-version:
	$(info [BUMP VERSION NUMBER])
	"$(run_script)" bump-version

bump-registry:
	$(info [BUMP PACKAGE REGISTRY])
	"$(run_script)" bump-registry

bump:
	$(info [BUMP])
	"$(run_script)" bump



