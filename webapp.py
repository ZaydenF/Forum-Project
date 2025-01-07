import pymongo
from flask import Flask, request, render_template, flash, url_for
from markupsafe import Markup
from flask import redirect
from flask import session
import os
import sys
import pprint
from flask_oauthlib.client import OAuth
from flask import render_template
from markupsafe import Markup
from pymongo import DESCENDING


app = Flask(__name__)

app.debug = False #Change this to False for production
#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #Remove once done debugging

app.secret_key = os.environ['SECRET_KEY'] #used to sign session cookies
oauth = OAuth(app)
oauth.init_app(app) #initialize the app to be able to make requests for user information

#Set up GitHub as OAuth provider
github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'], #your web app's "username" for github's OAuth
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],#your web app's "password" for github's OAuth
    request_token_params={'scope': 'user:email'}, #request read-only access to the user's email.  For a list of possible scopes, see developer.github.com/apps/building-oauth-apps/scopes-for-oauth-apps
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',  
    authorize_url='https://github.com/login/oauth/authorize' #URL for github's OAuth login
)


#context processors run before templates are rendered and add variable(s) to the template's context
#context processors must return a dictionary 
#this context processor adds the variable logged_in to the conext for all templates
@app.context_processor
def inject_logged_in():
    is_logged_in = 'github_token' in session #this will be true if the token is in the session and false otherwise
    return {"logged_in":is_logged_in}

@app.route('/')
def home():
    
    
    firstPost=get_posts()
    if 'user_data' in session:
        followers = session['user_data']['followers']
    else:
        followers = 'no'; #needs fixing
        firstPost=get_posts()  
    return render_template('home.html', follower_user_data=followers, firstPost = firstPost)
@app.route('/ForumOne',methods=['GET','POST'])
def renderForumOneAnswers():
    firstPost=get_posts()
    if "user_data" in session:
        firstPost=request.form['ques1']
        doc = {"username":session['user_data']['login'], "number":"ee","text":firstPost}
     
        collection.insert_one(doc)
    for anything in collection.find():
        firstPost=anything["text"]
        firstPost=get_posts()
    return render_template('home.html',firstPost = firstPost)

def get_posts():
    option = []
    for s in collection.find():
        formatted_post = f"<pre>{s['username']} : {s['text']}</pre>"
        option.append(formatted_post)
    
    return Markup((option))

#redirect to GitHub's OAuth page and confirm callback URL
@app.route('/login')
def login():   
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='http')) #callback URL must match the pre-configured callback URL

@app.route('/logout')
def logout():
    session.clear()
    return render_template('message.html', message='You were logged out')

@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None:
        session.clear()
        message = 'Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args)      
    else:
        try:
            session['github_token'] = (resp['access_token'], '') #save the token to prove that the user logged in
            session['user_data']=github.get('user').data
            #pprint.pprint(vars(github['/email']))
            #pprint.pprint(vars(github['api/2/accounts/profile/']))
            message='You were successfully logged in as ' + session['user_data']['login'] + '.'
        except Exception as inst:
            session.clear()
            print(inst)
            message='Unable to login, please try again.  '
    return render_template('message.html', message=message)



@app.route('/googleb4c3aeedcc2dd103.html')
def render_google_verification():
    return render_template('googleb4c3aeedcc2dd103.html')


#the tokengetter is automatically called to check who is logged in.
@github.tokengetter
def get_github_oauth_token():
    return session['github_token']



connection_string = os.environ["MONGO_CONNECTION_STRING"]
db_name = os.environ["MONGO_DBNAME"]

client = pymongo.MongoClient(connection_string)
db = client[db_name]
collection = db['Forum_pro'] #1. put the name of your collection in the quotes

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

    #2. add a document to your collection using the insert_one method

    
    #3. print the number of documents in the collection
    
    #4. print the first document in the collection
    
    #5. print all documents in the collection
    
    #6. print all documents with a particular value for some attribute
    #ex. print all documents with the birth date 12/1/1990
    
    
if __name__=="__main__":
    app.run()