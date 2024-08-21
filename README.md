# E-commerce Platform

A comprehensive e-commerce solution built with Django and Django Rest Framework. This platform provides a robust backend for managing products, orders, user accounts, and more.

## Table of Contents

- [E-commerce Platform](#e-commerce-platform)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
  - [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **User Management**
  - Custom user model with email-based authentication
  - User profiles with additional information
  - JWT authentication

- **Product Management**
  - Product categories, images, and tags
  - Inventory management with stock adjustments
  - Flexible pricing system with discounts and promotions

- **Shopping Experience**
  - Shopping cart functionality
  - Order placement and management
  - Product review system

- **Search and Filtering**
  - Advanced product search with multiple filters and sorting options

- **Supplier Features**
  - Supplier-specific views and permissions
  - Inventory and pricing management for suppliers

## Technologies Used

- Django 5.0.4
- Django Rest Framework
- SimpleJWT for authentication
- SQLite (easily adaptable to other databases)

## Project Structure

The project is organized into several Django apps, each responsible for specific functionalities:

- `users`: User authentication and management
- `profiles`: User profile management
- `products`: Product information and management
- `inventory`: Inventory management
- `pricing`: Product pricing, discounts, and promotions
- `cart`: Shopping cart functionality
- `orders`: Order processing and management
- `reviews`: Product review system
- `search`: Search functionality

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/mertcolakoglu/ecommerce_all.git
   cd ecommerce_all
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   - Create a `.env` file in the project root
   - Add the following variables:
     ```
     SECRET_KEY=your_secret_key
     DEBUG=True
     ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

## Usage

1. Start the development server:
   ```
   python manage.py runserver
   ```

2. Access the admin panel at `http://localhost:8000/admin/` to manage users, products, and other data.

3. Use the API endpoints to interact with the e-commerce platform programmatically.

## API Endpoints

Here are some of the main API endpoints:

- User Registration: `POST /auth/users/`
- User Login: `POST /auth/jwt/create/`
- User Profile: `GET /api/profiles/me/`
- Product List: `GET /api/products/`
- Create Product: `POST /api/products/`
- Search Products: `GET /api/search/?q=<query>`
- Add to Cart: `POST /api/carts/add_to_cart/`
- Place Order: `POST /api/orders/`
- Create Review: `POST /api/reviews/`

For a full list of endpoints and their usage, please refer to the API documentation (TODO: Add link to API docs).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.