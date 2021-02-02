# 8queenP
import time
import copy
import random


class Queen:
    def __init__(self, queenNum):
        self.queenNum = queenNum
        self.Matrix = []
        self.availabeNum = 0
        self.queenPos = []  # 元组为元素 待完善
        self.curMinCollisionNum = 999
        self.isSucceed = 0

    def countWholeCollision(self, newMatrix):
        wholeCollision = 0
        if newMatrix is None:
            return None
        for i in range(self.queenNum):
            for j in range(self.queenNum):
                if newMatrix[i][j] == 1:
                    wholeCollision += self.countCollision(i, j, newMatrix)
                    break
        return wholeCollision
        # 计算newMatrix总的冲突数

    def moveLeft(self, i, j, n):
        try:
            tempMatrix = copy.deepcopy(self.Matrix)
            tempMatrix[i][j] = 0
            tempMatrix[i][j - n] = 1
            return tempMatrix
        except:
            return None
        # 第i 行j 列的皇后 向左移动n位，i,j 为findShouldMoveIndex确定，n为findMoveToIndex决定

    def moveRight(self, i, j, n):
        try:
            tempMatrix = copy.deepcopy(self.Matrix)
            tempMatrix[i][j] = 0
            tempMatrix[i][j + n] = 1
            return tempMatrix
        except:
            return None
        # 同理moveLeft

    def findShouldMoveIndex(self):
        shouldMoveQueen = []
        for i in range(self.queenNum):
            for j in range(self.queenNum):
                if self.Matrix[i][j] == 1:
                    curNodeCollision = self.countCollision(i, j, self.Matrix)
                    shouldMoveQueen.append([curNodeCollision, i, j])
                    break
        shouldMoveQueen.sort(reverse=True)
        return shouldMoveQueen
        # 找到冲突最多的皇后，由countCollision计算每个皇后的冲突

    def findMoveToIndex(self, i, j):
        collisionLMatrix = 999
        nForL = 0
        nForR = 0
        for n in range(1, j + 1):
            tempCollision = self.countWholeCollision(self.moveLeft(i, j, n))
            if collisionLMatrix > tempCollision:
                collisionLMatrix = tempCollision
                nForL = n
        collisionRMatrix = 999
        for n in range(1, self.queenNum - j):
            tempCollision = self.countWholeCollision(self.moveRight(i, j, n))
            if collisionRMatrix > tempCollision:
                collisionRMatrix = tempCollision
                nForR = n
        if collisionRMatrix > self.curMinCollisionNum and collisionLMatrix > self.curMinCollisionNum:
            return None
        if collisionLMatrix is not None and collisionRMatrix is not None:
            if collisionLMatrix < collisionRMatrix:
                self.curMinCollisionNum = collisionLMatrix
                return -nForL
            else:
                self.curMinCollisionNum = collisionRMatrix
                return nForR
        else:
            if collisionLMatrix is None:
                return 1
            else:
                return -1
        # 找到i行，j列的皇后移动到i行哪个位置冲突最小

    def slightlyMove(self, Times):
        flag = -1
        moveTimes = 0
        while True:
            shouldMoveQueen = self.findShouldMoveIndex()
            while True:
                if flag == -1:
                    shouldMoveQueen = self.findShouldMoveIndex()
                if not shouldMoveQueen or moveTimes > Times:
                    # print("结束".center(20, '*'))
                    break
                curCollisionUseless, shouldMoveIndexI, shouldMoveIndexJ = shouldMoveQueen[0]
                candidate = [shouldMoveQueen[0]]
                shouldMoveQueen.pop(0)
                for i in range(len(shouldMoveQueen)):
                    if shouldMoveQueen[i][0] >= curCollisionUseless:
                        candidate.append(shouldMoveQueen[i])
                curCollisionUseless, shouldMoveIndexI, shouldMoveIndexJ = random.choice(candidate)
                # print("当前shouldMoveQueen长度为",len(shouldMoveQueen),"flag is ",flag)
                tempN = self.findMoveToIndex(shouldMoveIndexI, shouldMoveIndexJ)
                if tempN is None:
                    # print("陷入死循环，正在退火")
                    self.GodHelpMe()
                    flag = 1
                    continue
                self.Matrix[shouldMoveIndexI][shouldMoveIndexJ] = 0
                self.Matrix[shouldMoveIndexI][shouldMoveIndexJ + tempN] = 1
                moveTimes += 1
                if self.countWholeCollision(self.Matrix) == 0:
                    print("\n\n{:*^20}".format("成功"))
                    self.isSucceed = 1
                    self.show()
                    break
                if moveTimes > Times:
                    # print("微调超过{:*^20}次还未成功".format(moveTimes))
                    break
                flag = -1
            break
        pass
        # 微调
        # 微调

    def countCollision(self, i, j, newMatrix):
        if newMatrix is None:
            return None
        originalI = i
        originalJ = j
        curNodeCollision = 0
        for orientI, orientJ in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0)]:
            i = originalI
            j = originalJ
            while True:  # 计算右下等各个方向
                if j + orientJ >= self.queenNum or i + orientI >= self.queenNum or j + orientJ < 0 or i + orientI < 0:
                    break
                if newMatrix[i + orientI][j + orientJ] == 1:
                    curNodeCollision += 1
                i = orientI + i
                j = orientJ + j
        return curNodeCollision
        # 计算i行，j列皇后冲突数

    def setMatrix(self):
        self.Matrix.clear()
        for i in range(self.queenNum):
            temp = []
            for j in range(self.queenNum):
                temp.append(0)
            temp[random.choice([i for i in range(self.queenNum)])] = 1
            self.Matrix.append(temp)
        # 初始化皇后位置矩阵

    def show(self):
        global isOver
        isOver = True
        self.availabeNum += 1
        for i in range(self.queenNum):
            for j in range(self.queenNum):
                print("{} ".format(self.Matrix[i][j]), end='')
            print("")
        print('\n\n')
        # 显示结果

    def GodHelpMe(self):  # 随机选择i，和j 进行调整
        """
        GodChoiceI = random.choice([i for i in range(self.queenNum)])
        for j in range(self.queenNum):
            if self.Matrix[GodChoiceI][j] == 1:
                self.Matrix[GodChoiceI][j] = 0
                break
        GodChoiceJ = random.choice([i for i in range(self.queenNum)])
        self.Matrix[GodChoiceI][GodChoiceJ] = 1
        # 当陷入局部最优时调用，随机选择第i行的皇后移动到第i行，第j列，模拟退火
        """
        # 或进行下面的随机
        candidates = random.sample([i for i in range(10)], 4)
        temp = self.Matrix[candidates[0]]
        self.Matrix[candidates[0]] = self.Matrix[candidates[1]]
        self.Matrix[candidates[1]] = temp
        temp = self.Matrix[candidates[2]]
        self.Matrix[candidates[2]] = self.Matrix[candidates[3]]
        self.Matrix[candidates[3]] = temp


def main():
    queenPos = Queen(queenNum)
    loop = 0
    print("*" * 40)
    startTime = time.perf_counter()
    while queenPos.isSucceed == 0:
        queenPos.setMatrix()
        queenPos.slightlyMove(2 * queenNum)
        loop += 1
        # if loop > 500:
        #     print("Ohh{:*^40}".format("Forgive The Useless God"))
        #     break
        endtime = time.perf_counter()
        if endtime - startTime > 2:
            break
    endTime = time.perf_counter()
    if isOver:
        print("用时{} s".format(endTime - startTime))


if __name__ == "__main__":
    while True:
        isOver = False
        queenNum = eval(input("请输入皇后数目"))
        for i in range(100):
            main()
            if isOver is True:
                break
            print("进行第{:*^20}次重启".format(i))
