from fastapi import APIRouter, HTTPException
from module.database import users_collection
from basemodel.product_id import ProductList  # Ensure this matches your data model
from pymongo.errors import BulkWriteError
from pymongo import UpdateOne

router = APIRouter(
    tags=["Product Management"],
    responses={404: {"description": "Not found"}}
)

@router.post("/add_product/")
async def add_product(list_product: ProductList):
    operations = []
    existing_product_ids = set()

    for product in list_product.list_product:
        if product.product_id in existing_product_ids or users_collection.find_one({"list_product.product_id": product.product_id}):
            raise HTTPException(status_code=400, detail=f"Product with ID {product.product_id} already exists")

        existing_product_ids.add(product.product_id)
        # Here, you're now adding the entire product object to the database
        operations.append(UpdateOne({"list_product.product_id": {"$ne": product.product_id}},
                                    {"$push": {"list_product": product.dict()}},
                                    upsert=True))

    if operations:
        try:
            users_collection.bulk_write(operations)
        except BulkWriteError as e:
            raise HTTPException(status_code=500, detail=str(e.details))

    return {"message": "Products added successfully"}
