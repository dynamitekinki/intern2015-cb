#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json
import re
from socket import gethostname
from subprocess import check_output


MEM_INFO_PATTERN = re.compile('^([^ ]+): *([0-9]+) ?([A-Za-z]+)?$')


def main():
    mem_info_output = check_output(['/bin/cat', '/proc/meminfo'])

    for line in mem_info_output.splitlines():
        m = MEM_INFO_PATTERN.match(line.decode('utf8'))
        if m.group(1) == 'MemFree':
            unit = m.group(3)
            scale = 1
            if unit == 'kB':
                scale = 1024
            else:
                raise ValueError('Unknown unit: ' + unit)
            mem_free = int(m.group(2)) * scale

    result = json.dumps({
        'hostname': gethostname(),
        'memfree': mem_free
    })

    print('HTTP/1.1 200 OK')
    print('Content-Type: application/json')
    print('Content-Length: {}'.format(len(result) + 1))
    print()
    print(result)


if __name__ == '__main__':
    main()
