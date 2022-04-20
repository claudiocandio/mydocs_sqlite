from django.contrib import messages

from documents.models import MyDocsSettings,Db
from datetime import datetime

def print_form_errors(request, formerror_messages):
    for msg in formerror_messages:
        # need to add danger with messages.error, withouth give white message
        messages.error(request, f"{msg}: {formerror_messages[msg]}", "danger")
        print(msg)

def get_request_FIELD(get_name, get):
    """
    Return a POST or GET field
    Can be used with self.request.POST.get or self.request.GET.get
    It return a txt and avoids to return None
    """
    get_txt = ""
    q = get(get_name)
    if q is not None:
        get_txt = q
    return get_txt

def myset_get_max_lines(user_id):
    #return MyDocsSettings.objects.values_list('max_lines', flat=True).get(pk=1)
    #return MyDocsSettings.objects.get(pk=1).max_lines
    # this way to avoid issues during makemigrations & migrate
    return MyDocsSettings.objects.values_list('max_lines', flat=True).filter(user_id=user_id).first()

def myset_get_max_upload_size(user_id):
    #return MyDocsSettings.objects.values_list('max_upload_size', flat=True).get(pk=1)
    #return MyDocsSettings.objects.get(pk=1).max_upload_size
    # this way to avoid issues during makemigrations & migrate
    return MyDocsSettings.objects.values_list('max_upload_size', flat=True).filter(user_id=user_id).first()

def myset_get_inactive_minute_logout(user_id):
    #return MyDocsSettings.objects.values_list('inactive_minute_logout', flat=True).get(pk=1)
    #return MyDocsSettings.objects.get(pk=1).inactive_minute_logout
    # this way to avoid issues during makemigrations & migrate
    return MyDocsSettings.objects.values_list('inactive_minute_logout', flat=True).filter(user_id=user_id).first()

def myset_get_db_id(user_id=None, db_name=None):
    if(user_id):
        return MyDocsSettings.objects.values_list('db', flat=True).filter(user_id=user_id).first()
    elif(db_name):
        return Db.objects.values_list('id', flat=True).filter(name=db_name).first()
    else:
        print("Error getting db id")
        return ""

def myset_get_db(user_id=None, db_id=None):
    if(user_id):
        database = MyDocsSettings.objects.filter(user_id=user_id).first()
        if database.db is None:
            # need to be "" to remove Save buttons from category, owner, document creates
            return ""
        else:
            return database.db.name
    elif(db_id):
        return Db.objects.values_list('name', flat=True).filter(id=db_id).first()
    return ""

def myset_default(user_id):
    uid = MyDocsSettings.objects.filter(user_id=user_id).first()
    if(uid is None):
        uid = MyDocsSettings.objects.create(user_id=user_id, max_lines=50, max_upload_size=314572800)

def db_removed(user_id):
    """ Remove db from MyDocsSettings in case it was removed from Db
    """
    # check whether any db was removed from the user's assigned databases and remove it also
    # from the MyDocsSettings
    uid = MyDocsSettings.objects.filter(user_id=user_id).first()
    dbs = Db.objects.filter(user=user_id).all()
    if uid.db not in dbs:
        uid.db = None
        uid.save()

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_database_dbs(self):
    db = myset_get_db(user_id=self.request.user.id)
    dbs = Db.objects.filter(user=self.request.user.id).exclude(name=db).all()
    return db, dbs

def get_remote_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

