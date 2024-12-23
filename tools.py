from aiohttp import web
from shema import CreatAdv, UpdateAdv, CreatUser, UpdateUser
from pydantic import ValidationError
from errors import get_http_error


def validate(schema_cls: type[CreatAdv] | type[UpdateAdv] | type[CreatUser] | type[UpdateUser], json_data):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        raise get_http_error(web.HTTPConflict, 'validation error')