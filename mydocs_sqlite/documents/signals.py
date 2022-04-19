from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from documents import util

@receiver(user_logged_in)
def user_logged_in_signal(sender, request, user, **kwargs):
    print(f"mydocs {util.now()}: User login {user.username} from IP {request.META.get('REMOTE_ADDR')}")
    util.myset_default(user.id)
    util.db_removed(user.id)
    util.myset_get_db_id(user.id)
 
@receiver(user_logged_out)
def user_logged_out_signal(sender, request, user, **kwargs):
    if(user):
        print(f"mydocs {util.now()}: User logout {user.username} from IP {request.META.get('REMOTE_ADDR')}")
    else:
        print(f"mydocs {util.now()}: User logout from IP {request.META.get('REMOTE_ADDR')}")
    util.db_removed(user.id)

@receiver(user_login_failed)
def user_login_failed_signal(sender, credentials, request, **kwargs):
    print(f"mydocs {util.now()}: User login failed {credentials.get('username')} from IP {request.META.get('REMOTE_ADDR')}")
