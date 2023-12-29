.SILENT: install test lint format

install:
	python -m pip install --upgrade pip
	pip install poetry
	poetry config virtualenvs.in-project true
	poetry config virtualenvs.prefer-active-python true 
	poetry install --no-root

test:
	poetry run python test_PDDL.py
	poetry run python test_planner.py
	poetry run python action.py
	poetry run python PDDL.py    examples/dinner/dinner.pddl examples/dinner/pb1.pddl
	poetry run python planner.py examples/dinner/dinner.pddl examples/dinner/pb1.pddl
	poetry run python planner.py examples/airport/airport.pddl examples/airport/pb1.pddl

lint:
	poetry run flake8 --max-line-length=120 --max-complexity=10 

format:
	poetry run yapf --in-place --recursive --style pep8 *.py

run:
	poetry run python planner.py
	
all: install lint test