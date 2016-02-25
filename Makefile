.PHONY: prod test prep
SHELL := /bin/bash

export ANSIBLE_NOCOWS = 1

prod: export ENVTYPE=prod
prod:
	ansible-playbook -i hosts cloudformation.yaml -v

prep:
	pip install -r requirements.txt

test:
	py.test --cov-report html --cov=reds tests/
