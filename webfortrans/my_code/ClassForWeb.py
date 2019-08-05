import jieba,re,Levenshtein
from ast import literal_eval
from webfortrans import models
from jieba import analyse


class Translate():
    def __init__(self,src,tgt_model,tgt_corpus,tgt_dic):
        self.src=src
        self.tgt_model=tgt_model
        self.tgt_corpus=tgt_corpus
        self.tgt_dic=tgt_dic

class Dic_demo():
    def __init__(self,key,value):
        self.key=key
        self.value=value

class Tf_tiqu():
    """方便分词模块在view中预加载"""
    def __init__(self):
        self.tfidf = analyse.extract_tags
        self.keyword=self.tfidf("加载")
        print(self.keyword)
    def keyword_extraction(self,sentence):
        return self.tfidf(sentence)



def get_dic_translate(src):
    '''
    :param src: 输入的原文
    :return:
    '''
    dic_list=[]
    out_put=jieba.cut(src, HMM=False)
    out_put=list(out_put)
    out_put=sorted(set(out_put), key=out_put.index) #去除重复元素
    for demo in out_put:
        # 词语
        if len(demo) > 1:
            obj = models.Dictionary.objects.filter(value__contains='【' + demo + '】')
            if len(obj)==0:
                # 未索引到词语则将词语拆开成字逐个搜索
                for x in demo:
                    obj=models.Dictionary.objects.filter(key=x)
                    if len(obj)!=0:
                        dic_x=Dic_demo(obj[0].key,literal_eval(obj[0].value))
                        dic_list.append(dic_x)
            else:
                dic_x = Dic_demo(obj[0].key, literal_eval(obj[0].value))
                dic_list.append(dic_x)
        # 单字
        if len(demo)==1:
            obj=models.Dictionary.objects.filter(key=demo)
            if len(obj)!=0:
                dic_x = Dic_demo(obj[0].key, literal_eval(obj[0].value))
                dic_list.append(dic_x)
    return dic_list



def find_max_similarity(obj_list,src_sentence):
    demo=0
    obj = None
    for l in obj_list:
        similarity=Levenshtein.ratio(src_sentence,l.old)
        if similarity>demo:
            obj=l
            demo=similarity
    return obj

def get_corpus_translate(tiqu,src):
    '''
    :param src: 表示查找的内容
    :return: 语料库列表（原文，译文，出处）
    '''
    corpus_list = []
    sentences = re.split('(。|\；|！|\!|\.|？|\?)', src)
    for i in range(int(len(sentences) / 2)):
        list_demo=[]
        input_sent = sentences[2 * i] + sentences[2 * i + 1]
        print(input_sent)
        obj = models.Corpus.objects.filter(old__contains=input_sent)
        if len(obj) == 0:
            tfidf = analyse.extract_tags
            keywords=tiqu.keyword_extraction(input_sent)
            final_list = []
            # 这部分keywords越多会影响速度
            for k in keywords[0:3]:
                print(k)
                objs = models.Corpus.objects.filter(old__contains=k)
                if len(objs) > 0:
                    obj = objs[0]
                    final_list.append(obj)
            corpus_list+=final_list
        else:
            corpus_list.append(obj[0])
    return corpus_list

def get_full_translate(tiqu,src):
    tgt_corpus=get_corpus_translate(tiqu,src)
    tgt_dic=get_dic_translate(src)
    Demo=Translate(src,src,tgt_corpus,tgt_dic)
    return Demo


