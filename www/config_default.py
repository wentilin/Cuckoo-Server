#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

configs = {
    'debug': False,
    'server': {
        'host': '127.0.0.1',
        'port': 9000
    },
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'www-data',
        'password': 'www-data',
        'db': 'cuckoodb'
    },
    'session': {
        'secret': 'Coolblog'
    },
    'resource_path': '/home/ubuntu/cuckoo_server/resource'
}

if configs['debug']:
    configs['resource_path'] = '/Users/wentilin/Desktop/cuckoo_server/resource'
    configs['server']['host'] = '192.168.1.101'
    configs['server']['port'] = 9001
