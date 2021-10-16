# web_app/routes/twitter_routes.py

from flask import Blueprint, jsonify, render_template, request, flash, redirect
# from pprint import pprint

from web_app.models import db, User, Tweet, parse_records
from web_app.services.twitter_service import api as twitter_api


twitter_routes = Blueprint("twitter_routes", __name__)

@twitter_routes.route("/users/<screen_name>/fetch")
def get_user(screen_name=None):
    print(screen_name)
    api = twitter_api
    twitter_user = api.get_user(screen_name=screen_name)
    statuses = api.user_timeline(screen_name=screen_name, tweet_mode="extended", count=35, exclude_replies=True, include_rts=False)
    print("Statuses count:", len(statuses))
    # return jsonify({"user": user._json, "num_tweets": len(statuses)})

    # get user from db or create new one
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()
    return "OK"

    # fetch embedding for each tweet


    # TODO: store tweets in database (w/ embeddings)

    # return f"FETCHED {screen_name} OK"

