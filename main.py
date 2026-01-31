import os
from flask import Flask, request, jsonify
import tidalapi

app = Flask(__name__)

@app.get('/')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Chybi parametr q"}), 400
    
    try:
        session = tidalapi.Session()
        # Guest login funguje pro vyhledávání ID nejstabilněji
        session.login_guest()
        
        search_result = session.search(query, models=[tidalapi.media.Track], limit=1)
        
        # Knihovna vrací výsledky buď jako objekt nebo jako slovník
        tracks = getattr(search_result, 'tracks', [])
        if not tracks and isinstance(search_result, dict):
            tracks = search_result.get('tracks', [])

        if tracks:
            track = tracks[0]
            # Vracíme přímou URL, kterou Google Apps Script uloží do buňky
            return jsonify({
                "url": f"https://tidal.com{track.id}",
                "id": track.id
            })
        
        return jsonify({"error": "Nenalezeno"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

