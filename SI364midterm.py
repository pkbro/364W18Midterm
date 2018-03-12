###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, RadioField # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy
import tweepy

consumer_k = "A9n9NyAfn4Hn8qLO5IcWNUOxq"
consumer_s = "K5t8z2PwJfl3KQKweMR3k03QTLVyVUd7czT22UkmqEIAyFw4xD"
access_t = 	"921084179328139264-IJUPDke6Chv5Ht7EQrs3titSSneGb74"
access_s = 	"hqEMQJWjCLl23hWHhDsV5ZIebCzi7qZckhhni54veVoqT"

auth = tweepy.OAuthHandler(consumer_k, consumer_s)
auth.set_access_token(access_t, access_s)

api = tweepy.API(auth)



## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string from si364'
## All app.config values
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/pkbro364Midterm"
## Provided:
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################
def get_or_create_user(username):

    u = User.query.filter_by(username = username).first()
    if u:
        return u
    else:
        try:
            resp = api.get_user(username.lower())
            u = User(username= "@"+resp.screen_name,fullname=resp.name,followers=resp.followers_count,desc=resp.description,likes=resp.favourites_count, tweet_count=resp.statuses_count)
            db.session.add(u)
            db.session.commit()
            return u
        except:
            return "User does not exist."

def get_or_create_tweets(username, count):

    user = get_or_create_user(username)
    if type(user) == str:
        return "This is not a real account."
    else:
        t = Tweet.query.filter_by(user_id = user.id).first()
        if t:
            resp = api.user_timeline(username, count=count,tweet_mode='extended')
            tweet_l = []
            #Functionality to return duplicate data but not save it
            if Tweet.query.filter_by(user_id=user.id).first():
                for user_tweet in resp:
                    tweet = Tweet(text=user_tweet.full_text,retweets=user_tweet.retweet_count,likes=user_tweet.favorite_count, user_id=user.id)
                    tweet_l.append(tweet)
                return tweet_l
        else:
            try:
                resp = api.user_timeline(username, count=count,tweet_mode='extended')
                tweet_l = []
                for user_tweet in resp:
                    tweet = Tweet(text=user_tweet.full_text,retweets=user_tweet.retweet_count,likes=user_tweet.favorite_count, user_id=user.id)
                    tweet_l.append(tweet)
                    db.session.add(tweet)
                    db.session.commit()
                return tweet_l
            except:
                return "This user is private. Unable to grab tweets."



##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64))
    fullname = db.Column(db.String(64))
    followers = db.Column(db.Integer)
    tweet_count = db.Column(db.Integer)
    tweets = db.relationship("Tweet", backref='User')
    desc = db.Column(db.String(200))
    likes = db.Column(db.Integer)

    def __repr__(self):
        return "{}, {}. {}. Followers: {} Likes: {}".format(self.username, self.fullname,self.desc, self.followers,self.likes)

class Tweet(db.Model):
    __tablename__ = "tweet"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(340))
    retweets = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "Tweet: {} Retweets: {} Likes: {} \n User: {}".format(self.text, self.retweets, self.likes,User.query.filter_by(id=self.user_id).first().username)


###################
###### FORMS ######
###################

class NameForm(FlaskForm):
    name = StringField("Please enter your name: ",validators=[Required()])
    submit = SubmitField()


def user_validate(form, field):
    if field.data[0] != "@" or len(field.data.split()) > 1:
        raise ValidationError("The @ symbol must be the first character in the entry. Entry must also not include spaces.")


class UserForm(FlaskForm):

    username = StringField("Enter a username (must start with @ and contain no spaces): ", validators=[Required(),Length(max=64,message="Length must be less than 64 characters"),user_validate])
    submit = SubmitField()

class NumTweetsForm(FlaskForm):

    username = StringField("Enter a username (must start with @ and contain no spaces): ", validators=[Required(),Length(max=64,message="Length must be less than 64 characters"),user_validate])
    number_of_tweets = RadioField("How many tweets do you want retrieved?",choices=[('10', 10),('20', 20),('30',30)],validators=[Required()])
    submit = SubmitField()



#######################
###### VIEW FXNS ######
#######################


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['POST', 'GET'])
def home():
    form = NameForm()
    num_users = len(Name.query.all())

    if form.validate_on_submit():
        if Name.query.filter_by(name=form.name.data).first():
            flash("You've already saved this user as someone who has used this application")
            name_l = Name.query.all()
            return redirect(url_for('home'))
        else:
            name = form.name.data
            newname = Name(name=name)
            db.session.add(newname)
            db.session.commit()
            num_users = len(Name.query.all())
            flash("Saved successfully")
            return render_template('home.html', form=form,num_users=num_users)
    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("There are errors in your submission: " + str(errors))
    return render_template('home.html',form=form, num_users = num_users)

@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('name_example.html',names=names)

@app.route('/username', methods=['POST','GET'])
def user_name():
    form = UserForm()
    return render_template('userform.html', form=form)


@app.route('/numtweets', methods=['POST','GET'])
def numtweets():
    form = NumTweetsForm()
    if form.validate_on_submit():
        username = form.username.data
        try:
            r = api.get_user(username)
            count = form.number_of_tweets.data
            u = User.query.filter_by(username='@'+r.screen_name).first()
            if u:
                if Tweet.query.filter_by(user_id=u.id).first():
                    t = get_or_create_tweets(username=username,count=count)
                    flash("You've already grabbed and saved tweets by this user.")
                    return render_template('list_tweets.html', list_tweets=t)
                else:
                    t = get_or_create_tweets(username=username,count=count) #gives us list of Tweet instances
                    if type(t) == str:
                        flash(t)
                        return render_template('numtweets.html', form=form)
                    flash("Tweets of " + username)
                    flash("To see tweets from all users, go the link to see all tweets.")
                    return render_template('list_tweets.html', list_tweets=t)
            else:

                t = get_or_create_tweets(username=username,count=count) #gives us list of Tweet instances
                if type(t) == str:
                    flash(t)
                    return render_template('numtweets.html', form=form)
                flash("Tweets of " + username)
                flash("To see tweets from all users, go the link to see all tweets.")
                return render_template('list_tweets.html', list_tweets=t, form=form)
        except:
            flash("User does not exist")
            return render_template('numtweets.html', form=form)
    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("There are errors in your submission: " + str(errors))
    return render_template('numtweets.html', form = form)



@app.route('/list_tweets', methods=["POST",'GET'])
def list_tweets():
    list_tweets = []
    tweets = Tweet.query.all()
    for tweet in tweets:
        user = User.query.filter_by(id = tweet.user_id).first()
        list_tweets.append((tweet.text, tweet.retweets, tweet.likes, user.username))

    return render_template('list_tweets.html', list_tweets=list_tweets)

@app.route('/list_users', methods = ['POST', 'GET'])
def list_users():
    users = User.query.all()
    user_l = []
    if request.args:

        username= request.args['username']
        if username[0] != "@" or len(username.split()) > 1:
            flash("The @ symbol must be the first character in the entry. Entry must also not include spaces.")
            return redirect(url_for('user_name'))
            try:
                r = api.get_user(username)
                u = User.query.filter_by(username= "@" + r.screen_name).first()
                if u:
                    flash("You've already saved this user.")
                    return redirect(url_for('user_name'))
                else:
                    u = get_or_create_user(username=username)
                    print(username)
                    users = User.query.all()
                    flash("Saved successfully")
                    for user in users:
                        user_l.append((user.username, user.fullname, user.desc, user.followers, user.likes, user.tweets, user.tweet_count))
                    return render_template('list_users.html', users = user_l)
            except:
                flash("User does not exist")
                return redirect(url_for('user_name'))

    for user in users:
        user_l.append((user.username, user.fullname, user.desc, user.followers, user.likes, user.tweets, user.tweet_count))

    return render_template('list_users.html',users =user_l)


@app.route('/list_names')
def list_names():
    names = Name.query.all()
    name_l = []
    for name in names:
        name_l.append(name.name)
    return render_template('name_example.html', name_l = name_l)

if __name__ == "__main__":
    db.create_all()
    app.run(use_reloader=True,debug=True)
