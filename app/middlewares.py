from flask import request, g
from .models import Post, db

def init_view_counter(app):
    @app.before_request
    def before_request():
        g.view_counted = False

    @app.after_request
    def after_request(response):
        if not g.view_counted and request.endpoint == 'main.article':
            slug = request.view_args.get('slug')
            if slug:
                post = Post.query.filter_by(slug=slug).first()
                if post:
                    post.views += 1
                    db.session.commit()
                    g.view_counted = True
        return response