from django.urls import path

from documents.views import (
                            HomeView,
                            DocumentCreateView,DocumentListView,DocumentUpdateView,DocumentDeleteView,DocumentCopyMoveView,
                            OwnerCreateView,OwnerListView,OwnerUpdateView,OwnerDeleteView,
                            CategoryCreateView,CategoryListView,CategoryUpdateView,CategoryDeleteView,
                            DbCreateView,DbListView,DbUpdateView,DbDeleteView,
                            MyDocsSettingsUpdateView,
                            file_download_view,file_upload_view,db_change_view,
                            )

# need this to reference pages in templates ex: mysite.com/documents/owner_create
app_name = 'documents'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('document_create/',DocumentCreateView.as_view(), name='document_create'),
    path('document_list/',DocumentListView.as_view(), name='document_list'),
    path('document_update/<int:pk>',DocumentUpdateView.as_view(), name='document_update'),
    path('document_delete/<int:pk>',DocumentDeleteView.as_view(), name='document_delete'),
    path('document_copymove/<int:pk>',DocumentCopyMoveView.as_view(), name='document_copymove'),
    path('owner_create/',OwnerCreateView.as_view(), name='owner_create'),
    path('owner_list/',OwnerListView.as_view(), name='owner_list'),
    path('owner_update/<int:pk>',OwnerUpdateView.as_view(), name='owner_update'),
    path('owner_delete/<int:pk>',OwnerDeleteView.as_view(), name='owner_delete'),
    path('category_create/',CategoryCreateView.as_view(), name='category_create'),
    path('category_list/',CategoryListView.as_view(), name='category_list'),
    path('category_update/<int:pk>',CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>',CategoryDeleteView.as_view(), name='category_delete'),
    path('file_download/<int:pk>',file_download_view, name='file_download'),
    path('file_upload/<int:document_id>',file_upload_view, name='file_upload'),
    path('settings_update/<int:user_id>',MyDocsSettingsUpdateView.as_view(), name='settings_update'),
    path('db_create/',DbCreateView.as_view(), name='db_create'),
    path('db_list/',DbListView.as_view(), name='db_list'),
    path('db_update/<int:pk>',DbUpdateView.as_view(), name='db_update'),
    path('db_delete/<int:pk>',DbDeleteView.as_view(), name='db_delete'),
    path('db_change/',db_change_view, name='db_change'),
]