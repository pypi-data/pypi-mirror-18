psqlparse
=========
[![Build Status](https://travis-ci.org/alculquicondor/psqlparse.svg?branch=master)](https://travis-ci.org/alculquicondor/psqlparse)

This Python module  uses the [libpg\_query](https://github.com/lfittl/libpg_query) to parse SQL
queries and return the internal PostgreSQL parsetree.

Installation
------------

```shell
pip install psqlparse
```

Usage
-----

```python
import psqlparse
psqlparse.parse('SELECT * from mytable')
```

Contributors
------------

- [Aldo Culquicondor](https://github.com/alculquicondor/)
