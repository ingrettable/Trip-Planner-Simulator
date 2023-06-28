from abc import ABC, abstractmethod
from typing import List

class pTPS_Transaction(ABC):
    @abstractmethod
    def doTransaction(self):
        pass

    @abstractmethod
    def undoTransaction(self):
        pass

    @abstractmethod
    def toString(self):
        pass

class pTPS:
    def __init__(self):
        self.transactions: List[pTPS_Transaction] = []
        self.numTransactions: int = 0
        self.mostRecentTransaction: int = -1
        self.performingDo: bool = False
        self.performingUndo: bool = False

    def isPerformingDo(self) -> bool:
        return self.performingDo

    def isPerformingUndo(self) -> bool:
        return self.performingUndo

    def hasTransactionToRedo(self) -> bool:
        return (self.mostRecentTransaction + 1) < self.numTransactions

    def hasTransactionToUndo(self) -> bool:
        return self.mostRecentTransaction >= 0

    def getSize(self) -> int:
        return len(self.transactions)

    def getRedoSize(self) -> int:
        return self.getSize() - self.mostRecentTransaction - 1

    def getUndoSize(self) -> int:
        return self.mostRecentTransaction + 1

    def addTransaction(self, transaction):
        while self.hasTransactionToRedo():
            self.transactions.pop()
            self.numTransactions -= 1
        self.numTransactions += 1
        self.transactions.append(transaction)
        self.doTransaction()

    def doTransaction(self):
        if self.hasTransactionToRedo():
            self.performingDo = True
            transaction = self.transactions[self.mostRecentTransaction + 1]
            transaction.doTransaction()
            self.mostRecentTransaction += 1
            self.performingDo = False

    def undoTransaction(self):
        if self.hasTransactionToUndo():
            self.performingUndo = True
            transaction = self.transactions[self.mostRecentTransaction]
            transaction.undoTransaction()
            self.mostRecentTransaction -= 1
        self.performingUndo = False

    def clearAllTransactions(self):
        self.transactions = []
        self.numTransactions = 0
        self.mostRecentTransaction = -1

    def toString(self):
        text = "--Number of Transactions: " + str(self.numTransactions) + '\n'
        text += "--Current Index on Stack: " + str(self.mostRecentTransaction) + '\n'
        text += "--Current Transaction Stack:" + '\n'
        for i in range(self.mostRecentTransaction + 1):
            pT = self.transactions[i]
            text += "----" + pT.toString() + '\n'
        return text
