import json
import sys

def parseAllUsers(data):
    users = {}

    for video in data:
        userUrl = video["user"]["link"]
        if userUrl not in users:
            users[userUrl] = {"name" : video["user"]["name"], "videos" : []}

        users[userUrl]["videos"].append(video)

    return users

def countLikes(data):
    total = 0
    for i in data["videos"]:
        total += int(i["metadata"]["connections"]["likes"]["total"])

    return total

def gategories(data):
    cat = set()
    for i in data["videos"]:
        for tag in i["tags"]:
            if tag is not None:
                cat.add(tag["name"])

    return cat

def parseVideoData(data):
    followers = data["videos"][0]["user"]["metadata"]["connections"]["followers"]["total"]
    likes = countLikes(data)
    videos = len(data["videos"])
    cat = gategories(data)
    
    return {"followers" : followers, "likes" : likes, "videos" : videos, "tags" : cat}

def formatTags(tags):
    txt = ""
    for i in tags:
        if len(txt) != 0:
            txt += ", "

        txt += i

    return txt

def main():
    data = None
    with open(sys.argv[1], "rb") as f:
        data = json.loads(f.read())

    users = parseAllUsers(data)
    print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format("user url", "user name", "followers", "likes", "videos", "tags"))
    for url, videoData in users.items():
        sums = parseVideoData(videoData)
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(url, videoData["name"], sums["followers"], sums["likes"], sums["videos"], formatTags(sums["tags"])))

    
    
    
if __name__ == "__main__":
    main()


    
