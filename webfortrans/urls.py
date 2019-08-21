from django.urls import path,re_path
from webfortrans import views

app_name='webfortrans'

urlpatterns=[
    path('index.html',views.index,name='translate'),
    path('index_1.html',views.index_1,name='translate_1'),
    path('index_2.html',views.index_2,name="translate_2"),
    path('index_3.html',views.index_3,name="translate_3"),
]
