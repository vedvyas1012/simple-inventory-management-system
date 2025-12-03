# Inventory Management System
## DBMS Course Project

A comprehensive Inventory Management System built with MySQL, Python Flask, and modern web technologies. This system provides complete inventory tracking, stock management, transaction logging, and reporting capabilities.

---

## 📋 Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Testing](#testing)
- [Contributors](#contributors)

---

## ✨ Features

### Core Functionality
- **Product Management**: Add, edit, delete, and search products
- **Inventory Tracking**: Real-time stock level monitoring
- **Stock Transactions**: Record stock in, stock out, and adjustments
- **Supplier Management**: Maintain supplier database
- **Category Management**: Organize products by categories
- **Low Stock Alerts**: Automatic notifications for low stock items
- **Transaction History**: Complete audit trail of all inventory movements
- **Reports & Analytics**: Comprehensive reports and dashboards

### Technical Features
- **3NF Database Design**: Normalized schema with referential integrity
- **RESTful API**: Complete REST API with JSON responses
- **Role-Based Access**: Admin, Manager, and Staff roles
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Stored Procedures**: Business logic encapsulated in database
- **Responsive UI**: Mobile-friendly Bootstrap 5 interface
- **Data Tables**: Advanced table features with search, sort, and pagination
- **Charts & Graphs**: Visual analytics using Chart.js

---

## 🛠 Technology Stack

### Backend
- **Python 3.x** - Programming language
- **Flask 3.0** - Web framework
- **MySQL 8.0** - Database management system
- **mysql-connector-python** - Database connector
- **bcrypt** - Password hashing
- **PyJWT** - JWT token authentication

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **JavaScript (ES6)** - Client-side scripting
- **Bootstrap 5** - UI framework
- **jQuery** - DOM manipulation and AJAX
- **DataTables** - Advanced table features
- **Chart.js** - Data visualization

### Database
- **MySQL 8.0** with InnoDB engine
- **Stored Procedures** for business logic
- **Triggers** for audit logging
- **Indexes** for performance optimization

---

## 📦 System Requirements

- **Python**: 3.8 or higher
- **MySQL**: 8.0 or higher
- **pip**: Python package manager
- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest version)
- **Operating System**: Windows, macOS, or Linux

### Minimum Hardware
- **RAM**: 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Processor**: Dual-core 2.0 GHz or higher

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/vedvyas1012/simple-inventory-management-system.git
cd simple-inventory-management-system
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄 Database Setup

### Step 1: Install MySQL

Download and install MySQL 8.0 from [official website](https://dev.mysql.com/downloads/mysql/)

### Step 2: Start MySQL Service

**On Windows:**
```bash
net start MySQL80
```

**On macOS:**
```bash
mysql.server start
```

**On Linux:**
```bash
sudo systemctl start mysql
```

### Step 3: Login to MySQL

```bash
mysql -u root -p
```
Enter your MySQL root password when prompted.

### Step 4: Create Database and Import Schema

```sql
-- Inside MySQL console
source /path/to/database/schema.sql
```

Or from command line:
```bash
mysql -u root -p < database/schema.sql
```

### Step 5: Import Sample Data (Optional)

```bash
mysql -u root -p inventory_management < database/sample_data.sql
```

### Step 6: Create Stored Procedures

```bash
mysql -u root -p inventory_management < database/stored_procedures.sql
```

### Verify Database Setup

```sql
USE inventory_management;
SHOW TABLES;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM suppliers;
```

You should see 6 tables and sample data if you imported it.

---

## ⚙️ Configuration

### Step 1: Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### Step 2: Configure Database Connection

Edit `.env` file with your database credentials:

```ini
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=inventory_management

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=change-this-to-random-secret-key
DEBUG=True
PORT=5000
HOST=0.0.0.0

# JWT Settings
JWT_SECRET_KEY=change-this-to-random-jwt-key
JWT_EXPIRATION_HOURS=24
```

### Step 3: Generate Secret Keys

Generate secure random keys for production:

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

Use the output for `SECRET_KEY` and `JWT_SECRET_KEY`.

---

## ▶️ Running the Application

### Development Mode

```bash
python run.py
```

The application will start on `http://localhost:5000`

### Production Mode

```bash
export FLASK_ENV=production
export DEBUG=False
python run.py
```

Or use a production WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

### Default Login Credentials

| Username | Password    | Role    |
|----------|-------------|---------|
| admin    | password123 | Admin   |
| manager1 | password123 | Manager |
| staff1   | password123 | Staff   |

**⚠️ IMPORTANT:** Change default passwords in production!

---

## 📁 Project Structure

```
inventory_management/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration settings
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── database.py          # Database utility
│   │   ├── product.py           # Product model
│   │   ├── supplier.py          # Supplier model
│   │   ├── category.py          # Category model
│   │   ├── inventory.py         # Inventory model
│   │   ├── transaction.py       # Transaction model
│   │   └── user.py              # User model
│   ├── routes/                  # API routes
│   │   ├── __init__.py
│   │   ├── product_routes.py
│   │   ├── supplier_routes.py
│   │   ├── category_routes.py
│   │   ├── inventory_routes.py
│   │   ├── transaction_routes.py
│   │   ├── report_routes.py
│   │   └── auth_routes.py
│   ├── static/                  # Static files
│   │   ├── css/
│   │   │   └── style.css        # Custom styles
│   │   └── js/
│   │       └── common.js        # Common JavaScript
│   └── templates/               # HTML templates
│       ├── base.html            # Base template
│       ├── login.html           # Login page
│       ├── dashboard.html       # Dashboard
│       ├── products/
│       │   └── list.html        # Products listing
│       ├── suppliers/
│       │   └── list.html
│       ├── categories/
│       │   └── list.html
│       ├── inventory/
│       │   └── list.html
│       ├── transactions/
│       │   └── list.html
│       └── reports/
│           └── dashboard.html
├── database/                    # Database scripts
│   ├── schema.sql              # Database schema (3NF)
│   ├── indexes.sql             # Index documentation
│   ├── stored_procedures.sql   # Stored procedures
│   └── sample_data.sql         # Sample data
├── docs/                       # Documentation
│   ├── database_design.md      # Database design with ER diagram
│   ├── normalization.md        # Normalization process (1NF→3NF)
│   ├── api_documentation.md    # API endpoints
│   └── project_report.md       # Project report template
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
└── README.md                   # This file
```

---

## 📖 API Documentation

Complete API documentation is available in [`docs/api_documentation.md`](docs/api_documentation.md)

### Quick API Reference

**Base URL:** `http://localhost:5000/api`

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/verify` - Verify JWT token

#### Products
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get product by ID
- `POST /api/products` - Create product
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product
- `GET /api/products/low-stock` - Get low stock products

#### Transactions
- `GET /api/transactions` - Get all transactions
- `POST /api/transactions/stock-in` - Record stock in
- `POST /api/transactions/stock-out` - Record stock out
- `POST /api/transactions/adjust` - Adjust stock

#### Reports
- `GET /api/reports/stock-summary` - Stock summary
- `GET /api/reports/dashboard-stats` - Dashboard statistics

See full documentation for all endpoints.

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)
*Real-time inventory overview with charts and analytics*

### Product Management
![Products](docs/screenshots/products.png)
*Complete product listing with search and filters*

### Stock Transactions
![Transactions](docs/screenshots/transactions.png)
*Transaction history with filtering options*

---

## 🧪 Testing

### Manual Testing

1. **Database Connection Test:**
```bash
python -c "from app.models.database import Database; print('✓ Connected' if Database.test_connection() else '✗ Failed')"
```

2. **Run Application:**
```bash
python run.py
```

3. **Test API Endpoints:**
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'

# Get Products
curl http://localhost:5000/api/products
```

### Test Stored Procedures

```sql
-- Test stock in
CALL sp_record_stock_in(1, 50, 'PO-TEST-001', 'Test purchase', 'admin');

-- Test low stock
CALL sp_get_low_stock_products(NULL);

-- Test stock valuation
CALL sp_get_stock_valuation();
```

---

## 📚 Additional Documentation

- **Database Design**: [`docs/database_design.md`](docs/database_design.md)
  - Complete ER diagram
  - Table descriptions
  - Relationships and constraints

- **Normalization**: [`docs/normalization.md`](docs/normalization.md)
  - Step-by-step normalization process
  - 1NF → 2NF → 3NF transformations

- **API Documentation**: [`docs/api_documentation.md`](docs/api_documentation.md)
  - All endpoints with examples
  - Request/response formats
  - Error handling

---

## 🔒 Security Considerations

- **Password Hashing**: Bcrypt with salt for secure password storage
- **SQL Injection Prevention**: Parameterized queries throughout
- **JWT Authentication**: Token-based authentication with expiration
- **Input Validation**: Server-side validation for all inputs
- **Role-Based Access**: Three-tier permission system
- **CORS Protection**: Configured CORS headers
- **Environment Variables**: Sensitive data in `.env` file

---

## 🐛 Troubleshooting

### Database Connection Error

**Error:** `Error 2003: Can't connect to MySQL server`

**Solution:**
1. Verify MySQL is running: `mysql --version`
2. Check credentials in `.env` file
3. Ensure database exists: `SHOW DATABASES;`

### Port Already in Use

**Error:** `Address already in use: Port 5000`

**Solution:**
```bash
# Change port in .env file
PORT=5001

# Or kill process using port 5000
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows
```

### Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 🤝 Contributors

- **Vedvyas** - Developer
- **Project Guide** - DBMS Course Instructor

---

## 📄 License

This project is created for educational purposes as part of DBMS course project.

---

## 🙏 Acknowledgments

- Bootstrap team for the UI framework
- Flask community for excellent documentation
- MySQL documentation and community
- Chart.js for visualization library

---

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Contact: vedvyas1012@github.com

---

**Made with ❤️ for DBMS Course Project**
