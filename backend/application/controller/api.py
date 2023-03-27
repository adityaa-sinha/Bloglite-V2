from datetime import datetime
from flask_restful import Resource, fields, marshal_with,reqparse
from flask_security import auth_required, current_user
from application.data.database import db
from application.data.models import *
from application.utils.validation import *
from sqlalchemy import desc
from flask import jsonify
from application.data import cached_func
from main import cache


#==================Get current user===============================

current_user_fields = {
    'username': fields.String,
}
class GetCurrentUser(Resource):
    @auth_required('token')
    @marshal_with(current_user_fields)
    def get(self):
        return current_user

#=======================Search API=======================================

search_parser = reqparse.RequestParser()
search_parser.add_argument("username")
search_result_fields = {"dp_url":fields.String, "username": fields.String }

class SearchAPI(Resource):
    @auth_required('token')
    @marshal_with(search_result_fields)
    def post(self):
        args = search_parser.parse_args()
        username = args.get("username", None)
        if username is None:
            raise BusinessValidationError(400,'S001','Supply username to search')
        elif username == '':
            raise BusinessValidationError(400,'S002','Type to search....') # if this is not specified, all the users are retured which is not required
        else:
            search_query = username+"%"
            search_results = User.query.filter(User.username.like(search_query)).all()
            return search_results
        

#======================Feed API=====================================

feed_fields = {
    'id' : fields.Integer,
    'title':fields.String,
    'caption':fields.String,
    'image_url':fields.String,
    'timestamp': fields.DateTime,
    'posted_by': fields.String
}
class FeedAPI(Resource):
    @auth_required('token')
    @marshal_with(feed_fields)
    def get(self):
        f = UserFollows.query.filter_by(user_id = current_user.id).all() #Fields of those users that the current_user follows
        if f==[]:
            raise BusinessValidationError(400,'Feed001','Follow someone to see their posts')
        f_follows = [i.follows for i in f] #User ids of those users that the current user follows
        #Getting usernames of such users
        fn = User.query.filter(User.id.in_(f_follows)).all()
        fn_username = [i.username for i in fn]
        #Getting posts of such users
        posts = Posts.query.filter(Posts.posted_by.in_(fn_username)).order_by(desc(Posts.timestamp)).all()
        if posts==[]:
            raise BusinessValidationError(400,'Feed002',"The people you follow haven't made a post yet.")
        return posts


#======================UserStatsAPI=======================================

class UserStatsAPI(Resource):
    @auth_required('token')
    def get(self, username):
        user = User.query.filter_by(username = username).first()
        if user is None:
            raise BusinessValidationError(400,'Stats001','User does not exist.') # Necessary, because username is provided by client
        posts = len(Posts.query.filter_by(posted_by = username).all())
        followers = len(UserFollows.query.filter_by(follows = user.id).all())
        following = len(UserFollows.query.filter_by(user_id = user.id).all())
        user_dp = user.dp_url
        is_current_user = False
        if username == current_user.username:
            is_current_user = True
        is_current_user_following = False
        following_check = UserFollows.query.filter_by(user_id = current_user.id, follows=user.id).first()
        if following_check:
            is_current_user_following = True
        return jsonify({
            "user_dp": user_dp,
            "is_current_user": is_current_user,
            "is_current_user_following":is_current_user_following,
            "posts":posts,
            "followers" : followers,
            "following":following
        })
    

#====================UserPosts=============================================

class UserPostsAPI(Resource):
    @auth_required('token')
    @marshal_with(feed_fields)
    def get(self, username):
        user = User.query.filter_by(username = username).first()
        if user is None:
            raise BusinessValidationError(400,'UserPosts001','User does not exist.') # Necessary, because username is provided by client
    
        # Using cached function
        user_posts = cached_func.get_posts_by_username(username) #Cached function

        return user_posts
    


#=======================Follow & Unfollow API==================================================

follow_result = {"msg":fields.String}
follow_parser = reqparse.RequestParser()
follow_parser.add_argument("target_username")

class FollowApi(Resource):
    @auth_required('token')
    @marshal_with(follow_result)
    def post(self):
        args = follow_parser.parse_args()
        target_username = args.get("target_username",None)
        if target_username is None:
            raise BusinessValidationError(400,'F001','Please specify a user to follow')
        if target_username == current_user.username:
            raise BusinessValidationError(400,'F002','You cannot follow yourself')
        
        target_user = User.query.filter_by(username = target_username).first()
        if target_user is None:
            raise BusinessValidationError(400,'F003','The user you wish to follow does not exist.')
        
        follow_check = UserFollows.query.filter_by( user_id = current_user.id, follows = target_user.id).first()
        if follow_check:
            raise BusinessValidationError(400,'F004','You are already following this user.')
        
        new = UserFollows(user_id = current_user.id, follows = target_user.id)
        db.session.add(new)
        db.session.commit()
        result = {"msg": "Follow successful!"}
        return result, 201
    
class UnFollowApi(Resource):
    @auth_required('token')
    @marshal_with(follow_result)
    def post(self):
        args = follow_parser.parse_args()
        target_username = args.get("target_username",None)
        if target_username is None:
            raise BusinessValidationError(400,'UF001','Please specify a user to unfollow')
        if target_username == current_user.username:
            raise BusinessValidationError(400,'UF002','You cannot unfollow yourself')
        
        target_user = User.query.filter_by(username = target_username).first()
        if target_user is None:
            raise BusinessValidationError(400,'UF003','The user you wish to unfollow does not exist.')
        
        follow_check = UserFollows.query.filter_by( user_id = current_user.id, follows = target_user.id).first()
        if follow_check is None:
            raise BusinessValidationError(400,'UF004','You are not yet following this user.')
        
        db.session.delete(follow_check)
        db.session.commit()
        result = {"msg": "Unfollow successful!"}
        return result, 201

# ==================Get followers and following of a user==========

class GetFollowers(Resource):
    @auth_required('token')
    @marshal_with(search_result_fields)
    def get(self, username):
        user = User.query.filter_by(username = username).first()
        if user is None:
            raise BusinessValidationError(400,'GF001','User does not exist.') # Necessary, because username is provided by client
        user_followers = UserFollows.query.filter_by(follows=user.id).all()
        uf = [i.user_id for i in user_followers]
        followers = User.query.filter(User.id.in_(uf)).all()
        return followers

class GetFollowing(Resource):
    @auth_required('token')
    @marshal_with(search_result_fields)
    def get(self, username):
        user = User.query.filter_by(username = username).first()
        if user is None:
            raise BusinessValidationError(400,'GFo001','User does not exist.') # Necessary, because username is provided by client
        user_following = UserFollows.query.filter_by(user_id=user.id).all()
        ufo = [i.follows for i in user_following]
        following = User.query.filter(User.id.in_(ufo)).all()
        return following
    
#=================== CRUD on Blog ========================================

blog_parser = reqparse.RequestParser()
blog_parser.add_argument("title")
blog_parser.add_argument("caption")
blog_parser.add_argument('image_url')

blog_update_parser = reqparse.RequestParser()
blog_update_parser.add_argument("title")
blog_update_parser.add_argument("caption")


class BlogAPI(Resource):
    @auth_required('token')
    @marshal_with(feed_fields)
    def post(self):
        args = blog_parser.parse_args()
        title = args.get('title',None)
        caption = args.get('caption',None)
        image_url = args.get('image_url',None)

        if title is None:
            raise BusinessValidationError(400, 'B001', 'Title cannot be empty.')
        if caption is None:
            raise BusinessValidationError(400, 'B002', 'Caption cannot be empty.')
        if image_url is None:
            raise BusinessValidationError(400, 'B003', 'image_url cannot be empty.')
        
        new = Posts(title=title, caption=caption, image_url = image_url , timestamp = datetime.now(), posted_by = current_user.username)
        db.session.add(new)
        db.session.commit()
        cache.delete_memoized(cached_func.get_posts_by_username, current_user.username )
        return new, 201
    
    @auth_required('token')
    @marshal_with(feed_fields)
    def get(self, id):
        blog = Posts.query.filter_by(id = id).first()
        if blog is None:
            raise BusinessValidationError(400,'B004','Blog not found.')
        return blog
    
    @auth_required('token')
    def delete(self, id):
        blog = Posts.query.filter_by(id = id).first()
        if blog is None:
            raise BusinessValidationError(400,'B004','Blog not found.')
        if blog.posted_by != current_user.username:
            raise BusinessValidationError(403,'B005','You are not allowed to delete this blog.')
        db.session.delete(blog)
        db.session.commit()
        cache.delete_memoized(cached_func.get_posts_by_username, current_user.username )
        return '', 200
    
    @auth_required('token')
    @marshal_with(feed_fields)
    def put(self, id):
        blog = Posts.query.filter_by(id = id).first()
        if blog is None:
            raise BusinessValidationError(400,'B004','Blog not found.')
        if blog.posted_by != current_user.username:
            raise BusinessValidationError(403,'B006','You are not allowed to edit this blog.')
        
        args = blog_update_parser.parse_args()
        title = args.get('title',None)
        caption = args.get('caption',None)

        if title is None:
            raise BusinessValidationError(400, 'B001', 'Title cannot be empty.')
        if caption is None:
            raise BusinessValidationError(400, 'B002', 'Caption cannot be empty.')
        
        blog.title = title
        blog.caption = caption
        db.session.commit()
        cache.delete_memoized(cached_func.get_posts_by_username, current_user.username )
        return blog, 200