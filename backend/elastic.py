# -*- coding: utf-8 -*-
import grequests
import requests
import json

class Elastic:
    def __init__(self):
        self.index_name = "corpus"
        self.base_url = "http://127.0.0.1:9200/" + self.index_name
        self.reqs = []

    def get(self, url):
        return requests.get(self.base_url + url, headers = {
            'Accept': 'application/json'
        })

    def post(self, url, data):
        return requests.post(self.base_url + url, headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, data = json.dumps(data))

    def post_asyn(self, url, data):
        return grequests.post(self.base_url + url, headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, data = json.dumps(data))

    def put(self, url, data):
        return requests.put(self.base_url + url, headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, data = json.dumps(data))

    def delete(self, url):
        return requests.delete(self.base_url + url, headers = {
            'Accept': 'application/json'
        })

    def delete_index(self):
        return self.delete("/")

    def create_index(self):
        return self.put("/", {
            "mappings": {
                "properties": {
                    "content": {
                        "type": "text",
                        "analyzer": "whitespace"
                    }
                }
            }
        })

    def insert_doc(self, content):
        self.reqs.append(self.post_asyn("/_doc/", {
            "content": content
        }))
        if len(self.reqs) == 1000:
            grequests.map(self.reqs)
            self.reqs = []

    def search_doc(self, value):
        return self.post("/_search/", {
            "size": 20,
            "query": {
                "regexp": {
                    "content": {
                        "value": value
                    }
                }
            }
        })

    def search_doc_multi(self, values):
        must = []
        for value in values:
            must.append({
                "regexp": {
                    "content": {
                        "value": value
                    }
                }
            })
        return self.post("/_search/", {
            "size": 1000,
            "query": {
                "bool": {
                    "must": must
                }
            }
        })
