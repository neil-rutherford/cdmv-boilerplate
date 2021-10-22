from app.api import bp
from config import Config
from flask import request, Response, abort
from app import db
from app.models import Content
import datetime
import json

@bp.route('/_api/create/content', methods=['POST'])
def create_content():
    if str(request.form.get('publisher_key')) != Config.PUBLISHER_KEY:
        abort(403, description='Incorrect `publisher_key`.')
    try:
        content = Content()
        content.file_name = str(request.form.get('file_name'))
        content.slug = str(request.form.get('slug'))
        content.author_name = str(request.form.get('author_name'))
        content.author_handle = str(request.form.get('author_handle'))
        content.title = str(request.form.get('title'))
        content.description = str(request.form.get('description'))
        content.category = int(request.form.get('category'))
        content.section = str(request.form.get('section'))
        content.tags = str(request.form.get('tags'))
        content.image_url = str(request.form.get('image_url'))
        content.published_time = datetime.datetime.utcnow()
        content.modified_time = datetime.datetime.utcnow()
        db.session.add(content)
        db.session.commit()
        return Response(
            status=201,
            response=json.dumps({
                'id': content.id,
                'file_name': content.file_name,
                'slug': content.slug,
                'author_name': content.author_name,
                'author_handle': content.author_handle,
                'title': content.title,
                'description': content.description,
                'category': content.category,
                'section': content.section,
                'tags': str(content.tags).split(', '),
                'image_url': content.image_url,
                'published_time': datetime.datetime.strftime(content.published_time, '%Y-%m-%d %H:%M:%S'),
                'modified_time': datetime.datetime.strftime(content.modified_time, '%Y-%m-%d %H:%M:%S'),
                'views': len(content.views)
            }),
            mimetype='application/json'
        )
    except Exception as e:
        abort(500, description='{}'.format(e))


@bp.route('/_api/read/content/<slug>', methods=['GET'])
def read_content(slug):
    content = Content.query.filter_by(slug=str(slug)).first_or_404()
    return Response(
        status=200,
        response=json.dumps({
            'id': content.id,
            'file_name': content.file_name,
            'slug': content.slug,
            'author_name': content.author_name,
            'author_handle': content.author_handle,
            'title': content.title,
            'description': content.description,
            'category': content.category,
            'section': content.section,
            'tags': str(content.tags).split(", "),
            'image_url': content.image_url,
            'published_time': datetime.datetime.strftime(content.published_time, '%Y-%m-%d %H:%M:%S'),
            'modified_time': datetime.datetime.strftime(content.modified_time, '%Y-%m-%d %H:%M:%S'),
            'views': len(content.views)
        }),
        mimetype='application/json'
    )


@bp.route('/_api/update/content/<slug>', methods=['POST'])
def update_content(slug):
    if str(request.form.get('publisher_key')) != Config.PUBLISHER_KEY:
        abort(403, description='Incorrect `publisher_key`.')
    content = Content.query.filter_by(slug=str(slug)).first_or_404()
    try:
        content.file_name = str(request.form.get('file_name'))
        content.author_name = str(request.form.get('author_name'))
        content.author_handle = str(request.form.get('author_handle'))
        content.title = str(request.form.get('title'))
        content.description = str(request.form.get('description'))
        content.category = int(request.form.get('category'))
        content.section = str(request.form.get('section'))
        content.tags = str(request.form.get('tags'))
        content.image_url = str(request.form.get('image_url'))
        content.modified_time = datetime.datetime.utcnow()
        db.session.commit()
        return Response(
            status=200,
            response=json.dumps({
                'id': content.id,
                'file_name': content.file_name,
                'slug': content.slug,
                'author_name': content.author_name,
                'author_handle': content.author_handle,
                'title': content.title,
                'description': content.description,
                'category': content.category,
                'section': content.section,
                'tags': str(content.tags).split(', '),
                'image_url': content.image_url,
                'published_time': datetime.datetime.strftime(content.published_time, '%Y-%m-%d %H:%M:%S'),
                'modified_time': datetime.datetime.strftime(content.modified_time, '%Y-%m-%d %H:%M:%S'),
                'views': len(content.views)
            }),
            mimetype='application/json'
        )
    except Exception as e:
        abort(500, description="{}".format(e))


@bp.route('/_api/delete/content/<slug>', methods=['POST'])
def delete_content(slug):
    if str(request.form.get('publisher_key')) != Config.PUBLISHER_KEY:
        abort(403, description='Incorrect `publisher_key`.')
    content = Content.query.filter_by(slug=str(slug)).first_or_404()
    try:
        db.session.delete(content)
        db.session.commit()
        return Response(
            status=204,
            response="Content with slug {} successfully deleted."
        )
    except Exception as e:
        abort(500, description="{}".format(e))