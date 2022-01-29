import Pyro4
Pyro4.config.SERIALIZER = 'pickle'
from MyBlockChain import MyBlockChain

BTC = MyBlockChain("BTC")

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(BTC)   # register the greeting maker as a Pyro object
ns.register("BTC", uri)   # register the object with a name in the name server
print("BTC Server has started!")
daemon.requestLoop()                   # start the event loop of the server to wait for calls