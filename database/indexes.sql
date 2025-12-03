-- ============================================
-- Inventory Management System - Additional Indexes
-- ============================================
-- This file documents additional indexes for performance optimization
-- Indexes are already created in schema.sql, but this file explains the rationale
-- ============================================

USE inventory_management;

-- ============================================
-- INDEX JUSTIFICATION AND PERFORMANCE ANALYSIS
-- ============================================

-- 1. SUPPLIERS TABLE INDEXES
-- --------------------------------------------
-- INDEX: idx_company_name ON suppliers(company_name)
-- Justification: Frequently used in search operations when looking up suppliers
-- Use Case: "Find all suppliers with name containing 'ABC'"
-- Performance: Converts O(n) full table scan to O(log n) B-tree lookup

-- INDEX: idx_city ON suppliers(city)
-- Justification: Useful for location-based queries and supplier reports by region
-- Use Case: "List all suppliers in Mumbai"
-- Performance: Enables quick filtering without scanning entire table

-- 2. CATEGORIES TABLE INDEXES
-- --------------------------------------------
-- INDEX: idx_category_name ON categories(category_name)
-- Justification: Category lookup is common in product filtering
-- Use Case: "Show all products in 'Electronics' category"
-- Performance: Speeds up JOIN operations with products table

-- 3. PRODUCTS TABLE INDEXES
-- --------------------------------------------
-- INDEX: idx_product_name ON products(product_name)
-- Justification: Most frequent search operation - users search products by name
-- Use Case: "Search for products containing 'laptop'"
-- Performance: Critical for autocomplete and search functionality
-- Expected Improvement: 100x faster on 1000+ products

-- INDEX: idx_sku ON products(sku)
-- Justification: SKU is unique identifier used in barcode scanning and lookups
-- Use Case: "Find product with SKU 'ELEC-LAP-001'"
-- Performance: O(1) lookup due to UNIQUE constraint with B-tree index
-- Note: Already enforced by UNIQUE constraint but explicitly indexed for clarity

-- INDEX: idx_category_id ON products(category_id)
-- Justification: Foreign key used in JOIN operations and category-based filtering
-- Use Case: "Show all products in category_id = 5"
-- Performance: Speeds up JOIN with categories table
-- Expected Improvement: 50x faster on large datasets

-- INDEX: idx_supplier_id ON products(supplier_id)
-- Justification: Foreign key for supplier-wise product reports
-- Use Case: "List all products from supplier_id = 3"
-- Performance: Enables efficient JOIN with suppliers table

-- 4. INVENTORY TABLE INDEXES
-- --------------------------------------------
-- INDEX: idx_product_id ON inventory(product_id)
-- Justification: One-to-one relationship lookup
-- Use Case: "Get current stock for product_id = 10"
-- Performance: O(log n) lookup instead of O(n) scan

-- INDEX: idx_quantity ON inventory(quantity_in_stock)
-- Justification: Used for low-stock alerts and stock level filtering
-- Use Case: "Find all products with stock < 10"
-- Performance: Range queries are optimized with this index

-- 5. TRANSACTIONS TABLE INDEXES
-- --------------------------------------------
-- INDEX: idx_product_id ON transactions(product_id)
-- Justification: Transaction history queries are very frequent
-- Use Case: "Show all transactions for product_id = 15"
-- Performance: Critical for audit trails and history views
-- Expected Improvement: 100x faster for products with many transactions

-- INDEX: idx_transaction_date ON transactions(transaction_date)
-- Justification: Date-range queries for reports
-- Use Case: "Show all transactions between 2024-01-01 and 2024-12-31"
-- Performance: Enables efficient range scans for report generation
-- Expected Improvement: Essential for monthly/yearly reports

-- INDEX: idx_transaction_type ON transactions(transaction_type)
-- Justification: Filtering by transaction type (STOCK_IN, STOCK_OUT, ADJUSTMENT)
-- Use Case: "Show all STOCK_OUT transactions"
-- Performance: Quick filtering for specific transaction analysis

-- INDEX: idx_reference_number ON transactions(reference_number)
-- Justification: Lookup transactions by PO number, invoice number, etc.
-- Use Case: "Find transaction with reference number 'PO-2024-001'"
-- Performance: Fast lookup for cross-referencing with external documents

-- 6. USERS TABLE INDEXES
-- --------------------------------------------
-- INDEX: idx_username ON users(username)
-- Justification: Authentication requires username lookup on every login
-- Use Case: "Authenticate user with username 'admin'"
-- Performance: Critical for login performance - must be O(log n)
-- Note: UNIQUE constraint automatically creates index

-- INDEX: idx_email ON users(email)
-- Justification: Password reset and user lookup by email
-- Use Case: "Find user with email 'user@example.com'"
-- Performance: Fast email-based queries

-- INDEX: idx_role ON users(role)
-- Justification: Role-based filtering for user management
-- Use Case: "List all users with role = 'admin'"
-- Performance: Quick filtering for admin panels

-- ============================================
-- COMPOSITE INDEX RECOMMENDATIONS
-- ============================================
-- These can be added if specific query patterns emerge:

-- For product search with category filter:
-- CREATE INDEX idx_product_category_name ON products(category_id, product_name);

-- For transaction reports by product and date:
-- CREATE INDEX idx_transaction_product_date ON transactions(product_id, transaction_date);

-- For low stock products by category:
-- CREATE INDEX idx_inventory_quantity_product ON inventory(quantity_in_stock, product_id);

-- ============================================
-- INDEX MAINTENANCE NOTES
-- ============================================
-- 1. Indexes improve SELECT performance but slow down INSERT/UPDATE/DELETE
-- 2. For this inventory system, reads are more frequent than writes
-- 3. Regular ANALYZE TABLE should be run to update index statistics
-- 4. Monitor slow queries using MySQL slow query log
-- 5. Use EXPLAIN to verify indexes are being used effectively

-- Example: Check if index is used
-- EXPLAIN SELECT * FROM products WHERE product_name LIKE 'laptop%';

-- ============================================
-- PERFORMANCE TESTING QUERIES
-- ============================================

-- Test 1: Product search without index (disable index temporarily)
-- ALTER TABLE products DROP INDEX idx_product_name;
-- SELECT * FROM products WHERE product_name LIKE 'laptop%';
-- Expected: Full table scan

-- Test 2: Product search with index
-- ALTER TABLE products ADD INDEX idx_product_name(product_name);
-- SELECT * FROM products WHERE product_name LIKE 'laptop%';
-- Expected: Index range scan

-- Test 3: Transaction date range query
-- EXPLAIN SELECT * FROM transactions
-- WHERE transaction_date BETWEEN '2024-01-01' AND '2024-12-31';
-- Expected: Using idx_transaction_date

-- ============================================
