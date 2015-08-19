#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json
import re
from datetime import datetime
from socket import gethostname
from subprocess import check_output

def main():
    # uptime$B%3%^%s%I$G(Bloadaverage$B$r3NG'(B
    uptime_output = check_output(['/usr/bin/uptime'])
    uptime_output = uptime_output.decode('utf8')
    uptime_list = filter(lambda w: len(w) > 0, re.split(r'\s| |,|\n', uptime_output))
    
    d = datetime.today()
    date_str = d.strftime("%Y-%m-%d %H:%M:%S")

    result = json.dumps({
        'hostname': gethostname(),
        'date': date_str,
        '1min-average': uptime_list[7],
        '5min-average': [8],
        '15min-average': load_average[9],
    })

    print('HTTP/1.1 200 OK')
    print('Content-Type: application/json')
    print('Content-Length: {}'.format(len(result) + 1))
    print()
    print(result)

if __name__ == '__main__':
    main()
