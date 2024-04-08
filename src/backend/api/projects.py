from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.database import databaseHandler
from src.backend.models import auth as auth_models
from src.backend.models import orders as orders_models
from src.backend.services.orders import services as orders_services
from src.backend.services.auth import services as auth_services

router = APIRouter(tags=["Projects"], prefix="/projects")


