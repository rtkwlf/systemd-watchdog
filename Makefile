.PHONY: build clean help install pypi-deploy test uninstall wheel_check
.SILENT: help install pypi-deploy test uninstall wheel_check

define HELP

Targets:

  - build      - builds the 'wheel' distribution file (calls clean)
  - clean      - cleans temporary files
  - install    - builds and locally installs to your interpreter (calls uninstall and build)
  - uninstall  - removes locally installed copy
  - test       - runs unit tests

endef

export HELP
help:
	echo "$${HELP}"
	false

build: wheel_check clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build dist *.egg-info __pycache__

install: build uninstall
	pip3 install --user ./dist/*.whl

uninstall:
	-pip3 uninstall -y systemd_watchdog

test:
	./test_systemd_watchdog.py

pypi-deploy: build test ~/.pypirc
	twine upload --repository pypi dist/*

WHEEL_INSTALLED = $(shell pip3 list | egrep '^wheel\s')
wheel_check:
ifeq ($(WHEEL_INSTALLED),)
  $(error Need to 'pip3 install wheel')
endif
	true
