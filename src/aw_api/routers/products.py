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


router = APIRouter() 


@router.get("/products", response_model=list[Product])
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
            ORDER BY productid
            LIMIT :limit
            OFFSET :offset
            """
        ),
        {"limit": limit, "offset": offset}
    )
    return search.mappings().all()


@router.get("/products/{id}", response_model=Product)
def get_specific_product(id: int, db: Session = Depends(get_db)):
    info = db.execute(
        text(
            """
            select * from production.product where productid = :productid
            """
        ),
        {"productid": id}
    )
    result =  info.mappings().first()
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return result


@router.get("/categories", response_model=list[ProductCategory])
def get_categories(db: Session = Depends(get_db)):
    get_all = db.execute(
        text("SELECT * FROM production.productcategory"),
        {}
    )    
    result = get_all.mappings().all()
    return result


# TODO: make a schema for the categories table and call it here as a response_model, then improve the query here, and move that query to a repo folder and file
@router.get("/category/{id}")
def get_specific_category(id: int, db: Session = Depends(get_db)):

    get_specific = db.execute(
        # TODO: make a better category query with more info being called about the category
        text("SELECT name FROM production.productcategory WHERE productcategoryid = :productcategoryid"),
        {"productcategoryid": id}
    )
    result = get_specific.mappings().first()
    if result is None:
        raise HTTPException(status_code=404, detail="Product category not found")
    return result


@router.get("/category/{id}/subcategory", response_model=list[ProductSubcategory])
def get_subcategories(id: int, db: Session = Depends(get_db)):
    # NOTE: First, check whether the category exists
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

    # NOTE: Category exists, so get its subcategories
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


@router.get("/category/{id}/subcategory-detailed", response_model=list[ProductSubcategoryDetailed])
def get_subcategory_detailed(id: int, db: Session = Depends(get_db)):
    
    category = db.execute(
        text("""
            SELECT productcategoryid
            FROM production.productcategory
            WHERE productcategoryid = :productcategoryid
        """),
        {"productcategoryid": id}
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Product category not found"
        )
        
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