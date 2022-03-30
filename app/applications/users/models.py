from typing import Optional

from tortoise import fields
from tortoise.exceptions import DoesNotExist

from app.applications.auth.utils.password import get_password_hash
from app.applications.users.schemas import BaseUserCreate
from app.database.mixins import BaseCreatedUpdatedAtModel, BaseMixinModel


class User(BaseMixinModel, BaseCreatedUpdatedAtModel):

    username = fields.CharField(max_length=20, unique=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    password_hash = fields.CharField(max_length=128, null=True)
    last_login = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    def full_name(self) -> str:
        if self.first_name or self.last_name:
            return ' '.join(filter(None, [self.first_name, self.last_name])).strip()
        return self.username


    @classmethod
    async def get_by_username(cls, username: str) -> Optional["User"]:
        try:
            return await cls.get(username=username)
        except DoesNotExist:
            return None

    @classmethod
    async def create(cls, user: BaseUserCreate) -> "User":
        user_dict = user.dict()
        password_hash = get_password_hash(password=user.password)
        model = cls(**user_dict, password_hash=password_hash)
        await model.save()
        return model

    class Meta:
        table = 'users'

    class PydanticMeta:
        computed = ["full_name"]