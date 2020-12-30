# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, time
from game import Agent

preAction = []
EndTime = 0


def checkAround(newFood, curXForP, curYForP, x, y):
    Sum = 0
    for i in range(curXForP - int(x / 2), curXForP + int(x / 2) + 1):
        for j in range(curYForP - int(y / 2), curYForP + int(y / 2) + 1):
            try:
                if newFood[i][j] is True:
                    Sum += 1
            except:
                pass
    return Sum


def findNearest(curXForP, curYForP, newFood, flagForQFour=0):
    mindist = 999
    nearestPos = ()
    try:
        for i in range(25):
            for j in range(len(newFood[0])):
                if flagForQFour == 1 and (i, j) == (3, 3) or (i, j) == (16, 3):
                    continue
                if newFood[i][j] is True and mindist > abs(curXForP - i) + abs(curYForP - j):
                    mindist = abs(curXForP - i) + abs(curYForP - j)
                    nearestPos = (i, j)
    except:
        pass
    return nearestPos, mindist


def countDist(curXForP, curYForP, i, j):
    return abs(curXForP - i) + abs(curYForP - j)


def evaluationFunction(currentGameState, action):
    global preAction
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    # 产生动作对应的状态
    newPos = successorGameState.getPacmanPosition()
    # 获得这个状态对应的吃豆人位置
    newFood = successorGameState.getFood()
    # 获得当前状态的食物分布
    GhostPos = successorGameState.getGhostPositions()
    # 获得幽灵的位置
    originalScore = successorGameState.getScore()
    # 获得此时的分数（注意，此时分数是指是从真实位置经过action到达的假设位置的分数，最终返回的值是curScore+originalScore）
    curScore = 0  # 计算当前状态经评价函数所得的评价值（越高越好）
    curXForP, curYForP = newPos  # 当前吃豆人x,y坐标
    distance = min(countDist(curXForP, curYForP, i, j) for i, j in GhostPos)
    # 幽灵可能不止一个，真正造成威胁的是离吃豆人最近的一个幽灵，故获取其离吃豆人的距离
    aroundFood = checkAround(newFood, curXForP, curYForP, 3, 3)
    # 评价函数的一个指标，获取以当前位置为中心的3*3方格内豆子个数，很显然我们想往豆子多的地方去
    nearestFoodPos, nearestdist = findNearest(curXForP, curYForP, newFood)
    # 获取离吃豆人最近的豆子的位置和距离（其实距离没有用）
    if successorGameState.hasWall(curXForP, curYForP):
        # 判断经过action后的位置是否是墙，是则返回-999代表最小值
        return -999
    if distance > 5:  # 当距离较大时，可以无视幽灵，专心吃豆子
        if aroundFood == 0:
            # 我们现在评价函数的指标为aroundFood，但如果3*3的范围内不再有豆子，则5个action所得的评价值都一样，
            # 吃豆人不知往哪走，会陷入死循环，故进行判断，用nearestFood使其走出死循环
            try:
                curScore += 1 / (abs(curXForP - nearestFoodPos[0]) + abs(curYForP - nearestFoodPos[1]))
                # 这里取与最近豆子距离的倒数，离得越近值越大，优先级越高
            except:
                pass
        else:
            curScore += aroundFood  # 否则以周围的食物个数作为评价值，显然个数越多优先级越大
    elif distance > 3:  # distance<=5 and distance>3:此时需要适度考虑幽灵，故里各取0.5的权重
        curScore += aroundFood + 0.5 * (1 / nearestdist) - 0.5 / distance
    else:  # 离幽灵已经非常近了，只考虑如何离幽灵更远
        curScore -= 2 / (distance + 1)
    return curScore + originalScore  # 返回经过评价函数的值+当前状态的值(注意要+originalScore因为如果吃到豆子分数会增加）


class ReflexAgent(Agent):
    global preAction, EndTime
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        global EndTime
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        """
        如果要是测试问题4，请把evaluationFunction换位betterEvaluationFunction
        """
        scores = [evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"
        EndTime -= 2
        return legalMoves[chosenIndex]


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExepctimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    global preAction, EndTime
    totalTimeAverage = 0

    def miniMax(self, iteration, index, perState):  # 是来获得perState状态的值，递归调用
        # iteration代表迭代次数，index代表智能体序号（0代表吃豆人，>1代表幽灵），perState代表当前状态
        currentScore = self.evaluationFunction(perState)
        if index == 0:  # 0代表吃豆人，此为Max层
            Max = -999
            legalActions = perState.getLegalActions(index)
            if iteration >= self.depth * 2 or perState.isLose() or perState.isWin():
                # 注意这句中是否赢或输不能少，否则吃豆人将不知道怎么走
                # 因为此处是吃豆人走一步iteration+1，幽灵走一步iteration+1故恰与与题设depth是其2倍关系，故*2
                """
                
                    如果要测试第4题，请改为：
                    return betterEvaluationFunction(perState, currentScore)
                    
                """
                return self.evaluationFunction(perState)  # 如果超过深度或已经输了或赢了，则返回评价值
            for action in legalActions:  # 对每一个合法动作生成一个状态
                tempState = perState.generateSuccessor(index, action)
                value = self.miniMax(iteration + 1, 1, tempState)  # 而幽灵会使吃豆人分数最低，再次掉用miniMax，
                # 注意此时iteration+1，因为从吃豆人变到幽灵移动
                # 同理index变为第一个幽灵
                if value > Max:
                    Max = value
                # 选择最大的值返回
            return Max
        else:  # >1代表幽灵，此为最小层
            Min = 999
            legalActions = perState.getLegalActions(index)
            if iteration >= self.depth or perState.isLose():  # 注意这句后半句不能少
                """

                    如果要测试第4题，请改为：
                    return betterEvaluationFunction(perState, currentScore)

                """
                return self.evaluationFunction(perState)
            for action in legalActions:
                tempState = perState.generateSuccessor(index, action)
                if index >= perState.getNumAgents() - 1:  # 已遍历完了最后一个幽灵，要开始吃豆人的行动了
                    value = self.miniMax(iteration + 1, 0, tempState)
                else:  # 应对多个幽灵
                    value = self.miniMax(iteration, index + 1, tempState)
                    # 注意此时iteration没有变，因为是同一层，取所有幽灵中使值最小的
                if value < Min:
                    Min = value
            return Min

    def getAction(self, gameState):
        global EndTime
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        Max = -999
        favourableAction = "Stop"  # 最佳行动
        legalActions = gameState.getLegalActions(0)  # 获得吃豆人合法动作，index=0
        startTime = time.perf_counter()
        for perAction in legalActions:  # 循环求得吃豆人的最佳action
            perState = gameState.generateSuccessor(0, perAction)  # 生成每一种动作对应的状态，作为miniMax的参数
            value = self.miniMax(0, 1, perState)
            # miniMax参数分别为iteration（迭代次数），index（index>0代表获得幽灵行动后的状态），perState
            # 因吃豆人先走，然后幽灵要使吃豆人分数最低，故index=1（如果有多个幽灵，index会以此增加，反复调用miniMax
            # 来取得使吃豆人得分最低的行动
            if Max < value:
                Max = value
                favourableAction = perAction
        endTime = time.perf_counter()
        # print("当前向{:*^20}方向走".format(favourableAction))
        # print(("用时" + str(endTime - startTime) + " s").center(20))
        EndTime -= 2  # 幽灵剩余的害怕时间，因吃豆人走一步后幽灵走一步，然后吃豆人再走，故要-2而不是-1
        return favourableAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    global preAction, EndTime

    def miniMax(self, iteration, index, perState, alpha, beta):  # 是来获得perState状态的值，递归调用
        currentScore = self.evaluationFunction(perState)
        # 多了参数alpha，beta，两者初始值分别为-∞，+∞
        if index == 0:  # 最大值代表吃豆人
            Max = -999
            legalActions = perState.getLegalActions(index)
            if iteration >= self.depth * 2 or perState.isLose() or perState.isWin():  # perState.isLose()不能少
                """

                    如果要测试第4题，请改为：
                    return betterEvaluationFunction(perState, currentScore)

                """
                return self.evaluationFunction(perState)
            for action in legalActions:
                tempState = perState.generateSuccessor(index, action)
                value = self.miniMax(iteration + 1, 1, tempState, alpha, beta)
                if value > Max:
                    Max = value
                if value >= beta:  # 当前层为最大层对下一层进行判断，如果下一层有一个值value
                    # value>=β 则没有必要再遍历剩下节点（因为当前值已经不满足条件，即使遍历剩下的节点返回值一定也是不满足条件的，故直接返回值
                    return value
                alpha = max(alpha, value)  # 更新alpha
            return Max
        else:  # 最小值代表幽灵
            Min = 999
            legalActions = perState.getLegalActions(index)
            if iteration >= self.depth or perState.isLose():  # perState.isLose()不能少
                """

                    如果要测试第4题，请改为：
                    return betterEvaluationFunction(perState, currentScore)

                """
                return self.evaluationFunction(perState)
            for action in legalActions:
                tempState = perState.generateSuccessor(index, action)
                if index >= perState.getNumAgents() - 1:  # 以遍历完了最后一个幽灵，要开始吃豆人的行动了
                    value = self.miniMax(iteration + 1, 0, tempState, alpha, beta)
                else:  # 应对多个幽灵
                    value = self.miniMax(iteration, index + 1, tempState, alpha,
                                         beta)  # 注意此时iteration没有变，因为是同一层，取所有幽灵中使值最小的
                if value <= alpha:  # 当前层为最小层对下一层进行判断，如果下一层有一个值value
                    # value<=alpha 则没有必要再遍历剩下节点（因为当前值已经不满足条件，即使遍历剩下的节点返回值一定也是不满足条件的
                    return value
                beta = min(value, beta)  # 更新beta
                if value < Min:
                    Min = value
            return Min

    def getAction(self, gameState):
        global EndTime
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        Max = -999
        favourableAction = "Stop"  # 最佳行动
        legalActions = gameState.getLegalActions(0)  # 获得合法动作
        startTime = time.perf_counter()
        for perAction in legalActions:  # 循环求得最佳action
            perState = gameState.generateSuccessor(0, perAction)  # 生成每一种动作对应的状态，作为miniMax的参数
            value = self.miniMax(0, 1, perState, -999, 999)
            # miniMax参数分别为iteration，index，perState，# 因吃豆人先走，幽灵要是
            if Max < value:
                Max = value
                favourableAction = perAction
        endTime = time.perf_counter()
        # print("当前向{:*^20}方向走".format(favourableAction))
        # print(("用时" + str(endTime - startTime) + " s").center(20))
        EndTime -= 2  # 幽灵剩余的害怕时间，因吃豆人走一步后幽灵走一步，然后吃豆人再走，故要-2而不是-1
        return favourableAction


def toAllTheDist(i_, j_, newFood):
    totalDist = 0
    for i in range(7):
        for j in range(20):
            try:
                if newFood[i][j] is True:
                    totalDist += countDist(i_, j_, i, j)
            except:
                pass
    return totalDist


def betterEvaluationFunction(currentGameState, currentScore, action=None):
    global preAction, EndTime
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    """
    本题在ReflectAgent下平均分1000，平均胜率80% 因不可避免两鬼夹击
        1.计算与所有鬼平均距离        代号D2AverageG
        2.计算与最近鬼的距离         代号D2NearestG
        3.计算离最近Food的距离      代号D2NearestF 
        4.计算周围Food的个数       代号D2AroundF  
        5. EndTime 表示鬼结束害怕还有多少时间 """
    "*** YOUR CODE HERE ***"
    capsulePos = currentGameState.getCapsules()
    if action is None:
        newGhostStates = currentGameState.getGhostStates()
        newPos = currentGameState.getPacmanPosition()
        GhostPos = currentGameState.getGhostPositions()
    else:  # 如果action不是None则是评价行动
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newGhostStates = successorGameState.getGhostStates()
        newPos = successorGameState.getPacmanPosition()
        GhostPos = successorGameState.getGhostPositions()
    newScaredTime = [ghostState.scaredTimer for ghostState in newGhostStates]
    EndTime = min(newScaredTime)
    newFood = currentGameState.getFood()
    curXForP, curYForP = newPos
    nearestDistanceG = min(countDist(curXForP, curYForP, i, j) for i, j in GhostPos)
    aroundFood = checkAround(newFood, curXForP, curYForP, 3, 3)
    nearestFoodPos, nearestdist = findNearest(curXForP, curYForP, newFood, 1)
    D2AroundF = aroundFood
    D2AverageG = sum(countDist(curXForP, curYForP, i, j) for i, j in GhostPos) / (currentGameState.getNumAgents() - 1)
    D2NearestG = nearestDistanceG
    D2NearestF = nearestdist
    if EndTime > 1:  # 如果当前幽灵处于害怕状态，则可以无视幽灵，又因当前位置是进行深度为2搜索后的位置，即设D2Nearest>1即可不会碰到幽灵,完全以吃豆子为目标
        D2NearestG = 10
    if (curXForP, curYForP) in capsulePos:  # 如果某一状态的位置可以吃到胶囊，则一定去吃
        return 999
    if D2NearestG > 1:  # 当前以附近的食物为主要评判依据，兼顾与所有食物距离
        weightForD2NearestG = 0
        weightForD2AverageG = 0
        weightForD2NearestF = 10
        weightForD2AroundF = 15
        weightForGetScore = 1
    else:  # 同时考虑食物和幽灵
        weightForD2NearestG = 8
        weightForD2AverageG = 6
        weightForD2NearestF = 6
        weightForD2AroundF = 1
        weightForGetScore = 0.5
    #  weightForGetScore为原程序自带显示分数函数，如果吃了豆子，分数会增加，如果离幽灵太近则不再考虑吃豆子，故设为0
    if D2NearestG == 0 or (curXForP, curYForP) in [(9, 4), (10, 4), (11, 4)]:
        #  避免吃豆人位于(9, 4), (10, 4), (11, 4)三个凹槽处（几乎必死）
        return -999
    return - weightForD2AverageG / D2AverageG - weightForD2NearestG / D2NearestG + weightForD2NearestF / (
            D2NearestF + 1) + weightForD2AroundF * D2AroundF + weightForGetScore * currentGameState.getScore() + \
           currentScore

    #  返回评价指标的线性组合


# Abbreviation

better = betterEvaluationFunction
