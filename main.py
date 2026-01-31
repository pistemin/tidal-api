import os
from flask import Flask, request, jsonify
import tidalapi

app = Flask(__name__)

@app.route('/')
def search_tidal():
    query = request.args.get('q')
    print(f"Prijaty dotaz: {query}") # Toto uvidite v Render Logs
    
    if not query:
        return jsonify({"error": "Chybi parametr q"}), 400
    
    try:
        session = tidalapi.Session()
        session.login_guest()
        
        # Vyhledávání
        search_result = session.search(query, models=[tidalapi.media.Track], limit=1)
        
        # Různé verze knihovny vrací výsledky různě, pojistíme to:
        tracks = []
        if isinstance(search_result, dict):
            tracks = search_result.get('tracks', [])
        else:
            tracks = search_result.tracks

        if tracks:
            track = tracks[0]
            track_url = f"https://tidal.com{track.id}"
            print(f"Nalezeno: {track_url}")
            return jsonify({"url": track_url, "id": track.id})
        
        return jsonify({"error": "Skladba nenalezena"}), 404
    except Exception as e:
        print(f"Chyba: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render vyžaduje port z prostředí (environ)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

