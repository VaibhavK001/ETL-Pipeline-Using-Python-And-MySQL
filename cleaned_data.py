import csv
import math
from datetime import datetime

INPUT_FILE = "raw_ecommerce_data.csv"
OUTPUT_FILE = "clean_ecommerce_data.csv"




def clean_text(value):
    """Remove extra spaces and convert empty values to None."""
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    return value


def clean_integer(value):
    """Convert a value to a positive integer."""
    value = clean_text(value)

    if value is None:
        return None

    try:
        number = int(value)

        if not math.isfinite(number) or number <= 0:
            return None

        return number

    except ValueError:
        return None


def clean_float(value):
    """Convert a value to a positive decimal number."""
    value = clean_text(value)

    if value is None:
        return None

    try:
        number = float(value)

        if not math.isfinite(number) or number <= 0:
            return None

        return round(number, 2)

    except ValueError:
        return None


def clean_date(value):
    """Validate date format YYYY-MM-DD."""
    value = clean_text(value)

    if value is None:
        return None

    try:
        date_obj = datetime.strptime(value, "%Y-%m-%d")
        return date_obj.strftime("%Y-%m-%d")

    except ValueError:
        return None



VALID_CATEGORIES = {
    "Electronics",
    "Accessories",
    "Home & Kitchen",
    "Bags",
    "Footwear",
    "Fashion"
}

VALID_PAYMENT_METHODS = {
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash on Delivery",
    "Net Banking"
}

VALID_ORDER_STATUS = {
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled",
    "Returned"
}



clean_rows = []
seen_order_ids = set()

duplicate_count = 0
invalid_count = 0


with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as file:

    reader = csv.DictReader(file)

    for row in reader:

      

        order_id = clean_text(row["order_id"])

        if order_id in seen_order_ids:
            duplicate_count += 1
            continue

        seen_order_ids.add(order_id)



        customer_id = clean_text(row["customer_id"])
        product = clean_text(row["product"])
        category = clean_text(row["category"])
        payment_method = clean_text(row["payment_method"])
        order_status = clean_text(row["order_status"])
        city = clean_text(row["city"])


     

        if category:
            category_mapping = {
                "electronics": "Electronics",
                "Electronics": "Electronics",
                "accessories": "Accessories",
                "Accessories": "Accessories",
                "fashion": "Fashion",
                "Fashion": "Fashion"
            }

            category = category_mapping.get(category, category)


        if payment_method:
            payment_mapping = {
                "upi": "UPI",
                "UPI": "UPI",
                "credit card": "Credit Card",
                "Credit Card": "Credit Card",
                "debit card": "Debit Card",
                "Debit Card": "Debit Card",
                "cash on delivery": "Cash on Delivery",
                "Cash on Delivery": "Cash on Delivery",
                "net banking": "Net Banking",
                "Net Banking": "Net Banking"
            }

            payment_method = payment_mapping.get(
                payment_method,
                payment_method
            )


        if order_status:
            status_mapping = {
                "deliverd": "Delivered",
                "Delivered": "Delivered",
                "Shipped": "Shipped",
                "Processing": "Processing",
                "Cancelled": "Cancelled",
                "Returned": "Returned"
            }

            order_status = status_mapping.get(
                order_status,
                order_status
            )



        order_date = clean_date(row["order_date"])


     

        quantity = clean_integer(row["quantity"])

        unit_price = clean_float(row["unit_price"])

        total_amount = clean_float(row["total_amount"])


      

        if category not in VALID_CATEGORIES:
            category = None

        if payment_method not in VALID_PAYMENT_METHODS:
            payment_method = None

        if order_status not in VALID_ORDER_STATUS:
            order_status = None


   

        if quantity is not None and unit_price is not None:

            calculated_total = round(
                quantity * unit_price,
                2
            )

            total_amount = calculated_total

        else:
            total_amount = None


      

        if order_id is None:
            invalid_count += 1
            continue

        if customer_id is None:
            invalid_count += 1
            continue

        if product is None:
            invalid_count += 1
            continue

        if order_date is None:
            invalid_count += 1
            continue

        if quantity is None:
            invalid_count += 1
            continue

        if unit_price is None:
            invalid_count += 1
            continue



        clean_row = {
            "order_id": order_id,
            "order_date": order_date,
            "customer_id": customer_id,
            "product": product,
            "category": category,
            "quantity": quantity,
            "unit_price": f"{unit_price:.2f}",
            "total_amount": f"{total_amount:.2f}",
            "payment_method": payment_method,
            "order_status": order_status,
            "city": city
        }

        clean_rows.append(clean_row)




fieldnames = [
    "order_id",
    "order_date",
    "customer_id",
    "product",
    "category",
    "quantity",
    "unit_price",
    "total_amount",
    "payment_method",
    "order_status",
    "city"
]


with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(clean_rows)



print("===== DATA CLEANING SUMMARY =====")

print("Raw records      :", len(seen_order_ids))
print("Duplicate records:", duplicate_count)
print("Invalid records  :", invalid_count)
print("Clean records    :", len(clean_rows))

print("\nClean file created:")
print(OUTPUT_FILE)
