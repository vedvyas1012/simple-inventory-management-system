-- ============================================
-- Inventory Management System - Database Schema
-- ============================================
-- This schema is designed following 3NF (Third Normal Form)
-- All tables have proper constraints, foreign keys, and indexes
-- ============================================

-- Drop existing database if exists and create new
DROP DATABASE IF EXISTS inventory_management;
CREATE DATABASE inventory_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE inventory_management;

-- ============================================
-- TABLE: suppliers
-- Purpose: Store supplier/vendor information
-- Normalization: 3NF - All non-key attributes depend only on primary key
-- ============================================
CREATE TABLE suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_company_name (company_name),
    INDEX idx_city (city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: categories
-- Purpose: Store product categories for classification
-- Normalization: 3NF - Simple entity with no transitive dependencies
-- ============================================
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    INDEX idx_category_name (category_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: products
-- Purpose: Store product master data
-- Normalization: 3NF - Category and supplier are referenced via foreign keys
-- preventing data redundancy and ensuring referential integrity
-- ============================================
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    sku VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    category_id INT NOT NULL,
    supplier_id INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    reorder_level INT NOT NULL DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT chk_unit_price CHECK (unit_price >= 0),
    CONSTRAINT chk_reorder_level CHECK (reorder_level >= 0),

    -- Foreign Keys with cascading actions
    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_products_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    -- Indexes for performance optimization
    INDEX idx_product_name (product_name),
    INDEX idx_sku (sku),
    INDEX idx_category_id (category_id),
    INDEX idx_supplier_id (supplier_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: inventory
-- Purpose: Track current stock levels for each product
-- Normalization: 3NF - One-to-one relationship with products
-- Each product has exactly one inventory record
-- ============================================
CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL UNIQUE,
    quantity_in_stock INT NOT NULL DEFAULT 0,
    warehouse_location VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT chk_quantity_in_stock CHECK (quantity_in_stock >= 0),

    -- Foreign Key
    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Index
    INDEX idx_product_id (product_id),
    INDEX idx_quantity (quantity_in_stock)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: transactions
-- Purpose: Record all inventory movements (stock in, stock out, adjustments)
-- Normalization: 3NF - Transaction log with product reference
-- Maintains audit trail of all inventory changes
-- ============================================
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    transaction_type ENUM('STOCK_IN', 'STOCK_OUT', 'ADJUSTMENT') NOT NULL,
    quantity INT NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reference_number VARCHAR(50),
    remarks TEXT,
    created_by VARCHAR(50) NOT NULL,

    -- Constraints
    CONSTRAINT chk_quantity CHECK (quantity > 0),

    -- Foreign Key
    CONSTRAINT fk_transactions_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    -- Indexes for performance (transaction queries are frequent)
    INDEX idx_product_id (product_id),
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_reference_number (reference_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLE: users
-- Purpose: Store user authentication and authorization data
-- Normalization: 3NF - Simple entity for user management
-- ============================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('admin', 'manager', 'staff') NOT NULL DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,

    -- Indexes
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- NORMALIZATION DOCUMENTATION
-- ============================================
--
-- 1NF (First Normal Form):
-- - All tables have atomic values in each column
-- - Each column contains values of a single type
-- - Each column has a unique name
-- - No repeating groups or arrays
--
-- 2NF (Second Normal Form):
-- - Satisfies 1NF
-- - All non-key attributes are fully functionally dependent on the primary key
-- - Example: In products table, product_name, sku depend on product_id (not partial dependency)
--
-- 3NF (Third Normal Form):
-- - Satisfies 2NF
-- - No transitive dependencies (no non-key attribute depends on another non-key attribute)
-- - Example: Instead of storing supplier_name in products table, we reference supplier_id
--   This eliminates transitive dependency: product_id -> supplier_id -> supplier_name
--   Now: product_id -> supplier_id (direct dependency)
--        supplier_id -> supplier_name (in suppliers table)
-- ============================================
