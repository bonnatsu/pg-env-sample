from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_conn

app = FastAPI()
class StockInRequest(BaseModel):
    id: int
    quantity: int

@app.post("/stock/in")
def stock_in(req: StockInRequest):

    if req.quantity <= 0:
        raise HTTPException(status_code=400,detail="quantity must be > 0")
    
    conn = get_conn()
    cur = conn.cursor()


    try:
        cur.execute(
            "SELECT 1 FROM products WHERE id = %s",
            (req.id,)
        )
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="product not found")
        
        cur.execute(
            "SELECT quantity FROM stocks WHERE product_id = %s FOR UPDATE",
            (req.id,)
        )
        row = cur.fetchone()

        if row is None:
            #在庫なければ作る
            cur.execute(
                "INSERT INTO stocks (product_id,quantity) VALUES (%s,%s)",
                (req.id,req.quantity)
            )
            new_qty = req.quantity
        else:
            cur.execute(
                "UPDATE stocks SET quantity = quantity + %s WHERE product_id = %s",
                (req.quantity,req.id)
            )
            new_qty = row[0] + req + req.quantity
        
        conn.commit()

        return {
            "id": req.id,
            "quantity": req.quantity
        }
    
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        cur.close()
        conn.close()
