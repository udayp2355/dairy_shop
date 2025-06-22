import pandas as pd
import numpy as np
import faker

# Initialize the Faker library for generating synthetic descriptions
fake = faker.Faker()

# Define the products and categories
product_names = ['Milk', 'Lassi', 'Ghee', 'Paneer', 'Shrikhand', 'Basundi', 'Cow Ghee', 'Amrkhand', 'ButterMilk', 'Dahi', 'Khawa', 'Kandhi Peda']
categories = product_names  # Each product name is also treated as a category here

# Function to generate specific ingredients based on product type
def generate_ingredients(product):
    base_ingredients = {
        'Milk': 'Milk',
        'Lassi': 'Milk, Sugar, Cardamom',
        'Ghee': 'Clarified Butter',
        'Paneer': 'Milk, Vinegar',
        'Shrikhand': 'Yogurt, Sugar, Saffron, Cardamom',
        'Basundi': 'Milk, Sugar, Nuts',
        'Cow Ghee': 'Cow Milk Butter',
        'Amrkhand': 'Yogurt, Mango, Sugar, Cardamom',
        'ButterMilk': 'Milk, Cultures, Salt',
        'Dahi': 'Milk, Live Cultures',
        'Khawa': 'Milk Solids',
        'Kandhi Peda': 'Milk, Sugar, Cardamom'
    }
    return base_ingredients.get(product, '')

# Generate a dataset with 5000 rows
num_rows = 5000
data = {
    'Product_ID': np.arange(1, num_rows + 1),
    'Product_Name': np.random.choice(product_names, num_rows),
    'Category': np.random.choice(categories, num_rows),
    'Description': [fake.sentence() for _ in range(num_rows)],
    'Ingredients': [generate_ingredients(product) for product in np.random.choice(product_names, num_rows)],
    'Price': np.random.uniform(1.0, 10.0, num_rows).round(2)
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('dairy_products_large.csv', index=False)

print("Large dataset generated and saved as 'dairy_products_large.csv'.")
