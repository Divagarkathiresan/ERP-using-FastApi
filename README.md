# FastAPI ERP Backend

A RESTful ERP backend API built with FastAPI, MongoDB, and JWT authentication. It provides role-based access control for managing products, users, inventory, and orders.

## Features

- **User Authentication & Authorization**: JWT-based login with role-based access (admin, manager, user)
- **Product Management**: CRUD operations with pagination, filtering, and sorting
- **User Management**: Registration and login with role-based permissions
- **Inventory Management**: Stock tracking with quantity management
- **Order Processing**: Order placement with invoice generation and inventory deduction
- **MongoDB Integration**: Document-based data storage with PyMongo

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB (PyMongo)
- **Authentication**: JWT (python-jose)
- **Validation**: Pydantic
- **Environment**: python-dotenv

## Project Structure

```
erp_backend/
├── main.py                          # App entry point
├── .gitignore
├── README.md
└── app/
    ├── Database/
    │   └── database.py              # MongoDB connection & collections
    ├── Models/
    │   └── models.py                # Pydantic schemas
    ├── Routes/
    │   ├── productRoutes.py         # Product endpoints
    │   ├── userRoutes.py            # User endpoints
    │   └── inventoryRoutes.py       # Inventory & Order endpoints
    ├── Services/
    │   ├── productService.py        # Product business logic
    │   ├── userService.py           # User & auth logic
    │   ├── inventoryService.py      # Inventory business logic
    │   └── orderService.py          # Order processing logic
    └── utils/
        └── jwtconfig.py             # JWT token utilities
```

## Setup

1. Clone the repository and navigate into the project
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn pymongo python-jose[cryptography] python-dotenv passlib bcrypt
   ```
4. Create a `.env` file in the root directory with the following variables:
   ```env
   MONGO_URI=your_mongodb_connection_string
   DB_NAME=your_database_name
   ```
5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
6. Open `http://localhost:8000/docs` to access the auto-generated Swagger UI.

## API Endpoints

### User Routes (`/user`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/user/register` | Register a new user | No |
| POST | `/user/login` | Login and get JWT token | No |
| GET | `/user` | Get all users | No |

### Product Routes (`/product`)
| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| POST | `/product` | Add new product | Yes | admin |
| GET | `/product` | Get all products | No | - |
| GET | `/product/{id}` | Get single product by ID | No | - |
| PUT | `/product/{id}` | Update a product | No | - |
| DELETE | `/product/{id}` | Delete a product by ID | No | - |
| DELETE | `/all` | Delete all products | No | - |
| GET | `/products/pagination` | Get paginated products | No | - |
| GET | `/products/filter?category={category}` | Filter products by category | No | - |
| GET | `/products/sort?order={asc|desc}&sorting={field}` | Sort products | No | - |

### Inventory Routes (`/inventory`)
| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| POST | `/inventory` | Add new inventory | Yes | manager |
| GET | `/inventory` | Get all inventories | Yes | manager |
| PUT | `/inventory/{id}` | Update inventory | Yes | manager |
| DELETE | `/inventory/{id}` | Delete inventory | Yes | manager |

### Order Routes (`/order`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/order` | Place a new order | No |

## Authentication

Most endpoints require a JWT token. After logging in via `/user/login`, include the token in the request header:

```
Authorization: Bearer <your_token>
```

## Roles

- **admin**: Can add products
- **manager**: Can manage inventory
- **user**: Default role for regular access

## Data Models

- **User**: `user_id`, `user_name`, `user_email`, `user_password`, `user_role`
- **Product**: `product_id`, `product_name`, `product_price`, `product_category`
- **Inventory**: `inventory_id`, `product_id`, `quantity`
- **OrderItem**: `product_id`, `quantity`
- **Orders**: `items` (list of OrderItem)
