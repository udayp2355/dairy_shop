from app import create_app
from models.database import db, Product

# Create the Flask app and push the context
app = create_app()

with app.app_context():
    products = Product.query.all()
    updated_count = 0
    for product in products:
        if product.image.startswith('images/'):
            old_image = product.image
            product.image = product.image[len('images/'):]
            print(f"Updated: {old_image} -> {product.image}")
            updated_count += 1
    if updated_count > 0:
        db.session.commit()
        print(f"\n{updated_count} product(s) updated.")
    else:
        print("No products needed updating.") 