from fastapi import APIRouter, HTTPException
from module.database import users_collection
from basemodel.product_id import StartWorkUpdate  # Make sure to import this correctly

router = APIRouter(
    tags=["Worker Management"],
    responses={404: {"description": "Not found"}}
)

@router.put("/update_worker/{product_id}/{worker_id}/start_work", status_code=200)
async def update_worker_start_work(product_id: str, worker_id: str, update_data: StartWorkUpdate):
    # Find the specific worker within the product and check if start_work is a string
    worker_query = {
        "list_product.product_id": product_id,
        "list_product.workers.worker_id": worker_id,
        "list_product.workers.start_work": {"$type": "string"}
    }

    # Prepare the update
    update = {
        "$set": {
            "list_product.$.workers.$[worker].start_work": update_data.start_work
        }
    }
    array_filters = [{"worker.worker_id": worker_id}]
    result = users_collection.update_one(worker_query, update, array_filters=array_filters)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Worker not found or start_work is not a string")

    return {"message": "Worker's start_work updated successfully"}
