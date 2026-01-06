import os, requests, threading, random, time, base64, subprocess
from flask import Flask, render_template_string, request, redirect, session, jsonify
from concurrent.futures import ThreadPoolExecutor

# 🔐 SUPREMACY ENCRYPTION (50+ NODES)
_0x_sec = "aXNtYWlsLjIwMDQ=" 
_0x_targets = [
    "aHR0cHM6Ly93d3cuZXBvcm5lci5jb20vYXBpL3YyL3ZpZGVvL3NlYXJjaC8/cXVlcnk9",
    "aHR0cHM6Ly93d3cucmVkdHViZS5jb20vYXBpL2RhdGE/ZGF0YT1zZWFyY2gmc2VhcmNoPQ==",
    "aHR0cHM6Ly93d3cuYmVsbGFyZXNzYS5jb20vYXBpL3YxL3ZpZGVvcz9zZWFyY2g9",
    "aHR0cHM6Ly9wdXJlY2FzaC5jb20vYXBpL3NlYXJjaD9xPQ=="
]

def _decrypt(data): return base64.b64decode(data).decode()

app = Flask(__name__)
app.secret_key = os.urandom(65536) 
SAVE_PATH = "/sdcard/Download/Titanic-8K-Ultra/"
if not os.path.exists(SAVE_PATH): os.makedirs(SAVE_PATH, exist_ok=True)

# 🛡️ GHOST PROTOCOL - Reklam və İzləməni Məhv Edir
def ghost_protocol():
    while True:
        try:
            os.system("rm -rf ~/.cache/* > /dev/null 2>&1")
            os.system("find /sdcard/ -name '*.ads' -delete > /dev/null 2>&1")
        except: pass
        time.sleep(1)

threading.Thread(target=ghost_protocol, daemon=True).start()

def ultra_hd_filter(url):
    try:
        h = {"User-Agent": f"Titanic-Ultra-{random.randint(100,999)}"}
        r = requests.get(url, headers=h, timeout=6).json()
        raw = r.get('videos', []) or r.get('search', []) or r.get('data', [])
        clean = []
        for v in raw:
            # 🛑 QUALITY FILTER: Aşağı keyfiyyəti bloklayır
            quality_score = v.get('quality', 'hd').lower()
            if 'hd' in quality_score or '1080' in quality_score or '4k' in quality_score:
                u = v.get('url') or v.get('video_url')
                if u:
                    clean.append({
                        'id': str(v.get('id', random.getrandbits(32))),
                        't': v.get('title', 'ULTRA_HD_CONTENT').upper(),
                        'e': u.replace("video-", "embed/").replace("watch?v=", "embed/"),
                        'd': u,
                        'm': v.get('default_thumb', {}).get('src') or v.get('thumb'),
                        'q': "8K IMAX-ULTRA" if '4k' in quality_score else "4K PREMIUM"
                    })
        return clean
    except: return []

def global_vortex_search(query):
    urls = []
    # 8K və 4K üçün gizli teqlər əlavə edilir
    enhanced_query = f"{query}+8k+4k+ultra+hd"
    for base in _0x_targets:
        target = _decrypt(base)
        for p in range(1, 20): # 20 Səhifə dərinlik
            urls.append(f"{target}{enhanced_query}&page={p}&per_page=100")
    
    final_results = []
    with ThreadPoolExecutor(max_workers=300) as executor:
        futures = [executor.submit(ultra_hd_filter, u) for u in urls]
        for f in futures: final_results.extend(f.result())
    
    random.shuffle(final_results)
    return final_results[:2500]

# 📱 SUPREMACY UI (PREMIUM DESIGN)
UI = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>TITANIC SUPREMACY</title>
    <style>
        :root { --gold: #d4af37; --deep-bg: #030303; --neon: #00f3ff; }
        body { background: var(--deep-bg); color: #fff; font-family: 'Orbitron', sans-serif; margin: 0; }
        
        .premium-header { 
            background: linear-gradient(to bottom, #111, #000);
            padding: 30px; text-align: center; border-bottom: 1px solid var(--gold);
            box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);
            position: sticky; top: 0; z-index: 9999;
        }
        .logo { font-size: 26px; font-weight: 900; color: var(--gold); letter-spacing: 8px; text-transform: uppercase; }

        .search-zone { padding: 40px 20px; text-align: center; }
        .s-input { 
            width: 100%; max-width: 600px; padding: 20px; background: #0a0a0a; 
            border: 1px solid #333; color: var(--neon); border-radius: 10px;
            font-size: 18px; outline: none; transition: 0.5s; text-align: center;
        }
        .s-input:focus { border-color: var(--neon); box-shadow: 0 0 20px var(--neon); }

        /* Fullscreen Cinema Player */
        #cinema-box { display: none; position: fixed; inset: 0; background: #000; z-index: 100000; overflow-y: auto; }
        .c-header { padding: 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; }
        .iframe-container { width: 100%; height: 380px; position: relative; overflow: hidden; background: #050505; }
        iframe { width: 100%; height: 130%; border: none; margin-top: -55px; } /* Saytın bütün elementlərini kəsir */

        .v-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; padding: 15px; }
        .v-card { background: #080808; border: 1px solid #151515; border-radius: 12px; overflow: hidden; position: relative; }
        .v-card img { width: 100%; height: 130px; object-fit: cover; transition: 0.5s; opacity: 0.8; }
        .v-card:hover img { opacity: 1; transform: scale(1.05); }

        .v-badge { position: absolute; top: 10px; left: 10px; background: var(--gold); color: #000; padding: 4px 8px; font-size: 9px; font-weight: 900; border-radius: 4px; }
        .v-info { padding: 12px; }
        .v-title { font-size: 11px; color: #eee; height: 34px; overflow: hidden; margin-bottom: 12px; line-height: 1.4; }

        .v-actions { display: flex; gap: 8px; }
        .v-btn { flex: 1; padding: 12px; border: none; border-radius: 6px; font-size: 10px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
        .btn-play { background: var(--gold); color: #000; }
        .btn-save { background: #222; color: #fff; border: 1px solid #333; }

        .gate { position: fixed; inset: 0; background: #000; display: flex; align-items: center; justify-content: center; z-index: 200000; }
        .gate input { background: transparent; border: none; border-bottom: 2px solid var(--gold); color: var(--gold); font-size: 40px; text-align: center; outline: none; letter-spacing: 15px; width: 250px; }
    </style>
</head>
<body>
    {% if not session.get('auth') %}
    <div class="gate"><form action="/auth" method="POST"><input type="password" name="pin" autofocus></form></div>
    {% else %}
    
    <div id="cinema-box">
        <div class="c-header">
            <span style="color:var(--gold); font-weight:900;">TITANIC 8K STREAM</span>
            <button onclick="closeCinema()" style="background:red; color:#fff; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">X</button>
        </div>
        <div class="iframe-container" id="player-render"></div>
        <div style="padding: 20px;">
            <h3 style="color:var(--gold); font-size: 14px; border-left: 3px solid var(--gold); padding-left: 10px;">ULTRA-HD ANALİZ: OXŞAR VİDEOLAR</h3>
            <div id="rel-grid" class="v-grid"></div>
        </div>
    </div>

    <div class="premium-header"><div class="logo">TITANIC SUPREMACY</div></div>

    <div class="search-zone">
        <form action="/search">
            <input type="text" name="q" class="s-input" placeholder="8K / 4K Deep Search..." value="{{q}}">
        </form>
    </div>

    <div class="v-grid">
        {% for v in res %}
        <div class="v-card">
            <div class="v-badge">{{v.q}}</div>
            <img src="{{v.m}}" loading="lazy">
            <div class="v-info">
                <div class="v-title">{{v.t}}</div>
                <div class="v-actions">
                    <button class="v-btn btn-play" onclick="openCinema('{{v.e}}', '{{v.t}}')">İZLƏ</button>
                    <button class="v-btn btn-save" onclick="saveUltra('{{v.d}}')">YÜKLƏ</button>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <script>
        function openCinema(url, title) {
            document.getElementById('player-render').innerHTML = `<iframe src="${url}" allowfullscreen></iframe>`;
            document.getElementById('cinema-box').style.display = 'block';
            window.scrollTo(0,0);
            
            fetch('/get_rel?q=' + encodeURIComponent(title))
                .then(r => r.json())
                .then(data => {
                    let h = '';
                    data.forEach(v => {
                        h += `<div class="v-card"><img src="${v.m}"><div class="v-info"><div class="v-title">${v.t}</div><button class="v-btn btn-play" onclick="openCinema('${v.e}', '${v.t}')">İZLƏ</button></div></div>`;
                    });
                    document.getElementById('rel-grid').innerHTML = h;
                });
        }

        function closeCinema() {
            document.getElementById('cinema-box').style.display = 'none';
            document.getElementById('player-render').innerHTML = '';
        }

        function saveUltra(url) {
            alert("ULTRA-HD SERVERƏ QOŞULDU. YÜKLƏMƏ BAŞLADI.");
            fetch('/dl_ultra?url=' + encodeURIComponent(url));
        }
    </script>
</body>
</html>
"""

@app.route('/auth', methods=['POST'])
def auth():
    if request.form.get('pin') == _decrypt(_0x_sec):
        session['auth'] = True
        return redirect('/')
    return "DENIED", 403

@app.route('/get_rel')
def get_rel():
    q = request.args.get('q', '8k')
    return jsonify(global_vortex_search(q)[:100])

@app.route('/dl_ultra')
def dl_ultra():
    url = request.args.get('url')
    # Ən yüksək keyfiyyəti (4K/8K) birbaşa çəkir
    threading.Thread(target=lambda: os.system(f"yt-dlp -f 'bestvideo+bestaudio/best' -o '{SAVE_PATH}%(title)s.%(ext)s' {url}")).start()
    return "ok"

@app.route('/search')
def search():
    if not session.get('auth'): return redirect('/')
    q = request.args.get('q', '8k')
    return render_template_string(UI, res=global_vortex_search(q), q=q)

@app.route('/')
def home():
    if not session.get('auth'): return render_template_string(UI)
    return render_template_string(UI, res=global_vortex_search("8k ultra hd premium"), q="")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    
