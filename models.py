import peewee as pw

database = pw.SqliteDatabase('data.db')


class BaseModel(pw.Model):
    class Meta:
        database = database


class Collection(BaseModel):
    id = pw.AutoField(column_name='ID')
    title = pw.TextField(column_name='Title', null=True)
    url = pw.TextField(column_name='Url', null=True)


class Comic(BaseModel):
    collected = pw.IntegerField(column_name='Collected', default=0)
    id = pw.TextField(column_name='ID', primary_key=True)
    raw_name = pw.TextField(column_name='RawName', null=True)


class ComicCollection(BaseModel):
    collection = pw.ForeignKeyField(
        column_name='CollectionId', field='id', model=Collection)
    comic = pw.ForeignKeyField(column_name='ComicId', field='id', model=Comic)
    order = pw.IntegerField(column_name='Order')

    class Meta:
        indexes = (
            (('collection', 'comic'), True),
        )
        primary_key = pw.CompositeKey('collection', 'comic')


def createSchema():
    Collection.create_table()
    Comic.create_table()
    ComicCollection.create_table()


if __name__ == '__main__':
    pass
