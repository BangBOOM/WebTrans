from django.shortcuts import render
from django.http import HttpResponse
from .my_code import ClassForWeb
import jieba
from jieba import analyse
# Create your views here.

jieba.load_userdict("D:\CSE\jetbrains\pycharm\WebTrans\webfortrans\myfiles\dict.txt")
jieba.load_userdict("D:\CSE\jetbrains\pycharm\WebTrans\webfortrans\myfiles\中国历史地名词典.txt")
jieba.load_userdict("D:\CSE\jetbrains\pycharm\WebTrans\webfortrans\myfiles\古代人名（25w）.txt")
jieba.load_userdict("D:\CSE\jetbrains\pycharm\WebTrans\webfortrans\myfiles\成语（5W）.txt")
# tfidf = analyse.extract_tags
# keywords=tfidf("加载")
# print(keywords)
# 将所有服务做成类然后在这部分预加载。
tiqu=ClassForWeb.Tf_tiqu()

def index(request):
    '''

    :param request: 提供的请求
    :return:
    '''
    try:
        src=request.POST.get('input')
        if src is None:
            return render(request, 'version-02/index.html')
    except:
        return render(request, 'version-02/index.html')
    print(request.POST)
    if "old2new.x" in request.POST:
        print('old2new')
        Demo=ClassForWeb.get_full_translate(tiqu,src)
        return render(request, 'version-02/index.html',{'Demo':Demo})
    return render(request, 'version-02/index.html')

