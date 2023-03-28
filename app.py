from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

@app.route('/')
def index():
    return render_template('updated_index.html')

@app.route('/generate_lyrics', methods=['POST'])
def generate_lyrics():
    print(openai.api_key)
    prompt = request.form['prompt']
    genre = request.form['genre']
    keyword1 = request.form.get('keyword1', '')
    keyword2 = request.form.get('keyword2', '')
    keyword3 = request.form.get('keyword3', '')
    structure = request.form['structure']

    keywords = ', '.join([k for k in [keyword1, keyword2, keyword3] if k])
    keywords_prompt = f" and include the keywords: {keywords}" if keywords else ""

    if structure == 'full':
        song_structure = "The song should have two verses and three choruses."
    elif structure == 'verse':
        song_structure = "Write a verse for the song."
    elif structure == 'chorus':
        song_structure = "Write a chorus for the song."
    else:  # structure == 'bridge'
        song_structure = "Write a bridge for the song."

    prompt = f"Write a {genre} song with the theme: {prompt}{keywords_prompt}. {song_structure}"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.8,
    )

    lyrics = response.choices[0].text.strip()
    return jsonify({'lyrics': lyrics})

if __name__ == '__main__':
    app.run(debug=True)
