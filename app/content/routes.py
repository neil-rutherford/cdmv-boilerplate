from app.content import bp
from flask import render_template, abort, Response, session, request, url_for
import json
from app.models import Content, Log
from app import db
import uuid
import datetime
from sqlalchemy import desc

@bp.route('/blog')
def blog():
    return render_template(
        'content/blog.html',
        title='Blog',
        description='Description'
    )


@bp.route('/blog/content/<slug>')
def content(slug):
    content = Content.query.filter_by(slug=str(slug)).first_or_404()
    if 'cookie_uuid' not in session:
        session['cookie_uuid'] = str(uuid.uuid4())
        session.permanent = True
    try:
        l = Log()
        l.content_id = content.id
        l.cookie_uuid = session['cookie_uuid']
        l.timestamp = datetime.datetime.utcnow()
        db.session.add(l)
        db.session.commit()
        return render_template(
            'content/blog/{}'.format(content.file_name),
            title=content.title,
            description=content.description,
            content=content
        )
    except:
        abort(404)


@bp.route('/_api/load/content')
def load_content():
    content = Content.query.filter_by().order_by(desc(Content.modified_time)).all()
    if 'counter' in request.args:
        counter = int(request.args.get('counter'))
        if counter >= len(content):
            data_json = json.dumps([])
        else:
            data_list = []
            for x in content[counter:counter+10]:
                data_dict = {
                    'image_url': x.image_url,
                    'tags': str(x.tags).split(', '),
                    'title': x.title,
                    'description': x.description,
                    'author_name': x.author_name,
                    'content_url': url_for('content.content', slug=x.slug),
                    'modified_time': datetime.datetime.strftime(x.modified_time, '%Y-%m-%d %H:%M:%S')
                }
                data_list.append(data_dict)
            data_json = json.dumps(data_list)
        return Response(
            status=200,
            response=data_json,
            mimetype='application/json'
        )
    else:
        abort(500, description='counter argument required.')        