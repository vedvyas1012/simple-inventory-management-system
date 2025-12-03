-- ============================================
-- Inventory Management System - Sample Data
-- ============================================
-- This file contains realistic sample data for testing
-- ============================================

USE inventory_management;

-- ============================================
-- INSERT USERS (Password: 'password123' hashed)
-- ============================================
INSERT INTO users (username, password_hash, full_name, email, role, is_active) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lWYPvYt5Zziq', 'Admin User', 'admin@inventory.com', 'admin', TRUE),
('manager1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lWYPvYt5Zziq', 'Rajesh Kumar', 'rajesh.kumar@inventory.com', 'manager', TRUE),
('staff1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lWYPvYt5Zziq', 'Priya Sharma', 'priya.sharma@inventory.com', 'staff', TRUE),
('staff2', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lWYPvYt5Zziq', 'Amit Patel', 'amit.patel@inventory.com', 'staff', TRUE);

-- ============================================
-- INSERT SUPPLIERS
-- ============================================
INSERT INTO suppliers (company_name, contact_person, phone, email, address, city, state, postal_code) VALUES
('Tech Distributors India Pvt Ltd', 'Suresh Menon', '022-28374650', 'suresh@techdist.com', '12, Andheri Industrial Estate', 'Mumbai', 'Maharashtra', '400053'),
('Global Electronics Supply Co', 'Meera Reddy', '080-45632189', 'meera@globalelec.com', '45, Electronic City Phase 1', 'Bangalore', 'Karnataka', '560100'),
('Furniture World Suppliers', 'Vikram Singh', '011-26547890', 'vikram@furnitureworld.com', '78, Okhla Industrial Area', 'New Delhi', 'Delhi', '110020'),
('Office Essentials Mart', 'Anjali Desai', '020-24567891', 'anjali@officemart.com', '23, Pune IT Park', 'Pune', 'Maharashtra', '411014'),
('Premium Home Appliances Ltd', 'Karthik Iyer', '044-28965432', 'karthik@premiumappl.com', '56, Guindy Industrial Estate', 'Chennai', 'Tamil Nadu', '600032'),
('Smart Gadgets International', 'Neha Gupta', '040-23456789', 'neha@smartgadgets.com', '89, Hi-Tech City', 'Hyderabad', 'Telangana', '500081');

-- ============================================
-- INSERT CATEGORIES
-- ============================================
INSERT INTO categories (category_name, description) VALUES
('Electronics', 'Electronic devices, gadgets, and accessories'),
('Computers & Laptops', 'Desktop computers, laptops, and related hardware'),
('Mobile Phones', 'Smartphones, feature phones, and accessories'),
('Home Appliances', 'Kitchen and household appliances'),
('Furniture', 'Office and home furniture'),
('Stationery', 'Office supplies and stationery items'),
('Networking', 'Routers, switches, cables, and networking equipment');

-- ============================================
-- INSERT PRODUCTS
-- ============================================
INSERT INTO products (product_name, sku, description, category_id, supplier_id, unit_price, reorder_level) VALUES
-- Electronics
('Samsung 55" 4K Smart TV', 'ELEC-TV-001', '55-inch 4K UHD Smart LED TV with HDR', 1, 2, 45999.00, 5),
('LG 43" Full HD TV', 'ELEC-TV-002', '43-inch Full HD LED TV with webOS', 1, 2, 28999.00, 8),
('Sony Wireless Headphones', 'ELEC-AUD-001', 'WH-1000XM4 Noise Cancelling Headphones', 1, 2, 24990.00, 10),
('JBL Bluetooth Speaker', 'ELEC-AUD-002', 'Portable Bluetooth Speaker with 10hr battery', 1, 2, 3499.00, 15),
('Canon DSLR Camera', 'ELEC-CAM-001', 'EOS 1500D 24.1MP DSLR with 18-55mm lens', 1, 2, 35999.00, 5),

-- Computers & Laptops
('Dell Inspiron 15 Laptop', 'COMP-LAP-001', 'Intel i5, 8GB RAM, 512GB SSD, Windows 11', 2, 1, 52999.00, 10),
('HP Pavilion Desktop', 'COMP-DES-001', 'Intel i7, 16GB RAM, 1TB HDD, Windows 11', 2, 1, 48999.00, 8),
('Lenovo ThinkPad E14', 'COMP-LAP-002', 'Intel i5, 8GB RAM, 256GB SSD, 14-inch', 2, 1, 54999.00, 10),
('Apple MacBook Air M1', 'COMP-LAP-003', 'M1 Chip, 8GB RAM, 256GB SSD, 13.3-inch', 2, 1, 92990.00, 5),
('Logitech Wireless Keyboard', 'COMP-ACC-001', 'K380 Multi-device Bluetooth Keyboard', 2, 4, 2499.00, 20),
('HP LaserJet Printer', 'COMP-PRT-001', 'LaserJet Pro M126nw Multifunction Printer', 2, 1, 14999.00, 10),

-- Mobile Phones
('Samsung Galaxy S23', 'MOB-SAM-001', '8GB RAM, 128GB Storage, 5G', 3, 6, 74999.00, 15),
('iPhone 14', 'MOB-APP-001', '128GB, 6.1-inch, 5G', 3, 6, 79900.00, 10),
('OnePlus 11R', 'MOB-ONE-001', '8GB RAM, 128GB Storage, 5G', 3, 6, 39999.00, 20),
('Xiaomi Redmi Note 12', 'MOB-XIA-001', '6GB RAM, 128GB Storage, 4G', 3, 6, 15999.00, 25),
('Realme 10 Pro', 'MOB-REA-001', '8GB RAM, 128GB Storage, 5G', 3, 6, 21999.00, 20),

-- Home Appliances
('LG Front Load Washing Machine', 'HOME-WAS-001', '7kg, 1200 RPM, Inverter Direct Drive', 4, 5, 32990.00, 8),
('Samsung Refrigerator', 'HOME-FRG-001', '253L, 3 Star, Frost Free Double Door', 4, 5, 24990.00, 10),
('Philips Air Fryer', 'HOME-KIT-001', '4.1L Digital Air Fryer with Rapid Air Technology', 4, 5, 9995.00, 15),
('Bajaj Mixer Grinder', 'HOME-KIT-002', '750W Mixer Grinder with 3 Jars', 4, 5, 3499.00, 20),

-- Furniture
('Executive Office Chair', 'FURN-CHA-001', 'Ergonomic High Back Chair with Lumbar Support', 5, 3, 8999.00, 15),
('Office Desk 4ft', 'FURN-DES-001', '4ft x 2ft Engineered Wood Office Table', 5, 3, 5999.00, 12),
('Meeting Table 6ft', 'FURN-TAB-001', '6ft Conference Table with Seating for 6', 5, 3, 18999.00, 8),
('Filing Cabinet 4 Drawer', 'FURN-CAB-001', 'Steel Filing Cabinet with Lock', 5, 3, 7499.00, 10),

-- Stationery
('A4 Copier Paper (Ream)', 'STAT-PAP-001', '500 Sheets, 75 GSM, JK Copier', 6, 4, 299.00, 50),
('Blue Ballpoint Pens (Box)', 'STAT-PEN-001', 'Cello Butterflow Pens - 50 pcs box', 6, 4, 250.00, 40),
('Stapler Heavy Duty', 'STAT-STA-001', 'Kangaro Heavy Duty Stapler', 6, 4, 399.00, 25),
('Whiteboard Markers Set', 'STAT-MAR-001', 'Set of 4 Colors - Camlin', 6, 4, 180.00, 30),

-- Networking
('TP-Link WiFi Router', 'NET-ROU-001', 'AC1200 Dual Band Wireless Router', 7, 1, 1899.00, 20),
('D-Link 8 Port Switch', 'NET-SWI-001', 'Unmanaged Desktop Switch', 7, 1, 1299.00, 15),
('Cat6 Ethernet Cable 10m', 'NET-CAB-001', 'High Speed LAN Cable', 7, 1, 299.00, 40);

-- ============================================
-- INSERT INVENTORY
-- ============================================
INSERT INTO inventory (product_id, quantity_in_stock, warehouse_location) VALUES
-- Electronics
(1, 12, 'A-01'), (2, 15, 'A-02'), (3, 25, 'A-03'), (4, 30, 'A-04'), (5, 8, 'A-05'),
-- Computers & Laptops
(6, 18, 'B-01'), (7, 14, 'B-02'), (8, 20, 'B-03'), (9, 10, 'B-04'), (10, 45, 'B-05'), (11, 12, 'B-06'),
-- Mobile Phones
(12, 25, 'C-01'), (13, 15, 'C-02'), (14, 35, 'C-03'), (15, 50, 'C-04'), (16, 40, 'C-05'),
-- Home Appliances
(17, 10, 'D-01'), (18, 12, 'D-02'), (19, 20, 'D-03'), (20, 28, 'D-04'),
-- Furniture
(21, 18, 'E-01'), (22, 15, 'E-02'), (23, 10, 'E-03'), (24, 14, 'E-04'),
-- Stationery
(25, 80, 'F-01'), (26, 60, 'F-02'), (27, 35, 'F-03'), (28, 45, 'F-04'),
-- Networking
(29, 25, 'G-01'), (30, 18, 'G-02'), (31, 55, 'G-03');

-- ============================================
-- INSERT TRANSACTIONS (50+ transactions)
-- ============================================
-- Stock In transactions
INSERT INTO transactions (product_id, transaction_type, quantity, transaction_date, reference_number, remarks, created_by) VALUES
(1, 'STOCK_IN', 20, '2024-01-15 10:30:00', 'PO-2024-001', 'Initial purchase order', 'admin'),
(2, 'STOCK_IN', 25, '2024-01-15 11:00:00', 'PO-2024-002', 'Initial purchase order', 'admin'),
(3, 'STOCK_IN', 30, '2024-01-16 09:15:00', 'PO-2024-003', 'Initial purchase order', 'admin'),
(4, 'STOCK_IN', 40, '2024-01-16 14:20:00', 'PO-2024-004', 'Initial purchase order', 'admin'),
(5, 'STOCK_IN', 10, '2024-01-17 10:00:00', 'PO-2024-005', 'Initial purchase order', 'admin'),
(6, 'STOCK_IN', 25, '2024-01-18 11:30:00', 'PO-2024-006', 'Initial purchase order', 'manager1'),
(7, 'STOCK_IN', 20, '2024-01-18 15:45:00', 'PO-2024-007', 'Initial purchase order', 'manager1'),
(8, 'STOCK_IN', 30, '2024-01-19 09:00:00', 'PO-2024-008', 'Initial purchase order', 'manager1'),
(9, 'STOCK_IN', 15, '2024-01-19 13:20:00', 'PO-2024-009', 'Initial purchase order', 'manager1'),
(10, 'STOCK_IN', 50, '2024-01-20 10:10:00', 'PO-2024-010', 'Initial purchase order', 'staff1'),
(11, 'STOCK_IN', 15, '2024-01-20 14:30:00', 'PO-2024-011', 'Initial purchase order', 'staff1'),
(12, 'STOCK_IN', 30, '2024-01-22 09:45:00', 'PO-2024-012', 'Initial purchase order', 'staff1'),
(13, 'STOCK_IN', 20, '2024-01-22 11:15:00', 'PO-2024-013', 'Initial purchase order', 'staff1'),
(14, 'STOCK_IN', 40, '2024-01-23 10:00:00', 'PO-2024-014', 'Initial purchase order', 'staff2'),
(15, 'STOCK_IN', 60, '2024-01-23 14:20:00', 'PO-2024-015', 'Initial purchase order', 'staff2'),
(16, 'STOCK_IN', 50, '2024-01-24 09:30:00', 'PO-2024-016', 'Initial purchase order', 'staff2'),
(17, 'STOCK_IN', 15, '2024-01-24 13:00:00', 'PO-2024-017', 'Initial purchase order', 'admin'),
(18, 'STOCK_IN', 18, '2024-01-25 10:45:00', 'PO-2024-018', 'Initial purchase order', 'admin'),
(19, 'STOCK_IN', 25, '2024-01-25 15:10:00', 'PO-2024-019', 'Initial purchase order', 'manager1'),
(20, 'STOCK_IN', 35, '2024-01-26 09:20:00', 'PO-2024-020', 'Initial purchase order', 'manager1'),

-- Stock Out transactions
(1, 'STOCK_OUT', 8, '2024-02-01 10:30:00', 'INV-2024-001', 'Sale to customer', 'staff1'),
(2, 'STOCK_OUT', 10, '2024-02-02 11:15:00', 'INV-2024-002', 'Sale to customer', 'staff1'),
(3, 'STOCK_OUT', 5, '2024-02-03 14:20:00', 'INV-2024-003', 'Sale to customer', 'staff2'),
(6, 'STOCK_OUT', 7, '2024-02-05 09:45:00', 'INV-2024-004', 'Sale to customer', 'staff2'),
(7, 'STOCK_OUT', 6, '2024-02-06 13:30:00', 'INV-2024-005', 'Sale to customer', 'staff1'),
(12, 'STOCK_OUT', 5, '2024-02-08 10:00:00', 'INV-2024-006', 'Sale to customer', 'staff1'),
(13, 'STOCK_OUT', 5, '2024-02-09 11:20:00', 'INV-2024-007', 'Sale to customer', 'staff2'),
(14, 'STOCK_OUT', 5, '2024-02-10 15:40:00', 'INV-2024-008', 'Sale to customer', 'staff2'),
(15, 'STOCK_OUT', 10, '2024-02-12 09:15:00', 'INV-2024-009', 'Sale to customer', 'staff1'),
(16, 'STOCK_OUT', 10, '2024-02-13 14:25:00', 'INV-2024-010', 'Sale to customer', 'staff1'),
(21, 'STOCK_OUT', 3, '2024-02-15 10:50:00', 'INV-2024-011', 'Corporate order', 'manager1'),
(22, 'STOCK_OUT', 3, '2024-02-16 11:30:00', 'INV-2024-012', 'Corporate order', 'manager1'),
(25, 'STOCK_OUT', 20, '2024-02-18 09:40:00', 'INV-2024-013', 'Bulk office supply order', 'staff1'),
(26, 'STOCK_OUT', 20, '2024-02-19 13:15:00', 'INV-2024-014', 'Bulk office supply order', 'staff1'),
(29, 'STOCK_OUT', 5, '2024-02-20 10:20:00', 'INV-2024-015', 'Network setup project', 'staff2'),

-- Recent Stock In (Replenishment)
(1, 'STOCK_IN', 5, '2024-11-01 10:00:00', 'PO-2024-101', 'Restock order', 'manager1'),
(3, 'STOCK_IN', 10, '2024-11-05 11:30:00', 'PO-2024-102', 'Restock order', 'manager1'),
(6, 'STOCK_IN', 8, '2024-11-08 09:45:00', 'PO-2024-103', 'Restock order', 'staff1'),
(10, 'STOCK_IN', 15, '2024-11-10 14:20:00', 'PO-2024-104', 'Restock order', 'staff1'),
(25, 'STOCK_IN', 50, '2024-11-12 10:15:00', 'PO-2024-105', 'Monthly stationery order', 'staff2'),

-- Adjustment transactions
(5, 'ADJUSTMENT', 2, '2024-10-15 16:30:00', NULL, 'Physical count - 2 units damaged', 'manager1'),
(10, 'ADJUSTMENT', 5, '2024-10-20 17:00:00', NULL, 'Physical count discrepancy', 'manager1'),
(27, 'ADJUSTMENT', 3, '2024-11-01 16:45:00', NULL, 'Found extra stock during audit', 'admin'),

-- Recent transactions (November 2024)
(12, 'STOCK_OUT', 3, '2024-11-15 10:30:00', 'INV-2024-051', 'Sale to customer', 'staff1'),
(14, 'STOCK_OUT', 8, '2024-11-16 11:45:00', 'INV-2024-052', 'Sale to customer', 'staff1'),
(19, 'STOCK_OUT', 5, '2024-11-18 14:20:00', 'INV-2024-053', 'Sale to customer', 'staff2'),
(21, 'STOCK_OUT', 2, '2024-11-20 09:30:00', 'INV-2024-054', 'Office setup', 'manager1'),
(29, 'STOCK_OUT', 3, '2024-11-22 13:15:00', 'INV-2024-055', 'Network upgrade project', 'staff2'),
(31, 'STOCK_OUT', 15, '2024-11-25 10:45:00', 'INV-2024-056', 'Bulk cable order', 'staff1'),
(4, 'STOCK_OUT', 10, '2024-11-28 15:30:00', 'INV-2024-057', 'Sale to customer', 'staff1'),
(8, 'STOCK_OUT', 10, '2024-11-29 11:20:00', 'INV-2024-058', 'Corporate laptop order', 'manager1');

-- ============================================
-- VERIFICATION QUERIES
-- ============================================
-- Run these to verify data insertion

-- Total products
-- SELECT COUNT(*) AS total_products FROM products;

-- Total inventory value
-- SELECT SUM(i.quantity_in_stock * p.unit_price) AS total_inventory_value
-- FROM inventory i
-- JOIN products p ON i.product_id = p.product_id;

-- Low stock products
-- SELECT p.product_name, i.quantity_in_stock, p.reorder_level
-- FROM products p
-- JOIN inventory i ON p.product_id = i.product_id
-- WHERE i.quantity_in_stock <= p.reorder_level;

-- Transaction summary
-- SELECT transaction_type, COUNT(*) AS count, SUM(quantity) AS total_quantity
-- FROM transactions
-- GROUP BY transaction_type;

-- ============================================
