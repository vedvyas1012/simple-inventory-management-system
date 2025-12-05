#!/bin/bash

# Inventory Management System - Database Setup Script
# This script will create the database and import all data

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Inventory Management System - Database Setup            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

MYSQL_PATH="/usr/local/mysql-9.5.0-macos15-arm64/bin/mysql"

echo "This script will:"
echo "  1. Create the inventory_management database"
echo "  2. Import the schema (6 tables)"
echo "  3. Import sample data (31 products, 6 suppliers, 58 transactions)"
echo "  4. Create stored procedures"
echo ""
echo "Please enter your MySQL root password when prompted."
echo ""

# Run schema
echo "→ Creating database and tables..."
$MYSQL_PATH -u root -p < database/schema.sql

if [ $? -eq 0 ]; then
    echo "✓ Database schema created successfully"
else
    echo "✗ Error creating database schema"
    exit 1
fi

# Import sample data
echo ""
echo "→ Importing sample data..."
$MYSQL_PATH -u root -p inventory_management < database/sample_data.sql

if [ $? -eq 0 ]; then
    echo "✓ Sample data imported successfully"
else
    echo "✗ Error importing sample data"
    exit 1
fi

# Create stored procedures
echo ""
echo "→ Creating stored procedures..."
$MYSQL_PATH -u root -p inventory_management < database/stored_procedures.sql

if [ $? -eq 0 ]; then
    echo "✓ Stored procedures created successfully"
else
    echo "✗ Error creating stored procedures"
    exit 1
fi

# Verify setup
echo ""
echo "→ Verifying setup..."
$MYSQL_PATH -u root -p inventory_management -e "
SELECT
    'Tables' as Type,
    COUNT(*) as Count
FROM information_schema.tables
WHERE table_schema = 'inventory_management'
UNION ALL
SELECT
    'Products' as Type,
    COUNT(*) as Count
FROM products
UNION ALL
SELECT
    'Suppliers' as Type,
    COUNT(*) as Count
FROM suppliers
UNION ALL
SELECT
    'Transactions' as Type,
    COUNT(*) as Count
FROM transactions;
"

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║   ✓ Database Setup Complete!                              ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "You can now run the application:"
    echo "  1. source venv/bin/activate"
    echo "  2. python run.py"
    echo "  3. Open http://localhost:5000"
    echo "  4. Login with: admin / password123"
    echo ""
else
    echo "✗ Error verifying setup"
    exit 1
fi
