from fastapi import APIRouter, HTTPException
from module.database import users_collection
from bson import json_util
import json

router = APIRouter(
    tags=["Product Services"],
    responses={404: {"description": "Not found"}}
)

@router.get("/products/")
async def get_all_products():
    try:
        # Fetch only the list_product field from all documents in the collection
        products_cursor = users_collection.find({}, {"_id": 0, "list_product": 1})

        all_products = []

        for document in products_cursor:
            # Some documents might not have a list_product field
            if 'list_product' in document:
                for product in document['list_product']:
                    json_data = json.loads(json_util.dumps(product))
                    all_products.append(json_data)


        return all_products
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
