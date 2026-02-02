# Fake data generator for Argos store for its Retail Sales Data Pipeline

import pandas as pd
from faker import Faker
import random

fake = Faker()

stores = ['Hendon', 'Mill Hill', 'Barnet', 'Penge', 'Southgate']
product_categories = ['Electronics', 'Clothings',
                      'Body Care', 'Dental Care', 'Hair Care']


# creating the random data

sales_data = []

for _ in range(1000000):
    customer_name = fake.name()
    quantity = random.randint(1, 10)
    product_price = round(random.uniform(5.00, 500.00), 2)
    total_amount = round(quantity*product_price, 2)
    sales_location = random.choice(stores)
    sales_category = random.choice(product_categories)
    sales_date = fake.date_this_year()

    sales_transaction = {
        "customer_name": customer_name,
        "store": sales_location,
        "category": sales_category,
        "quantity": quantity,
        "product_price": product_price,
        "total_amount": total_amount,
        "date": sales_date
    }

    sales_data.append(sales_transaction)

# creating the dataframe
df = pd.DataFrame(sales_data)
df.to_csv('sales_data.csv', index=False)

print("Sales data generated and saved to sales_data.csv")


