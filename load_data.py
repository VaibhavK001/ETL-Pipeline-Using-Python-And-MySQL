import csv
import mysql.connector


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vk111",
    database="ecommerce_pipeline"
)

cursor = connection.cursor()


sql = """
    INSERT INTO orders (
        order_id,
        order_date,
        customer_id,
        product,
        category,
        quantity,
        unit_price,
        total_amount,
        payment_method,
        order_status,
        city
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


with open("clean_ecommerce_data.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    count = 0

    
    for row in reader:

        values = (
            row["order_id"],
            row["order_date"],
            row["customer_id"],
            row["product"],
            row["category"],
            row["quantity"],
            row["unit_price"],
            row["total_amount"],
            row["payment_method"],
            row["order_status"],
            row["city"]
        )

        
        cursor.execute(sql, values)

        count += 1



connection.commit()

print(count, "records loaded successfully!")


cursor.close()
connection.close()