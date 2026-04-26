import os
from flask import Flask, redirect, render_template_string

app = Flask(__name__)

HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Deepfake AI Videos Reporting Tool</title>
  <style>
    body{
      margin:0;
      font-family: Arial, sans-serif;
      background: #0b1220;
      color: #e8eefc;
      min-height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
    }
    .card{
      width:min(920px, 92vw);
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius:16px;
      padding: 28px 22px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.35);
      backdrop-filter: blur(8px);
      text-align:center;
    }
    h1{ margin: 0 0 8px 0; font-size: 1.7rem; }
    .sub{ margin:0 0 18px 0; opacity:0.9; font-size: 0.98rem; }

    .section{
      text-align:left;
      margin: 18px auto 0 auto;
      width:min(780px, 100%);
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.10);
      border-radius: 14px;
      padding: 16px;
    }
    .section h2{ margin:0 0 10px 0; font-size: 1.1rem; }
    ul{ margin: 8px 0 0 18px; padding:0; line-height: 1.55; }

    .btnRow{
      margin-top: 14px;
      display:flex;
      gap:10px;
      justify-content:center;
      flex-wrap:wrap;
    }
    a.button{
      cursor:pointer;
      padding: 12px 16px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 0.95rem;
      text-decoration:none;
      display:inline-block;
    }
    a.primary{ background: #4f7cff; color:white; }
    a.secondary{
      background: rgba(255,255,255,0.12);
      color:#e8eefc;
      border: 1px solid rgba(255,255,255,0.18);
    }

    .warn{ margin-top:12px; font-size:0.86rem; opacity:0.85; }
    .footer{ margin-top:14px; font-size:0.82rem; opacity:0.75; text-align:center; }

    .highlight{
      background: rgba(79,124,255,0.16);
      border: 1px solid rgba(79,124,255,0.35);
      border-radius: 12px;
      padding: 12px 14px;
      margin: 10px 0 12px 0;
      font-weight: 600;
    }

    /* Tap-to-call button */
    .callbtn{
      display:inline-block;
      padding: 12px 16px;
      border-radius: 12px;
      font-weight: 800;
      font-size: 0.95rem;
      text-decoration:none;
      background: #22c55e;
      color: #07120b;
      border: 1px solid rgba(255,255,255,0.18);
    }
    .callbtn:active{ transform: scale(0.98); }

    /* Show call button mainly for mobile */
    @media (min-width: 768px){
      .mobileOnly{ display:none; }
    }

    .meter{ display:grid; gap:10px; margin-top:10px; }
    input[type="range"]{ width:100%; }
    .scoreBox{
      display:flex;
      justify-content:space-between;
      font-size:0.92rem;
      opacity:0.95;
      align-items:center;
    }
    .tag{
      display:inline-block;
      padding:6px 10px;
      border-radius:999px;
      font-weight:700;
      font-size:0.85rem;
      background: rgba(255,255,255,0.10);
      border: 1px solid rgba(255,255,255,0.18);
    }
    .checklist{ margin-top:10px; display:grid; gap:8px; }
    .check{ display:flex; gap:10px; align-items:flex-start; }
    .check input{ margin-top: 3px; }
  </style>
</head>

<body>
  <div class="card">
    <h1>Deepfake AI Videos Reporting Tool</h1>
    <p class="sub">A simple awareness page to help you respond calmly and safely.</p>

    <div class="section">
      <h2>What to do when you see suspicious content</h2>

      <div class="highlight">
        🚨 <b>Financial Fraud / Money Lost?</b> Call <b>1930</b> immediately.
        <div style="margin-top:10px; text-align:center;">
          <a class="callbtn mobileOnly" href="tel:1930">📞 Tap to Call 1930</a>
        </div>
      </div>

      <ul>
        <li><b>If you see spam/scam online:</b> report it on the platform (YouTube / Instagram) and do not share it.</li>
        <li><b>If you see offensive content:</b> report it and block the account.</li>
        <li><b>To stay safe:</b> don’t panic. Save evidence, talk to parents/elders, and proceed step-by-step.</li>
        <li><b>If something must be officially reported:</b> use the Govt portal button below.</li>
      </ul>

      <div class="btnRow">
        <a class="button secondary" target="_blank" rel="noopener"
           href="https://support.google.com/youtube/answer/2802027">Report on YouTube</a>
        <a class="button secondary" target="_blank" rel="noopener"
           href="https://help.instagram.com/192435014247952">Report on Instagram</a>
      </div>

      <p class="warn">
        Note: App steps may change with updates. Always use the in-app “Report” option.
      </p>
    </div>

    <div class="section">
      <h2>Awareness Meter (Suspicion Score)</h2>
      <p style="margin:0; opacity:0.9;">
        This is <b>not</b> an AI detector. It helps you judge warning signs and decide the next safe action.
      </p>

      <div class="meter">
        <label for="score"><b>How suspicious does it feel?</b></label>
        <input id="score" type="range" min="0" max="100" value="35" oninput="updateScore(this.value)">

        <div class="scoreBox">
          <span>Low</span>
          <span class="tag" id="labelTag">Medium suspicion</span>
          <span>High</span>
        </div>

        <div class="checklist">
          <div class="check">
            <input type="checkbox" onchange="recalc()">
            <div>Face looks unnatural / lips don’t match audio.</div>
          </div>
          <div class="check">
            <input type="checkbox" onchange="recalc()">
            <div>Voice sounds robotic / sudden accent or tone changes.</div>
          </div>
          <div class="check">
            <input type="checkbox" onchange="recalc()">
            <div>Lighting/shadows look odd or blur flickers around the face.</div>
          </div>
          <div class="check">
            <input type="checkbox" onchange="recalc()">
            <div>It creates urgency or asks for money/OTP/personal info.</div>
          </div>
        </div>

        <p class="warn" id="adviceText">
          Advice: Pause. Don’t share. Verify from trusted sources or elders.
        </p>
      </div>

      <div class="btnRow">
        <a class="button primary" href="/report">Report on Govt Portal</a>
        <a class="button secondary" target="_blank" rel="noopener"
           href="https://cybercrime.gov.in/">Open Cybercrime Portal Home</a>
      </div>

      <p class="warn" style="text-align:center;">
        For financial fraud or money loss, call <b>1930</b> immediately.
      </p>

      <div class="footer">
        Reporting happens only on the official Government portal. This page does not collect or store personal data.
      </div>
    </div>
  </div>

<script>
  function updateScore(val){
    const tag = document.getElementById('labelTag');
    const advice = document.getElementById('adviceText');
    const v = parseInt(val, 10);

    if(v < 35){
      tag.textContent = "Low suspicion";
      advice.textContent = "Advice: Verify before sharing. If unsure, don’t forward it.";
    } else if(v < 70){
      tag.textContent = "Medium suspicion";
      advice.textContent = "Advice: Pause. Verify source. Report on the platform if needed.";
    } else {
      tag.textContent = "High suspicion";
      advice.textContent = "Advice: Don’t share. Save evidence. Talk to parents/elders. Report using official channels.";
    }
  }

  function recalc(){
    const checks = document.querySelectorAll('.checklist input[type="checkbox"]');
    let count = 0;
    checks.forEach(c => { if(c.checked) count++; });

    let base = 20;
    let score = base + (count * 15);
    if(score > 100) score = 100;

    const slider = document.getElementById('score');
    slider.value = score;
    updateScore(score);
  }

  updateScore(document.getElementById('score').value);
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/report")
def report():
    return redirect("https://cybercrime.gov.in/Webform/Accept.aspx")

if __name__ == "__main__":
    # Deployment-friendly: hosting platforms set PORT; local defaults to 5000
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)