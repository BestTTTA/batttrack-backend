from fastapi import APIRouter, HTTPException
from module.database import users_collection
from basemodel.product_id import EndWorkUpdate  # Import the model


router = APIRouter(
    tags=["Product Management"],
    responses={404: {"description": "Not found"}}
)

@router.put("/update_product/{product_id}/end_work", status_code=200)
async def update_end_work(product_id: str, update_data: EndWorkUpdate):
    result = users_collection.update_one(
        {"list_product.product_id": product_id},
        {"$set": {"list_product.$.end_work": update_data.end_work}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product end_work updated successfully"}