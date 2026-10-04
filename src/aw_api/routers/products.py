from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session
from sqlalchemy import text

from aw_api.database import get_db
from aw_api.schemas.products import (
    Product,
    ProductCategory,
    ProductSubcategory,
    ProductSubcategoryDetailed
)
from aw_api.repositories import products as product_repo

router = APIRouter() 


@router.get("/products", response_model=list[Product])
def get_products(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    return product_repo.get_all_products(db, limit, offset)


@router.get("/products/{id}", response_model=Product)
def get_specific_product(id: int, db: Session = Depends(get_db)):
    
    result = product_repo.get_specific_product_by_id(db, id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@router.get("/categories", response_model=list[ProductCategory])
def get_categories(db: Session = Depends(get_db)):
   return product_repo.get_all_categories(db)


@router.get("/category/{id}", response_model=ProductCategory)
def get_specific_category(id: int, db: Session = Depends(get_db)):
    result = product_repo.get_specific_category(db, id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product category not found")
    return result


@router.get("/category/{id}/subcategory", response_model=list[ProductSubcategory])
def get_subcategories(id: int, db: Session = Depends(get_db)):
    return product_repo.get_subcategories_by_id(db, id)


@router.get("/category/{id}/subcategory-detailed", response_model=list[ProductSubcategoryDetailed])
def get_subcategory_detailed(id: int, db: Session = Depends(get_db)):
    return product_repo.get_subcategory_detailed_by_id(db, id)