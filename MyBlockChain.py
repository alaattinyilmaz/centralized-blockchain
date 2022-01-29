import Pyro4
import threading

class MyBlock:
    def __init__(self, tx=None):
        self.tx = tx
        self.next = None

@Pyro4.expose
class MyBlockChain:
    def __init__(self, chainName):
        self.head = None
        self.chainName = chainName
        self.mutex = threading.Lock()

    def createAccount(self, amount: int):
        ptr = self.head
        _max = 0

        while(ptr is not None):
            accountNumber = ptr.tx[1][0]
            
            if(accountNumber > _max):
                _max = accountNumber
            
            ptr = ptr.next
        
        newAccountNumber = _max+1
        newNode = MyBlock(("CREATEACCOUNT",(newAccountNumber,amount)))
        self.insert(newNode)

        return newAccountNumber
    
    
    def transfer(self, _from: int, to: int, amount: int):

        if(self.isExist(_from) == -1 or self.isExist(to) == -1):
            return -1
        
        if(amount > 0):
            sender = _from
        else:
            sender = to
        
        if(self.calculateBalance(sender) < abs(amount)):
            return -1
        
        newNode = MyBlock(("TRANSFER",(_from,to,amount)))
        self.insert(newNode)
        return 1


    def calculateBalance(self, accountNumber : int):
        
        ptr = self.head
        balance = 0

        while(ptr is not None):
            
            txType = ptr.tx[0]
            
            if(txType == "CREATEACCOUNT"):
                txAccountNumber = ptr.tx[1][0]
                if(txAccountNumber == accountNumber):
                    txAmount = ptr.tx[1][1]
                    balance += txAmount

            elif(txType == "TRANSFER"):
                txAccountNumberFrom, txAccountNumberTo, transferAmount  = ptr.tx[1][0], ptr.tx[1][1], ptr.tx[1][2]

                if(txAccountNumberFrom == accountNumber):
                    if(transferAmount > 0):
                        balance -= abs(transferAmount)
                    else:
                        balance += abs(transferAmount)
                if(txAccountNumberTo == accountNumber):
                    if(transferAmount > 0):
                        balance += abs(transferAmount)
                    else:
                        balance -= abs(transferAmount)

            elif(txType == "EXCHANGE"):
                txAccountNumberFrom, txAccountNumberTo, toChain, transferAmount = ptr.tx[1][0], ptr.tx[1][1], ptr.tx[1][2], ptr.tx[1][3]
                if(txAccountNumberFrom == accountNumber):
                    if(transferAmount > 0):
                        balance -= abs(transferAmount)
                    else:
                        balance += abs(transferAmount)

            ptr = ptr.next
        
        return balance

    # Inserting at the begining of the chain
    def insert(self, newNode):
        if(self.head == None):
            self.head = newNode
        else:
            newNode.next = self.head
            self.head = newNode

    def isExist(self, accountNumber : int):
        ptr = self.head

        while(ptr is not None):
            
            txType = ptr.tx[0]
            
            if(txType == "CREATEACCOUNT"):
                txAccountNumber = ptr.tx[1][0]
                if(txAccountNumber == accountNumber):
                    return 1

            ptr = ptr.next
        
        return -1

    def exchange(self, _from, to, toChain, amount):

        self.mutex.acquire()
        if(self.isExist(_from) == -1 or toChain.isExist(to) == -1):
            self.mutex.release()
            return -1
        
        if(amount > 0):
            sender = _from
            senderChain = self
        else:
            sender = to
            senderChain = toChain
        
        if(senderChain.calculateBalance(sender) < abs(amount)):
            self.mutex.release()
            return -1

        newNode =  MyBlock(("EXCHANGE",(_from, to, toChain, amount)))
        self.insert(newNode)

        newNodeToOtherChain = MyBlock(("EXCHANGE",(to, _from, self, -amount)))
        toChain.insert(newNodeToOtherChain)
        self.mutex.release()
        return 1
    
    def printChain(self):
        ptr = self.head
        while(ptr is not None):
            txType = ptr.tx[0]
            if(txType == "EXCHANGE"):
                tx = ptr.tx
                print((tx[0],(tx[1][0],tx[1][1],tx[1][2].chainName,tx[1][3])))
            else:
                print(ptr.tx)
            ptr = ptr.next

def mytrial():
    BTCChain = MyBlockChain("BTCChain")
    ETHChain = MyBlockChain("ETHChain")

    BTCChain.createAccount(100) # 1
    BTCChain.createAccount(100) # 2
    BTCChain.createAccount(100) # 3
    BTCChain.createAccount(100) # 4

    ETHChain.createAccount(100) # 1
    ETHChain.createAccount(100) # 2
    ETHChain.createAccount(100) # 3
    ETHChain.createAccount(100) # 4

    BTCChain.transfer(1,1,25)
    BTCChain.transfer(1,2,25)
    BTCChain.transfer(1,2,25)
    BTCChain.exchange(1,2,ETHChain,25)

    print("BTC Chain")
    BTCChain.printChain()

    print("ETH Chain")
    ETHChain.printChain()

    print(BTCChain.calculateBalance(1))

    print(ETHChain.calculateBalance(2))

mytrial()