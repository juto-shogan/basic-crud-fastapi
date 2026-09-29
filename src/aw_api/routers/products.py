from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session
from sqlalchemy import text

from aw_api.database import get_db
from aw_api.schemas.products import Products, ProductCategory, ProductSubcategory

router = APIRouter() 


@router.get("/products", response_model=list[Products])
def get_products(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    search = db.execute(
        text(
            """
            SELECT *
            FROM production.product
            LIMIT :limit
            OFFSET :offset
            """
        ),
        {"limit": limit, "offset": offset}
    )

    return search.mappings().all()


@router.get("/products/{id}", response_model=list[Products])
def get_specific_product(id: int, db: Session = Depends(get_db)):
    info = db.execute(
        text(
            """
            select * from production.product where productid = :productid
            """
        ),
        {"productid": id}
    )
    return info.mappings().all()


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
def get_subcategories(id: int, db: Session = Depends(get_db)):
    # First, check whether the category exists
    category = db.execute(
        text(
            """
            SELECT productcategoryid
            FROM production.productcategory
            WHERE productcategoryid = :productcategoryid
            """
        ),
        {"productcategoryid": id}
    ).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Product category not found")

    # Category exists, so get its subcategories
    info = db.execute(
        text(
            """
            SELECT *
            FROM production.productsubcategory
            WHERE productcategoryid = :productcategoryid
            """
        ),
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