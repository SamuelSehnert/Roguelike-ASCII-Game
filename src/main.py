import curses
import level as lv
import character as CHARACTER

def main(screen):
    player = CHARACTER.Player("Sam", 10, 100, False)
    #enemy = CHARACTER.NPC("Jose", "bandit", 5, 5, True)
    npc = CHARACTER.NPC("Bobbu", "bandit", 3, 3, True)

    level = lv.Level("pathfindingTest.txt", {"player":player, 
                                     #"bandit":enemy,
                                     "bandit2":npc})
    c = ""
    while c != 27:
        screen.clear()
        full = level.refreshLayout()
        if level.instructions or level.characterMenu:
            for x,i in enumerate(full):
                screen.addstr(x+10, 25, i)
        else:
            for x, i in enumerate(full):
                screen.addstr(x+10, 50, i)

        screen.refresh()
        c = screen.getch()
        level.distributeInput(level.entities["player"], c)
        

curses.wrapper(main)
