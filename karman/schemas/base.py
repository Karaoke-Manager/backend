from typing import Any, Callable, Optional

import orjson
from pydantic import BaseModel

from karman.config import settings


def to_camel_case(string: str) -> str:
    """
    Converts a ``snake_case`` string to ``camelCase``.
    :param string: A ``snake_case`` string.
    :return: A ``camelCase`` version of the input.
    """
    components = string.split("_")
    return components[0] + "".join(x.capitalize() for x in components[1:])


def orjson_dumps(v: Any, *, default: Optional[Callable[[Any], Any]]) -> str:
    """
    Makes ``orjson.dumps`` compatible with Pydantic.
    """
    return orjson.dumps(v, default).decode()


class BaseSchema(BaseModel):
    """
    The ``BaseSchema`` should be used as superclass for all Karman schemas. The
    schema sets some sensible defaults in the Pydantic config.
    """

    class Config:
        # Get some extra performance in production by disabling validations
        validate_all = settings.debug
        validate_assignment = settings.debug
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True
        alias_generator = to_camel_case
