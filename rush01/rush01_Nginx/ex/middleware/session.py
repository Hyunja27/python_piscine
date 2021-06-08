from django.http import HttpRequest
from django.conf import settings as s
from django.utils.deprecation import MiddlewareMixin
import time, random

class AnonymousSessionMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if request.user.is_authenticated:
            return

        init_time = request.session.get(
            s.SESSSION_TIME_KEY, time.time())

        session_is_expired = time.time() - init_time > s.EXFIRE_TIME

        if session_is_expired:
            request.session.flush()

        request.session.setdefault('anonymous', random.choice(s.ID_LIST))
        request.session.setdefault(
                    s.SESSSION_TIME_KEY, time.time())

        request.user.username = request.session.get('anonymous')


        # if request.user.is_authenticated:
        #     return

        # request.session['anonymous'] = random.choice(s.ID_LIST)
        
        # if request.session.get(s.SESSSION_TIME_KEY):
        #     start_at = request.session[s.SESSSION_TIME_KEY]
        #     # start_at = request.session.setdefault(request , s.SESSSION_TIME_KEY)
        # else:
        #     start_at = request.session[s.SESSSION_TIME_KEY] = time.time()

        # is_exfired = start_at - time.time() > s.EXFIRE_TIME

        # if is_exfired:
        #     request.session.flush()
        #     request.session['anonymous'] = random.choice(s.ID_LIST)