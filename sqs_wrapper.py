import json
import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sqs_resource = boto3.client('sqs')


class SQS:
    def __init__(self, sqs_resource, queue_url) -> None:
        self.sqs = sqs_resource
        self.queue_url = queue_url

    @staticmethod
    def list_queues(sqs_resource):

        response = sqs_resource.list_queues()
        logger.info(response)

    @staticmethod
    def create_queue(sqs_resource, queue_name):
        """
        parameters:
        Delay Seconds set to 1 minute
        Message Retention Period is 24 Hours by default
        """

        response = sqs_resource.create_queue(
            QueueName=queue_name,
            Attributes={
                'DelaySeconds': '60',
                'MessageRetentionPeriod': '86400'
            }
        )
        logger.info(response)

    @staticmethod
    def delete_queue(sqs_resource, queue_url):
        response = sqs_resource.delete_queue(QueueUrl=queue_url)
        logger.info(response)

    @staticmethod
    def get_queue_url(sqs_resource, queue_name):
        response = sqs_resource.get_queue_url(QueueName=queue_name)
        logger.info(response)

    def send_message(self, att, body):
        """
        att : dict 
        body: str
        """
        response = self.sqs.send_message(



            # Message Attribute {
            #                 'Title': {
            #                     'DataType': 'String',
            #                     'StringValue': 'The Whistler'
            #                 },
            #                 'Author': {
            #                     'DataType': 'String',
            #                     'StringValue': 'John Grisham'
            #                 },
            #                 'WeeksOn': {
            #                     'DataType': 'Number',
            #                     'StringValue': '6'
            #                 }
            #             },

            QueueUrl=self.queue_url,
            DelaySeconds=10,
            MessageAttributes=att,
            MessageBody=(body)
        )

        logger.info(response)

    def receive_message(self):
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )

        logger.info(response)
        # return response

    def delete_fifo_message(self):

        message = self.receive_message()
        receipt_handle = message["Messages"][0]['ReceiptHandle']
        body = message["Messages"][0]['Body']
        response = self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )
        logger.info(response)

        print('deleted message: %s' % receipt_handle)


sqs = SQS(sqs_resource,
          os.getenv('SQS_URL'))


att = {'Query': {
    'DataType': 'String',
    'StringValue': 'SELECT *  FROM dbo.StoreDetail'},
    'Source': {
    'DataType': 'String',
    'StringValue': 'studios'},
    'Destination': {
    'DataType': 'String',
    'StringValue': 'studios'},
    'Job': {
    'DataType': 'String',
    'StringValue': 'Job123'},
}


body = "This is a Job Queue 33"


# sqs.send_message(att, body)
sqs.receive_message()
# sqs.delete_fifo_message()
