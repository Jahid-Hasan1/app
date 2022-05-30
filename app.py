from flask import Flask, render_template, request
import urllib.parse
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=="POST":
        outls = []
        outpt = []
        link = request.form.get("inputurl")
        # print(link)
        #function for getting video id from url given by user
        def get_yt_video_id(url):        
            if url.startswith(('youtu', 'www')):
                url = 'http://' + url

            query = urlparse(url)

            if 'youtube' in query.hostname:
                if query.path == '/watch':
                    return parse_qs(query.query)['v'][0]
                elif query.path.startswith(('/embed/', '/v/')):
                    return query.path.split('/')[2]
            elif 'youtu.be' in query.hostname:
                return query.path[1:]
            else:
                raise ValueError
        #function for transcrpition
        vid_id = get_yt_video_id(link)

        try:
            tx = YouTubeTranscriptApi.get_transcript(vid_id, languages=['en'])
            for i in tx:
                outtxt = (i['text'])
                outls.append(outtxt)
                #print (outls)
            for x in outls:
                outpt.append(x.replace("\n", " "))
                final_transcript=' '.join(outpt)
                
        except:
            final_transcript = "Subtitles are disabled for this video"
            # print (final_transcript)
        return render_template('index.html', transcript=final_transcript)
    return render_template('index.html')

    
if __name__ == '__main__':
    app.secret_key = 'secret'
    app.run(debug=True)