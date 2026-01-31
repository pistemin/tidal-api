import os
from flask import Flask, request, jsonify
import tidalapi

app = Flask(__name__)

@app.route('/')
def get_track():
    query = request.args.get('q')
    if not query:
        return "Chybí parametr q", 400
    
    try:
        session = tidalapi.Session()
        # Přihlášení jako host (nevyžaduje vaše klíče)
        session.login_guest()
        search_result = session.search(query, models=[tidalapi.media.Track], limit=1)
        
        if search_result['tracks']:
            track = search_result['tracks'][0]
            return jsonify({
                "url": f"https://tidal.com{track.id}",
                "id": track.id
            })
        return "Nenalezeno", 404
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
