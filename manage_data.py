import os,re,jieba,time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebTrans.settings")
import django,paramiko,Levenshtein,time
django.setup()
from  webfortrans import models
from jieba import analyse
# 向字典中导入数据
def deal_dic():
    path = "D:\\NEU\\大创\\数据\\词典\\字典\\古汉语字典_01.txt"
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        f.close()

    '''存储字典的列表'''
    dic_list = []

    for i in range(len(lines)):
        if len(lines[i].strip()) == 1:
            dic = {}
            dic['key'] = lines[i].strip()
            list = []
            for j in range(i + 1, len(lines)):
                if len(lines[j].strip()) != 1:
                    list.append(lines[j].strip())
                if len(lines[j].strip()) == 1:
                    dic['value'] = list
                    dic_list.append(dic)
                    break
    for d in dic_list:
        k = d['key']
        v = d['value']
        models.Dictionary.objects.create(key=k, value=v)

# 向语料库中导入数据
def deal_corpus():
    from webfortrans import models
    path="G:\大学时代\大创数据\总数据（处理后）\总数据按书分类合计"
    name_list=os.listdir(path)
    for i in range(0,len(name_list),2):
        src_path=path+'\\'+name_list[i]
        tgt_path=path+'\\'+name_list[i+1]
        title=name_list[i].replace('.txt','')
        print(title)
        with open(src_path,'r',encoding='utf-8') as f:
            src_lines=f.readlines()
        with open(tgt_path,'r',encoding='utf-8') as f:
            tgt_lines=f.readlines()
        for j in range(len(src_lines)):
            src=src_lines[j]
            tgt=tgt_lines[j]
            models.Corpus.objects.create(old=src,new=tgt,title=title)


def search_corpus(input_line):
    sentences=re.split('(。|\；|！|\!|\.|？|\?)', input_line)
    output_sents=[]
    for i in models.Corpus.objects.all():
        print(i.old)
    for i in range(int(len(sentences) / 2)):
        src_tgt_title_dic={}
        input_sent = sentences[2 * i] + sentences[2 * i + 1]
        obj=models.Corpus.objects.filter(old__contains=input_sent)
        if len(obj)==0:
            print('无语料库翻译')
            continue
        src_tgt_title_dic['src']=obj[0].src.strip()
        src_tgt_title_dic['tgt']=obj[0].tgt.strip()
        src_tgt_title_dic['title']=obj[0].title.strip()
        output_sents.append(obj[0])
    return output_sents

'''
语料库查找还需进一步完善，相似匹配
'''
# 直接把对象传出

def search_dic(input_line):
    out_put=jieba.cut(input_line,HMM=False)
    for demo in out_put:
        if len(demo)>1:
            try:
                obj=models.Dictionary.objects.filter(value__contains='【'+demo+'】')
                print(obj[0].value.strip())
            except:
                for l in demo:
                    obj = models.Dictionary.objects.filter(key__contains=l)
                    print(obj[0].key.strip())
                    for l in eval(obj[0].value):
                        print(l)

        if len(demo)==1:
            try:
                obj=models.Dictionary.objects.filter(key__contains=demo)
                print(obj[0].key.strip())
                for l in eval(obj[0].value):
                    print(l)
            except:
                pass
    return



def find_max_similarity(obj_list,src_sentence):
    demo=0
    obj = None
    for l in obj_list:
        similarity=Levenshtein.ratio(src_sentence,l.old)
        if similarity>demo:
            obj=l
            demo=similarity
    return obj

if __name__=='__main__':
    text="东至于海，登丸山，及岱宗。西至于空桐，登鸡头。"
    tfidf = analyse.extract_tags
    start = time.time()
    keywords=tfidf("加载")
    end =time.time()
    print(end-start)
    final_list=[]
    print("hello")
    keywords = tfidf(text)
    for k in keywords:
        # print(k)
        objs=models.Corpus.objects.filter(old__contains=k)
        if len(objs)>0:
            obj=find_max_similarity(objs,text)
            final_list.append(obj)
    if len(final_list)>0:
        for l in final_list:
            print(l.old.strip())
            print(l.new.strip())
            print(l.title.strip())







