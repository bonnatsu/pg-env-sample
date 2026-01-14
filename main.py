from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_conn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

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
            "SELECT product_name FROM products WHERE id = %s",
            (req.id,)
        )
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="product not found")
        
        product_name = row[0]
        
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
            new_qty = row[0] + req.quantity
        
        conn.commit()

        return {
            "id": req.id,
            "product_name":product_name,
            "quantity": req.quantity,
            "message": f"商品名:{product_name} 入庫完了"
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

templates = Jinja2Templates(directory="templates")

@app.get("/stock/in-page", response_class=HTMLResponse)
def stock_in_page(request: Request):
    return templates.TemplateResponse(
        "stock_in.html",
        {"request": request}
    )