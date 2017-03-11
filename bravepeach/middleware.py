"""
Middlewares.
"""
from django_user_agents.utils import get_user_agent


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
