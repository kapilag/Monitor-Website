
class FactoryObj:
    obj_list = []
    def getModel(self, url):
        for map in FactoryObj.obj_list:
            if url in map:
                return map[url]
        obj = URLMeta(url)
        FactoryObj.obj_list.append({url:obj})
        return obj

    def getModelList(self):
        return FactoryObj.obj_list


class URLMeta:

    def setStatusResult(self,result):
        self.prev_status_cond = self.status_cond
        self.status_cond = result

    def getCurrentStatusResult(self):
        return self.status_cond

    def getPrevStatusResult(self):
        return self.prev_status_cond

    def setPageLoadResult(self, result):
        self.prev_pageLoadedResult = self.pageLoadedResult
        self.pageLoadedResult = result

    def getCurrentPageLoadResult(self):
        return self.pageLoadedResult

    def getPrevPageLoadResult(self):
        return self.prev_pageLoadedResult

    def setTimeToLoad(self,time):
        self.prev_time_to_load = self.time_to_load
        self.time_to_load = time

    def getTimeToLoad(self):
        return self.time_to_load

    def getPrevTimeToLoad(self):
        return self.prev_time_to_load

    def getUrl(self):
        self.url

    def __init__(self, url):
        self.url = url
        self.status_cond = 'FirstRun'
        self.pageLoadedResult = 'FirstRun'
        self.time_to_load = 'FirstRun'
