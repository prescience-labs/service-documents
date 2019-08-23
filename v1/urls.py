#pylint: disable=invalid-name
from django.urls import path
from v1 import views

urlpatterns = [
    path('/documents', views.DocumentList.as_view(), name='document_list'),
    path('/documents/<str:id>', views.DocumentDetail.as_view(), name='document_detail'),
]
