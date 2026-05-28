"""Improved calculator GUI using tkinter with a safe evaluator.

Features:
- Safe expression evaluation using AST (no use of eval on raw input)
- Basic arithmetic, power, parentheses
- Buttons: AC, DEL, +/-, %, √, digits, operators, =
- Keyboard support for numbers/operators, Enter, Backspace, Escape
"""

import tkinter as tk
import ast
import math


class SafeEvaluator:
    """Evaluate a simple arithmetic expression safely using AST."""

    @staticmethod
    def eval(expr: str) -> float:
        node = ast.parse(expr, mode="eval").body
        return SafeEvaluator._eval(node)

    @staticmethod
    def _eval(node):
        if isinstance(node, ast.BinOp):
            left = SafeEvaluator._eval(node.left)
            right = SafeEvaluator._eval(node.right)
            op = node.op
            if isinstance(op, ast.Add):
                return left + right
            if isinstance(op, ast.Sub):
                return left - right
            if isinstance(op, ast.Mult):
                return left * right
            if isinstance(op, ast.Div):
                return left / right
            if isinstance(op, ast.Mod):
                return left % right
            if isinstance(op, ast.Pow):
                return left ** right
            raise ValueError("Unsupported binary operator: %s" % type(op))

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -SafeEvaluator._eval(node.operand)

        if isinstance(node, ast.Num):
            return node.n

        if hasattr(ast, 'Constant') and isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

        if isinstance(node, ast.Expression):
            return SafeEvaluator._eval(node.body)

        # disallow everything else (calls, names, attributes, etc.)
        raise ValueError("Unsupported expression")


class CalculatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Calculator")
        root.resizable(False, False)

        self.display_var = tk.StringVar(value="0")
        self._expression = ""

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        display = tk.Label(self.root, textvariable=self.display_var,
                           font=("Segoe UI", 36), anchor="e", bg="#222", fg="#fff",
                           padx=10)
        display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        buttons = [
            ["AC", "DEL", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "+/-", "="]
        ]

        btn_specs = {
            "fg": "#fff",
            "bg": "#333",
            "font": ("Segoe UI", 18),
            "width": 5,
            "height": 2,
            "bd": 0,
            "activebackground": "#444",
        }

        for r, row in enumerate(buttons, start=1):
            for c, val in enumerate(row):
                action = lambda v=val: self._on_button(v)
                b = tk.Button(self.root, text=val, command=action, **btn_specs)

                # style special buttons
                if val in ("/", "*", "-", "+", "="):
                    b.config(bg="#ff9500")
                elif val in ("AC", "DEL", "%", "+/-"):
                    b.config(bg="#a6a6a6", fg="#000")

                b.grid(row=r, column=c, padx=4, pady=4)

        # make the 0 button span two columns
        zero = tk.Button(self.root, text="0", command=lambda: self._on_button("0"), **btn_specs)
        zero.grid(row=5, column=0, columnspan=2, sticky="we", padx=4, pady=4)

    def _bind_keys(self):
        self.root.bind('<Key>', self._on_key)
        self.root.bind('<Return>', lambda e: self._on_button('='))
        self.root.bind('<BackSpace>', lambda e: self._on_button('DEL'))
        self.root.bind('<Escape>', lambda e: self._on_button('AC'))

    def _on_key(self, event):
        ch = event.char
        if ch.isdigit() or ch in '.+-*/()%':
            self._append(ch)
        elif ch == '\r':
            self._on_button('=')

    def _on_button(self, value: str):
        if value == 'AC':
            self._expression = ''
            self.display_var.set('0')
            return

        if value == 'DEL':
            self._expression = self._expression[:-1]
            self.display_var.set(self._expression or '0')
            return

        if value == '+/-':
            # toggle sign of the current expression value
            try:
                val = SafeEvaluator.eval(self._expression) if self._expression else 0
                val = -val
                self._expression = str(val)
                self.display_var.set(self._expression)
            except Exception:
                self.display_var.set('Error')
            return

        if value == '%':
            try:
                val = SafeEvaluator.eval(self._expression) if self._expression else 0
                val = val / 100.0
                self._expression = str(val)
                self.display_var.set(self._expression)
            except Exception:
                self.display_var.set('Error')
            return

        if value == '√':
            try:
                val = SafeEvaluator.eval(self._expression) if self._expression else 0
                val = math.sqrt(val)
                self._expression = str(val)
                self.display_var.set(self._expression)
            except Exception:
                self.display_var.set('Error')
            return

        if value == '=':
            try:
                # replace any accidental Unicode division signs
                expr = self._expression.replace('÷', '/')
                result = SafeEvaluator.eval(expr)
                # format result nicely
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self._expression = str(result)
                self.display_var.set(self._expression)
            except Exception:
                self.display_var.set('Error')
            return

        # default: append button value to the expression
        self._append(value)

    def _append(self, text: str):
        # avoid multiple leading zeros like "00"
        if self._expression == '0' and text.isdigit():
            self._expression = text
        else:
            self._expression += text
        self.display_var.set(self._expression)


def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
