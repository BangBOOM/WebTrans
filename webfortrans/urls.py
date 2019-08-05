from django.urls import path,re_path
from webfortrans import views

app_name='webfortrans'

urlpatterns=[path('index.html',views.index,name='translate'),]