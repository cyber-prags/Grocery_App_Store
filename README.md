
![logo](https://github.com/cyber-prags/Movie_Review_Prediction/assets/74003758/3cd72fe2-143d-4092-b525-78b0c58fe9f4)

# Grocify: Bridging the Gap Between Traditional and Online Grocery Shopping


Welcome to Grocify, your community-focused e-commerce grocery store committed to delivering the freshest groceries directly to your doorstep. Our platform is designed to offer the best of both worlds, combining the convenience of online shopping with the quality and personal touch of traditional grocery stores.

## Project Overview

The Online web-app Grocify is all about enhancing the grocery shopping experience. We leverage the power of analytics to bring you personalized shopping journeys and targeted promotions.

## Technologies Used

- **Flask**: The backbone of our application, handling routing and server-side logic to provide a seamless user experience.

- **Flask-Sqlalchemy**: An extension that simplifies database interactions through Object-Relational Mapping (ORM), making data management intuitive and efficient.

- **Flask-login**: Enhancing our application's security with secure authentication, enabling essential features like sign-up and login.

- **Matplotlib**: Empowering our managers with interactive data visualization, enabling data-driven decision-making and insightful analytics.

- **Bootstrap**: Responsible for the appealing and responsive design of our platform, ensuring a user-friendly and visually appealing interface.

- **Datetime**: A fundamental component for managing date and time data types, especially critical for handling product expiry dates and ensuring timely deliveries.


## Database Schema: 

![app_images](https://github.com/cyber-prags/Movie_Review_Prediction/assets/74003758/3b8045b2-0945-4962-9408-9f40d09085e4)

## Database Structure

Grocify's database is organized into five interconnected tables, each serving a specific purpose:

- **Managers**: This table stores essential information about store managers, including a unique Manager_ID, Name, Username, Email, and Password. Managers possess the authority to manage categories and products, enabling them to add, edit, or delete entries.

- **Customers**: The Customers table contains customer profiles, with each entry featuring a unique Customer_ID, Name, Username, Email, and Password. It forms the foundation of our user accounts.

- **Categories**: In this table, we maintain information about various product categories. Each category is identified by a unique Category_ID and comes with a Category Name (Cat_name). The Category Manager_ID is linked as a foreign key, ensuring that only authorized managers can make modifications.

- **Products**: This table provides a comprehensive overview of our store's inventory. It includes Product_ID, Product_Name, Price, per_rate, Expiry_Date, Store_QTY, Picture, Availability, and Category_ID. These details allow us to efficiently manage our product listings.

- **Purchases**: The Purchases table tracks customer transactions, documenting crucial details such as Purchase_ID, Customer_ID, Category_ID, Product_ID, Quantity, and Total Price. It is the core of our order management system, facilitating the smooth processing of customer purchases.
