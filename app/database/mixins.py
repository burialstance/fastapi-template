from tortoise import Model, fields


class BaseMixinModel(Model):
    class Meta:
        abstract = True

    id = fields.BigIntField(pk=True, index=True)

    async def as_dict(self):
        d = {}
        for field in self._meta.db_fields:
            d[field] = getattr(self, field)
        for field in self._meta.backward_fk_fields:
            d[field] = await getattr(self, field).all().values()
        return d

    async def _update(self, **kwargs):
        passed_fields = self._set_kwargs(kwargs)
        updated_fields = {field for field in passed_fields if field in kwargs}
        if passed_fields:
            await self.save(update_fields=updated_fields)
            return True
        return False


class UUIDDBModel:
    id = fields.UUIDField(unique=True, pk=True)


class BaseCreatedAtModel:
    created_at = fields.DatetimeField(auto_now_add=True)


class BaseCreatedUpdatedAtModel:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)