from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView
from tortoise.contrib.sanic import register_tortoise

from fibonacci import fibonacci
from models import (
    RequestedNumber, RequestedNumber_Pydantic, RequestedNumber_Pydantic_List
)


app = Sanic(name='fibonacci-rest-service')


class Fibonacci(HTTPMethodView):
    async def get(self, request):
        pydantic_objects = await RequestedNumber_Pydantic_List.from_queryset(RequestedNumber.all())

        return json(pydantic_objects.dict())

    async def post(self, request):
        requested_number = await RequestedNumber.create(
            number=request.json['number'],
            result=fibonacci(request.json['number']))
        pydantic_object = await RequestedNumber_Pydantic.from_tortoise_orm(
            requested_number)

        return json(pydantic_object.dict())


app.add_route(Fibonacci.as_view(), '/')

register_tortoise(app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
