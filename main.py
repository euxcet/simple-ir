# -*- coding: utf-8 -*-
from elastic import Elastic
import time
from tqdm import tqdm

elastic = Elastic()

def exception_handler(request, exception):
    print("Request failed")

def create_index():
    print(elastic.delete_index())
    print(elastic.create_index())
    fin = open("sogou0011", "r", encoding = 'utf-8')
    for i in range(4700000):
        line = fin.readline()
        elastic.insert_doc(line)
        if i % 5000 == 0:
            print(i)




if __name__ == '__main__':
    create_index()
    #print(elastic.insert_doc("中国/a 是/b 北京/c").json())
    #time.sleep(1)
    #print(elastic.search_doc("中国/.*").json())