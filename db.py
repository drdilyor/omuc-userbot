from tortoise import Tortoise, Model, fields


async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['db']}
    )
    await Tortoise.generate_schemas()


async def close():
    await Tortoise.close_connections()


class Colorlist(Model):
    text = fields.CharField(4096)
    is_black = fields.BooleanField()
