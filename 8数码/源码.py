# 8P PrimeBFS
import time


class State:
    def __init__(self, stateNum=None, g=9999, h=9999):
        self.G = g  # 此为父亲状态至当前状态的花费
        self.H = h  # 此为当前状态至目标状态的预估花费
        self.F = g + h  # 此为总花费
        # 以上三个属性会在A*中使用
        self.stateNum = stateNum  # Xing Jinming
        self.depth = 0  # 供DFS确定当前节点在第几层


class Solution:
    def __init__(self, stateNum, goalNum, depth):
        self.stateNum = stateNum  # 初始状态码
        self.goalNum = goalNum  # 目标状态码
        self.checkedForDFS = []  # 供DFS使用的检查列表
        self.flag = 0  # 作为DFS结束的标志
        self.pathForDFS = {}  # 供DFS存储路径
        self.depth = depth  # 供DFS使用的深度
        # Xing Jinming

    def down(self, stateNum):
        if stateNum == self.goalNum:
            return self.goalNum
        if stateNum.find('0') > 5 or None:
            return
        curPos = stateNum.find('0')
        curval = stateNum[curPos + 3]
        stateNum = stateNum.replace("0", 't')
        stateNum = stateNum.replace(stateNum[curPos + 3], '0')
        stateNum = stateNum.replace('t', curval)
        return stateNum

    def up(self, stateNum):
        if stateNum == self.goalNum:
            return self.goalNum
        if stateNum.find('0') <= 2 or None:
            return
        curPos = stateNum.find('0')
        curval = stateNum[curPos - 3]
        stateNum = stateNum.replace("0", 't')
        stateNum = stateNum.replace(stateNum[curPos - 3], '0')
        stateNum = stateNum.replace('t', curval)
        return stateNum

    def left(self, stateNum):
        if stateNum == self.goalNum:
            return self.goalNum
        if stateNum.find('0') in (0, 3, 6) or None:
            return
        curPos = stateNum.find('0')
        curval = stateNum[curPos - 1]
        stateNum = stateNum.replace("0", 't')
        stateNum = stateNum.replace(stateNum[curPos - 1], '0')
        stateNum = stateNum.replace('t', curval)
        return stateNum

    def right(self, stateNum):
        if stateNum == self.goalNum:
            return self.goalNum
        if stateNum.find('0') in (2, 5, 8) or None:
            return
        curPos = stateNum.find('0')
        curval = stateNum[curPos + 1]
        stateNum = stateNum.replace("0", 't')
        stateNum = stateNum.replace(stateNum[curPos + 1], '0')
        stateNum = stateNum.replace('t', curval)
        return stateNum

    def resolveBFS(self):
        path = {}
        path[self.stateNum] = None
        existedNum = [None, ]
        curState = State(self.stateNum)
        queue = []
        queue.append(curState)
        while queue:
            curState = queue.pop(0)
            curStateNum = curState.stateNum
            existedNum.append(curStateNum)
            if curStateNum is None:
                continue
            if curStateNum == self.goalNum:
                print("BFS找到解")
                self.showpath(path)
                return
            upState = State(self.up(curStateNum))
            if upState.stateNum not in existedNum:
                path[upState.stateNum] = curStateNum
                queue.append(upState)
            downState = State(self.down(curStateNum))
            if downState.stateNum not in existedNum:
                path[downState.stateNum] = curStateNum
                queue.append(downState)
            leftState = State(self.left(curStateNum))
            if leftState.stateNum not in existedNum:
                path[leftState.stateNum] = curStateNum
                queue.append(leftState)
            rightState = State(self.right(curStateNum))
            if rightState.stateNum not in existedNum:
                path[rightState.stateNum] = curStateNum
                queue.append(rightState)

    def resolveDFS(self, curState):
        if self.flag == 1:
            return
        if curState.stateNum == self.goalNum:
            self.flag = 1
            return
        if curState.depth > self.depth or curState.stateNum in self.checkedForDFS:
            return
        self.checkedForDFS.append(curState.stateNum)
        if self.up(curState.stateNum) is not None:
            upState = State(self.up(curState.stateNum))
        else:
            upState = None
        if self.down(curState.stateNum) is not None:
            downState = State(self.down(curState.stateNum))
        else:
            downState = None
        if self.left(curState.stateNum) is not None:
            leftState = State(self.left(curState.stateNum))
        else:
            leftState = None
        if self.right(curState.stateNum) is not None:
            rightState = State(self.right(curState.stateNum))
        else:
            rightState = None
        for step in (upState, downState, leftState, rightState):
            if step is None or step.stateNum in self.checkedForDFS:
                continue
            self.pathForDFS[step.stateNum] = curState.stateNum
            step.depth = curState.depth + 1
            self.resolveDFS(step)
            if self.flag == 1:
                return

    def A_star(self, beginH):
        path = {}
        path[self.stateNum] = None
        beginState = State(self.stateNum, 0, beginH)
        openList = []  # 每次自动排序，前面为最小值存储状态
        closeListStateNum = []  # 存储状态码
        openListStateNum = []  # 存储状态码
        openList.append(beginState)
        openListStateNum.append(beginState.stateNum)
        while openList:
            curState = openList.pop(0)
            curStateNum = curState.stateNum
            if curStateNum == self.goalNum:
                print("A_star找到解\n")
                self.showpath(path)
                return
            closeListStateNum.append(curStateNum)
            if self.up(curState.stateNum) is not None:
                upState = State(self.up(curState.stateNum), curState.G + 1,
                                self.countAggregateH(self.up(curState.stateNum)))
            else:
                upState = None
            if self.down(curState.stateNum) is not None:
                downState = State(self.down(curState.stateNum), curState.G + 1,
                                  self.countAggregateH(self.down(curState.stateNum)))
            else:
                downState = None
            if self.left(curState.stateNum) is not None:
                leftState = State(self.left(curState.stateNum), curState.G + 1,
                                  self.countAggregateH(self.left(curState.stateNum)))
            else:
                leftState = None
            if self.right(curState.stateNum) is not None:
                rightState = State(self.right(curState.stateNum), curState.G + 1,
                                   self.countAggregateH(self.right(curState.stateNum)))
            else:
                rightState = None
            for item in (upState, downState, leftState, rightState):
                if item is None or item.stateNum in closeListStateNum:
                    continue
                if item.stateNum not in openListStateNum:
                    path[item.stateNum] = curStateNum
                    openList.append(item)
                    openListStateNum.append(item.stateNum)
                    openList = sorted(openList, key=lambda x: x.F)  # 每次保证排序
                elif item.G > curState.G + 1:
                    path[item.stateNum] = curStateNum
                    item.G = curState.G + 1
                    item.F = item.G + item.H
                    openList = sorted(openList, key=lambda x: x.F)  # 每次保证排序
        return None  # 2019284091 邢金明

    def isSovelable(self, num):  # 返回逆序数
        result = 0
        numTemp = list(num)
        numTemp.remove('0')
        numTemp = list(numTemp)
        for i in range(8):
            for j in range(7 - i):
                if numTemp[7 - i] < numTemp[j]:
                    result += 1
        return result

    def countAggregateH(self, curNum):  # 计算启发函数1模式下的H（n)
        if curNum is None:
            return 9999  # 假定9999为正无穷
        Sum = 0
        for eachnum in curNum:
            x_cur, y_cur = divmod(curNum.find(eachnum), 3)
            x_goal, y_goal = divmod(self.goalNum.find(eachnum), 3)
            Sum += (abs(x_cur - x_goal) + abs(y_goal - y_cur))
        return Sum  # 2019284091 邢金明

    def countNotProper(self, curNum):
        if curNum is None:
            return 9999
        Sum = 0
        for i in range(9):
            if curNum[i] != self.goalNum[i]:
                Sum += 1
        return Sum  # 2019284091 邢金明

    def showpath(self, path):  # 为所有方法输出步骤,没有输出起始和目标状态
        sta = []
        goal = self.goalNum
        subloop = 0
        loop = 1
        while goal is not None:
            sta.append(goal)
            goal = path[goal]
        while sta:
            print("第{}步".format(loop))
            for pernum in sta.pop():
                print(pernum, end=' ')
                subloop += 1
                if subloop % 3 == 0:
                    print('')
            loop += 1


def main():
    # 初始化
    stateNum = input("请输入起始状态码(为一串数字，从左到右从上到下，如123456780表示：\n1 2 3\n4 5 6\n7 8 0\n：")
    goalNum = input("请输入目标状态码(同上）")
    searchDepth = eval(input("请输入DFS的搜索深度"))
    solution = Solution(stateNum, goalNum, searchDepth)  # 实例化solution类

    checkstateNum = solution.isSovelable(stateNum)
    checkgoalNum = solution.isSovelable(goalNum)
    if checkgoalNum % 2 != checkstateNum % 2:  # 以上三行用于判断是否可解
        print("不可解")
        return

    # A_star
    startTime = time.perf_counter()
    beginH = solution.countAggregateH(stateNum)
    # 如果是启发2则为
    # beginH=solution.countNotProper(stateNum)
    solution.A_star(beginH)
    endTime = time.perf_counter()
    print("A_star用时{} s".format(endTime - startTime))

    # DFS
    startTime = time.perf_counter()
    startState = State(stateNum)
    solution.pathForDFS[stateNum] = None
    solution.resolveDFS(startState)
    endTime = time.perf_counter()
    if solution.flag == 0:
        print("\nDFS无法找到解（原因可能为设置的搜索深度太小")
    else:
        print("\nDFS找到解")
        solution.showpath(solution.pathForDFS)
    print("DFS总用时{} s\n".format(endTime - startTime))

    # BFS
    print("BFS可能时间较长，请等待".center(20, '*'))
    startTime = time.perf_counter()
    solution.resolveBFS()
    endTime = time.perf_counter()
    print("BFS总用时{} s\n".format(endTime - startTime))


if __name__ == "__main__":
    main()
    print("程序结束".center(20, '*'))
