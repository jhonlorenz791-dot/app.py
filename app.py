from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "Secret123"

# --- CLASSES ---

class User:
    def __init__(self, username, password, role, linked_emp_id=None):
        self._username = username
        self._password = password  
        self._role = role.lower()
        self.linked_emp_id = linked_emp_id

    def get_username(self):
        return self._username

    def get_role(self):
        return self._role.capitalize()

    def check_login(self, input_user, input_pass):
        return self._username == input_user and self._password == input_pass

class Employee:
    employee_data = {} 

    def __init__(self, emp_id, name, address, contact):
        self._emp_id = str(emp_id)
        self._name = name
        self._address = address
        self._contact = contact
        self.leave_credits = 10 

    def get_emp_id(self): return self._emp_id
    def get_name(self): return self._name
    def get_address(self): return self._address
    def get_contact(self): return self._contact

    def update_emp_info(self, new_name, new_address, new_contact):
        if new_name: self._name = new_name
        if new_address: self._address = new_address
        if new_contact: self._contact = new_contact

    @classmethod
    def add_new_employee(cls, name, emp_id, address, contact, user_name, user_password):
        if str(emp_id) in cls.employee_data:
            return False
        new_emp = Employee(emp_id, name, address, contact)
        cls.employee_data[str(emp_id)] = new_emp
        users_db.append(User(user_name, user_password, "Employee", linked_emp_id=str(emp_id)))
        return True

class LeaveSystem:
    leave_requests = [] 
    
    @classmethod
    def apply_leave(cls, name, emp_id, reason, leave_date, req_type="Leave Request"):
        request_data = {
            "name": name,
            "id": str(emp_id),
            "leave_date": leave_date,
            "reason": reason, 
            "type": req_type,
            "status": "Pending",
            "date_submitted": datetime.now().strftime("%Y-%m-%d")
        }
        cls.leave_requests.append(request_data)
    
    @classmethod
    def request_cancellation(cls, index, reason):
        if 0 <= index < len(cls.leave_requests):
            req = cls.leave_requests[index]
            # Flowchart Logic: Update to Pending Cancellation
            req['status'] = "Pending Cancellation"
            req['cancel_reason'] = reason
            req['type'] = "Cancellation"
            return True
        return False

# --- DATABASE INITIALIZATION ---

users_db = [
    User("admin", "admin123", "admin"),
    User("employee", "employee123", "employee", linked_emp_id="101")
]
# Initial data para sa testing
Employee.employee_data["101"] = Employee("101", "Juan Dela Cruz", "Manila", "09123456789")

# --- ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('login'))

#MODULE 1: AUTHENTICATION LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Hanapin ang user sa database
        active_user = next((u for u in users_db if u.check_login(username, password)), None)

        if active_user:
            session['user_id'] = active_user.linked_emp_id 
            session['role'] = active_user.get_role() # "Admin" o "Employee"
            session['username'] = active_user.get_username()
            
            if session['role'] == 'Admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('employee_dashboard'))
        
        # kung wrong ang password/username, mobalik sa login nga naay error message 
        return render_template('login.html', error='Invalid username or password')

   
    return render_template('login.html')  

#LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- ADMIN ROUTES ---

#ADMIN DASHBOARD
@app.route('/admindashboard')
def admin_dashboard():
    if session.get('role') != 'Admin':       #Security Check
        return redirect(url_for('login'))

    #Kuhaon tanang employee data para ma-display sa admin dashboard
    all_emps = list(Employee.employee_data.values())

    #Kuhaon tanang leave requests para ma-display sa admin dashboard
    leave_reqs = LeaveSystem.leave_requests

    #kuhaon ang search query gikan sa URL parameters, default empty string kung walay gi-provide          
    query = request.args.get('search', '').lower() 

    #Kung naay search query, i-filter ang employee list base sa name nga nag-match sa query (case-insensitive). Kung walay query, ipakita tanan employees. 
    reports = [e for e in all_emps if query in e.get_name().lower()] if query else all_emps 
    
    #Ipadala ang tanan employee data ug leave requests sa admin dashboard template para ma-display. Apil na ang filtered reports base sa search query.
    return render_template('admindashboard.html', employees=all_emps, leaves=leave_reqs, reports=reports, enumerate=enumerate) 

#MODULE 2: REGISTER UG EMPLOYEE
@app.route('/register_employee', methods=['POST'])
# Route para sa pag-register ng employee; POST dahil form submission ito

def register_employee():
    if session.get('role') != 'Admin':
        # Security check: siguraduhin na Admin lang ang may access sa route na ito. 
        return redirect(url_for('login'))
        
    name = request.form.get('name')
    emp_id = request.form.get('emp_id')
    address = request.form.get('address')
    contact = request.form.get('contact_no')
    username = request.form.get('username')
    password = request.form.get('password')

    if Employee.add_new_employee(name, emp_id, address, contact, username, password):
                #Tawagon ang class method  para mo gamaw ug Employee object ug corresponding user account. 
        flash("Employee registered successfully!", "success")
    else:
        flash("Error: Employee ID already exists!", "danger")
        
    return redirect(url_for('admin_dashboard'))

#MODULE 3: EDIT EMPLOYEE INFORMATION
@app.route('/update_employee', methods=['POST'])
def update_employee():
    if session.get('role') != 'Admin':
        return redirect(url_for('login'))

    emp_id = request.form.get('emp_id')
    name = request.form.get('name')
    address = request.form.get('address')
    contact = request.form.get('contact')

    emp = Employee.employee_data.get(emp_id)
    if emp:
        emp.update_emp_info(name, address, contact)
        flash("Employee updated successfully!", "success")
    else:
        flash("Employee not found.", "danger")

    return redirect(url_for('admin_dashboard'))

# MODULE 4: APPROVE/REJECT LEAVE REQUESTS
@app.route('/handle_leave/<int:index>/<string:action>')
# Route na tumatanggap ng:
# index = position ng leave request sa list
# action = "approve" or "reject"

def handle_leave(index, action):
    # Function na magha-handle ng approval/rejection

    if session.get('role') != 'Admin': 
        # Security check: Admin lang ang pwede
        return redirect(url_for('login'))
        # Kung hindi admin, balik login

    if 0 <= index < len(LeaveSystem.leave_requests):
        # Check kung valid ang index (para iwas error)

        req = LeaveSystem.leave_requests[index]
        # Kunin ang specific leave request gamit ang index

        emp = Employee.employee_data.get(str(req['id']))
        # pangitaon ang employee nga nag-request gamit ang ID

        # Check if the request is still pending to avoid double processing
        if req['status'] not in ['Pending', 'Pending Cancellation']:
            # Kung na-process na (Approved/Rejected/Cancelled)

            flash("This request has already been processed.", "info")
            return redirect(url_for('admin_dashboard'))
            # Iwas double approve/reject

        if action == 'approve':
            # Kapag pinili ng admin ay APPROVE

            if req.get('type') == "Cancellation":
                # Kung cancellation leave request

                req['status'] = "Cancelled"
                # I-set nga cancelled

                if emp: emp.leave_credits += 1
                # Ibalik ang leave credit sa employee

                flash("Cancellation Approved. Credit restored.", "success")

            else:
                # Kung normal leave request

                req['status'] = "Approved"
                # I-approve ang leave

                if emp: emp.leave_credits -= 1
                # Bawasan ng 1 ang leave credits

                flash("Leave Approved. Credit deducted.", "success")

        elif action == 'reject':
            # Kapag REJECT ang pinili

            if req.get('type') == "Cancellation":
                # Kung cancellation leave request

                req['status'] = "Approved"
                # Ibalik sa approved leave (hindi natuloy ang cancel)

                req['type'] = "Leave Request"
                # Ibalik sa original type

                flash("Cancellation Rejected.", "info")

            else:
                # Kung normal leave request

                req['status'] = "Rejected"
                # I-reject ang leave

                flash("Leave Request Rejected.", "warning")

        return redirect(url_for('admin_dashboard'))
        # Pagkahuman sa action, balik sa dashboard
    
# --- EMPLOYEE ROUTES ---

@app.route('/employee_dashboard')  # Route para sa employee dashboard page
def employee_dashboard():
    
    emp_id = session.get('user_id')  # Kuhaon ang user_id gikan sa session (kung naka login na)
    
    if not emp_id:  # Kung walay user_id (dili maka-login)
        flash("Please login first.", "warning")  # Magpakita ug warning message
        return redirect(url_for('login'))  # I-redirect sa login page

    emp_info = Employee.employee_data.get(str(emp_id))  # Kuhaon ang employee info gamit ang ID
    
    if not emp_info:  # Kung walay nakita na employee record
        flash("Employee record not found.", "danger")  # Error message
        return redirect(url_for('login'))  # mobalik sa login

    # Kuhaon ang history ng leave ng employee
    emp_history = [
        (i, req) for i, req in enumerate(LeaveSystem.leave_requests)  # Loop sa tanan leave requests
        if str(req.get('id')) == str(emp_id)  # I-filter kung kinsang employee lang
    ]

    # I-display sa dashboard ang employee info at history
    return render_template('employee_dashboard.html', employee=emp_info, history=emp_history, enumerate=enumerate)


@app.route('/apply_leave', methods=['POST'])  # Route para mag-submit ug leave request
def apply_leave():
    emp_id = session.get('user_id')  # Kuhaon ug balik ang user_id

    if not emp_id:  # Kung wala naka-login
        return redirect(url_for('login'))  # Redirect sa login

    emp_id = str(emp_id)  # himoong string ang ID
    emp_info = Employee.employee_data.get(emp_id)  # Kuhaon employee info

    if emp_info:  # Kung naay valid na employee
        
        # 1. Check kung naay nahibiling leave credits
        if emp_info.leave_credits <= 0:
            flash("Error: You have 0 leave credits left.", "danger")  # Error message
            return redirect(url_for('employee_dashboard'))  # Balik dashboard

        reason = request.form.get('reason')  # Kuhaon ang reason gikan sa form
        
        if not reason:  # Kung walay gibutang na reason
            flash("Error: Please provide a reason.", "warning")
            return redirect(url_for('employee_dashboard'))

        leave_date = request.form.get('leave_date')  # Kuhaon ang leave date
        
        if not leave_date:  # Kung walay date
            flash("Error: Please provide a leave date.", "warning")
            return redirect(url_for('employee_dashboard'))

        # Convert string date to date object
        leave_date_obj = datetime.strptime(leave_date, "%Y-%m-%d").date()
        
        # Check kung past date ang gipili
        if leave_date_obj < date.today():
            flash("Error: Cannot select past dates.", "danger")
            return redirect(url_for('employee_dashboard'))

        # I-save ang leave request sa system
        LeaveSystem.apply_leave(emp_info.get_name(), emp_id, reason, leave_date)
        
        flash("Leave request submitted successfully!", "success")  # Success message
        return redirect(url_for('employee_dashboard'))  # Balik dashboard

    # Kung walay employee info
    flash("Error: Employee information not found.", "danger")
    return redirect(url_for('login'))


@app.route('/cancel_leave/<int:index>', methods=['POST'])  # Route para mag-cancel ug leave
def cancel_leave(index):
    
    reason = request.form.get('cancel_reason')  # Kuhaon ang reason sa cancellation
    
    # Tawgon ang function para mag-request ug cancellation
    if LeaveSystem.request_cancellation(index, reason):
        flash("Cancellation request sent to HR.", "success")  # Success message
    else:
        flash("Error: Cannot cancel leave or invalid request.", "danger")  # Error message
    
    return redirect(url_for('employee_dashboard'))  # Balik dashboard


if __name__ == '__main__':
    app.run(debug=True) 