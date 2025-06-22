from models.database import db, Product
from app import create_app
import os

def update_image_links():
    app = create_app()
    with app.app_context():
        products = Product.query.all()
        updated = 0
        for product in products:
            if product.image and product.image.startswith('images/'):
                product.image = product.image.replace('images/', '', 1)
                updated += 1
        db.session.commit()
        print(f'Updated {updated} product image links.')

if __name__ == '__main__':
    update_image_links() 