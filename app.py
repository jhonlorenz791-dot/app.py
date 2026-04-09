from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'Secret123' 

users_db = [
    ('admin', 'admin123', 'admin'),
    ('employee', 'employee123', 'employee')
]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        active_user = next((u for u in users_db if u[0] == username and u[1] == password), None)

        if active_user:
            session['username'] = active_user[0]
            session['role'] = active_user[2]

            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('employee_dashboard'))
            
        return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admindashboard.html')

@app.route('/employee')
def employee_dashboard():
    if 'username' not in session or session.get('role') != 'employee':
        return redirect(url_for("login"))
    return render_template('employeedashboard.html')

if __name__ == '__main__':
    app.run(debug=True)