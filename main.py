from tkinter import *
from tkinter import messagebox
from letters import generate_password
import pyperclip
import json

EMAIL = "bobbypetts@gmail.com"


def find_password():
    entered_website = website_entry.get()
    try:
        with open('passwords.json', 'r') as file:
            pw_data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="File Not Found", message="passwords.json not found in directory.")
    else:
        if entered_website in pw_data:
            email = pw_data[f"{entered_website}"]["email"]
            password = pw_data[f"{entered_website}"]["password"]
            messagebox.showinfo(title=f"{entered_website}", message=f"Email: {email}\nPassword: {password}")
        elif entered_website == "":
            messagebox.showinfo(message="Please enter a website to search credentials for.")
        else:
            messagebox.showinfo(title=f"{entered_website}", message=f"Entry does not exist for {entered_website}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    password_entry.delete(0, END)
    newpass = generate_password()
    password_entry.insert(0, newpass)
    pyperclip.copy(newpass)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def delete_data():
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    email_user_entry.delete(0, END)
    email_user_entry.insert(END, EMAIL)


def save_data():
    website = str(website_entry.get())
    email = str(email_user_entry.get())
    password = str(password_entry.get())
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if website == "" or email == "" or password == "":
        messagebox.showinfo(title="WARNING", message="Please make sure all fields are filled in and try again.")
    else:
        is_ok = messagebox.askokcancel(title="New Entry", message=f"These are the details entered: \n" +
                                                                  f"Website: {website}\n" +
                                                                  f"Email {email}\nPassword: {password}\n" +
                                                                  f"Would you like to save?")
        if is_ok:
            try:
                with open('passwords.json', 'r') as file:
                    # reading old data
                    data = json.load(file)
                    # updating old data with new data
                    data.update(new_data)
            except FileNotFoundError:
                with open('passwords.json', 'w') as file:
                    json.dump(new_data, file, indent=4)
                    # updating old data with new data
            else:
                data.update(new_data)
            finally:
                delete_data()


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=33)
website_entry.grid(column=1, row=1, sticky='w')
website_entry.focus()

email_user_label = Label(text="Email/Username:")
email_user_label.grid(column=0, row=2)

email_user_entry = Entry(width=51)
email_user_entry.grid(column=1, columnspan=2, row=2, sticky='w')
# email_user_entry.insert(0, "bobbypetts@gmail.com")
email_user_entry.insert(END, EMAIL)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=33)
password_entry.grid(column=1, row=3, sticky='w', padx=0)

generate = Button(text="Generate Password", width=14, command=generate)
generate.grid(row=3, column=2)

search = Button(text="Search", width=14, command=find_password)
search.grid(row=1, column=2)

add_button = Button(text="Add", width=43, command=save_data)
add_button.grid(column=1, columnspan=2, sticky='w', row=4)

window.mainloop()
