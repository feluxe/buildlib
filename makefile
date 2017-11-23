run_script = "pipenv run python scripts/build.py"


buildbump:
	$(info [BUMP BUILD])
	"$(run_script)" bump-build

gitbump:
	$(info [BUMP GIT])
	"$(run_script)" bump-git

versionbump:
	$(info [BUMP VERSION NUMBER])
	"$(run_script)" bump-version

registrybump:
	$(info [BUMP PACKAGE REGISTRY])
	"$(run_script)" bump-registry

bump:
	$(info [BUMP])
	"$(run_script)" bump



