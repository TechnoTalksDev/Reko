import json, requests
import os
ip=input("Server IP: ")
url = "https://api.mcsrvstat.us/2/" + ip
#url = "https://api.mcsrvstat.us/2/mc.hypixel.net"
#url = "https://api.mcsrvstat.us/2/bedwarspractice.club"
thing = requests.get(url)

data = json.loads(thing.content)

debug=True

if debug==True:
    print (data)
else:
    print("Debug is disabled... Enable to see raw data!")

print ("---------------------------------------------------------------------------------------------------------------------------")
print("Server Hostname: " + data["hostname"])
print("Online: {}".format(data["online"]))
print("Naked IP: " + data["ip"])
#print("Player Count: {}".format(data["players"]["online"]))
#print("MOTD: {}".format(data["motd"]["clean"]))
print("Version: {}".format(data["version"]))
print(os.system("ping " + ip))
print ("---------------------------------------------------------------------------------------------------------------------------")
