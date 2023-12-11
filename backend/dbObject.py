import pymysql
from datetime import datetime
import json
import base64
import os
from dotenv import load_dotenv


load_dotenv()
class dbObject:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.setup()

    # DB setup and connection
    def setup(self):
        self.conn = None
        self.cur = None
        self.fields = []
        self.data = [] #data is a list of dictionaries representing rows in our table
        self.conn = pymysql.connect(host=os.getenv('db_host'), port=3306, user=os.getenv('db_user'),
                       passwd=os.getenv('db_passwd'), db=os.getenv('db_name'), autocommit=True)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        print("Database connection established: " + os.getenv('db_name'))

    # only for use in app.py
    def close(self):
        self.cur.close()
        self.conn.close()
        print("Database connection closed: " + os.getenv('db_name'))


########################### User functions #########################

    def get_user_id(self, email):
        try:
            query = "SELECT userID FROM `user` WHERE `email` = %s"
            self.cur.execute(query, (email))
            user_id = self.cur.fetchone()
            
            if user_id is not None:
                return user_id['userID']
            else:
                return None  # Return a sentinel value to indicate no user was found
        except pymysql.MySQLError as e:
            print("Error getting user ID:", e)
            return None  # Return a sentinel value to indicate an error

    def get_user_vol(self, user_id):
        # get current vol
        query = "SELECT vol, categories FROM `user` WHERE `userID` = %s"
        self.cur.execute(query, (user_id))
        vol_cat_dict = self.cur.fetchone()

        # kinda wonky, +1 allows for vol field in db to init at 0
        return vol_cat_dict['vol'] + 1
    
    def update_user_vol(self, user_id):
        # get current vol
        query = "SELECT vol FROM `user` WHERE `userID` = %s"
        self.cur.execute(query, (user_id))
        vol_cat_dict = self.cur.fetchone()
        
        # increment vol in db
        query = "UPDATE `user` SET `vol` = %s WHERE `userID` = %s"
        self.cur.execute(query, (vol_cat_dict['vol'] + 1, user_id))


    def add_user(self, email, password, first_name, categories):
        first_name = first_name.capitalize() # ensures record is capitalized
        categories = categories.lower() # categories all need to be lowercase

        # add password encryption
        
        if not self.user_exist(email):
            try:
                query = "INSERT INTO `user` (`email`, `password`, `firstName`, `categories`) VALUES (%s, %s, %s, %s)"
                self.cur.execute(query, (email, password, first_name, categories))
                print(f"User '{first_name}' added successfully")
            except pymysql.MySQLError as e:
                print("Error adding user:", e)
        else:
            print(f"User '{email}' already exists")

    def update_user_settings(self, email, categories):
        if self.user_exist(email):
            categories = categories.lower() # categories all need to be lowercase
            try:
                query = "UPDATE `user` SET `categories` = %s WHERE `email` = %s"
                self.cur.execute(query, (categories, email))
                print(f"User '{email}' settings updated")
            except pymysql.MySQLError as e:
                print("Error updating user settings:", e)
        else:
            print(f"User '{email}' does not exist")

    # don't really need this anymore but it's used in other funcs as a double check
    def user_exist(self, email):
        try:
            query = "SELECT `email` FROM `user` WHERE `email` = %s"
            self.cur.execute(query, (email))
            if self.cur.fetchone():
                print(f"User '{email}' exists")
                return True
            else:
                print(f"User '{email}' does not exist")
                return False
        except pymysql.MySQLError as e:
            print("Error checking user existence:", e)
            return False
        
    def auth_user(self, email, password):

        # encrypt password to check against encrypted password in database

        try:
            query = "SELECT `email`,`password` FROM `user` WHERE `email` = %s AND `password` = %s"
            self.cur.execute(query, (email, password))
            email_password = self.cur.fetchone()
            # print(email_password)
            if email_password['email'] == email and email_password['password'] == password:
                print(f"User '{email}' authenticated")
                return True
            else:
                print(f"User '{email}' not authenticated")
                return False
        except pymysql.MySQLError as e:
            print("Error authenticating user:", e)
            return False
        
    def get_user_categories(self, user_id):
        try:
            query = "SELECT `categories` FROM `user` WHERE `userID` = %s"
            self.cur.execute(query, (user_id))
            user_categories = self.cur.fetchone()
            return user_categories['categories']
        except pymysql.MySQLError as e:
            print("Error getting user categories:", e)
            return False

########################## Category Content Functions ########################

    def table_exists(self, table_name):
        # not modifying table name in case i want to depend on case sensitivity returning false
        try:
            self.cur.execute("SHOW TABLES LIKE %s", (table_name))
            if self.cur.fetchone():
                print(f"Table '{table_name}' exists")
                return True
            else:
                print(f"Table '{table_name}' does not exist")
                return False
        except pymysql.MySQLError as e:
            print(f"Error checking table {table_name} existence:", e)
            return False
        

    def create_category_table(self, category):
        if not self.table_exists(category):
            try:
                # category name needs to be alphanumeric
                if not category.isalnum():
                    print(f"Invalid category name: {category}")
                    return
                
                # had a weird problem can't use %s with table name, so i'm using fstring
                query = f"""CREATE TABLE `{category}` (
                                recordID INT AUTO_INCREMENT PRIMARY KEY,
                                userID INT NOT NULL,
                                last_updated DATE,
                                headline VARCHAR(255),
                                summary TEXT,
                                url VARCHAR(255),
                                FOREIGN KEY (userID) REFERENCES user(userID)
                                )"""
                self.cur.execute(query)  # Notice the change here
                print(f"Table '{category}' created successfully")
            except pymysql.MySQLError as e:
                print(f"Error creating table for category {category}:", e)


    def records_today_exist(self, user_id, category):
        try:
            # table names need to be alphanumeric
            if not category.isalnum():
                print(f"Invalid category name: {category}")
                return False

            today = datetime.now().date()
            query = f"SELECT COUNT(*) as count FROM `{category}` WHERE userID = %s AND last_updated = %s"
            self.cur.execute(query, (user_id, today))
            result = self.cur.fetchone()
            if result['count'] < 3:
                # print(f"Less than 3 records for user '{user_id}' in '{category}' exist today. Can add more.")
                return False
            else:
                print(f"3 or more records for user '{user_id}' in '{category}' already exist today. Cannot add more.")
                return True
        except pymysql.MySQLError as e:
            print("Error checking records:", e)
            return False


    def insert_or_replace_record(self, user_id, category, headline, summary, url):
        try:
            # Ensure category is alphanumeric
            if not category.isalnum():
                print(f"Invalid category name: {category}")
                return

            today = datetime.now().date()
            
            # Delete all records for the user that are from before the current day
            query = f"DELETE FROM `{category}` WHERE userID = %s AND last_updated < %s"
            self.cur.execute(query, (user_id, today))

            # Insert new record
            query = f"""INSERT INTO `{category}` 
                        (userID, last_updated, headline, summary, url) 
                        VALUES (%s, %s, %s, %s, %s)"""
            self.cur.execute(query, (user_id, today, headline, summary, url))
            print(f"Record for user {user_id} in category {category} added")
        except pymysql.MySQLError as e:
            print("Error inserting or replacing records:", e)


# # this got super redundant
#     def update_user_content_categories(self, user_id, content): 
#         for category, records in content.items():
#             # make sure all categories have a table
#             # this is a double check. App.py already does this. Delete if it's making it slow
#             if not self.table_exists(category):
#                 self.create_category_table(category)

#             # add or replace records if old ones exist. If already been done today, don't do anything
#             if not self.records_today_exist(user_id, category):
#                 for record in records:
#                     self.insert_or_replace_record(user_id, category, record['headline'], record['summary'], record['url'])

    def update_category_content(self, user_id, category, content):
        for record in content:
            self.insert_or_replace_record(user_id, category, record['headline'], record['summary'], record['url'])
        return True






########################## Landing Section Content ########################

    def record_exists_today_landing(self, user_id):
        today = datetime.now().date()
        query = "SELECT COUNT(*) as count FROM landing WHERE userID = %s AND last_updated = %s"
        self.cur.execute(query, (user_id, today))
        result = self.cur.fetchone()
        return result['count'] > 0

    def insert_new_record_landing(self, user_id, meme_term, image_blob, headline, summary):
        today = datetime.now().date()
        query = """INSERT INTO landing
                   (userID, memeTerm, image, headline, summary, last_updated) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cur.execute(query, (user_id, meme_term, image_blob, headline, summary, today))

    def update_landing(self, user_id, meme_term, image_blob, headline, summary):
        if self.record_exists_today_landing(user_id):
            print(f"Landing section record for user {user_id} already exists today.")
            return
        else:
            # delete old record
            today = datetime.now().date()
            query = "DELETE FROM landing WHERE userID = %s AND last_updated < %s"
            self.cur.execute(query, (user_id, today))

            self.insert_new_record_landing(user_id, meme_term, image_blob, headline, summary)
            print(f"New landing section record for user {user_id} added.")

########################## Audio Content ########################
    def record_exists_today_audio(self, user_id):
        today = datetime.now().date()
        query = "SELECT COUNT(*) as count FROM audio_data WHERE userID = %s AND DATE(created_at) = %s"
        self.cur.execute(query, (user_id, today))
        result = self.cur.fetchone()
        return result['count'] > 0

    def add_audio_file(self, user_id, mp3_binary, script):
        # delete previous record
        try:
            delete_query = "DELETE FROM audio_data WHERE userID = %s"
            self.cur.execute(delete_query, (user_id,))
            print("Deleted existing audio record for user:", user_id)
        except pymysql.MySQLError as e:
            print("Error deleting existing record(s):", e) 

        # insert new record
        try:
            insert_query = "INSERT INTO audio_data (userID, audioFile, script) VALUES (%s, %s, %s)"
            self.cur.execute(insert_query, (user_id, mp3_binary, script))
            print("Audio file and script saved to database for user:", user_id)
        except pymysql.MySQLError as e:
            print("Error saving audio file and script to database:", e)


    # download the audio and store it locally as an mp3
    def call_audio_file(self, user_id):
        try:
            query = "SELECT audioFile FROM audio_data WHERE userID = %s"
            self.cur.execute(query, (user_id,))
            audio_file = self.cur.fetchone()
            return audio_file['audioFile']  # return the audio data as a BLOB
        except pymysql.MySQLError as e:
            print("Error calling audio file:", e)
            return None

########################## Economic Content ########################
    def update_econ_data(self, user_id, econ_data):
        # serialize all the data
        data_json = json.dumps(econ_data)

        # delete existing record if there is one
        delete_sql = 'DELETE FROM econ_data WHERE userID = %s'
        self.cur.execute(delete_sql, (user_id,))

        # add new econ data
        sql = 'INSERT INTO econ_data (userID, data) VALUES (%s, %s)'
        self.cur.execute(sql, (user_id, data_json))


    def call_econ_data(self, user_id):
        try:
            query = "SELECT data FROM econ_data WHERE userID = %s"
            self.cur.execute(query, (user_id,))
            record = self.cur.fetchone()
            
            # deserialize the data
            econ_data = json.loads(record['data'])

            return econ_data
        
        except pymysql.MySQLError as e:
            print("Error calling econ data:", e)
            return None
        
######################### Get content functions #########################

    def call_all_content(self, user_id):
        # Fetch user details
        self.cur.execute("SELECT userID, firstName, categories FROM user WHERE userID = %s", (user_id,))
        user = self.cur.fetchone()
        if not user:
            return json.dumps({"error": "User not found"})

        # fetch vol counter separately bc func also updates
        vol_counter = self.get_user_vol(user_id)

        # fetch landing details
        self.cur.execute("SELECT memeTerm, image, headline, summary FROM landing WHERE userID = %s", (user_id,))
        landing = self.cur.fetchone()

        # Encode the image blob to base64 if it exists
        image_base64 = ''
        if landing and landing['image']:
            image_base64 = base64.b64encode(landing['image']).decode('utf-8')

        # fetch content from category tables
        categories_content = {}
        categories_list = self.get_user_categories(user_id).split(',')
        for category in categories_list:
            self.cur.execute(f"SELECT headline, summary, url FROM {category} WHERE userID = %s", (user_id,))
            categories_content[category] = self.cur.fetchall()

        # fetch audio file
        self.cur.execute("SELECT audioFile FROM audio_data WHERE userID = %s", (user_id,))
        audio_file = self.cur.fetchone()
        audio_blob = audio_file['audioFile']  # return the audio data as a BLOB
        audio_base64 = base64.b64encode(audio_blob).decode('utf-8') if audio_blob else ''

        # fetch econ data
        stats_data = self.call_econ_data(user_id)  # returns a dict

        # Construct the final result
        result = {
            "userID": user["userID"],
            "firstName": user["firstName"],
            "vol": vol_counter,
            "landing": {
                "memeTerm": landing["memeTerm"] if landing else '',
                "image": image_base64,
                "headline": landing["headline"] if landing else '',
                "summary": landing["summary"] if landing else ''
            },
            "audioFile": audio_base64,
            "statsData": stats_data,
            "categories": categories_content
        }

        return result
    

    # I think I actually need to call category content in app.py
    def call_category_content(self, user_id, category):
        try:
            # Ensure category is alphanumeric
            if not category.isalnum():
                print(f"Invalid category name: {category}")
                return '[]'  # Return an empty JSON array as a string

            today = datetime.now().date()
            # Modify the query to properly format the table name with backticks
            query = f"SELECT headline, summary, url FROM `{category}` WHERE userID = %s"
            self.cur.execute(query, (user_id,))
            category_content = self.cur.fetchall()

            # Print some information for debugging
            # print("Category:", category)
            # print("Category Content:", category_content)

            # Return an empty JSON array as a string if no content found
            if not category_content:
                return '[]'

            return category_content
        except pymysql.MySQLError as e:
            print("Error calling category content:", e)
            return '[]'  # Return an empty JSON array as a string in case of an exception



    def call_landing_content(self, user_id):
        # Fetch content from the specified category table
        self.cur.execute("SELECT memeTerm, image, headline, summary FROM landing WHERE userID = %s", (user_id,))
        landing_content = self.cur.fetchone() 
        # this is just json right? Should I just return that instead of stringifying them jsonifying?

        return json.dumps(landing_content, indent=4)
