from flask import Flask, render_template, request, send_file
from application.facebook import Facebook
from application.twitter import Twitter
from application.threads import Threads
from application.tiktok import Tiktok
from application.instagram import Instagram

app = Flask(__name__)

@app.route('/instagram/downloader/', methods=['POST', 'GET'])
def DownloadFromInstagram():
    if request.method == "POST":
        get_json_data = request.get_json()
        video_stream = Instagram(get_json_data['url'])
        if isinstance(video_stream, tuple):
            message, status = video_stream
            return (message, status)
        return send_file(video_stream, as_attachment=True, download_name='instagram-video.mp4', mimetype='video/mp4')
    else:
        return render_template('unduh.html', platform="instagram", placeholder="Example: https://www.instagram.com/reel/...")

@app.route('/facebook/downloader/', methods=['POST', 'GET'])
def DownloadFromFacebook():
    if request.method == "POST":
        get_json_data = request.get_json()
        video_stream = Facebook(get_json_data['url'])
        if isinstance(video_stream, tuple):
            message, status = video_stream
            return (message, status)
        return send_file(video_stream, as_attachment=True, download_name='facebook-video.mp4', mimetype='video/mp4')
    else:
        return render_template('unduh.html', platform="facebook", placeholder="Example: https://www.facebook.com/share/r/...")

@app.route('/tiktok/downloader/', methods=['POST', 'GET'])
def DownloadFromTiktok():
    if request.method == "POST":
        get_json_data = request.get_json()
        video_stream = Tiktok(get_json_data['url'])
        if isinstance(video_stream, tuple):
            message, status = video_stream
            return (message, status)
        return send_file(video_stream, as_attachment=True, download_name='tiktok-video.mp4', mimetype='video/mp4')
    else:
        return render_template('unduh.html', platform="tiktok", placeholder="Example: https://vm.tiktok.com/...")

@app.route('/threads/downloader/', methods=['POST', 'GET'])
def DownloadFromThreads():
    if request.method == "POST":
        get_json_data = request.get_json()
        video_stream = Threads(get_json_data['url'])
        if isinstance(video_stream, tuple):
            message, status = video_stream
            return (message, status)
        return send_file(video_stream, as_attachment=True, download_name='threads-video.mp4', mimetype='video/mp4')
    else:
        return render_template('unduh.html', platform="threads", placeholder="Example: https://www.threads.net/@.../post/...")

@app.route('/twitter/downloader/', methods=['POST', 'GET'])
def DownloadFromTwitter():
    if request.method == "POST":
        get_json_data = request.get_json()
        video_stream = Twitter(get_json_data['url'])
        if isinstance(video_stream, tuple):
            message, status = video_stream
            return (message, status)
        return send_file(video_stream, as_attachment=True, download_name='twitter-video.mp4', mimetype='video/mp4')
    else:
        return render_template('unduh.html', platform="twitter", placeholder="Example: https://x.com/.../status/...")

@app.route('/terms-of-service/')
def TermsOfService():
    return render_template('terms-of-service.html')

@app.route('/')
def HomePage():
    return render_template('index.html')

@app.route('/privacy-policy/')
def PrivacyPolicy():
    return render_template('privacy-policy.html')

if __name__=='__main__':
    app.run(debug=True)