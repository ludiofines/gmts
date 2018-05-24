
.PHONY: all
all:
	@echo usage:
	@echo make activate: creates virtualenv and installs deps

.PHONY: activate
activate:
	( \
		virtualenv -p /usr/bin/python3 . && \
		bash -c 'source $(PWD)/bin/activate' && \
		bin/pip3 install -r $(PWD)/requirements.txt; \
	)

.PHONY: clean
clean:
	@rm -fr bin/
	@rm -fr include/
	@rm -rf share/
	@rm -rf lib/
