


run_script = "pipenv run python scripts/build.py"

.PHONY: build


init:

	# Create a virtual env and install dependencies.

	$(info [INIT PROJECT FOR DEV])
	pipenv --python 3.6
	pipenv install --dev


build-wheel:

	# Build Python Wheel.

	$(info [BUILD])
	"$(run_script)" build-wheel


bump-git:

	# Run interactive git bump routine.

	$(info [BUMP GIT])
	"$(run_script)" bump-git


bump-version:

	# Run interactive version bump routine.

	$(info [BUMP VERSION NUMBER])
	"$(run_script)" bump-version


push-registry:

	# Push wheel to package registry.

	$(info [PUSH TO PACKAGE REGISTRY])
	"$(run_script)" push-registry


bump:

	# Run interactive bump routine.

	$(info [BUMP])
	"$(run_script)" bump



