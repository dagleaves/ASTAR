

class Node:
    def __init__(self, x_step_size: int, y_step_size, x: int, y: int, startX: int, startY: int, goalX: int, goalY: int):
        self.x = x
        self.y = y
        self.topLeft = (x - x_step_size, y - y_step_size)
        self.topRight = (x + x_step_size, y - y_step_size)
        self.bottomLeft = (x - x_step_size, y + y_step_size)
        self.bottomRight = (x + x_step_size, y + y_step_size)
        self.isOpen = True
        self.isTarget = self.x == goalX and self.y == goalY
        self.fCost = self.setFCost(startX, startY, goalX, goalY)

    def setFCost(self, startX, startY, goalX, goalY):
        self.fCost = self.setGCost(startX, startY) + \
            self.setHCost(goalX, goalY)

    def setGCost(self, startX, startY):
        return abs((self.x - startX)**2 - (self.y - startY))**.5

    def setHCost(self, goalX, goalY):
        return abs((goalX - self.x) - (goalY - self.y))**.5
