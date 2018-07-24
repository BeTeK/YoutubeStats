import vimeo
import json
import time
import urllib
import urllib.parse
import sys
import time

class Vimeo:
    def __init__(self, clientId, clientSecret):
        self.vimeo = vimeo.VimeoClient(key=clientId, secret=clientSecret)
        self.vimeo.load_client_credentials()
        

    def getVideos(self, queryTxt, loadedVideoReportFn):
        qurl = "/videos"
        data = {"query" : queryTxt, \
                "direction" : "desc", \
                "sort" : "likes"}
        
        self.__loadAll__(qurl, data, loadedVideoReportFn)

    def __loadAll__(self, query, dataIn, loadedVideoReportFn):
        pageNum = 1
        lastPage = None
        startTime = time.time()
        
        while lastPage is None or pageNum <= lastPage:
            data = dict(dataIn)
            data["page"] = "{0}".format(pageNum)
            data["per_page"] = "{0}".format(100)
            
            content = json.loads(self.__makeQuerty(query, data))

            lastPageUrl = urllib.parse.urlparse(content["paging"]["last"])
            lastPageParams = urllib.parse.parse_qs(lastPageUrl.query)
            lastPage = int(lastPageParams["page"][0])

            for videoData in content["data"]:
                loadedVideoReportFn(videoData)
            
            sys.stderr.write("page {0}/{1}, ellapsed: {2}\n".format(pageNum, lastPage, time.time() - startTime))
            pageNum += 1

 
    def __makeQuerty(self, queryUrl, data):
        sleepTime = 1
        respCode = None
        resp = None
        
        while respCode != 200:
            try:
                resp = self.vimeo.get(queryUrl + "?" + urllib.parse.urlencode(data))
                respCode = resp.status_code
            except:
                pass
            
            if respCode != 200:
                sys.stderr.write("failed {0} - {1}. retrying\n".format(data, respCode))
                time.sleep(sleepTime)
                sleepTime = sleepTime * 5
                if sleepTime > 60 * 60:
                    sleepTime = 60 * 60
            
        return resp.content
