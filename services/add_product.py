from fastapi import APIRouter, HTTPException
from module.database import users_collection
from basemodel.product_id import ProductList

router = APIRouter(
    tags=["Product Management"],
    responses={404: {"description": "Not found"}}
)

@router.post("/add_product/")
async def add_product(list_product: ProductList):
    try:
        for product in list_product.list_product:
            # Check if product_id already exists
            if users_collection.find_one({"product_id": product.product_id}):
                raise HTTPException(status_code=400, detail=f"Product with ID {product.product_id} already exists")

            # Update the existing document by pushing the new product_id to list_product
            update_result = users_collection.update_one(
                {},
                {"$push": {"list_product": {"product_id": product.product_id}}}
            )
            
            # If the update did not match any documents, insert the first product_id
            if update_result.matched_count == 0:
                users_collection.insert_one({"list_product": [{"product_id": product.product_id}]})
        
        return {"message": "Products added successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
