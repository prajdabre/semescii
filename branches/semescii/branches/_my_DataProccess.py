# !-- coding: UTF-8 --!

class DataProccess():
       
    @staticmethod
    def encode(params):
        return ";".join(["%s=%s" % (k, v) for k, v in params.items()])
    
    @staticmethod
    def decode(data):
        params = {}
        for string in data.split(';') : 
            k,v = string.split('=')
            params[k] = v
    
        return params
    
