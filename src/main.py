import curses
import level as lv
import character as CHARACTER

def main(screen):
    player = CHARACTER.Player("Sam", "player", "@", 10, 100, 1, False)

    level = lv.all_levels["level_1"]
    level.entities["player"] = player
    level.player = player
    level.initEntities(level.entities)


    c = ""
    while c != 27:
        screen.clear()
        full = level.refreshLayout()
        if level.instructions or level.characterMenu or level.search:
            for x,i in enumerate(full):
                screen.addstr(x+5, 25, i)
        else:
            for x, i in enumerate(full):
                screen.addstr(x+5, 50, i)

        screen.refresh()
        c = screen.getch()
        level.distributeInput(level.entities["player"], c)

curses.wrapper(main)
