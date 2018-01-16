
.PHONY: run
.PHONY: build


help:
	# Print builder tool help text.
	pipenv run python -m builder --help

init:
	# Create a virtual env and install dependencies.
	$(info [INIT PROJECT FOR DEV])
	pipenv --python 3.6
	pipenv install --dev

%:
	# Arguments given to 'make' are passed through to the builder tool.
	pipenv run python -m builder $(filter-out "$@",$(MAKECMDGOALS))
