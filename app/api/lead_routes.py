from app.api import bp
from app.models import Lead
from flask import Response, abort, request
from config import Config
import datetime
import json
from sqlalchemy import desc

@bp.route('/_api/read/leads', methods=['POST'])
def read_leads():
    if str(request.form.get('admin_key')) != Config.ADMIN_KEY:
        abort(403, description='Incorrect `admin_key`.')
    leads = Lead.query.filter_by(can_contact=True).order_by(desc(Lead.timestamp)).all()
    data_list = []
    for x in leads:
        data_dict = {
            'id': x.id,
            'first_name': x.first_name,
            'last_name': x.last_name,
            'email': x.email,
            'category': x.category,
            'can_contact': x.can_contact,
            'timestamp': datetime.datetime.strftime(x.timestamp, '%Y-%m-%d %H:%M:%S')
        }
        data_list.append(data_dict)
    data_json = json.dumps(data_list)
    return Response(
        status=200,
        response=data_json,
        mimetype='application/json'
    )