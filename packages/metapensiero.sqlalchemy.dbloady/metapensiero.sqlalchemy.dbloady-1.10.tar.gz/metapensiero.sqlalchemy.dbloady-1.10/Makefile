# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- YAML based data loader
# :Created:   ven  1 gen 2016, 16.19.54, CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2016 Lele Gaifax
#

all: help

help::
	@printf "Development targets\n"
	@printf "===================\n\n"

help::
	@printf "test\n\tRun basic functional test (needs PostgreSQL)\n"

.PHONY: test
test:
	$(MAKE) -C tests/adaptor test
	$(MAKE) -C tests/fields test
	$(MAKE) -C tests/hstore test
	$(MAKE) -C tests/preload test
	$(MAKE) -C tests/dump test
	$(MAKE) -C tests/generic_fk test
	$(MAKE) -C tests/non_rel_attrs test
	$(MAKE) -C tests/json test
	$(MAKE) -C tests/composite_pk test
	$(MAKE) -C tests/raw_sql test

.PHONY: clean
clean:
	$(MAKE) -C tests/adaptor clean
	$(MAKE) -C tests/fields clean
	$(MAKE) -C tests/hstore clean
	$(MAKE) -C tests/preload clean
	$(MAKE) -C tests/dump realclean
	$(MAKE) -C tests/generic_fk clean
	$(MAKE) -C tests/non_rel_attrs clean
	$(MAKE) -C tests/json clean
	$(MAKE) -C tests/composite_pk clean
	$(MAKE) -C tests/raw_sql clean

include Makefile.release
