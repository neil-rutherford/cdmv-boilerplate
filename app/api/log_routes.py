from app.api import bp
from flask import request, Response
from app.models import Log, Content
import datetime
from sqlalchemy import desc
import json

@bp.route('/_api/read/logs')
def read_logs():
    master_list = []
    content_list = []
    cookie_list = []
    time_list = []

    if request.args:
        if 'slug' in request.args:
            content = Content.query.filter_by(slug=str(request.args.get('slug'))).first_or_404()
            logs = Log.query.filter_by(content_id=content.id).order_by(desc(Log.timestamp)).all()
            for log in logs:
                content_list.append(log)
        if 'cookie_uuid' in request.args:
            logs = Log.query.filter_by(cookie_uuid=str(request.args.get('cookie_uuid'))).order_by(desc(Log.timestamp)).all()
            for log in logs:
                cookie_list.append(log)
        if 'start_date' in request.args:
            if 'end_date' in request.args:
                logs = Log.query.filter(
                    Log.timestamp >= datetime.datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
                ).order_by(desc(Log.timestamp)).all()
                for log in logs:
                    if log.timestamp <= datetime.datetime.strptime(request.args.get('end_date'), '%Y-%m-%d'):
                        time_list.append(log)
            else:
                logs = Log.query.filter(
                    Log.timestamp >= datetime.datetime.strptime(str(request.args.get('start_date')), '%Y-%m-%d')
                ).order_by(desc(Log.timestamp)).all()
                for log in logs:
                    time_list.append(log)

        if len(content_list) > 0:
            master_list.append(set(content_list))
        if len(cookie_list) > 0:
            master_list.append(set(cookie_list))
        if len(time_list) > 0:
            master_list.append(set(time_list))

        results_set = set.intersection(*master_list) if master_list else set()
        results = list(results_set)
        data_list = []
        for result in results:
            data_dict = {
                'id': result.id,
                'slug': result.content.slug,
                'cookie_uuid': result.cookie_uuid,
                'timestamp': datetime.datetime.strftime(result.timestamp, '%Y-%m-%d %H:%M:%S')
            }
            data_list.append(data_dict)
        data_json = json.dumps(data_list)
    else:
        now = datetime.datetime.utcnow()
        bom = datetime.datetime(now.year, now.month, 1)
        logs = Log.query.filter(Log.timestamp > bom).order_by(Log.timestamp.desc()).all()
        for log in logs:
            data_dict = {
                'id': log.id,
                'slug': log.content.slug, 
                'cookie_uuid': log.cookie_uuid,
                'timestamp': datetime.datetime.strftime(log.timestamp, '%Y-%m-%d %H:%M:%S')
            }
            master_list.append(data_dict)
        data_json = json.dumps(master_list)
    return Response(
        status=200,
        response=data_json,
        mimetype='application/json'
    )