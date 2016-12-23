#_*_coding:utf-8_*_
'''
Created on 2016年12月16日

@author: ZWJ
'''

class RequestExeute1(object):
     
    def process_request(self,request):
        print 'process_request1'
        os = request.META['OS']
        addr = request.META['REMOTE_ADDR']
        print 'request os:%s,addr:%s'%(os,addr)
        #request.
        return 
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print 'process_view1'

    def process_exception(self, request, exception):
        print 'process_exception1'
        pass
     
    def process_response(self, request, response):
        print 'process_response1'
        return response
    
class RequestExeute2(object):
     
    def process_request(self,request):
        print 'process_request2'
        return 
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print 'process_view2'
        i =1
        pass
    def process_exception(self, request, exception):
        print 'process_exception2'
        pass
     
    def process_response(self, request, response):
        print 'process_response2'
        return response