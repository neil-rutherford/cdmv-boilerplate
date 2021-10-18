from app.api import bp

@bp.route('/_api/create/content')

@bp.route('/_api/read/content/<slug>')

@bp.route('/_api/update/content/<slug>')

@bp.route('/_api/delete/content/<slug>')