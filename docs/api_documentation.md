# API Documentation
## Inventory Management System REST API

---

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Products API](#products-api)
4. [Suppliers API](#suppliers-api)
5. [Categories API](#categories-api)
6. [Inventory API](#inventory-api)
7. [Transactions API](#transactions-api)
8. [Reports API](#reports-api)
9. [Authentication/Users API](#authenticationusers-api)
10. [Error Handling](#error-handling)

---

## Overview

**Base URL:** `http://localhost:5000/api`

**Response Format:** JSON

**Date Format:** ISO 8601 (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)

**Currency:** Indian Rupees (₹)

### Standard Response Structure

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message description"
}
```

---

## Authentication

### Login

**Endpoint:** `POST /api/auth/login`

**Description:** Authenticate user and receive JWT token

**Request Body:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": 1,
    "username": "admin",
    "full_name": "Admin User",
    "email": "admin@inventory.com",
    "role": "admin",
    "is_active": true
  }
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": "Invalid username or password"
}
```

### Verify Token

**Endpoint:** `POST /api/auth/verify`

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

---

## Products API

### Get All Products

**Endpoint:** `GET /api/products`

**Description:** Retrieve paginated list of products with optional filters

**Query Parameters:**
- `page` (int, default: 1) - Page number
- `per_page` (int, default: 10) - Items per page
- `search` (string) - Search in product name or SKU
- `category_id` (int) - Filter by category
- `supplier_id` (int) - Filter by supplier

**Example Request:**
```
GET /api/products?page=1&per_page=10&search=laptop&category_id=2
```

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "product_id": 6,
      "product_name": "Dell Inspiron 15 Laptop",
      "sku": "COMP-LAP-001",
      "description": "Intel i5, 8GB RAM, 512GB SSD, Windows 11",
      "category_id": 2,
      "category_name": "Computers & Laptops",
      "supplier_id": 1,
      "supplier_name": "Tech Distributors India Pvt Ltd",
      "unit_price": 52999.00,
      "reorder_level": 10,
      "quantity_in_stock": 18,
      "created_at": "2024-01-18T11:30:00",
      "updated_at": "2024-01-18T11:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 31,
    "pages": 4
  }
}
```

### Get Product by ID

**Endpoint:** `GET /api/products/:id`

**Example Request:**
```
GET /api/products/6
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "product_id": 6,
    "product_name": "Dell Inspiron 15 Laptop",
    "sku": "COMP-LAP-001",
    "description": "Intel i5, 8GB RAM, 512GB SSD, Windows 11",
    "category_id": 2,
    "category_name": "Computers & Laptops",
    "supplier_id": 1,
    "supplier_name": "Tech Distributors India Pvt Ltd",
    "unit_price": 52999.00,
    "reorder_level": 10,
    "quantity_in_stock": 18,
    "warehouse_location": "B-01",
    "created_at": "2024-01-18T11:30:00",
    "updated_at": "2024-01-18T11:30:00"
  }
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "Product not found"
}
```

### Create Product

**Endpoint:** `POST /api/products`

**Request Body:**
```json
{
  "product_name": "New Laptop Model",
  "sku": "LAP-NEW-001",
  "description": "Latest model with great specs",
  "category_id": 2,
  "supplier_id": 1,
  "unit_price": 45999.50,
  "reorder_level": 15
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Product created successfully",
  "product_id": 32
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "SKU already exists"
}
```

### Update Product

**Endpoint:** `PUT /api/products/:id`

**Request Body:** (Same as Create Product)

**Success Response (200):**
```json
{
  "success": true,
  "message": "Product updated successfully"
}
```

### Delete Product

**Endpoint:** `DELETE /api/products/:id`

**Success Response (200):**
```json
{
  "success": true,
  "message": "Product deleted successfully"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Cannot delete product with existing transactions"
}
```

### Get Low Stock Products

**Endpoint:** `GET /api/products/low-stock`

**Query Parameters:**
- `threshold` (int, optional) - Custom stock threshold

**Example Request:**
```
GET /api/products/low-stock?threshold=20
```

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "product_id": 5,
      "product_name": "Canon DSLR Camera",
      "sku": "ELEC-CAM-001",
      "category_name": "Electronics",
      "supplier_name": "Global Electronics Supply Co",
      "quantity_in_stock": 8,
      "reorder_level": 5,
      "unit_price": 35999.00
    }
  ]
}
```

---

## Suppliers API

### Get All Suppliers

**Endpoint:** `GET /api/suppliers`

**Query Parameters:**
- `page` (int, default: 1)
- `per_page` (int, default: 10)
- `search` (string) - Search in company name, contact person, or city

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "supplier_id": 1,
      "company_name": "Tech Distributors India Pvt Ltd",
      "contact_person": "Suresh Menon",
      "phone": "022-28374650",
      "email": "suresh@techdist.com",
      "address": "12, Andheri Industrial Estate",
      "city": "Mumbai",
      "state": "Maharashtra",
      "postal_code": "400053",
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 6,
    "pages": 1
  }
}
```

### Get Supplier by ID

**Endpoint:** `GET /api/suppliers/:id`

### Create Supplier

**Endpoint:** `POST /api/suppliers`

**Request Body:**
```json
{
  "company_name": "New Supplier Ltd",
  "contact_person": "John Doe",
  "phone": "011-12345678",
  "email": "john@newsupplier.com",
  "address": "123 Business Street",
  "city": "Delhi",
  "state": "Delhi",
  "postal_code": "110001"
}
```

### Update Supplier

**Endpoint:** `PUT /api/suppliers/:id`

### Delete Supplier

**Endpoint:** `DELETE /api/suppliers/:id`

### Get Supplier's Products

**Endpoint:** `GET /api/suppliers/:id/products`

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "product_id": 6,
      "product_name": "Dell Inspiron 15 Laptop",
      "sku": "COMP-LAP-001",
      "category_name": "Computers & Laptops",
      "unit_price": 52999.00,
      "quantity_in_stock": 18
    }
  ]
}
```

---

## Categories API

### Get All Categories

**Endpoint:** `GET /api/categories`

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "category_id": 1,
      "category_name": "Electronics",
      "description": "Electronic devices, gadgets, and accessories",
      "product_count": 5
    }
  ]
}
```

### Get Category by ID

**Endpoint:** `GET /api/categories/:id`

### Create Category

**Endpoint:** `POST /api/categories`

**Request Body:**
```json
{
  "category_name": "New Category",
  "description": "Category description"
}
```

### Update Category

**Endpoint:** `PUT /api/categories/:id`

### Delete Category

**Endpoint:** `DELETE /api/categories/:id`

---

## Inventory API

### Get All Inventory

**Endpoint:** `GET /api/inventory`

**Query Parameters:**
- `page`, `per_page`, `search`

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "inventory_id": 1,
      "product_id": 1,
      "product_name": "Samsung 55\" 4K Smart TV",
      "sku": "ELEC-TV-001",
      "category_name": "Electronics",
      "supplier_name": "Global Electronics Supply Co",
      "quantity_in_stock": 12,
      "reorder_level": 5,
      "warehouse_location": "A-01",
      "unit_price": 45999.00,
      "stock_value": 551988.00,
      "last_updated": "2024-11-01T10:00:00"
    }
  ],
  "pagination": { ... }
}
```

### Get Inventory by Product ID

**Endpoint:** `GET /api/inventory/:product_id`

### Update Inventory

**Endpoint:** `PUT /api/inventory/:product_id`

**Request Body:**
```json
{
  "quantity": 25,
  "warehouse_location": "A-05"
}
```

### Get Inventory Summary

**Endpoint:** `GET /api/inventory/summary`

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "total_products": 31,
    "total_units": 682,
    "total_value": 3458769.00,
    "low_stock_count": 3,
    "out_of_stock_count": 0
  }
}
```

### Get Inventory by Category

**Endpoint:** `GET /api/inventory/by-category`

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "category_id": 2,
      "category_name": "Computers & Laptops",
      "product_count": 6,
      "total_units": 119,
      "total_value": 630985.00
    }
  ]
}
```

### Get Inventory by Supplier

**Endpoint:** `GET /api/inventory/by-supplier`

---

## Transactions API

### Get All Transactions

**Endpoint:** `GET /api/transactions`

**Query Parameters:**
- `page`, `per_page`
- `product_id` (int) - Filter by product
- `type` (string) - Filter by type: STOCK_IN, STOCK_OUT, ADJUSTMENT
- `start_date` (date) - Filter from date
- `end_date` (date) - Filter to date

**Example Request:**
```
GET /api/transactions?type=STOCK_IN&start_date=2024-01-01&end_date=2024-12-31
```

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "transaction_id": 1,
      "product_id": 1,
      "product_name": "Samsung 55\" 4K Smart TV",
      "sku": "ELEC-TV-001",
      "transaction_type": "STOCK_IN",
      "quantity": 20,
      "transaction_date": "2024-01-15T10:30:00",
      "reference_number": "PO-2024-001",
      "remarks": "Initial purchase order",
      "created_by": "admin",
      "transaction_value": 919980.00
    }
  ],
  "pagination": { ... }
}
```

### Get Product Transaction History

**Endpoint:** `GET /api/transactions/history/:product_id`

**Query Parameters:**
- `start_date`, `end_date`

### Record Stock In

**Endpoint:** `POST /api/transactions/stock-in`

**Description:** Add stock to inventory

**Request Body:**
```json
{
  "product_id": 6,
  "quantity": 50,
  "reference_number": "PO-2024-150",
  "remarks": "Bulk purchase order",
  "created_by": "admin"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Success: 50 units added to product ID 6",
  "transaction_id": 59
}
```

### Record Stock Out

**Endpoint:** `POST /api/transactions/stock-out`

**Description:** Remove stock from inventory

**Request Body:**
```json
{
  "product_id": 6,
  "quantity": 10,
  "reference_number": "INV-2024-200",
  "remarks": "Sale to customer",
  "created_by": "staff1"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Success: 10 units removed from product ID 6",
  "transaction_id": 60,
  "remaining_stock": 58
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Insufficient stock. Available: 5, Requested: 10"
}
```

### Adjust Stock

**Endpoint:** `POST /api/transactions/adjust`

**Description:** Adjust stock for corrections (damaged goods, count discrepancies)

**Request Body:**
```json
{
  "product_id": 6,
  "new_quantity": 55,
  "remarks": "Physical count discrepancy - 3 units damaged",
  "created_by": "manager1"
}
```

### Get Transaction Summary

**Endpoint:** `GET /api/transactions/summary`

**Query Parameters:**
- `start_date`, `end_date`

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "transaction_type": "STOCK_IN",
      "transaction_count": 25,
      "total_quantity": 750,
      "total_value": 4250000.00
    },
    {
      "transaction_type": "STOCK_OUT",
      "transaction_count": 30,
      "total_quantity": 250,
      "total_value": 1500000.00
    }
  ]
}
```

### Get Recent Transactions

**Endpoint:** `GET /api/transactions/recent`

**Query Parameters:**
- `limit` (int, default: 10)

---

## Reports API

### Stock Summary Report

**Endpoint:** `GET /api/reports/stock-summary`

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "total_products": 31,
    "total_units": 682,
    "total_value": 3458769.00,
    "low_stock_count": 3,
    "out_of_stock_count": 0
  }
}
```

### Low Stock Report

**Endpoint:** `GET /api/reports/low-stock`

**Query Parameters:**
- `threshold` (int, optional)

### Transaction Summary Report

**Endpoint:** `GET /api/reports/transaction-summary`

**Query Parameters:**
- `start_date`, `end_date`

### Category-wise Report

**Endpoint:** `GET /api/reports/category-wise`

### Supplier-wise Report

**Endpoint:** `GET /api/reports/supplier-wise`

### Dashboard Statistics

**Endpoint:** `GET /api/reports/dashboard-stats`

**Description:** Comprehensive dashboard data

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "stock_summary": {
      "total_products": 31,
      "total_units": 682,
      "total_value": 3458769.00,
      "low_stock_count": 3,
      "out_of_stock_count": 0
    },
    "low_stock_count": 3,
    "recent_transactions": [
      { ... }
    ]
  }
}
```

---

## Authentication/Users API

### Get All Users

**Endpoint:** `GET /api/auth/users`

**Authorization:** Admin only

**Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "user_id": 1,
      "username": "admin",
      "full_name": "Admin User",
      "email": "admin@inventory.com",
      "role": "admin",
      "created_at": "2024-01-01T00:00:00",
      "is_active": true
    }
  ]
}
```

### Get User by ID

**Endpoint:** `GET /api/auth/users/:id`

### Create User

**Endpoint:** `POST /api/auth/users`

**Authorization:** Admin only

**Request Body:**
```json
{
  "username": "newuser",
  "password": "securepassword",
  "full_name": "New User Name",
  "email": "newuser@inventory.com",
  "role": "staff"
}
```

### Update User

**Endpoint:** `PUT /api/auth/users/:id`

**Authorization:** Admin only

### Change Password

**Endpoint:** `POST /api/auth/change-password`

**Request Body:**
```json
{
  "user_id": 1,
  "old_password": "currentpassword",
  "new_password": "newsecurepassword"
}
```

### Toggle User Active Status

**Endpoint:** `PUT /api/auth/users/:id/toggle-active`

**Authorization:** Admin only

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data or validation error |
| 401 | Unauthorized | Authentication required or failed |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

### Common Error Responses

**Validation Error (400):**
```json
{
  "success": false,
  "error": "Missing required field: product_name"
}
```

**Authentication Error (401):**
```json
{
  "success": false,
  "error": "Invalid or expired token"
}
```

**Not Found Error (404):**
```json
{
  "success": false,
  "error": "Product not found"
}
```

**Database Error (500):**
```json
{
  "success": false,
  "error": "Database connection failed"
}
```

---

## Testing with cURL

### Example cURL Commands

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'
```

**Get Products:**
```bash
curl -X GET "http://localhost:5000/api/products?page=1&per_page=10"
```

**Create Product:**
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Test Product",
    "sku": "TEST-001",
    "category_id": 1,
    "supplier_id": 1,
    "unit_price": 999.99,
    "reorder_level": 10
  }'
```

**Record Stock In:**
```bash
curl -X POST http://localhost:5000/api/transactions/stock-in \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 50,
    "reference_number": "PO-TEST-001",
    "remarks": "Test stock in",
    "created_by": "admin"
  }'
```

---

*End of API Documentation*
