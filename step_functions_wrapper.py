import json
import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sfn_resource = boto3.client('stepfunctions')


class StepFunctions:
    def __init__(self, sfn_resource, sm_arn) -> None:
        self.resource = sfn_resource  # the boto3 resource for step function.
        self.sm_arn = sm_arn  # state machine arn.

    def describe_state_machine(self):
        response = self.resource.describe_state_machine(
            stateMachineArn=self.sm_arn)
        logger.info(response)
        return response

    def send_task_success(self, token, output):
        """[send success status after an external resource is done executing]

        Args:
            token ([string]): [Task token recieved from the state machine activity]
            output ([string]): [output string to the activity]
        """
        response = self.resource.send_task_success(
            taskToken=token, output=output)
        logger.info(response)

    def send_task_failure(self, token, error, cause):
        response = self.resource.send_task_success(
            taskToken=token, error=error, cause=cause)
        logger.info(response)

    def send_task_heartbeat(self, token):
        self.resource.send_task_heartbeat(taskToken=token)


sm_arn = os.getenv("SFN_ARN")
sfn = StepFunctions(sfn_resource=sfn_resource, sm_arn=sm_arn)
sfn.describe_state_machine()
