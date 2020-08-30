import queue_array
from visual import Crosshair
from character import Player

def validPath(layout, startingTile, x, y): #player.x = x, player.y = y
    Q = queue_array.Queue(1000)

    startingTile.previous = None

    Q.enqueue(layout[y][x])

    while Q.size() > 0:

        current = Q.peek()
        current.visited = True
        y = current.y
        x = current.x

        if y + 1 < len(layout):
            if isinstance(layout[y + 1][x], Crosshair):
                layout[y + 1][x].previous = current
                current = layout[y + 1][x]
                break
            elif not layout[y + 1][x].visited:
                Q.enqueue(layout[y + 1][x])
                layout[y + 1][x].previous = current
                layout[y + 1][x].visited = True

        if y - 1 >= 0:
            if isinstance(layout[y - 1][x], Crosshair):
                layout[y - 1][x].previous = current
                current = layout[y - 1][x]
                break
            elif not layout[y - 1][x].visited:
                Q.enqueue(layout[y - 1][x])
                layout[y - 1][x].previous = current
                layout[y - 1][x].visited = True

        if x + 1 < len(layout[y]):
            if isinstance(layout[y][x + 1], Crosshair):
                layout[y][x + 1].previous = current
                current = layout[y][x + 1]
                break

            elif not layout[y][x + 1].visited:
                Q.enqueue(layout[y][x + 1])
                layout[y][x + 1].previous = current
                layout[y][x + 1].visited = True

        if x - 1 >= 0:
            if isinstance(layout[y][x - 1], Crosshair):
                layout[y][x - 1].previous = current
                current = layout[y][x - 1]
                break

            elif not layout[y][x - 1].visited:
                Q.enqueue(layout[y][x - 1])
                layout[y][x - 1].previous = current
                layout[y][x - 1].visited = True

        Q.dequeue()


    current = current.previous
    while True:
        current.symbol = "!"
        if current.collide == True:
            return False

        elif isinstance(current, Player):
            return True

        current = current.previous
    return True

