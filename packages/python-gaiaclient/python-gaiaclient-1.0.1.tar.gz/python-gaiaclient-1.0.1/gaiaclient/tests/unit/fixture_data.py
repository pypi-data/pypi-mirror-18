
fixtures = {
    '/v1/servers/': {
        'POST': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                'server':
                {
                    'id': '1',
                    'name': 'server1',
                    'description': 'desc',
                    'status': 'Active',
                    'created_at': '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            },
        ),
    },
    '/v1/servers/?sort_dir=desc&sort_key=name': {
        'GET': (
            {'X-Dc-Id': '1234'},
            {'servers': [
                {
                    'id': '1',
                    'name': 'server1-1',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': '2',
                    'name': 'server2',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/servers/?sort_dir=asc': {
        'GET': (
            {'X-Dc-Id': '1234'},
            {'servers': [
                {
                    'id': '1',
                    'name': 'server1-1',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': '2',
                    'name': 'server2',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/servers/1': {
        'GET': (
            {},
            {
                'server': {
                    'id': '1',
                    'name': 'dc-1',
                    'description': 'desc',
                    'status': 'Active',
                    'created_at' : '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            }
        ),
        'PUT': (
            {},
            {
                'server': {
                    'id': '1',
                    'name': 'dc-1',
                    'description': 'desc',
                    'status': 'Active',
                    'created_at' : '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            }
        ),
        'DELETE': ({}, None),
    },
    '/v1/servers/1/start': {
        'POST': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                'status': 'ok'
            },
        ),
    },
    '/v1/servers/1/stop': {
        'POST': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                'status': 'ok'
            },
        ),
    },
    '/v1/servers/1/interfaces': {
        'GET': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {'server-interfaces':
                [
                    {
                        "port_state": "ACTIVE",
                        "port_id": "1",
                        "fixed_ips": [
                            {
                                "subnet_id": "1",
                                "ip_address": "1.1.1.1"
                            }
                        ],
                        "net_id": "1",
                        "mac_addr": "fa:16:3e:cb:2d:c4"
                    }
                ]
            },
        ),
        'POST': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {'server-interface':
                {
                    "port_state": "ACTIVE",
                    "port_id": "1",
                    "fixed_ips": [
                        {
                            "subnet_id": "1",
                            "ip_address": "1.1.1.1"
                        }
                    ],
                    "net_id": "1",
                    "mac_addr": "fa:16:3e:cb:2d:c4"
                }
            },
        ),
    },
    '/v1/servers/1/interfaces/1': {
        'DELETE': (
            {}, {}
        )
    },
    '/v1/servers/1/volumes': {
        'GET': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {'server-volumes':
                [
                    {
                        "volume_id": "1",
                        "device": "/dev/vdc"
                    },
                    {
                        "volume_id": "2",
                        "device": "/dev/vdc"
                    }
                ]
            },
        ),
        'POST': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                "server-volume":
                    {
                        "volume_id": "1",
                        "device": "/dev/vdc"
                    }

            }
        ),
    },
    '/v1/servers/1/volumes/1': {
        'DELETE': ({}, {})
    },
    '/v1/servers/1/reboot?type=SOFT': {
        'POST': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                'status': 'ok'
            },
        ),
    },
    '/v1/servers/1/reboot?type=HARD': {
        'POST': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                'status': 'ok'
            },
        ),
    },
    '/v1/servers/1/console?type=NOVNC': {
        'POST': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                'console':
                    {
                        'type': 'novnc',
                        'url': 'http://0.0.0.0/vnc'
                    }
            },
        ),
    },
    '/v1/dcs/': {
        'GET': (
            {},
            {'dcs': [
                {
                    'id': 'a',
                    'name': 'dc1',
                    'status': 'Active',
                },
                {
                    'id': 'b',
                    'name': 'dc2',
                    'status': 'Active',
                },
            ]},
        ),
    },
    '/v1/images/?name=i1': {
        'GET': (
            {},
            {'images': [
                {
                    'id': 'i1',
                    'name': 'image1',
                    'status': 'Active',
                    'size': 1024
                }
            ]},
        ),
    },
    '/v1/images/?sort_dir=asc&sort_key=name': {
        'GET': (
            {},
            {'images': [
                {
                    'id': 'i1',
                    'name': 'image1',
                    'status': 'Active',
                    'size': 1024
                }
            ]},
        ),
    },
    '/v1/images/?sort_dir=asc&sort_key=name&visibility=public':{
        'GET': (
            {},
            {'images': [
                {
                    'id': 'i1',
                    'name': 'image1',
                    'status': 'Active',
                    'size': 1024
                }
            ]},
        ),
    },
    '/v1/flavors/1': {
        'GET': (
            {},
            {
                'flavor':
                    {
                        'id': '1',
                        'name': 'flavor1'
                    }
            }
        )
    },
    '/v1/flavors/': {
        'GET': (
            {},
            {
                'flavors':
                    [{
                        'id': '1',
                        'name': 'flavor1'
                    }]
            }
        ),
        'POST': (
            {},
            {
                'flavor':
                    {
                        'id': '1',
                        'name': 'flavor1'
                    }
            }
        )
    },
    '/v1/volumes/?sort_key=name': {
        'GET': (
            {},
            {
                'volumes':
                    [{
                        'id': 'v1',
                        'name': 'volume1',
                        'attachments': ['s1', 's2']
                    }]
            }
        )
    },
    '/v1/volumes/?sort_dir=asc': {
        'GET': (
            {},
            {
                'volumes':
                    [{
                        'id': 'v1',
                        'name': 'volume1',
                        'attachments': ['s1', 's2']
                    }]
            }
        )
    },
    '/v1/volumes/': {
        'POST': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                'volume':
                    {
                        'id': '1',
                        'name': 'volume1',
                        'metadata': {
                            'readonly': True
                        }
                    }
            }
        )
    },
    '/v1/volumes/1': {
        'GET': (
            {},
            {
                'volume':
                    {
                        'id': '1',
                        'name': 'volume1',
                        'metadata': {
                            'readonly': True
                        }
                    }
            }
        ),
        'PUT': (
            {},
            {
                'volume':
                    {
                        'id': '1',
                        'name': 'volume2',
                    }
            }
        ),
        'DELETE': ({}, None),
    },
    '/v1/networks/?sort_dir=asc': {
        'GET': (
            {},
            {
                'networks':
                    [{
                        'id': 'n1',
                        'name': 'nentwork1'
                    }]
            }
        )
    },
    '/v1/networks/': {
        'GET': (
            {},
            {
                'networks':
                    [{
                        'id': 'n1',
                        'name': 'nentwork1'
                    }]
            }
        )
    },
    '/v1/subnets/': {
        'GET': (
            {},
            {
                'subnets':
                    [{
                        'id': '1',
                        'name': 'subnet1'
                    }]
            }
        )
    },
    '/': {
        'GET': (
            {},
            {"versions": [
                {
                    "status": "EXPERIMENTAL",
                    "id": "v3.0",
                    "links": [
                        {
                            "href": "http://10.229.45.145:9292/v3/",
                            "rel": "self"
                        }
                    ]
                },
                {
                    "status": "CURRENT",
                    "id": "v2.3",
                    "links": [
                        {
                            "href": "http://10.229.45.145:9292/v2/",
                            "rel": "self"
                        }
                    ]
                },
                {
                    "status": "SUPPORTED",
                    "id": "v1.0",
                    "links": [
                        {
                            "href": "http://10.229.45.145:9292/v1/",
                            "rel": "self"
                        }
                    ]
                }
            ]}
        )
    },
    '/v1/usages/': {
        'GET': (
            {},
            {
                "usages": {
                    "metadata_items": {
                        "quota": 128
                    },
                    "injected_file_content_bytes": {
                        "quota": 10240
                    },
                    "gigabytes_ZTE-CLOVE": {
                        "available": 'Infinity',
                        "quota": 'Infinity'
                    },
                    "volumes": {
                        "available": 7,
                        "used": 25,
                        "quota": 32
                    },
                    "gigabytes": {
                        "available": 1200,
                        "used": 1900,
                        "quota": 3100
                    },
                    "fixed_ips": {
                        "available": 'Infinity',
                        "quota": 'Infinity'
                    },
                    "ram": {
                        "available": 4096,
                        "used": 61440,
                        "quota": 65536
                    },
                    "floating_ips": {
                        "available": 9,
                        "used": 1,
                        "quota": 10
                    },
                    "key_pairs": {
                        "quota": 100
                    },
                    "instances": {
                        "available": 3,
                        "used": 9,
                        "quota": 12
                    },
                    "snapshots_ZTE-CLOVE": {
                        "available": 'Infinity',
                        "quota": 'Infinity'
                    },
                    "security_group_rules": {
                        "quota": 20
                    },
                    "snapshots_Test": {
                        "available": 'Infinity',
                        "quota": 'Infinity'
                    },
                    "snapshots": {
                        "available": 28,
                        "used": 4,
                        "quota": 32
                    },
                    "volumes_ZTE-CLOVE": {
                        "available": 'Infinity',
                        "quota": 'Infinity'
                    },
                    "injected_files": {
                        "quota": 12
                    },
                    "gigabytes_Test": {
                        "quota": 0
                    },
                    "cores": {
                        "available": 4,
                        "used": 24,
                        "quota": 28
                    },
                    "volumes_Test": {
                        "quota": 0
                    },
                    "injected_file_path_bytes": {
                        "quota": 255
                    },
                    "security_groups": {
                        "quota": 10
                    }
                }
            }

        )
    }
}
