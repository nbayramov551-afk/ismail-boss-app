from flask import Flask, render_template_string, request, jsonify, send_from_directory
import yt_dlp, os, threading, uuid, socket, requests, qrcode, datetime
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "ares_v600_ultimate_2026"

# --- STRUKTUR ---
BASE = os.path.expanduser('~/.ares_v600')
PATHS = {
    "vault": os.path.join(BASE, 'vault'),
    "qr": os.path.join(BASE, 'qr'),
    "docs": os.path.join(BASE, 'docs')
}
for p in PATHS.values(): os.makedirs(p, exist_ok=True)

# --- GLOBAL STATUS ---
DL_DATA = {"p": "0%", "s": "0 KB/s", "status": "Hazır", "title": ""}

# --- TUNNEL ---
print("\n" + "⚔️ " * 15)
TUNNEL_URL = input("🔗 SSH Link (Boşdursa Enter): ").strip()
MY_IP = TUNNEL_URL if TUNNEL_URL else f"http://{socket.gethostbyname(socket.gethostname())}:5000"
print(f"📡 ARES SUPREME AKTİVDİR: {MY_IP}")
print("⚔️ " * 15 + "\n")

# --- BACKEND API ---
@app.route('/api/rates')
def get_rates():
    try:
        # Bütün dünya valyutaları üçün genişləndirilmiş siyahı
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=2)
        data = r.json()
        data['date_now'] = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M:%S")
        return jsonify(data)
    except: 
        return jsonify({"rates": {"AZN": 1.70, "RUB": 95.5, "TRY": 35.8, "USD": 1.0, "EUR": 0.92, "GBP": 0.79}, "date_now": "OFFLINE"})

@app.route('/api/dl')
def dl():
    u = request.args.get('u')
    mode = request.args.get('m')
    qual = request.args.get('q', 'best')
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace(' ', '')
            s = d.get('_speed_str', '0 KB/s')
            DL_DATA.update({"p": p, "s": s, "status": "Yüklənir...", "title": d.get('filename', 'Fayl').split('/')[-1]})
        elif d['status'] == 'finished':
            DL_DATA.update({"p": "100%", "status": "Tamamlandı!"})

    def run_dl():
        opts = {
            'outtmpl': f"{PATHS['vault']}/%(title)s.%(ext)s",
            'progress_hooks': [progress_hook],
            'quiet': True
        }
        if mode == 'mp3':
            opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]})
        else:
            opts.update({'format': f'bestvideo[height<={qual}]+bestaudio/best/best' if qual != 'best' else 'best'})
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([u])
        except: DL_DATA.update({"status": "Xəta!"})

    threading.Thread(target=run_dl).start()
    return jsonify({"ok": True})

@app.route('/api/qr', methods=['POST'])
def qr_gen():
    m = request.form.get('m')
    qr_fn = f"qr_{uuid.uuid4().hex}.png"
    if m == 'txt':
        d = request.form.get('d')
    else:
        f = request.files['f']
        f_fn = f"img_{uuid.uuid4().hex}.png"
        f.save(os.path.join(PATHS['qr'], f_fn))
        d = f"{MY_IP}/f/qr/{f_fn}"
    
    img = qrcode.make(d)
    img.save(os.path.join(PATHS['qr'], qr_fn))
    return jsonify({"f": qr_fn})

@app.route('/api/cv', methods=['POST'])
def mk_cv():
    d = request.json
    fn = f"cv_{uuid.uuid4().hex}.pdf"
    pdf = FPDF()
    pdf.add_page()
    # Dizayn
    pdf.set_fill_color(0, 40, 40)
    pdf.rect(0, 0, 210, 50, 'F')
    pdf.set_text_color(0, 255, 204)
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 25, d.get('ad', 'PROFESSIONAL CV').upper(), 0, 1, 'C')
    pdf.ln(15)
    
    pdf.set_text_color(0, 0, 0)
    sections = [
        ("EMAIL", d.get('mail')), ("TEL", d.get('tel')), 
        ("UNVAN", d.get('unv')), ("TEHSIL", d.get('teh')), 
        ("TECRUBE", d.get('tec')), ("BACARIQLAR", d.get('bac'))
    ]
    for label, val in sections:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 10, f"{label}:")
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, str(val))
        pdf.ln(2)

    # Möhür
    pdf.ln(10)
    pdf.set_draw_color(150, 0, 0)
    pdf.set_text_color(150, 0, 0)
    pdf.ellipse(150, 240, 40, 40, 'D')
    pdf.set_font("Arial", 'B', 8)
    pdf.text(155, 260, "ARES SUPREME")
    pdf.text(158, 265, "OFFICIAL SEAL")
    
    pdf.output(os.path.join(PATHS['docs'], fn))
    return jsonify({"f": fn})

@app.route('/api/st')
def st(): return jsonify(DL_DATA)

@app.route('/api/ls')
def ls(): 
    return jsonify({
        "vault": os.listdir(PATHS['vault']), 
        "docs": os.listdir(PATHS['docs']), 
        "qr": os.listdir(PATHS['qr'])
    })

@app.route('/api/delete', methods=['POST'])
def del_file():
    d = request.json
    try:
        os.remove(os.path.join(PATHS[d['folder']], d['fn']))
        return jsonify({"ok": True})
    except: return jsonify({"ok": False})

@app.route('/f/<dir>/<n>')
def serve(dir, n): return send_from_directory(PATHS[dir], n)

@app.route('/')
def index(): return render_template_string(UI_DATA, clr="#00ffcc")

# --- UI DATA ---
UI_DATA = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>ARES SUPREME</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        :root { --neon: {{clr}}; --bg: #000; }
        body { background: var(--bg); color: var(--neon); font-family: 'JetBrains Mono', monospace; margin: 0; overflow: hidden; }
        .container { padding: 15px; height: 100vh; overflow-y: auto; padding-bottom: 100px; box-sizing: border-box; }
        .card { background:rgba(10,10,10,0.9); border:1px solid #222; padding:20px; border-radius:20px; margin-bottom:15px; border-top:3px solid var(--neon); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        input, select, button, textarea { width:100%; padding:14px; margin:6px 0; border-radius:12px; border:1px solid #333; background:#050505; color:var(--neon); font-weight:bold; outline:none; }
        button { background:var(--neon); color:#000; border:none; cursor:pointer; text-transform: uppercase; }
        .nav { position: fixed; bottom:0; width:100%; background:rgba(0,0,0,0.95); display:flex; justify-content:space-around; padding:15px 0; border-top:1px solid #222; backdrop-filter: blur(10px); }
        .nav i { font-size: 24px; color: #444; transition: 0.3s; }
        .nav i.active { color: var(--neon); transform: translateY(-5px); text-shadow: 0 0 15px var(--neon); }
        .panel { display: none; animation: fadeIn 0.4s; } .panel.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .progress-box { background: #111; border-radius: 10px; height: 25px; margin-top: 10px; overflow: hidden; position: relative; border: 1px solid #333; }
        .progress-bar { background: var(--neon); height: 100%; width: 0%; transition: 0.3s; box-shadow: 0 0 15px var(--neon); }
        #war-zone { position: fixed; top:0; left:0; width:100%; height:100%; background:#000; z-index:9999; display:none; flex-direction:column; align-items:center; justify-content:center; }
        .scanner { width: 80%; height: 2px; background: var(--neon); animation: scan 2s infinite; }
        @keyframes scan { 0% { transform: translateY(-100px); } 100% { transform: translateY(100px); } }
    </style>
</head>
<body>
    <div id="war-zone"><div class="scanner"></div><h2 style="margin-top:20px;">PURGE ACTIVE...</h2><div id="p-status">CLEANING...</div></div>

    <div class="container">
        <div id="p-1" class="panel active">
            <div class="card">
                <div id="live-date" style="text-align:center; font-size:10px; margin-bottom:10px;"></div>
                <div id="flags-grid" style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:15px;"></div>
                <input type="number" id="amt" placeholder="Məbləğ...">
                <div style="display:flex; gap:10px;">
                    <select id="from_c"></select>
                    <select id="to_c"></select>
                </div>
                <button onclick="convert()">ÇEVİR</button>
                <h1 id="res-val" style="text-align:center;">0.00</h1>
            </div>
        </div>

        <div id="p-2" class="panel">
            <div class="card">
                <h3><i class="fa fa-bolt"></i> OMEGA DL V3</h3>
                <input id="u" placeholder="YouTube/İnstagram Link...">
                <select id="m_mode"><option value="video">VİDEO (MP4)</option><option value="mp3">MAHNI (MP3)</option></select>
                <select id="v_qual"><option value="best">MAX</option><option value="1080">1080p</option><option value="720">720p</option><option value="480">480p</option></select>
                <button onclick="startDL()">SİSTEMƏ YÜKLƏ</button>
                <div id="dl-area" style="display:none; margin-top:15px;">
                    <div id="dl-title" style="font-size:10px;"></div>
                    <div class="progress-box"><div class="progress-bar" id="p-bar"></div></div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-top:5px;">
                        <span id="dl-status"></span><span id="dl-speed"></span>
                    </div>
                </div>
            </div>
        </div>

        <div id="p-3" class="panel">
            <div class="card">
                <h3><i class="fa fa-id-card"></i> PRO CV BUILDER</h3>
                <input id="cv_ad" placeholder="Ad Soyad">
                <input id="cv_mail" placeholder="Email">
                <input id="cv_tel" placeholder="Telefon">
                <input id="cv_unv" placeholder="Ünvan">
                <textarea id="cv_teh" placeholder="Təhsil..."></textarea>
                <textarea id="cv_tec" placeholder="Təcrübə..."></textarea>
                <textarea id="cv_bac" placeholder="Bacarıqlar..."></textarea>
                <button onclick="mkCV()">CV PDF YARAT</button>
                <hr style="border:0; border-top:1px solid #222; margin:15px 0;">
                <input type="file" id="qf">
                <button onclick="mkQR('img')">ŞƏKİLDƏN QR</button>
                <div id="gen-res" style="text-align:center; margin-top:10px;"></div>
            </div>
        </div>

        <div id="p-5" class="panel">
            <div id="vault-list"></div>
            <button onclick="startWar()" style="background:red; color:white; margin-top:20px;">SİSTEMİ TƏMİZLƏ (PURGE)</button>
        </div>
    </div>

    <div class="nav">
        <i class="fa fa-coins active" onclick="tab('p-1', this)"></i>
        <i class="fa fa-download" onclick="tab('p-2', this)"></i>
        <i class="fa fa-id-card" onclick="tab('p-3', this)"></i>
        <i class="fa fa-folder-open" onclick="tab('p-5', this)"></i>
    </div>

    <script>
        let rates = {};
        const flags = {"USD":"🇺🇸","AZN":"🇦🇿","RUB":"🇷🇺","TRY":"🇹🇷","EUR":"🇪🇺","GBP":"🇬🇧"};

        async function loadRates(){
            const r = await (await fetch('/api/rates')).json();
            rates = r.rates;
            document.getElementById('live-date').innerText = r.date_now;
            let opt = Object.keys(rates).map(c=>`<option value="${c}">${c} ${flags[c]||''}</option>`).join('');
            document.getElementById('from_c').innerHTML = opt;
            document.getElementById('to_c').innerHTML = opt;
            document.getElementById('from_c').value = "AZN";
            document.getElementById('to_c').value = "USD";
            document.getElementById('flags-grid').innerHTML = Object.keys(flags).map(c=>`
                <div style="background:#111; padding:10px; border-radius:10px; text-align:center; font-size:12px;">
                    ${flags[c]} ${c}: <b>${rates[c].toFixed(2)}</b>
                </div>
            `).join('');
        }

        function convert(){
            let a = document.getElementById('amt').value;
            let f = document.getElementById('from_c').value;
            let t = document.getElementById('to_c').value;
            let res = (a / rates[f]) * rates[t];
            document.getElementById('res-val').innerText = res.toFixed(2) + " " + t;
        }

        async function startDL(){
            let u = document.getElementById('u').value;
            if(!u) return;
            document.getElementById('dl-area').style.display='block';
            fetch(`/api/dl?u=${encodeURIComponent(u)}&m=${document.getElementById('m_mode').value}&q=${document.getElementById('v_qual').value}`);
            let itv = setInterval(async () => {
                let r = await (await fetch('/api/st')).json();
                document.getElementById('p-bar').style.width = r.p;
                document.getElementById('dl-status').innerText = r.status + " " + r.p;
                document.getElementById('dl-speed').innerText = r.s;
                document.getElementById('dl-title').innerText = r.title;
                if(r.p == "100%") clearInterval(itv);
            }, 1000);
        }

        async function mkCV(){
            let d = { 
                ad: document.getElementById('cv_ad').value, mail: document.getElementById('cv_mail').value,
                tel: document.getElementById('cv_tel').value, unv: document.getElementById('cv_unv').value,
                teh: document.getElementById('cv_teh').value, tec: document.getElementById('cv_tec').value,
                bac: document.getElementById('cv_bac').value 
            };
            let r = await (await fetch('/api/cv', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(d)})).json();
            document.getElementById('gen-res').innerHTML = `<a href="/f/docs/${r.f}" download style="color:white">📄 CV YÜKLƏ</a>`;
        }

        async function mkQR(m){
            let fd = new FormData(); fd.append('m', m);
            fd.append('f', document.getElementById('qf').files[0]);
            let r = await (await fetch('/api/qr', {method:'POST', body:fd})).json();
            document.getElementById('gen-res').innerHTML = `<img src="/f/qr/${r.f}" style="width:150px; border:5px solid white; border-radius:10px;">`;
        }

        async function loadVault(){
            let r = await (await fetch('/api/ls')).json();
            let h = r.vault.map(f => `
                <div class="card">
                    <b>${f}</b><br>
                    ${f.endsWith('.mp3') ? `<audio src="/f/vault/${f}" controls style="width:100%"></audio>` : `<video src="/f/vault/${f}" controls style="width:100%"></video>`}
                    <button onclick="delFile('${f}','vault')" style="background:red; margin-top:10px;">SİL</button>
                </div>
            `).join('') + r.docs.map(f => `<div class="card">📄 ${f} <button onclick="delFile('${f}','docs')" style="background:red; float:right;">SİL</button></div>`).join('');
            document.getElementById('vault-list').innerHTML = h || "<center>ANBAR BOŞDUR</center>";
        }

        async function delFile(fn, folder){
            if(confirm("SİLİNSİN?")){
                await fetch('/api/delete', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({fn, folder})});
                loadVault();
            }
        }

        function startWar(){
            let w = document.getElementById('war-zone'); w.style.display='flex';
            let s = ["DECRYPTING...","PURGING CACHE...","REMOVING TRACES...","DONE!"];
            let i = 0;
            let itv = setInterval(()=>{
                document.getElementById('p-status').innerText = s[i]; i++;
                if(i==s.length){ clearInterval(itv); setTimeout(()=>w.style.display='none',1000); }
            }, 800);
        }

        function tab(id, el){
            document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
            document.querySelectorAll('.nav i').forEach(i=>i.classList.remove('active'));
            document.getElementById(id).classList.add('active'); el.classList.add('active');
            if(id=='p-5') loadVault();
        }
        window.onload = loadRates;
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
    
