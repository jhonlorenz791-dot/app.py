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

it allows admin to:

* View Employee List: it allows the Admin to see all registered employees in the system.
* Register New Employee: it allows the Admin to add a new employee to the system.
* Edit Existing Profile: it allows the Admin to modify employee personal information
* Leave Requests: it allows the Admin to see all submitted leave applications.
* View all reports: it allows the Admin to see all reports of the employee.

## Module 2: Register New Employee (Admin Dashboard)

it allows admin to:

* Add new employee
* Input the full name of the employee
* Input the home address of the employee
* Input the ID of the employee
* Input the contact number of the employee
* Create Employee account

* We enhance this module so the admin can add the employee information especially the password and username so he/she can access the system when they are registered. We ensure that the ID of every employee is unique and display a error message if the ID already existed and	all required fields must be filled out.