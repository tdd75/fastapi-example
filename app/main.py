from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import setting
from app.api.department_api import department_router
from app.api.employee_api import employee_router
from app.api.location_api import location_router
from app.api.organization_api import organization_router
from app.api.position_api import position_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=setting.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include routers
app.include_router(organization_router)
app.include_router(employee_router)
app.include_router(department_router)
app.include_router(location_router)
app.include_router(position_router)
