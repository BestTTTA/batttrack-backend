from fastapi import FastAPI
from services import get_productID, get_product, register, login, add_product, createModelworker, endWorkupdate, stageWorkupdate, updataStageworker, updateStartworker, updateEndworker, getStagework, getendWork, get_worker_id
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

app.include_router(register.router)
app.include_router(login.router)
app.include_router(add_product.router)
app.include_router(createModelworker.router)
app.include_router(endWorkupdate.router)
app.include_router(stageWorkupdate.router)
app.include_router(updataStageworker.router)
app.include_router(updateStartworker.router)
app.include_router(updateEndworker.router)

app.include_router(get_productID.router)
app.include_router(get_product.router)
app.include_router(getStagework.router)
app.include_router(getendWork.router)

app.indlude_router(get_worker_id)

@app.get("/")
def read_root():
    return {"Hello": "World"}
