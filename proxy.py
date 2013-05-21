#!/bin/env python
#encoding=utf8

import urllib2
import random

class HTTPProxy:
    def __init__(self,check=False,target="http://www.baidu.com"):
        self.datafile = {
            "raw":"rawProxy.lst",
            "good":"proxy.good.lst",
            "goodbak":"proxy.good.lst.bak"
        }
        self.testTarget = target

        if check:
            self.checkProxy()

        self._initOpener()

    def _initOpener(self):
        opener = []
        for i in file("proxy.good.lst"):
            proxy_host = i.strip('\n')
            proxy_support = urllib2.ProxyHandler({"http": proxy_host})
            one = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
            opener.append(one)
        if len(opener) <= 0:
            raise RuntimeError("no opener,need none empty proxy.good.lst")
        self.opener = opener

    def _checkProxy(self):
        #first back up the good list 
        self._bak(self.datafile["good"],self.datafile["goodbak"])

        request = urllib2.Request(self.testTarget)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7')

        fw = open(self.datafile["good"], 'w')
        for i in file(self.datafile["raw"]):
            proxy_host = i.strip('\n').split('\t')[0]
            proxy_support = urllib2.ProxyHandler({"http": proxy_host})
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            
            c = 0
            for i in xrange(1,6):
                try:
                    urllib2.urlopen(request, timeout = 2)
                    c += 1
                except:
                    pass
            if c >= 4:
                fw.write(proxy_host+'\n')
        fw.close()

    def _bak(self,old,new):
        import shutil
        try:
            f = open(old,'r')
            shutil.move(old,new)
        except:
            pass
        finally:
            f.close()
    
    #fetch use proxy to fetch data,retry 3 times
    def fetch(self,url,cnt=0):
        if cnt > 3:
            return None

        request = urllib2.Request(url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7')
        o = random.choice(self.opener)
        try:
            return o.open(request,timeout = 2).read()
        except:
            self.fetch(url,cnt+1)


