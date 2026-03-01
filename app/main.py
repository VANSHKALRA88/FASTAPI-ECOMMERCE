from fastapi import FastAPI , HTTPException , Query 
from app.service.products import get_all_products , add_product , remove_product
from fastapi import Path
from uuid import uuid4 , UUID
from app.schema.products import Product
from datetime import datetime



app=FastAPI()


@app.get("/products")
def get_products():
    return get_all_products()

@app.get("/products")
def list_products(name:str=Query(
    default=None,
    min_length=1,
    max_length=50,
    description="Search product by name(case insensitive)",
    ),
    sort_by_price:bool=Query(default=False,Description="SORT PRODUCTS BY PRICE"),
        order:str=Query(default="asc",Description="SORT ORDER WHEN SORT_BY_PRICE=TRUE(ASC,DESC)"),
        limit:int=Query(
            default=10,
            ge=1,
            le=100,
            description="Number of items to return",
    ),
    offset:int=Query(
            default=0,
            ge=0,
            description="Pagination off set",
    ),
    
):
    products=get_all_products()
    if name:
        needle=name.strip().lower()
        products=[p for p in products if needle in p.get("name", "").lower()]

        if not products:
            raise HTTPException(status_code=404, detail=f"No product found with this name={name}")
        
    if sort_by_price:
        reverse=order=="desc"
        products=sorted(products,key=lambda p:p.get("price",0),reverse=reverse)
    
    
    total=len(products)
    products=products[offset:offset+limit]


    return {"total":total,"limit":limit,"items":products}

@app.get("/products/{product_id}")
def get_product_by_id(product_id:str=Path(...,min_length=1,max_length=36,description="UUID OF PRODUCTS",examples=111)):
    products=get_all_products()
    for product in products:
        if product["id"]==product_id:
            return product

    raise HTTPException(status_code=404,detail="Product not found")


@app.post("/products",status_code=201)
def create_product(product:Product):
    product_dict=product.model_dump(mode="json")
    product_dict["id"]=str(uuid4())
    product_dict["created_at"]=datetime
    try:
        add_product(product_dict)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return product.model_dump(mode="json")


@app.put("/products",status_code=201)
def update_product(product:Product):
    product_dict=product.model_dump(mode="json")
    product_dict["id"]=str(uuid4())
    product_dict["created_at"]=datetime
    try:
        add_product(product_dict)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return product.model_dump(mode="json")

@app.delete("/products/{product_id}")
def delete_product(product_id:int=Path(...,description="Product ID")
):
    try:
        res=remove_product(product_id)

        return res

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
