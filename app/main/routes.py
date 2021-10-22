from app.main import bp
import datetime
from app import db
from app.models import Lead
from flask import flash, redirect, url_for, render_template
from app.main.forms import LeadCaptureForm
from app.main.email import send_alert_email

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = LeadCaptureForm()
    if form.validate_on_submit():
        lead = Lead()
        lead.first_name = str(form.first_name.data)
        lead.last_name = str(form.last_name.data)
        lead.email = str(form.email.data)
        lead.phone_number = str(form.phone_number.data)
        lead.category = int(form.category.data)
        lead.can_contact = True
        lead.timestamp = datetime.datetime.utcnow()
        db.session.add(lead)
        db.session.commit()
        flash("Thank you for your interest. We'll be in touch!")
        send_alert_email(lead=lead)
        return redirect(url_for('main.index'))
    return render_template(
        'main/index.html',
        title='Title',
        description='Description',
        form=form
    )


@bp.route('/unsubscribe/<email>')
def unsubscribe(email):
    u = Lead.query.filter_by(email=str(email)).first_or_404()
    u.can_contact = False
    db.session.commit()
    flash("You have been removed from our mailing list. Sorry for the inconvenience!")
    return redirect(url_for('main.index'))