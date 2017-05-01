import tkinter as tk
import requests
from bs4 import BeautifulSoup


def get_xml():
    stop = "135001"
    link = "htt s://data.dublinked.ie/cgi-bin/rtpi/realtimebusinformation?stopid="+stop+"&format=xml"
    data = requests.get(link).text
    soup = BeautifulSoup(data, 'xml')
    xs = soup.find_all("result")

    headers = {
        "duetime": "Due Time",  # In minutes
        "route": "Route Number",
        "destination": "Destination",
        "origin": "Origin",
        "operator": "Operator"
    }

    ys = {k: [x.text for x in xs.find_all(k)] }

    import pdb; pdb.set_trace()

if __name__ == "__main__":
    top = tk.Tk()

    bop = tk.Frame()
    bop.grid(row=0,column=0)

    tk.Button(bop, text='Exit', command=top.destroy).pack(side=tk.BOTTOM)

    height = 5
    width = 5
    grid = [[None for _ in range(width)] for _ in range(height)]
    for i in range(height):
        for j in range(1, width):
            b = tk.Entry(top, text="")
            b.grid(row=i, column=j)
            grid[i][j] = b

    get_xml()

    top.mainloop()
