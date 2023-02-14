from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.controller import product as controller
from app.db.session import get_db
from app.schemas import product as schemas
from app.models.product import Product as ProductModel

router = APIRouter()


@router.get("/product", tags=["product"], response_model=List[schemas.Product])
def product_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[ProductModel]:
    products = controller.get_list_product(db, skip=skip, limit=limit)
    return products


@router.post("/product", tags=["product"])
def product_create(product: schemas.ProductCreate, db: Session = Depends(get_db)) -> JSONResponse:
    controller.create_product(db=db, product=product)
    return JSONResponse(content={"message": "product created"})


@router.get("/product/{product_id}", tags=["product"], response_model=schemas.Product)
def product_detail(product_id: int, db: Session = Depends(get_db)) -> ProductModel:
    db_product = controller.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/product/{product_id}", tags=["product"])
def product_update(
    product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)
) -> JSONResponse:
    db_product = controller.update_product(db, product=product, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return JSONResponse(content={"message": "product updated"})
