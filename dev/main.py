import apiKey
import Youtube
import googleapiclient
import googleapiclient.errors
import sys

def countGategories(stats):
    results = {}
    for key, value in stats.items():
        if value["categoryId"] not in results:
            results[value["categoryId"]] = 0
        results[value["categoryId"]] += 1

    return results
        

def gatherChannelVideoData(youtube, channelId):
    playlists = youtube.getChannelPlaylists(channelId)
    itemsInPlaylist = list(set([videoId for playlistId in playlists for videoId in youtube.getItemsInPlaylist(playlistId)]))
    stats = youtube.getVideoStatistics(itemsInPlaylist)

    likes = sum([int(valueIfInDistOrDefault(i, "likeCount", 0)) for i in stats.values()])
    dislikes = sum([int(valueIfInDistOrDefault(i, "dislikeCount", 0)) for i in stats.values()])
    views = sum([int(valueIfInDistOrDefault(i, "viewCount", 0)) for i in stats.values()])
    videoCount = len(itemsInPlaylist)
    gategories = countGategories(stats)

    return {"likes" : likes, "dislikes" : dislikes, "views" : views, "videoCount" : videoCount, "gategories" : gategories}

def valueIfInDistOrDefault(d, k, default):
    return d[k] if k in d else default

def gatherChannelInfo(youtube, channelId):
    info = youtube.getChannelInfo([channelId])
    subCount = int(info[channelId]["statistics"]["subscriberCount"]) if not info[channelId]["statistics"]["hiddenSubscriberCount"] else None
    title = info[channelId]["snippet"]["title"]
    description = info[channelId]["snippet"]["description"].replace("\n", "\\n")
    
    return {"subCount" : subCount, "title": title, "description" : description}

def gatherAllChannelInfo(youtube, channelNameOrId):
    try:
        channelId = youtube.getChannelId(channelNameOrId)
        videoData = gatherChannelVideoData(youtube, channelId)
        channelData = gatherChannelInfo(youtube, channelId)
        
        gategories = sorted(list(videoData["gategories"].items()), key=lambda i:i[1])
        gategories = list(reversed([(youtube.getVideoGategory(i[0]), i[1]) for i in gategories]))
        topGategories = [i[0] for i in gategories[:3]]
        
        out = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(channelData["title"], channelData["subCount"], videoData["likes"], videoData["dislikes"], videoData["views"], videoData["videoCount"], channelData["description"], "\t".join(topGategories))
        sys.stdout.write(out)
    except Exception as ex:
        print(ex)
        print("Failed. video id {0}".format(channelNameOrId))
        raise ex
    
def main():
    youtube = Youtube.Youtube(apiKey.apiKey)
    sys.stdout.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format("title", "subcriber count", "likes", "dislikes", "views", "video count", "description", "top gategories"))
    for i in sys.stdin:
        sys.stderr.write("processing {0}".format(i))
        channelName = i.replace("\n", "").replace("\r", "")
        if len(i) == 0 or i.startswith("#"):
            continue

        gatherAllChannelInfo(youtube, channelName)
        sys.stdout.flush()
    

if __name__ == "__main__":
    main()
