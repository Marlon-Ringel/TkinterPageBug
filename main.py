import tkinter as tk

class PageSwitcher(tk.Frame):
    def __init__(self, parent:tk, desiredHeight:int, desiredWidth:int) -> None:
        self.managedPages:list[tk.Frame] = []
        self.currentlyDisplayedPage:tk.Frame = None

        tk.Frame.__init__(self, parent, height=desiredHeight, width=desiredWidth)
        self.grid_propagate(False)
        self.rowconfigure(index=(0,2), weight=1)
        self.columnconfigure(index=(0,2), weight=1)

    def addPage(self, pageToAdd:tk.Frame) -> None:
        self.managedPages.append(pageToAdd)

    def displayPage(self, pageId:int) -> None:
        if self.currentlyDisplayedPage != None:
            self.currentlyDisplayedPage.grid_remove()
        self.currentlyDisplayedPage = self.managedPages[pageId]
        self.currentlyDisplayedPage.grid(row=1, column=1)
        self.currentlyDisplayedPage.focus_force()

class PageSelector(tk.Frame):
    def __init__(self, parent:tk, desiredHeight:int, desiredWidth:int, pageSwitchFunction) -> None:
        self.pageSwitchFunction = pageSwitchFunction
        self.width = desiredWidth
        self.managedSelectors:list[PageSelector.Selector] = []

        tk.Frame.__init__(self, parent, height=desiredHeight, width=desiredWidth)
        self.grid_propagate(False)    

    def registerPage(self, pageName:str, pageId:int):
        selector = self.Selector(
            parent=self, 
            desiredWidth=self.width-10, #For 5px of padding on each side of selector
            name=pageName, 
            pageId=pageId, 
            selectFunction=self.select
        )
        selector.grid(row=self.grid_size()[1], column=0, padx=5, pady=2)
        self.managedSelectors.append(selector)

    def select(self, pageId) -> None:
        self.pageSwitchFunction(pageId) 
    
    class Selector(tk.Frame):
        def __init__(self, parent:tk, name:str, pageId:int, selectFunction, desiredWidth:int) -> None:
            self.pageId = pageId
            self.selectFunction = selectFunction

            tk.Frame.__init__(self, parent, height=32, width=desiredWidth, border=2, relief="raised")
            self.grid_propagate(False)

            self.name = tk.Label(self, text=name, font="Bold")
            self.name.grid(row=1, column=0, padx=5)

            self.bind("<Button-1>", self.select)
            self.name.bind("<Button-1>", self.select)

        def select(self, event:tk.Event) -> None:
            self.selectFunction(self.pageId)

def main():
    height = 600
    width = 600

    window = tk.Tk()
    window.geometry(f"{width}x{height}")

    pageSwitcher = PageSwitcher(window, height, width//2)
    pageSelector = PageSelector(window, height, width//2, pageSwitcher.displayPage)
    pageSwitcher.grid(row=0, column=1)
    pageSelector.grid(row=0, column=0)

    pageNamesAndColors = ["red", "orange", "yellow", "green", "lime", "lightBlue", "blue", "purple", "pink"]

    for index, color in enumerate(pageNamesAndColors):
        newPage = tk.Frame(pageSwitcher, height=height, width=width//2, bg=color)
        pageSwitcher.addPage(newPage)
        pageSelector.registerPage(pageName=f"{color} Page", pageId=index)

    window.mainloop()

main()