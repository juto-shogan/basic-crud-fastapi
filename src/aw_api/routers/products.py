from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import text

from aw_api.database import get_db
from pydantic import BaseModel

router = APIRouter()

class ProductCategory(BaseModel):
    name: str

class ProductSubcategory(BaseModel):
    productsubcategoryid: int
    productcategoryid: int
    name: str
    
    
@router.get("/categories", response_model=list[ProductCategory])
def get_category(db: Session = Depends(get_db)):
    get_all = db.execute(
        text("SELECT * FROM production.productcategory"),
        {}
    )    
    result = get_all.mappings().all()
    return result


@router.get("/category/{id}")
def get_specific_category(id: int, db: Session = Depends(get_db)):

    get_specific = db.execute(
        text("SELECT name FROM production.productcategory WHERE productcategoryid = :productcategoryid"),
        {"productcategoryid": id}
    )
    result = get_specific.mappings().first()
    if result is None:
        raise HTTPException(status_code=404, detail="Id is missing.")
    return result

@router.get("/category/{id}/subcategory", response_model=list[ProductSubcategory])
def get_subcategories(id:int, db:Session = Depends(get_db)):
    info = db.execute(
        text("SELECT * FROM production.productsubcategory WHERE productcategoryid = :productcategoryid"),
        {"productcategoryid": id}
    )    
    return info.mappings().all()

@router.get("/category/{id}/subcategory-detailed")
def get_specific_subcategory(id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            SELECT psc.productsubcategoryid, pc.name AS category_name, psc.name AS subcategory_name
            FROM production.productsubcategory AS psc
            JOIN production.productcategory AS pc USING(productcategoryid)
            WHERE pc.productcategoryid = :productcategoryid
            """
        ),
        {"productcategoryid":id}
    )
    return result.mappings().all()