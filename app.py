from flask import Flask,render_template
import requests
import datetime


app = Flask(__name__)



def fetch_spacex():
    response = requests.get("https://api.spacexdata.com/v4/launches")
    if response.status_code == 200:
        return response.json()
    else:
        return []
    


def categorize_launches(Launches):
    success = list(filter(lambda x:x['success'] and not x['upcoming'],Launches))
    failure = list(filter(lambda x:not x['success'] and not x['upcoming'],Launches))
    upcoming = list(filter(lambda x:x['upcoming'],Launches))

    return {
            "successful":success,
            "failure":failure,
            "upcoming":upcoming
        }

Launches = categorize_launches(fetch_spacex())

@app.route("/")
def index():
    return render_template("success.html",launches = Launches)

@app.route("/failure")
def failure():
    return render_template("failure.html",launches = Launches)

@app.route("/upcoming")
def upcoming():
    return render_template("upcoming.html",launches = Launches)
    

  
if __name__ == "__main__":
    app.run(debug=True)
