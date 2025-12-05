# 🚀 QUICK START GUIDE
## Get Your Inventory Management System Running in 5 Minutes!

---

## ⚡ Super Fast Setup

### **Step 1: Setup Database** (2 minutes)

Open Terminal and run:

```bash
cd "/Users/vedvyas/Desktop/vs code/simple-inventory-management-system"
./setup_database.sh
```

**When prompted, enter your MySQL root password** (the one you set during MySQL installation).

This will:
- ✅ Create the `inventory_management` database
- ✅ Create 6 tables (suppliers, categories, products, inventory, transactions, users)
- ✅ Import 31 sample products
- ✅ Import 6 suppliers
- ✅ Import 58 transactions
- ✅ Create 7 stored procedures
- ✅ Verify everything is working

---

### **Step 2: Configure Database Password** (30 seconds)

Edit the `.env` file:

```bash
nano .env
```

Change line 5:
```
DB_PASSWORD=
```

To your MySQL root password:
```
DB_PASSWORD=your_mysql_password
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

---

### **Step 3: Start the Application** (1 minute)

```bash
./start.sh
```

This will:
- Activate Python virtual environment
- Install dependencies (if needed)
- Start the Flask server

You should see:
```
╔═══════════════════════════════════════════════════════════╗
║   Inventory Management System                              ║
║   Running on: http://0.0.0.0:5000                         ║
╚═══════════════════════════════════════════════════════════╝

 * Running on http://127.0.0.1:5000
```

---

### **Step 4: Open in Browser** (10 seconds)

1. Open your web browser
2. Go to: **http://localhost:5000**
3. Login with:
   - **Username:** `admin`
   - **Password:** `password123`

---

## 🎉 You're Done!

You should now see the **Dashboard** with:
- 📊 Summary cards showing inventory statistics
- 📈 Charts visualizing stock by category
- 📝 Recent transaction history

---

## 🔍 What's Included?

### **Pre-loaded Data:**

**31 Products** including:
- Dell Inspiron 15 Laptop (₹52,999)
- Samsung 55" 4K Smart TV (₹45,999)
- iPhone 14 (₹79,900)
- LG Washing Machine (₹32,990)
- Executive Office Chair (₹8,999)
- And 26 more...

**6 Suppliers:**
- Tech Distributors India (Mumbai)
- Global Electronics Supply Co (Bangalore)
- Furniture World Suppliers (Delhi)
- Office Essentials Mart (Pune)
- Premium Home Appliances (Chennai)
- Smart Gadgets International (Hyderabad)

**7 Categories:**
- Electronics
- Computers & Laptops
- Mobile Phones
- Home Appliances
- Furniture
- Stationery
- Networking

**58 Transactions:**
- Stock In, Stock Out, and Adjustments
- Complete audit trail with dates and users

**4 User Accounts:**
- admin / password123 (Full access)
- manager1 / password123 (Management access)
- staff1 / password123 (Basic access)
- staff2 / password123 (Basic access)

---

## 🎯 Quick Navigation Guide

After logging in, explore these sections:

### **1. Dashboard**
Click "Dashboard" in navigation
- View summary statistics
- See charts and graphs
- Check recent transactions

### **2. Products**
Click "Products"
- View all 31 products
- Click "Add Product" to create new
- Click pencil icon to edit
- Click trash icon to delete
- Use search box to filter

### **3. Inventory**
Click "Inventory"
- See current stock levels
- View stock values
- Check warehouse locations
- Identify low stock items (red/yellow badges)

### **4. Transactions**
Click "Transactions"
- View transaction history
- Filter by date, type, or product
- See complete audit trail

### **5. Stock In** (Receiving Products)
Go to Transactions → Click "Stock In" button
1. Select product
2. Enter quantity received
3. Enter PO number
4. Add remarks
5. Submit
→ Stock increases immediately!

### **6. Stock Out** (Selling Products)
Go to Transactions → Click "Stock Out" button
1. Select product
2. Enter quantity sold
3. Enter invoice number
4. Submit
→ Stock decreases with validation!

### **7. Suppliers**
Click "Manage" → "Suppliers"
- View all 6 suppliers
- Add new suppliers
- Edit supplier details
- View products per supplier

### **8. Categories**
Click "Manage" → "Categories"
- View all 7 categories
- Add new categories
- Edit descriptions
- See product counts

### **9. Reports**
Click "Reports"
- Stock Summary Report
- Low Stock Report
- Category-wise Analysis
- Supplier-wise Analysis
- Transaction Summary

---

## 💡 Try These Actions

### **Test Drive the System:**

1. **View a Product:**
   - Go to Products
   - Click on "Dell Inspiron 15 Laptop"
   - See details, current stock (18 units), price (₹52,999)

2. **Record a Sale:**
   - Go to Transactions
   - Click "Stock Out"
   - Select "Samsung 55" 4K Smart TV"
   - Enter quantity: 2
   - Reference: TEST-INV-001
   - Submit
   - Check inventory - stock decreased by 2!

3. **Receive New Stock:**
   - Go to Transactions
   - Click "Stock In"
   - Select "iPhone 14"
   - Enter quantity: 10
   - Reference: PO-TEST-2024
   - Submit
   - Stock increased by 10!

4. **View Transaction History:**
   - Go to Transactions
   - See your test transactions appear
   - Filter by product or date

5. **Check Low Stock:**
   - Go to Reports
   - Click "Low Stock Report"
   - See products below reorder level
   - Plan restocking

6. **Add a New Product:**
   - Go to Products
   - Click "Add Product"
   - Fill in details:
     - Name: Test Product
     - SKU: TEST-001
     - Category: Electronics
     - Supplier: Any supplier
     - Price: 999.00
     - Reorder Level: 5
   - Submit
   - New product appears in list!

---

## 🛠️ Troubleshooting

### **Can't connect to database?**
```bash
# Check MySQL is running
/usr/local/mysql-9.5.0-macos15-arm64/bin/mysql -u root -p

# If you can login, the password in .env is wrong
# Edit .env and update DB_PASSWORD
```

### **Port 5000 already in use?**
```bash
# Edit .env and change:
PORT=5001

# Then restart:
./start.sh
```

### **Page not loading?**
```bash
# Make sure Flask is running (you should see output in terminal)
# Check browser URL is: http://localhost:5000
# Try: http://127.0.0.1:5000
```

### **Login not working?**
- Username: `admin` (lowercase)
- Password: `password123` (no spaces)
- Make sure sample_data.sql was imported

---

## 📚 Next Steps

1. **Explore all features** - Click around, try everything!
2. **Read the docs** - Check `docs/` folder for detailed documentation
3. **Customize** - Add your own products, suppliers, categories
4. **Learn** - Study the code, understand how it works
5. **Extend** - Add new features as needed

---

## 🎓 For Your DBMS Project

This system demonstrates:
- ✅ Database normalization (3NF)
- ✅ ER diagrams and relationships
- ✅ SQL queries and JOINs
- ✅ Stored procedures
- ✅ Triggers and constraints
- ✅ Indexing strategies
- ✅ Transaction management
- ✅ Full-stack integration
- ✅ Security best practices

All documentation is in the `docs/` folder:
- `database_design.md` - Complete DB design
- `normalization.md` - 1NF → 2NF → 3NF process
- `api_documentation.md` - All API endpoints
- `project_report.md` - Academic report template

---

## 🚀 Commands Summary

```bash
# Setup database (one time)
./setup_database.sh

# Start application (every time)
./start.sh

# Or manually:
source venv/bin/activate
python run.py

# Stop application
# Press Ctrl+C in terminal
```

---

## 🎊 Enjoy Your System!

Your Inventory Management System is now ready to use!

**Login:** http://localhost:5000
**Username:** admin
**Password:** password123

Have fun exploring! 🎉
