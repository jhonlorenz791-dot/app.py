## Employee Information and Leave Management System

**Employee Information and Leave Management System** is a web-based application that connects employees with Human Resources by storing records and leave information in a centralized database. It simplifies HR tasks, reduces paperwork, speeds up processing, and ensures data is organized and accurate. The system allows HR to manage employee records by adding new employees, view all employee list, editing employee information, approve/reject leave request and view all reports. It also enables employees to view their own profile, submit leave request, cancel leave request and view all history of their leave.

---

## Developers (BSCS-1B)
* **Japay, John Lorenz**
* **Huit, John Christian**
* **Zafra, Lonaliza**
* **Mangmang, Ronald**

---

## Prerequisites
Before running the project, ensure you have the following installed:
  * **VScode**
  * **Python 3.11.9**
  * **VScode extension** ('Pylance - Python - Python Debugger - Python environments')
  * **Templates folder**
  * **Github**
  * **Git**
  * **Python Flask**

---

## Installation:
    1.Git Clone: HTTPS-https://github.com/jhonlorenz791-dot/app.py.git
      SSH - git@github.com:jhonlorenz791-dot/app.py.git 
      GitHub CLI - gh repo clone jhonlorenz791-dot/app.py

    2. PIP Flask Flask Install PIP - version 3.1.3

    3. Save the code- Save the python code in app.py in your folder
    
    4. Application Link - http://127.0.0.1:5000/login

---

## Usage Guide

## Authentication

Use the following credentials to access the available user roles of the system:

* **Admin Access**
    * **Username:** admin
    * **Password:** admin123
* **Employee Access**
    * **Username:** employee
    * **Password:** employee123

 After a successful login, it determines the user’s role (Admin or Employee) and displays the appropriate dashboard based on their role.

## Admin Dashboard and Action Selection

* **Employee list:** 
* **Register New Employee**
* **Edit Existing Profile**
* **Leave Requests**
* **View all reports**

---

## Module Description

Completed Module:

## Module 1:Admin Dashboard and Action Selection

it allows admin to choose action:

* View Employee List: it allows the Admin to see all registered employees in the system.
* Register New Employee: it allows the Admin to add a new employee to the system.
* Edit Employee Information: it allows the Admin to modify employee personal information
* Leave Requests: it allows the Admin to see all submitted leave applications.
* View all reports: it allows the Admin to see all reports of the employee.

---

## Module 2: Register New Employee (Admin Dashboard)

This module allows the admin to add and register new employees into the system. Through the admin dashboard, the admin can:

* Add a new employee record
* Enter the employee’s full name
* Enter the employee’s home address
* Assign a unique employee ID
* Input the employee’s contact number
* Create a username and password for the employee’s system account

* The system verifies that each employee ID is unique if a duplicate ID is entered an error message will be displayed and the registration will not proceed. Additionally all required fields must be completed before submission. If any field is left blank the system will show the admin with an appropriate error message and prevent the data from being saved.

---

## Module 3: Edit Employee Information (Admin Dashboard)

the admin can modify the following information:

* Employee Full Name
* Employee Address
* Employee Conact Number

* We ensure that all required fields must be completed before any changes can be saved. If the admin attempts to submit the form with missing or incomplete information, the system will display an appropriate error message and prevent the update from being saved.

---

## Module 4: View All Employee List (Admin Dashboard)

This module allows the administrator to view a complete list of all registered employees in the system. Through the admin dashboard, the following employee details are displayed:

* Employee ID
* Employee Full Name
* Employee Address
* Employee Contact Number
* Employee Leave Credits

* The View All Employee List feature provides a centralized overview of employee records, making it easier for the admin to monitor, verify, and manage employee information efficiently. It ensures that important details are readily accessible, supporting better decision-making and record management within the system.