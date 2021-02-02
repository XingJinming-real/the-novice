# 8queueP
import os
import time


class Queen:
    def __init__(self, queenNum):
        self.queenNum = queenNum
        self.Matrix = []
        self.availabeNum = 0

    def getPrePos(self, i):
        for j in range(self.queenNum):
            if self.Matrix[i - 1][j] == 1:
                return i - 1, j
        return None, None

    def checkIsOk(self, curi, i, j):  # 进行前向检查
        if curi == 0:
            return 1
        prei, prej = self.getPrePos(curi)
        if prei == prej is None:
            return None
        if prei == i or prej == j or abs(prei - i) == abs(prej - j):
            # 如果是对角线即横纵座标差的绝对值相同返回不ok
            return 0
        return self.checkIsOk(curi - 1, i, j)  # 递归进行前向检查，直到检查到第一行

    def setMatrix(self):
        for i in range(self.queenNum):
            temp = []
            for j in range(self.queenNum):
                temp.append(0)
            self.Matrix.append(temp)

    def putQueen(self, i):  # 递归调用,i 表示现在放置第i行皇后
        global isOver
        if isOver is True:
            return 1
        if i >= self.queenNum:
            self.show()
            self.availabeNum += 1
        for j in range(self.queenNum):
            flag = self.checkIsOk(i, i, j)  # 检查是否合理，合理返回1，否则返回0
            if flag == 1:
                self.Matrix[i][j] = 1
                flag = self.putQueen(i + 1)  # 进行第i+1行放置，返回0则不合理，返回1即是到达了边界，故均设为0
                if flag == 0:
                    self.Matrix[i][j] = 0
                elif flag == 1:
                    self.Matrix[i][j] = 0
        return 0

    def show(self):
        for i in range(self.queenNum):
            for j in range(self.queenNum):
                print("{} ".format(self.Matrix[i][j]), end='')
            print("")
        print('\n\n')


def main():
    queenNum = eval(input("请输入皇后数目"))
    queenPosGraph = Queen(queenNum)
    startTime = time.perf_counter()
    queenPosGraph.setMatrix()
    queenPosGraph.putQueen(0)
    endTime = time.perf_counter()
    print("共有{:*^20}种摆法".format(queenPosGraph.availabeNum))
    print("用时{:*^20} s".format(endTime - startTime))
    pass


if __name__ == "__main__":
    while True:
        isOver = False
        main()
