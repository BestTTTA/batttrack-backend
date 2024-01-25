from fastapi import APIRouter, HTTPException
from module.database import users_collection
from basemodel.product_id import WorkerUpdateData
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    tags=["Product_id Services"],
    responses={404: {"description": "Not found"}}
)

@router.patch("/api/update_worker/{product_id}", status_code=200)
async def update_worker_data(product_id: str, worker_data: WorkerUpdateData):
    try:
        # Query to find the document that contains the product in its list_product
        document = users_collection.find_one({"list_product.product_id": product_id})
        if not document:
            raise HTTPException(status_code=404, detail="Product not found in list_product")

        # Find the specific product in the list_product
        product = next((prod for prod in document['list_product'] if prod['product_id'] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Check if 'workers' exists in product, if not, create it
        if 'workers' not in product:
            product['workers'] = []

        # Update or add worker data
        for i, worker in enumerate(product['workers']):
            if worker['worker_id'] == worker_data.worker_id:
                product['workers'][i] = worker_data.dict()
                break
        else:  # This else corresponds to the for loop
            product['workers'].append(worker_data.dict())

        # Update the document in the database
        users_collection.update_one({"list_product.product_id": product_id}, {"$set": {"list_product.$": product}})
        return {"message": "Worker data updated successfully in list_product"}

    except HTTPException as http_ex:
        # Directly re-raise HTTPExceptions without changing them
        raise http_ex
    except Exception as e:
        # Handle other exceptions
        logger.error(f"Error updating worker data in list_product: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
