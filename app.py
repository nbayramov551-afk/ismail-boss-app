import http.server, socketserver, urllib.parse, base64

PORT = 55937
B_KEY = "BOSS_ISMAIL_V260_IMMORTAL"

def b_crypt(d, k): 
    return "".join([chr(ord(c) ^ ord(k[i % len(k)])) for i, c in enumerate(d)])

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>İsmail Boss Immortal</title>
    <script src="https://cdn.jsdelivr.net/npm/peerjs@1.4.7/dist/peerjs.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --main: #00f2fe; --neon: #4facfe; --bg: #010409; --card: rgba(22, 27, 34, 0.8); }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, sans-serif; }
        body { background: var(--bg); color: #c9d1d9; height: 100dvh; display: flex; flex-direction: column; overflow: hidden; }
        
        .header { background: #161b22; padding: 15px; border-bottom: 2px solid var(--main); box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3); z-index: 100; }
        .boss-row { display: flex; align-items: center; justify-content: space-between; }
        
        #call-ui { position: fixed; inset: 0; background: #000; z-index: 9999; display: none; flex-direction: column; }
        video { width: 100%; height: 50%; object-fit: cover; background: #000; }
        .v-actions { position: absolute; bottom: 30px; width: 100%; display: flex; justify-content: center; }

        .chat { flex: 1; padding: 20px; overflow-y: auto; background-image: radial-gradient(#1f2937 0.5px, transparent 0.5px); background-size: 20px 20px; display: flex; flex-direction: column; gap: 15px; }
        
        .boss-badge { align-self: center; background: var(--card); border: 1px solid var(--main); padding: 15px; border-radius: 12px; text-align: center; width: 85%; backdrop-filter: blur(5px); box-shadow: 0 0 20px rgba(0, 242, 254, 0.1); }
        .boss-badge b { color: var(--main); font-size: 15px; text-transform: uppercase; letter-spacing: 2px; }

        .msg { max-width: 80%; padding: 12px; border-radius: 15px; font-size: 16px; position: relative; word-wrap: break-word; }
        .sent { align-self: flex-end; background: linear-gradient(135deg, #00f2fe, #4facfe); color: #000; font-weight: 500; }
        .received { align-self: flex-start; background: #30363d; border: 1px solid #484f58; }

        .audio-wrap { display: flex; align-items: center; gap: 10px; padding: 5px; }
        audio { height: 35px; width: 150px; }

        .footer { padding: 12px; background: #161b22; display: flex; align-items: center; gap: 10px; border-top: 1px solid #30363d; }
        .in-bar { flex: 1; background: #0d1117; border-radius: 25px; padding: 0 15px; height: 48px; display: flex; align-items: center; border: 1px solid #30363d; }
        input { background: none; border: none; color: white; flex: 1; outline: none; font-size: 16px; }
        .btn-main { width: 48px; height: 48px; border-radius: 50%; border: none; background: var(--main); color: #000; font-size: 20px; cursor: pointer; box-shadow: 0 0 10px var(--main); }
    </style>
</head>
<body>

<div id="call-ui">
    <video id="remV" autoplay playsinline></video>
    <video id="locV" autoplay muted playsinline style="height:30%; border-top:2px solid var(--main);"></video>
    <div class="v-actions">
        <button onclick="location.reload()" style="background:#ff3e3e; width:65px; height:65px; border-radius:50%; border:none; color:white; font-size:25px;"><i class="fas fa-phone-slash"></i></button>
    </div>
</div>

<div class="header">
    <div class="boss-row">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:42px; height:42px; background:var(--main); border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#000;">IB</div>
            <div><b style="font-size:17px; color:var(--main);">İsmail Boss</b><br><small id="st" style="color:#8b949e;">BAĞLANIR...</small></div>
        </div>
        <div style="display:flex; gap:22px; color:var(--main); font-size:22px;">
            <i class="fas fa-video" onclick="callBoss()"></i>
            <i class="fas fa-camera" onclick="document.getElementById('f').click()"></i>
        </div>
    </div>
</div>

<div class="chat" id="chat">
    <div class="boss-badge">
        <b>🔱 Immortal Sovereign 🔱</b><br>
        <small style="opacity:0.8; font-size:11px;">İnternet kəsilsə belə sistem avtomatik bərpa olunur.</small>
    </div>
</div>

<div class="footer">
    <div class="in-bar"><input type="text" id="mIn" placeholder="Mesaj yaz..." autocomplete="off"></div>
    <button class="btn-main" id="mBtn" onmousedown="sR()" onmouseup="eR()" ontouchstart="sR()" ontouchend="eR()">
        <i class="fas fa-microphone" id="mIcon"></i>
    </button>
</div>

<audio id="dial" src="https://www.soundjay.com/phone/phone-calling-1.mp3" loop></audio>
<audio id="ring" src="https://assets.mixkit.co/active_storage/sfx/1359/1359-preview.mp3" loop></audio>
<input type="file" id="f" hidden onchange="up(this)">

<script>
    const KEY = "BOSS_ISMAIL_V260_IMMORTAL";
    const cr = (s, k) => s.split('').map((c, i) => String.fromCharCode(c.charCodeAt(0) ^ k.charCodeAt(i % k.length))).join('');
    const isG = new URLSearchParams(window.location.search).has('join');
    
    let peer, conn, mediaRec, chunks = [];

    function initPeer() {
        peer = new Peer(isG ? 'guest_immortal' : 'boss_immortal', {
            config: {'iceServers': [{ 'urls': 'stun:stun.l.google.com:19302' }]}
        });

        peer.on('open', (id) => { 
            if(isG) { connectToBoss(); }
        });

        peer.on('connection', c => { conn = c; handle(conn); });
        
        peer.on('call', async call => {
            document.getElementById('ring').play().catch(()=>{});
            if(confirm("🔱 İSMAİL BOSS ZƏNG EDİR. QƏBUL EDİLSİN?")) {
                document.getElementById('ring').pause();
                const s = await navigator.mediaDevices.getUserMedia({video:true, audio:true});
                document.getElementById('call-ui').style.display='flex';
                document.getElementById('locV').srcObject = s;
                call.answer(s);
                call.on('stream', rs => document.getElementById('remV').srcObject = rs);
            } else { document.getElementById('ring').pause(); }
        });

        peer.on('disconnected', () => { peer.reconnect(); });
    }

    function connectToBoss() {
        conn = peer.connect('boss_immortal', {reliable: true});
        handle(conn);
    }

    function handle(c) {
        c.on('open', () => { 
            document.getElementById('st').innerText = 'ONLAYN'; 
            document.getElementById('st').style.color = '#39d353'; 
        });
        c.on('close', () => { 
            document.getElementById('st').innerText = 'BƏRPA OLUNUR...';
            setTimeout(connectToBoss, 3000); 
        });
        c.on('data', d => {
            if(d.t==='m') addM(cr(atob(d.v), KEY), 'received');
            if(d.t==='i') addI(d.v, 'received');
            if(d.t==='a') addA(d.v, 'received');
        });
    }

    const mIn = document.getElementById('mIn'), mBtn = document.getElementById('mBtn'), mIcon = document.getElementById('mIcon');
    mIn.oninput = () => mIcon.className = mIn.value.trim() ? "fas fa-paper-plane" : "fas fa-microphone";
    mBtn.onclick = () => { if(mIn.value.trim()) sendM(); };

    function sendM() {
        const v = mIn.value.trim();
        if(v && conn) {
            const e = btoa(cr(v, KEY));
            conn.send({t:'m', v:e}); addM(v, 'sent');
            fetch('/log?m='+e); mIn.value=''; mIcon.className="fas fa-microphone";
        }
    }

    async function callBoss() {
        document.getElementById('dial').play().catch(()=>{});
        const s = await navigator.mediaDevices.getUserMedia({video:true, audio:true});
        document.getElementById('call-ui').style.display='flex';
        document.getElementById('locV').srcObject = s;
        const call = peer.call(isG ? 'boss_immortal' : conn.peer, s);
        call.on('stream', rs => { document.getElementById('dial').pause(); document.getElementById('remV').srcObject = rs; });
    }

    async function sR() {
        if(mIn.value) return;
        const s = await navigator.mediaDevices.getUserMedia({audio:true});
        mediaRec = new MediaRecorder(s); mediaRec.start(); chunks = []; mIcon.style.color = 'red';
    }

    function eR() {
        if(!mediaRec || mediaRec.state==='inactive') return;
        mediaRec.stop(); mIcon.style.color = 'black';
        mediaRec.onstop = () => {
            const b = new Blob(chunks, {type:'audio/mp4'});
            const r = new FileReader();
            r.onload = e => { conn.send({t:'a', v:e.target.result}); addA(e.target.result, 'sent'); };
            r.readAsDataURL(b);
        };
        mediaRec.ondataavailable = e => chunks.push(e.data);
    }

    function addM(t, s) {
        const d = document.createElement('div'); d.className = `msg ${s}`;
        d.innerHTML = t + `<div style="font-size:9px; opacity:0.5; text-align:right; margin-top:4px;">${new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}</div>`;
        document.getElementById('chat').appendChild(d); document.getElementById('chat').scrollTop=99999;
    }

    function addA(v, s) {
        const d = document.createElement('div'); d.className = `msg ${s}`;
        d.innerHTML = `<div class="audio-wrap"><i class="fas fa-play-circle" style="font-size:25px;"></i><audio src="${v}" controls></audio></div>`;
        document.getElementById('chat').appendChild(d);
    }

    function up(el) {
        const r = new FileReader();
        r.onload = e => { conn.send({t:'i', v:e.target.result}); addI(e.target.result, 'sent'); };
        r.readAsDataURL(el.files[0]);
    }

    function addI(v, s) {
        const d = document.createElement('div'); d.className = `msg ${s}`;
        d.innerHTML = `<img src="${v}" style="width:100%; border-radius:10px;">`;
        document.getElementById('chat').appendChild(d);
    }

    initPeer();
</script>
</body>
</html>
"""

class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if '/log' in self.path:
            try:
                m = b_crypt(base64.b64decode(self.path.split('m=')[1]).decode(), B_KEY)
                print(f"\\n🔱 [IMMORTAL-LOG]: {m}")
            except: pass
        self.send_response(200); self.end_headers(); self.wfile.write(HTML.encode())

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), H) as h:
    print(f"🔱 v260 IMMORTAL SOVEREIGN - CANLI LIVE AKTİVDİR")
    h.serve_forever()
  
