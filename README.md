# Vendor Management System

This is a Vendor Management System developed using Django and Django REST Framework. The system handles vendor profiles, purchase order tracking, and vendor performance metrics.

## Installation

1. Clone the repository:

git clone https://github.com/your_username/vendor-management-system.git

2. Navigate to the project directory:

cd vendor-management-system

3. Install dependencies:

pip install -r requirements.txt

## Usage

1. Run migrations:

python manage.py migrate

2. Create a superuser:

python manage.py createsuperuser

3. Start the development server:

python manage.py runserver

4. Access the admin interface at `http://127.0.0.1:8000/admin/` and log in with the superuser credentials.

5. Use the provided API endpoints for vendor profile management, purchase order tracking, and vendor performance evaluation.

## Acknowledgment Date

- The acknowledgment date represents the date and time when a vendor acknowledges the receipt of a purchase order (PO). It is an important field in the system, indicating when the vendor formally confirms the reception of the PO and commits to fulfilling it according to the specified terms and conditions.
### API Endpoints

- **Acknowledgment Date Endpoint**:
  - POST /purchase_orders/{po_id}/acknowledge: Acknowledge the receipt of a purchase order. This endpoint updates the acknowledgment date and triggers the recalculation of average response time.

  Example:
POST /purchase_orders/1/acknowledge

## API Endpoints

- **Vendor Profile Management**:
  - POST /vendors/: Create a new vendor.
  - GET /vendors/: List all vendors.
  - GET /vendors/{vendor_id}/: Retrieve a specific vendor's details.
  - PUT /vendors/{vendor_id}/: Update a vendor's details.
  - DELETE/vendors/{vendor_id}/: Delete a vendor.

- **Purchase Order Tracking**:
  - POST /purchase_orders/: Create a purchase order.
  - GET /purchase_orders/: List all purchase orders with an option to filter by vendor.
  - GET /purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
  - PUT /purchase_orders/{po_id}/: Update a purchase order.
  - DELETE/purchase_orders/{po_id}/: Delete a purchase order.

- **Vendor Performance Evaluation**:
  - GET /vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics.

## Additional Details

- The project adheres to RESTful principles in API design.
- Comprehensive data validations are implemented for models.
- Django ORM is used for database interactions.
- API endpoints are secured with token-based authentication.
- PEP 8 style guidelines are followed for Python code.
- Each API endpoint is thoroughly documented.
