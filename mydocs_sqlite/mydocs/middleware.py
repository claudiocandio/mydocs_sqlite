from django.contrib.auth import logout
from documents import util
import datetime

from mydocs.settings import SESSION_IDLE_TIMEOUT

class SessionIdleTimeout(object):
    """Middle ware to ensure user gets logged out after defined period if inactvity."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_datetime = int(datetime.datetime.now().timestamp()) # unix time seconds 1970
            if 'last_active_time' in request.session:
                idle_period = current_datetime - request.session['last_active_time']
                if idle_period > SESSION_IDLE_TIMEOUT:
                    print(f"mydocs {util.now()}: User timeout logout {request.user.username} from IP {request.META.get('REMOTE_ADDR')}")
                    logout(request)
                    request.session.flush()

            # ok with unix time 1970
            # to use datetime format need to change to SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
            # not really good for security https://docs.djangoproject.com/en/4.0/topics/http/sessions/
            request.session['last_active_time'] = current_datetime

        response = self.get_response(request)
        return response