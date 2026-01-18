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
        row = cur.fetchone()
        if row is None:
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
            "current_quantity": new_qty,
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



@app.post("/stock/out")
def stock_out(req: StockInRequest):

    if req.quantity <= 0:
        raise HTTPException(status_code=400,detail="quantity must be > 0")
    
    conn = get_conn()
    cur = conn.cursor()


    try:
        cur.execute(
            "SELECT product_name FROM products WHERE id = %s",
            (req.id,)
        )
        row = cur.fetchone()
        if row is None:
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
                "UPDATE stocks SET quantity = quantity - %s,updated_at = now() WHERE product_id = %s",
                (req.quantity,req.id)
            )
            new_qty = row[0] - req.quantity
        
        conn.commit()

        return {
            "id": req.id,
            "product_name":product_name,
            "quantity": req.quantity,
            "current_quantity": new_qty,
            "message": f"商品名:{product_name} 出庫完了"
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

@app.get("/stock/out-page", response_class=HTMLResponse)
def stock_out_page(request: Request):
    return templates.TemplateResponse(
        "stock_out.html",
        {"request": request}
    )

@app.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/stock/list")
def stock_list():
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                p.id AS product_id,
                p.product_name,
                COALESCE(SUM(s.quantity), 0) AS quantity
            FROM products p
            LEFT JOIN stocks s
                ON p.id = s.product_id
            GROUP BY
                p.id, p.product_name
            ORDER BY
                p.id
        """)

        rows = cur.fetchall()

        return [
            {
                "product_id": r[0],
                "product_name": r[1],
                "quantity": r[2]
            }
            for r in rows
        ]

    finally:
        cur.close()
        conn.close()

templates = Jinja2Templates(directory="templates")

@app.get("/stock/list-page", response_class=HTMLResponse)
def stock_list_page(request: Request):
    return templates.TemplateResponse(
        "stock_list.html",
        {"request": request}
    )