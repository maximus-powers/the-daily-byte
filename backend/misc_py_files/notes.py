


####### Image Processes ########
@app.route('/find_gif_for_headline')
def find_gif_for_headline():
    # pass a headline into GPT for a funny reaction suggestion
    # search GIFFY for a gif using the suggestion
    return 'Hello, World!'


####### Audio Processes ########
@app.route('/generate_script')
def generate_script():
    # pass all headlines and descriptions into gpt
    # send it to gpt to make a script under 500 words
    return 'Hello, World!'

@app.route('/generate_audio')
def generate_audio():
    # call a text to speech api on script
    return 'Hello, World!'
