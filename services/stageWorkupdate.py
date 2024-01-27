from fastapi import APIRouter, HTTPException
from module.database import users_collection
from basemodel.product_id import StageWorkUpdate  

router = APIRouter(
    tags=["Product Management"],
    responses={404: {"description": "Not found"}}
)

@router.put("/update_product/{product_id}/stage_work", status_code=200)
async def update_stage_work(product_id: str, update_data: StageWorkUpdate):
    # Update the stage_work
    result = users_collection.update_one(
        {"list_product.product_id": product_id},
        {"$set": {"list_product.$.stage_work": update_data.stage_work}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    # Retrieve the updated stage_work
    updated_product = users_collection.find_one(
        {"list_product.product_id": product_id},
        {"list_product.$": 1}
    )

    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found after update")

    updated_stage_work = updated_product['list_product'][0]['stage_work']

    return {"message": "Product stage_work updated successfully", "stage_work": updated_stage_work}
