# 📌 Leave Management System (LMS) – FastAPI  

A lightweight **Leave Management System** built with **FastAPI + SQLite + JWT Authentication**, designed for managing employee leave requests with HR/Admin oversight.  

---

## 🚀 Features  
- Employee management (Add, View, List employees)  
- Leave management (Apply, Approve/Reject, Withdraw, Balance check)  
- Role-based access control (HR/Admin vs Employees)  
- JWT Authentication for HR/Admin  
- Health check endpoint  
- Admin DB dump to view all employees + leave history  

---

## 🏗️ Tech Stack  
- **Backend**: FastAPI (Python 3.10+)  
- **Database**: SQLite (default, can be swapped to PostgreSQL/MySQL)  
- **Auth**: JWT (with `.env` secrets)  
- **ORM**: SQLAlchemy  
- **Password Hashing**: Passlib (bcrypt)  

---

## ⚙️ Setup Steps  

### 1️⃣ Clone Repository  
```bash
git clone https://github.com/Templar121/Leave-Management.git
cd leave-management-system
```


### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables (.env)
```bash
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
HR_USERNAME=admin
HR_PASSWORD=secret123
ADMIN_USERNAME=superadmin
ADMIN_PASSWORD=supersecret
```

### 5️⃣ Run the API
```bash
uvicorn app.main:app --reload
```

API will be available at: http://127.0.0.1:8000

### 6️⃣ API Docs

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 📌 API Endpoints
### 🔑 Auth

 - POST /auth/login → Login as HR/Admin (returns JWT)

---

### 👨‍💼 Employee

 - POST /employees/ → Add employee (HR only)

 - GET /employees/{id} → Get employee by ID

 - GET /employees/ → List all employees (HR only)

---

### 🌴 Leave

 - POST /leaves/{emp_id} → Apply leave (Employee)

 - PUT /leaves/{leave_id}/status?status=approved/rejected → Approve/Reject (HR only)

 - PUT /leaves/{leave_id}/withdraw → Withdraw leave (Employee)

 - GET /leaves/balance/{emp_id} → View leave balance

 - GET /leaves/employee/{emp_id} → View all leave requests for an employee

---

### 🛠 Admin

 - GET /admin/db-dump → View all employees + leave requests (Admin only)

---

### ❤️ Health

 - GET /health/ → Service health check

 ---

### 📸 Example API Flow

 - HR logs in → gets JWT token.

 - HR adds employees.

 - Employee applies for leave.

 - HR approves/rejects leave.

 - Employee withdraws leave if needed.

 - Admin fetches DB dump for auditing.

---

### ⚡ Edge Cases Handled

 - Overlapping leave requests blocked.

 - Cannot approve expired leaves.

 - Cannot withdraw already approved/rejected leaves.

 - Employee leave balance auto-updated.

- Unauthorized access blocked with 401 Unauthorized.

---

### 📝 Assumptions

 - Each employee has 20 leave days/year (configurable).

 - HR/Admin users are seeded via .env (no signup flow).

 - Employees do not need login for this version (future improvement).

---

### 🚀 Potential Improvements

 - Employee authentication (separate login system).

 - Email/SMS notifications for leave status changes.

 - Role-based access control (Admin > HR > Employee).

 - Bulk approval/rejection endpoints for HR.

 - Dashboard (React/Angular frontend).

 - Export reports in CSV/Excel for HR/Admin.

---

### 📊 HLD Diagram (Class Diagram)

                        +---------------------+
                        |      HRUser         |
                        |---------------------|
                        | - id: int           |
                        | - username: str     |
                        | - password_hash: str|
                        +---------------------+

                        +---------------------+
                        |     Employee        |
                        |---------------------|
                        | - id: int           |
                        | - name: str         |
                        | - email: str        |
                        | - department: str   |
                        | - joining_date: date|
                        | - leave_balance: int|
                        +---------------------+
                                 |
                                 | 1..* (has many)
                                 v
                        +---------------------+
                        |       Leave         |
                        |---------------------|
                        | - id: int           |
                        | - employee_id: int  |
                        | - start_date: date  |
                        | - end_date: date    |
                        | - status: enum      |
                        +---------------------+

---

### 📌 Component Interaction

[Client (Postman/Web)] ---> [FastAPI Backend] ---> [Database]

FastAPI Modules:
- Auth Controller
  • POST /auth/login
- Employee Controller
  • POST /employees/
  • GET /employees/{id}
  • GET /employees/
- Leave Controller
  • POST /leaves/{emp_id}
  • PUT /leaves/{leave_id}/status
  • PUT /leaves/{leave_id}/withdraw
  • GET /leaves/balance/{emp_id}
- Admin Controller
  • GET /admin/db-dump

---