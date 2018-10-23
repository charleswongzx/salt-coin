from block import Block
import time
import json

class Blockchain:
    def __init__(self):
        self.chain=[self.createGenesisBlock()]
        self.miningReward=100

    def createGenesisBlock(self):
        return Block("01/09/2018", [], "0")

    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]

# add
# fork
# resolve



