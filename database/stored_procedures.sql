-- ============================================
-- Inventory Management System - Stored Procedures
-- ============================================
-- These procedures encapsulate business logic and ensure data consistency
-- ============================================

USE inventory_management;

DELIMITER $$

-- ============================================
-- PROCEDURE: sp_record_stock_in
-- Purpose: Add stock to inventory and record transaction
-- Parameters:
--   - p_product_id: Product ID to add stock
--   - p_quantity: Quantity to add
--   - p_reference_number: PO number or reference
--   - p_remarks: Additional notes
--   - p_created_by: Username of person recording transaction
-- Returns: Success message or error
-- ============================================
DROP PROCEDURE IF EXISTS sp_record_stock_in$$

CREATE PROCEDURE sp_record_stock_in(
    IN p_product_id INT,
    IN p_quantity INT,
    IN p_reference_number VARCHAR(50),
    IN p_remarks TEXT,
    IN p_created_by VARCHAR(50)
)
BEGIN
    DECLARE v_error_message VARCHAR(255);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error: Transaction failed. Stock not added.' AS error_message;
    END;

    -- Start transaction
    START TRANSACTION;

    -- Validate product exists
    IF NOT EXISTS (SELECT 1 FROM products WHERE product_id = p_product_id) THEN
        SET v_error_message = CONCAT('Error: Product ID ', p_product_id, ' does not exist.');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_error_message;
    END IF;

    -- Validate quantity
    IF p_quantity <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Quantity must be greater than 0.';
    END IF;

    -- Update inventory (or insert if not exists)
    INSERT INTO inventory (product_id, quantity_in_stock, last_updated)
    VALUES (p_product_id, p_quantity, NOW())
    ON DUPLICATE KEY UPDATE
        quantity_in_stock = quantity_in_stock + p_quantity,
        last_updated = NOW();

    -- Record transaction
    INSERT INTO transactions (product_id, transaction_type, quantity, reference_number, remarks, created_by)
    VALUES (p_product_id, 'STOCK_IN', p_quantity, p_reference_number, p_remarks, p_created_by);

    COMMIT;

    SELECT
        CONCAT('Success: ', p_quantity, ' units added to product ID ', p_product_id) AS success_message,
        LAST_INSERT_ID() AS transaction_id;
END$$

-- ============================================
-- PROCEDURE: sp_record_stock_out
-- Purpose: Remove stock from inventory and record transaction
-- Parameters:
--   - p_product_id: Product ID to remove stock
--   - p_quantity: Quantity to remove
--   - p_reference_number: Invoice/order number
--   - p_remarks: Additional notes
--   - p_created_by: Username of person recording transaction
-- Returns: Success message or error
-- ============================================
DROP PROCEDURE IF EXISTS sp_record_stock_out$$

CREATE PROCEDURE sp_record_stock_out(
    IN p_product_id INT,
    IN p_quantity INT,
    IN p_reference_number VARCHAR(50),
    IN p_remarks TEXT,
    IN p_created_by VARCHAR(50)
)
BEGIN
    DECLARE v_current_stock INT;
    DECLARE v_error_message VARCHAR(255);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error: Transaction failed. Stock not removed.' AS error_message;
    END;

    -- Start transaction
    START TRANSACTION;

    -- Validate product exists
    IF NOT EXISTS (SELECT 1 FROM products WHERE product_id = p_product_id) THEN
        SET v_error_message = CONCAT('Error: Product ID ', p_product_id, ' does not exist.');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_error_message;
    END IF;

    -- Validate quantity
    IF p_quantity <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Quantity must be greater than 0.';
    END IF;

    -- Get current stock
    SELECT quantity_in_stock INTO v_current_stock
    FROM inventory
    WHERE product_id = p_product_id;

    -- Check if sufficient stock available
    IF v_current_stock IS NULL OR v_current_stock < p_quantity THEN
        SET v_error_message = CONCAT('Error: Insufficient stock. Available: ', COALESCE(v_current_stock, 0), ', Requested: ', p_quantity);
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_error_message;
    END IF;

    -- Update inventory
    UPDATE inventory
    SET quantity_in_stock = quantity_in_stock - p_quantity,
        last_updated = NOW()
    WHERE product_id = p_product_id;

    -- Record transaction
    INSERT INTO transactions (product_id, transaction_type, quantity, reference_number, remarks, created_by)
    VALUES (p_product_id, 'STOCK_OUT', p_quantity, p_reference_number, p_remarks, p_created_by);

    COMMIT;

    SELECT
        CONCAT('Success: ', p_quantity, ' units removed from product ID ', p_product_id) AS success_message,
        LAST_INSERT_ID() AS transaction_id,
        (v_current_stock - p_quantity) AS remaining_stock;
END$$

-- ============================================
-- PROCEDURE: sp_adjust_stock
-- Purpose: Adjust inventory for corrections (damaged goods, count discrepancies)
-- Parameters:
--   - p_product_id: Product ID to adjust
--   - p_new_quantity: New stock quantity after adjustment
--   - p_remarks: Reason for adjustment
--   - p_created_by: Username of person recording adjustment
-- ============================================
DROP PROCEDURE IF EXISTS sp_adjust_stock$$

CREATE PROCEDURE sp_adjust_stock(
    IN p_product_id INT,
    IN p_new_quantity INT,
    IN p_remarks TEXT,
    IN p_created_by VARCHAR(50)
)
BEGIN
    DECLARE v_current_stock INT;
    DECLARE v_difference INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error: Adjustment failed.' AS error_message;
    END;

    START TRANSACTION;

    -- Validate product exists
    IF NOT EXISTS (SELECT 1 FROM products WHERE product_id = p_product_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Product does not exist.';
    END IF;

    -- Validate new quantity
    IF p_new_quantity < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: New quantity cannot be negative.';
    END IF;

    -- Get current stock
    SELECT COALESCE(quantity_in_stock, 0) INTO v_current_stock
    FROM inventory
    WHERE product_id = p_product_id;

    -- Calculate difference
    SET v_difference = ABS(p_new_quantity - COALESCE(v_current_stock, 0));

    -- Update inventory
    INSERT INTO inventory (product_id, quantity_in_stock, last_updated)
    VALUES (p_product_id, p_new_quantity, NOW())
    ON DUPLICATE KEY UPDATE
        quantity_in_stock = p_new_quantity,
        last_updated = NOW();

    -- Record transaction
    INSERT INTO transactions (product_id, transaction_type, quantity, remarks, created_by)
    VALUES (p_product_id, 'ADJUSTMENT', v_difference, p_remarks, p_created_by);

    COMMIT;

    SELECT
        CONCAT('Success: Stock adjusted from ', COALESCE(v_current_stock, 0), ' to ', p_new_quantity) AS success_message,
        LAST_INSERT_ID() AS transaction_id;
END$$

-- ============================================
-- PROCEDURE: sp_get_low_stock_products
-- Purpose: Get list of products below specified threshold
-- Parameters:
--   - p_threshold: Stock level threshold (optional, defaults to reorder_level)
-- Returns: List of products with low stock
-- ============================================
DROP PROCEDURE IF EXISTS sp_get_low_stock_products$$

CREATE PROCEDURE sp_get_low_stock_products(
    IN p_threshold INT
)
BEGIN
    IF p_threshold IS NULL THEN
        -- Use reorder_level if threshold not specified
        SELECT
            p.product_id,
            p.product_name,
            p.sku,
            c.category_name,
            s.company_name AS supplier_name,
            i.quantity_in_stock,
            p.reorder_level,
            p.unit_price,
            (p.reorder_level - i.quantity_in_stock) AS quantity_to_order
        FROM products p
        INNER JOIN inventory i ON p.product_id = i.product_id
        INNER JOIN categories c ON p.category_id = c.category_id
        INNER JOIN suppliers s ON p.supplier_id = s.supplier_id
        WHERE i.quantity_in_stock <= p.reorder_level
        ORDER BY i.quantity_in_stock ASC;
    ELSE
        -- Use specified threshold
        SELECT
            p.product_id,
            p.product_name,
            p.sku,
            c.category_name,
            s.company_name AS supplier_name,
            i.quantity_in_stock,
            p.reorder_level,
            p.unit_price,
            (p.reorder_level - i.quantity_in_stock) AS quantity_to_order
        FROM products p
        INNER JOIN inventory i ON p.product_id = i.product_id
        INNER JOIN categories c ON p.category_id = c.category_id
        INNER JOIN suppliers s ON p.supplier_id = s.supplier_id
        WHERE i.quantity_in_stock <= p_threshold
        ORDER BY i.quantity_in_stock ASC;
    END IF;
END$$

-- ============================================
-- PROCEDURE: sp_get_stock_valuation
-- Purpose: Calculate total inventory value
-- Returns: Total inventory value and breakdown by category
-- ============================================
DROP PROCEDURE IF EXISTS sp_get_stock_valuation$$

CREATE PROCEDURE sp_get_stock_valuation()
BEGIN
    -- Overall valuation
    SELECT
        'TOTAL' AS category,
        SUM(i.quantity_in_stock * p.unit_price) AS total_value,
        SUM(i.quantity_in_stock) AS total_units,
        COUNT(DISTINCT p.product_id) AS total_products
    FROM inventory i
    INNER JOIN products p ON i.product_id = p.product_id

    UNION ALL

    -- Category-wise valuation
    SELECT
        c.category_name AS category,
        SUM(i.quantity_in_stock * p.unit_price) AS total_value,
        SUM(i.quantity_in_stock) AS total_units,
        COUNT(DISTINCT p.product_id) AS total_products
    FROM inventory i
    INNER JOIN products p ON i.product_id = p.product_id
    INNER JOIN categories c ON p.category_id = c.category_id
    GROUP BY c.category_id, c.category_name
    ORDER BY total_value DESC;
END$$

-- ============================================
-- PROCEDURE: sp_get_product_transaction_history
-- Purpose: Get complete transaction history for a product
-- Parameters:
--   - p_product_id: Product ID
--   - p_start_date: Start date for filtering (optional)
--   - p_end_date: End date for filtering (optional)
-- ============================================
DROP PROCEDURE IF EXISTS sp_get_product_transaction_history$$

CREATE PROCEDURE sp_get_product_transaction_history(
    IN p_product_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    IF p_start_date IS NULL THEN
        SET p_start_date = '2000-01-01';
    END IF;

    IF p_end_date IS NULL THEN
        SET p_end_date = CURDATE();
    END IF;

    SELECT
        t.transaction_id,
        t.transaction_type,
        t.quantity,
        t.transaction_date,
        t.reference_number,
        t.remarks,
        t.created_by,
        p.product_name,
        p.sku
    FROM transactions t
    INNER JOIN products p ON t.product_id = p.product_id
    WHERE t.product_id = p_product_id
        AND DATE(t.transaction_date) BETWEEN p_start_date AND p_end_date
    ORDER BY t.transaction_date DESC;
END$$

-- ============================================
-- PROCEDURE: sp_get_transaction_summary
-- Purpose: Get transaction summary for a date range
-- Parameters:
--   - p_start_date: Start date
--   - p_end_date: End date
-- ============================================
DROP PROCEDURE IF EXISTS sp_get_transaction_summary$$

CREATE PROCEDURE sp_get_transaction_summary(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT
        t.transaction_type,
        COUNT(*) AS transaction_count,
        SUM(t.quantity) AS total_quantity,
        SUM(t.quantity * p.unit_price) AS total_value
    FROM transactions t
    INNER JOIN products p ON t.product_id = p.product_id
    WHERE DATE(t.transaction_date) BETWEEN p_start_date AND p_end_date
    GROUP BY t.transaction_type
    ORDER BY t.transaction_type;
END$$

DELIMITER ;

-- ============================================
-- USAGE EXAMPLES
-- ============================================

-- Example 1: Record stock in
-- CALL sp_record_stock_in(1, 100, 'PO-2024-001', 'Initial stock purchase', 'admin');

-- Example 2: Record stock out
-- CALL sp_record_stock_out(1, 50, 'INV-2024-001', 'Sale to customer', 'staff1');

-- Example 3: Adjust stock (physical count correction)
-- CALL sp_adjust_stock(1, 45, 'Physical count discrepancy - 5 units damaged', 'manager');

-- Example 4: Get low stock products (using reorder level)
-- CALL sp_get_low_stock_products(NULL);

-- Example 5: Get low stock products (custom threshold)
-- CALL sp_get_low_stock_products(20);

-- Example 6: Get stock valuation
-- CALL sp_get_stock_valuation();

-- Example 7: Get product transaction history
-- CALL sp_get_product_transaction_history(1, '2024-01-01', '2024-12-31');

-- Example 8: Get transaction summary
-- CALL sp_get_transaction_summary('2024-01-01', '2024-12-31');

-- ============================================
