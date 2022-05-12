import globals
from ui.TurbineGui import TurbineGui
from server import Server


def main():
    globals.server = Server()
    globals.gui = TurbineGui(width=300, height=400)
    globals.gui.mainloop()
    globals.server.trigger.set()
    globals.server.join()


if __name__ == '__main__':
    main()
