from django import forms
from django.forms.widgets import Textarea
from bootstrap_datepicker_plus.widgets import DatePickerInput

from documents.models import Document, MyDocsSettings,Owner,Category,File,Db

class OwnerModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # add db_id to self, this needs get_form_kwargs rewrite in views.py
        if('db_id' in kwargs):
            self.db_id = kwargs.pop('db_id')
        super(OwnerModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Owner
        fields = "__all__" # or just some fields --> fields = ['name',etc etc]
        widgets = {
            'note': Textarea(attrs={'cols': 80, 'rows': 5}),
        }

    # checks whether same category already exists, case insensitive
    # this goes along with the db constraint in Category model
    def clean(self):
        if('name' not in self.initial or self.cleaned_data['name'] != self.initial['name']):
            cleaned_data = super().clean()
            name = cleaned_data.get('name')
            o = Owner.objects.filter(name__iexact=name).filter(db_id__exact=self.db_id).first()
            if(o):
                raise forms.ValidationError('Owner with this Name already exists.')

class CategoryModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # add db_id to self, this needs get_form_kwargs rewrite in views.py
        if('db_id' in kwargs):
            self.db_id = kwargs.pop('db_id')
        super(CategoryModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Category
        fields = "__all__"

    # checks whether same category already exists, case insensitive
    # this goes along with the db constraint in Category model
    def clean(self):
        if('name' not in self.initial or self.cleaned_data['name'] != self.initial['name']):
            cleaned_data = super().clean()
            name = cleaned_data.get('name')
            c = Category.objects.filter(name__iexact=name).filter(db_id__exact=self.db_id).first()
            if(c):
                raise forms.ValidationError('Category with this Name already exists.')

class DbModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DbModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Db
        fields = "__all__"
        labels = {
            "name": "Database Name",
            "user": "User Assigned",
        }

    # checks whether same db already exists, case insensitive
    # this goes along with the db constraint in Db model
    def clean(self):
        if('name' not in self.initial or self.cleaned_data['name'] != self.initial['name']):
            cleaned_data = super().clean()
            name = cleaned_data.get('name')
            c = Db.objects.filter(name__iexact=name).first()
            if(c):
                raise forms.ValidationError('Database with this Name already exists.')

class DocumentCopyMoveForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentCopyMoveForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
        self.fields['document_name'].disabled = True
        # adding the below as disabled field would fail form validation
        self.fields['document_name'].initial = self.instance.document_name

    class Meta:
        model = Document
        fields = (
            'document_name',
        )
        labels = {
            "document_name": "Document Name",
        }


class MyDocsSettingsCopyMoveModelForm(forms.ModelForm):
    class Meta:
        model = MyDocsSettings
        fields = (
            'db',
        )
        labels = {
            "db": "Database"
        }

class DocumentModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # add db_id to self, this needs get_form_kwargs rewrite in views.py
        if('db_id' in kwargs):
            self.db_id = kwargs.pop('db_id')
        super(DocumentModelForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(db_id=self.db_id)
        self.fields['owner'].queryset = Owner.objects.filter(db_id=self.db_id)

    class Meta:
        model = Document
        fields = "__all__"
        widgets = {
            'note': Textarea(attrs={'cols': 80, 'rows': 5}),
            'date': DatePickerInput(options={'format': 'YYYY-MM-DD'}),
            #'owner': forms.widgets.CheckboxSelectMultiple(),
            #'category': forms.widgets.CheckboxSelectMultiple(),
        }
        labels = {
            "document_name": "Document Name",
        }

class DocumentListForm(forms.ModelForm):

    def __init__(self, db_id, *args, **kwargs):
        super(DocumentListForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(db_id=db_id)
        self.fields['owner'].queryset = Owner.objects.filter(db_id=db_id)

    class Meta:
        model = Document
        fields = "__all__"

    search_all = forms.CharField(required=False, label='Document Search (Name, Owner, Category, Date)', max_length=250)
    date_start = forms.DateField(
        #initial=datetime.date.today(),
        input_formats=['%Y-%m-%d'],
        required=False,
        label='Date Start',
        widget=DatePickerInput(
            # https://getdatepicker.com/4/Options/
            options={
                'format': 'YYYY-MM-DD',
            }
            )#.start_of('event days'),
        )
    date_end = forms.DateField(
        #initial=datetime.date.today(),
        input_formats=['%Y-%m-%d'],
        required=False,
        label='Date End',
        widget=DatePickerInput(
            # https://getdatepicker.com/4/Options/
            options={
                'format': 'YYYY-MM-DD',
            }
            )#.end_of('event days'),
        )

### Start File ###
class FileForm(forms.Form):

    class Meta:
        model = File
        fields = "__all__" # or just some fields --> fields = ['name',etc etc]

class MyDocsSettingsModelForm(forms.ModelForm):

    class Meta:
        model = MyDocsSettings
        fields = "__all__"
        labels = {
            "max_lines": "Max Lines",
            "max_upload_size": "Max Upload Size Bytes",
            "db": "Database"
        }

    def __init__(self, *args, **kwargs):
        super(MyDocsSettingsModelForm, self).__init__(*args, **kwargs)
        self.fields['db'].queryset = Db.objects.filter(user=self.initial['user_id'])
        self.fields['user_id'].widget.attrs['readonly'] = True
        