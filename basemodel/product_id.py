from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    product_id: str

class ProductList(BaseModel):
    list_product: List[Product]

class WorkerUpdateData(BaseModel):
    worker_id: str
    user_name: str
    stage_work: str
    holding_time: str   
    start_work: str
    end_work: str   