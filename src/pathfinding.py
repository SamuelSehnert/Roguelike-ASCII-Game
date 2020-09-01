import queue
from visual import Crosshair
from character import Player

def validPath(layout, startingTile, target, x, y): #player.x = x, player.y = y
    """
    Finds the shortest path to a target and returns true if
    no collision is detected on the backtracked path or false
    if there is a collision

    layout is the layout of the level (populated by Tile objects
    starting Tile is the current tile that the player is standing on
    target is the NPC object you are currently attacking
    x is the current x position of the player
    y is the current y position of the player
    """
    if isinstance(target, Player):
        return True
    
    Q = queue.Queue()

    startingTile.previous = None

    Q.put(layout[y][x])

    while Q.qsize() > 0:

        current = Q.get()
        current.visited = True
        y = current.y
        x = current.x

        if y + 1 < len(layout):
            if layout[y + 1][x].standingOn == target:
                layout[y + 1][x].previous = current
                current = layout[y + 1][x]
                break
            elif not layout[y + 1][x].visited:
                Q.put(layout[y + 1][x])
                layout[y + 1][x].previous = current
                layout[y + 1][x].visited = True

        if y - 1 >= 0:
            if layout[y - 1][x].standingOn == target:
                layout[y - 1][x].previous = current
                current = layout[y - 1][x]
                break
            elif not layout[y - 1][x].visited:
                Q.put(layout[y - 1][x])
                layout[y - 1][x].previous = current
                layout[y - 1][x].visited = True

        if x + 1 < len(layout[y]):
            if layout[y][x + 1].standingOn == target:
                layout[y][x + 1].previous = current
                current = layout[y][x + 1]
                break

            elif not layout[y][x + 1].visited:
                Q.put(layout[y][x + 1])
                layout[y][x + 1].previous = current
                layout[y][x + 1].visited = True

        if x - 1 >= 0:
            if layout[y][x - 1].standingOn == target:
                layout[y][x - 1].previous = current
                current = layout[y][x - 1]
                break

            elif not layout[y][x - 1].visited:
                Q.put(layout[y][x - 1])
                layout[y][x - 1].previous = current
                layout[y][x - 1].visited = True

        if x - 1 >= 0 and y - 1 >= 0:
            if layout[y - 1][x - 1].standingOn == target:
                layout[y - 1][x - 1].previous = current
                current = layout[y - 1][x - 1]
                break

            elif not layout[y - 1][x - 1].visited:
                Q.put(layout[y - 1][x - 1])
                layout[y - 1][x - 1].previous = current
                layout [y - 1][x - 1].visited = True

        if x - 1 >= 0 and y + 1 < len(layout):
            if layout[y + 1][x - 1].standingOn == target:
                layout[y + 1][x - 1].previous = current
                current = layout[y + 1][x - 1]
                break

            elif not layout[y + 1][x - 1].visited:
                Q.put(layout[y + 1][x - 1])
                layout[y + 1][x - 1].previous = current
                layout [y + 1][x - 1].visited = True

        if x + 1 < len(layout[y]) and y - 1 >= 0:
            if layout[y - 1][x + 1].standingOn == target:
                layout[y - 1][x + 1].previous = current
                current = layout[y - 1][x + 1]
                break

            elif not layout[y - 1][x + 1].visited:
                Q.put(layout[y - 1][x + 1])
                layout[y - 1][x + 1].previous = current
                layout [y - 1][x + 1].visited = True

        if x + 1 < len(layout[y]) and y + 1 < len(layout):
            if layout[y + 1][x + 1].standingOn == target:
                layout[y + 1][x + 1].previous = current
                current = layout[y + 1][x + 1]
                break

            elif not layout[y + 1][x + 1].visited:
                Q.put(layout[y + 1][x + 1])
                layout[y + 1][x + 1].previous = current
                layout [y + 1][x + 1].visited = True

    while current.previous != None:
        if current.collide == True:
            return False

        elif isinstance(current, Player):
            return True

        current = current.previous

    return True

