from __future__ import print_function

import base64
import json
import logging
import _pickle as cPickle
from datetime import datetime
import decimal
import uuid
import boto3
from copy import deepcopy
import time
import ast

s3_client = boto3.client('s3')
s3_bucket = "videostreambucket"
rekog_client = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

dynamodb = boto3.resource('dynamodb')
ddb_table = dynamodb.Table("EnrichedFrame")

# SNS Configuration
sns_client = boto3.client('sns')
label_watch_sns_topic_arn = "###############################" 


endpointArnList = []
label_watch_sns_topic_arn = ""


def getEndPointsArn():
    
    endpoint_list = []
    
    access_key_id='####################'
    secret_access_key= '########################################' 
    regionname='us-east-1'
    
    client = boto3.client('sns', aws_access_key_id = access_key_id, 
            aws_secret_access_key = secret_access_key, 
            region_name = regionname)
            
    
    response = client.list_endpoints_by_platform_application(
            PlatformApplicationArn='##########################'
    )
    
    for endpoints in response['Endpoints']:
        endpoint_list.append(endpoints['EndpointArn'])
    
    return endpoint_list


def process_image(event,context):
    frame_package=''
    item = {}
    for records in event['Records']:
        frame_package_b64 = records['kinesis']['data']
        frame_package = cPickle.loads(base64.b64decode(frame_package_b64))
        print(frame_package)    
        x = str(frame_package['rekog_labels'])
        y = x.replace('"',"'")
        frame_package['rekog_labels'] = y
        s3_key = frame_package['s3_key']
        img_bytes = frame_package['img_bytes']
        notification_type = frame_package['notification_type'] 
        notification_message = frame_package['notification']
        notification_title = frame_package['notification_title'] 
        
        s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=img_bytes)
        del frame_package['img_bytes']
        #if (frame_package['notification_title']!='nothing'):
        response = ddb_table.put_item(Item = frame_package)
        endpointArnList = getEndPointsArn()
        #For APNS
    
        # APNS Notification
        if(notification_type == 'known'):
            person = notification_message.split()[0]
            apns_dict = {'aps':{'alert': notification_message, 'name' : person , 's3_bucket' : 'videostreambucket', 's3_key': s3_key, 'title' : 'Jupyter' , 'function' : 'VideoAnalytic'  }}
            apns_string = json.dumps(apns_dict,ensure_ascii=False)
            message = {'default':'default message','APNS_SANDBOX':apns_string}
            messageJSON = json.dumps(message,ensure_ascii=False)
            #logger.info("Publishing to iOS APNS_SANDBOX")
            for label_watch_sns_topic_arn  in endpointArnList: 
                respFace = sns_client.publish(TargetArn=label_watch_sns_topic_arn, Message =  messageJSON,  MessageStructure='json')
        if(notification_type == 'unknown'):
            person = 'An unknown'
            apns_dict = {'aps':{'alert': notification_message, 'name' : person , 's3_bucket' : 'videostreambucket', 's3_key': s3_key, 'title' : 'Jupyter' , 'function' : 'VideoAnalytic'  }}
            apns_string = json.dumps(apns_dict,ensure_ascii=False)
            message = {'default':'default message','APNS_SANDBOX':apns_string}
            messageJSON = json.dumps(message,ensure_ascii=False)
            #logger.info("Publishing to iOS APNS_SANDBOX")
            for label_watch_sns_topic_arn  in endpointArnList: 
                respFace = sns_client.publish(TargetArn=label_watch_sns_topic_arn, Message =  messageJSON,  MessageStructure='json')
        
        
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed  records.')
    }

def lambda_handler(event, context):
    print(event)
    return process_image(event, context)
	