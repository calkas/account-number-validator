from account_number_validator import AccountNumberValidator
import ocr_account_number_processor
import os
from tkinter import *
from tkinter import filedialog
from PIL import Image
from tkinter import messagebox

image_file = None


def browse_image_file():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select a File",
                                          filetypes=(
                                              ("Image png", "*.png"), ("Image jpg", "*.jpg"), ("all files", "*.*")))
    message_output_box.config(bg=default_color, text="")
    global image_file
    image_file = Image.open(filename)
    messagebox.showinfo("Information", filename + "\n\nFile loaded!")


def validate():
    if not image_file:
        messagebox.showerror("Error", "Select image first")
        return

    input_account_number = input_account_number_box.get()
    anv = AccountNumberValidator()
    status = anv.determine_type_of_account_number(input_account_number)

    if not status[0]:
        messagebox.showerror("Error", status[1])
        return

    account_format_pattern_type = anv.get_account_number_pattern()

    parsed_account_number = ocr_account_number_processor.get_number_account_from_image(image_file,
                                                                                       account_format_pattern_type)
    is_good = anv.is_valid(parsed_account_number)
    percentage_of_correctness = str(int(anv.get_percentage_of_correctness())) + "%"

    output_msg = ("Input Account Number:\n" + input_account_number + "\nParsed Account Number:\n" +
                  parsed_account_number + "\n\nMatched in " + percentage_of_correctness)

    if is_good:
        messagebox.showinfo("Information", "Validation Passed")
        message_output_box.config(bg='lightgreen', text=output_msg)
        print("Validation process - \x1b[32mPASSED\x1b[0m")
    else:
        messagebox.showerror("Error", "Validation Failed!\n\nMatched in " + percentage_of_correctness)
        message_output_box.config(bg='WhiteSmoke', text=output_msg)
        print("Validation process - \x1b[31mFAILED\x1b[0m")

    anv.generate_report()


# Create the root window
window = Tk()

# Set window title
window.title('Bank Account Number Validator')

# Set window size
window.geometry("400x300")

default_color = window.cget("bg")

# GUI
input_label = Label(window, text="Account Number:")

input_account_number_box = Entry(window, selectbackground="lightblue", selectforeground="black", width=35)

browse_button = Button(window, text="Browse  ", width=25, command=browse_image_file)

validate_button = Button(window, text="Validate", width=25, command=validate)

output_label = Label(window, text="Output:")

message_output_box = Message(window, text="", width=250)

input_label.pack()
input_account_number_box.pack(pady=10)
browse_button.pack()
validate_button.pack()
output_label.pack(pady=10)
message_output_box.pack()

# Let the window wait for any events
window.mainloop()
