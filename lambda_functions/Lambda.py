import boto3
import json
import os

# Initialize clients
s3_client = boto3.client('s3')
sf_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    # Config S3 location
    bucket_name = 'sr-spot-csi'
    config_key = 'code1/SRS_Step_Config_PREPROD.json'
    
    # Step Function ARN
    state_machine_arn = 'arn:aws:states:eu-west-1:040479514560:stateMachine:samplespot'

    # Read config file from S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=config_key)
        config_data = response['Body'].read().decode('utf-8')
        config_json = json.loads(config_data)
    except Exception as e:
        print(f"Error reading config file: {e}")
        raise e

    # Start Step Function execution
    try:
        response = sf_client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(config_json)
        )
        print(f"Execution started successfully: {response['executionArn']}")
    except Exception as e:
        print(f"Error starting Step Function execution: {e}")
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Step Function Execution started successfully.')
    }
