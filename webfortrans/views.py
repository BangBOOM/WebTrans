from django.shortcuts import render
from .my_code import ClassForWeb
import jieba
# Create your views here.

jieba.load_userdict("D:\CSE\jetbrains\pycharm\WebTrans\webfortrans\myfiles\dict.txt")
jieba.load_userdict("D:\CSE\jetbrains\pycharm\WebTrans\webfortrans\myfiles\中国历史地名词典.txt")
jieba.load_userdict("D:\CSE\jetbrains\pycharm\WebTrans\webfortrans\myfiles\古代人名（25w）.txt")
jieba.load_userdict("D:\CSE\jetbrains\pycharm\WebTrans\webfortrans\myfiles\成语（5W）.txt")
# tfidf = analyse.extract_tags
# keywords=tfidf("加载")
# print(keywords)
# 将所有服务做成类然后在这部分预加载。

get_keyword=ClassForWeb.Tf_tiqu()

def index(request):
    '''
    :param request: 提供的请求
    :return:
    '''
    if request.method=="GET":
        print("get method")
        return render(request, 'version-02/index.html')
    else:
        print(request.POST)
        src=request.POST.get('input')
        if len(src.strip())==0:
            return render(request, 'version-02/index.html')
        # 前端提交古文到现代文翻译
        if "old2new.x" in request.POST:
            print('old2new')
            Demo=ClassForWeb.get_full_translate(get_keyword, src, src)
            return render(request, 'version-02/index.html',{'Demo':Demo})

        # 前端提交添加标点
        if "autopunc.x" in request.POST:
            print('autopunc')
            Demo = ClassForWeb.auto_add_punctuation(get_keyword, src, src)
            return render(request, 'version-02/index.html',{'Demo':Demo})

        # 前端提交现代文到古文
        if "new2old.x" in request.POST:
            print("new2old")
            Demo = ClassForWeb.get_back_translate(get_keyword, src, src)
            return render(request, 'version-02/index.html',{'Demo':Demo})

def index_1(request):
    return render(request,'version-03/index_1.html')

def index_2(request):
    return render(request,'version-03/index_2.html')

def index_3(request):
    return render(request,'version-03/index_3.html')