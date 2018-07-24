import apiKey
import Vimeo
import json
import sys

def reportFn(data):
    sys.stdout.write(json.dumps(data) + "\n")

def main():
    vimeo = Vimeo.Vimeo(apiKey.vimeoClientId, apiKey.vimeoClientSecret)
    vimeo.getVideos("review", reportFn)
        

if __name__ == "__main__":
    main()
