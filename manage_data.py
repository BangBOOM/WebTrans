import os,re,jieba,time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebTrans.settings")
import django,paramiko
django.setup()
from  webfortrans import models
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
    for i in range(int(len(sentences) / 2)):
        src_tgt_title_dic={}
        input_sent = sentences[2 * i] + sentences[2 * i + 1]
        obj=models.Corpus.objects.filter(src__contains=input_sent)
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


def get_model_translate(src):
    src_cut=jieba.cut(src,HMM=False)
    src_cut=' '.join(src_cut)
    with open('src.txt','w',encoding='utf-8') as f:
        f.write(src_cut)
    hostname = '39.104.88.70'
    password = '.'
    username = 'dingjiapeng'
    port = 22
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(hostname, port=port, username=username, password=password)

    # 上传文件
    sftp=client.open_sftp()
    sftp.put('src.txt','/home/dingjiapeng/ywq/new_src.txt')
    # 执行翻译命令
    command_x = 'CUDA_VISIBLE_DEVICES=-1 python3 /home/dingjiapeng/tensor2tensor/bin/t2t-decoder' \
               + ' --data_dir=/home/dingjiapeng/data/' \
               + ' --problem=wmt_zhen_tokens_32k --model=transformer --hparams_set=transformer_base_single_gpu ' \
               + '--output_dir=/home/dingjiapeng/model ' \
               + '--decode_beam_size=12 --decode_alpha=1.3  ' \
               + '--decode_from_file=/home/dingjiapeng/ywq/new_src.txt ' \
               + '--decode_to_file=/home/dingjiapeng/ywq/new_tgt.txt'
    stdin, stdout, stderr = client.exec_command(command_x)
    time.sleep(60)
    sftp.get('/home/dingjiapeng/ywq/new_tgt.txt','tgt.txt')
    with open('tgt.txt','r',encoding='utf-8') as f:
        for l in f.readlines():
            print(l)




if __name__=='__main__':

    deal_corpus()