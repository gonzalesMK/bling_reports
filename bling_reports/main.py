#!usr/env/bin python
from tkinter import *
from reports.reports.weekly_sales import generate
from bling.bling_api import BlingClient

import os


class Table:
    def __init__(self, root):
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=20, fg="blue", font=("Arial", 16, "bold"))

                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])


# Create the client
client = BlingClient(os.environ["BLING_API_KEY"])

report = generate(client, n_weeks=1)
repo = report[0]

# take the data
lst = [(key, value.qtd, value.value) for key, value in repo.item_info.items()]

# find total number of rows and
# columns in list
total_rows = len(lst)
total_columns = len(lst[0])

# create root window
root = Tk()
t = Table(root)
root.mainloop()
