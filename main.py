from fastapi import FastAPI
from services import add_user_inproduct, get_productID, get_product, register, login, add_product
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(add_user_inproduct.router)
app.include_router(get_productID.router)
app.include_router(get_product.router)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(add_product.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
