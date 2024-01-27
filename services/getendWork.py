from fastapi import APIRouter, HTTPException
from module.database import users_collection

router = APIRouter(
    tags=["Product Management"],
    responses={404: {"description": "Not found"}}
)

@router.get("/get_product/{product_id}/end_work", status_code=200)
async def get_end_work(product_id: str):
    product = users_collection.find_one(
        {"list_product.product_id": product_id},
        {"list_product.$": 1}
    )

    if product is None or 'list_product' not in product or len(product['list_product']) == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    end_work = product['list_product'][0].get('end_work')

    if end_work is None:
        raise HTTPException(status_code=404, detail="End work data not found for the product")

    return {"product_id": product_id, "end_work": end_work}
