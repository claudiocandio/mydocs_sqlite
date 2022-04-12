from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.functions import Lower
from django.contrib.auth.models import Group, User

class Owner(models.Model):
    db_id = models.IntegerField(default=0, editable=False, db_index=True)
    name = models.CharField(max_length=250, db_index=True)
    email = models.EmailField(max_length=250, db_index=True, blank=True)
    address = models.CharField(max_length=250, db_index=True, blank=True)
    note = models.TextField(max_length=2000, blank=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

    class Meta:
        # db constraint, need to check this in forms.py as well
        # mariadb does not support UniqueConstraint, however this check is also done in forms.py
        constraints = [
            models.UniqueConstraint(Lower('name'), 'db_id', name='unique_lower_name_owner_db_id'),
        ]
        ordering = ['name']

class Category(models.Model):
    db_id = models.IntegerField(default=0, editable=False, db_index=True)
    name = models.CharField(max_length=250, db_index=True)

    class Meta:
        # db constraint, need to check this in forms.py as well
        # mariadb does not support UniqueConstraint, however this check is also done in forms.py
        constraints = [
            models.UniqueConstraint(Lower('name'), 'db_id', name='unique_lower_name_category_db_id'),
        ]
        ordering = ['name']
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Document(models.Model):
    db_id = models.IntegerField(default=0, editable=False, db_index=True)
    document_name = models.CharField(max_length=250, db_index=True)
    owner = models.ManyToManyField(Owner, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    date = models.DateField(db_index=True)
    note = models.TextField(max_length=2000, blank=True)

    def owners(self):
        return " | ".join([str(d) for d in self.owner.all()])

    def categories(self):
        return " | ".join([str(d) for d in self.category.all()])

    def __str__(self):
        """String for representing the Model object."""
        return f"Document Name: {self.document_name} | Date: {self.date}"

    class Meta:
        ordering = ['-date','document_name']

class File(models.Model):
    db_id = models.IntegerField(default=0, editable=False, db_index=True)
    file_bin = models.BinaryField()
    file_name = models.FileField(max_length=250)
    file_size = models.TextField(null=True)
    file_type = models.TextField(null=True)
    file_date = models.DateField(default=date.today)
    document = models.ForeignKey(Document, db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.file_name)

    class Meta:
        ordering = ['-file_date','file_name']

"""
    def save(self, *args, **kwargs): # this rewrites the save function
        super(File, self).save(*args, **kwargs)
        
        filename = self.file_name.url
        filename = filename[1:] # remove first char /
        
        self.file_size = filesizeformat(os.path.getsize(filename))
        
        #import magic
        mime = magic.Magic(mime=True)
        self.file_type = mime.from_file(filename)
        
        fp = open(filename,'rb')
        self.file_bin = fp.read()
        
        fp.close()
        os.remove(filename)
        
        return super(File, self).save(*args, **kwargs)
        # self.file_name.url will contain the path of the file in the file system
        # (the location is controlled by the MEDIA_ROOT Django setting).
        # You can then, for example, parse the data into models and populate the database with them.

"""

class Db(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    user = models.ManyToManyField(User, blank=True)

    class Meta:
        # db constraint, need to check this in forms.py as well
        # mariadb does not support UniqueConstraint, however this check is also done in forms.py
        constraints = [
            models.UniqueConstraint(Lower('name'), name='unique_lower_name_db'),
        ]
        ordering = ['name']

    def users(self):
        return " | ".join([str(d) for d in self.user.all()])
    
    def __str__(self):
        """String for representing the Model object."""
        #return f"Database: {self.name} | User: {self.user}"
        return self.name

class MyDocsSettings(models.Model):
    user_id = models.IntegerField(default=0, unique=True, db_index=True)
    db = models.ForeignKey(Db, blank=True, null=True, on_delete=models.SET_NULL)
    max_lines = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(2000000000)
        ]        
    )       # max lines with lists
    max_upload_size = models.IntegerField(
        validators=[
            MinValueValidator(1048576),     # 1MB
            MaxValueValidator(2147483647)   # 2GB
        ]        
    ) # max file size upload

    def __str__(self):
        """String for representing the Model object."""
        return f"Settings: max_line = {self.max_lines} | max_upload_size = {self.max_upload_size}"
    
