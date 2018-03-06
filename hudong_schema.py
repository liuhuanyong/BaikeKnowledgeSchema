#coding=utf-8
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib,urllib2
from urllib import quote,unquote
import json
from lxml import etree
import pymongo
conn=pymongo.MongoClient()
db=conn['concept_project']
record_list=set()

def get_categories(url):
    content=json.loads(urllib.urlopen(url).read())
    return content
   
def check_child(p_name,p_id,content):
    if len(content) <1 :
        return 
    else:
       for item in content:
            name=item['name']
            _id=item['id']
            print name,_id,p_id,p_name
            pair=name+'_'+str(_id)+'_'+str(p_id)+'_'+p_name
            if pair not in record_list:
                record_list.add(pair)
                if p_name == name:
                    return 
                else:
                    insert_db(name,_id,p_id,p_name)
                    content=get_categories('http://fenlei.baike.com/category/Ajax_cate.jsp?catename='+quote(name.encode('utf-8')))
                    check_child(name,_id,content)
                    
def insert_db(name,_id,p_id,p_name):
    data={}
    data['name']=name
    data['id']=_id
    data['p_id']=p_id
    data['p_name']=p_name
    db['hudong_concept'].insert(data)


def collect_categorys():
    url='http://fenlei.baike.com/category/Ajax_cate.jsp?catename=%E9%A1%B5%E9%9D%A2%E6%80%BB%E5%88%86%E7%B1%BB'
    content=get_categories(url)
    name = 'root'
    _id = 0
    sum=0
    if len(content)>0:
        check_child(name,_id,content)


if __name__=="__main__":
    count_words()
