import mysql.connector
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
import sys

# establish a connection to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Denji123@",
    database="university"
)

if mydb.is_connected():
    print("Connection successful")
else:
    print("Connection failed")

# define global window variable
window = None


def insert_student():
    global window  # access global window variable

    # create a new window for user input
    input_window = tk.Toplevel(window)

    # create Entry widgets for input fields
    input_first_name = tk.Entry(input_window)
    input_last_name = tk.Entry(input_window)
    input_address = tk.Entry(input_window)
    input_phone_number = tk.Entry(input_window)
    input_email = tk.Entry(input_window)
    input_date_of_birth = tk.Entry(input_window)
    input_password = tk.Entry(input_window)

    # add labels for input fields
    tk.Label(input_window, text="First Name").pack()
    input_first_name.pack()
    tk.Label(input_window, text="Last Name").pack()
    input_last_name.pack()
    tk.Label(input_window, text="Address").pack()
    input_address.pack()
    tk.Label(input_window, text="Phone Number").pack()
    input_phone_number.pack()
    tk.Label(input_window, text="Email").pack()
    input_email.pack()
    tk.Label(input_window, text="Date of Birth").pack()
    input_date_of_birth.pack()
    tk.Label(input_window, text="Password").pack()
    input_password.pack()

    # add a button to save the input and close the window
    save_button = tk.Button(input_window, text="Save", command=lambda: save_data(input_first_name.get(), input_last_name.get(), input_address.get(), input_phone_number.get(), input_email.get(), input_date_of_birth.get(), input_password.get()))
    save_button.pack()

    # define function to save data to database
    def save_data(first_name, last_name, address, phone_number, email, date_of_birth, password):
        # execute the insert statement
        cursor = mydb.cursor()
        sql = "INSERT INTO Student (first_name, last_name, address, phone_number, email, date_of_birth, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (first_name, last_name, address, phone_number, email, date_of_birth, password)
        cursor.execute(sql, val)
        mydb.commit()

        # clear the input fields
        input_first_name.delete(0, tk.END)
        input_last_name.delete(0, tk.END)
        input_address.delete(0, tk.END)
        input_phone_number.delete(0, tk.END)
        input_email.delete(0, tk.END)
        input_date_of_birth.delete(0, tk.END)
        input_password.delete(0, tk.END)

        # close the input window
        input_window.destroy()

    # wait for user to enter data
    input_window.wait_window(input_window)

def register():
    insert_student()

def close_program():
    window.destroy()

def login():
    input_window = tk.Toplevel(window)

    # create a label and Entry widget to get the student ID
    tk.Label(input_window, text="Email").pack()
    input_Email = tk.Entry(input_window)
    input_Email.pack()

    # create a label and Entry widget to get the password
    tk.Label(input_window, text="Password").pack()
    input_password = tk.Entry(input_window, show="*")
    input_password.pack()

    # create a button to submit the login credentials
    tk.Button(input_window, text="Login", command=lambda: authenticate(input_Email.get(), input_password.get(), input_window)).pack()

def authenticate(student_id, password, input_window):
    cursor = mydb.cursor()
    query = "SELECT * FROM Student WHERE Email =%s AND Password =%s"
    cursor.execute(query, (student_id, password))
    result = cursor.fetchone()

    if result is None:
        # authentication failed, show error message
        tk.messagebox.showerror("Error", "Invalid student ID or password")
    else:
        # authentication successful, close the login window and the main window
        tk.messagebox.showinfo("Success", "Login successful")
        input_window.destroy()
        window.destroy()

def close_program():
    window.destroy()
    sys.exit()

def main_screen():
    global window  # access global window variable
    window = tk.Tk()
    window.geometry("300x250")
    window.title("University Database")

    # bind the X button to close the program
    window.protocol("WM_DELETE_WINDOW", close_program)

    tk.Label(text="Student Login and Registration", bg="grey", width="300", height="2", font=("Calibri", 13)).pack()
    tk.Label(text="").pack()
    tk.Button(text="Login", height="2", width="30", command=login).pack()
    tk.Label(text="").pack()
    tk.Button(text="Register", height="2", width="30", command=register).pack()

    window.mainloop()

main_screen()

#define the function to select students
def select_students():
    # clear the existing data
    for item in treeview.get_children():
        treeview.delete(item)

    # select all students from the database
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()

    # insert each student into the Treeview widget
    for i, student in enumerate(students):
        treeview.insert("", "end", text=student[0], values=student[:-1])

def delete_menu(event, student_id):
    menu = tk.Menu(window, tearoff=0)
    menu.add_command(label="Delete", command=lambda: delete_student(student_id))
    menu.post(event.x_root, event.y_root)


def delete_student():
    # prompt the user to enter the student id to delete
    student_id = simpledialog.askstring("Delete Student", "Enter the ID of the student to delete:")

    if not student_id:
        return

    # create a confirmation dialog box
    if not tk.messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this student?"):
        return

    # execute the delete statement
    cursor = mydb.cursor()
    sql = "DELETE FROM Student WHERE Student_ID=%s"
    val = (student_id,)
    cursor.execute(sql, val)
    mydb.commit()

    # reset the AUTO_INCREMENT value for the Student_ID column
    sql = "ALTER TABLE Student AUTO_INCREMENT = 1"
    cursor.execute(sql)
    mydb.commit()

    # refresh the Treeview widget
    select_students()

def update_student():
    input_window = tk.Toplevel(window)

    # create a label and Entry widget to get the student ID
    tk.Label(input_window, text="Student ID").pack()
    input_student_id = tk.Entry(input_window)
    input_student_id.pack()

    # add a button to retrieve the student ID and update the data
    update_button = tk.Button(input_window, text="Update", command=lambda: retrieve_update_data(input_student_id.get()))
    update_button.pack()

def retrieve_update_data(student_id):
    # create a new window for user input
    input_window = tk.Toplevel(window)

    # create Entry widgets for input fields
    input_email = tk.Entry(input_window)
    input_phone_number = tk.Entry(input_window)
    input_address = tk.Entry(input_window)

    # add labels for input fields
    tk.Label(input_window, text="Email").pack()
    input_email.pack()
    tk.Label(input_window, text="Phone Number").pack()
    input_phone_number.pack()
    tk.Label(input_window, text="Address").pack()
    input_address.pack()

    # add a button to save the input and close the window
    save_button = tk.Button(input_window, text="Save",
                            command=lambda: save_update_data(student_id, input_email.get(), input_phone_number.get(), input_address.get()))
    save_button.pack()

def save_update_data(student_id, email, phone_number, address):
    # create a confirmation dialog box
    if not tk.messagebox.askyesno("Confirm Update", "Are you sure you want to update this student?"):
        return

    # execute the update statement with the modified columns
    cursor = mydb.cursor()
    sql = "UPDATE Student SET "
    val = []
    if email:
        sql += "Email=%s, "
        val.append(email)
    if phone_number:
        sql += "Phone_Number=%s, "
        val.append(phone_number)
    if address:
        sql += "Address=%s, "
        val.append(address)
    # remove the last comma and space from the statement
    sql = sql[:-2]
    # add the WHERE clause and the student ID parameter
    sql += " WHERE Student_ID=%s"
    val.append(student_id)

    cursor.execute(sql, tuple(val))
    mydb.commit()

    # refresh the Treeview widget
    select_students()



# create a window
window = tk.Tk()

window.title("My Application")
window.geometry("1500x700")

label = tk.Label(window, text="Welcome to the university database!")
label.pack()

button = tk.Button(window, text="Show students in database.", command=select_students)
button.pack()

insert_button = tk.Button(window, text="Insert student", command=insert_student)
insert_button.pack()

delete_button = tk.Button(window, text="Delete student", command=delete_student)
delete_button.pack()

update_button = tk.Button(window, text="Update student", command=update_student)
update_button.pack()

# create a Treeview widget
style = ttk.Style()
style.configure("Treeview.Heading", padx=5, pady=3)

treeview = ttk.Treeview(window, columns=("ID", "First Name", "Last Name", "Address", "Phone Number", "Email", "Date of Birth"))

# set column widths and stretching
treeview.column("#0", width=0, stretch=False)
treeview.column("ID", minwidth=100, stretch=False)
treeview.column("First Name", minwidth=100, stretch=False)
treeview.column("Last Name", minwidth=100, stretch=False)
treeview.column("Address", minwidth=150, stretch=False)
treeview.column("Phone Number", minwidth=100, stretch=False)
treeview.column("Email", minwidth=200, stretch=False)
treeview.column("Date of Birth", minwidth=100, stretch=False)

# add column headings
treeview.heading("ID", text="ID", anchor="w")
treeview.heading("First Name", text="First Name", anchor="w")
treeview.heading("Last Name", text="Last Name", anchor="w")
treeview.heading("Address", text="Address", anchor="w")
treeview.heading("Phone Number", text="Phone Number", anchor="w")
treeview.heading("Email", text="Email", anchor="w")
treeview.heading("Date of Birth", text="Date of Birth", anchor="w")
treeview.pack()

# start the main event loop
window.mainloop()
