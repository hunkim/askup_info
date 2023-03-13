VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

ifneq ("$(wildcard .env)","")
include .env
export
endif

export PYTHONPATH := $(PYTHONPATH):./jobs/


# Need to use python 3.9 for aws lambda
$(VENV)/bin/activate: requirements.txt
	python3.9 -m venv $(VENV)
	$(PIP) install -r requirements.txt

$(VENV_DEV)/bin/activate: requirements.dev.txt
	python3.9 -m venv $(VENV_DEV)
	$(PIP_DEV) install -r requirements.dev.txt

main: news weather

news: $(VENV)/bin/activate
	$(PYTHON) jobs/news.py > news.txt

weather: $(VENV)/bin/activate
	$(PYTHON) jobs/weather.py > weather.txt

gpt: $(VENV)/bin/activate
	$(PYTHON) jobs/chatgpt.py