import tkinter #Tkinter is Python’s built-in toolkit for creating graphical user interfaces (GUIs)

button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

right_symbols = ["÷", "*", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]

color_black = "#1C1C1C"
color_light_gray = "#E5E515"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

# Window setup
window = tkinter.Tk()
window.title("Calculator")
window.resizable(False, False)

frame = tkinter.Frame(window)
frame.pack()

# Display label
label = tkinter.Label(frame, text="0", font=("arial", 45),
                      background=color_black, foreground=color_white, anchor="e")
label.grid(row=0, column=0, columnspan=4, sticky="we")

# Expression tracker
expression = ""

# Button click handler
def button_clicked(value):
    global expression

    if value == "AC":
        expression = ""
        label.config(text="0")
    elif value == "+/-":
        if expression.startswith("-"):
            expression = expression[1:]
        else:
            expression = "-" + expression
        label.config(text=expression)
    elif value == "%":
        try:
            result = str(eval(expression) / 100)
            expression = result
            label.config(text=result)
        except:
            label.config(text="Error")
    elif value == "=":
        try:
            result = str(eval(expression.replace("÷", "/").replace("√", "**0.5")))
            expression = result
            label.config(text=result)
        except:
            label.config(text="Error")
    elif value == "√":
        expression += "**0.5"
        label.config(text=expression)
    else:
        expression += value.replace("÷", "/")
        label.config(text=expression)

# Create buttons
for row in range(len(button_values)):
    for column in range(len(button_values[row])):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, font=("arial", 20),
                                width=5, height=2,
                                command=lambda value=value: button_clicked(value))
        if value in top_symbols:
            button.configure(foreground=color_black, background=color_light_gray)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_orange)
        else:
            button.config(foreground=color_white, background=color_dark_gray)

        button.grid(row=row + 1, column=column)

window.mainloop()
