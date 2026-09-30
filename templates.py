from fastapi import APIRouter

router = APIRouter(prefix="/templates", tags=["Templates"])

TEMPLATES = [
    {"id": "employment", "name": "Employment Agreement"},
    {"id": "nda", "name": "Non-Disclosure Agreement"},
    {"id": "lease", "name": "Lease Agreement"},
    {"id": "consulting", "name": "Consulting Agreement"},
]

@router.get("")
def list_templates():
    return TEMPLATES
