from apiclient.discovery import build

class Youtube:
    def __init__(self, key):
        self.youtube = build("youtube", "v3", developerKey=key)
        self.gategoryIdCache = {}

    def getChannelPlaylists(self, channelName):
        params = {"part": "id", "maxResults": 50, "channelId": channelName}
        results = self._iterateAllItems(self.youtube.playlists().list, params)

        return [i["id"] for i in results]

    def getItemsInPlaylist(self, playlistId):
        params = {"part": "snippet", "maxResults": 50, "playlistId": playlistId}
        results = self._iterateAllItems(self.youtube.playlistItems().list, params)

        return [i["snippet"]["resourceId"]["videoId"] for i in results]

    def getChannelInfo(self, channelIds):
        results = {}
        for chunk in self._chunks(channelIds, 50):
            for key, value in self._getChannelInfoImpl(chunk).items():
                results[key] = value

        return results

    def _getChannelInfoImpl(self, channelIds):
        params = {"part": "statistics,snippet", "maxResults": 50, "id": ",".join(channelIds)}
        results = self._iterateAllItems(self.youtube.channels().list, params)
        
        return {i["id"] : {"statistics": i["statistics"], "snippet": i["snippet"]} for i in results}
        
    
    def getVideoStatistics(self, videoIds):
        results = {}
        for chunk in self._chunks(videoIds, 50):
            for key, value in self._getVideoStatisticsImpl(chunk).items():
                results[key] = value

        return results
    
    def _getVideoStatisticsImpl(self, videoIds):
        params = {"part": "statistics,snippet", "maxResults": 50, "id": ",".join(videoIds)}
        results = self._iterateAllItems(self.youtube.videos().list, params)
        
        return {i["id"] : {j[0] : j[1] for j in list(i["statistics"].items()) + list(i["snippet"].items())} for i in results}


    def getVideoGategory(self, gategoryId):
        if gategoryId not in self.gategoryIdCache:
            result = self.youtube.videoCategories().list(part="snippet", hl="en_US", id=gategoryId).execute()
            self.gategoryIdCache[gategoryId] = result["items"][0]["snippet"]["title"]

        return self.gategoryIdCache[gategoryId]

    def getChannelId(self, nameOrId):
        user = self.youtube.channels().list(part="id", forUsername=nameOrId).execute()
        chId = self.youtube.channels().list(part="id", id=nameOrId).execute()

        if len(user["items"]) > 0:
            return user["items"][0]["id"]
        if len(chId["items"]) > 0:
            return chId["items"][0]["id"]
        
        raise Exception("Cannot find id for channel {0}".format(nameOrId))

    def _iterateAllItems(self, fn, params):
        results = fn(**params).execute()
        
        out = results["items"]
        
        if "nextPageToken" in results:
            nextParams = dict(params)
            nextParams["pageToken"] = results["nextPageToken"]
            
            out += self._iterateAllItems(fn, nextParams)

        return out


    def _chunks(self, l, n):
        n = max(1, n)
        return (l[i:i+n] for i in range(0, len(l), n))
    
