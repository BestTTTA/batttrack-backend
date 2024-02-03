from fastapi import APIRouter, HTTPException
from module.database import users_collection
from basemodel.product_id import WorkerUpdateData

router = APIRouter(
    tags=["CreateWorkermodel Authentication"],
    responses={404: {"description": "Not found"}}
)

@router.put("/update_worker/{product_id}/worker_model", status_code=200)
async def update_worker_model(product_id: str, worker_data: WorkerUpdateData):
    try:
        document = users_collection.find_one({"list_product.product_id": product_id})
        if not document:
            raise HTTPException(status_code=404, detail="Product not found in list_product")

        product = next((prod for prod in document['list_product'] if prod['product_id'] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        worker_updated = False
        for worker in product.get('workers', []):
            if worker['worker_id'] == worker_data.worker_id:
                if 'stage_work' in worker and worker['stage_work']:
                    raise HTTPException(status_code=400, detail="Stage work can only be set once per worker")
                if 'start_work' in worker and worker['start_work']:
                    raise HTTPException(status_code=400, detail="Start work can only be set once per worker")
                worker.update(worker_data.dict())
                worker_updated = True
                break

        if not worker_updated:
            # Append new worker if not found
            product.setdefault('workers', []).append(worker_data.dict())

        users_collection.update_one({"list_product.product_id": product_id}, {"$set": {"list_product.$": product}})
        return {"message": "Worker data updated successfully in list_product"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
