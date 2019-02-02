#!/usr/bin/env bash

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
venv_root="${HOME}/.virtualenvs/artslob-bot"

cd "$project_root"

if [[ ! -e "$venv_root" ]]; then
    python3 -m venv "$venv_root"
fi

source "${venv_root}/bin/activate"
python3 -m pip install -r requirements.txt
python3 bot.py

