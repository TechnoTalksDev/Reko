from mcstatus import MinecraftServer

def latencyr(ip):
    try:
        server = MinecraftServer.lookup(ip+":25565")
        status = server.status()
        ping="{}".format(status.latency)
        return ping
    except:
        return "Fail"
