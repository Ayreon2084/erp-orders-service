# ERP Orders Service

Backend service for managing orders, products, categories, and clients in an ERP system.

## Features

- REST API for order management
- Product catalog with hierarchical categories (unlimited nesting levels)
- Client management
- Order processing with multiple products per order
- Historical price tracking in orders
- Soft delete support for data recovery

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Containerization**: Docker, Docker Compose
- **Language**: Python 3.13
- **Linter**: Ruff

## Project Structure

```
erp-orders-service/
├── app/
│   ├── api/              # API endpoints
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/             # Configuration and enums
│   ├── db/               # Database models and session
│   │   └── models/
│   ├── repositories/     # Data access layer
│   ├── services/         # Business logic layer
│   └── schemas/          # Pydantic schemas
├── migrations/           # Alembic migrations
├── sql/                  # SQL queries (requirements 2.1-2.3)
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh         # DB wait, migrations, uvicorn (Docker)
└── pyproject.toml
```

## Database Schema

### Entities

1. **Products** (Nomenclature)
   - `name` - Product name
   - `quantity` - Stock quantity
   - `price` - Current price
   - `sku` - Unique product code
   - `category_id` - Reference to category

2. **Categories** (Hierarchical catalog)
   - `name` - Category name
   - `parent_id` - Reference to parent category (NULL for root)
   - `root_category_id` - Reference to root (top-level) category; denormalization for reports without recursive queries
   - Supports unlimited nesting levels

3. **Clients**
   - `full_name` - Client name
   - `address` - Delivery address
   - `email` - Contact email

4. **Orders**
   - `client_id` - Reference to client
   - `status` - Order status (new, processing, paid, completed, cancelled)
   - Multiple products per order via `OrderProduct` junction table
   - `price_at_order` - Historical price at order time

See `sql/DATABASE_SCHEMA.md` for detailed ER diagram and schema description.

## Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for local development)
- Poetry (for dependency management)

### Setup

1. Clone the repository:
```bash
git clone git@github.com:Ayreon2084/erp-orders-service.git
cd erp-orders-service
```

2. Create `.env` from example and set your values:
```bash
cp .env.example .env
```

3. Start the application:

**Using Docker (recommended)** — database, migrations, and app start together (entrypoint runs `alembic upgrade head` before uvicorn):
```bash
docker-compose up
```
API: `http://localhost:8000`

**Or run locally** — start only the database, then run migrations and the app on your machine:
```bash
docker-compose up -d db
alembic upgrade head
poetry install
uvicorn app.main:app --reload
```
API: `http://localhost:8000`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Main Endpoints

### Orders

- `POST /api/v1/orders/` - Create new order
- `GET /api/v1/orders/` - List orders
- `GET /api/v1/orders/{order_id}` - Get order details
- `POST /api/v1/orders/{order_id}/items` - Add product to order
- `POST /api/v1/orders/{order_id}/items/batch` - Add multiple products to order
- `PATCH /api/v1/orders/{order_id}/status` - Update order status
- `DELETE /api/v1/orders/{order_id}` - Delete order

### Products

- `POST /api/v1/products/` - Create product
- `GET /api/v1/products/` - List products
- `GET /api/v1/products/{product_id}` - Get product details
- `PATCH /api/v1/products/{product_id}` - Update product details
- `DELETE /api/v1/products/{product_id}` - Delete product

### Categories

- `POST /api/v1/categories/` - Create category
- `GET /api/v1/categories/` - List categories (flat, with pagination)
- `GET /api/v1/categories/roots` - List root categories (tree)
- `GET /api/v1/categories/{category_id}` - Get category (tree)
- `GET /api/v1/categories/{category_id}/children` - Get direct children
- `PATCH /api/v1/categories/{category_id}` - Update category
- `DELETE /api/v1/categories/{category_id}` - Delete category

### Clients

- `POST /api/v1/clients/` - Create client
- `GET /api/v1/clients/` - List clients
- `GET /api/v1/clients/{client_id}` - Get client
- `PATCH /api/v1/clients/{client_id}` - Update client
- `DELETE /api/v1/clients/{client_id}` - Delete client

## SQL Queries (Task Requirements 2.1-2.3)

All SQL queries required by the technical specification are located in the `sql/` directory:

- `sql/2.1_client_order_totals.sql` - Total order amounts per client
- `sql/2.2_category_first_level_children_count.sql` - Count of first-level children for categories
- `sql/2.3.1_top_products_view.sql` - Creates VIEW for top-5 products last month
- `sql/2.3.2_query_optimization_analysis.md` - Query optimization analysis

## Example Usage

### Add Product to Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders/1/items" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

### Create Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders/?client_id=1"
```

## Architecture

The project has layered architecture:

1. **API Layer** (`app/api/`) - HTTP request handling
2. **Service Layer** (`app/services/`) - Business logic
3. **Repository Layer** (`app/repositories/`) - Data access abstraction
4. **Model Layer** (`app/db/models/`) - Database models
5. **Serialization** (`app/schemas/`) - Pydantic schemas

This separation ensures:
- Testability
- Maintainability
- Compliance with SOLID principles
- Easy to extend and modify


## Development

### Code Formatting

```bash
poetry run ruff format .
poetry run ruff check .
```

### Creating Migrations

```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## License

This project is a test assignment.

## Author

Alexander Zhukov
