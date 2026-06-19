import tkinter as tk


def _rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


class UILeds(tk.Tk):
    def __init__(self, num_leds, ** kwargs):
        super().__init__(**kwargs)
        self.num_leds = num_leds
        self.led_frames = []
        for i in range(num_leds):
            led_frame = tk.Frame(self, width=30, height=30,
                                 background=_rgb((0, 0, 0)), borderwidth=3, relief="ridge")
            self.led_frames.append(led_frame)
            self.led_frames[i].grid(row=0, column=i*2)
            pad = tk.Frame(self, width=5 if i % 2 == 0 else 20, height=30,
                           background="black")
            pad.grid(row=0, column=(i*2)+1)

        self.focus_force()

    def update_pix(self, i: int, rgb):
        self.led_frames[i].config(bg=_rgb(rgb))

    def update_buff(self, buffer):
        for i in range(self.num_leds):
            r = buffer[i*3]
            g = buffer[(i*3)+1]
            b = buffer[(i*3)+2]
            self.led_frames[i].config(bg=_rgb((r, g, b)))

    def clear(self):
        for i in range(self.num_leds):
            self.update_pix(i, (0, 0, 0))


if __name__ == "__main__":
    ui = UILeds()
    ui.mainloop()
