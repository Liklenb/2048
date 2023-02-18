import tkinter
from background import controller


def main():
    # create the root
    root = tkinter.Tk()
    # set the title and the size
    root.title('2048')
    root.state('zoomed')
    root.resizable(False, False)
    # update the root to get the size later
    root.update()
    # create the frame controller
    controller.Controller(root)
    root.mainloop()


if __name__ == '__main__':
    main()
