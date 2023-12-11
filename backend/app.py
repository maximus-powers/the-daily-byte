from flask import Flask, jsonify, request, Response, send_file
from flask_cors import CORS
from llmObject import LLMObject
from newsObject import NewsObject
from dbObject import dbObject
from landingObject import landingObject
from ttsObject import TTSObject
from econObject import EconObject
from apscheduler.schedulers.background import BackgroundScheduler # for scheduling the refresh_content function in the bg
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()
db_obj = dbObject()
llm_obj = LLMObject()
news_obj = NewsObject()
landing_obj = landingObject()
tts_obj = TTSObject()
econ_obj = EconObject()

################# USER ####################
# I ditched users for now, but it's here to add later

# 'Email', 'Password', 'fName', 'Categories' in the header
# do I need to do some check here to prevent signup spamming
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    email = request.headers.get('Email')
    password = request.headers.get('Password')
    first_name = request.headers.get('fName')
    categories = request.headers.get('Categories')

    db_obj.add_user(email, password, first_name, categories)
    return jsonify({"success": "User added successfully"}), 200    

# 'Email' and 'Categories' in the header
@app.route('/update_settings', methods=['GET', 'POST'])
def update_settings():
    email = request.headers.get('Email')
    categories = request.headers.get('Categories')

    db_obj.update_user_settings(email, categories)
    return jsonify({"success": "User settings updated successfully"}), 200

# 'Email' and 'Password' in the header
@app.route('/auth_user', methods=['GET', 'POST'])
def auth_user():
    email = request.headers.get('Email')
    password = request.headers.get('Password')

    if db_obj.auth_user(email, password): # if user is authenticated
        return jsonify({"success": "User authenticated successfully"}), 200
    else: # if not
        return jsonify({"error": "User authentication failed"}), 401



################# NEWS ####################            
@app.route('/get_content')
def get_content():
    user_id = 2 # hard coded to 2 (the general user id, for anyone). add signups later that get  user id from email
    db_content = db_obj.call_all_content(user_id)

    print('JSON sent')
    # db_content = {
        # userID: int,
        # firstName:  str,
        # vol: int,
        # landing: n,
        # audioFile: str?
        # statsData: {markets:{}, economy:{}}, 
        # categories: {category: [{headline: str, summary: str, url: str}, ...], ...}
    # }

    return jsonify(db_content)


'''FUNCTIONS'''
def refresh_content():
    print('Running refresh content')
    category_list = db_obj.get_user_categories(2).split(',')

    results = {category: [] for category in category_list} # need to init this here with all the categories for the loop to populate

    ############## REFRESH CATEGORIES ##############
    for category in category_list:
        if not db_obj.records_today_exist(2, category): # checks if content has been refreshed today (for each category)
            
            # handles if there's been a new category added. Not really important to the logic
            if not db_obj.table_exists(category): 
                db_obj.create_category_table(category)
                # no handling for updating the categories field in user

            # call news api
            articles_ordered = news_obj.call_news(category)  # returns: list of {headline: str, url: str}

            # rewrite the top three headlines an summarize them
            results[category] = []
            i = 0
            while len(results[category]) < 3:
                new_headline = llm_obj.rewrite_headline(articles_ordered[i]['headline'])
                summary = llm_obj.summarize_article(articles_ordered[i]['url'], 750)
                if summary is not False:
                    results[category].append({'headline': new_headline, 'summary': summary, 'url': articles_ordered[i]['url']})
                i += 1
                
            # update the category table of db
            db_obj.update_category_content(2, category, results[category])

    ############## REFRESH LANDING ##############
    if not db_obj.record_exists_today_landing(2):
    # gen content and parse return dict
        landing_content = landing_obj.gen_landing_content(2)
        headline = landing_content['headline']
        summary = landing_content['summary']
        alt_text = landing_content['alt_text']
        image_blob = landing_content['image_blob']

        # update db
        db_obj.update_landing(2, alt_text, image_blob, headline, summary)
        db_obj.update_user_vol(2)

    ############## REFRESH AUDIO ##############
    if not db_obj.record_exists_today_audio(2):
        all_content = db_obj.call_all_content(2) # call data to use in script
        script = llm_obj.generate_script(all_content['categories']) # generate a script
        audio_and_script = tts_obj.script_to_audio(script) # call tts
        db_obj.add_audio_file(2, audio_and_script['audio'], audio_and_script['script']) # update the db

    ############### REFRESH ECON DATA ##############
    econ_data = econ_obj.get_econ_data()
    db_obj.update_econ_data(2, econ_data)


scheduler = BackgroundScheduler()
scheduler.add_job(func=refresh_content, trigger=CronTrigger(hour=6, minute=30)) # runs at 4am
scheduler.start()
# refresh_content() # run it once on startup

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()