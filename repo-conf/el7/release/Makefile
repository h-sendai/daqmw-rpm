cwd = $(shell pwd)
dist = ".el7"

all:
	#@echo $(cwd)
	@rpmbuild --define "_topdir $(cwd)" --define "dist $(dist)" -bb SPECS/kek-daqmiddleware.spec
	@rpmbuild --define "_topdir $(cwd)" --define "dist $(dist)" -bs SPECS/kek-daqmiddleware.spec

clean:
	@rm -f RPMS/noarch/* SRPMS/*
	@rm -fr BUILD/*

