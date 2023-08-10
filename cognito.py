import boto3
import os

def lambda_handler(event, context):
    user_pool_id = 'us-west-2_your_pool'
    attribute_name = 'custom:user_id_test'
    attribute_name_role = 'custom:user_role'
    client = boto3.client('cognito-idp')

    paginator = client.get_paginator('list_users')
    response_iterator = paginator.paginate(UserPoolId=user_pool_id)

    for page in response_iterator:
        for user in page['Users']:
            username = user['Username']
            response = client.admin_get_user(UserPoolId=user_pool_id, Username=username)

            for attribute in response['UserAttributes']:
                if attribute['Name'] == 'custom:employee_id':
                    employee_id = attribute['Value']
                    client.admin_update_user_attributes(
                        UserPoolId=user_pool_id,
                        Username=username,
                        UserAttributes=[
                            {
                                'Name': attribute_name,
                                'Value': employee_id
                            },
                        ]
                    )
                if attribute['Name'] == 'custom:user_role':
                    user_role = attribute['Value']
                    client.admin_update_user_attributes(
                        UserPoolId=user_pool_id,
                        Username=username,
                        UserAttributes=[
                            {
                                'Name': attribute_name_role,
                                'Value': user_role
                            },
                        ]
                    )

    return {
        'statusCode': 200,
        'body': 'User attributes updated successfully.'
    }
