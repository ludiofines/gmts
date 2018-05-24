

all:
	@echo usage:
	@echo make activate: creates virtualenv and installs deps

activate:
	( \
		virtualenv -p /usr/bin/python3 . && \
		bash -c 'source $(PWD)/bin/activate' && \
		pip3 install -r $(PWD)/requirements.txt; \
	)

