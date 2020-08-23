from flask import Flask, render_template, url_for, redirect, request
from service import fillData
from models import *

app = Flask('ComicsColletionManager')


@app.route('/')
def allCollection():
    return render_template('index.html',
                           collections=Collection
                           .select())


@app.route('/collection/<int:idCollection>/<int:collected>')
def comicsCollection(idCollection, collected):
    cc = ComicCollection.select().join(Comic).where(ComicCollection.collection == idCollection, Comic.collected == collected).order_by(ComicCollection.order)
    col = Collection.get_by_id(idCollection)
    return render_template('collection.html',
                           comicsoncollection=cc,
                           thiscollection=col)


@app.route('/collect/<int:idCollection>/<string:idComic>')
def collectComic(idComic, idCollection):
    query = Comic.update(Collected=1).where(Comic.id == idComic)
    query.execute()
    return redirect(url_for('comicsCollection', idCollection=idCollection))


@app.route('/getData')
def getComicData():
    fillData()
    return redirect(url_for('allCollection'))


if __name__ == '__main__':
    createSchema()
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
