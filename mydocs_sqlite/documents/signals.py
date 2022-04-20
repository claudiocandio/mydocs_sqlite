from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

import logging

from documents import util

logger = logging.getLogger('mydocs')

@receiver(user_logged_in)
def user_logged_in_signal(sender, request, user, **kwargs):
    logger.info(f"User {user.username} logged in from IP {util.get_remote_ip(request)}")
    util.myset_default(user.id)
    util.db_removed(user.id)
    util.myset_get_db_id(user.id)
 
@receiver(user_logged_out)
def user_logged_out_signal(sender, request, user, **kwargs):
    if(user):
        logger.info(f"User {user.username} logged out from IP {util.get_remote_ip(request)}")
    else:
        logger.info(f"User logged out from IP {util.get_remote_ip(request)}")
    util.db_removed(user.id)

@receiver(user_login_failed)
def user_login_failed_signal(sender, credentials, request, **kwargs):
    logger.warning(f"User login failed {credentials.get('username')} from IP {util.get_remote_ip(request)}")
