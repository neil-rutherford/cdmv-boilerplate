from app.content import bp
from flask import render_template, abort, Response, session
import json
from app.models import Content, Log
from app import db
import uuid
import datetime

@bp.route('/blog')
def blog():
    return "blog"


@bp.route('/blog/content/<slug>')
def content(slug):
    content = Content.query.filter_by(slug=str(slug)).first_or_404()
    if 'cookie_uuid' not in session:
        session['cookie_uuid'] = str(uuid.uuid4())
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
    content = Content.query.filter_by().order_by(Content.modified_time.desc()).all()
    if 'counter' in request.args:
        counter = int(request.args.get('counter'))
        if counter >= len(contents):
            data_json = json.dumps([])
        else:
            data_list = []
            for x in content[counter:counter+10]:
                data_dict = {
                    'image_url': x.image_url,
                    'tags': str(x.tags).split(', '),
                    'title': x.title,
                    'description': x.description,
                    'author': x.author,
                    'content_url': url_for('content.content', slug=x.slug),
                    'modified_time': x.modified_time
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