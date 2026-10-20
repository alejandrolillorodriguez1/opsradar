from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.organization import Organization
from app.schemas.organizations import OrganizationCreate, OrganizationRead

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