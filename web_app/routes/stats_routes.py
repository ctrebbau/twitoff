from flask import Blueprint, request, render_template

from web_app.models import User, Tweet

from web_app.services import spacy_service

stats_routes = Blueprint("stats_route", __name__)

@stats_routes.route("/predict", methods=["POST"])
def predict():
    print("Predict Route...")
    print("Form Data:", dict(request.form))
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    return render_template("prediction_results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely="TODO"
    )
