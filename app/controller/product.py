from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.product import Product as ProductModel
from app.schemas.product import ProductCreate as SchemaProductCreate


def get_list_product(db: Session, skip: int = 0, limit: int = 100) -> List[ProductModel]:
    """get list of product from db"""
    return db.query(ProductModel).offset(skip).limit(limit).all()


def create_product(db: Session, product: SchemaProductCreate) -> ProductModel:
    """create product and save it to db"""
    db_product = ProductModel(
        title=product.title, description=product.description, stocks=product.stocks
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Optional[ProductModel]:
    """get one product from db"""
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def update_product(db: Session, product_id: int, product: SchemaProductCreate) -> Optional[ProductModel]:
    """update product and save it db"""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        for column, value in product.dict(exclude_unset=True).items():
            setattr(db_product, column, value)
        db.commit()
    return db_product
