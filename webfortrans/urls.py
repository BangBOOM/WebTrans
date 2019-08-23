from django.urls import path,re_path
from webfortrans import views

app_name='webfortrans'

urlpatterns=[
    # path('index.html',views.index,name='translate'),
    path('index_1.html',views.index_1,name='translate_1'),
    path('index_2.html',views.index_2,name="translate_2"),
    path('index_3.html',views.index_3,name="translate_3"),
    path('get_trans/',views.get_trans,name='get_trans'),
    path('index_demo.html',views.index_demo,name="index_demo"),
    path('add_punc/',views.add_punc,name='add_punc'),
    path('get_corpus/',views.get_corpus,name='get_corpus'),
    path('get_dict/',views.get_dict,name='get_dict'),

]
