from flask import Flask, request, send_file, Response, render_template
from pytube import YouTube
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    resolution = request.form['resolution']

    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_by_resolution(resolution)
        
        if not video_stream:
            return "Video not available in the selected resolution."
        
        video_bytes = io.BytesIO()
        video_stream.stream_to_buffer(video_bytes)
        video_bytes.seek(0)

        response = Response(video_bytes, content_type="video/mp4")
        response.headers["Content-Disposition"] = f"attachment; filename={yt.title}.mp4"

        return response
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
