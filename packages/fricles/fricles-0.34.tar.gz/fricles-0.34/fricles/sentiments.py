import copy
import requests

class sentiments(object):

    def __init__(self):
        self.url = "http://fricles.com:8080/fricles/api/v1/get_sentiments"
        return
    
    def get_sentiments(self, text):
        """
        Extract sentiments and keywords from english text.

        Parameters
        ----------
        text : string
                Text for which sentiments has to be extracted
        
        Returns
        ----------
        dict
                "status" : dict containing status_code and status_string
                "output" : dict contains a list of keywords and sentiments with a breakup of sentiments into positive, negative and neutral categories

                example: {"status": {"status_code": 0, "status_string": "success"}, "output": {"keywords": ["movie", "good"], "sentiments": {"positive": 0.0, "neutral": 25.0, "negative": 75.0}}}
        """
        try:
            r = requests.post(self.url, data={'text':text})
            return r
        except Exception, err:
            return {"status" : "Failed", "http_code" : err.code, "message" : err.message}
