from datetime import datetime, timedelta
from decimal import Decimal
import uuid
import logging

from sqlalchemy.orm import Session
from models.users import User
from models.address import Address
from models.channel import Channel
from models.categories import Category
from models.products import ProductType, Product, ProductVariant
from models.tax import TaxClass, TaxClassCountryRate
from models.shipping import ShippingZone, ShippingMethod
from models.stock import Warehouse
from models.order import Order

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def seed_database(db: Session):
    try:
        # 1. Create base data
        logger.info("Creating admin user...")
        admin_user = User(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyDAQn1Zd.4Km2",  # 'password'
            is_staff=True,
            is_active=True,
            is_superuser=True,
            date_joined=datetime.utcnow()
        )
        db.add(admin_user)
        db.flush()
        logger.info("Admin user created successfully")

        # 2. Create addresses
        logger.info("Creating warehouse address...")
        warehouse_address = Address(
            street_address_1="123 Warehouse St",
            city="Storage City",
            country="US",
            postal_code="12345",
            created_by=admin_user.id
        )
        db.add(warehouse_address)
        db.flush()
        logger.info("Warehouse address created successfully")

        # 3. Create channel
        logger.info("Creating main channel...")
        main_channel = Channel(
            name="Main Store",
            slug="main-store",
            currency_code="USD",
            default_country="US",
            is_active=True,
            created_by=admin_user.id
        )
        db.add(main_channel)
        logger.info("Main channel created successfully")

        # 4. Create tax classes
        logger.info("Creating tax classes...")
        standard_tax = TaxClass(
            name="Standard Rate",
            created_by=admin_user.id
        )
        db.add(standard_tax)
        db.flush()

        tax_rate_us = TaxClassCountryRate(
            tax_class_id=standard_tax.id,
            country="US",
            rate=Decimal("0.0725"),
            created_by=admin_user.id
        )
        db.add(tax_rate_us)
        logger.info("Tax classes created successfully")

        # 5. Create categories
        logger.info("Creating categories...")
        electronics = Category(
            name="Electronics",
            slug="electronics",
            created_by=admin_user.id
        )
        db.add(electronics)
        db.flush()

        phones = Category(
            name="Phones",
            slug="phones",
            parent_id=electronics.id,
            created_by=admin_user.id
        )
        db.add(phones)
        db.flush()
        logger.info("Categories created successfully")

        # 6. Create product types
        logger.info("Creating product types...")
        phone_type = ProductType(
            name="Smartphone",
            slug="smartphone",
            has_variants=True,
            is_shipping_required=True,
            tax_class_id=standard_tax.id,
            created_by=admin_user.id
        )
        db.add(phone_type)
        db.flush()
        logger.info("Product types created successfully")

        # 7. Create products and variants
        logger.info("Creating products and variants...")
        iphone = Product(
            name="iPhone 15",
            slug="iphone-15",
            product_type_id=phone_type.id,
            category_id=phones.id,
            tax_class_id=standard_tax.id,
            created_by=admin_user.id
        )
        db.add(iphone)
        db.flush()

        iphone_variant = ProductVariant(
            sku="IPH-15-128",
            name="iPhone 15 128GB",
            product_id=iphone.id,
            created_by=admin_user.id
        )
        db.add(iphone_variant)
        db.flush()

        # Update product with default variant
        iphone.default_variant_id = iphone_variant.id
        db.add(iphone)
        logger.info("Products and variants created successfully")

        # 8. Create warehouse
        logger.info("Creating warehouse...")
        main_warehouse = Warehouse(
            name="Main Warehouse",
            code="MAIN-01",
            address_id=warehouse_address.id,
            created_by=admin_user.id
        )
        db.add(main_warehouse)
        logger.info("Warehouse created successfully")

        # 9. Create shipping zones and methods
        logger.info("Creating shipping zones and methods...")
        us_zone = ShippingZone(
            name="United States",
            default=True,
            created_by=admin_user.id
        )
        db.add(us_zone)
        db.flush()

        standard_shipping = ShippingMethod(
            name="Standard Shipping",
            type="price_based",
            shipping_zone_id=us_zone.id,
            minimum_order_price_amount=Decimal("0.00"),
            maximum_order_price_amount=Decimal("1000.00"),
            created_by=admin_user.id
        )
        db.add(standard_shipping)
        logger.info("Shipping zones and methods created successfully")

        # 10. Create a sample order
        logger.info("Creating sample customer and order...")
        customer = User(
            email="customer@example.com",
            first_name="John",
            last_name="Doe",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyDAQn1Zd.4Km2",
            is_active=True,
            date_joined=datetime.utcnow(),
            created_by=admin_user.id
        )
        db.add(customer)
        db.flush()

        customer_address = Address(
            first_name="John",
            last_name="Doe",
            street_address_1="456 Customer St",
            city="Buyerville",
            country="US",
            postal_code="67890",
            created_by=customer.id
        )
        db.add(customer_address)
        db.flush()

        order = Order(
            number=1001,
            status="UNFULFILLED",
            user_id=customer.id,
            billing_address_id=customer_address.id,
            shipping_address_id=customer_address.id,
            channel_id=main_channel.id,
            shipping_method_id=standard_shipping.id,
            collection_point_id=main_warehouse.id,
            currency="USD",
            created_by=customer.id
        )
        db.add(order)
        logger.info("Sample customer and order created successfully")

        # Commit all changes
        logger.info("Committing all changes to database...")
        db.commit()
        logger.info("Database seeding completed successfully!")

    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        db.rollback()
        raise