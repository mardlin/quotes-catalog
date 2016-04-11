from catalog import app
from flask import render_template, request, redirect, url_for
from flask import jsonify, flash, make_response
from flask.ext.seasurf import SeaSurf

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property
from database_setup import Base, Category, Item, User

# login_session will be a dict for storing a user's session variables
from flask import session as login_session
# IMPORTS for anti-forgergy state tokens
import random
import string

# import and initialize SeaSurf for CSRF protection
from flask.ext.seasurf import SeaSurf
csrf = SeaSurf(app)

engine = create_engine('sqlite:///quotes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#  We'll need the categories in all templates for the header menu
@app.context_processor
def inject_categories():
    """    """

    categories = session.query(Category).all()
    return dict(categories=categories)


@app.route('/themes')
@app.route('/')
def showCatalog():
    """Page to display categories and recently added (latest) items"""

    latest_items = session.query(Item).order_by(desc(Item.date_created))\
        .limit(3)
    return render_template('showCatalog.html', latest_items=latest_items)


@app.route('/themes/json')
def showCatalogJSON():
    """Page to display categories and recently added (latest) items"""

    categories = session.query(Category).all()
    category_list = []
    for c in categories:
        category_list.append(c.serialize)
    return jsonify(category=category_list)


@app.route('/themes/<category_name>/quotes')
@app.route('/themes/<category_name>')
def showCategory(category_name):
    """Page to display items in a given category"""

    items = session.query(Item).filter(Item.category.has(name=category_name))\
        .all()
    return render_template(
        'showCategory.html', category_name=category_name, items=items)


@app.route('/themes/<category_name>/json')
def showCategoryJSON(category_name):
    """Page to display items in a given category"""

    category = session.query(Category).filter_by(name=category_name).first()

    return jsonify(category=category.serialize)


# helper functions
def getItem(category_name, item_name):
    category_items = (
        session.query(Item)
        .filter(Item.category.has(name=category_name))
    )
    # use .first() to get an empty list if there is no match
    item = category_items.filter_by(name=item_name).first()
    return item


@app.route('/themes/<category_name>/<item_name>')
def showItem(category_name, item_name):
    """Page to display the description and image of an item"""

    item = getItem(category_name=category_name, item_name=item_name)
    if not item:
        flash("There is no such item")
        return redirect(url_for('showCatalog'))

    items = session.query(Item).filter(Item.category.has(name=category_name))\
        .all()
    return render_template(
        'showItem.html', category_name=category_name, items=items, item=item,
        item_name=item_name, item_creator=item.user_id)


@app.route('/themes/<category_name>/<item_name>/json')
def showItemJSON(category_name, item_name):
    """Page to display the description and image of an item"""

    item = getItem(category_name=category_name, item_name=item_name)
    if item:
        return jsonify(item=item.serialize)
    else:
        return 'Item does not exist', 404


# Helper for generating a "name" for a new quote entry
def firstThreeWords(description):
    words_list = description.split(' ')
    name = " ".join(words_list[0:3]) + "..."
    return name


@app.route('/themes/<category_name>/add', methods=['GET', 'POST'])
def addItem(category_name):
    """Page to display for adding an item"""

    user_id = login_session.get('user_id')

    if user_id is None:
        flash("You must login to add an item")
        return redirect(url_for('showCategory', category_name=category_name))

    category = session.query(Category).filter_by(name=category_name).first()
    if request.method == 'POST':
        print request.form
        new_item = Item(category_id=category.id)
        new_item.description = request.form['description']
        new_item.name = firstThreeWords(new_item.description)
        new_item.author = request.form['author']
        new_item.user_id = login_session['user_id']

        session.add(new_item)
        session.commit()
        flash('"%s" item successfully added to "%s" category' % (
                new_item.name, category_name))
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('addItem.html', category_name=category_name)


@app.route('/themes/<category_name>/<item_name>/edit', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    """Page to display for editing an item"""

    category = session.query(Category).filter_by(name=category_name).first()
    itemToEdit = getItem(category_name=category_name, item_name=item_name)

    if login_session['user_id'] != itemToEdit.user_id:
        flash("Only the item's creator can edit an item")
        return redirect(url_for('showItem', category_name=category_name,
                        item_name=item_name))

    if request.method == 'POST':
        itemToEdit.description = request.form['description']
        itemToEdit.name = firstThreeWords(itemToEdit.description)
        itemToEdit.author = request.form['author']
        session.add(itemToEdit)
        session.commit()
        flash('"%s" item successfully edited in "%s" category' % (
                itemToEdit.name, category_name))
        return redirect(url_for(
            'showItem', category_name=category_name, item_name=itemToEdit.name)
        )
    return render_template(
        'editItem.html', category_name=category_name, item_name=item_name,
        item=itemToEdit
        )


@app.route('/themes/<category_name>/<item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    """Page to display for deleting an item"""

    itemToDelete = getItem(category_name=category_name, item_name=item_name)
    if login_session['user_id'] != itemToDelete.user_id:
        flash("Only the item's creator can delete an item")
        return redirect(url_for('showItem', category_name=category_name,
                        item_name=item_name))

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('"%s" item successfully deleted from "%s" category' % (
            item_name, category_name))
        return redirect(url_for('showCategory', category_name=category_name))
    return render_template('deleteItem.html', category_name=category_name,
                           item=itemToDelete, item_name=item_name)


@app.route('/themes/<category_name>/quotes/json')
def jsonCategory(category_name):
    """return data in a json format."""

    return jsonify({
        'page': 'category json endpoint.'
        })


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404
