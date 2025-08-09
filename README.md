# **College Canteen Pre-Order System**

This is a full-stack web application developed to serve as a pre-order system for a college canteen. The primary goal is to minimize queue times and streamline the ordering process for students by allowing them to place orders and manage pickup times online. The application is built as a Minimum Viable Product (MVP) following the provided implementation document.

## **1\. Problem and Solution**

**Problem:** College canteens often experience long queues during peak hours, leading to student dissatisfaction and operational bottlenecks. The traditional ordering process is slow and inefficient.

**Solution:** The College Canteen Pre-Order System provides a web-based platform where students can browse the menu, place orders, and track their status in real-time. Canteen staff (sellers) can manage these incoming orders, update their status, and prepare them for pickup, creating a seamless and efficient workflow.

## **2\. Implementation Details**

### **Tech Stack**

* **Backend:** Django (version 5.2.5)  
* **API:** Django REST Framework (version 3.16.1)  
* **Database:** SQLite3  
* **Frontend:** HTML5, Tailwind CSS (via CDN)  
* **Package Management:** pip with a requirements.txt file

### **Key Features**

* **Role-Based Access Control:** The application supports three distinct user roles:  
  * **Student:** Can browse the menu, add items to a cart, place and track orders, and view order history.  
  * **Seller:** Can view incoming orders, update their status (e.g., Pending → Preparing → Ready), and view order details.  
  * **Admin:** Manages all users, menu items, and has full control over the system via the Django Admin Panel.  
* **Modern UI:** The user interface is designed to be modern and responsive, with a focus on mobile-first design, clean typography, and a user-friendly layout.  
* **Simulated Functionality:** For the MVP, the payment process is simulated, and user and seller registration is handled exclusively through the Django Admin Panel.

### **Database Models**

The application is built around several key database models to handle the core functionality:

* User: Manages user accounts with a role field (student, seller, admin).  
* MenuItem: Stores details for each food item, including name, price, category, and availability.  
* Order: Represents a single order, linking a user to a list of MenuItems and tracking its status and total\_amount.  
* OrderItem: A junction table that links Orders to MenuItems, storing the quantity and price at the time of the order.  
* OrderStatusHistory: Logs all status changes for an order, providing a complete audit trail.

## **3\. How to Run the Application**

Follow these steps to get the project up and running on your local machine.

### **Prerequisites**

* Python 3.8 or higher installed on your system.

### **Steps**

1. **Clone the project folder** and navigate into the main directory in your terminal.  
   git clone https://github.com/Shomyym/QuickBite.git  
2. **Create and activate a virtual environment:**  
   \# Create the virtual environment  
   python3 \-m venv venv

   \# Activate it  
   \# On macOS/Linux:  
   source venv/bin/activate  
   \# On Windows:  
   venv\\Scripts\\activate

3. **Install the required packages** using the requirements.txt file:  
   (venv) ➜ pip install \-r requirements.txt

4. **Run database migrations** to ensure your local database is set up correctly:  
   (venv) ➜ python manage.py migrate

5. **Start the Django development server:**  
   (venv) ➜ python manage.py runserver

The application will now be accessible at http://127.0.0.1:8000/.

## **4\. Demo Credentials**

The database has been pre-seeded with sample data to allow for immediate testing of all user roles.

| Role | Username | Password |
| :---- | :---- | :---- |
| **Admin** | mia | miamiamia |
| **Student** | shomy | \!aH8hymQxWgRP7v |
| **Seller** | staff | DvT$JLEGJb@QW3f |

### **To Test the Application:**

* **Student Flow:** Log in as student1, browse the menu, add items to the cart, and place an order.  
* **Seller Flow:** Log in as seller1, go to the dashboard, and change the status of the order placed by student1.  
* **Admin Flow:** Log in to the Django Admin at http://127.0.0.1:8000/admin/ to manage users and menu items.
