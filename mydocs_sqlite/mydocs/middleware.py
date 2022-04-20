from django.contrib.auth import logout
from documents import util
import datetime
import logging

from mydocs.settings import SESSION_IDLE_TIMEOUT

logger = logging.getLogger('mydocs')

class MyDocsMW(object):
    """Middle ware to ensure user gets logged out after defined period if inactvity."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_datetime = int(datetime.datetime.now().timestamp()) # unix time seconds 1970
            if 'last_active_time' in request.session:
                idle_period = current_datetime - request.session['last_active_time']
                if idle_period > SESSION_IDLE_TIMEOUT:
                    logger.info(f"User {request.user.username} logged out timeout from IP {util.get_remote_ip(request)}")
                    logout(request)
                    request.session.flush()

            # ok with unix time 1970
            # to use datetime format need to change to SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
            # not really good for security https://docs.djangoproject.com/en/4.0/topics/http/sessions/
            request.session['last_active_time'] = current_datetime

        logs = dict()
        logs['user'] = request.user.username
        logs['user_id'] = request.user.id
        logs['from_ip'] = util.get_remote_ip(request)
        logs['method'] = request.method
        #logs['path'] = request.path
        logs['referrer'] = request.META.get('HTTP_REFERER',None)

        # change mydocs loggers level to DEBUG in settings.py
        if(logging.getLevelName(logger.level) == 'DEBUG'):
            logs['session_key'] = request.session.session_key
            data = dict()
            data['get'] = dict(request.GET.copy())
            data['post'] = dict(request.POST.copy())
            # remove password from post data for security reasons
            keys_to_remove = ['password', 'csrfmiddlewaretoken']
            for key in keys_to_remove:
                data['post'].pop(key, None)
            logs['data'] = data

        logger.info(f"{logs}")

        response = self.get_response(request)
        return response
