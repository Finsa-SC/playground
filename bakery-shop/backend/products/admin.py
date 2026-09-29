from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from db.helper import transaction

router = APIRouter(prefix="/admin/products", tags=["Admin Products"])


# Schema untuk Create Product
class ProductCreate(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    description: Optional[str] = None


# Schema untuk Patch/Update Product (semua field bersifat opsional)
class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None


# 1. READ ALL (Admin View: bisa melihat produk yang sudah terhapus juga)
@router.get("/")
def get_all_products_admin(include_deleted: bool = False):
    with transaction() as db:
        query = """
            SELECT id, product_name, price, stock, description, created_at, deleted_at 
            FROM products
        """
        if not include_deleted:
            query += " WHERE deleted_at IS NULL"

        query += " ORDER BY id ASC;"
        products = db.execute_query(query)
        return {"data": products}


# 2. CREATE (Tambah Produk Baru)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate):
    with transaction() as db:
        query = """
            INSERT INTO products (product_name, price, stock, description)
            VALUES (%s, %s, %s, %s)
            RETURNING id, product_name, price, stock, description, created_at;
        """
        new_product = db.execute_query(
            query,
            (payload.product_name, payload.price, payload.stock, payload.description)
        )
        return {
            "message": "Produk berhasil ditambahkan",
            "data": new_product[0]
        }


# 3. PATCH (Update Parsial Produk)
@router.patch("/{product_id}")
def update_product(product_id: int, payload: ProductUpdate):
    # Cek apakah setidaknya ada 1 field yang dikirim untuk di-update
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tidak ada data yang dikirim untuk diperbarui"
        )

    with transaction() as db:
        # COALESCE digunakan agar jika value %s adalah NULL, dia tetap memakai nilai lama dari kolom
        query = """
            UPDATE products 
            SET 
                product_name = COALESCE(%s, product_name),
                price = COALESCE(%s, price),
                stock = COALESCE(%s, stock),
                description = COALESCE(%s, description)
            WHERE id = %s AND deleted_at IS NULL
            RETURNING id, product_name, price, stock, description, created_at;
        """
        updated_product = db.execute_query(
            query,
            (
                payload.product_name,
                payload.price,
                payload.stock,
                payload.description,
                product_id
            )
        )

        if not updated_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produk tidak ditemukan atau sudah terhapus"
            )

        return {
            "message": "Produk berhasil diperbarui",
            "data": updated_product[0]
        }


# 4. DELETE (Soft Delete: Mengisi deleted_at)
@router.delete("/{product_id}")
def delete_product(product_id: int):
    with transaction() as db:
        query = """
            UPDATE products 
            SET deleted_at = CURRENT_TIMESTAMP 
            WHERE id = %s AND deleted_at IS NULL
            RETURNING id;
        """
        deleted_product = db.execute_scalar(query, (product_id,))

        if not deleted_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produk tidak ditemukan atau sudah dihapus sebelumnya"
            )

        return {"message": f"Produk dengan ID {product_id} berhasil di-soft delete"}