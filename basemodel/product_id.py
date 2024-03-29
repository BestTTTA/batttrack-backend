from pydantic import BaseModel, constr
from typing import List

class Product(BaseModel):
    product_id: str
    start_work: str
    end_work: str
    stage_work: int
    
class ProductList(BaseModel):
    list_product: List[Product]

class WorkerUpdateData(BaseModel):
    worker_id: str
    user_name: str
    stage_work: int  
    start_work: str
    
class EndWorkUpdate(BaseModel):
    end_work: str
    
class StageWorkUpdate(BaseModel):
    stage_work: int
    
class StartWorkUpdate(BaseModel):
    start_work: constr(strict=True)