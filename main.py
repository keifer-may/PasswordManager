from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    if len(password_entry.get()) > 0:
        password_entry.delete(0, END)
    else:
        pass

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for i in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for i in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for i in range(random.randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, string=f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def add_password():
    website_name = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website_name: {
            "email": email,
            "password": password,
        }
    }

    if len(website_name) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you have entered a password and website.")
    else:
        is_ok = messagebox.askokcancel(title=website_name, message=f"These are the details provided:\nEmail: {email}\nPassword: {password}\nIs it okay to save this?")
        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
                    data.update(new_data)
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
        else:
            pass


# ----------------------------Search Data for Password & Email-------------------------#

def search_data():
    website_name = website_entry.get()

    if len(website_name) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you have provided a website to search for.")
    else:
        try:
            with open("data.json", "r") as file:
                data_dict = json.load(file)
                email = data_dict[website_name]["email"]
                password = data_dict[website_name]["password"]
                messagebox.showinfo(title=website_name,
                                    message=f"The email for {website_name} is: \n          {email}\n  and the password is: \n          {password}")
        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="You haven't used the password manager yet.")
        except KeyError:
            messagebox.showinfo(title="Oops",
                                message=f'Please make sure the website you\'ve provided is spelled correctly and you have an account there.\nYou provided "{website_name}" as the website.')


# ---------------------------- UI SETUP ----------------------------------#
window = Tk()
window.title("Password Manager")
window.minsize(220, 220)
window.config(padx=40, pady=40)

canvas = Canvas(width=200, height=200, highlightthickness=0)
lock = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock)
canvas.grid(row=0, column=1)

website_label = Label(text="Website: ")
website_label.grid(row=1, column=0)

website_entry = Entry(width=32)
website_entry.grid(row=1, column=1)
website_entry.focus()

search_button = Button(text="Search Websites", width=15, command=search_data)
search_button.grid(row=1, column=2)

email_label = Label(text="Email/Username: ")
email_label.grid(row=2, column=0)

email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password: ")
password_label.grid(row=3, column=0)

password_entry = Entry(width=32)
password_entry.grid(row=3, column=1)

password_button = Button(text="Generate Password", width=15, command=generate_password)
password_button.grid(row=3, column=2)

add_pass_button = Button(text="Add Password", width=45, command=add_password)
add_pass_button.grid(row=4, column=1, columnspan=2)

window.mainloop()

