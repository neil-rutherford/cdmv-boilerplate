from app.api import bp
from app.models import User
from flask import Response, abort

@bp.route('/_api/read/leads')
def read_leads():
    try:
        users = User.query.filter_by(category='BUYER').order_by(User.timestamp.desc()).all()
        data_list = []
        for x in users:
            data_dict = {
                'id': x.id,
                'first_name': x.first_name,
                'last_name': x.last_name,
                'email': x.email,
                'category': x.category,
                'can_contact': x.can_contact,
                'timestamp': x.timestamp
            }
            data_list.append(data_dict)
        data_json = json.dumps(data_list)
        return Response(
            status=200,
            response=data_json,
            mimetype='application/json'
        )
    except Exception as e:
        abort(500, description="{}".format(e))