# 🚀 COMPLETE SETUP INSTRUCTIONS

## You're Almost There! Just 3 Steps Left:

---

## **STEP 1: Set MySQL Password & Create Database**

Run this command:

```bash
./setup_mysql.sh
```

**What happens:**
- Sets MySQL root password to `inventory123`
- Creates `inventory_management` database
- Imports schema (6 tables)
- Loads 31 sample products
- Loads 6 suppliers
- Loads 58 transactions
- Creates 7 stored procedures

**When prompted for password:**
- First time: Press `Enter` (empty password)
- Second time: Type `inventory123` and press `Enter`

---

## **STEP 2: Verify Configuration**

Your `.env` file is already configured with:
- ✅ MySQL password: `inventory123`
- ✅ Secure SECRET_KEY
- ✅ Secure JWT_SECRET_KEY
- ✅ Port: 5001
- ✅ Database: inventory_management

**All set!** No changes needed.

---

## **STEP 3: Start the Application**

```bash
./start.sh
```

You should see:
```
╔═══════════════════════════════════════════════════════════╗
║   Inventory Management System                              ║
║   Running on: http://0.0.0.0:5001                         ║
╚═══════════════════════════════════════════════════════════╝

✓ Database connection successful
 * Running on http://127.0.0.1:5001
```

---

## **STEP 4: Access the System**

1. **Open browser** → `http://localhost:5001`
2. **Login with:**
   - Username: `admin`
   - Password: `password123`
3. **Explore!** 🎉

---

## 🎯 **Quick Test After Login**

Try these to verify everything works:

### **1. View Dashboard**
- Should see 31 total products
- Charts showing stock distribution
- Recent transactions

### **2. Browse Products**
Click "Products" → You'll see:
- Dell Inspiron 15 Laptop - ₹52,999 (18 in stock)
- Samsung 55" 4K Smart TV - ₹45,999 (12 in stock)
- iPhone 14 - ₹79,900 (15 in stock)
- And 28 more products...

### **3. Record a Sale (Test Transaction)**
1. Click "Transactions" in menu
2. Click "Stock Out" button
3. Select "Samsung 55" 4K Smart TV"
4. Quantity: `2`
5. Reference: `TEST-001`
6. Click Submit
7. ✅ Success! Stock decreases from 12 to 10

### **4. Check Transaction History**
Click "Transactions" → You'll see your test sale logged with:
- Date/Time
- Product name
- Quantity: 2
- Type: STOCK_OUT
- Your username

---

## 🐛 **Troubleshooting**

### **Problem: MySQL password error**
```
Error 1045 (28000): Access denied for user 'root'@'localhost'
```

**Solution:**
```bash
# Reset MySQL password
/usr/local/mysql-9.5.0-macos15-arm64/bin/mysql -u root -p
# Enter your current password, then:
ALTER USER 'root'@'localhost' IDENTIFIED BY 'inventory123';
FLUSH PRIVILEGES;
EXIT;

# Update .env file
nano .env
# Change DB_PASSWORD=inventory123
```

---

### **Problem: Database already exists**
```
ERROR 1007 (HY000): Can't create database 'inventory_management'; database exists
```

**Solution:** The database is already created! Just run `./start.sh`

Or to recreate from scratch:
```bash
/usr/local/mysql-9.5.0-macos15-arm64/bin/mysql -u root -p
DROP DATABASE inventory_management;
EXIT;
./setup_mysql.sh
```

---

### **Problem: Port 5001 already in use**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Or change port in .env:
nano .env
# Change: PORT=5002
```

---

### **Problem: Can't connect to browser**

**Try these URLs:**
- http://localhost:5001
- http://127.0.0.1:5001
- http://10.31.91.240:5001 (your local network IP)

---

## 📋 **What's Included**

### **Pre-loaded Data:**

**31 Products** across 7 categories:
- 📱 **Electronics**: Samsung TV, Sony Headphones, JBL Speaker, Canon Camera
- 💻 **Computers**: Dell Laptop, HP Desktop, Lenovo ThinkPad, MacBook Air, Logitech Keyboard, HP Printer
- 📱 **Mobile Phones**: Samsung Galaxy S23, iPhone 14, OnePlus 11R, Xiaomi Redmi, Realme 10 Pro
- 🏠 **Home Appliances**: LG Washing Machine, Samsung Refrigerator, Philips Air Fryer, Bajaj Mixer
- 🪑 **Furniture**: Office Chair, Desk, Meeting Table, Filing Cabinet
- 📝 **Stationery**: Paper, Pens, Stapler, Markers
- 🌐 **Networking**: TP-Link Router, D-Link Switch, Cat6 Cable

**6 Suppliers:**
- Tech Distributors India (Mumbai)
- Global Electronics Supply Co (Bangalore)
- Furniture World Suppliers (Delhi)
- Office Essentials Mart (Pune)
- Premium Home Appliances (Chennai)
- Smart Gadgets International (Hyderabad)

**4 User Accounts:**
- `admin` / `password123` - Full system access
- `manager1` / `password123` - Management access
- `staff1` / `password123` - Basic operations
- `staff2` / `password123` - Basic operations

**58 Transaction Records:**
- Stock In (purchases from suppliers)
- Stock Out (sales to customers)
- Adjustments (inventory corrections)
- Complete audit trail from Jan-Nov 2024

---

## 🎓 **Features to Explore**

### **Navigation Menu:**
1. **Dashboard** - Overview, charts, recent activity
2. **Products** - CRUD operations, search, filter
3. **Inventory** - Stock levels, warehouse locations
4. **Transactions** - Record sales, purchases, adjustments
5. **Manage** → **Suppliers** - Vendor management
6. **Manage** → **Categories** - Product categories
7. **Reports** - Analytics and summaries

### **Key Operations:**

**Stock In (Receiving):**
- Records new inventory from suppliers
- Updates stock levels
- Creates audit trail
- Links to PO numbers

**Stock Out (Sales):**
- Validates sufficient stock
- Decreases inventory
- Records sale details
- Links to invoice numbers

**Stock Adjustment:**
- Physical count corrections
- Damaged goods
- Returns processing
- Audit trail for all changes

**Reports:**
- Stock Summary (total value, units)
- Low Stock Alert (items to reorder)
- Category-wise Analysis
- Supplier-wise Analysis
- Transaction Summary by date range

---

## 🔒 **Security Notes**

Your `.env` file now has:
- ✅ Strong SECRET_KEY (64 characters)
- ✅ Strong JWT_SECRET_KEY (64 characters)
- ✅ Secure MySQL password

**Important for Demo:**
- This is configured for local development
- Default passwords are for demo only
- Change passwords before any production use

---

## 📚 **Documentation**

All project documentation is in the `docs/` folder:

- **database_design.md** - ER diagram, schema, relationships
- **normalization.md** - 1NF → 2NF → 3NF process explained
- **api_documentation.md** - All 40+ REST API endpoints
- **project_report.md** - Academic project report template

---

## ✅ **Checklist**

- [ ] Run `./setup_mysql.sh` (sets password, creates database)
- [ ] Verify `.env` has `DB_PASSWORD=inventory123`
- [ ] Run `./start.sh` (starts application)
- [ ] Open `http://localhost:5001` in browser
- [ ] Login with `admin` / `password123`
- [ ] Test creating a transaction
- [ ] Browse all features

---

## 🎉 **You're Ready!**

Your complete inventory management system is configured and ready to use.

**Next:** Run `./setup_mysql.sh` to create the database!

---

## 💡 **Quick Commands Reference**

```bash
# Setup database (first time only)
./setup_mysql.sh

# Start application (every time)
./start.sh

# Stop application
# Press Ctrl+C in terminal

# Check MySQL connection
/usr/local/mysql-9.5.0-macos15-arm64/bin/mysql -u root -p
# Password: inventory123

# View database
USE inventory_management;
SHOW TABLES;
SELECT COUNT(*) FROM products;
```

---

**Having issues? The application runs on port 5001 now (changed from 5000 to avoid conflicts).**

**All set? Run: `./setup_mysql.sh`** 🚀
