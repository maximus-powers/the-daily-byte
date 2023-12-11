# Backend Architecture

## SQL Database Tables:
- **user**: userID(int, pk, auto), firstName(varchar), email(varchar), password(varchar), categories(varchar), vol(int)
- **landing**: landingID(int, pk, auto), userID(int, fk), memeTerm(varchar), image(longblob), headline(text), summary(text), last_updated(date)
- **audio_data**: id(int, pk, auto), userID(int, fk), audioFile(longblob), script(text), created_at(timestamp, sql generated)
- **econ_data**: userID(int, fk), data(text)
- **category tables**: recordID(int, pk, auto), userID(int, fk), last_updated(date), headline(varchar), summary(text), url(varchar)
- *categories: business, entertainment, general, health, science, sports, technology*


## Flask Server
### app.py
- **refresh_content()**:
    - Scheduler refreshes the database's content once per day at 4am (-04:00 UTC)
    - Refresh Categories:
        - Call news api for each of the categories from user table (newsapi.org)
            - Has a check to make sure it hasn't run already today
            - Has a check to make sure there's a table for this category, if not it creates one
        - Write new headlines and summaries for each story, until it has 3 news stories
            - Skip a news story if source url is broken, paywall, or llm couldn't summarize
        - Update each category table with new content

    - Refresh Landing Content:
        - Has a check to make sure it hasn't run already today
        - Call all categories' content from db
        - Generate new landing content from all categories' content
            - Find the top story
            - Generate headline and subheading
                - Has a check to make sure both are successful
            - Generate an image (Dalle-3)
        - Update landing table with new content
        - Update vol counter
    - Refresh Audio:
        - Has a check to make sure it hasn't run already today
        - Call all categories' content from db
        - Generate a script from all content
        - Send script to Google Text-To-Speech api
        - Update audioFile in db
    - Refresh Economic Data:
        - Call economic data api (alphavantage.co)
        - Update econ_data table


- **/get_content Endpoint**
    - tdb-api.maximus-powers.com is live, has this endpoint
    - Calls all content from the db
    - JSON Response:
        db_content = {
            userID: int,
            firstName:  str,
            vol: int,
            landing: {
                memeTerm: str, 
                image: base64 str, 
                headline: str, 
                summary: str
                },
            audioFile: base64 str,
            statsData: {
                markets: {}, 
                economy: {}
                }, 
            categories: {
                category: [{
                    headline: str, 
                    summary: str, 
                    url: str
                    }, ...], 
                ...}
        }
    
### ENV Variables
- **OPENAI_API_KEY**: [API Portal](https://platform.openai.com/api-keys)
- **NEWS_API_KEY**: [API Portal](https://newsapi.org/register)
- **GOOGLE_APPLICATION_CREDENTIALS**: [google.cloud](https://console.cloud.google.com/)
- **ALPHAV_API_KEY**: [Alpha Vantage API](https://www.alphavantage.co/)
- **RAPIDAPI_KEY**: [RapidAPI](https://fear-and-greed-index.p.rapidapi.com/)
- **db_host**: SQL server IP address
- **db_user**: username
- **db_passwd**: password
- **db_name**: database name


### Python Class Objects
- **NewsObject**:
    - *Uses [News API](https://newsapi.org)*
    - __init__():
        - set API key from env, set /top-headlines endpoint url
    - call_news(category)
        - string --> [{'headline': headline, 'url': url}, ...]
        - Currently set to call 20 stories from the category passed in, has to be one of newsapi.org's categories
            - Has a check that skips stories from youtube, google, or homepages of news sites
            - Skip stories more than 36 hours old

- **LLMObject**:
    - *Uses [LangChain](https://js.langchain.com/docs/get_started) chat templates and structured outputs*
    - *Should've just used OpenAI's library. LangChain isn't that good*
    - *Uses [OpenAI API](https://platform.openai.com/api-keys)*
    - __init__(): 
        - sets API key from env
        - currently set to gpt-3.5-turbo. 'gpt-4' works better but more expensive
    - rank_dictionary(headlines_urls)
        - {headlines: urls} --> [{headline: str, url: str, importance: int}, ...]
    - rewrite_headline(headline)
        - old headline str --> new headline str (slightly punny)
    - summarize_article(article_url, num_of_chars)
        - loads article from URL
            - Returns false if invalid, paywall, or llm can't summarize
            - Has a check to make sure context is under 3000 tokens, truncates
        - Summarizes the article in the given number of characters, returns str
    - generate_script(content)
        - Takes any content and writes a 500 word script for a podcast
            - Focuses on the three most important stories
        - Returns str
    - generate_image_prompt(headline, subheading)
        - Writes a dall-e-3 safe prompt for the given headline and subheading, returns str
    - gen_safer_image_prompt(old_img_prompt)
        - Modifies an image prompt to tone it down

- **ImageObject**:
    - *Uses OpenAI API, set to dalle-3*
    - __init__()
        - Set the OpenAI client, import API key from env
    - generate_image(prompt)
        - turns prompt into an image at a temp url
        - string --> image_url
    - download_image_as_blog(image_url)
        - string --> binary blob

- **TTSObject**:
    - *Uses [google.cloud](https://console.cloud.google.com/) texttospeech package*
    - Google credentials set in .env
    - __init__()
        - setup text-to-speech client
    - script_to_audio(script)
        - Voice model settings
        - returns {'audio': blob, 'script': str}

- **EconObject**
    - *Uses [Alpha Vantage API](https://www.alphavantage.co/) for market data*
    - *Uses [RapidAPI](https://fear-and-greed-index.p.rapidapi.com/) for fear and greed index*
    - __init__()
        - Set api key from env, and today's date
    - get_econ_data()
        - returns {
            'markets':{
                'fear_greed':fear_greed_data, 
                'sp500':sp500_data, 
                'itb':housing_data, 
                'eth':eth_data
                }, 
            'economy':{
                'gdp':gdp_data, 
                'cpi':cpi_data, 
                'fed':fed_data, 
                'unemployment':unemp_data, 
                'oil':crude_oil_data
                }
            }
    - get_cpi_data(num_months)
        - defaults to 6
        - returns a list of dicts [{'date': '2023-10-01', 'value': '307.671'}, ...]
    - get_fed_data(num_months)
        - defaults to 6
    - get_stock_data(symbol, num_days)
        - num_days defaults to 10 (2 weeks, 24/5)
    - get_crypto_data(symbol, num_days)
        - num_days defaults to 14 (2 weeks 24/7)
    - get_unemployment_data(num_months)
        - defaults to 12
    - get_oil_data(num_months)
        - defaults to 6
    - get_fear_greed()
        - get api key from env

- **LandingObject**:
    - __init__()
        - imports a bunch of the other objects
    - gen_landing_content(user_id)
        - Relies on database being up to date, must come after db refresh in refresh_content()
        - Call user categories from database
        - Call content from each category's table
            - Ranks them all
        - Write headline and subheading for top record
            - If summarization doesn't work, it tries again with the next record
            - Remove periods if there are any
        - Generate image
            - Generate prompt, try it, if it doesn't work make it safer and try again (up to 3 times)
            - Download image blob
        - returns {
            'headline': top_headline,
            'summary': summary_sentence,
            'url': top_url,
            'alt_text': 'not working rn',
            'image_blob': image_blob
        }

- **DBObject**:
    - *These are all the functions used for interacting with the sql database*
    - __init__
    - setup(): Establishes connection
    - close(): Closes connection

    - User Methods
        - get_user_id(email)
        - get_user_vol(user_id)
        - update_user_vol(user_id)
        - add_user(email, password, first_name, categories): no encryption, user auth not implemented anymore
        - update_user_settings(email, categories)
        - user_exist(email)
        - auth_user(email, password)
        - get_user_categories(user_id)
    
    - Category Content Methods
        - table_exists(table_name)
        - create_category_table(category)
        - records_today_exist(user_id, category)
        - insert_or_replace_record(user_id, category, headline, summary, url)
        - update_category_content(user_id, category, content)

    - Landing Section Methods
        - record_exists_today_landing(user_id)
        - insert_new_record_landing(user_id, meme_term, image_blob, headline, summary)
        - update_landing(user_id, meme_term, image_blob, headline, summary)

    - Audio Content Methods
        - record_exists_today_audio(user_id)
        - add_audio_file(user_id, mp3_binary, script)
        - call_audio_file(user_id)

    - Economic Content Methods
        - update_econ_data(user_id, econ_data)
        - call_econ_data(user_id)

    - Get Content Methods
        - call_all_content(user_id)
            - returns {
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
        - call_category_content(user_id, category)
        - call_landing_content(user_id)






