# -*- coding: utf-8 -*-
import boto3


def get_parameters(param_key):
    ssm = boto3.client('ssm', region_name='ap-northeast-1')
    response = ssm.get_parameters(
        Names=[
            param_key,
        ],
        WithDecryption=True
    )
    return response['Parameters'][0]['Value']
