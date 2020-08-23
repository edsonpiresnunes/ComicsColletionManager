from flask import Flask, render_template, url_for, redirect, request
from service import fillData
from models import *

app = Flask('ComicsColletionManager')


@app.route('/')
def allCollection():
    return render_template('index.html',
                           collections=Collection
                           .select())


@app.route('/collection/<int:idCollection>')
def comicsCollection(idCollection):
    return render_template('collection.html',
                           comicsoncollection=ComicCollection
                           .select()
                           .join(Comic)
                           .where(ComicCollection.collection == idCollection, Comic.collected == 0)
                           .order_by(ComicCollection.order))


@app.route('/collect/<int:idCollection>/<string:idComic>')
def collectComic(idComic, idCollection):
    query = Comic.update(Collected=1).where(Comic.id == idComic)
    query.execute()
    return redirect(url_for('comicsCollection', idCollection=idCollection))


if __name__ == '__main__':
    createSchema()
    fillData()
    app.run(debug=True, use_reloader=True)
