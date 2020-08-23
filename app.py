from flask import Flask, render_template, url_for, redirect, request
from service import fillData
from models import *

app = Flask('ComicsColletionManager')


@app.route('/')
def allCollection():
    return render_template('index.html',
                           collections=Collection
                           .select())


@app.route('/collection/<int:idCollection>/<int:collected>/<string:OrderBy>')
def comicsCollection(idCollection, collected, OrderBy):
    order = ComicCollection.order
    if OrderBy == 'name':
        order = Comic.raw_name
    cc = ComicCollection.select().join(Comic).where(ComicCollection.collection == idCollection, Comic.collected == collected).order_by(order)
    col = Collection.get_by_id(idCollection)
    return render_template('collection.html',
                           comicsoncollection=cc,
                           thiscollection=col,
                           collected = collected,
                           OrderBy = OrderBy)


@app.route('/collect/<int:idCollection>/<string:idComic>/<int:collected>/<string:OrderBy>')
def collectComic(idComic, idCollection, collected, OrderBy):
    query = Comic.update(Collected=collected).where(Comic.id == idComic)
    query.execute()
    collected = not collected
    return redirect(url_for('comicsCollection', idCollection=idCollection, collected = collected, OrderBy = OrderBy))


@app.route('/getData')
def getComicData():
    fillData()
    return redirect(url_for('allCollection'))


if __name__ == '__main__':
    createSchema()
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
