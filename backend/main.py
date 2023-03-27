# Imports

import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from application.data.database import db
from application.jobs import workers
from application.data.models import User, Role
from flask_security import Security, SQLAlchemyUserDatastore
from flask_caching import Cache


app = None
api = None
celery = None
cache = None

def create_app():
    app = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Starting Local Development")
      app.config.from_object(LocalDevelopmentConfig) # App config
    
    # Database setup
    db.init_app(app)
    app.app_context().push()

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore) 

    # API setup
    api = Api(app)
    app.app_context().push()

    #Create celery
    celery = workers.celery
    #Update with configuration
    celery.conf.update(
       broker_url = app.config["CELERY_BROKER_URL"],
       result_backend = app.config["CELERY_RESULT_BACKEND"]
    )    
    #use our ContextTask instead of built-in Task
    celery.Task = workers.ContextTask
    app.app_context().push()

    #Cache setup
    cache = Cache(app)
    app.app_context().push()

    # CORS setup 
    CORS(app)  
    return app, api, celery, cache

app,api,celery,cache = create_app()


from application.data import cached_func

from application.controller.api import FollowApi, SearchAPI, FeedAPI, UserStatsAPI, UserPostsAPI, GetCurrentUser, BlogAPI, UnFollowApi, GetFollowers, GetFollowing

api.add_resource(FollowApi, "/api/follow")
api.add_resource(SearchAPI, "/api/search")
api.add_resource(FeedAPI, "/api/feed")
api.add_resource(UserStatsAPI, "/api/stats/<string:username>")
api.add_resource(UserPostsAPI, "/api/posts/<string:username>")
api.add_resource(GetCurrentUser, "/api/currentuser")
api.add_resource(BlogAPI, '/api/blog', '/api/blog/<int:id>')
api.add_resource(UnFollowApi, '/api/unfollow')
api.add_resource(GetFollowers, '/api/followers/<string:username>')
api.add_resource(GetFollowing, '/api/following/<string:username>')


#================File upload=====================
from application.controller.upload import *

# ===============Controllers=====================
from application.controller.controllers import *


if __name__ == '__main__':
  # Run the Flask app
  app.run()
