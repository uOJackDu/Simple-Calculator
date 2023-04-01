import tkinter as tk
from tkinter import ttk

import math


class Util:
    PI = math.pi
    E = math.e

    @staticmethod
    def ln(x):
        return math.log(x)

    @staticmethod
    def log(x):
        return math.log10(x)

    @staticmethod
    def sin(x):
        return math.sin(x)

    @staticmethod
    def cos(x):
        return math.cos(x)

    @staticmethod
    def tan(x):
        return math.tan(x)

    @staticmethod
    def asin(x):
        return math.asin(x)

    @staticmethod
    def acos(x):
        return math.acos(x)

    @staticmethod
    def atan(x):
        return math.atan(x)

    @staticmethod
    def sin_deg(x):
        return math.sin(math.radians(x))

    @staticmethod
    def cos_deg(x):
        return math.cos(math.radians(x))

    @staticmethod
    def tan_deg(x):
        return math.tan(math.radians(x))

    @staticmethod
    def asin_deg(x):
        return math.degrees(math.asin(x))

    @staticmethod
    def acos_deg(x):
        return math.degrees(math.acos(x))

    @staticmethod
    def atan_deg(x):
        return math.degrees(math.atan(x))


class Calculator:
    actions = (
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "+", "-", "*", "/", "^", "=", "(", ")",
        "ln", "log", "sin", "cos", "tan", "asin", "acos", "atan", "\u03C0", "e",
        "CLEAR", "DEL", "DEG", "PREV", "NEXT", "SHIFT"
    )

    def __init__(self, master):
        self.DISPLAY_PRECISION = 12

        self.shifted = False
        self.deg_mode = False

        self.master = master
        master.title("Calculator")
        master.resizable(False, False)

        # Create the display

        num_cols = 7

        self.display = tk.Entry(master, width=35, font=("SF Pro", 16, 'bold'), justify=tk.RIGHT, state="disabled")
        self.display.grid(row=0, column=0, columnspan=num_cols)

        # Create the buttons

        self.btns = {}
        self.init_btns()

        r = 1
        c = 0

        for btn in self.btns.values():
            btn.grid(row=r, column=c, sticky="nsew")

            c += 1
            if c >= num_cols:
                c = 0
                r += 1

        # Bind the keyboard events
        master.bind("<Key>", self.key_pressed)

        self.history = []
        self.MAX_HISTORY_SIZE = 5
        self.history_idx = -1
        self.cur_expr = ""

    def init_btns(self):
        btn_names = [
            "\u03C0", "ln",  "7", "8", "9", "+", "C",
            "DEG",    "sin", "4", "5", "6", "-", "(",
            "Prev",   "cos", "1", "2", "3", "*", ")",
            "Shift",  "tan", "0", ".", "^", "/", "="
        ]

        GREY = "#c8c8c8"
        YELLOW = "#ffff00"
        ORANGE = "#ff8200"

        for b in btn_names:
            cmd = lambda x=b: self.btn_pressed(x)
            btn = tk.Button(self.master, width=6, height=2, text=b, font=("SF Pro", 14, "bold"), fg="#404040", command=cmd, highlightthickness=0)

            self.btns[b] = btn

        for btn_name in self.btns:
            if btn_name in ("+", "-", "*", "/", "C", "(", ")", "="):
                btn_color = YELLOW

            elif btn_name in ("ln", "sin", "cos", "tan", "\u03C0", "DEG", "Prev", "Shift"):
                btn_color = ORANGE

            else:
                btn_color = GREY

            self.btns[btn_name].configure(highlightbackground=btn_color)

    def action(self, key):
        if not (key in Calculator.actions):
            print("Forbidden action:", key)
            return

        self.display.configure(state="normal")

        if self.display.get() == "Error":
            self.display.delete(0, tk.END)

        if key == "=":
            if self.display.get() != "":
                try:
                    expr = self.display.get()

                    self.add_to_history(expr)
                    print(self.history)

                    expr = self.convert_input_expr(expr)
                    print(expr)

                    res = f"{eval(expr):.{self.DISPLAY_PRECISION}f}".rstrip("0").rstrip(".")

                    self.cur_expr = res

                except:
                    res = "Error"
                    self.cur_expr = ""

                self.display.delete(0, tk.END)
                self.display.insert(tk.END, res)

        elif key == "CLEAR":
            self.display.delete(0, tk.END)
            self.cur_expr = self.display.get()

        elif key == "DEL":
            del_size = 1

            display_str = self.display.get();
            for symbol in ("ln(", "log(", "sin(", "cos(", "tan(", "asin(", "acos(", "atan("):
                if display_str.endswith(symbol):
                    del_size = len(symbol)

            self.display.delete(len(display_str) - del_size, tk.END)
            self.cur_expr = self.display.get()

        elif key == "DEG":
            self.shift_deg_mode()

        elif key == "PREV":
            if self.history_idx < len(self.history) - 1:
                self.history_idx += 1

                self.display.delete(0, tk.END)

                i = len(self.history) - 1 - self.history_idx
                self.display.insert(tk.END, self.history[i])

        elif key == "NEXT":
            if self.history_idx >= 0:
                self.history_idx -= 1

                self.display.delete(0, tk.END)

                i = len(self.history) - 1 - self.history_idx

                if i < len(self.history):
                    self.display.insert(tk.END, self.history[i])
                else:
                    self.display.insert(tk.END, self.cur_expr)

        elif key == "SHIFT":
            self.shift()

        elif key in ("ln", "log", "sin", "cos", "tan", "asin", "acos", "atan"):
            self.display.insert(tk.END, key + "(")
            self.cur_expr = self.display.get()

        else:
            self.display.insert(tk.END, key)
            self.cur_expr = self.display.get()

        if key != "PREV" and key != "NEXT" and key != "SHIFT":
            self.history_idx = -1

        self.display.configure(state="disabled")

    def btn_pressed(self, btn):
        action_on_shift_map = {
            "CLEAR": "DEL",
            "ln": "log",
            "sin": "asin",
            "cos": "acos",
            "tan": "atan",
            "\u03C0": "e",
            "PREV": "NEXT"
        }

        action_key = btn

        if btn == "C":
            action_key = "CLEAR"

        elif btn == "Prev":
            action_key = "PREV"

        elif btn == "Shift":
            action_key = "SHIFT"

        if self.shifted and action_key in action_on_shift_map:
            action_key = action_on_shift_map[action_key]

        self.action(action_key)

    def key_pressed(self, event):
        enterable_symbols = ("+", "-", "*", "/", ".", "^", "(", ")", "\u03C0", "e")

        symbol_shortcuts = {
            "p": "\u03C0",
            "l": "ln",
            "s": "sin",
            "o": "cos",
            "t": "tan",
            "L": "log",
            "S": "asin",
            "O": "acos",
            "T": "atan"
        }

        action_key = "FORBIDDEN"

        if event.char.isdigit() or event.char in enterable_symbols:
            action_key = event.char

        elif event.char in symbol_shortcuts:
            action_key = symbol_shortcuts[event.char]

        elif event.keysym == "Return":
            action_key = "="

        elif event.keysym == "c":
            action_key = "CLEAR"

        elif event.keysym == "BackSpace":
            action_key = "DEL"

        elif event.keysym == "Up":
            action_key = "PREV"

        elif event.keysym == "Down":
            action_key = "NEXT"

        if action_key == "FORBIDDEN":
            return

        self.action(action_key)

    def shift(self):
        self.shifted = not self.shifted
        self.update_btns()

    def shift_off(self):
        self.shifted = False
        self.update_btns()

    def shift_deg_mode(self):
        self.deg_mode = not self.deg_mode
        self.update_btns()

    def update_btns(self):
        update_on_shift_map = {
            "C": "DEL",
            "ln": "log",
            "sin": "asin",
            "cos": "acos",
            "tan": "atan",
            "\u03C0": "e",
            "Prev": "Next",
            "Shift": "SHIFT"
        }

        if self.shifted:
            for btn in update_on_shift_map:
                updated_text = update_on_shift_map[btn]
                self.btns[btn].configure(text=updated_text)
        
        else:
            for btn in update_on_shift_map:
                self.btns[btn].configure(text=btn)

        if self.deg_mode:
            self.btns["DEG"].configure(text="RAD")
        
        else:
            self.btns["DEG"].configure(text="DEG")

    def convert_input_expr(self, expr):
        symbol_replacement_map = {
            "ln": "Util.ln",
            "log": "Util.log",
            "sin": "Util.sin",
            "cos": "Util.cos",
            "tan": "Util.tan",
            "aUtil.sin": "Util.asin",
            "aUtil.cos": "Util.acos",
            "aUtil.tan": "Util.atan",
            "^": "**",
            "\u03C0": "Util.PI",
            "e": "Util.E"
        }

        for symbol in symbol_replacement_map:
            replacement = symbol_replacement_map[symbol]
            expr = expr.replace(symbol, replacement)

        if self.deg_mode:
            expr = expr.replace("sin", "sin_deg")
            expr = expr.replace("cos", "cos_deg")
            expr = expr.replace("tan", "tan_deg")

        return expr

    def add_to_history(self, expr):
        if self.MAX_HISTORY_SIZE <= 0:
            return

        size = len(self.history)

        if size > 0 and self.history[-1] == expr:
            return

        if size >= self.MAX_HISTORY_SIZE:
            start = size - (self.MAX_HISTORY_SIZE - 1)
            self.history = self.history[start:]

        self.history.append(expr)


root = tk.Tk()
app = Calculator(root)
root.mainloop()
