#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
from cloudspecs import data_file

type_ids = [
    'c3.2xlarge',
    'c3.4xlarge',
    'c3.8xlarge',
    'c3.large',
    'c3.xlarge',
    'c4.2xlarge',
    'c4.4xlarge',
    'c4.8xlarge',
    'c4.large',
    'c4.xlarge',
    'cc2.8xlarge',
    'cg1.4xlarge',
    'cr1.8xlarge',
    'd2.2xlarge',
    'd2.4xlarge',
    'd2.8xlarge',
    'd2.xlarge',
    'f1.16xlarge',
    'f1.2xlarge',
    'g2.2xlarge',
    'g2.8xlarge',
    'hi1.4xlarge',
    'hs1.8xlarge',
    'i2.2xlarge',
    'i2.4xlarge',
    'i2.8xlarge',
    'i2.xlarge',
    'm3.2xlarge',
    'm3.large',
    'm3.medium',
    'm3.xlarge',
    'm4.10xlarge',
    'm4.16xlarge',
    'm4.2xlarge',
    'm4.4xlarge',
    'm4.large',
    'm4.xlarge',
    'p2.16xlarge',
    'p2.8xlarge',
    'p2.xlarge',
    'r3.2xlarge',
    'r3.4xlarge',
    'r3.8xlarge',
    'r3.large',
    'r3.xlarge',
    'r4.16xlarge',
    'r4.2xlarge',
    'r4.4xlarge',
    'r4.8xlarge',
    'r4.large',
    'r4.xlarge',
    't2.2xlarge',
    't2.large',
    't2.medium',
    't2.micro',
    't2.nano',
    't2.small',
    't2.xlarge',
    'x1.16xlarge',
    'x1.32xlarge'
]

instance_details = {}

for instance_type in type_ids:
    data_file_path = 'aws/ec2/instances/{}.json'.format(instance_type)
    instance_details[instance_type] = json.load(data_file(data_file_path))
