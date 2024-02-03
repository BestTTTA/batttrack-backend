from fastapi import APIRouter, HTTPException
from module.database import users_collection
from basemodel.product_id import ProductList  # Ensure this matches your data model
from pymongo.errors import BulkWriteError
from pymongo import UpdateOne

router = APIRouter(
    tags=["Product Management"], responses={404: {"description": "Not found"}}
)

@router.post("/add_product/")
async def add_product(list_product: ProductList):
    operations = []
    existing_product_ids = set()
    added_products = [] 

    for product in list_product.list_product:
        product_data = product.dict()  
        existing_product = users_collection.find_one(
            {"list_product.product_id": product.product_id}
        )
        if product.product_id in existing_product_ids or existing_product:
            duplicate_product_data = existing_product['list_product'][0] if existing_product and 'list_product' in existing_product else product_data
            return { 
                "added_products": duplicate_product_data 
            }

        existing_product_ids.add(product.product_id)
        operations.append(
            UpdateOne(
                {"list_product.product_id": {"$ne": product.product_id}},
                {"$push": {"list_product": product_data}},
                upsert=True,
            )
        )
        added_products.append(product_data)  # Add product data to the list

    if operations:
        try:
            users_collection.bulk_write(operations)
        except BulkWriteError as e:
            raise HTTPException(status_code=500, detail=str(e.details))

    return {
        "added_products": added_products  # Return the details of added products
    }
