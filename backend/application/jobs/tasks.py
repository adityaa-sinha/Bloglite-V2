from application.jobs.workers import celery
from datetime import datetime
from celery.schedules import crontab
from application.data.models import User, Posts, UserFollows
from sqlalchemy import desc
from application.controller.email import send_reminder_email, send_monthly_report
import csv
from flask import current_app as app
import os
    
@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0,hour=17), # Daily reminder job at 5.00 PM
        daily_reminder.s(),
        name="Daily reminder" 
        )
    
    sender.add_periodic_task(crontab(minute=0, hour=17, day_of_month=1), # Monthly report on day 1 of every month at 5:00 PM
        monthly_report.s(),
        name="Monthly report" 
        )


# Daily reminder job at 5:00 PM
@celery.task()
def daily_reminder():
    users = User.query.all()
    for user in users:
        last_post = Posts.query.filter_by(posted_by=user.username).order_by(desc(Posts.timestamp)).first()
        if last_post:
            days_count =int((datetime.now() - last_post.timestamp).total_seconds()/86400)
            if (days_count>=1):
                send_reminder_email(user.email, user.username,days_count)
                # print(user.email)
        else:
            pass

# Monthly report on day 1 of every month at 5:00 PM
@celery.task
def monthly_report():
    users = User.query.all()
    for user in users:
        followers_count =len(UserFollows.query.filter_by(follows = user.id).all())
        following_count =len(UserFollows.query.filter_by(user_id = user.id).all())
        posts = Posts.query.filter_by(posted_by=user.username).all()
        posted_thismonth = 0
        now = datetime.now()
        for blog in posts:
            if blog.timestamp.month == now.month:
                posted_thismonth+=1
        total_posts = len(posts)
        data = {
            "total_posts": total_posts,
            "followers_count":followers_count,
            "following_count":following_count,
            "posted_thismonth": posted_thismonth
        }
        send_monthly_report(user.email, user.username, now.strftime('%B'), data)


# User triggered job
@celery.task()
def export_as_csv(username):
    user_posts = Posts.query.filter_by(posted_by = username).all()
    filename = username + '-blogs.csv'
    filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)
    with open (filepath, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Caption', 'Timestamp'])
        if user_posts:
            for blog in user_posts:
                writer.writerow([blog.title, blog.caption, blog.timestamp])
    return filename
    

    
