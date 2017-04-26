"""
Middlewares.
"""
import json
import datetime

import boto3
from django_user_agents.utils import get_user_agent

from bravepeach.settings import SNS_ARN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class UserAgentMiddleware(object):
    """
    Check UA of request.
    Adds user_agent and flavour attr.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user_agent = get_user_agent(request)
        if request.user_agent.is_mobile:
            request.flavour = "mobile"
        else:
            request.flavour = "pc"

        response = self.get_response(request)
        return response


class ActionLogMiddleware(object):
    """
    Log all user action using celery and Amazon SQS.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path not in ["/get_alarm/", "/favicon.ico"]:
            message = {}
            if request.user.is_authenticated:
                message['user_id'] = request.user.id
            else:
                message['user_id'] = -1
            message['referer'] = request.META.get("HTTP_REFERER", "")
            message['path'] = request.path
            message['get_param'] = request.GET.dict()
            message['post_param'] = request.POST.dict()
            message['UA'] = str(request.user_agent)
            message["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            client = boto3.client("sns", region_name="ap-northeast-1", aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            resp = client.publish(TopicArn=SNS_ARN, Message=json.dumps(message))
            print(resp)
        response = self.get_response(request)
        return response
