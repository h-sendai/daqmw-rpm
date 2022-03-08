cwd = $(shell pwd)
dist = ".el7"

SPEC_EXT = -testing3
SPECFILE = kek-daqmiddleware$(SPEC_EXT).spec

all:
	#@echo $(cwd)
	@rpmbuild --define "_topdir $(cwd)" --define "dist $(dist)" -bb SPECS/$(SPECFILE)
	@rpmbuild --define "_topdir $(cwd)" --define "dist $(dist)" -bs SPECS/$(SPECFILE)

clean:
	@rm -f RPMS/noarch/* SRPMS/*
	@rm -fr BUILD/*

setupdir:
	@mkdir BUILD BUILDROOT RPMS SOURCES SPECS SRPMS
