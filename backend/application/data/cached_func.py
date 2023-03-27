from application.data.models import Posts
from sqlalchemy import desc
from main import cache

@cache.memoize(120)
def get_posts_by_username(username):
    return Posts.query.filter_by(posted_by = username).order_by(desc(Posts.timestamp)).all()




