#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   MySQL Setup for Inventory Management System             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

MYSQL_PATH="/usr/local/mysql-9.5.0-macos15-arm64/bin/mysql"

echo "This script will:"
echo "  1. Try to login to MySQL with empty password"
echo "  2. Set root password to 'inventory123'"
echo "  3. Create the database"
echo ""

# Try to set password (if current password is empty)
echo "→ Attempting to set MySQL root password..."
$MYSQL_PATH -u root << EOF 2>/dev/null
ALTER USER 'root'@'localhost' IDENTIFIED BY 'inventory123';
FLUSH PRIVILEGES;
EOF

if [ $? -eq 0 ]; then
    echo "✓ Password set successfully"
else
    echo "ℹ️  Password might already be set, trying with current password..."
fi

# Now try to create database with the password
echo ""
echo "→ Creating database..."
echo "Please enter MySQL password (should be: inventory123)"

$MYSQL_PATH -u root -p << EOF
DROP DATABASE IF EXISTS inventory_management;
CREATE DATABASE inventory_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE inventory_management;
\. database/schema.sql
\. database/sample_data.sql
\. database/stored_procedures.sql

-- Verify
SELECT 'Database created!' as Status;
SELECT COUNT(*) as Products FROM products;
SELECT COUNT(*) as Suppliers FROM suppliers;
SELECT COUNT(*) as Transactions FROM transactions;
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║   ✓ MySQL Setup Complete!                                 ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "Your MySQL credentials:"
    echo "  Username: root"
    echo "  Password: inventory123"
    echo ""
    echo "Database 'inventory_management' created with sample data!"
    echo ""
    echo "Now you can start the application:"
    echo "  ./start.sh"
    echo ""
else
    echo "✗ Error setting up database"
    exit 1
fi
