# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gtourdia <gtourdia@student.42mulhouse.f    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: Invalid date        by                   #+#    #+#              #
#    Updated: 2026/03/27 22:47:19 by gtourdia         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


# PROJECT CONFIGURATION
AUTHOR=gtourdia
PROJECT_NAME=Fly-In
PROJECT_START_DATE=2026-02-11
GITHUB=https://github.com/sousampere/
INPUT=maps/easy/01_linear_path.txt


# COLORS
YELLOW=\033[0;33m
CYAN=\033[0;36m
GREEN=\033[0;32m
RESET=\033[0m

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
	uv run python main.py

runarg:
	uv run python main.py --input $(ARGS)

drun:
	clear && clear
	uv run python main.py

lint:
	uv run -m flake8 src main.py
	uv run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run -m flake8 src main.py
	uv run mypy src main.py --strict

debug:
	uv run python -m pdb main.py

lindt:
	@echo "🍫🍫 !!"
	uv run -m flake8 src main.py
	uv run mypy src main.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	rm -rf .venv
	rm -rf .mypy_cache
	rm -rf .vscode