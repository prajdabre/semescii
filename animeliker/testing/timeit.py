import logging
import time
def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        msg = '%r %2.2f sec' % \
              (method.__name__, te-ts)
        
        LOG_FILENAME = '/var/www/log.out'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
        logging.debug(msg)  
        
        return result

    return timed