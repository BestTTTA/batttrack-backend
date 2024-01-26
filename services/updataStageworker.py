from fastapi import APIRouter, HTTPException
from module.database import users_collection
from basemodel.product_id import StageWorkUpdate  # Ensure this is correctly imported

router = APIRouter(
    tags=["Worker Management"],
    responses={404: {"description": "Not found"}}
)

@router.put("/update_worker/{product_id}/{worker_id}/stage_work", status_code=200)
async def update_worker_stage_work(product_id: str, worker_id: str, update_data: StageWorkUpdate):
    query = {
        "list_product.product_id": product_id,
        "list_product.workers.worker_id": worker_id
    }
    update = {
        "$set": {
            "list_product.$.workers.$[worker].stage_work": update_data.stage_work
        }
    }
    array_filters = [{"worker.worker_id": worker_id}]
    result = users_collection.update_one(query, update, array_filters=array_filters)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Worker or Product not found")

    return {"message": "Worker's stage_work updated successfully"}
