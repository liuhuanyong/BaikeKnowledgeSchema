#coding = utf-8
from urllib import quote,urlopen
from lxml import etree
import pymongo
conn = pymongo.MongoClient()

def init_seed(seed_path):#初始化种子词
    seed_dict = {}
    for line in open('seed_category.txt'):
        line = line.strip().split(',')
        category = line[0]
        par_category = line[1]
        seed_dict[category] = par_category

    return seed_dict

def search_main(word):#搜索主函数
    url = 'http://baike.baidu.com/fenlei/%s'%quote(word)
    content = urlopen(url).read()
    sub_list,brother_list = collect_schema(content)
    if not sub_list:
        return 
    else:
        if sub_list:
            for sub_word in sub_list:
                data = {}
                data['concept'] = word
                data['sub_concept'] = sub_word
                data['brother_concept'] = sub_list
                conn['concept_project']['baidu_concept'].insert(data)
                search_main(sub_word.encode('utf-8'))

def collect_schema(content): #上下位抽取主函数
    selector = etree.HTML(content)
    title = ' '.join(selector.xpath('//title/text()'))
    schema_list = selector.xpath('//div[starts-with(@class,"category")]')  
    sub_list = []
    brother_list = []

    if len(schema_list) == 2:
        sub = schema_list[0]
        brother = schema_list[1]
        sub_list = sub.xpath('./a/text()')
        brother_list = brother.xpath('./a/text()')
        
    elif len(schema_list) == 1:
        brother = schema_list[0]
        brother_list = brother.xpath('./a/text()')

    return sub_list,brother_list


def main():
    seed_path = './seed_baike_category.txt'
    seed_dict = init_seed(seed_path)
    for seed,seed_par in seed_dict.items():
        search_main(seed)

main()

