# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gtourdia <@student.42mulhouse.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#                                                      #+#    #+#              #
#    26/01/2026            Fly-in                     ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


# PROJECT CONFIGURATION
AUTHOR=gtourdia
PROJECT_NAME=Fly-In
PROJECT_START_DATE=2026-02-11
GITHUB=https://github.com/sousampere/

# COLORS
YELLOW=\033[0;33m
CYAN=\033[0;36m
GREEN=\033[0;32m
RESET=\033[0m

# MAIN VARIABLES
INTERPRETER			=	python3


install:
	@printf "\033[2J\033[H"
	@printf "$(YELLOW)╔════════════════════════════════════════════════════════════════╗\n"
	@printf "$(YELLOW)║                                                                ║\n"
	@printf "$(YELLOW)║  44  44    2222    $(GREEN)Made by $(AUTHOR) $(YELLOW)\n"
	@printf "$(YELLOW)║  44  44   22  22   Project: $(CYAN)$(PROJECT_NAME) $(YELLOW)\n"
	@printf "$(YELLOW)║  444444      22    Started in: $(CYAN)$(PROJECT_START_DATE) $(YELLOW)\n"
	@printf "$(YELLOW)║      44     22     Github: $(CYAN)$(GITHUB) $(YELLOW)\n"
	@printf "$(YELLOW)║      44   222222                                               ║\n"
	@printf "$(YELLOW)║                                                                ║\n"
	@printf "$(YELLOW)╚════════════════════════════════════════════════════════════════╝\n"
	@printf "\033[3;66H║"
	@printf "\033[4;66H║"
	@printf "\033[5;66H║"
	@printf "\033[6;66H║"
	@printf "\033[7;66H║"
	@printf "\033[8;66H║"
	@printf "\033[9;80H\n"
	@printf "$(CYAN)[Installation]$(RESET) ➡️  Synchronizing uv\n"
# 	uv sync

run:
	uv run python code/main.py

flake8: sync
	uv run python3.14 -m flake8 ./src

mypy: sync
	uv run python3.14 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

mypy-strict: sync
	uv run python3.14 -m mypy . --strict

lint: flake8 mypy

lint-strict: flake8 mypy-strict

debug:
# 	echo "debug needs to be run in the virtual env -> source .venv/bin/activate"
# 	python -m pdb -m src --input $(DEFAULT_INPUT) --output $(DEFAULT_OUTPUT)

tester:
# 	run tester

clean:
# 	rm -rf data/output
# 	rm -rf .venv
# 	rm -rf .mypy_cache
# 	rm -rf __pycache__
# 	rm -rf .pytest_cache
# 	rm -rf .llm
# 	rm -rf .uv_cache

re: clean install
# 	aaaa