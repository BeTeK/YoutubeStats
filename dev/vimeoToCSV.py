import json
import sys

def decodeInput(fObj):
    out = []
    for rawLine in fObj:
        data = json.loads(rawLine)
        yield data

def getLikes(data):
    return int(data["metadata"]["connections"]["likes"]["total"])

def getLink(data):
    return data["link"]

def getDescription(data):
    desc = data["description"]
    if desc is None:
        desc = "No description"
        
    return desc.replace("\n", "\\n").replace("\t", "    ")

def getPlays(data):
    plays = data["stats"]["plays"]
    if plays is None:
        return -1
    else:
        return int(plays)

def getUserName(data):
    return data["user"]["name"]

def getUserUrl(data):
    return data["user"]["link"]

def getUserFollowers(data):
    return int(data["user"]["metadata"]["connections"]["followers"]["total"])
    
def main():
    lineCount = 0
    
    print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format("video url", "likes", "views", "description", "user name", "user url", "followers"))
    sortedInput = sorted(list(decodeInput(sys.stdin)), key=getPlays)
    
    for vidData in sortedInput:
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(getLink(vidData), getLikes(vidData), getPlays(vidData), getDescription(vidData), getUserName(vidData), getUserUrl(vidData), getUserFollowers(vidData)))

        lineCount += 1

        if lineCount % 1000 == 0:
            sys.stderr.write("line: {0}\n".format(lineCount))
        

if __name__ == "__main__":
    main()
