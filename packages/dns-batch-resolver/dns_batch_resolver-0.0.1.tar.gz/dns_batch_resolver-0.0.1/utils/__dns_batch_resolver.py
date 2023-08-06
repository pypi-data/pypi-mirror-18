#!/usr/bin/env python

from sys import argv, stderr
from dns_batch_resolver import cleanup, resolv, query

if argv[1] == '--cleanup':
    print('cleanup') >> stderr
    cleanup()
elif argv[1] == '--resolv':
    print('resolv') >> stderr
    resolv()
elif argv[1] == '--query':
    print('query') >> stderr
    query()
else:
    raise ValueError(argv, message='Unknown args')
