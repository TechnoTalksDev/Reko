import urllib.request
import json

def getsubs():
    data = urllib.request.urlopen("https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UCHZEwmLpm3O69jfV2_bIbLA&key=AIzaSyAykMmQaNVVWEGmXeYRfzzg5uuY7wdJBX4").read()
    subsraw = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    subs = "{:,d}".format(int(subsraw))
    print("Subs: "+subs)
    return subs

print(getsubs())