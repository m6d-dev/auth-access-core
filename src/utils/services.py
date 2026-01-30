from abc import ABC
from typing import (
    Any,
    Generic,
    Iterable,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    List,
    Mapping,
)

from django.db.models import QuerySet
from rest_framework import status

from src.utils.functions import raise_validation_error_detail


from .repositories import (
    AbstractEditRepository,
    AbstractFetchRepository,
    AbstractRepository,
)
from .types import TModel, TDTO


class AbstractFetchService(Generic[TDTO]):
    def __init__(self, repository: Union[AbstractFetchRepository]):
        self._repository = repository

    @property
    def model(self) -> TDTO:
        return self._repository.model

    def get(self, *args, **kwargs) -> TDTO:
        return self._repository.get(*args, **kwargs)

    def filter(self, *args, **kwargs) -> List[TDTO]:
        return self._repository.filter(*args, **kwargs)

    def all(self) -> List[TDTO]:
        return self._repository.all()

    def count(self, *args, **kwargs) -> int:
        return self._repository.count(*args, **kwargs)

    def exists(self, *args, **kwargs) -> bool:
        return self._repository.exists(*args, **kwargs)

    def filter_values(
        self, dto_class: TDTO, fields: Optional[List[str]] = None, **filters
    ):
        return self._repository.filter_values(
            dto_class=dto_class, fields=fields, **filters
        )


class AbstractEditService(Generic[TDTO]):
    def __init__(self, repository: AbstractEditRepository[TDTO]):
        self._repository = repository

    @property
    def model(self) -> TDTO:
        return self._repository.model

    def create(self, **kwargs) -> TDTO:
        self._validate(**kwargs)
        instance: TDTO = self._repository.create(**kwargs)
        return instance

    def get_or_create(
        self, defaults: Optional[MutableMapping[str, Any]] = None, **kwargs
    ) -> Tuple[TDTO, bool]:
        return self._repository.get_or_create(defaults=defaults, **kwargs)

    def _validate(self, validate: bool = True, **kwargs) -> TDTO:
        self.validate_fields(**kwargs)
        return self.model(**kwargs)  # noqa

    def update(self, **kwargs) -> TDTO:
        return self._repository.update(**kwargs)

    def delete(self, instance) -> None:
        return self._repository.delete(instance)

    def save(self, instance: TModel, **kwargs):
        return self._repository.save(instance, **kwargs)

    def bulk_create_from_dict(
        self, data: Iterable[Mapping[str, Any]], **kwargs
    ) -> List[TModel]:
        instances = [self._validate(**kwargs, **item) for item in data]
        return self._repository.bulk_create(instances)

    def bulk_create(self, instances: Sequence[TModel]) -> List[TModel]:
        return self._repository.bulk_create(instances)

    def validate_fields(self, **kwargs) -> None:
        model_fields_names = {field.name for field in self.model._meta.fields}
        for field in kwargs.keys():
            if (
                field not in model_fields_names
                and field.removesuffix("_id") not in model_fields_names
            ):
                raise_validation_error_detail(
                    f"Model {self.model.__name__} has no field {field}"
                )


class AbstractService(
    ABC, Generic[TDTO], AbstractFetchService[TDTO], AbstractEditService[TDTO]
):
    def __init__(self, repository: Union[AbstractRepository[TModel]]):
        super().__init__(repository=repository)
