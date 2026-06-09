export default function handler(req, res) {
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.status(200).send(`<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>TrendBase Admin</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css"/>
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    :root{--bg:#0A0B0D;--bg2:#111318;--bg3:#181C23;--border:#22262F;--border2:#2E3340;--text:#EEF0F4;--text2:#7C8594;--text3:#3D4450;--green:#00D97E;--red:#FF4757;--orange:#FF8C42;--accent:#6C63FF;--card:#12151C}
    body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
    
    /* LOGIN */
    .login-wrap{display:flex;align-items:center;justify-content:center;min-height:100vh}
    .login-box{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:2.5rem;width:100%;max-width:360px}
    .login-logo{font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;margin-bottom:2rem;text-align:center}
    .login-logo span{color:var(--accent)}
    .login-label{font-size:.78rem;color:var(--text2);margin-bottom:.4rem;display:block}
    .login-input{width:100%;background:var(--bg3);border:1px solid var(--border2);color:var(--text);border-radius:8px;padding:.7rem 1rem;font-size:.88rem;font-family:'DM Sans',sans-serif;outline:none;margin-bottom:1rem}
    .login-input:focus{border-color:var(--accent)}
    .login-btn{width:100%;padding:.75rem;background:var(--accent);color:#fff;border:none;border-radius:8px;font-size:.9rem;font-weight:600;cursor:pointer;font-family:'DM Sans',sans-serif;transition:opacity .2s}
    .login-btn:hover{opacity:.85}
    .login-err{font-size:.78rem;color:var(--red);text-align:center;margin-top:.5rem;display:none}

    /* DASHBOARD */
    .dashboard{display:none}
    header{display:flex;align-items:center;justify-content:space-between;padding:1.25rem 2rem;border-bottom:1px solid var(--border);background:var(--bg2)}
    .header-logo{font-family:'Syne',sans-serif;font-weight:800;font-size:1.1rem}
    .header-logo span{color:var(--accent)}
    .header-right{display:flex;align-items:center;gap:1rem}
    .last-update{font-size:.75rem;color:var(--text2)}
    .refresh-btn{background:var(--bg3);border:1px solid var(--border2);color:var(--text2);padding:.4rem .8rem;border-radius:7px;font-size:.78rem;cursor:pointer;font-family:'DM Sans',sans-serif;display:flex;align-items:center;gap:.4rem;transition:all .2s}
    .refresh-btn:hover{color:var(--text);border-color:var(--accent)}
    .main{padding:2rem;max-width:1100px;margin:0 auto}
    .page-title{font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;margin-bottom:1.75rem}

    /* KPIs */
    .kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin-bottom:2rem}
    .kpi-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.25rem 1.5rem}
    .kpi-label{font-size:.72rem;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:.5rem;display:flex;align-items:center;gap:.4rem}
    .kpi-val{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;line-height:1}
    .kpi-sub{font-size:.75rem;margin-top:.35rem}
    .up{color:var(--green)} .dn{color:var(--red)} .neu{color:var(--text2)}

    /* GRID */
    .grid-2{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin-bottom:1.25rem}
    @media(max-width:700px){.grid-2{grid-template-columns:1fr}}
    .panel{background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden}
    .panel-head{padding:1rem 1.25rem;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
    .panel-head h3{font-size:.88rem;font-weight:600;display:flex;align-items:center;gap:.5rem}
    .panel-body{padding:1.25rem}

    /* ONBOARDING BARS */
    .ob-item{margin-bottom:1rem}
    .ob-label{display:flex;justify-content:space-between;font-size:.82rem;margin-bottom:.35rem}
    .ob-bar{height:8px;background:var(--bg3);border-radius:4px;overflow:hidden}
    .ob-fill{height:100%;border-radius:4px;transition:width .8s ease}

    /* TOP PRODUCTS TABLE */
    .top-table{width:100%;border-collapse:collapse}
    .top-table tr{border-bottom:1px solid var(--border)}
    .top-table tr:last-child{border-bottom:none}
    .top-table td{padding:.7rem .5rem;font-size:.82rem;vertical-align:middle}
    .rank{font-family:'Syne',sans-serif;font-weight:800;color:var(--text3);width:28px}
    .medal{font-size:1rem;width:28px;text-align:center}
    .prod-name{font-weight:500}
    .prod-cat{font-size:.7rem;color:var(--text2)}
    .count-badge{background:rgba(0,217,126,.12);color:var(--green);font-size:.72rem;font-weight:700;padding:.2rem .55rem;border-radius:100px}

    /* RECENT SALES */
    .sale-item{display:flex;align-items:center;gap:.75rem;padding:.65rem 0;border-bottom:1px solid var(--border)}
    .sale-item:last-child{border-bottom:none}
    .sale-dot{width:8px;height:8px;border-radius:50%;background:var(--green);flex-shrink:0}
    .sale-name{font-size:.82rem;font-weight:500;flex:1}
    .sale-cat{font-size:.7rem;color:var(--text2)}
    .sale-time{font-size:.7rem;color:var(--text3)}

    /* EMPTY */
    .empty{text-align:center;padding:2rem;color:var(--text2);font-size:.82rem}

    /* LOADING */
    .spinner{width:20px;height:20px;border:2px solid var(--border2);border-top-color:var(--accent);border-radius:50%;animation:spin .8s linear infinite;margin:2rem auto}
    @keyframes spin{to{transform:rotate(360deg)}}
  </style>
</head>
<body>

<!-- LOGIN -->
<div class="login-wrap" id="loginWrap">
  <div class="login-box">
    <div class="login-logo">Trend<span>Base</span> Admin</div>
    <label class="login-label">Contraseña de acceso</label>
    <input class="login-input" type="password" id="secretInput" placeholder="••••••••••••" onkeydown="if(event.key==='Enter')doLogin()"/>
    <button class="login-btn" onclick="doLogin()">Ingresar</button>
    <div class="login-err" id="loginErr">Contraseña incorrecta</div>
  </div>
</div>

<!-- DASHBOARD -->
<div class="dashboard" id="dashboard">
  <header>
    <div class="header-logo">Trend<span>Base</span> <span style="font-weight:300;color:var(--text2);font-size:.85rem">Admin</span></div>
    <div class="header-right">
      <span class="last-update" id="lastUpdate">—</span>
      <button class="refresh-btn" onclick="loadData()"><i class="ti ti-refresh"></i> Actualizar</button>
    </div>
  </header>

  <div class="main">
    <div class="page-title">Panel de control</div>

    <div class="kpi-grid" id="kpiGrid">
      <div class="kpi-card"><div class="kpi-label"><i class="ti ti-check"></i> Ventas totales</div><div class="kpi-val" id="kTotalSales">—</div><div class="kpi-sub up" id="kSalesSub">cargando...</div></div>
      <div class="kpi-card"><div class="kpi-label"><i class="ti ti-users"></i> Encuestas</div><div class="kpi-val" id="kOnboarding">—</div><div class="kpi-sub neu" id="kOnboardingSub">cargando...</div></div>
      <div class="kpi-card"><div class="kpi-label"><i class="ti ti-trending-up"></i> Tasa de éxito</div><div class="kpi-val up" id="kSuccess">—</div><div class="kpi-sub neu">respondieron "Sí vendí"</div></div>
      <div class="kpi-card"><div class="kpi-label"><i class="ti ti-star"></i> Producto top</div><div class="kpi-val" id="kTopProduct" style="font-size:1rem;letter-spacing:0;line-height:1.3">—</div><div class="kpi-sub up" id="kTopSales">—</div></div>
    </div>

    <div class="grid-2">
      <!-- Onboarding -->
      <div class="panel">
        <div class="panel-head"><h3><i class="ti ti-chart-bar"></i> Respuestas onboarding</h3><span id="obTotal" style="font-size:.75rem;color:var(--text2)"></span></div>
        <div class="panel-body" id="obPanel"><div class="spinner"></div></div>
      </div>

      <!-- Recent sales -->
      <div class="panel">
        <div class="panel-head"><h3><i class="ti ti-clock"></i> Ventas recientes</h3></div>
        <div class="panel-body" id="recentPanel"><div class="spinner"></div></div>
      </div>
    </div>

    <!-- Top products -->
    <div class="panel">
      <div class="panel-head"><h3><i class="ti ti-trophy"></i> Productos más vendidos por usuarios</h3></div>
      <div class="panel-body" id="topPanel"><div class="spinner"></div></div>
    </div>
  </div>
</div>

<script>
var SECRET = '';

function doLogin() {
  var val = document.getElementById('secretInput').value.trim();
  if(!val) return;
  SECRET = val;
  loadData();
}

async function loadData() {
  try {
    const res = await fetch('/api/admin?secret='+SECRET);
    if(res.status===401) {
      document.getElementById('loginErr').style.display='block';
      return;
    }
    const data = await res.json();
    document.getElementById('loginWrap').style.display='none';
    document.getElementById('dashboard').style.display='block';
    renderDashboard(data);
  } catch(e) {
    document.getElementById('loginErr').style.display='block';
  }
}

function timeAgo(dateStr) {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff/60000);
  if(mins < 1) return 'hace unos segundos';
  if(mins < 60) return 'hace '+mins+'min';
  const hrs = Math.floor(mins/60);
  if(hrs < 24) return 'hace '+hrs+'hs';
  return 'hace '+Math.floor(hrs/24)+'d';
}

function renderDashboard(data) {
  document.getElementById('lastUpdate').textContent = 'Actualizado ' + new Date().toLocaleTimeString('es-AR');

  // KPIs
  document.getElementById('kTotalSales').textContent = data.total_sales;
  document.getElementById('kSalesSub').textContent = data.total_sales === 1 ? '1 producto vendido' : data.total_sales+' productos vendidos';
  document.getElementById('kOnboarding').textContent = data.onboarding_total;
  const yesCount = data.onboarding_answers?.yes || 0;
  const successRate = data.onboarding_total > 0 ? Math.round(yesCount/data.onboarding_total*100) : 0;
  document.getElementById('kSuccess').textContent = successRate+'%';
  const top = data.top_products?.[0];
  document.getElementById('kTopProduct').textContent = top ? top.name : '—';
  document.getElementById('kTopSales').textContent = top ? top.count+' venta'+(top.count>1?'s':'') : 'sin datos aún';

  // Onboarding bars
  const ob = data.onboarding_answers || {yes:0,no:0,exploring:0};
  const obTotal = data.onboarding_total || 1;
  document.getElementById('obTotal').textContent = data.onboarding_total+' respuestas';
  const obItems = [
    {label:'✅ Sí, ya vendí algo', key:'yes', color:'var(--green)'},
    {label:'🔍 Explorando', key:'exploring', color:'var(--accent)'},
    {label:'😕 No encontré nada útil', key:'no', color:'var(--red)'},
  ];
  document.getElementById('obPanel').innerHTML = obItems.map(function(item){
    const count = ob[item.key]||0;
    const pct = Math.round(count/obTotal*100);
    return '<div class="ob-item">'+
      '<div class="ob-label"><span>'+item.label+'</span><span style="font-weight:600">'+count+' ('+pct+'%)</span></div>'+
      '<div class="ob-bar"><div class="ob-fill" style="width:'+pct+'%;background:'+item.color+'"></div></div>'+
    '</div>';
  }).join('') || '<div class="empty">Sin respuestas aún</div>';

  // Recent sales
  const recent = data.recent_sales || [];
  document.getElementById('recentPanel').innerHTML = recent.length ? recent.map(function(s){
    return '<div class="sale-item">'+
      '<div class="sale-dot"></div>'+
      '<div style="flex:1"><div class="sale-name">'+s.product_name+'</div><div class="sale-cat">'+s.product_cat+'</div></div>'+
      '<div class="sale-time">'+timeAgo(s.created_at)+'</div>'+
    '</div>';
  }).join('') : '<div class="empty">Aún no hay ventas registradas</div>';

  // Top products
  const tops = data.top_products || [];
  const medals = ['🥇','🥈','🥉'];
  document.getElementById('topPanel').innerHTML = tops.length ?
    '<table class="top-table">'+tops.map(function(p,i){
      return '<tr>'+
        '<td class="medal">'+(medals[i]||'<span class="rank">#'+(i+1)+'</span>')+'</td>'+
        '<td><div class="prod-name">'+p.name+'</div></td>'+
        '<td style="text-align:right"><span class="count-badge">'+p.count+' venta'+(p.count>1?'s':'')+'</span></td>'+
      '</tr>';
    }).join('')+'</table>'
    : '<div class="empty">Los productos vendidos por usuarios aparecerán aquí</div>';
}

// Auto-refresh cada 30 segundos si ya está logueado
setInterval(function(){ if(SECRET) loadData(); }, 30000);
</script>
</body>
</html>
`);
}
