from fastapi import APIRouter, Depends, HTTPException,status,Response
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.organization import Organization
from app.schemas.organizations import OrganizationCreate, OrganizationRead,OrganizationUpdate

router = APIRouter()


@router.post("/organizations",response_model=OrganizationRead,)
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db),
) -> Organization:
    organization = Organization(name=organization.name)
    db.add(organization)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(organization)

    return organization

@router.get("/organizations/{organization_id}", response_model = OrganizationRead,)

def get_organization(organization_id : int,db : Session = Depends(get_db),
):
    organization = db.get(Organization,organization_id)
    if organization is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )
    return organization

@router.patch("/organizations/{organizations_id}",response_model = OrganizationRead,)

def update_organization(organizations_id : int,organization_in: OrganizationUpdate,db : Session = Depends(get_db),
)->Organization:
    organization = db.get(Organization,organizations_id)
    if organization is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )

    organization.name = organization_in.name

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(organization)

    return organization


@router.delete(
    "/organizations/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
) -> Response:
    organization = db.get(Organization, organization_id)

    if organization is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found",
        )

    db.delete(organization)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
