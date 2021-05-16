""" tk_ToolTip_class101.py
gives a Tkinter widget a tooltip as the mouse is above the widget
tested with Python27 and Python34  by  vegaseat  09sep2014
www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

Modified to include a delay time by Victor Zaccardo, 25mar16
https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
"""


import tkinter as tk
import tkinter.ttk as ttk


class ToolTip:
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='canvas info', bg='#FFFFEA', pad=(5, 3, 5, 3),  waittime=50,
                 wraplength=250):
        self.waittime = waittime     # miliseconds
        self.wraplength = wraplength   # pixels
        self.bg = bg
        self.pad = pad
        self.widget = widget
        self.text = text
        self.bind_widget_events()
        self.id = None
        self.tw = None

    def bind_widget_events(self, *args):
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background=self.bg, relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(padx=(self.pad[0], self.pad[2]),
                   pady=(self.pad[1], self.pad[3]),)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class CanvasTooltip(ToolTip):
    '''
    It creates a tooltip for a given canvas tag or id as the mouse is
    above it.

    This class has been derived from the original Tooltip class I updated
    and posted back to StackOverflow at the following link:

    https://stackoverflow.com/questions/3221956/
           what-is-the-simplest-way-to-make-tooltips-in-tkinter/
           41079350#41079350

    Alberto Vassena on 2016.12.10.
    '''

    def __init__(self, canvas, tag_or_id, **kwargs):
        self._tag_or_id = tag_or_id
        super().__init__(canvas, **kwargs)

    def bind_widget_events(self, *args):
        self.widget.tag_bind(self._tag_or_id, "<Enter>", self.enter)
        self.widget.tag_bind(self._tag_or_id, "<Leave>", self.leave)
        self.widget.tag_bind(self._tag_or_id, "<ButtonPress>", self.leave)

    def showtip(self, event=None):

        bg = self.bg
        pad = self.pad
        canvas = self.widget

        # creates a toplevel window
        self.tw = tk.Toplevel(canvas.master)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        win = tk.Frame(self.tw,
                       background=bg,
                       borderwidth=0)
        label = ttk.Label(win,
                          text=self.text,
                          justify=tk.LEFT,
                          background=bg,
                          relief=tk.SOLID,
                          borderwidth=0,
                          wraplength=self.wraplength)

        label.grid(padx=(pad[0], pad[2]),
                   pady=(pad[1], pad[3]),
                   sticky=tk.NSEW)
        win.grid()

        x, y = self._tip_pos_calculator(canvas, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def _tip_pos_calculator(self, canvas, label, *, tip_delta=(10, 5), pad=(5, 3, 5, 3)):

        c = canvas

        s_width, s_height = c.winfo_screenwidth(), c.winfo_screenheight()

        width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
                         pad[1] + label.winfo_reqheight() + pad[3])

        mouse_x, mouse_y = c.winfo_pointerxy()

        x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
        x2, y2 = x1 + width, y1 + height

        x_delta = x2 - s_width
        if x_delta < 0:
            x_delta = 0
        y_delta = y2 - s_height
        if y_delta < 0:
            y_delta = 0

        offscreen = (x_delta, y_delta) != (0, 0)

        if offscreen:

            if x_delta:
                x1 = mouse_x - tip_delta[0] - width

            if y_delta:
                y1 = mouse_y - tip_delta[1] - height

        offscreen_again = y1 < 0  # out on the top

        if offscreen_again:
            # No further checks will be done.

            # TIP:
            # A further mod might automagically augment the
            # wraplength when the tooltip is too high to be
            # kept inside the screen.
            y1 = 0

        return x1, y1

    def hide(self):
        if self.tw:
            self.tw.destroy()
        self.tw = None
