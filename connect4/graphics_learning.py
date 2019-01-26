import tkinter as tk

def main():
    master = tk.Tk()

    w = tk.Canvas(master, width=700, height=700)
    w.pack()

    w.create_rectangle(0, 100, 700, 700, outline='', fill='gold')

    linecolor = 'goldenrod'
    for y in range(200, 701, 100):
        w.create_line(0, y, 700, y, width=3, fill=linecolor)

    for x in range(0, 701, 100):
        w.create_line(x, 100, x, 700, width=3, fill=linecolor)
    w.create_line(3, 100, 3, 700, width=6, fill=linecolor)

    # w.create_circle(50, 150, 40)

    index_to_cord = dict()

    for row_i, row in zip(range(10, 56, 9), range(0, 7)):
            for col_i, col in zip(range(row_i, row_i+7), range(0, 8)):
                index_to_cord[col_i] = (50+100*col, 150+100*row)

    for index in index_to_cord.values():
        w.create_circle(index[0], index[1], 40, outline='', fill='SteelBlue3')

    print(index_to_cord)

    master.mainloop()


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


tk.Canvas.create_circle = _create_circle

main()