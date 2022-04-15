from django.shortcuts import redirect
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import filesizeformat
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.http import JsonResponse, Http404
from django.db import transaction
from django.utils.safestring import mark_safe

import datetime
from dateutil.relativedelta import relativedelta

from documents import util
from documents.models import Document,Owner,Category,File,MyDocsSettings,Db
from documents.forms import (
                            OwnerModelForm,CategoryModelForm,DocumentModelForm,DocumentListForm,DocumentCopyMoveForm,
                            FileForm,MyDocsSettingsModelForm,DbModelForm,
                            )

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        return context

### Start Owner ###

class OwnerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Owner
    # as UpdateView will use: owner_form.html
    form_class = OwnerModelForm
    success_message = "Owner successfully created"
    #success_url = reverse_lazy('documents:thanks')
    def get_success_url(self):
        return reverse("documents:owner_update", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        # Insert db_id (current database) from settings
        form.instance.db_id = util.myset_get_db_id(self.request.user.id)
        return super().form_valid(form)

    def get_form_kwargs(self):
        """ Add db_id to kwargs in order to have it in the forms.py """
        kwargs = super(OwnerCreateView, self).get_form_kwargs()
        kwargs['db_id'] = util.myset_get_db_id(self.request.user.id)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        return context

class OwnerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Owner
    # as CreateView will use: owner_form.html
    form_class = OwnerModelForm
    success_message = "Owner successfully updated"
    #success_url = reverse_lazy('documents:owner_list')

    def get_object(self, queryset=None):
        """ Hook to ensure object db_id is an allowed database for the user. """
        obj = super(OwnerUpdateView, self).get_object()
        if not obj.db_id == util.myset_get_db_id(self.request.user.id):
            raise Http404
        return obj

    # what to do with the form data here: form.cleaned_data that is a dictionary with post data
    #def form_valid(self, form):
    #    messages.success(self.request, "Account created successfully")
    #    return super().form_valid(form)

    def get_form_kwargs(self):
        """ Add db_id to kwargs in order to have it in the forms.py """
        kwargs = super(OwnerUpdateView, self).get_form_kwargs()
        kwargs['db_id'] = util.myset_get_db_id(self.request.user.id)
        return kwargs

    def get_success_url(self):
        return reverse("documents:owner_update", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        return context

class OwnerListView(LoginRequiredMixin, ListView):
    model = Owner

    def get_queryset(self):
        self.paginate_by = util.myset_get_max_lines(self.request.user.id)
        search_name = util.get_request_FIELD('search_name', self.request.GET.get)
        search_email = util.get_request_FIELD('search_email', self.request.GET.get)
        search_address = util.get_request_FIELD('search_address', self.request.GET.get)

        object_list = Owner.objects.filter(
            Q(name__icontains=search_name) & 
            Q(email__icontains=search_email) &
            Q(address__icontains=search_address) &
            # Force search only for current db_id (current database) from settings
            Q(db_id__exact=util.myset_get_db_id(self.request.user.id))
        ).distinct()

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        context['search_name'] = util.get_request_FIELD('search_name', self.request.GET.get)
        context['search_email'] = util.get_request_FIELD('search_email', self.request.GET.get)
        context['search_address'] = util.get_request_FIELD('search_address', self.request.GET.get)
        return context

class OwnerDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Owner
    # default will use: owner_confirm_delete.html
    template_name = 'documents/owner_delete.html'
    success_url = reverse_lazy('documents:owner_list')
    success_message = "Owner successfully deleted"

    def get_context_data(self, **kwargs): # to get a list of documents with this owner
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        context['owner_documents'] = Document.objects. \
            filter(owner=self.object.id).all()[0:util.myset_get_max_lines(self.request.user.id)]
        return context    

    def get_object(self, queryset=None):
        """ Hook to ensure object db_id is an allowed database for the user. """
        obj = super(OwnerDeleteView, self).get_object()
        if not obj.db_id == util.myset_get_db_id(self.request.user.id):
            raise Http404
        return obj

### End Owner ###

### Start Category ###

class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryModelForm
    success_message = "Category successfully created"

    def get_success_url(self):
        return reverse("documents:category_update", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        # Insert db_id (current database) from settings
        form.instance.db_id = util.myset_get_db_id(self.request.user.id)
        return super().form_valid(form)

    def get_form_kwargs(self):
        """ Add db_id to kwargs in order to have it in the forms.py """
        kwargs = super(CategoryCreateView, self).get_form_kwargs()
        kwargs['db_id'] = util.myset_get_db_id(self.request.user.id)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        return context

class CategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryModelForm
    success_message = "Category successfully updated"

    def get_object(self, queryset=None):
        """ Hook to ensure object db_id is an allowed database for the user. """
        obj = super(CategoryUpdateView, self).get_object()
        if not obj.db_id == util.myset_get_db_id(self.request.user.id):
            raise Http404
        return obj

    def get_form_kwargs(self):
        """ Add db_id to kwargs in order to have it in the forms.py """
        kwargs = super(CategoryUpdateView, self).get_form_kwargs()
        kwargs['db_id'] = util.myset_get_db_id(self.request.user.id)
        return kwargs

    def get_success_url(self):
        return reverse("documents:category_update", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        return context

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

    def get_queryset(self):
        self.paginate_by = util.myset_get_max_lines(self.request.user.id)
        search_name = util.get_request_FIELD('search_name', self.request.GET.get)

        object_list = Category.objects.filter(
            Q(name__icontains=search_name)  &
            # Force search only for current db_id (current database) from settings
            Q(db_id__exact=util.myset_get_db_id(self.request.user.id))
        )

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        context['search_name'] = util.get_request_FIELD('search_name', self.request.GET.get)
        return context

class CategoryDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Category
    template_name = 'documents/category_delete.html'
    success_url = reverse_lazy('documents:category_list')
    success_message = "Category successfully deleted"

    def get_context_data(self, **kwargs): # to get a list of documents with this category
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        context['category_documents'] = Document.objects. \
            filter(category=self.object.id).all()[0:util.myset_get_max_lines(self.request.user.id)]
        return context    

    def get_object(self, queryset=None):
        """ Hook to ensure object db_id is an allowed database for the user. """
        obj = super(CategoryDeleteView, self).get_object()
        if not obj.db_id == util.myset_get_db_id(self.request.user.id):
            raise Http404
        return obj

### End Category ###

### Start Db ###

class DbCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Db
    form_class = DbModelForm
    success_message = "Database successfully created"

    def get_success_url(self):
        return reverse("documents:db_update", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        return context

class DbUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Db
    form_class = DbModelForm
    success_message = "Database successfully updated"

    def get_success_url(self):
        return reverse("documents:db_update", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        return context

class DbListView(LoginRequiredMixin, ListView):
    model = Db

    def get_queryset(self):
        self.paginate_by = util.myset_get_max_lines(self.request.user.id)
        search_name = util.get_request_FIELD('search_name', self.request.GET.get)

        object_list = Db.objects.filter(
            Q(name__icontains=search_name)
        )

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        context['search_name'] = util.get_request_FIELD('search_name', self.request.GET.get)
        return context

class DbDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """ 
    Here I will just remove the database name
    For security I do not remove documents, owners and categories automatically
    """
    model = Db
    template_name = 'documents/db_delete.html'
    success_url = reverse_lazy('documents:db_list')
    success_message = "Database successfully deleted"

    def get_context_data(self, **kwargs): # to get a list of documents with this database
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        context['db_documents'] = Document.objects. \
            filter(db_id=self.kwargs['pk']).all()[0:util.myset_get_max_lines(self.request.user.id)]
        return context

    def get_object(self, queryset=None):
        """ Hook to ensure object db_id is an allowed database for the user. """
        obj = super(DbDeleteView, self).get_object()
        dbs = Db.objects.filter(user=self.request.user.id).all()
        if not obj in dbs:
            raise Http404
        return obj

### End Db ###

### Start Document ###

class DocumentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Document
    form_class = DocumentModelForm
    success_message = "Document successfully created"

    def get_success_url(self):
        return reverse("documents:document_update", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        # Insert db_id (current database) from settings
        form.instance.db_id = util.myset_get_db_id(self.request.user.id)
        return super().form_valid(form)

    def get_form_kwargs(self):
        """ Add db_id to kwargs in order to have it in the forms.py """
        kwargs = super(DocumentCreateView, self).get_form_kwargs()
        kwargs['db_id'] = util.myset_get_db_id(self.request.user.id)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        return context

class DocumentCopyMoveView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Document
    form_class = DocumentCopyMoveForm
    template_name = 'documents/document_copymove.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        db = util.myset_get_db(user_id=self.request.user.id)
        db_id = util.myset_get_db_id(self.request.user.id)
        context['database'] = db
        context['dbs'] = Db.objects.filter(user=self.request.user.id).exclude(name=db).all()
        doc = Document.objects.get(pk=self.kwargs['pk'])
        docs_similar = Document.objects.filter(document_name__iexact=doc.document_name) \
                        .filter(date=doc.date) \
                        .exclude(db_id=db_id).all()
        context['docs_similar'] = docs_similar
        # add db_name to docs_similar
        for i in range(len(context['docs_similar'])):
            context['docs_similar'][i].db_name = util.myset_get_db(db_id=context['docs_similar'][i].db_id)
        return context

    def get_success_url(self):
        to_db = self.request.POST.get("to_db")
        to_db_id = util.myset_get_db_id(db_name=to_db)
        db_id = util.myset_get_db_id(user_id=self.request.user.id)
        doc_id = self.kwargs['pk']

        if self.request.POST.get("copy"):
            msg = self.document_copymove(doc_id,db_id,to_db,to_db_id,copy=True)
            messages.success(self.request, mark_safe(msg))
            return reverse("documents:document_update", kwargs={"pk": doc_id})    

        elif self.request.POST.get("move"):
            msg = self.document_copymove(doc_id,db_id,to_db,to_db_id)
            messages.success(self.request, mark_safe(msg))
        
        return reverse("documents:document_list")

    def document_copymove(self,doc_id,db_id,to_db,to_db_id, copy=False):
        with transaction.atomic():
            doc = Document.objects.get(pk=doc_id)
            if(copy):
                doc_to = doc
                doc_to.pk = None
                doc_to.id = None
                doc_to.db_id = to_db_id
                doc_to.save()
            else:
                doc.db_id = to_db_id
                doc.save()

            # Files
            if(copy):
                files = File.objects.filter(document=doc_id).all()
                for f in files:
                    f.pk = None
                    f.id = None
                    f.document_id = doc_to.id
                    f.db_id = to_db_id
                    f.save()
            else:
                File.objects.filter(document=doc.id).update(db_id=to_db_id)

            # doc needs to be read again here
            doc = Document.objects.get(pk=doc_id)        
            # Owners
            for o in doc.owner.all():
                # check whether the same owner already exists in the to_db
                owner_to = Owner.objects.filter(name__iexact=o).filter(db_id__exact=to_db_id).first()
                if(not owner_to):
                    #duplicate owner in the to_db
                    owner = Owner.objects.filter(name__exact=o).filter(db_id__exact=db_id).first()
                    owner_to = Owner.objects.create(
                                                    name=owner.name,
                                                    email=owner.email,
                                                    address=owner.address,
                                                    note=owner.note,
                                                    db_id=to_db_id
                                                    )
                if(copy):
                    doc_to.owner.add(owner_to)
                else:
                    doc.owner.remove(o)
                    doc.owner.add(owner_to)
                owner_to.save()

            # Categories
            for c in doc.category.all():
                # check whether the same category already exists in the to_db
                category_to = Category.objects.filter(name__iexact=c).filter(db_id__exact=to_db_id).first()
                if(not category_to):
                    #duplicate category in the to_db
                    category = Category.objects.filter(name__exact=c).filter(db_id__exact=db_id).first()
                    category_to = Category.objects.create(
                                                    name=category.name,
                                                    db_id=to_db_id
                                                    )
                if(copy):
                    doc_to.category.add(category_to)
                else:
                    doc.category.remove(c)
                    doc.category.add(category_to)
                category_to.save()
            if(copy):
                doc_to.save()
                msg = f"Document: {doc}<br/>copied successfully to database: {to_db}"
            else:
                doc.save()
                msg = f"Document: {doc}<br/>moved successfully to database: {to_db}"

        return(msg)

class DocumentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Document
    form_class = DocumentModelForm

    def get_success_url(self):
        files_id_delete = ''
        if self.request.POST.get("file_id_delete"):
            files_id_delete = util.get_request_FIELD('file_id_delete', self.request.POST.getlist)
        elif self.request.POST.get("files_id_delete"):
            files_id_delete = util.get_request_FIELD('checkbox_items', self.request.POST.getlist)
        if len(files_id_delete):
            for pk in files_id_delete:
                fp = File.objects.get(pk=pk)
                file_name = fp.file_name
                fp.delete()
                messages.success(self.request, f"File {file_name} successfully deleted")
            return reverse("documents:document_update", kwargs={"pk": self.object.id})    
        
        messages.success(self.request, "Document updated successfully")
        return reverse("documents:document_update", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        context['doc_files'] = File.objects. \
            filter(document=self.object.id). \
            filter(db_id__exact=util.myset_get_db_id(self.request.user.id)). \
            values('id','file_name','file_size','file_type','file_date').all()
        context['max_upload_size'] = f"Max Upload Size {filesizeformat(util.myset_get_max_upload_size(self.request.user.id))}"
        return context

    def get_form_kwargs(self):
        """ Add db_id to kwargs in order to have it in the forms.py """
        kwargs = super(DocumentUpdateView, self).get_form_kwargs()
        kwargs['db_id'] = util.myset_get_db_id(self.request.user.id)
        return kwargs

    def get_object(self, queryset=None):
        """ Hook to ensure object db_id is an allowed database for the user. """
        obj = super(DocumentUpdateView, self).get_object()
        if not obj.db_id == util.myset_get_db_id(self.request.user.id):
            raise Http404
        return obj

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    #template_name = 'documents/document_list.html' # already this by default
    #context_object_name = "document_list" # default is object_list

    def get_queryset(self):
        self.paginate_by = util.myset_get_max_lines(self.request.user.id)
        search_all = util.get_request_FIELD('search_all', self.request.GET.get)
        date_start = util.get_request_FIELD('date_start', self.request.GET.get)
        date_end = util.get_request_FIELD('date_end', self.request.GET.get)
        months = util.get_request_FIELD('months', self.request.GET.get)
        days = util.get_request_FIELD('days', self.request.GET.get)
        owner = util.get_request_FIELD('owner', self.request.GET.getlist)
        category = util.get_request_FIELD('category', self.request.GET.getlist)

        if days != '' and days != '0' and date_start == '' and date_end == '':
            date_start, date_end = self.set_datew(days=days)
        elif days != '' and days != '0' and date_start == '':
            date_start, _ = self.set_datew(days=days, date_end=date_end)

        if months != '' and months != '0' and date_start == '' and date_end == '':
            date_start, date_end = self.set_datew(months=months)
        elif months != '' and months != '0' and date_start == '':
            date_start, _ = self.set_datew(months=months, date_end=date_end)

        query = Q()
        if len(search_all):
            query &= (
            Q(document_name__icontains=search_all)  |
            Q(owner__name__icontains=search_all)    |
            Q(category__name__icontains=search_all) |
            Q(date__icontains=search_all)
            )
        if len(owner):
            query &= Q(owner__id__in=owner)
        if len(category):
            query &= Q(category__id__in=category)
        if len(date_start) & len(date_end):
            date_start = parse_date(date_start)
            date_end = parse_date(date_end)
            query &= Q(date__range=[date_start,date_end])
        elif len(date_start):
            date_start = parse_date(date_start)
            query &= Q(date__gte=date_start)
        elif len(date_end):
            date_end = parse_date(date_end)
            query &= Q(date__lte=date_end)

        # Force search only for current db_id (current database) from settings
        query &= Q(db_id__exact=util.myset_get_db_id(self.request.user.id))

        object_list = Document.objects.filter(query).distinct()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        months = util.get_request_FIELD('months', self.request.GET.get)
        days = util.get_request_FIELD('days', self.request.GET.get)
        date_start = util.get_request_FIELD('date_start', self.request.GET.get)
        date_end = util.get_request_FIELD('date_end', self.request.GET.get)

        form = DocumentListForm(util.myset_get_db_id(self.request.user.id))

        if days != '' and days != '0' and date_start == '' and date_end == '':
            date_start, date_end = self.set_datew(days=days)
        elif days != '' and days != '0' and date_start == '':
            date_start, _ = self.set_datew(days=days, date_end=date_end)

        if months != '' and months != '0' and date_start == '' and date_end == '':
            date_start, date_end = self.set_datew(months=months)
        elif months != '' and months != '0' and date_start == '':
            date_start, _ = self.set_datew(months=months, date_end=date_end)

        form.fields['search_all'].initial = util.get_request_FIELD('search_all', self.request.GET.get)
        form.fields['date_start'].initial = date_start
        form.fields['date_end'].initial = date_end

        form.fields['owner'].initial = util.get_request_FIELD('owner', self.request.GET.getlist)
        form.fields['category'].initial = util.get_request_FIELD('category', self.request.GET.getlist)

        context['form'] = form # to send the form to the html, with ListView doesn't have any
        context['months'] = months
        context['days'] = days

        return context

    def set_datew(self, months=0, days=0, date_end=''):
        if months == '0' and days == 0 and date_end=='':
            date_start = ''
            date_end = ''
        elif months and date_end!='':
            date_end = parse_date(date_end)
            date_start = date_end + relativedelta(months=-int(months))
        elif months:
            date_start = datetime.date.today() + relativedelta(months=-int(months))
            date_end = datetime.date.today()
        elif days and date_end!='':
            date_end = parse_date(date_end)
            date_start = date_end + relativedelta(days=-int(days))
        elif days:
            date_start = datetime.date.today() + relativedelta(days=-int(days))
            date_end = datetime.date.today()

        return str(date_start), str(date_end)

class DocumentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Document
    template_name = 'documents/document_delete.html'
    success_url = reverse_lazy('documents:document_list')
    success_message = "Document successfully deleted"

    def get_object(self, queryset=None):
        """ Hook to ensure object db_id is an allowed database for the user. """
        obj = super(DocumentDeleteView, self).get_object()
        if not obj.db_id == util.myset_get_db_id(self.request.user.id):
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        return context

### End Document ###

### Start MyDocsSettings ###

class MyDocsSettingsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MyDocsSettings
    form_class = MyDocsSettingsModelForm
    success_message = "Settings successfully updated"

    def get_success_url(self):
        return reverse("documents:settings_update", kwargs={'user_id': self.request.user.id})

    # to override pk as main filter for the object
    def get_object(self, queryset=None):
        # to always get the logged in user.id settings, avoid url manipolation reading others settings
        return MyDocsSettings.objects.get(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'], context['dbs'] = util.get_database_dbs(self)
        return context

### End MyDocsSettings ###

@login_required
def db_change_view(request):
    # called from ajax, redirect won't work here
    if request.method == "POST":
        db = request.POST.get('db')
        # check if db is assigned to this user
        dbs = Db.objects.filter(user=request.user.id).values_list('name',flat=True).all()
        if not db in dbs:
            raise Http404
        db_id =  util.myset_get_db_id(db_name=db)
        MyDocsSettings.objects.filter(user_id=request.user.id).update(db_id=db_id)

        messages.success(request, f"Current Database is: {db}")

        # this return to ajax as data.url
        return JsonResponse({'url':'/documents/'})

### Start File ###

@login_required
def file_upload_view(request, document_id):
   
    if request.method == "POST":
        #Get the posted form
        form = FileForm(request.POST, request.FILES)
        form.full_clean()

        if 'file_name' in request.POST: # if file_name exists no file was selected
            messages.warning(request, "Select a File to add")
            return redirect(reverse('documents:document_update', kwargs={'pk': document_id}))

        if form.is_valid():

            files = request.FILES.getlist('file_name')
            files_size = 0
            for f in files:
                files_size += f.size

            # Checking max_upload_size summing up all files size
            if files_size > util.myset_get_max_upload_size(request.user.id):
                messages.warning(request, f"Please keep files size under {filesizeformat(util.myset_get_max_upload_size(request.user.id))}. Current files size {filesizeformat(files_size)}")
                return JsonResponse({'data':'Data uploaded'})
                # comment above and use this if not using ajax progress upload
                #return redirect(reverse('documents:document_update', kwargs={'pk': document_id}))
            
            for f in files:
                file_uploaded = f.file
                file_bytes = file_uploaded.read()
                file_name = f.name

                File.objects.create(
                    document_id = document_id,
                    file_name = file_name,
                    file_size = f.size,
                    file_type = f.content_type,
                    file_bin = file_bytes,
                    db_id = util.myset_get_db_id(request.user.id),
                    )
                messages.success(request, f"File {file_name} successfully uploaded")
            return JsonResponse({'data':'Data uploaded'})
            # comment above and use this if not using ajax progress upload
            #return redirect(reverse('documents:document_update', kwargs={'pk': document_id}))
        else:
            util.print_form_errors(request, form.errors)
            return redirect(reverse('documents:document_update', kwargs={'pk': document_id}))

    return redirect(reverse('documents:document_update', kwargs={'pk': document_id}))

@login_required
def file_download_view(request, pk):
    myfile = File.objects.get(pk=pk)
    response = HttpResponse(content_type=f"{myfile.file_type}")
    # force browser to download file
    response['Content-Disposition'] = f'attachment; filename={myfile.file_name}'
    response.write(bytes(myfile.file_bin))
    return response

### End File ###
