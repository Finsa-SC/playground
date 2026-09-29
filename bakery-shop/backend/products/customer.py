from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.helper import transaction

router = APIRouter(prefix="/products", tags=["Products"])

class BuyRequest(BaseModel):
    count: int = 1

@router.get("/")
def get_all_products():
    with transaction() as db:
        query = """
            SELECT id, product_name, price, stock, description, created_at 
            FROM products 
            WHERE deleted_at IS NULL
            ORDER BY id ASC;
        """
        products = db.execute_query(query)
        return {"data": products}

@router.get("/popular")
def get_popular_products():
    with transaction() as db:
        query = """
            SELECT 
                p.id,
                p.product_name,
                p.price,
                p.stock,
                COALESCE(SUM(t.count), 0) AS total_sold
            FROM products p
            JOIN transactions t ON p.id = t.product_id
            WHERE 
                t.created_at >= NOW() - INTERVAL '1 month'
                AND p.deleted_at IS NULL
            GROUP BY p.id, p.product_name, p.price, p.stock
            ORDER BY total_sold DESC
            LIMIT 10;
        """
        popular_products = db.execute_query(query)
        return {"data": popular_products}

# Endpoint: Ambil 1 Produk Berdasarkan ID
@router.get("/{product_id}")
def get_product_by_id(product_id: int):
    with transaction() as db:
        query = """
            SELECT id, product_name, price, stock, description, created_at 
            FROM products 
            WHERE id = %s AND deleted_at IS NULL;
        """
        product = db.execute_query(query, (product_id,))

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produk tidak ditemukan"
            )

        return {"data": product[0]}
# Endpoint: Beli Produk Berdasarkan ID dan Count

@router.post("/{product_id}/buy")
def buy_product(product_id: int, payload: BuyRequest):
    if payload.count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Jumlah pembelian harus lebih dari 0"
        )

    with transaction() as db:
        # Step A: Cek ketersediaan stok & ambil harga produk saat ini
        check_query = """
            SELECT price, stock 
            FROM products 
            WHERE id = %s AND deleted_at IS NULL 
            FOR UPDATE;
        """
        product = db.execute_query(check_query, (product_id,))

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produk tidak ditemukan"
            )

        current_price = product[0]["price"]
        current_stock = product[0]["stock"]

        # Validasi kecukupan stok
        if current_stock < payload.count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stok tidak cukup. Stok tersisa: {current_stock}"
            )

        # Step B: Kurangi stok di tabel products
        update_stock_query = """
            UPDATE products 
            SET stock = stock - %s 
            WHERE id = %s;
        """
        db.execute_non_query(update_stock_query, (payload.count, product_id))

        # Step C: Hitung total harga & Insert catatan ke tabel transactions
        total_price = current_price * payload.count
        insert_tx_query = """
            INSERT INTO transactions (product_id, count, price) 
            VALUES (%s, %s, %s) 
            RETURNING id;
        """
        tx_id = db.execute_scalar(insert_tx_query, (product_id, payload.count, total_price))

        return {
            "message": "Pembelian berhasil!",
            "transaction_id": tx_id,
            "product_id": product_id,
            "qty": payload.count,
            "total_price": total_price
        }