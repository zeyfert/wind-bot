install:
	poetry install

lint:
	poetry run flake8 wind_bot

.PHONY: install lint
