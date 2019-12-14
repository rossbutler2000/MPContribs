from flask import current_app, render_template, url_for
from flask_mongoengine import Document
from mongoengine.fields import StringField, BooleanField, DictField, URLField, MapField, EmailField
from mongoengine import signals


class Projects(Document):
    __project_regex__ = '^[a-zA-Z0-9_]{3,31}$'
    project = StringField(
        min_length=3, max_length=30, regex=__project_regex__, primary_key=True,
        help_text=f"project name/slug (valid format: `{__project_regex__}`)"
    )
    is_public = BooleanField(required=True, default=False, help_text='public/private project')
    title = StringField(
        min_length=5, max_length=40, required=True, unique=True,
        help_text='(short) title for the project/dataset'
    )
    authors = StringField(
        required=True, help_text='comma-separated list of authors'
    )
    description = StringField(
        min_length=5, max_length=1500, required=True,
        help_text='brief description of the project'
    )
    urls = MapField(URLField(), required=True, help_text='list of URLs for references')
    other = DictField(help_text='other information')
    owner = EmailField(required=True, unique_with='project', help_text='owner / corresponding email')
    is_approved = BooleanField(required=True, default=False, help_text='project approved?')
    meta = {'collection': 'projects', 'indexes': ['is_public', 'owner', 'is_approved']}

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        admin_email = current_app.config['ADMIN_EMAIL']
        if kwargs.get('created'):
            email_project = f'{document.owner} {document.project}'
            ts = current_app.config['USTS']
            tokens = [ts.dumps(email_project, salt=f'{action}-project') for action in ['approve', 'deny']]
            links = [url_for('projects.applications', token=t, _external=True) for t in tokens]
            subject = f'[MPContribs] New project "{document.project}"'
            hours = int(current_app.config['USTS_MAX_AGE'] / 3600)
            html = render_template(
                'admin_email.html', doc=document.to_mongo(),
                links=links, admin_email=admin_email, hours=hours
            )
            print(html)
            #send_email(admin_email, subject, html)  # TODO
        else:
            set_keys = document._delta()[0].keys()
            if 'is_approved' in set_keys and document.is_approved:
                subject = f'[MPContribs] Your project "{document.project}" has been approved'
                html = render_template('owner_email.html', approved=True, admin_email=admin_email)
                print(html)
                #send_email(document.owner, subject, html)  # TODO

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        admin_email = current_app.config['ADMIN_EMAIL']
        subject = f'[MPContribs] Your project "{document.project}" has been deleted'
        html = render_template('owner_email.html', approved=False, admin_email=admin_email)
        print(html)
        #send_email(document.owner, subject, html)  # TODO

signals.post_save.connect(Projects.post_save, sender=Projects)
signals.post_delete.connect(Projects.post_delete, sender=Projects)
