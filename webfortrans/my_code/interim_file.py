# coding=gbk
import json
from ast import literal_eval
str="['liǎo', '①<动>结束；完毕；了结。《林黛玉进贾府》：“一语未～，只听后院中有人笑声。”', '②<动>明白；懂得。《南史·蔡撙传》：“卿殊不～事。”', '③<副>全；完全。《晋书·谢安传》：“～无喜色。”', '④<副>毕竟；终于。《新唐书·姚南仲传》：“虽欲自近，～复何益？”', '⑤<形>眼珠明亮。《孟子·离娄上》：“眸子不能掩其恶，胸中正，则眸子～焉。”', '⑥<形>清晰；清楚。《论衡·自纪》：“言～于耳，则事味于心。”', '⑦<形>高；远。《楚辞·九辨》：“～冥冥而薄天。”', 'liào', '<动>了望。黄尊宪《东沟行》：“我军～敌遽飞砲。”', 'le', '<助>用于动词、形容词后或句末，表示终结。岳飞《满江红》：“莫等闲，白～少年头，空悲切。”']"
listx=literal_eval(str)
print(type(listx))
for l in listx:
    print(l)


#
# str.replace("[",'')
# str.replace("]",'')
# list_str=str.split("\', \'")
# print(len(list_str))
# for l in list_str:
#     print(l)
