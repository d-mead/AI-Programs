import tkinter as tk

def main():
    master = tk.Tk()

    w = tk.Canvas(master, width=700, height=700)
    w.pack()

    for y in range(200, 701, 100):
        w.create_line(0, y, 700, y)

    for x in range(0, 701, 100):
        w.create_line(x, 100, x, 700)
    w.create_line(3, 100, 3, 700)

    w.create_circle(50, 150, 40)

    index_to_cord = dict()

    for row_i, row in zip(range(10, 56, 9), range(0, 7)):
            for col_i, col in zip(range(row_i, row_i+7), range(0, 8)):
                index_to_cord[col_i] = (50+100*col, 150+100*row

    print(index_to_cord)


    # w.create_line(100, 100, 200, 100)
    # w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

    # w.create_rectangle(50, 25, 150, 75, fill="blue")

    master.mainloop()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

tk.Canvas.create_circle = _create_circle

main()