from flask import Blueprint, request, render_template

from web_app.models import User, Tweet
from web_app.services import spacy_service
from web_app.services.spacy_service import nlp

from web_app.models import db

from sklearn.linear_model import LogisticRegression


stats_routes = Blueprint("stats_route", __name__)

@stats_routes.route("/predict", methods=["POST"])
def predict():
    print("Predict Route...")
    print("Form Data:", dict(request.form))
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    user_a = User.query.filter_by(screen_name=screen_name_a).first()
    user_b = User.query.filter_by(screen_name=screen_name_b).first()
    user_a_tweets = user_a.tweets
    user_b_tweets = user_b.tweets
    print("Users fetched from db:", user_a, user_b)

    embeddings_a = [
    tweet.embedding for tweet in user_a_tweets
    ]
    embeddings_b = [
    tweet.embedding for tweet in user_b_tweets
    ]
    embeddings = embeddings_a + embeddings_b

    labels = ([screen_name_a] * len(embeddings_a))+([screen_name_b] * len(embeddings_b))

    classifier = LogisticRegression()

    classifier.fit(embeddings, labels)
    tweet_text = request.form["tweet_text"]
    most_likey_tweeter = classifier.predict([nlp(tweet_text).vector])[0]

    return render_template("prediction_results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely=most_likey_tweeter
    )
