from abc import ABC
from typing import (
    Any,
    Generic,
    Iterable,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    List,
)
from src.utils.functions import raise_validation_error
from src.utils.types import TModel, TDTO, TQS


class AbstractFetchRepository(Generic[TModel]):
    model: Type[TModel]

    @property
    def table_name(self) -> str:
        return self.model._meta.db_table

    def get(self, *args, **kwargs) -> Union[TModel, None]:
        res = self.filter(*args, **kwargs)
        if len(res) == 0:
            return None
        if len(res) > 1:
            raise_validation_error("Multiple objects found")
        return res[0]

    def filter(self, *args, **kwargs) -> TQS:
        return self.model.objects.filter(*args, **kwargs)

    def all(self) -> List[TQS]:
        qs: TQS = self.model.objects.all()
        return list(qs)

    def count(self, *args, **kwargs) -> int:
        return self.filter(*args, **kwargs).count()

    def exists(self, *args, **kwargs) -> bool:
        return self.model.objects.filter(*args, **kwargs).exists()


class AbstractEditRepository(Generic[TModel]):
    model: Type[TModel]

    def create(self, **kwargs) -> TModel:
        return self.model.objects.create(**kwargs)

    def update_or_create(
        self, defaults: Optional[MutableMapping[str, Any]] = None, **kwargs
    ) -> Tuple[TModel, bool]:
        instance, created = self.model.objects.update_or_create(
            defaults=defaults, **kwargs
        )
        return instance, created

    def get_or_create(
        self, defaults: Optional[MutableMapping[str, Any]] = None, **kwargs
    ) -> Tuple[TModel, bool]:
        instance, created = self.model.objects.get_or_create(
            defaults=defaults, **kwargs
        )
        return instance, created

    def update(self, filters: dict, **kwargs) -> int:
        return self.model.objects.filter(**filters).update(**kwargs)

    def delete(self, filters: dict) -> int:
        qs = self.model.objects.filter(**filters)
        count = qs.count()
        qs.delete()
        return count

    @staticmethod
    def save(instance: TModel, **kwargs):
        instance.save(**kwargs)

    def bulk_create(self, instances: Iterable[TModel], **kwargs) -> List[TDTO]:
        return self.model.objects.bulk_create(instances, **kwargs)

    def bulk_update(
        self,
        instances: Iterable[TModel],
        fields: Sequence[str],
        batch_size: Optional[int],
    ) -> int:
        return self.model.objects.bulk_update(
            objs=instances, fields=fields, batch_size=batch_size
        )


class AbstractRepository(
    Generic[TModel],
    AbstractFetchRepository[TModel],
    AbstractEditRepository[TModel],
    ABC,
): ...
