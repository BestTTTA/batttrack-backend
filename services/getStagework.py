from fastapi import APIRouter, HTTPException
from module.database import users_collection

router = APIRouter(
    tags=["Product Management"],
    responses={404: {"description": "Not found"}}
)

@router.get("/get_product/{product_id}/stage_work", status_code=200)
async def get_stage_work(product_id: str):
    # Retrieve the stage_work for the specified product_id
    product = users_collection.find_one(
        {"list_product.product_id": product_id},
        {"list_product.$": 1}
    )

    if product is None or 'list_product' not in product or len(product['list_product']) == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    stage_work = product['list_product'][0]['stage_work']

    return {"product_id": product_id, "stage_work": stage_work}
