import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pytube import YouTube

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key.

# Define the path for saving downloaded videos
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")

# Ensure the downloads folder exists
if not os.path.exists(DOWNLOADS_FOLDER):
    os.makedirs(DOWNLOADS_FOLDER)

# Define available resolution options
RESOLUTION_OPTIONS = [
    ('2160p', '2160p'),
    ('1440p', '1440p'),
    ('1080p', '1080p'),
    ('720p', '720p'),
    ('480p', '480p'),
    ('360p', '360p'),
]

@app.route('/')
def index():
    return render_template('index.html', resolution_options=RESOLUTION_OPTIONS)

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        url = request.form['url']
        resolution = request.form['resolution']

        try:
            yt = YouTube(url)
            stream = None
            
            if resolution == '2160p':
                stream = yt.streams.filter(res="2160p").first()
            elif resolution == '1440p':
                stream = yt.streams.filter(res="1440p").first()
            elif resolution == '1080p':
                stream = yt.streams.filter(res="1080p").first()
            elif resolution == '720p':
                stream = yt.streams.filter(res="720p").first()
            elif resolution == '480p':
                stream = yt.streams.filter(res="480p").first()
            elif resolution == '360p':
                stream = yt.streams.filter(res="360p").first()
            
            if stream:
                stream.download(output_path=DOWNLOADS_FOLDER)
                flash(f"Video '{yt.title}' downloaded successfully to Downloads folder in {resolution} resolution.", 'success')
            else:
                flash(f"No video stream available in {resolution} resolution.", 'error')
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')