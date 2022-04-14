from doctest import master
from tkinter import *
from tkinter import messagebox
from lab_7.employees import Employee
from lab_7.workplace import workplace

root = Tk()

LIST_EMPLOYEES = []
WORKPLACES = []
EMPLOYEES_ID = []


def check_valid():
    """
    Функция проверяет информацию о работнике на корректный ввод
    :return: 1 при корректном вводе, 0 при некорректном
    """
    if employee_first_name.get() and  \
            employee_last_name.get() and employee_workplace.get() and \
            employee_position.get() and employee_id.get() not \
            in EMPLOYEES_ID:
        try:
            int(employee_id.get())
        except ValueError:
            return 0
        try:
            int(employee_salary.get())
        except ValueError:
            return 0
        return 1
    else:
        return 0


def delete_employee_from_list(employee_number):
    """
    Функция удаляет работников из списка
    :param employee_number:
    :return:
    """
    LIST_EMPLOYEES.pop(int(employee_number)-1)
    messagebox.showinfo(title='Employee deleted',
                        message=f'employee {employee_number}'
                                f' has been deleted!')


def btn_about_click():
    """
    Функция открывает новое окно с информацией о программе
    :return:
    """
    about_window = Toplevel(master)
    about_window.title("Program info")
    about_window.geometry("600x300")
    Label(about_window, text="Program to manage employees\n\n"
                             "Based on Program from task 7\n"
                             "Allows to add/delete new employees and manage "
                             "Workplaces\n\nVersion 1.0\nMade by Daniil "
                             "Shynkarenko\n\n© 2021 Daniil Shynkarenko "
                             "dahhwe@gmail.com", font=("Helvetica", 15)).pack()


def add_employee():
    """
    Функция добавляет нового сотрудника в список LIST_EMPLOYEES
    :return:
    """

    first_name = employee_first_name.get()
    last_name = employee_last_name.get()
    place_of_work = employee_workplace.get()
    position = employee_position.get()
    salary = employee_salary.get()
    employee_info = Employee(first_name, last_name, place_of_work,
                             position,
                             salary)
    LIST_EMPLOYEES.append(employee_info)


def clear_employees_frame():
    """
    Функция отчищает frame_employees
    :return:
    """
    for widgets in frame_employees.winfo_children():
        widgets.destroy()


def btn_show_employees_click():
    """
    Функция вызывается при нажатии на кнопку shpw_employees
    :return:
    """
    clear_employees_frame()
    if not LIST_EMPLOYEES:
        lbl_no_employees = Label(frame_employees,
                                 text='No employees', bg='red',
                                 font=("Helvetica", 15))
        lbl_no_employees.grid(row=1, column=3)
    else:
        for i, val in enumerate(LIST_EMPLOYEES):
            list_to_output = Employee.list_data(LIST_EMPLOYEES[i])
            lbl_show_employees = Label(frame_employees,
                                       text=f'{i+1} — {list_to_output}',
                                       font=("Helvetica", 15), anchor="w")
            lbl_show_employees.grid(sticky=W, row=1+i, column=3)


def btn_show_workplaces_click():
    """
    Функция выводит список мест работы на главное окно
    """
    for i, val in enumerate(WORKPLACES):
        list_to_output = workplace.list_data(WORKPLACES[i])
        lbl_show_workplaces = Label(frame_workplaces,
                                    text=f'{list_to_output}',
                                    font=("Helvetica", 15),
                                    anchor="w")
        lbl_show_workplaces.grid(sticky=W, row=1+i, column=3)


def check_valid_delete_input():
    """
    Функция проверят на корректный ввод
    :return: Возвращает 1 при корректном вводе, 0 при некорректном
    """
    try:
        int(delete_employee.get())
    except ValueError:
        return 0
    return 1


def btn_add_employee_click():
    """
    Функция добавляет работника
    :return:
    """
    valid_employee = check_valid()
    if valid_employee:
        EMPLOYEES_ID.append(employee_id.get())
        emp_add_msg = f'{employee_first_name.get()} has been added!'
        messagebox.showinfo(title='New employee', message=emp_add_msg)
        add_employee()
        btn_show_employees_click()
    else:
        messagebox.showinfo(title='Incorrect input',
                            message='Input is INCORRECT!')


def btn_delete_employee_click():
    """
    Функция удаляет работника
    :return:
    """
    valid_delete_input = check_valid_delete_input
    if not LIST_EMPLOYEES:
        messagebox.showinfo(title='Empty employees list',
                            message='Employees not show or not present!')
    elif delete_employee.get() and valid_delete_input:
        if int(delete_employee.get()) > len(LIST_EMPLOYEES) or \
                int(delete_employee.get()) <= 0:
            messagebox.showinfo(title='Out of range',
                                message='Input is out of range!')
        else:
            delete_employee_from_list(delete_employee.get())
            btn_show_employees_click()
    else:
        messagebox.showinfo(title='incorrect input',
                            message='Input is INCORRECT!')


def get_employees_list():
    """
    Получен список сотрудников
    :return:
    """
    emp_1 = Employee('Tyler', 'Joseph', 'office', 'manager', '50000')
    emp_2 = Employee('Seamus', 'Smith', 'technical center', 'engineer', '4200')
    emp_3 = Employee('Isac', 'Nel', 'store', 'salesman', '20000')
    if not LIST_EMPLOYEES:
        LIST_EMPLOYEES.append(emp_1)
        LIST_EMPLOYEES.append(emp_2)
        LIST_EMPLOYEES.append(emp_3)


def get_workplaces_list():
    """
    Функция получает информацию о местах работы
    :return:
    """
    workplace_1 = workplace('Headquaters', 'Baker st. 221b', 'Russia',
                            'Senior programmer')
    workplace_2 = workplace('Research dev.', 'Gleneagles ave 10', 'Russia',
                            '3 years experience')
    workplace_3 = workplace('Shop', 'epidemic ave 54', 'Russia',
                            'Salesman skills')
    WORKPLACES.append(workplace_1)
    WORKPLACES.append(workplace_2)
    WORKPLACES.append(workplace_3)


btn_add_employee = \
    Button(root, text='Add an employee',
           command=btn_add_employee_click,
           font=("Helvetica", 15))

btn_delete_employee = \
    Button(root, text='Delete employee',
           command=btn_delete_employee_click, fg='red',
           font=("Helvetica", 15))
btn_about = \
    Button(root, text='About', padx=50,
           command=btn_about_click, fg='green', font=("Helvetica", 15))

frame_employees = Frame(root, padx=20, pady=5)
frame_workplaces = Frame(root, padx=20, pady=5)

lbl_employees_title = Label(root, text='Employees:',
                            font=("Helvetica", 15))
lbl_workplaces_title = Label(root, text='Workplaces:',
                             font=("Helvetica", 15))
lbl_add_employee_title = Label(root, text='Add an employee:',
                               font=("Helvetica", 15))
lbl_add_employee_id = Label(root, text='Enter Employees id:',
                            font=("Helvetica", 15))
lbl_employee_first_name = Label(root, text='Enter First name:',
                                font=("Helvetica", 15))
lbl_employee_last_name = Label(root, text='Enter Last name:',
                               font=("Helvetica", 15))
lbl_employee_workplace = Label(root, text='Enter Workplace:',
                               font=("Helvetica", 15))
lbl_employee_position = Label(root, text='Enter Position:',
                              font=("Helvetica", 15))
lbl_employee_salary = Label(root, text='Enter Salary:',
                            font=("Helvetica", 15))
lbl_delete_employee = Label(root,
                            text='Enter Employee number\n'
                                 ' to delete:',
                            font=("Helvetica", 15))

employee_id = Entry(root, width=40, borderwidth=3)
employee_first_name = Entry(root, width=40, borderwidth=3)
employee_last_name = Entry(root, width=40, borderwidth=3)
employee_workplace = Entry(root, width=40, borderwidth=3)
employee_position = Entry(root, width=40, borderwidth=3)
employee_salary = Entry(root, width=40, borderwidth=3)
delete_employee = Entry(root, width=40, borderwidth=3)

frame_workplaces.grid(row=10, column=3)
frame_employees.grid(row=1, column=3)

lbl_employees_title.grid(row=0, column=3)
lbl_workplaces_title.grid(row=8, column=3)
lbl_add_employee_title.grid(row=0, column=0, sticky=E)
lbl_add_employee_id.grid(row=1, column=0, sticky=E)
lbl_employee_first_name.grid(row=2, column=0, sticky=E)
lbl_employee_last_name.grid(row=3, column=0, sticky=E)
lbl_employee_workplace.grid(row=4, column=0, sticky=E)
lbl_employee_position.grid(row=5, column=0, sticky=E)
lbl_employee_salary.grid(row=6, column=0, sticky=E)
lbl_delete_employee.grid(row=10, column=0, sticky=E)

employee_id.grid(row=1, column=1)
employee_first_name.grid(row=2, column=1)
employee_last_name.grid(row=3, column=1)
employee_workplace.grid(row=4, column=1)
employee_position.grid(row=5, column=1)
employee_salary.grid(row=6, column=1)
delete_employee.grid(row=10, column=1)

btn_delete_employee.grid(row=11, column=1)
btn_about.grid(row=11, column=0)
btn_add_employee.grid(row=8, column=1)

# btn_show_employees = \
#     Button(root, text='Show employees', padx=50,
#            command=btn_show_employees_click)
# btn_show_employees.grid(row=0, column=3)


def run():
    """
    Функция запускается при запуске программы
    :return:
    """
    get_employees_list()
    get_workplaces_list()
    btn_show_employees_click()
    btn_show_workplaces_click()
    root.mainloop()


if __name__ == '__main__':
    run()
