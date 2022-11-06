import xml.etree.ElementTree as ET
from sortedcontainers import SortedDict
import datetime
import time

start = time.time()
print(f"Processing started at: {datetime.datetime.now()}")
mytree = ET.parse('orders.xml')
myroot = mytree.getroot()

class OrderBook:

    buyList = []
    sellList = []

    def __init__(self, book):
        self.bookid = book

    def insertBuy(self, volume, price, orderId):

        if(len(self.sellList)!=0):
            ind = -1
            for i in range(len(self.sellList)):
                if(self.sellList[i][1]<=price):
                    vol = min(volume, self.sellList[i][0])
                    volume-=vol
                    self.sellList[i]=(self.sellList[i][0]-vol, self.sellList[i][1], self.sellList[i][2])
                    if(self.sellList[i][0]==0):
                        ind = i
                if(volume==0):
                    break
            self.sellList = self.sellList[ind+1:]
    
        if(volume!=0):
            flag = False
            for i in range(len(self.buyList)):
                if(self.buyList[i][1]<price):
                    self.buyList.insert(i, (volume,price,orderId))
                    flag = True
                    break
            if(not flag):
                self.buyList.append((volume,price,orderId))

    def delete(self, orderId):
        for i in range(len(self.sellList)):
            if(self.sellList[i][2]==orderId):
                del self.sellList[i]
                break

        for i in range(len(self.buyList)):
            if(self.buyList[i][2]==orderId):
                del self.buyList[i]
                break

    def insertSell(self, volume, price, orderId):

        if(len(self.buyList)!=0):
            ind = -1
            for i in range(len(self.buyList)):
                if(price<=self.buyList[i][1]):
                    vol = min(volume, self.buyList[i][0])
                    volume-=vol
                    self.buyList[i]=(self.buyList[i][0]-vol, self.buyList[i][1], self.buyList[i][2])
                    if(self.buyList[i][0]==0):
                        ind = i
                if(volume==0):
                    break
            self.buyList = self.buyList[ind+1:]
    
        if(volume!=0):
            flag = False
            for i in range(len(self.sellList)):
                if(self.sellList[i][1]>price):
                    self.sellList.insert(i, (volume,price,orderId))
                    flag = True
                    break
            if(not flag):
                self.sellList.append((volume,price,orderId))

database = SortedDict()

for i in myroot:
    if(i.tag=="AddOrder"):
        book = i.attrib['book']
        volume = int(i.attrib['volume'])
        price = float(i.attrib['price'])
        orderId = int(i.attrib['orderId'])
        operation = i.attrib['operation']
        if book not in database.keys():
            database[book] = OrderBook(book)
        if(operation=="SELL"):
            database[book].insertSell(volume, price, orderId)
        else:
            database[book].insertBuy(volume, price, orderId)
    else:
        database[i.attrib['book']].delete(int(i.attrib['orderId']))


for i in database:
    print("book: "+i)
    j = database[i]
    print("\t\t  Buy -- Sell")
    print("---------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------")
    l1 = len(j.buyList)
    l2 = len(j.sellList)
    sz = max(l1,l2)
    for k in range(sz):
        if(k<l1 and k<l2):
            print(f"\t\t{j.buyList[k][0]}@{j.buyList[k][1]} -- {j.sellList[k][0]}@{j.sellList[k][1]}")
        elif(k<l1):
            print(f"\t\t{j.buyList[k][0]}@{j.buyList[k][1]} --")
        else:
            print(f"\t\t\t -- {j.sellList[k][0]}@{j.sellList[k][1]}")
    print()

print(f"Processing completed at: {datetime.datetime.now()}")
end = time.time()
print(f"Total Execution time in seconds: {(end-start)}")