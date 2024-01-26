from pydantic import BaseModel, constr
from typing import List

class Product(BaseModel):
    product_id: str
    start_work: str
    end_work: str
    stage_work: str
    
class ProductList(BaseModel):
    list_product: List[Product]

class WorkerUpdateData(BaseModel):
    worker_id: str
    user_name: str
    stage_work: str
    holding_time: str   
    start_work: str
    end_work: str   
    
class EndWorkUpdate(BaseModel):
    end_work: str
    
class StageWorkUpdate(BaseModel):
    stage_work: str
    
class StartWorkUpdate(BaseModel):
    start_work: constr(strict=True)