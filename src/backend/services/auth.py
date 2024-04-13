from datetime import timedelta, datetime

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPBasic
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend import tables
from src.backend.models import auth as models
from src.backend.models import role as role_models
from src.backend.settings import settings
from src.backend.services.role import services as role_services


oauth_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class AuthServices:
    @classmethod
    def hash_password(cls, password: str):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @classmethod
    def validate_password(cls, password: str, hash_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hash_password)

    @classmethod
    def encode_jwt(
            cls,
            payload: dict,
            private_key: str = settings.private_key_path.read_text(),
            algorithm: str = settings.algorithm,
            expire_timedelta: timedelta | None = None,
            expire_minutes: int = settings.access_token_expire,
    ):

        to_encode = payload.copy()
        now = datetime.utcnow()

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode.update(
            exp=expire,  # Время, когда токен закончит свою работу
            iat=now,  # Время, когда выпущен токен
        )

        return jwt.encode(to_encode, key=private_key, algorithm=algorithm)

    @classmethod
    def decode_jwt(
            cls,
            token: str | bytes,
            public_key: str = settings.public_key_path.read_text(),
            algorithms: str = settings.algorithm) -> dict:

        return jwt.decode(token, key=public_key, algorithms=[algorithms])

    async def validate_token(
            self,
            token,
    ) -> models.User:

        confirm_user = self.decode_jwt(token).get("user")

        try:
            user = models.User.parse_obj(confirm_user)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials") from None

        return user

    async def get_current_user(self, token: str = Depends(oauth_schema)) -> models.User:
        if token:
            return await self.validate_token(token)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not validate token. Token={token}") from None

    def create_token(self, user: tables.User, roles) -> models.Token:
        userdata = models.User(
            id=user.id,
            username=user.username,
            roles=roles
        )

        payload = {
            "sub": str(userdata.id),
            "user": userdata.dict()
        }

        return models.Token(access_token=self.encode_jwt(payload))

    async def login(self, username: str, password: str, session: AsyncSession) -> models.Token:

        #  Get user from DATABASE

        stmt = select(tables.User).where(tables.User.username == username)
        db_response = await session.execute(stmt)
        user = db_response.scalar()

        if user:
            user_roles = await role_services.get_list_user_roles_by_id_user(user_id=user.id, session=session)
            # hashed_password = str.encode(user.password, encoding="utf-8")

            if self.validate_password(password, str.encode(user.password, encoding="utf-8")):
                return self.create_token(user=user, roles=user_roles)

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not exist, please register")

    async def register(self, user_data: models.UserRegister, session: AsyncSession):
        stmt = select(tables.User).where(tables.User.username == user_data.username)
        db_response = await session.execute(stmt)
        db_user = db_response.scalar()

        if db_user is None:
            user = tables.User(
                username=user_data.username,
                password=str(self.hash_password(user_data.password)).replace("b'", "").replace("'", "")
            )
            session.add(user)
            await session.commit()

            #  ADD ROLE FOR NEW USER

            stmt_undef_role = select(tables.Role).where(tables.Role.name == role_models.EnumBackendRole.UNDEFINED)
            resp = await session.execute(stmt_undef_role)
            undef_role = resp.scalar()

            new_role = tables.SecondaryUserRole(
                user_id=user.id,
                role_id=undef_role.id
            )

            session.add(new_role)
            await session.commit()

            # self.create_token(user)
            return {"response": 200, "message": "Registration completed"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Users already exist",
                headers={
                    "WWW-Authenticate": 'Bearer'
                }
            )



services = AuthServices()
