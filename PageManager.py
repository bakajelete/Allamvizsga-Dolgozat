import tkinter as tk

class PageManager:
    def __init__(self, root):
        self.root = root
        self.pages = {}

    def show_page(self, page_name):
        page = self.pages.get(page_name)
        
        if page:
            page.show()
        else:
            raise ValueError(f"Page '{page_name}' does not exist.")

    def create_page(self, page_name, page_class):
        
        page = page_class(self.root, self)
        page.place(x=0, y=0, relwidth=1, relheight=1)
        self.pages[page_name] = page
