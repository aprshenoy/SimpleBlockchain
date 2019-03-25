
import uuid
import hashlib
import binascii
import datetime
import collections
from collections import OrderedDict
import json

#Helper
def doubleSha256(hex):
    bin = binascii.unhexlify(hex)
    hash = hashlib.sha256(bin).digest()
    hash2 = hashlib.sha256(hash).digest()
    return hash2
#Helper ends here

#Class declarations
class Header:
    Version = 0
    hashPrevBlock = ""
    Timestamp = ''
    Bits = None
    hashMerkRoot = ""
    Nonce = 0

    def __init__(self, hash, Ver):
        self.Version = Ver
        self.hashPrevBlock = hash
        self.Timestamp = str(datetime.datetime.now())
        self.Bits = 0
        self.Nonce = 0

    def hash(self):
        h = hashlib.sha256()
        h.update(str(self.Nonce).encode('utf-8') +
                 str(self.Bits).encode('utf-8') +
                 str(self.hashPrevBlock).encode('utf-8') +
                 str(self.Timestamp).encode('utf-8')
                 )
        return h.hexdigest()

    def updateHashmerkRoot(self, newTransactionHash):
        hashMerkRoot = hashMerkRoot+newTransactionHash


class Transaction:
    VersionNumber = 0
    InCounter = 0
    ListOfInputs = 0
    OutCounter = 0
    ListOfOutputs = 0
    TransactionHash = 0

    def _init_(self):
        VersionNumber = 0
        InCounter = 0
        ListOfInputs = []
        OutCounter = 0
        ListOfOutputs = []
        TransactionHash = 0

    def hash(self):
        h = hashlib.sha256()
        h.update(str(self.VersionNumber).encode('utf-8') +
                 str(self.InCounter).encode('utf-8') +
                 str(self.ListOfInputs).encode('utf-8') +
                 str(self.ListOfOutputs).encode('utf-8')
                 )
        return h.hexdigest()

    def printTransaction():
        print("this shit is a transaction")


class Block:
    MagicNumber = 0
    Blocksize = 0
    BlockHeader = None
    TransactionCounter = 0
    Transaction = []
    Blockhash = None
    PreviousHash = None
    blockHeight = 0

    def hash(self):
        h = hashlib.sha256()

    def __init__(self, PreviousHash, Version):
        self.MagicNumber = uuid.uuid4().hex
        self.Blocksize = 0
        self.TransactionCounter = 0
        self.Transaction = []
        self.BlockHeader = Header(PreviousHash, Version)
        self.Blockhash = self.BlockHeader.hash()

    def submit_transaction(self, sender_address, recipient_address, value, signature):
        transaction = OrderedDict(
            {'sender_address': sender_address, 'recipient_address': recipient_address})
        h = hashlib.sha256()
        h.update(str(transaction).encode('utf-8'))
        self.Transaction.append(h.hexdigest())

    def isBlockOutOfCapacity(self):
        if(self.Transaction.__len__() >= 5 or self.BlockHeader.hashPrevBlock == "000000000000000000000000000000"):
            return True
        return False

    def printBlock(self):
        print("Block Hash :", self.Blockhash)
        print("Header")
        print("----------------------------")
        print("TimeStamp :", self.BlockHeader.Timestamp)
        print("HashMerkRoot :", self.BlockHeader.hashMerkRoot)
        print("----------------------------")
        print("Height :",self.blockHeight)
        print("Transactions :", self.Transaction)
        print("previous block :", self.PreviousHash)


class BlockChain:
    block = None
    chain = []  # not nessesary just to keep track and used to store the blocks . We as of now dont have anyother mechanish to keep track of individual bloaks

    def __init__(self):
        genesis = Block("000000000000000000000000000000", 1)
        self.chain.append(genesis)  # first block will be genesis block
        self.block = genesis

    def addBlock(self):
        newBlock = Block(self.block.Blockhash, 1)
        height = self.block.blockHeight
        newBlock.blockHeight = height + 1
        newBlock.PreviousHash = self.block.Blockhash
        self.chain.append(newBlock)
        self.block = newBlock

    def submitTransaction(self, sender, reciever, value):
        # this method will check number of transactions in the block and verify if it can contain more, if it cannot (for now iam manually adding a new block
        if(self.block.isBlockOutOfCapacity()):
            self.addBlock()  # adding a block manually
        self.block.submit_transaction(
            sender, reciever, value, 'sendersignature')

    def getBlockChainHeight(self):
        return self.block.blockHeight

    def findBlockByHeight(self):
        height = input("Enter Block Height :")

        filtered = [x for x in self.chain if str(x.blockHeight) == height]
        if filtered.__len__() > 0:
            filtered[0].printBlock()
        else:
            print("No Block with height ",height," found")
            


    def findBlockByHash(self):
        hashval = input("Enter Block Hash :")
        filtered = [x for x in self.chain if str(x.Blockhash) == hashval]
        if filtered.__len__() > 0:
            filtered[0].printBlock()
        else:
            print("no block with Hasvalue ",hashval," found")
           
    def printBlockchain(self):
        for i in range(self.chain.__len__()):
            print()
            print()
            print("Block ", i)
            print("*****************************************************")
            self.chain[i].printBlock()

            print("*****************************************************")


    def getUserInput(self):
        print()
        print("* Press 1 for viewing all available blocks in this chain")
        print("* Press 2 for finding block by height ")
        print("* Press 3 for finding block by block Hash")
        print("* Press any other key to exit")
        choice = input("Please enter your choice :")
        return choice


    def processInput(self,val):
        if val == str(1):
            self.printBlockchain()
        elif val==str(2):
            self.findBlockByHeight()
        elif val==str(3):
            self.findBlockByHash()
        
        self.doOperation(val)

    
    def doOperation(self,choice):
        print() #newline
        if(choice in [str(1),str(2),str(3)]):
            choice = self.getUserInput()
            self.processInput(choice)

#Class declaration ends here



def main():
    chain1 = BlockChain()
    # adding 10 transactions
    for i in range(10):
        chain1.submitTransaction('sender', 'reciever', i)
    print("Hello!! Welcome to a simple block chain data structure :-) ")
    print("Now in this test POC we have a simple block chain designed and is ready for adding more transactions and blocks")
    
    chain1.doOperation("1") # adding this function to the scope of the object to get persisted data to do one round of operation. this actually should be actually out of object scope
    # chain1.printBlockchain()


main()
