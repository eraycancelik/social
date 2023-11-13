from fastapi import FastAPI
from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
import json
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)


# Base.metadata.create_all(bind=engine)

# Her Post işleminde status_code=201 ile 201 kodu döndürülür.
# BaseModel: Pydantic kütüphanesinden gelen bir sınıf. Pydantic, veri doğrulama ve serielleştirme için kullanılır.
# BaseModel sınıfından türetilen sınıflar, Pydantic tarafından otomatik olarak doğrulanır ve serielleştirilir.
# Pydantic, veri doğrulama ve serielleştirme için kullanılır.


# BaseModal post edilen verilerin doğruluğunu kontrol eder.
# Post ise post edilen verileri tutar.
app = FastAPI()


class Product(BaseModel):
    product_name: str
    product_price: float
    product_photo_url: str
    product_category: str


while True:
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="159632159",
            cursor_factory=RealDictCursor,
        )
        cursor = connection.cursor()
        print("Veritabanına bağlanıldı.")
        break
    except Exception as error:
        print("Veritabanına bağlanılamadı.")
        print("Hata:")
        print(str(error))
        time.sleep(2)


@app.get("/")
def say_hi():
    return {"message": "server is running"}


@app.get("/sqlalchemy")
def get_sqlalchemy(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    # db.query(models.Product) -> SELECT * FROM products
    return {"data": products}




@app.get("/products")
def get_latest():
    cursor.execute("""SELECT * FROM products""")
    products = cursor.fetchall()
    return {"products": products}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    cursor.execute("""SELECT * FROM products WHERE id=%s""", (product_id,))
    product = cursor.fetchone()
    if not product:
        raise HTTPException(
            status_code=404, detail=f"Product with id:{product_id} was not found"
        )
    return {"product": product}


# Her Post işleminde status_code=201 ile 201 kodu döndürülür.
@app.post("/products", status_code=201)
def create_product(post: Product):
    cursor.execute(
        """INSERT INTO products(name,price,photo_url,category) VALUES (%s,%s,%s,%s) RETURNING *""",
        (post.name, post.price, post.photo_url, post.category),
    )
    new_product = cursor.fetchone()
    connection.commit()
    return {"data": new_product}


@app.put("/products/{product_id}")
def update_product(product_id: int, post: Product):
    cursor.execute("""SELECT * FROM products WHERE id=%s""", (product_id,))
    product = cursor.fetchone()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id:{product_id} was not found",
        )
    cursor.execute(
        """UPDATE products SET name=%s,price=%s,photo_url=%s,category=%s WHERE id=%s RETURNING *""",
        (post.name, post.price, post.photo_url, post.category, product_id),
    )
    updated_product = cursor.fetchone()
    connection.commit()
    return {"data": updated_product}


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    cursor.execute("""SELECT * FROM products WHERE id=%s""", (product_id,))
    product = cursor.fetchone()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id:{product_id} was not found",
        )
    cursor.execute("""DELETE FROM products WHERE id=%s""", (product_id,))
    connection.commit()
    return {"data": f"Product with id:{product_id} was deleted successfully"}
