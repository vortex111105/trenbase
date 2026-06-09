
// ── PLACEHOLDER products while API loads ──────────────────────────────────────
const PLACEHOLDER_IMGS = {
  Tecnología: 'https://picsum.photos/seed/101/400/300',
  Belleza:    'https://picsum.photos/seed/201/400/300',
  Hogar:      'https://picsum.photos/seed/301/400/300',
  Moda:       'https://picsum.photos/seed/401/400/300',
  Deportes:   'https://picsum.photos/seed/501/400/300',
};

const PLANS = {
  free:    { maxProducts: 20,    ai: false, advFilters: false, history: 7,  analysis: false, comparator: false, aiMessages: 0  },
  starter: { maxProducts: 150,   ai: true,  advFilters: true,  history: 90, analysis: true,  comparator: false, aiMessages: 10 },
  pro:     { maxProducts: 99999, ai: true,  advFilters: true,  history: 90, analysis: true,  comparator: true,  aiMessages: 15 },
};
function currentPlan(){ return PLANS[plan] || PLANS.free; }

const PLT={
  TT:{label:'TikTok',bg:'#000000',fg:'#fff'},
  IG:{label:'Instagram',bg:'#E1306C',fg:'#fff'},
  YT:{label:'YouTube',bg:'#FF0000',fg:'#fff'},
  PT:{label:'Pinterest',bg:'#E60023',fg:'#fff'},
  FB:{label:'Facebook',bg:'#1877F2',fg:'#fff'},
  AM:{label:'Amazon',bg:'#FF9900',fg:'#000'},
  ML:{label:'Mercado Libre',bg:'#FFE600',fg:'#000'},
  GT:{label:'Google Trends',bg:'#4285F4',fg:'#fff'},
  AE:{label:'AliExpress',bg:'#FF4747',fg:'#fff'},
};
const PRICES={AR:{starter:'$9.999/mes',pro:'$19.999/mes',period:'ARS'},UY:{starter:'$390/mes',pro:'$790/mes',period:'UYU'},CL:{starter:'$4.990/mes',pro:'$9.990/mes',period:'CLP'}};
const WEEKS=['Sem 1','Sem 2','Sem 3','Sem 4','Sem 5','Sem 6','Sem 7','Sem 8','Sem 9','Sem 10','Sem 11','Sem 12','Sem 13','Sem 14','Sem 15','Hoy'];
const LEADERS=['\u{1F1E6}\u{1F1F7} Argentina','\u{1F1FA}\u{1F1FE} Uruguay','\u{1F1E8}\u{1F1F1} Chile','\u{1F1E6}\u{1F1F7} Argentina','\u{1F1E8}\u{1F1F1} Chile','\u{1F1FA}\u{1F1FE} Uruguay','\u{1F1E6}\u{1F1F7} Argentina','\u{1F1E8}\u{1F1F1} Chile'];

let PRODUCTS = [];
let ALL_PRODUCTS = [];
let productsLoaded = false;
let user=null,plan='free',currentProd=null,authMode='login',aiHistory=[],aiLoading=false;
let saved=JSON.parse(localStorage.getItem('tb_saved')||'[]');
let filter={plt:'',region:'',cat:'',minMargin:0,comp:'',minPrice:0};
let filterOpen=false,histChart=null,analysisChart=null,currentPage=1;
const PAGE_SIZE=20;
let loadRetries = 0;

// ── LOAD PRODUCTS FROM API ────────────────────────────────────────────────────
async function loadProducts() {
  const loadingEl = document.getElementById('productsLoading');
  const kpiEl = document.getElementById('kpiProductos');
  try {
    if(loadingEl){loadingEl.style.display='flex';loadingEl.innerHTML='<div style="width:20px;height:20px;border:2px solid var(--border);border-top-color:var(--dark);border-radius:50%;animation:spin 1s linear infinite"></div><span style="font-size:.83rem;color:var(--text2)">Cargando productos...</span>';}
    const res = await fetch('/api/products');
    const text = await res.text();
    let data;
    try { data = JSON.parse(text); } catch(e) { throw new Error('Respuesta inválida del servidor'); }
    if(!res.ok) throw new Error(data.error || 'Error ' + res.status);

    // If no products or stale, trigger background generation
    if(!data.products || !data.products.length || data.stale || data.generating) {
      if(loadingEl) loadingEl.innerHTML='<div style="width:20px;height:20px;border:2px solid var(--border);border-top-color:var(--dark);border-radius:50%;animation:spin 1s linear infinite"></div><span style="font-size:.83rem;color:var(--text2)">Generando productos con IA... (puede tardar ~30 seg)</span>';
      // Trigger generation chain
      triggerGeneration(0);
      // If we have stale products, show them while generating
      if(data.products && data.products.length) {
        setProducts(data.products, data);
      }
      return;
    }

    setProducts(data.products, data);
  } catch(e) {
    console.error('Error cargando productos:', e.message);
    if(loadingEl) {
      loadingEl.style.display='flex';
      loadingEl.innerHTML = '<span style="color:var(--red);font-size:.8rem">⚠️ Error cargando productos. <button onclick="loadProducts()" style="background:var(--dark);color:var(--white);border:none;border-radius:6px;padding:.3rem .75rem;cursor:pointer;font-size:.75rem;margin-left:.5rem">Reintentar</button></span>';
    }
    if(loadRetries < 3) { loadRetries++; setTimeout(loadProducts, 4000); }
  }
}

function setProducts(products, data) {
  const loadingEl = document.getElementById('productsLoading');
  const kpiEl = document.getElementById('kpiProductos');
  // Map DB fields to frontend fields
  const mapped = products.map(p => ({
    name: p.name, cat: p.cat, score: p.score, change: p.change,
    changeNum: p.change_num !== undefined ? p.change_num : p.changeNum,
    plts: p.plts || [], margin: p.margin,
    marginStr: p.margin_str || p.marginStr,
    hot: p.hot, regions: p.regions || [],
    comp: p.comp, priceMin: p.price_min || p.priceMin,
    priceStr: p.price_str || p.priceStr,
    history: p.history || [], rank: p.rank || 0,
    suppliers: p.suppliers || [],
  }));
  ALL_PRODUCTS = mapped;
  PRODUCTS = mapped;
  productsLoaded = true;
  if(loadingEl) loadingEl.style.display='none';
  if(kpiEl) kpiEl.textContent = (data&&data.count?data.count:PRODUCTS.length) + '+';
  updateNav();
  renderLandingProducts();
  renderProducts(true);
  populateAnalysisSelect();
  if(document.getElementById('sec-analisis')&&document.getElementById('sec-analisis').style.display!=='none')renderAnalysis();
  const freshEl = document.getElementById('freshness');
  if(freshEl && data) {
    const mins = Math.floor((data.age||0)/60);
    freshEl.textContent = data.stale ? '⟳ Actualizando...' : (mins < 2 ? '✓ Recién actualizado' : 'Hace ' + mins + ' min');
    freshEl.style.color = data.stale ? 'var(--orange)' : 'var(--green)';
  }
}

async function triggerGeneration(batchIndex) {
  try {
    const res = await fetch('/api/generate?secret=trendbase2025&batch=' + batchIndex);
    const data = await res.json();
    if(data.nextBatch !== null && data.nextBatch !== undefined) {
      // Continue chain
      setTimeout(() => triggerGeneration(data.nextBatch), 1000);
    } else if(data.done) {
      // All done — reload products
      setTimeout(() => loadProducts(), 1000);
    }
  } catch(e) {
    console.error('Generation error batch ' + batchIndex + ':', e.message);
  }
}

async function loadAEProducts(productName, container) {
  try {
    const res = await fetch('/api/aliexpress?q='+encodeURIComponent(productName));
    const data = await res.json();
    if(!data.products||!data.products.length) return;
    const items = data.products.slice(0,4).map(p=>{
      const div = document.createElement('a');
      div.href = p.url;
      div.target = '_blank';
      div.rel = 'noopener';
      div.style.cssText = 'display:flex;align-items:center;gap:.75rem;padding:.75rem;background:var(--bg);border:1px solid var(--border);border-radius:10px;text-decoration:none;color:var(--text);transition:all .15s';
      div.onmouseover = () => div.style.borderColor = 'var(--dark)';
      div.onmouseout = () => div.style.borderColor = 'var(--border)';
      const img = document.createElement('img');
      img.src = '/api/imgproxy?url=' + encodeURIComponent(p.image);
      img.style.cssText = 'width:50px;height:50px;object-fit:cover;border-radius:6px;flex-shrink:0';
      img.onerror = () => img.style.display = 'none';
      const info = document.createElement('div');
      info.style.cssText = 'flex:1;min-width:0';
      info.innerHTML = '<div style="font-size:.82rem;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+p.title+'</div>' +
        '<div style="font-size:.75rem;color:var(--text2);margin-top:.15rem">' +
        (p.commission ? '<span style="background:#DCFCE7;color:#15803D;padding:.1rem .4rem;border-radius:3px;font-size:.68rem;font-weight:700;margin-right:.35rem">'+p.commission+'% comisión</span>' : '') +
        (p.rating ? '⭐ '+p.rating+'%' : '') + '</div>';
      const price = document.createElement('div');
      price.style.cssText = 'font-size:.9rem;font-weight:800;color:var(--green);flex-shrink:0';
      price.textContent = p.price;
      div.appendChild(img);div.appendChild(info);div.appendChild(price);
      return div;
    });
    const wrap = document.createElement('div');
    wrap.style.cssText = 'grid-column:1/-1;margin-top:.75rem';
    const title = document.createElement('div');
    title.className = 'modal-section-title';
    title.textContent = 'Productos reales en AliExpress';
    const list = document.createElement('div');
    list.style.cssText = 'display:flex;flex-direction:column;gap:.5rem';
    items.forEach(i => list.appendChild(i));
    wrap.appendChild(title);wrap.appendChild(list);
    container.appendChild(wrap);
  } catch(e) {
    console.log('AliExpress search error:', e.message);
  }
}


// ===== ANALYSIS ENGINE =====
let analysisPeriod = 30;
let catChartInst = null, pltChartInst = null;

function setAnalysisPeriod(days) {
  analysisPeriod = days;
  ['ap7','ap30','ap90'].forEach(function(id){var b=document.getElementById(id);if(b)b.classList.remove('ap-active');});
  var btn=document.getElementById('ap'+days);if(btn)btn.classList.add('ap-active');
  var base = ALL_PRODUCTS&&ALL_PRODUCTS.length ? ALL_PRODUCTS : PRODUCTS;
  if(!base||!base.length){renderAnalysis();return;}
  var histPoints = days===7?2:days===30?8:16;
  PRODUCTS = base.map(function(p) {
    var hist = p.history||[];
    var recent = hist.slice(-Math.min(histPoints,hist.length));
    var trend = recent.length>1?(recent[recent.length-1]-recent[0]):0;
    return Object.assign({}, p, {_trendScore: p.score + trend*0.5});
  }).sort(function(a,b){return b._trendScore - a._trendScore;});
  renderAnalysis();
}

async function renderPublicLeaderboard(){
  var el=document.getElementById('publicLeaderboard');
  if(!el){setTimeout(renderPublicLeaderboard,1000);return;}
  try{
    var controller=new AbortController();
    var timeout=setTimeout(function(){controller.abort();},5000);
    var res=await fetch('/api/leaderboard',{signal:controller.signal});
    clearTimeout(timeout);
    var data=await res.json();
    var tops=data.top_products||[];
    var total=data.total_sales||0;

    // Update stats
    var cSales=document.getElementById('cStatSales');
    var cUsers=document.getElementById('cStatUsers');
    var cTop=document.getElementById('cStatTop');
    if(cSales)cSales.textContent=total;
    if(cUsers)cUsers.textContent=tops.length;
    if(cTop&&tops[0])cTop.textContent=tops[0].name.split(' ').slice(0,3).join(' ')+'...';

    if(!tops.length){
      el.innerHTML='<div style="text-align:center;padding:2rem;color:var(--text2);font-size:.85rem;grid-column:1/-1">Sé el primero en registrar una venta 🚀</div>';
      return;
    }

    var medals=['🥇','🥈','🥉'];
    el.innerHTML=tops.slice(0,6).map(function(p,i){
      var barPct=Math.round(p.count/tops[0].count*100);
      return '<div style="background:var(--white);border:1px solid var(--border);border-radius:14px;padding:1.25rem;display:flex;flex-direction:column;gap:.75rem">'+
        '<div style="display:flex;align-items:center;gap:.75rem">'+
          '<span style="font-size:1.5rem">'+(medals[i]||'#'+(i+1))+'</span>'+
          '<div style="flex:1;min-width:0">'+
            '<div style="font-size:.88rem;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+p.name+'</div>'+
            '<div style="font-size:.72rem;color:var(--text2)">'+p.count+' venta'+(p.count>1?'s'+'':'')+'</div>'+
          '</div>'+
        '</div>'+
        '<div style="height:5px;background:var(--bg2);border-radius:3px">'+
          '<div style="width:'+barPct+'%;height:100%;background:'+(i===0?'#F59E0B':i===1?'#94A3B8':'#CD7C2F')+';border-radius:3px"></div>'+
        '</div>'+
      '</div>';
    }).join('');
  }catch(e){
    var el2=document.getElementById('publicLeaderboard');
    if(el2)el2.innerHTML='<div style="text-align:center;padding:2rem;color:var(--text2);font-size:.85rem;grid-column:1/-1">Sé el primero en registrar una venta 🚀</div>';
    var cS=document.getElementById('cStatSales');var cU=document.getElementById('cStatUsers');var cT=document.getElementById('cStatTop');
    if(cS)cS.textContent='0';if(cU)cU.textContent='0';if(cT)cT.textContent='—';
  }
}

function renderAnalysis() {
  var prods = PRODUCTS||ALL_PRODUCTS||[];
  if(!prods.length) { setTimeout(renderAnalysis, 800); return; }
  if(!PRODUCTS||!PRODUCTS.length) PRODUCTS = prods;
  renderAnalysisKPIs();
  renderOpportunities();
  renderGainers();
  renderMarginBars();
  renderRegionHeatmap();
  renderTopMargin();
  renderStartToday();
  populateComparators();
  setTimeout(function(){
    renderCatChart();
    renderPltChart();
    renderAnalysisCatChart();
  }, 100);
  if(!aiSummaryLoaded) renderAISummary();
  renderCommunityTop();
}

function renderAnalysisKPIs() {
  var el=document.getElementById('analysisKpis');if(!el)return;
  var prods=PRODUCTS;
  var avgScore=Math.round(prods.reduce(function(a,p){return a+p.score;},0)/prods.length);
  var avgMargin=Math.round(prods.reduce(function(a,p){return a+p.margin;},0)/prods.length);
  var cats={};prods.forEach(function(p){cats[p.cat]=(cats[p.cat]||0)+1;});
  var topCat=Object.entries(cats).sort(function(a,b){return b[1]-a[1];})[0];
  var hotCount=prods.filter(function(p){return p.hot;}).length;
  var lowComp=prods.filter(function(p){return p.comp==='Baja';}).length;
  var topScore=prods[0]?prods[0].score:0;
  el.innerHTML='<div class="kpi"><div class="kpi-label">Productos analizados</div><div class="kpi-value">'+prods.length+'</div><div class="kpi-sub kpi-up">'+hotCount+' HOT ahora</div></div>'+
    '<div class="kpi"><div class="kpi-label">Categoria lider ('+analysisPeriod+'d)</div><div class="kpi-value" style="font-size:1.1rem;letter-spacing:0">'+(topCat?topCat[0]:'')+'</div><div class="kpi-sub kpi-up">'+(topCat?Math.round(topCat[1]/prods.length*100):0)+'% del total</div></div>'+
    '<div class="kpi"><div class="kpi-label">Margen promedio ('+analysisPeriod+'d)</div><div class="kpi-value">'+avgMargin+'%</div><div class="kpi-sub kpi-up">↑ vs mes anterior</div></div>'+
    '<div class="kpi"><div class="kpi-label">Oportunidades Baja comp.</div><div class="kpi-value">'+lowComp+'</div><div class="kpi-sub" style="color:var(--green)">Score top: '+topScore+'</div></div>';
}

function opportunityScore(p) {
  var compScore=p.comp==='Baja'?3:p.comp==='Media'?2:1;
  return Math.round((p.score*p.margin*compScore)/100);
}

function renderOpportunities() {
  var el=document.getElementById('opportunityList');if(!el)return;
  var sorted=[].concat(PRODUCTS).sort(function(a,b){return opportunityScore(b)-opportunityScore(a);}).slice(0,5);
  el.innerHTML=sorted.map(function(p){
    var bg=p.comp==='Baja'?'#DCFCE7':p.comp==='Media'?'#FEF9C3':'#FEE2E2';
    var fg=p.comp==='Baja'?'#15803D':p.comp==='Media'?'#854D0E':'#B91C1C';
    var label=p.comp==='Baja'?'IDEAL':p.comp==='Media'?'BUENO':'DIFICIL';
    return '<div class="opp-item"><div style="flex:1;min-width:0"><div style="font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+p.name+'</div><div style="font-size:.7rem;color:var(--text2)">'+p.cat+' · comp '+p.comp+'</div></div><div style="text-align:right;margin-left:.5rem"><div style="font-weight:800;color:var(--green)">'+p.marginStr+'</div><div style="font-size:.68rem;color:var(--text2)">Score '+p.score+'</div></div><span class="opp-badge" style="background:'+bg+';color:'+fg+';margin-left:.5rem">'+label+'</span></div>';
  }).join('');
}

function renderGainers() {
  var el=document.getElementById('gainersList');if(!el)return;
  var sorted=[].concat(PRODUCTS).filter(function(p){return p.changeNum>0;}).sort(function(a,b){return b.changeNum-a.changeNum;}).slice(0,5);
  el.innerHTML=sorted.map(function(p){
    return '<div class="opp-item"><div style="flex:1;min-width:0"><div style="font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+p.name+'</div><div style="font-size:.7rem;color:var(--text2)">'+p.cat+'</div></div><span style="font-weight:800;color:var(--green);font-size:.9rem">'+p.change+'</span></div>';
  }).join('');
}

function renderCatChart() {
  // Dashboard cat chart (card-body with id catChart)
  var el=document.getElementById('catChart');
  if(!el)return;
  var cats={};
  (PRODUCTS||[]).forEach(function(p){if(p.cat)cats[p.cat]=(cats[p.cat]||0)+1;});
  var total=(PRODUCTS||[]).length||1;
  var sorted=Object.entries(cats).sort(function(a,b){return b[1]-a[1];}).slice(0,5);
  var colors=['#7B61FF','#00c47a','#00D4FF','#FF6B35','#FF4060'];
  el.innerHTML=sorted.map(function(e,i){
    var pct=Math.round(e[1]/total*100);
    return '<div style="margin-bottom:.75rem">'+
      '<div style="display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:4px">'+
        '<span style="color:var(--text2)">'+e[0]+'</span>'+
        '<span style="font-weight:600;color:'+(colors[i]||'#888')+'">'+pct+'%</span>'+
      '</div>'+
      '<div style="height:6px;border-radius:3px;background:var(--bg3)">'+
        '<div style="width:'+pct+'%;height:100%;border-radius:3px;background:'+(colors[i]||'#888')+'"></div>'+
      '</div>'+
    '</div>';
  }).join('');
  // Also render analysis cat chart
  renderAnalysisCatChart();
}

function renderAnalysisCatChart(){
  var el=document.getElementById('analysisCatChart');
  if(!el)return;
  var cats={};
  (PRODUCTS||[]).forEach(function(p){if(p.cat)cats[p.cat]=(cats[p.cat]||0)+1;});
  var total=(PRODUCTS||[]).length||1;
  var sorted=Object.entries(cats).sort(function(a,b){return b[1]-a[1];});
  var colors=['#1a1a2e','#7B61FF','#00c47a','#f59e0b','#00D4FF','#FF6B35'];
  el.innerHTML=sorted.map(function(e,i){
    var pct=Math.round(e[1]/total*100);
    return '<div style="margin-bottom:.5rem">'+
      '<div style="display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:.2rem">'+
        '<span style="font-weight:600">'+e[0]+'</span>'+
        '<span style="font-weight:700;color:'+(colors[i]||'#888')+'">'+pct+'%</span>'+
      '</div>'+
      '<div style="height:8px;border-radius:4px;background:var(--border)">'+
        '<div style="width:'+pct+'%;height:100%;border-radius:4px;background:'+(colors[i]||'#888')+';transition:width .6s ease"></div>'+
      '</div>'+
    '</div>';
  }).join('');
}

function renderPltChart() {
  var canvas=document.getElementById('pltChart');
  if(!canvas)return;
  if(typeof Chart==='undefined'){setTimeout(renderPltChart,300);return;}
  var plts={};
  var PLT_NAMES={TT:'TikTok',IG:'Instagram',YT:'YouTube',PT:'Pinterest',FB:'Facebook',AM:'Amazon',ML:'MercadoLibre',GT:'Google',AE:'AliExpress'};
  (PRODUCTS||[]).forEach(function(p){(p.plts||[]).forEach(function(pl){plts[pl]=(plts[pl]||0)+1;});});
  var sorted=Object.entries(plts).sort(function(a,b){return b[1]-a[1];}).slice(0,7);
  if(!sorted.length)return;
  var colors={TT:'#000',IG:'#E1306C',YT:'#FF0000',PT:'#E60023',FB:'#1877F2',AM:'#FF9900',ML:'#FFE600',GT:'#4285F4',AE:'#FF6A00'};
  try{if(pltChartInst){pltChartInst.destroy();pltChartInst=null;}}catch(e){}
  try{
    pltChartInst=new Chart(canvas,{
      type:'bar',
      data:{
        labels:sorted.map(function(x){return PLT_NAMES[x[0]]||x[0];}),
        datasets:[{data:sorted.map(function(x){return x[1];}),backgroundColor:sorted.map(function(x){return colors[x[0]]||'#888';}),borderRadius:4,borderSkipped:false}]
      },
      options:{responsive:true,maintainAspectRatio:true,plugins:{legend:{display:false}},scales:{y:{display:false},x:{ticks:{font:{size:9},maxRotation:30}}}}
    });
  }catch(e){console.error('pltChart error:',e);}
}

function renderMarginBars() {
  var el=document.getElementById('marginBars');if(!el)return;
  var cats={};PRODUCTS.forEach(function(p){if(!cats[p.cat])cats[p.cat]={total:0,count:0};cats[p.cat].total+=p.margin;cats[p.cat].count++;});
  var sorted=Object.entries(cats).map(function(e){return [e[0],Math.round(e[1].total/e[1].count)];}).sort(function(a,b){return b[1]-a[1];});
  el.innerHTML=sorted.map(function(e){return '<div class="cat-bar-item"><div class="cat-bar-label"><span>'+e[0]+'</span><span style="font-weight:700;color:var(--green)">'+e[1]+'%</span></div><div class="cat-bar-track"><div class="cat-bar-fill" style="width:'+e[1]+'%;background:var(--green)"></div></div></div>';}).join('');
}

function renderRegionHeatmap() {
  var el=document.getElementById('regionHeatmap');if(!el)return;
  var regions={AR:{count:0,name:'Argentina',flag:'🇦🇷',color:'#3b82f6'},UY:{count:0,name:'Uruguay',flag:'🇺🇾',color:'#10b981'},CL:{count:0,name:'Chile',flag:'🇨🇱',color:'#f59e0b'}};
  (PRODUCTS||[]).forEach(function(p){(p.regions||[]).forEach(function(r){if(regions[r])regions[r].count++;});});
  var total=(PRODUCTS||[]).length||1;
  el.innerHTML=Object.entries(regions).map(function(e){
    var k=e[0],r=e[1];
    var pct=Math.round(r.count/total*100);
    return '<div style="padding:.75rem;border-radius:10px;border:2px solid '+r.color+'20;background:'+r.color+'08">'+
      '<div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem">'+
        '<span style="font-size:1.4rem">'+r.flag+'</span>'+
        '<div><div style="font-weight:700;font-size:.85rem">'+r.name+'</div><div style="font-size:.7rem;color:var(--text2)">'+r.count+' productos</div></div>'+
        '<div style="margin-left:auto;font-size:1.1rem;font-weight:800;color:'+r.color+'">'+pct+'%</div>'+
      '</div>'+
      '<div style="height:8px;border-radius:4px;background:var(--border)">'+
        '<div style="width:'+pct+'%;height:100%;border-radius:4px;background:'+r.color+';transition:width .8s ease"></div>'+
      '</div>'+
    '</div>';
  }).join('');
}

function renderTopMargin() {
  var el=document.getElementById('topMarginList');if(!el)return;
  var sorted=[].concat(PRODUCTS).sort(function(a,b){return b.margin-a.margin;}).slice(0,5);
  el.innerHTML=sorted.map(function(p,i){return '<div class="opp-item"><span style="font-weight:800;color:var(--text3);margin-right:.5rem">#'+(i+1)+'</span><div style="flex:1;min-width:0"><div style="font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+p.name+'</div><div style="font-size:.7rem;color:var(--text2)">'+p.cat+'</div></div><span style="font-weight:800;color:var(--green)">'+p.marginStr+'</span></div>';}).join('');
}

function renderStartToday() {
  var el=document.getElementById('startTodayList');if(!el)return;
  var picks=[].concat(PRODUCTS).sort(function(a,b){return opportunityScore(b)-opportunityScore(a);}).slice(0,3);
  var medals=['🥇','🥈','🥉'];
  el.innerHTML=picks.map(function(p,i){
    var idx=PRODUCTS.indexOf(p);
    return '<div style="padding:.6rem;border:1px solid var(--border);border-radius:8px;margin-bottom:.5rem;cursor:pointer" onclick="openProduct('+idx+')"><div style="display:flex;justify-content:space-between;align-items:center"><div style="font-weight:600;font-size:.82rem">'+medals[i]+' '+p.name+'</div><span style="font-size:.7rem;font-weight:700;color:var(--green)">'+p.marginStr+'</span></div><div style="font-size:.7rem;color:var(--text2);margin-top:.2rem">'+p.cat+' · Competencia '+p.comp+' · Score '+p.score+'</div></div>';
  }).join('');
}

function calcROI() {
  var cost=parseFloat(document.getElementById('calcCost').value)||0;
  var price=parseFloat(document.getElementById('calcPrice').value)||0;
  var ads=parseFloat(document.getElementById('calcAds').value)||0;
  var sales=parseInt(document.getElementById('calcSales').value)||0;
  var el=document.getElementById('calcResult');if(!el)return;
  if(!cost||!price){el.innerHTML='<p style="font-size:.8rem;color:var(--text2)">Completa los campos.</p>';return;}
  var netPerSale=price-cost-ads;
  var monthlyProfit=netPerSale*sales;
  var margin=Math.round((netPerSale/price)*100);
  var roi=cost>0?Math.round((netPerSale/cost)*100):0;
  var breakeven=netPerSale>0?Math.ceil(cost/netPerSale):0;
  el.innerHTML='<div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem;margin-top:.25rem">'+
    '<div style="padding:.5rem;background:var(--bg2);border-radius:6px;text-align:center"><div style="font-size:.68rem;color:var(--text2)">Ganancia/venta</div><div style="font-weight:800;color:'+(netPerSale>0?'var(--green)':'var(--red)')+'">$'+netPerSale.toFixed(2)+'</div></div>'+
    '<div style="padding:.5rem;background:var(--bg2);border-radius:6px;text-align:center"><div style="font-size:.68rem;color:var(--text2)">Margen neto</div><div style="font-weight:800">'+margin+'%</div></div>'+
    '<div style="padding:.5rem;background:var(--bg2);border-radius:6px;text-align:center"><div style="font-size:.68rem;color:var(--text2)">ROI</div><div style="font-weight:800">'+roi+'%</div></div>'+
    '<div style="padding:.5rem;background:var(--bg2);border-radius:6px;text-align:center"><div style="font-size:.68rem;color:var(--text2)">Ganancia/mes</div><div style="font-weight:800;color:'+(monthlyProfit>0?'var(--green)':'var(--red)')+'">$'+monthlyProfit.toFixed(0)+'</div></div>'+
    '<div style="grid-column:1/-1;padding:.5rem;background:'+(netPerSale>0?'#F0FDF4':'#FEF2F2')+';border-radius:6px;text-align:center"><div style="font-size:.68rem;color:var(--text2)">Break-even</div><div style="font-weight:700;font-size:.9rem">'+breakeven+' ventas</div></div>'+
  '</div>';
}

function populateComparators() {
  var options='<option value="">Selecciona</option>'+PRODUCTS.slice(0,100).map(function(p,i){return '<option value="'+i+'">'+p.name+'</option>';}).join('');
  ['cmp1','cmp2'].forEach(function(id){
    var sel=document.getElementById(id);if(!sel)return;
    sel.innerHTML=options;
  });
  // Also populate analysisSelect for 90-day history
  var aSel=document.getElementById('analysisSelect');
  if(aSel){
    aSel.innerHTML='<option value="">-- Selecciona un producto --</option>'+PRODUCTS.slice(0,200).map(function(p,i){return '<option value="'+i+'">'+p.name+'</option>';}).join('');
  }
}

var histChartInst=null;
function renderAnalysisChart(){
  var sel=document.getElementById('analysisSelect');
  if(!sel||!sel.value){return;}
  var p=PRODUCTS[parseInt(sel.value)];
  if(!p)return;
  var hist=p.history||[];
  var container=document.getElementById('historyChartContainer');
  if(!container)return;

  // Generate history if product doesn't have one
  if(!hist.length){
    var base=p.score||50;
    hist=[];
    for(var i=0;i<13;i++){
      var v=Math.max(10,Math.min(100,base+Math.round((Math.random()-0.48)*18)));
      hist.push(v);base=v;
    }
  }

  var maxVal=Math.max.apply(null,hist)||1;
  // Generate labels dynamically
  var labels=hist.map(function(_,i){return 'S'+(i+1);});

  // Render as HTML bars (no Chart.js dependency)
  var BAR_HEIGHT=100;
  var html='<div style="display:flex;align-items:flex-end;gap:3px;height:'+(BAR_HEIGHT+40)+'px">';
  hist.forEach(function(v,i){
    var pct=Math.max(4,Math.round(v/maxVal*BAR_HEIGHT));
    var color=v>=70?'#00c47a':v>=40?'#7B61FF':'#8B95A3';
    html+='<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%">';
    html+='<div style="font-size:.58rem;color:#8B95A3;margin-bottom:2px">'+v+'</div>';
    html+='<div style="width:100%;height:'+pct+'px;background:'+color+';border-radius:3px 3px 0 0"></div>';
    html+='<div style="font-size:.55rem;color:#4A5260;margin-top:3px">'+labels[i]+'</div>';
    html+='</div>';
  });
  html+='</div>';
  html+='<div style="display:flex;justify-content:space-between;margin-top:.5rem;font-size:.72rem;color:var(--text2)">';
  html+='<span>Score: <b style="color:var(--text)">'+hist[hist.length-1]+'</b></span>';
  html+='<span>Pico: <b style="color:var(--green)">'+Math.max.apply(null,hist)+'</b></span>';
  html+='<span>Mín: <b style="color:var(--text3)">'+Math.min.apply(null,hist)+'</b></span>';
  html+='</div>';
  container.innerHTML=html;
}

// Sales tracking
function getUserId() {
  let uid = localStorage.getItem('tb_uid');
  if(!uid) { uid = 'u_'+Math.random().toString(36).slice(2)+Date.now().toString(36); localStorage.setItem('tb_uid', uid); }
  return uid;
}
function getSalesData() {
  try { return JSON.parse(localStorage.getItem('tb_sales')||'{}'); } catch(e){ return {}; }
}
function saveSalesData(data) {
  try { localStorage.setItem('tb_sales', JSON.stringify(data)); } catch(e){}
}

var currentProductIdx = null;
function markAsSold() {
  if(currentProductIdx===null) return;
  var p = PRODUCTS[currentProductIdx];
  if(!p) return;
  var sales = getSalesData();
  var key = (p.name||'').toLowerCase().trim();
  sales[key] = (sales[key]||0) + 1;
  saveSalesData(sales);
  // Also sync to negocio if product exists there
  var negProducts=getNegocioProducts();
  var negIdx=negProducts.findIndex(function(np){return (np.name||'').toLowerCase().trim()===key;});
  if(negIdx>=0){
    negProducts[negIdx].sold=(negProducts[negIdx].sold||0)+1;
    negProducts[negIdx].lastSale=Date.now();
    saveNegocioProducts(negProducts);
  }
  // Send to Supabase
  fetch('/api/track', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({
      type:'sale',
      user_id: getUserId(),
      product_name: p.name,
      product_cat: p.cat,
      product_score: p.score
    })
  }).catch(function(){});
  // Show confirmation
  var confirm = document.getElementById('soldConfirm');
  if(confirm) { confirm.classList.remove('hidden'); setTimeout(function(){ confirm.classList.add('hidden'); }, 3000); }
  // Update button
  var btn = document.getElementById('pmSoldBtn');
  if(btn) { btn.innerHTML='<i class="ti ti-check"></i> Registrado ✓'; btn.disabled=true; btn.style.opacity='.6'; }
  renderCommunityTop();
}

// ── PERFIL ─────────────────────────────────────────────────────────────────
function getProfile(){
  try{return JSON.parse(localStorage.getItem('tb_profile')||'{}');}catch(e){return{};}
}
function saveProfile(data){
  try{localStorage.setItem('tb_profile',JSON.stringify(data));}catch(e){}
  // Sync to Supabase
  fetch('/api/track',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({type:'profile',user_id:getUserId(),...data})}).catch(function(){});
}

function renderPerfil(){
  var el=document.getElementById('perfilContent');
  if(!el)return;
  var p=getProfile();
  el.innerHTML=`
  <div style="max-width:560px">
    <div style="background:var(--white);border:1px solid var(--border);border-radius:16px;padding:2rem;margin-bottom:1rem">
      <div style="display:flex;align-items:center;gap:1.25rem;margin-bottom:1.75rem">
        <div style="width:64px;height:64px;border-radius:50%;background:var(--dark);color:var(--white);display:flex;align-items:center;justify-content:center;font-size:1.5rem;font-weight:800;flex-shrink:0" id="avatarCircle">${(p.name||'?')[0].toUpperCase()}</div>
        <div>
          <div style="font-size:1.1rem;font-weight:700">${p.name||'Tu nombre'}</div>
          <div style="font-size:.8rem;color:var(--text2)">${p.country||'País no definido'} · Plan ${plan||'free'}</div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;gap:1rem">
        <div>
          <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Nombre o apodo</label>
          <input id="pfName" value="${p.name||''}" placeholder="Ej: Ignacio" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none"/>
        </div>
        <div>
          <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">País</label>
          <select id="pfCountry" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none">
            <option value="">Seleccioná tu país</option>
            <option value="Argentina" ${p.country==='Argentina'?'selected':''}>🇦🇷 Argentina</option>
            <option value="Uruguay" ${p.country==='Uruguay'?'selected':''}>🇺🇾 Uruguay</option>
            <option value="Chile" ${p.country==='Chile'?'selected':''}>🇨🇱 Chile</option>
            <option value="México" ${p.country==='México'?'selected':''}>🇲🇽 México</option>
            <option value="Colombia" ${p.country==='Colombia'?'selected':''}>🇨🇴 Colombia</option>
            <option value="Otro" ${p.country==='Otro'?'selected':''}>🌎 Otro</option>
          </select>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:.75rem">
          <div>
            <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Moneda de venta</label>
            <select id="pfSellCurrency" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none">
              <option value="ARS" \${(p.sellCurrency||'ARS')==='ARS'?'selected':''}>🇦🇷 ARS</option>
              <option value="UYU" \${p.sellCurrency==='UYU'?'selected':''}>🇺🇾 UYU</option>
              <option value="CLP" \${p.sellCurrency==='CLP'?'selected':''}>🇨🇱 CLP</option>
              <option value="USD" \${p.sellCurrency==='USD'?'selected':''}>🇺🇸 USD</option>
            </select>
          </div>
          <div>
            <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Moneda de compra</label>
            <select id="pfBuyCurrency" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none">
              <option value="USD" \${(p.buyCurrency||'USD')==='USD'?'selected':''}>🇺🇸 USD</option>
              <option value="ARS" \${p.buyCurrency==='ARS'?'selected':''}>🇦🇷 ARS</option>
              <option value="UYU" \${p.buyCurrency==='UYU'?'selected':''}>🇺🇾 UYU</option>
              <option value="CLP" \${p.buyCurrency==='CLP'?'selected':''}>🇨🇱 CLP</option>
            </select>
          </div>
        </div>
        <div>
          <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Meta mensual de ventas</label>
          <div style="display:flex;align-items:center;gap:.5rem">
            <input id="pfGoal" type="number" value="${p.goal||''}" placeholder="Ej: 10" min="1" max="999" style="width:100px;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none"/>
            <span style="font-size:.85rem;color:var(--text2)">ventas por mes</span>
          </div>
        </div>
        <div>
          <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Experiencia en dropshipping</label>
          <select id="pfExp" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none">
            <option value="">Seleccioná</option>
            <option value="nuevo" ${p.exp==='nuevo'?'selected':''}>🌱 Recién empiezo</option>
            <option value="basico" ${p.exp==='basico'?'selected':''}>📦 Menos de 1 año</option>
            <option value="intermedio" ${p.exp==='intermedio'?'selected':''}>🚀 1-3 años</option>
            <option value="avanzado" ${p.exp==='avanzado'?'selected':''}>💎 Más de 3 años</option>
          </select>
        </div>
        <div style="display:flex;align-items:center;gap:.5rem">
          <input type="checkbox" id="pfPublic" ${p.public?'checked':''} style="width:16px;height:16px;cursor:pointer"/>
          <label for="pfPublic" style="font-size:.83rem;cursor:pointer">Aparecer en el leaderboard público de TrendBase</label>
        </div>
        <button onclick="savePerfil()" style="padding:.75rem;background:var(--dark);color:var(--white);border:none;border-radius:10px;font-size:.88rem;font-weight:600;cursor:pointer;font-family:inherit;transition:opacity .2s">Guardar perfil</button>
        <div id="pfSaved" style="display:none;text-align:center;font-size:.82rem;color:var(--green)">✓ Perfil guardado</div>
      </div>
    </div>
  </div>`;
}

function savePerfil(){
  var name=document.getElementById('pfName').value.trim();
  var country=document.getElementById('pfCountry').value;
  var goal=parseInt(document.getElementById('pfGoal').value)||0;
  var exp=document.getElementById('pfExp').value;
  var pub=document.getElementById('pfPublic').checked;
  var sellCurrency=document.getElementById('pfSellCurrency').value;
  var buyCurrency=document.getElementById('pfBuyCurrency').value;
  saveProfile({name,country,goal,exp,public:pub,sellCurrency,buyCurrency});
  updateCurrencyDisplay();
  // Update avatar
  var av=document.getElementById('avatarCircle');
  if(av&&name)av.textContent=name[0].toUpperCase();
  var saved=document.getElementById('pfSaved');
  if(saved){saved.style.display='block';setTimeout(function(){saved.style.display='none';},2000);}
  // Re-render progress
  renderProgreso();
}

// ── PROGRESO ────────────────────────────────────────────────────────────────
var BADGES=[
  {id:'first',icon:'🥇',name:'Primera venta',desc:'Registraste tu primera venta',req:function(s){return s>=1;}},
  {id:'five',icon:'🔥',name:'En llamas',desc:'5 ventas registradas',req:function(s){return s>=5;}},
  {id:'ten',icon:'💎',name:'Dropshipper serio',desc:'10 ventas registradas',req:function(s){return s>=10;}},
  {id:'twenty',icon:'🚀',name:'En órbita',desc:'20 ventas registradas',req:function(s){return s>=20;}},
  {id:'fifty',icon:'👑',name:'Rey del drop',desc:'50 ventas registradas',req:function(s){return s>=50;}},
];

function renderProgreso(){
  var el=document.getElementById('progresoContent');
  if(!el)return;
  var sales=getSalesData();
  var totalSales=Object.values(sales).reduce(function(a,b){return a+b;},0);
  var totalProducts=Object.keys(sales).length;
  var saved=JSON.parse(localStorage.getItem('tb_saved')||'[]').length;
  var profile=getProfile();
  var goal=profile.goal||10;
  var goalPct=Math.min(100,Math.round(totalSales/goal*100));
  var activeBadges=BADGES.filter(function(b){return b.req(totalSales);});
  var nextBadge=BADGES.find(function(b){return !b.req(totalSales);});

  // Streak
  var streak=parseInt(localStorage.getItem('tb_streak')||'0');
  var lastActive=localStorage.getItem('tb_last_active');
  var today=new Date().toISOString().slice(0,10);
  if(lastActive!==today){
    var yesterday=new Date(Date.now()-86400000).toISOString().slice(0,10);
    streak=lastActive===yesterday?streak+1:1;
    localStorage.setItem('tb_streak',streak);
    localStorage.setItem('tb_last_active',today);
  }

  el.innerHTML=`
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-bottom:1.5rem">
    <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.25rem">
      <div style="font-size:.72rem;color:var(--text2);margin-bottom:.4rem;text-transform:uppercase;letter-spacing:.5px">Ventas registradas</div>
      <div style="font-size:2rem;font-weight:900">${totalSales}</div>
      <div style="font-size:.75rem;color:var(--green);margin-top:.25rem">${totalProducts} productos distintos</div>
    </div>
    <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.25rem">
      <div style="font-size:.72rem;color:var(--text2);margin-bottom:.4rem;text-transform:uppercase;letter-spacing:.5px">Guardados</div>
      <div style="font-size:2rem;font-weight:900">${saved}</div>
      <div style="font-size:.75rem;color:var(--text2);margin-top:.25rem">en tu lista</div>
    </div>
    <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.25rem">
      <div style="font-size:.72rem;color:var(--text2);margin-bottom:.4rem;text-transform:uppercase;letter-spacing:.5px">Racha activa</div>
      <div style="font-size:2rem;font-weight:900">${streak}🔥</div>
      <div style="font-size:.75rem;color:var(--text2);margin-top:.25rem">días consecutivos</div>
    </div>
    <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.25rem">
      <div style="font-size:.72rem;color:var(--text2);margin-bottom:.4rem;text-transform:uppercase;letter-spacing:.5px">Meta mensual</div>
      <div style="font-size:2rem;font-weight:900">${goalPct}%</div>
      <div style="height:6px;background:var(--bg2);border-radius:3px;margin-top:.5rem"><div style="width:${goalPct}%;height:100%;background:${goalPct>=100?'var(--green)':'var(--dark)'};border-radius:3px"></div></div>
      <div style="font-size:.72rem;color:var(--text2);margin-top:.3rem">${totalSales} de ${goal} ventas</div>
    </div>
  </div>

  <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.5rem;margin-bottom:1rem">
    <h3 style="font-size:.95rem;font-weight:700;margin-bottom:1.25rem">🏅 Logros</h3>
    <div style="display:flex;flex-wrap:wrap;gap:.75rem">
      ${BADGES.map(function(b){
        var earned=b.req(totalSales);
        return '<div style="display:flex;align-items:center;gap:.75rem;padding:.75rem 1rem;border-radius:10px;border:1px solid '+(earned?'var(--green)':'var(--border)')+';background:'+(earned?'rgba(22,163,74,.06)':'var(--bg2)')+';opacity:'+(earned?'1':'.5')+';min-width:200px">'+
          '<span style="font-size:1.5rem">'+b.icon+'</span>'+
          '<div><div style="font-size:.82rem;font-weight:600">'+(earned?b.name:'???')+'</div>'+
          '<div style="font-size:.72rem;color:var(--text2)">'+(earned?b.desc:'Seguí vendiendo')+'</div></div>'+
        '</div>';
      }).join('')}
    </div>
    ${nextBadge?'<div style="margin-top:1rem;font-size:.78rem;color:var(--text2)">Próximo logro: <b>'+nextBadge.name+'</b> '+nextBadge.icon+'</div>':'<div style="margin-top:1rem;font-size:.82rem;color:var(--green);font-weight:600">🎉 ¡Desbloqueaste todos los logros!</div>'}
  </div>

  <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.5rem">
    <h3 style="font-size:.95rem;font-weight:700;margin-bottom:1rem">📦 Productos que vendiste</h3>
    ${Object.keys(sales).length?
      '<div style="display:flex;flex-direction:column;gap:.5rem">'+
      Object.entries(sales).sort(function(a,b){return b[1]-a[1];}).map(function(e){
        return '<div style="display:flex;justify-content:space-between;align-items:center;padding:.5rem .75rem;background:var(--bg2);border-radius:8px">'+
          '<span style="font-size:.83rem;font-weight:500">'+e[0]+'</span>'+
          '<span style="font-size:.75rem;background:rgba(22,163,74,.1);color:var(--green);padding:.2rem .55rem;border-radius:100px;font-weight:700">'+e[1]+' venta'+(e[1]>1?'s':'')+'</span>'+
        '</div>';
      }).join('')+'</div>'
    :'<div style="text-align:center;padding:1.5rem;color:var(--text2);font-size:.83rem">Aún no registraste ventas.<br>Usá el botón <b>"Lo vendí"</b> en cada producto.</div>'}
  </div>`;
}

// ── MI NEGOCIO ─────────────────────────────────────────────────────────────
function timeAgo(ts){
  var diff=Date.now()-ts;
  var mins=Math.floor(diff/60000);
  if(mins<1)return 'hace unos segundos';
  if(mins<60)return 'hace '+mins+'min';
  var hrs=Math.floor(mins/60);
  if(hrs<24)return 'hace '+hrs+'hs';
  return 'hace '+Math.floor(hrs/24)+'d';
}

function getNegocioProducts(){
  try{return JSON.parse(localStorage.getItem('tb_negocio')||'[]');}catch(e){return[];}
}
function saveNegocioProducts(arr){
  try{localStorage.setItem('tb_negocio',JSON.stringify(arr));}catch(e){}
}

var editingNegocioIdx=null;

function showAddProductModal(idx){
  editingNegocioIdx = idx!==undefined ? idx : null;
  var products = getNegocioProducts();
  var p = idx!==undefined ? products[idx] : {};
  var overlay=document.createElement('div');
  overlay.id='negocioModal';
  overlay.style.cssText='position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:600;display:flex;align-items:center;justify-content:center;padding:1rem';
  // Build TrendBase products list
  var tbProducts = (PRODUCTS||[]).slice(0,100).map(function(p,i){return {name:p.name,cat:p.cat,score:p.score,idx:i};});

  overlay.innerHTML=`
  <div style="background:var(--white);border-radius:16px;width:100%;max-width:500px;max-height:90vh;overflow-y:auto">
    <div style="padding:1.25rem 1.5rem;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:var(--white);z-index:10">
      <h3 style="font-size:1rem;font-weight:700">${idx!==undefined?'Editar':'Agregar'} producto</h3>
      <button onclick="document.getElementById('negocioModal').remove()" style="background:transparent;border:none;cursor:pointer;font-size:1.2rem;color:var(--text2)">✕</button>
    </div>
    <div style="padding:1.5rem;display:flex;flex-direction:column;gap:1rem">
      ${idx===undefined?`
      <div>
        <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.5rem">Origen del producto</label>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem;margin-bottom:.75rem">
          <button id="srcCustom" onclick="setProductSource('custom')" style="padding:.65rem;border-radius:8px;border:2px solid var(--dark);background:var(--dark);color:var(--white);font-size:.82rem;font-weight:600;cursor:pointer;font-family:inherit;transition:all .2s">✏️ Producto propio</button>
          <button id="srcTrend" onclick="setProductSource('trend')" style="padding:.65rem;border-radius:8px;border:2px solid var(--border2);background:transparent;color:var(--text);font-size:.82rem;font-weight:600;cursor:pointer;font-family:inherit;transition:all .2s">🔥 De TrendBase</button>
        </div>
        <div id="trendSearch" style="display:none">
          <input id="np-trend-search" oninput="filterTrendProducts()" placeholder="Buscar producto de TrendBase..." style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none;margin-bottom:.5rem"/>
          <div id="trendList" style="max-height:180px;overflow-y:auto;border:1px solid var(--border);border-radius:8px;background:var(--bg)">
            ${tbProducts.map(function(tp){
              var tpJson=JSON.stringify(tp).replace(/"/g,"'");
              return '<div onclick="selectTrendProduct('+tpJson+',this)" style="padding:.6rem .875rem;cursor:pointer;font-size:.82rem;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center">'+
                '<span>'+tp.name+'</span>'+
                '<span style="font-size:.7rem;color:#71717A">'+tp.cat+' · '+tp.score+'</span>'+
              '</div>';
            }).join('')}
          </div>
        </div>
      </div>`:''}
      <div>
        <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Nombre del producto</label>
        <input id="np-name" value="${p.name||''}" placeholder="Ej: Mini proyector portátil" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none"/>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:.75rem">
        <div>
          <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Precio de costo (${getBuyCurrency()})</label>
          <input id="np-cost" type="number" value="${p.cost||''}" placeholder="5.25" min="0" step="0.01" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none"/>
        </div>
        <div>
          <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Precio de venta (${getSellCurrency()})</label>
          <input id="np-price" type="number" value="${p.price||''}" placeholder="15000" min="0" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none"/>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:.75rem">
        <div>
          <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Stock comprado</label>
          <input id="np-stock" type="number" value="${p.stock||''}" placeholder="10" min="0" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none"/>
        </div>
        <div>
          <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Unidades vendidas</label>
          <input id="np-sold" type="number" value="${p.sold||0}" placeholder="0" min="0" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none"/>
        </div>
      </div>
      <div>
        <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Inversión en publicidad (ARS)</label>
        <input id="np-ads" type="number" value="${p.ads||0}" placeholder="0" min="0" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none"/>
      </div>
      <div>
        <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Proveedor</label>
        <select id="np-supplier" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none">
          <option value="AliExpress" ${(p.supplier||'AliExpress')==='AliExpress'?'selected':''}>AliExpress</option>
          <option value="CJ Dropshipping" ${p.supplier==='CJ Dropshipping'?'selected':''}>CJ Dropshipping</option>
          <option value="Alibaba" ${p.supplier==='Alibaba'?'selected':''}>Alibaba</option>
          <option value="Local" ${p.supplier==='Local'?'selected':''}>Proveedor local</option>
          <option value="Otro" ${p.supplier==='Otro'?'selected':''}>Otro</option>
        </select>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:.75rem">
        <div>
          <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Tipo de cambio (${getBuyCurrency()}→${getSellCurrency()})</label>
          <input id="np-fx" type="number" value="${p.fx||1100}" placeholder="1100" min="1" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none"/>
        </div>
        <div>
          <label style="font-size:.75rem;font-weight:600;color:var(--text2);display:block;margin-bottom:.35rem">Estado</label>
          <select id="np-status" style="width:100%;padding:.65rem .875rem;border:1px solid var(--border2);border-radius:8px;font-size:.88rem;background:var(--bg);color:var(--text);font-family:inherit;outline:none">
            <option value="activo" ${(p.status||'activo')==='activo'?'selected':''}>🟢 Activo</option>
            <option value="pausado" ${p.status==='pausado'?'selected':''}>🟡 Pausado</option>
            <option value="agotado" ${p.status==='agotado'?'selected':''}>🔴 Agotado</option>
          </select>
        </div>
      </div>
      <div style="display:flex;gap:.75rem;margin-top:.5rem">
        <button onclick="saveNegocioProduct()" style="flex:1;padding:.75rem;background:var(--dark);color:var(--white);border:none;border-radius:10px;font-size:.88rem;font-weight:600;cursor:pointer;font-family:inherit">Guardar producto</button>
        ${idx!==undefined?'<button onclick="deleteNegocioProduct('+idx+')" style="padding:.75rem 1rem;background:transparent;border:1px solid var(--red);color:var(--red);border-radius:10px;font-size:.85rem;cursor:pointer;font-family:inherit">Eliminar</button>':''}
      </div>
    </div>
  </div>`;
  document.body.appendChild(overlay);
}

function setProductSource(type){
  var btnCustom=document.getElementById('srcCustom');
  var btnTrend=document.getElementById('srcTrend');
  var trendSearch=document.getElementById('trendSearch');
  if(!btnCustom)return;
  if(type==='custom'){
    btnCustom.style.background='var(--dark)';btnCustom.style.color='var(--white)';btnCustom.style.borderColor='var(--dark)';
    btnTrend.style.background='transparent';btnTrend.style.color='var(--text)';btnTrend.style.borderColor='var(--border2)';
    trendSearch.style.display='none';
  } else {
    btnTrend.style.background='var(--dark)';btnTrend.style.color='var(--white)';btnTrend.style.borderColor='var(--dark)';
    btnCustom.style.background='transparent';btnCustom.style.color='var(--text)';btnCustom.style.borderColor='var(--border2)';
    trendSearch.style.display='block';
  }
}

function filterTrendProducts(){
  var q=(document.getElementById('np-trend-search').value||'').toLowerCase();
  var items=document.getElementById('trendList').querySelectorAll('div');
  items.forEach(function(el){
    el.style.display=el.textContent.toLowerCase().includes(q)?'':'none';
  });
}

function selectTrendProduct(tp, el){
  // Fill name
  var nameInput=document.getElementById('np-name');
  if(nameInput)nameInput.value=tp.name;
  // Highlight selected
  document.getElementById('trendList').querySelectorAll('div').forEach(function(d){d.style.background='';});
  el.style.background='rgba(22,163,74,.1)';
  el.style.borderColor='var(--green)';
  // Track that this is a TrendBase product
  document.getElementById('np-name').dataset.trendProduct='true';
  document.getElementById('np-name').dataset.trendCat=tp.cat;
  document.getElementById('np-name').dataset.trendScore=tp.score;
}

function saveNegocioProduct(){
  var products=getNegocioProducts();
  var p={
    name:document.getElementById('np-name').value.trim(),
    cost:parseFloat(document.getElementById('np-cost').value)||0,
    price:parseFloat(document.getElementById('np-price').value)||0,
    stock:parseInt(document.getElementById('np-stock').value)||0,
    sold:parseInt(document.getElementById('np-sold').value)||0,
    ads:parseFloat(document.getElementById('np-ads').value)||0,
    supplier:document.getElementById('np-supplier').value,
    fx:parseFloat(document.getElementById('np-fx').value)||1100,
    status:document.getElementById('np-status').value,
    createdAt:editingNegocioIdx!==null?(products[editingNegocioIdx]?.createdAt||Date.now()):Date.now()
  };
  if(!p.name){alert('Ingresá el nombre del producto');return;}
  // Track if from TrendBase
  var nameEl=document.getElementById('np-name');
  if(nameEl&&nameEl.dataset.trendProduct){
    p.fromTrendBase=true;
    p.cat=nameEl.dataset.trendCat||'';
    p.score=parseInt(nameEl.dataset.trendScore)||0;
    // Track in Supabase as a product being sold from TrendBase
    fetch('/api/track',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({type:'sale',user_id:getUserId(),product_name:p.name,product_cat:p.cat,product_score:p.score})
    }).catch(function(){});
  }
  if(editingNegocioIdx!==null){products[editingNegocioIdx]=p;}else{products.push(p);}
  saveNegocioProducts(products);
  document.getElementById('negocioModal').remove();
  renderNegocio();
}

function deleteNegocioProduct(idx){
  if(!confirm('¿Eliminar este producto?'))return;
  var products=getNegocioProducts();
  products.splice(idx,1);
  saveNegocioProducts(products);
  document.getElementById('negocioModal').remove();
  renderNegocio();
}

function quickSale(idx){
  var products=getNegocioProducts();
  if(!products[idx])return;
  if(products[idx].sold>=products[idx].stock){
    showToast('Sin stock disponible','error');return;
  }
  products[idx].sold=(products[idx].sold||0)+1;
  products[idx].lastSale=Date.now();
  saveNegocioProducts(products);
  // Sync to unified sales tracker
  var sales=getSalesData();
  var key=(products[idx].name||'').toLowerCase().trim();
  sales[key]=(sales[key]||0)+1;
  saveSalesData(sales);
  // Sync to Supabase
  fetch('/api/track',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({type:'sale',user_id:getUserId(),product_name:products[idx].name,product_cat:'',product_score:0})
  }).catch(function(){});
  renderNegocio();
  showToast('¡Venta registrada! +1 '+products[idx].name,'success');
}

function quickStock(idx){
  var products=getNegocioProducts();
  if(!products[idx])return;
  var qty=parseInt(prompt('¿Cuántas unidades agregás al stock?','10'));
  if(isNaN(qty)||qty<=0)return;
  products[idx].stock=(products[idx].stock||0)+qty;
  saveNegocioProducts(products);
  renderNegocio();
  showToast('+'+qty+' unidades agregadas al stock','success');
}

function showToast(msg, type){
  var t=document.createElement('div');
  var bg=type==='success'?'var(--green)':type==='error'?'var(--red)':'var(--dark)';
  t.style.cssText='position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:'+bg+';color:#fff;padding:.65rem 1.25rem;border-radius:10px;font-size:.83rem;font-weight:600;z-index:999;box-shadow:0 4px 20px rgba(0,0,0,.15);white-space:nowrap;animation:fadeInUp .3s ease';
  t.textContent=msg;
  document.body.appendChild(t);
  setTimeout(function(){t.style.opacity='0';t.style.transition='opacity .3s';setTimeout(function(){t.remove();},300);},2500);
}

function renderNegocio(){
  var el=document.getElementById('negocioContent');
  if(!el)return;
  var products=getNegocioProducts();

  // Global KPIs
  var totalInverted=0,totalRevenue=0,totalAds=0,totalStock=0,totalSold=0;
  products.forEach(function(p){
    var costARS=p.cost*p.fx;
    var costConverted=p.cost*p.fx;
    totalInverted+=costConverted*p.stock;
    totalRevenue+=p.price*p.sold;
    totalAds+=p.ads;
    totalStock+=p.stock;
    totalSold+=p.sold;
  });
  var totalProfit=totalRevenue-totalInverted-totalAds;
  var roi=totalInverted>0?Math.round(totalProfit/(totalInverted+totalAds)*100):0;
  var stockValue=products.reduce(function(a,p){return a+p.cost*(p.fx||1)*(p.stock-p.sold);},0);

  var fmt=function(n){return formatCurrency(n);};

  // Unified progress stats
  var allSales=getSalesData();
  var totalAllSales=Object.values(allSales).reduce(function(a,b){return a+b;},0);
  var profile=getProfile();
  var goal=profile.goal||10;
  var goalPct=Math.min(100,Math.round(totalAllSales/goal*100));
  var streak=parseInt(localStorage.getItem('tb_streak')||'0');
  var activeBadge=BADGES.filter(function(b){return b.req(totalAllSales);}).pop();

  el.innerHTML=`
  <!-- Progreso unificado -->
  <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.25rem;margin-bottom:1rem;display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap">
    <div style="display:flex;align-items:center;gap:.75rem">
      <span style="font-size:1.75rem">${activeBadge?activeBadge.icon:'🌱'}</span>
      <div>
        <div style="font-size:.83rem;font-weight:700">${activeBadge?activeBadge.name:'Empezando'}</div>
        <div style="font-size:.72rem;color:var(--text2)">${totalAllSales} ventas totales · ${streak}🔥 días de racha</div>
      </div>
    </div>
    <div style="flex:1;min-width:200px">
      <div style="display:flex;justify-content:space-between;font-size:.72rem;color:var(--text2);margin-bottom:.3rem">
        <span>Meta mensual</span><span>${totalAllSales}/${goal} ventas (${goalPct}%)</span>
      </div>
      <div style="height:8px;background:var(--bg2);border-radius:4px"><div style="width:${goalPct}%;height:100%;background:${goalPct>=100?'var(--green)':'var(--dark)'};border-radius:4px;transition:width .6s"></div></div>
    </div>
    <button onclick="goSection('perfil')" style="padding:.4rem .875rem;background:var(--bg2);border:1px solid var(--border);border-radius:8px;font-size:.75rem;cursor:pointer;font-family:inherit;color:var(--text2)">Editar meta</button>
  </div>

  <!-- KPIs financieros -->
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.75rem;margin-bottom:1.5rem">
    <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.1rem">
      <div style="font-size:.7rem;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:.35rem">Ingresos totales</div>
      <div style="font-size:1.6rem;font-weight:900;color:var(--green)">${fmt(totalRevenue)}</div>
      <div style="font-size:.72rem;color:var(--text2);margin-top:.2rem">${totalSold} unidades vendidas</div>
    </div>
    <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.1rem">
      <div style="font-size:.7rem;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:.35rem">Ganancia neta</div>
      <div style="font-size:1.6rem;font-weight:900;color:${totalProfit>=0?'var(--green)':'var(--red)'}">${fmt(totalProfit)}</div>
      <div style="font-size:.72rem;color:var(--text2);margin-top:.2rem">ROI: ${roi}%</div>
    </div>
    <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.1rem">
      <div style="font-size:.7rem;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:.35rem">Inversión total</div>
      <div style="font-size:1.6rem;font-weight:900">${fmt(totalInverted+totalAds)}</div>
      <div style="font-size:.72rem;color:var(--text2);margin-top:.2rem">Stock + publicidad</div>
    </div>
    <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:1.1rem">
      <div style="font-size:.7rem;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:.35rem">Valor en stock</div>
      <div style="font-size:1.6rem;font-weight:900">${fmt(stockValue)}</div>
      <div style="font-size:.72rem;color:var(--text2);margin-top:.2rem">${totalStock-totalSold} unidades disponibles</div>
    </div>
  </div>

  <!-- Tabla de productos -->
  ${products.length?`
  <div style="background:var(--white);border:1px solid var(--border);border-radius:12px;overflow:hidden;margin-bottom:1rem">
    <div style="padding:1rem 1.25rem;border-bottom:1px solid var(--border);font-size:.88rem;font-weight:700">Mis productos</div>
    <div style="overflow-x:auto">
      <table style="width:100%;border-collapse:collapse">
        <thead>
          <tr style="background:var(--bg2)">
            <th style="text-align:left;padding:.6rem .875rem;font-size:.7rem;color:var(--text2);font-weight:600;text-transform:uppercase;letter-spacing:.5px">Producto</th>
            <th style="text-align:right;padding:.6rem .875rem;font-size:.7rem;color:var(--text2);font-weight:600;text-transform:uppercase;letter-spacing:.5px">Costo</th>
            <th style="text-align:right;padding:.6rem .875rem;font-size:.7rem;color:var(--text2);font-weight:600;text-transform:uppercase;letter-spacing:.5px">Venta</th>
            <th style="text-align:right;padding:.6rem .875rem;font-size:.7rem;color:var(--text2);font-weight:600;text-transform:uppercase;letter-spacing:.5px">Stock</th>
            <th style="text-align:right;padding:.6rem .875rem;font-size:.7rem;color:var(--text2);font-weight:600;text-transform:uppercase;letter-spacing:.5px">Vendido</th>
            <th style="text-align:right;padding:.6rem .875rem;font-size:.7rem;color:var(--text2);font-weight:600;text-transform:uppercase;letter-spacing:.5px">Ganancia</th>
            <th style="text-align:right;padding:.6rem .875rem;font-size:.7rem;color:var(--text2);font-weight:600;text-transform:uppercase;letter-spacing:.5px">ROI</th>
            <th style="padding:.6rem .875rem;font-size:.7rem;color:var(--text2);font-weight:600"></th>
          </tr>
        </thead>
        <tbody>
          ${products.map(function(p,i){
            var costSell=p.cost*p.fx; // cost converted to sell currency
            var ganancia=(p.price-costSell)*p.sold-p.ads;
            var roi=((costSell*p.stock)+p.ads)>0?Math.round(ganancia/((costSell*p.stock)+p.ads)*100):0;
            var remaining=p.stock-p.sold;
            var statusColor=p.status==='activo'?'#16a34a':p.status==='pausado'?'#d97706':'#dc2626';
            var stockAlert = remaining<=2 && p.stock>0;
            var lastSaleStr = p.lastSale ? timeAgo(p.lastSale) : 'Sin ventas';
            var profitIcon = ganancia>0?'▲':ganancia<0?'▼':'—';
            return '<tr style="border-top:1px solid var(--border)'+(stockAlert?';background:rgba(220,38,38,.03)':'')+'" >'+
              '<td style="padding:.75rem .875rem">'+
                '<div style="display:flex;align-items:center;gap:.5rem">'+
                  '<div style="width:6px;height:6px;border-radius:50%;background:'+statusColor+';flex-shrink:0"></div>'+
                  '<div>'+
                    '<div style="font-size:.83rem;font-weight:600">'+p.name+'</div>'+
                    '<div style="font-size:.7rem;color:var(--text2)">'+p.supplier+' · Última venta: '+lastSaleStr+'</div>'+
                    (stockAlert?'<div style="font-size:.68rem;color:var(--red);font-weight:600">⚠ Stock bajo</div>':'')+
                  '</div>'+
                '</div>'+
              '</td>'+
              '<td style="padding:.75rem .875rem;text-align:right;font-size:.82rem">'+p.cost.toFixed(2)+' '+getBuyCurrency()+'<br><span style="font-size:.7rem;color:var(--text2)">'+fmt(costSell)+'</span></td>'+
              '<td style="padding:.75rem .875rem;text-align:right;font-size:.82rem;font-weight:600">'+fmt(p.price)+'</td>'+
              '<td style="padding:.75rem .875rem;text-align:right">'+
                '<span style="font-size:.82rem;color:'+(stockAlert?'var(--red)':'inherit')+'">'+remaining+'/'+p.stock+'</span>'+
                '<div style="height:4px;background:var(--bg2);border-radius:2px;margin-top:3px;width:60px;margin-left:auto">'+
                  '<div style="width:'+(p.stock>0?Math.round(remaining/p.stock*100):0)+'%;height:100%;background:'+(stockAlert?'var(--red)':'var(--dark)')+';border-radius:2px"></div>'+
                '</div>'+
              '</td>'+
              '<td style="padding:.75rem .875rem;text-align:right;font-size:.82rem;font-weight:600;color:var(--green)">'+p.sold+'</td>'+
              '<td style="padding:.75rem .875rem;text-align:right;font-size:.82rem;font-weight:700;color:'+(ganancia>=0?'var(--green)':'var(--red)')+'">'+profitIcon+' '+fmt(Math.abs(ganancia))+'</td>'+
              '<td style="padding:.75rem .875rem;text-align:right;font-size:.82rem;font-weight:700;color:'+(roi>=0?'var(--green)':'var(--red)')+'">'+roi+'%</td>'+
              '<td style="padding:.75rem .875rem;text-align:right">'+
                '<div style="display:flex;gap:.35rem;justify-content:flex-end">'+
                  '<button onclick="quickSale('+i+')" title="Registrar venta" style="background:rgba(22,163,74,.1);border:1px solid rgba(22,163,74,.3);color:var(--green);border-radius:6px;padding:.3rem .6rem;font-size:.75rem;cursor:pointer;font-family:inherit;font-weight:700">+1 Venta</button>'+
                  '<button onclick="quickStock('+i+')" title="Agregar stock" style="background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:.3rem .6rem;font-size:.72rem;cursor:pointer;font-family:inherit">📦</button>'+
                  '<button onclick="showAddProductModal('+i+')" style="background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:.3rem .6rem;font-size:.72rem;cursor:pointer;font-family:inherit">✏️</button>'+
                '</div>'+
              '</td>'+
            '</tr>';
          }).join('')}
        </tbody>
      </table>
    </div>
  </div>`
  :'<div style="background:var(--white);border:1px solid var(--border);border-radius:12px;padding:3rem;text-align:center;color:var(--text2)"><div style="font-size:2rem;margin-bottom:1rem">📦</div><div style="font-weight:600;margin-bottom:.5rem">Todavía no agregaste productos</div><div style="font-size:.83rem;margin-bottom:1.5rem">Cargá tus productos para ver tu rentabilidad en tiempo real</div><button onclick="showAddProductModal()" style="padding:.75rem 1.5rem;background:var(--dark);color:var(--white);border:none;border-radius:10px;font-size:.88rem;font-weight:600;cursor:pointer;font-family:inherit">+ Agregar primer producto</button></div>'}
  `;
}

function renderCommunityTop() {
  var el = document.getElementById('communityTopProducts');
  if(!el) return;
  var sales = getSalesData();
  if(!Object.keys(sales).length) {
    el.innerHTML='<div style="font-size:.78rem;color:var(--text2);text-align:center;padding:1rem">Aún no hay ventas registradas. ¡Sé el primero en marcar un producto como vendido!</div>';
    return;
  }
  // Match sales with products
  var ranked = Object.entries(sales)
    .sort(function(a,b){ return b[1]-a[1]; })
    .slice(0,10)
    .map(function(e){
      var prod = PRODUCTS.find(function(p){ return (p.name||'').toLowerCase().trim()===e[0]; });
      return { name: e[0], count: e[1], prod: prod };
    })
    .filter(function(e){ return e.prod; });

  if(!ranked.length) {
    el.innerHTML='<div style="font-size:.78rem;color:var(--text2);text-align:center;padding:1rem">Sé el primero en registrar una venta.</div>';
    return;
  }

  var maxCount = ranked[0].count || 1;
  el.innerHTML = ranked.map(function(e, i){
    var pct = Math.round(e.count/maxCount*100);
    var medal = i===0?'🥇':i===1?'🥈':i===2?'🥉':'';
    return '<div style="display:flex;align-items:center;gap:.75rem;margin-bottom:.75rem;cursor:pointer" onclick="openProduct(PRODUCTS.indexOf(e.prod))">' +
      '<div style="font-size:1rem;width:24px;text-align:center">'+(medal||'<span style="font-size:.75rem;color:var(--text3)">#'+(i+1)+'</span>')+'</div>' +
      '<div style="flex:1">' +
        '<div style="font-size:.83rem;font-weight:600;margin-bottom:3px">' + e.prod.name + '</div>' +
        '<div style="height:6px;background:var(--border);border-radius:3px"><div style="width:'+pct+'%;height:100%;background:var(--green);border-radius:3px"></div></div>' +
      '</div>' +
      '<div style="font-size:.75rem;color:var(--green);font-weight:700;min-width:40px;text-align:right">' + e.count + ' venta'+(e.count>1?'s':'')+'</div>' +
    '</div>';
  }).join('');
}

function checkOnboarding() {
  var shown = localStorage.getItem('tb_onboarding_shown');
  if(shown) return;
  var firstVisit = localStorage.getItem('tb_first_visit');
  if(!firstVisit) { localStorage.setItem('tb_first_visit', Date.now()); return; }
  var daysSince = (Date.now() - parseInt(firstVisit)) / (1000*60*60*24);
  if(daysSince >= 7) {
    setTimeout(function(){
      var el = document.getElementById('onboardingPopup');
      if(el) el.classList.remove('hidden');
    }, 3000);
  }
}

function closeOnboarding() {
  var el = document.getElementById('onboardingPopup');
  if(el) el.classList.add('hidden');
  localStorage.setItem('tb_onboarding_shown', '1');
}

function answerOnboarding(answer) {
  closeOnboarding();
  fetch('/api/track', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({
      type:'onboarding',
      user_id: getUserId(),
      answer: answer,
      plan: currentPlan ? currentPlan().name : 'free'
    })
  }).catch(function(){});
  if(answer === 'yes') {
    setTimeout(function(){
      alert('¡Excelente! Si querés compartir tu experiencia, escribinos a hola@trendbase.app 🙌');
    }, 500);
  }
}

function compareProducts() {
  if(!currentPlan().comparator){ showUpgradeToast('El comparador de productos requiere plan Pro.'); return; }
  var i1=parseInt(document.getElementById('cmp1').value);
  var i2=parseInt(document.getElementById('cmp2').value);
  var el=document.getElementById('compareResult');if(!el)return;
  if(isNaN(i1)||isNaN(i2)||i1===i2){el.innerHTML='<p style="font-size:.8rem;color:var(--text2)">Selecciona dos productos distintos.</p>';return;}
  var a=PRODUCTS[i1],b=PRODUCTS[i2];
  var metrics=[
    {label:'Score',av:a.score,bv:b.score},
    {label:'Margen',av:a.margin,bv:b.margin},
    {label:'Cambio %',av:a.changeNum,bv:b.changeNum},
    {label:'Precio min',av:a.priceMin,bv:b.priceMin},
    {label:'Comp (3=Baja)',av:a.comp==='Baja'?3:a.comp==='Media'?2:1,bv:b.comp==='Baja'?3:b.comp==='Media'?2:1}
  ];
  el.innerHTML='<div style="display:grid;grid-template-columns:1fr auto 1fr;gap:.4rem;font-size:.8rem;margin-top:.5rem">'+
    '<div style="font-weight:700;text-align:center;padding:.4rem;background:var(--bg2);border-radius:6px">'+a.name.slice(0,20)+'</div>'+
    '<div style="display:flex;align-items:center;justify-content:center;font-size:.7rem;color:var(--text2)">VS</div>'+
    '<div style="font-weight:700;text-align:center;padding:.4rem;background:var(--bg2);border-radius:6px">'+b.name.slice(0,20)+'</div>'+
    metrics.map(function(m){
      return '<div style="text-align:center;padding:.35rem;border-radius:6px;background:'+(m.av>=m.bv?'#F0FDF4':'#fff')+';font-weight:'+(m.av>=m.bv?700:400)+'">'+m.av+'</div>'+
        '<div style="text-align:center;font-size:.7rem;color:var(--text2);display:flex;align-items:center;justify-content:center">'+m.label+'</div>'+
        '<div style="text-align:center;padding:.35rem;border-radius:6px;background:'+(m.bv>m.av?'#F0FDF4':'#fff')+';font-weight:'+(m.bv>m.av?700:400)+'">'+m.bv+'</div>';
    }).join('')+
  '</div>';
}

var aiSummaryLoaded=false;
async function renderAISummary() {
  var el=document.getElementById('aiSummary');if(!el)return;
  var top5=PRODUCTS.slice(0,5).map(function(p){return p.name+' (score '+p.score+', '+p.cat+')';}).join(', ');
  var cats={};PRODUCTS.forEach(function(p){cats[p.cat]=(cats[p.cat]||0)+1;});
  var catSummary=Object.entries(cats).sort(function(a,b){return b[1]-a[1];}).map(function(e){return e[0]+': '+e[1];}).join(', ');
  try{
    var res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:[{role:'user',content:'Sos un analista de mercado para dropshipping en LATAM. Datos: top productos: '+top5+'. Distribucion por categoria: '+catSummary+'. Total: '+PRODUCTS.length+' productos, periodo: '+analysisPeriod+' dias. Genera un resumen ejecutivo de 4-5 oraciones: tendencias principales, categoria con mas oportunidad, y una recomendacion concreta. Sin bullets, en parrafos.'}]})});
    var data=await res.json();
    var text=data.content&&data.content[0]?data.content[0].text:(data.text||'No se pudo generar.');
    el.innerHTML='<p style="line-height:1.7;color:var(--text)">'+text+'</p>';
    aiSummaryLoaded=true;
  }catch(e){el.innerHTML='<p style="color:var(--text2)">Error al generar. Intenta de nuevo.</p>';}
}

async function refreshAISummary(){
  aiSummaryLoaded=false;
  var el=document.getElementById('aiSummary');
  if(el)el.innerHTML='<div style="display:flex;align-items:center;gap:.5rem"><div style="width:16px;height:16px;border:2px solid var(--border);border-top-color:var(--dark);border-radius:50%;animation:spin 1s linear infinite"></div>Generando...</div>';
  await renderAISummary();
}

function init(){console.log("TrendBase v2.1 loaded");
  try{const s=JSON.parse(localStorage.getItem('tb_session')||'null');if(s&&s.email){user={email:s.email};plan=localStorage.getItem('tb_plan')||'free';}}catch(e){}
  if(location.search.includes('subscribed=1')){plan='starter';localStorage.setItem('tb_plan','starter');history.replaceState({},'','/');if(user)enterDash();}
  // Demo mode: ?demo=starter|pro
  const demoParam=new URLSearchParams(location.search).get('demo');
  if(demoParam&&['starter','pro'].includes(demoParam)){
    user={email:'demo@trendbase.app'};plan=demoParam;
    localStorage.setItem('tb_session',JSON.stringify({email:'demo@trendbase.app'}));
    localStorage.setItem('tb_plan',demoParam);
    history.replaceState({},'','/');
  }
  updateNav();renderWeekChart();renderCatChart();savedCount();
  // Load products async
  loadProducts();
  // Load public leaderboard
  setTimeout(renderPublicLeaderboard, 500);
  document.getElementById('navLogo').onclick=goLanding;
  document.getElementById('navInicio').onclick=goLanding;
  document.getElementById('navDash').onclick=()=>user?enterDash():openAuth();
  document.getElementById('navLogin').onclick=()=>openAuth('login');
  document.getElementById('navCTA').onclick=()=>user?enterDash():openAuth('signup');
  document.getElementById('heroCTA').onclick=()=>user?enterDash():openAuth('signup');
  document.getElementById('planFreeBtn').onclick=()=>user?enterDash():openAuth('signup');
  document.getElementById('planStarterBtn').onclick=()=>subscribe('starter');
  document.getElementById('planProBtn').onclick=()=>subscribe('pro');
  document.getElementById('ddDash').onclick=()=>{closeDD();enterDash();};
  document.getElementById('ddSaved').onclick=()=>{closeDD();enterDash();goSection('guardados');};
  let secs=6*60*60;setInterval(()=>{secs--;if(secs<0){secs=6*60*60;loadProducts();}const h=Math.floor(secs/3600),m=Math.floor((secs%3600)/60);const el=document.getElementById('countdown');if(el)el.textContent=h+'h '+m+'m';},1000);
  document.addEventListener('click',e=>{const dd=document.getElementById('userDD');const av=document.getElementById('userAvatar');if(dd&&!dd.contains(e.target)&&e.target!==av)dd.classList.add('hidden');});
  // Open sidebar groups by default
  // Sidebar groups start collapsed
}

function setCountry(c,btn){
  document.querySelectorAll('.country-btn').forEach(b=>b.classList.remove('active'));btn.classList.add('active');
  const p=PRICES[c];
  document.getElementById('starter-price').innerHTML=p.starter.split('/')[0]+' <span class="plan-period">'+p.period+'/'+p.starter.split('/')[1]+'</span>';
  document.getElementById('pro-price').innerHTML=p.pro.split('/')[0]+' <span class="plan-period">'+p.period+'/'+p.pro.split('/')[1]+'</span>';
  document.getElementById('free-period').textContent=p.period+'/mes';
}

function updateNav(){
  if(user){
    document.getElementById('navAuthBtns').classList.add('hidden');
    document.getElementById('navUser').classList.remove('hidden');
    document.getElementById('userAvatar').textContent=user.email.substring(0,2).toUpperCase();
    document.getElementById('userEmailLabel').innerHTML=user.email+'<br><span class="plan-badge">'+plan.charAt(0).toUpperCase()+plan.slice(1)+'</span>';
  }else{
    document.getElementById('navAuthBtns').classList.remove('hidden');
    document.getElementById('navUser').classList.add('hidden');
  }
  const cp=currentPlan();
  const gate=document.getElementById('planGate'),ai=document.getElementById('aiCard');
  if(cp.ai){gate&&gate.classList.add('hidden');ai&&ai.classList.remove('hidden');}
  else{gate&&gate.classList.remove('hidden');ai&&ai.classList.add('hidden');}
  // Filter panel only for paid plans
  const fp=document.getElementById('filterToggleBtn');
  if(fp){fp.style.opacity=cp.advFilters?'1':'0.4';fp.title=cp.advFilters?'':'Requiere plan Starter o superior';}
  // Analysis section only for starter+
  const sbAnalisis=document.getElementById('sb-analisis');
  if(sbAnalisis){sbAnalisis.style.opacity=cp.analysis?'1':'0.4';sbAnalisis.title=cp.analysis?'':'Requiere plan Starter o superior';}
  // Show plan limit banner in table
  const cp2=currentPlan();
  const limitBanner=document.getElementById('planLimitBanner');
  const tableTitle=document.getElementById('tableTitle');
  if(tableTitle)tableTitle.textContent='Top '+cp2.maxProducts+' productos';
  if(limitBanner){
    if(PRODUCTS.length>cp2.maxProducts){
      limitBanner.classList.remove('hidden');
      limitBanner.innerHTML='🔒 Estás viendo '+cp2.maxProducts+' de '+PRODUCTS.length+' productos. <button onclick="scrollToPlans()" style="background:var(--dark);color:var(--white);border:none;border-radius:6px;padding:.25rem .75rem;font-size:.75rem;cursor:pointer;font-family:Inter,sans-serif;font-weight:600;margin-left:.5rem">Desbloquear todo →</button>';
    } else { limitBanner.classList.add('hidden'); }
  }
}

function goLanding(){
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.getElementById('view-landing').classList.add('active');
  var mobileNav=document.getElementById('mobileNav');
  if(mobileNav)mobileNav.style.display='none';
  renderPublicLeaderboard();
}
function enterDash(){
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.getElementById('view-dash').classList.add('active');
  var mobileNav=document.getElementById('mobileNav');
  if(mobileNav){
    mobileNav.style.display=window.innerWidth<=480?'flex':'none';
    mobileNav.classList.add('dash-only');
  }
  var badge=document.getElementById('currencyBadge');
  if(badge){badge.style.display='inline-flex';badge.textContent=getSellCurrency();}
  goSection('tendencias');
}

function goSection(s){
  document.querySelectorAll('.dash-section').forEach(el=>el.classList.remove('active'));
  document.getElementById('sec-'+s).classList.add('active');
  document.querySelectorAll('.sidebar-item').forEach(el=>el.classList.remove('active'));
  const sb=document.getElementById('sb-'+s);if(sb)sb.classList.add('active');
  if(s==='guardados')renderSaved();
  if(s==='progreso')renderProgreso();
  if(s==='perfil')renderPerfil();
  if(s==='negocio')renderNegocio();
  if(s==='tendencias'){filter.plt='';filter.cat='';renderProducts(true);}
  if(s==='alertas'){const b=document.getElementById('alertBadge');if(b)b.classList.add('hidden');}
  if(s==='analisis'){
    // Free users can access analysis but with limited sections
    if(!currentPlan().analysis) {
      // Show analysis but hide premium cards after render
      setTimeout(function(){
        var cards = document.querySelectorAll('.analysis-card');
        cards.forEach(function(card){
          var h4 = card.querySelector('h4');
          if(!h4) return;
          var title = h4.textContent;
          var allowed = ['Calculadora','Para empezar','empezar hoy'];
          var isAllowed = allowed.some(function(t){ return title.toLowerCase().includes(t.toLowerCase()); });
          if(!isAllowed) {
            card.style.position='relative';
            card.style.overflow='hidden';
            var overlay = card.querySelector('.plan-overlay');
            if(!overlay){
              overlay = document.createElement('div');
              overlay.className='plan-overlay';
              overlay.style.cssText='position:absolute;inset:0;background:rgba(255,255,255,.85);backdrop-filter:blur(3px);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.5rem;z-index:10;border-radius:12px';
              overlay.innerHTML='<span style="font-size:1.2rem">🔒</span><span style="font-size:.78rem;font-weight:600;color:var(--text2)">Requiere Starter o Pro</span><button onclick="showUpgradeModal()" style="padding:.35rem .8rem;background:var(--dark);color:#fff;border:none;border-radius:6px;font-size:.75rem;cursor:pointer">Ver planes</button>';
              card.appendChild(overlay);
            }
          }
        });
      }, 300);
    }
  }
  if(s==='analisis'&&PRODUCTS.length){renderAnalysis();setTimeout(renderAnalysisCatChart,200);}
  const titles={tendencias:'Tendencias',analisis:'Análisis de mercado',alertas:'Alertas',guardados:'Guardados'};
  const t=document.getElementById('secTitle');if(t)t.textContent=titles[s]||'Dashboard';
}

// ── CURRENCY ────────────────────────────────────────────────────────────────
var CURRENCY_CONFIG = {
  ARS: { symbol: '$', name: 'ARS', locale: 'es-AR', decimals: 0 },
  UYU: { symbol: '$', name: 'UYU', locale: 'es-UY', decimals: 0 },
  CLP: { symbol: '$', name: 'CLP', locale: 'es-CL', decimals: 0 },
  USD: { symbol: 'USD ', name: 'USD', locale: 'en-US', decimals: 2 },
};

function getSellCurrency(){
  var p = getProfile();
  return p.sellCurrency || 'ARS';
}

function getBuyCurrency(){
  var p = getProfile();
  return p.buyCurrency || 'USD';
}

function formatCurrency(amount, currency){
  var cur = currency || getSellCurrency();
  var cfg = CURRENCY_CONFIG[cur] || CURRENCY_CONFIG.ARS;
  if(cfg.decimals > 0) return cfg.symbol + parseFloat(amount).toFixed(cfg.decimals);
  return cfg.symbol + Math.round(amount).toLocaleString(cfg.locale);
}

function updateCurrencyDisplay(){
  // Update currency badge in nav
  var badge = document.getElementById('currencyBadge');
  if(badge) badge.textContent = getSellCurrency();
  // Re-render negocio if visible
  var neg = document.getElementById('sec-negocio');
  if(neg && neg.classList.contains('active')) renderNegocio();
  var prog = document.getElementById('sec-progreso');
  if(prog && prog.classList.contains('active')) renderProgreso();
}

function toggleTheme(){
  var html=document.documentElement;
  var isDark=html.getAttribute('data-theme')==='dark';
  if(isDark){
    html.removeAttribute('data-theme');
    localStorage.setItem('tb_theme','light');
    ['themeIcon','themeIconMobile'].forEach(function(id){var el=document.getElementById(id);if(el)el.className='ti ti-moon';});
  } else {
    html.setAttribute('data-theme','dark');
    localStorage.setItem('tb_theme','dark');
    ['themeIcon','themeIconMobile'].forEach(function(id){var el=document.getElementById(id);if(el)el.className='ti ti-sun';});
  }
}

function initTheme(){
  var saved=localStorage.getItem('tb_theme');
  if(saved==='dark'){
    document.documentElement.setAttribute('data-theme','dark');
    ['themeIcon','themeIconMobile'].forEach(function(id){var el=document.getElementById(id);if(el)el.className='ti ti-sun';});
  }
}

function updateMobileNav(section) {
  document.querySelectorAll('.mobile-nav-item').forEach(function(b){ b.classList.remove('active'); });
  var btn = document.getElementById('mbn-'+section);
  if(btn) btn.classList.add('active');
}

function toggleSidebarGroup(id){
  const group=document.getElementById('group-'+id);
  const arrow=document.getElementById('arrow-'+id);
  if(!group)return;
  const isOpen=group.classList.contains('open');
  group.classList.toggle('open',!isOpen);
  if(arrow)arrow.classList.toggle('open',!isOpen);
}

function filterCat(cat){
  filter.cat=cat;filter.plt='';
  document.querySelectorAll('.sidebar-item').forEach(el=>el.classList.remove('active'));
  const key='sb-cat-'+(cat||'');
  const sb=document.getElementById(key);if(sb)sb.classList.add('active');
  document.querySelectorAll('.dash-section').forEach(el=>el.classList.remove('active'));
  document.getElementById('sec-tendencias').classList.add('active');
  const t=document.getElementById('secTitle');if(t)t.textContent=cat||'Tendencias';
  document.querySelectorAll('.cat-tab').forEach(tab=>{
    const match=!cat?tab.textContent.trim()==='Todos':tab.textContent.includes(cat);
    tab.classList.toggle('active',match);
  });
  renderProducts(true);
}

function filterCatTab(cat,btn){
  filter.cat=cat;
  document.querySelectorAll('.cat-tab').forEach(t=>t.classList.remove('active'));btn.classList.add('active');
  renderProducts(true);
}

function filterPlt(plt){
  filter.plt=plt;filter.cat='';
  document.querySelectorAll('.sidebar-item').forEach(el=>el.classList.remove('active'));
  const sb=document.getElementById('sb-'+plt);if(sb)sb.classList.add('active');
  document.querySelectorAll('.dash-section').forEach(el=>el.classList.remove('active'));
  document.getElementById('sec-tendencias').classList.add('active');
  const names={TT:'TikTok',IG:'Instagram',YT:'YouTube',PT:'Pinterest',FB:'Facebook',AM:'Amazon',ML:'Mercado Libre',GT:'Google Trends',AE:'AliExpress'};
  const t=document.getElementById('secTitle');if(t)t.textContent=names[plt];
  renderProducts(true);
}

function toggleFilterPanel(){
  if(!currentPlan().advFilters){showUpgradeToast('Los filtros avanzados requieren plan Starter o superior.');return;}
  filterOpen=!filterOpen;
  document.getElementById('filterPanel').classList.toggle('collapsed',!filterOpen);
  document.getElementById('filterToggleBtn').classList.toggle('active',filterOpen);
}

function toggleComp(val,btn){
  filter.comp=val;
  btn.parentElement.querySelectorAll('.filter-chip').forEach(c=>c.classList.remove('active'));
  btn.classList.add('active');renderProducts(true);
}

function toggleCountryFilter(val,btn){
  filter.region=val;
  btn.parentElement.querySelectorAll('.filter-chip').forEach(c=>c.classList.remove('active'));
  btn.classList.add('active');
  const rs=document.getElementById('regionSel');if(rs)rs.value=val;
  renderProducts(true);
}

function applyFilters(){
  const rs=document.getElementById('regionSel');if(rs)filter.region=rs.value;
  const mf=document.getElementById('marginFilter');if(mf){filter.minMargin=parseInt(mf.value)||0;const mv=document.getElementById('marginVal');if(mv)mv.textContent='Mín: '+filter.minMargin+'%';}
  const pf=document.getElementById('priceFilter');if(pf){filter.minPrice=parseInt(pf.value)||0;const pv=document.getElementById('priceVal');if(pv)pv.textContent='Mín: $'+filter.minPrice;}
  renderProducts(true);
}

function clearFilters(){
  filter.region='';filter.minMargin=0;filter.comp='';filter.minPrice=0;
  const mf=document.getElementById('marginFilter');if(mf)mf.value=0;
  const pf=document.getElementById('priceFilter');if(pf)pf.value=0;
  const mv=document.getElementById('marginVal');if(mv)mv.textContent='Mín: 0%';
  const pv=document.getElementById('priceVal');if(pv)pv.textContent='Mín: $0';
  const rs=document.getElementById('regionSel');if(rs)rs.value='';
  renderProducts(true);
}

function getFiltered(){
  const cp=currentPlan();
  const ss=document.getElementById('sortSel');
  const sort=ss?ss.value:'score';

  // Sort first, then apply plan limit, then filter by category/platform
  let all=[...PRODUCTS];
  if(sort==='change')all.sort((a,b)=>b.changeNum-a.changeNum);
  else if(sort==='margin')all.sort((a,b)=>b.margin-a.margin);
  else all.sort((a,b)=>b.score-a.score);

  // Apply plan limit FIRST — user only sees their allowed products
  let limited = all.slice(0, cp.maxProducts);

  // Now filter within that limited set
  return limited.filter(p=>{
    if(filter.plt&&!p.plts.includes(filter.plt))return false;
    if(filter.region&&!p.regions.includes(filter.region))return false;
    if(filter.cat&&p.cat!==filter.cat)return false;
    if(cp.advFilters){
      if(p.margin<filter.minMargin)return false;
      if(filter.comp&&p.comp!==filter.comp)return false;
      if(p.priceMin<filter.minPrice)return false;
    }
    return true;
  });
}

const CAT_EMOJI={'Tecnología':'💻','Belleza':'✨','Hogar':'🏠','Moda':'👗','Deportes':'🏆'};
const CAT_COLOR={'Tecnología':'#EFF6FF','Belleza':'#FDF4FF','Hogar':'#F0FDF4','Moda':'#FFFBEB','Deportes':'#FFF7ED'};

// Curated product images from Pexels — varied by category
const CAT_IMGS = {
  'Tecnología': [
    'https://images.pexels.com/photos/3780681/pexels-photo-3780681.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1714208/pexels-photo-1714208.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/356056/pexels-photo-356056.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1649771/pexels-photo-1649771.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/577769/pexels-photo-577769.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1591056/pexels-photo-1591056.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/4526414/pexels-photo-4526414.jpeg?auto=compress&cs=tinysrgb&w=400',
  ],
  'Belleza': [
    'https://images.pexels.com/photos/3373736/pexels-photo-3373736.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/2113855/pexels-photo-2113855.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/3735657/pexels-photo-3735657.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/3785147/pexels-photo-3785147.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/4041392/pexels-photo-4041392.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/2631985/pexels-photo-2631985.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/3762875/pexels-photo-3762875.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1115128/pexels-photo-1115128.jpeg?auto=compress&cs=tinysrgb&w=400',
  ],
  'Hogar': [
    'https://images.pexels.com/photos/1643383/pexels-photo-1643383.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1350789/pexels-photo-1350789.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/271618/pexels-photo-271618.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/2029694/pexels-photo-2029694.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1112598/pexels-photo-1112598.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/3935350/pexels-photo-3935350.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/6489107/pexels-photo-6489107.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/4352247/pexels-photo-4352247.jpeg?auto=compress&cs=tinysrgb&w=400',
  ],
  'Moda': [
    'https://images.pexels.com/photos/934070/pexels-photo-934070.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/996329/pexels-photo-996329.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1536619/pexels-photo-1536619.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/2220316/pexels-photo-2220316.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1082528/pexels-photo-1082528.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/3622608/pexels-photo-3622608.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/2294342/pexels-photo-2294342.jpeg?auto=compress&cs=tinysrgb&w=400',
  ],
  'Deportes': [
    'https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/2204196/pexels-photo-2204196.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1552249/pexels-photo-1552249.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/3621185/pexels-photo-3621185.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/2261477/pexels-photo-2261477.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/3490348/pexels-photo-3490348.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/4753879/pexels-photo-4753879.jpeg?auto=compress&cs=tinysrgb&w=400',
    'https://images.pexels.com/photos/1552212/pexels-photo-1552212.jpeg?auto=compress&cs=tinysrgb&w=400',
  ],
};

const imgCache = {};

function getProductImgSync(name, cat) {
  const key = (name||cat||'').toLowerCase().trim();
  if(imgCache[key]) return imgCache[key];
  // Return category fallback immediately (sync)
  const imgs = CAT_IMGS[cat] || CAT_IMGS['Tecnología'];
  let hash = 0;
  for(let i=0;i<(name||'').length;i++) hash = (hash*31 + (name||'').charCodeAt(i)) & 0xffff;
  return imgs[hash % imgs.length];
}

async function getProductImg(name, cat) {
  const key = (name||cat||'').toLowerCase().trim();
  if(imgCache[key]) return imgCache[key];
  try {
    // Search by product name via our proxy
    const q = encodeURIComponent((name||cat||'producto').split(' ').slice(0,5).join(' '));
    const res = await fetch('/api/imgproxy?q='+q);
    const data = await res.json();
    if(data.url) {
      imgCache[key] = data.url;
      return data.url;
    }
  } catch(e) {}
  // Fallback to category image
  return getProductImgSync(name, cat);
}

function imgEl(src,cls,cat,name){
  const emoji=CAT_EMOJI[cat]||'📦';
  const color=CAT_COLOR[cat]||'#F4F4F5';
  const cached=getProductImgSync(name||'',cat||'');
  if(cached){
    return '<img src="'+cached+'" class="'+cls+'" loading="lazy" data-emoji="'+emoji+'" data-color="'+color+'" onerror="imgFallback(this)"/>';
  }
  // Show emoji placeholder, load async
  const uid='img_'+Math.random().toString(36).slice(2);
  setTimeout(async()=>{
    const url=await getProductImg(name||'',cat||'');
    const el=document.getElementById(uid);
    if(el&&url){const img=document.createElement('img');img.src=url;img.className=el.className;img.loading='lazy';img.dataset.emoji=emoji;img.dataset.color=color;img.onerror=()=>imgFallback(img);el.replaceWith(img);}
  },0);
  return '<div id="'+uid+'" class="'+cls+'" style="background:'+color+';display:flex;align-items:center;justify-content:center;font-size:2rem">'+emoji+'</div>';
}

function imgFallback(el){
  el.onerror=null;
  const d=document.createElement('div');
  d.className=el.className;
  d.style.background=el.dataset.color||'#f4f4f5';
  d.style.display='flex';
  d.style.alignItems='center';
  d.style.justifyContent='center';
  d.style.fontSize='2rem';
  d.textContent=el.dataset.emoji||'📦';
  el.replaceWith(d);
}

function renderLandingProducts(){
  const el=document.getElementById('landingProducts');if(!el)return;
  if(!PRODUCTS.length){el.innerHTML='<div style="grid-column:1/-1;text-align:center;padding:3rem;color:var(--text2)"><div style="width:36px;height:36px;border:3px solid var(--border);border-top-color:var(--dark);border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 1rem"></div>Cargando productos...</div>';return;}
  el.innerHTML=PRODUCTS.slice(0,4).map(p=>{
    const idx=PRODUCTS.indexOf(p);
    const click=user?'enterDash();setTimeout(()=>openProduct('+idx+'),300)':'openAuth(\'signup\')';
    return '<div class="product-card" onclick="'+click+'">' +
      imgEl(p.img,'product-img',p.cat,p.name) +
      '<div class="product-info">' +
        '<div class="product-score"><span class="score-pill">'+p.score+'</span>' +
        '<span style="font-size:.72rem;font-weight:600;color:'+(p.changeNum>=0?'var(--green)':'var(--red)')+'">'+p.change+'</span>' +
        (p.hot?'<span class="tag tag-hot" style="font-size:.65rem">HOT</span>':'') +
        '</div>' +
        '<div class="product-name">'+p.name+'</div>' +
        '<div class="product-cat">'+p.cat+'</div>' +
        '<div class="product-footer">' +
          '<div class="product-margin">Margen '+p.marginStr+'</div>' +
          '<div class="product-plts">'+p.plts.map(pl=>'<span class="plt-pill" style="background:'+PLT[pl].bg+';color:'+PLT[pl].fg+'">'+pl+'</span>').join('')+'</div>' +
        '</div></div></div>';
  }).join('');
}

function renderProducts(resetPage){
  if(resetPage) currentPage=1;
  const allFiltered=getFiltered(),tbody=document.getElementById('productsTbody'),noRes=document.getElementById('noResults'),count=document.getElementById('resultsCount');
  if(!tbody)return;
  if(!PRODUCTS.length){
    tbody.innerHTML='<tr><td colspan="9" style="text-align:center;padding:2.5rem;color:var(--text2)"><div style="width:28px;height:28px;border:3px solid var(--border);border-top-color:var(--dark);border-radius:50%;animation:spin 1s linear infinite;margin:0 auto .75rem"></div>Generando productos con IA...</td></tr>';
    if(noRes)noRes.classList.add('hidden');if(count)count.textContent='Cargando...';
    renderPagination(0,0);return;
  }
  if(!allFiltered.length){tbody.innerHTML='';if(noRes)noRes.classList.remove('hidden');if(count)count.textContent='0 resultados';renderPagination(0,0);return;}
  if(noRes)noRes.classList.add('hidden');
  const totalPages=Math.ceil(allFiltered.length/PAGE_SIZE);
  if(currentPage>totalPages)currentPage=totalPages;
  const start=(currentPage-1)*PAGE_SIZE;
  const list=allFiltered.slice(start,start+PAGE_SIZE);
  if(count)count.textContent=allFiltered.length+' producto'+(allFiltered.length!==1?'s':', pág '+currentPage+'/'+totalPages);
  const tt=document.getElementById('tableTitle');
  const maxP=currentPlan().maxProducts;
  if(tt)tt.textContent=maxP>=9999?'Todos los productos':'Top '+maxP+' productos';
  tbody.innerHTML=list.map((p,i)=>{
    const idx=PRODUCTS.indexOf(p);
    const cc=p.comp==='Baja'?'comp-low':p.comp==='Alta'?'comp-high':'comp-med';
    return '<tr onclick="openProduct('+idx+')">' +
      '<td style="font-weight:800;color:var(--text3);font-size:.9rem">'+(start+i+1)+'</td>' +
      '<td style="min-width:180px"><div class="prod-row-info">'+imgEl(p.img,'prod-row-img',p.cat,p.name) +
        '<div><div class="prod-row-name">'+p.name+(p.hot?' <span class="tag tag-hot">HOT</span>':'')+'</div>' +
        '<div class="prod-row-cat">'+p.cat+'</div></div></div></td>' +
      '<td><div class="score-bar-wrap"><div class="score-bar"><div class="score-fill" style="width:'+p.score+'%;background:'+(p.score>90?'var(--green)':p.score>70?'var(--dark)':'var(--text3)')+'"></div></div><div class="score-val" style="color:'+(p.score>90?'var(--green)':p.score>70?'var(--dark)':'var(--text3)')+'">'+p.score+'</div></div></td>' +
      '<td><span class="tag '+(p.changeNum>=0?'tag-up':'tag-dn')+'">'+p.change+'</span></td>' +
      '<td style="font-weight:600;color:var(--green);font-size:.83rem">'+p.marginStr+'</td>' +
      '<td><span class="comp-badge '+cc+'">'+p.comp+'</span></td>' +
      '<td style="font-size:.82rem;color:var(--text2)">'+p.priceStr+'</td>' +
      '<td style="font-size:.82rem;color:var(--text3)">'+(p.suppliers&&p.suppliers[1]?p.suppliers[1].price:'—')+'</td>' +
      '<td><button onclick="event.stopPropagation();toggleSave('+idx+')" style="background:transparent;border:none;cursor:pointer;font-size:1rem;color:'+(saved.includes(idx)?'var(--dark)':'var(--text3)')+'"><i class="ti ti-bookmark'+(saved.includes(idx)?'-filled':'')+'"></i></button></td>' +
      '</tr>';
  }).join('');
  renderPagination(totalPages, allFiltered.length);
}

function renderPagination(totalPages, total){
  const el=document.getElementById('pagination');if(!el)return;
  if(totalPages<=1){el.innerHTML='';return;}
  let html='';
  // Prev button
  html+='<button class="page-btn" '+(currentPage===1?'disabled':'')+' onclick="goPage('+(currentPage-1)+')">‹</button>';
  // Page numbers
  const range=[];
  for(let i=1;i<=totalPages;i++){
    if(i===1||i===totalPages||Math.abs(i-currentPage)<=2) range.push(i);
    else if(range[range.length-1]!=='...') range.push('...');
  }
  range.forEach(p=>{
    if(p==='...') html+='<span style="padding:0 .25rem;color:var(--text3)">…</span>';
    else html+='<button class="page-btn'+(p===currentPage?' active':'')+'" onclick="goPage('+p+')">'+p+'</button>';
  });
  // Next button
  html+='<button class="page-btn" '+(currentPage===totalPages?'disabled':'')+' onclick="goPage('+(currentPage+1)+')">›</button>';
  html+='<span class="page-info">'+total+' productos</span>';
  el.innerHTML=html;
}

function goPage(p){
  currentPage=p;
  renderProducts();
  document.getElementById('sec-tendencias').scrollIntoView({behavior:'smooth',block:'start'});
}

function renderWeekChart(){
  const days=['Lun','Mar','Mié','Jue','Vie','Sáb','Hoy'],vals=[55,70,62,80,75,92,100];
  const el=document.getElementById('weekChart');if(!el)return;
  el.innerHTML=vals.map((v,i)=>'<div class="bar'+(i===6?' active-bar':'')+'" style="height:'+v+'%"></div>').join('');
  const wl=document.getElementById('weekLabels');if(wl)wl.innerHTML=days.map(d=>'<div class="bar-label">'+d+'</div>').join('');
}

function renderCatChart(){
  const cats=[{name:'Tecnología',pct:38},{name:'Belleza',pct:27},{name:'Hogar',pct:20},{name:'Moda',pct:15}];
  const el=document.getElementById('catChart');if(!el)return;
  el.innerHTML=cats.map(c=>'<div style="margin-bottom:.875rem"><div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="font-size:.78rem;color:var(--text2);font-weight:500">'+c.name+'</span><span style="font-size:.78rem;font-weight:700">'+c.pct+'%</span></div><div style="height:4px;background:var(--bg2);border-radius:2px;overflow:hidden"><div style="height:100%;width:'+c.pct+'%;background:var(--dark);border-radius:2px"></div></div></div>').join('');
}

function populateAnalysisSelect(){
  const sel=document.getElementById('analysisProductSel');if(!sel)return;
  sel.innerHTML='<option value="">— Seleccioná un producto —</option>'+PRODUCTS.map((p,i)=>'<option value="'+i+'">'+p.name+'</option>').join('');
}

function renderAnalysisHistory(){
  const sel=document.getElementById('analysisProductSel');if(!sel||sel.value==='')return;
  if(!currentPlan().analysis){showUpgradeToast('El análisis por producto requiere plan Starter o superior.');return;}
  const idx=parseInt(sel.value);const p=PRODUCTS[idx];
  const days=currentPlan().history;
  const hist=days===7?p.history.slice(-2):p.history;
  const wks=days===7?WEEKS.slice(-2):WEEKS;
  if(analysisChart){analysisChart.destroy();analysisChart=null;}
  const ctx=document.getElementById('analysisChart');
  if(ctx)analysisChart=buildChartSliced(ctx,hist,wks);
  renderHistoryTableSliced(p,hist,wks,'analysisTbody');
}

function buildChartSliced(ctx,historyData,labels){
  return new Chart(ctx,{type:'line',data:{labels:labels,datasets:[{label:'TrendScore',data:historyData,borderColor:'#09090B',backgroundColor:'rgba(9,9,11,.06)',borderWidth:2.5,pointRadius:4,pointBackgroundColor:'#09090B',pointBorderColor:'#fff',pointBorderWidth:2,tension:.4,fill:true}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:'#09090B',titleColor:'#fff',bodyColor:'rgba(255,255,255,.75)',padding:10,cornerRadius:8,callbacks:{label:ctx=>'Score: '+ctx.parsed.y}}},scales:{x:{grid:{display:false},ticks:{font:{size:10},color:'#A1A1AA',maxTicksLimit:8}},y:{min:0,max:100,grid:{color:'rgba(0,0,0,.05)'},ticks:{font:{size:10},color:'#A1A1AA',stepSize:20}}}}});
}

function renderHistoryTableSliced(p,historyData,labels,tbodyId){
  const tbody=document.getElementById(tbodyId);if(!tbody)return;
  tbody.innerHTML=historyData.map((score,i)=>{
    const prev=historyData[i-1]||score;const diff=score-prev;
    return '<tr><td>'+labels[i]+'</td><td style="font-weight:700">'+score+'</td><td style="color:'+(diff>=0?'var(--green)':'var(--red)')+';font-weight:600">'+(diff>=0?'+':'')+diff+'</td><td>'+LEADERS[i%LEADERS.length]+'</td></tr>';
  }).join('');
}

function buildChart(ctx,p){
  return new Chart(ctx,{type:'line',data:{labels:WEEKS,datasets:[{label:'TrendScore',data:p.history,borderColor:'#09090B',backgroundColor:'rgba(9,9,11,.06)',borderWidth:2.5,pointRadius:4,pointBackgroundColor:'#09090B',pointBorderColor:'#fff',pointBorderWidth:2,tension:.4,fill:true}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:'#09090B',titleColor:'#fff',bodyColor:'rgba(255,255,255,.75)',padding:10,cornerRadius:8,callbacks:{label:ctx=>'Score: '+ctx.parsed.y}}},scales:{x:{grid:{display:false},ticks:{font:{size:10},color:'#A1A1AA',maxTicksLimit:8}},y:{min:0,max:100,grid:{color:'rgba(0,0,0,.05)'},ticks:{font:{size:10},color:'#A1A1AA',stepSize:20}}}}});
}

function renderHistoryTable(p,tbodyId){
  const tbody=document.getElementById(tbodyId);if(!tbody)return;
  tbody.innerHTML=p.history.map((score,i)=>{
    const prev=p.history[i-1]||score;const diff=score-prev;
    return '<tr><td>'+WEEKS[i]+'</td><td style="font-weight:700">'+score+'</td><td style="color:'+(diff>=0?'var(--green)':'var(--red)')+';font-weight:600">'+(diff>=0?'+':'')+diff+'</td><td>'+LEADERS[i%LEADERS.length]+'</td></tr>';
  }).join('');
}

function switchModalTab(tab,btn){
  // Block history for free plan
  if(tab==='history'&&!currentPlan().history>7){
    showUpgradeToast('El historial de 90 días requiere plan Starter o superior.');return;
  }
  document.querySelectorAll('.modal-tab').forEach(t=>t.classList.remove('active'));btn.classList.add('active');
  document.querySelectorAll('.modal-tab-content').forEach(c=>c.classList.remove('active'));
  document.getElementById('tab-'+tab).classList.add('active');
  if(tab==='history'&&currentProd!==null){
    const p=PRODUCTS[currentProd];
    const days=currentPlan().history;
    const slicedHistory=days===7?p.history.slice(-2):p.history;
    const slicedWeeks=days===7?WEEKS.slice(-2):WEEKS;
    if(histChart){histChart.destroy();histChart=null;}
    const ctx=document.getElementById('historyChart');
    if(ctx)histChart=buildChartSliced(ctx,slicedHistory,slicedWeeks);
    renderHistoryTableSliced(p,slicedHistory,slicedWeeks,'historyTbody');
  }
}

function showUpgradeToast(msg){
  let t=document.getElementById('upgradeToast');
  if(!t){t=document.createElement('div');t.id='upgradeToast';t.style.cssText='position:fixed;bottom:2rem;left:50%;transform:translateX(-50%);background:var(--dark);color:var(--white);padding:.75rem 1.5rem;border-radius:10px;font-size:.85rem;font-weight:500;z-index:9999;display:flex;gap:1rem;align-items:center;box-shadow:0 8px 30px rgba(0,0,0,.2)';document.body.appendChild(t);}
  t.innerHTML=msg+'<button onclick="scrollToPlans()" style="background:var(--white);color:var(--dark);border:none;border-radius:6px;padding:.3rem .75rem;font-size:.78rem;cursor:pointer;font-weight:700;font-family:Inter,sans-serif">Ver planes</button>';
  t.style.display='flex';clearTimeout(t._to);t._to=setTimeout(()=>t.style.display='none',4000);
}

function openProduct(idx){ currentProductIdx=idx;
  const p=PRODUCTS[idx];if(!p)return;currentProd=idx;
  document.getElementById('pmTitle').textContent=p.name;
  document.getElementById('pmImgWrap').innerHTML=imgEl(p.img,'prod-modal-img',p.cat,p.name);
  document.getElementById('pmScore').textContent=p.score;
  document.getElementById('pmChange').textContent=p.change;
  document.getElementById('pmMargin').textContent=p.marginStr;
  document.getElementById('pmCat').textContent=p.cat;
  document.getElementById('pmPrice').textContent=p.priceStr;
  const ce=document.getElementById('pmComp');
  ce.textContent=p.comp;ce.className='comp-badge '+(p.comp==='Baja'?'comp-low':p.comp==='Alta'?'comp-high':'comp-med');
  const tag=document.getElementById('pmTag');tag.textContent=p.hot?'HOT':'TENDENCIA';tag.className='tag '+(p.hot?'tag-hot':'tag-up');
  document.getElementById('pmPlats').innerHTML=p.plts.map(pl=>'<span class="plt-badge" style="background:'+PLT[pl].bg+';color:'+PLT[pl].fg+'">'+PLT[pl].label+'</span>').join('');
  const cmap={AR:'\u{1F1E6}\u{1F1F7} Argentina',UY:'\u{1F1FA}\u{1F1FE} Uruguay',CL:'\u{1F1E8}\u{1F1F1} Chile'};
  document.getElementById('pmCountries').innerHTML=(p.regions||[]).map(r=>'<span style="font-size:.82rem;background:var(--bg2);padding:.3rem .75rem;border-radius:6px;font-weight:500">'+(cmap[r]||r)+'</span>').join('');
  const suppEl=document.getElementById('pmSuppliers');
  renderSuppliersTab(p, suppEl);
  document.getElementById('pmSaveBtn').innerHTML=saved.includes(idx)?'<i class="ti ti-bookmark-filled"></i> Guardado':'<i class="ti ti-bookmark"></i> Guardar';
  document.querySelectorAll('.modal-tab').forEach((t,i)=>t.classList.toggle('active',i===0));
  document.querySelectorAll('.modal-tab-content').forEach((c,i)=>c.classList.toggle('active',i===0));
  if(histChart){histChart.destroy();histChart=null;}
  document.getElementById('prodModal').classList.remove('hidden');
}

// ── SUPPLIERS ───────────────────────────────────────────────────────────────
const SUPPLIERS_BUY = [
  { name:'AliExpress', icon:'🛒', url:'https://www.aliexpress.com/wholesale?SearchText=', aff:true, ship:'10-25 días · Envío gratis', note:'El más popular para dropshipping', color:'#FF4747' },
  { name:'Alibaba', icon:'🏭', url:'https://www.alibaba.com/trade/search?SearchText=', aff:true, ship:'20-35 días · Mayorista', note:'Precios más bajos, mínimo por lote', color:'#FF6A00' },
  { name:'DHgate', icon:'🌐', url:'https://www.dhgate.com/wholesale/search.do?searchkey=', aff:true, ship:'15-30 días · Desde China', note:'Sin mínimo de compra', color:'#E31837' },
  { name:'1688.com', icon:'🇨🇳', url:'https://s.1688.com/selloffer/offerlist.htm?keywords=', aff:false, ship:'20-40 días · Precio fábrica', note:'Precio más bajo, requiere intermediario', color:'#FF4200' },
  { name:'Temu', icon:'🟠', url:'https://www.temu.com/search_result.html?search_key=', aff:false, ship:'7-15 días · Envío rápido', note:'Precios ultra bajos, creciendo en LATAM', color:'#FF6900' },
  { name:'Shein Mayorista', icon:'🛍️', url:'https://www.shein.com/pdsearch/', aff:false, ship:'10-20 días · Moda', note:'Ideal para ropa y accesorios', color:'#000' },
  { name:'Banggood', icon:'📦', url:'https://www.banggood.com/search/', aff:true, ship:'12-25 días · Gadgets', note:'Especializado en tecnología', color:'#E94E24' },
  { name:'CJ Dropshipping', icon:'🚀', url:'https://cjdropshipping.com/search/', aff:true, ship:'7-12 días · Bodega LATAM', note:'Bodega en Brasil y México', color:'#00A87E' },
  { name:'Chinabrands', icon:'🏪', url:'https://www.chinabrands.com/search/', aff:true, ship:'10-20 días', note:'Dropshipping directo', color:'#E5002B' },
  { name:'Global Sources', icon:'🌍', url:'https://www.globalsources.com/gsol/I/search/', aff:false, ship:'20-35 días · B2B', note:'Proveedores verificados de China', color:'#0066CC' },
  { name:'Made-in-China', icon:'🏗️', url:'https://www.made-in-china.com/products-search/', aff:false, ship:'20-40 días', note:'Fabricantes directos', color:'#CC0000' },
  { name:'Dropdeal', icon:'⚡', url:'https://www.dropdeal.com.br/search/', aff:true, ship:'5-10 días · LATAM', note:'Stock en Argentina y Brasil', color:'#7B61FF' },
  { name:'Spocket', icon:'🌎', url:'https://www.spocket.co/products/', aff:true, ship:'5-8 días · Locales', note:'Proveedores locales en LATAM', color:'#6366F1' },
  { name:'Zendrop', icon:'💨', url:'https://app.zendrop.com/products/', aff:true, ship:'3-7 días · Express', note:'El más rápido para envío a LATAM', color:'#00D4FF' },
];

const SUPPLIERS_SELL = [
  { name:'Mercado Libre', icon:'🛒', url:'https://www.mercadolibre.com', note:'El marketplace #1 de LATAM', color:'#FFE600', textColor:'#333' },
  { name:'Tiendanube', icon:'☁️', url:'https://www.tiendanube.com', note:'Tu propia tienda online en minutos', color:'#00B1E1', textColor:'#fff' },
  { name:'Shopify', icon:'🟢', url:'https://www.shopify.com', note:'Plataforma global de e-commerce', color:'#96BF48', textColor:'#fff' },
  { name:'Instagram Shop', icon:'📸', url:'https://www.instagram.com', note:'Venta directa por redes sociales', color:'#E1306C', textColor:'#fff' },
  { name:'Facebook Market', icon:'👥', url:'https://www.facebook.com/marketplace', note:'Marketplace de Facebook, sin comisión', color:'#1877F2', textColor:'#fff' },
  { name:'OLX', icon:'🟡', url:'https://www.olx.com.ar', note:'Clasificados online, muy usado en AR', color:'#F0A500', textColor:'#fff' },
  { name:'Yapo.cl', icon:'🇨🇱', url:'https://www.yapo.cl', note:'Clasificados #1 en Chile', color:'#00A859', textColor:'#fff' },
  { name:'Gallito.uy', icon:'🇺🇾', url:'https://www.gallito.com.uy', note:'Clasificados #1 en Uruguay', color:'#0066CC', textColor:'#fff' },
  { name:'WooCommerce', icon:'🛍️', url:'https://woocommerce.com', note:'Plugin para WordPress, 100% gratis', color:'#7F54B3', textColor:'#fff' },
  { name:'TikTok Shop', icon:'🎵', url:'https://shop.tiktok.com', note:'Vender directamente en TikTok', color:'#010101', textColor:'#fff' },
];

function renderSuppliersTab(p, el){
  if(!el) return;
  var q = encodeURIComponent(p.name||'');

  // Show loading state
  el.innerHTML = '<div style="text-align:center;padding:2rem;color:var(--text2);font-size:.83rem">Buscando precios reales...</div>';

  // Fetch real price from AliExpress
  fetch('/api/aliexpress?q='+q)
    .then(function(r){return r.json();})
    .then(function(data){
      var aeProducts = data.products||[];
      var aePrice = aeProducts[0] ? parseFloat(aeProducts[0].price) : null;
      renderSuppliersContent(p, el, q, aePrice);
    })
    .catch(function(){
      renderSuppliersContent(p, el, q, null);
    });
}

function renderSuppliersContent(p, el, q, aeBasePrice){
  // Use real AliExpress price or fallback to score-based estimate
  var basePrice = aeBasePrice || Math.max(3, Math.round(p.score * 0.08));

  el.innerHTML = `
  <div style="margin-bottom:1.25rem">
    <div style="font-size:.72rem;font-weight:700;letter-spacing:1px;color:var(--text3);text-transform:uppercase;margin-bottom:.75rem;display:flex;align-items:center;gap:.5rem">
      <span style="width:18px;height:18px;background:#EFF6FF;border-radius:4px;display:inline-flex;align-items:center;justify-content:center;font-size:.75rem">📦</span>
      DÓNDE COMPRAR — Proveedores mayoristas
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem">
      ${SUPPLIERS_BUY.map(function(s){
        var link = s.url + q;
        // Price multipliers relative to AliExpress base price
        var mults = {'AliExpress':1.0,'Alibaba':0.75,'DHgate':1.1,'1688.com':0.6,'Temu':0.85,'Shein Mayorista':0.9,'Banggood':1.15,'CJ Dropshipping':1.25,'Chinabrands':1.1,'Global Sources':0.8,'Made-in-China':0.7,'Dropdeal':1.4,'Spocket':1.6,'Zendrop':1.5};
        var mult = mults[s.name]||1.0;
        var estPrice = (basePrice*mult).toFixed(2);
        return '<a href="'+link+'" target="_blank" rel="noopener" style="display:block;padding:.75rem;border:1px solid var(--border);border-radius:10px;text-decoration:none;transition:border-color .15s;background:var(--white)">'+
          '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.3rem">'+
            '<span style="font-size:.85rem;font-weight:700">'+s.icon+' '+s.name+'</span>'+
            (s.aff?'<span style="font-size:.6rem;background:#DCFCE7;color:#15803D;padding:.15rem .4rem;border-radius:3px;font-weight:700">AFIL.</span>':'')+
          '</div>'+
          '<div style="font-size:.7rem;color:var(--text2);margin-bottom:.3rem">'+s.ship+'</div>'+
          '<div style="font-size:.7rem;color:var(--text3)">'+s.note+'</div>'+
          '<div style="font-size:.82rem;font-weight:800;color:var(--green);margin-top:.4rem">~USD '+estPrice+' est.</div>'+
        '</a>';
      }).join('')}
    </div>
  </div>

  <div>
    <div style="font-size:.72rem;font-weight:700;letter-spacing:1px;color:var(--text3);text-transform:uppercase;margin-bottom:.75rem;display:flex;align-items:center;gap:.5rem">
      <span style="width:18px;height:18px;background:#F0FDF4;border-radius:4px;display:inline-flex;align-items:center;justify-content:center;font-size:.75rem">💰</span>
      DÓNDE VENDER — Plataformas de reventa
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem">
      ${SUPPLIERS_SELL.map(function(s){
        return '<a href="'+s.url+'" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:.6rem;padding:.75rem;border:1px solid var(--border);border-radius:10px;text-decoration:none;transition:border-color .15s;background:var(--white)">'+
          '<span style="font-size:1.25rem;flex-shrink:0">'+s.icon+'</span>'+
          '<div>'+
            '<div style="font-size:.82rem;font-weight:700;color:var(--text)">'+s.name+'</div>'+
            '<div style="font-size:.7rem;color:var(--text2)">'+s.note+'</div>'+
          '</div>'+
        '</a>';
      }).join('')}
    </div>
  </div>`;
}

function closeProdModal(e){if(e.target===document.getElementById('prodModal'))closeProdModalDirect();}
function closeProdModalDirect(){document.getElementById('prodModal').classList.add('hidden');}
function saveCurrentProduct(){if(currentProd===null)return;toggleSave(currentProd);document.getElementById('pmSaveBtn').innerHTML=saved.includes(currentProd)?'<i class="ti ti-bookmark-filled"></i> Guardado':'<i class="ti ti-bookmark"></i> Guardar';}
function toggleSave(idx){const i=saved.indexOf(idx);if(i===-1)saved.push(idx);else saved.splice(i,1);localStorage.setItem('tb_saved',JSON.stringify(saved));savedCount();renderProducts(true);renderLandingProducts();}
function savedCount(){const el=document.getElementById('savedCount');if(el)el.textContent=saved.length;}
function renderSaved(){
  const el=document.getElementById('savedContent');if(!el)return;
  if(!saved.length){el.innerHTML='<div class="empty-state"><i class="ti ti-bookmark"></i><p>No tenés productos guardados todavía.</p></div>';return;}
  el.innerHTML='<div class="saved-grid">'+saved.map(idx=>{const p=PRODUCTS[idx];if(!p)return'';return'<div class="saved-card" onclick="openProduct('+idx+')">'+imgEl(p.img,'saved-card-img',p.cat,p.name)+'<div class="saved-card-body"><div class="saved-name">'+p.name+'</div><div class="saved-meta">'+p.cat+' · Margen '+p.marginStr+'</div><div class="saved-score">'+p.score+'</div><button class="btn-remove" onclick="event.stopPropagation();toggleSave('+idx+');renderSaved()">✕ Quitar</button></div></div>';}).join('')+'</div>';
}
function analyzeProduct(){if(currentProd===null)return;const p=PRODUCTS[currentProd];closeProdModalDirect();enterDash();setTimeout(()=>askAI('Analizá el producto "'+p.name+'" con TrendScore '+p.score+', margen '+p.marginStr+' y competencia '+p.comp+'. ¿Por qué está en tendencia y cómo lo venderías en LATAM?'),300);}
function markAllRead(){document.querySelectorAll('.alert-dot').forEach(d=>d.style.background='var(--text3)');}

function openAuth(m='login'){document.getElementById('authModal').classList.remove('hidden');setAuthMode(m);}
function closeAuth(){document.getElementById('authModal').classList.add('hidden');}
function setAuthMode(m){
  authMode=m;
  document.getElementById('tabLogin').classList.toggle('active',m==='login');
  document.getElementById('tabSignup').classList.toggle('active',m==='signup');
  document.getElementById('authTitle').textContent=m==='login'?'Bienvenido de vuelta':'Creá tu cuenta gratis';
  document.getElementById('authSubtitle').textContent=m==='login'?'Ingresá para acceder al dashboard':'Empezá gratis, suscribite cuando quieras';
  document.getElementById('authSubmit').textContent=m==='login'?'Iniciar sesión':'Crear cuenta';
  document.getElementById('authErr').classList.add('hidden');document.getElementById('authOk').classList.add('hidden');
}
async function doAuth(){
  const email=document.getElementById('authEmail').value.trim(),pass=document.getElementById('authPass').value,btn=document.getElementById('authSubmit');
  document.getElementById('authErr').classList.add('hidden');document.getElementById('authOk').classList.add('hidden');
  if(!email||!pass){document.getElementById('authErr').textContent='Completá email y contraseña';document.getElementById('authErr').classList.remove('hidden');return;}
  if(pass.length<6){document.getElementById('authErr').textContent='Contraseña mínimo 6 caracteres';document.getElementById('authErr').classList.remove('hidden');return;}
  btn.disabled=true;btn.textContent='Procesando...';
  try{
    const res=await fetch('/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:authMode,email,password:pass})});
    const data=await res.json();
    if(!res.ok)throw new Error(data.error||'Error de autenticación');
    if(authMode==='signup'){document.getElementById('authOk').textContent='\u2705 \u00a1Cuenta creada! Ya podés iniciar sesión.';document.getElementById('authOk').classList.remove('hidden');setTimeout(()=>setAuthMode('login'),2000);}
    else{user={email};plan='free';localStorage.setItem('tb_session',JSON.stringify({email,access_token:data.access_token||''}));localStorage.setItem('tb_plan','free');closeAuth();updateNav();enterDash();}
  }catch(e){document.getElementById('authErr').textContent=e.message;document.getElementById('authErr').classList.remove('hidden');}
  btn.disabled=false;btn.textContent=authMode==='login'?'Iniciar sesión':'Crear cuenta';
}
async function loginGoogle(){try{const res=await fetch('/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'google'})});const data=await res.json();if(data.url)location.href=data.url;}catch(e){document.getElementById('authErr').textContent='Error al conectar con Google';document.getElementById('authErr').classList.remove('hidden');}}
function logout(){user=null;plan='free';localStorage.removeItem('tb_session');localStorage.removeItem('tb_plan');closeDD();updateNav();goLanding();}
function toggleDD(){document.getElementById('userDD').classList.toggle('hidden');}
function closeDD(){const dd=document.getElementById('userDD');if(dd)dd.classList.add('hidden');}
function scrollToPlans(){closeDD();goLanding();setTimeout(()=>document.getElementById('pricing').scrollIntoView({behavior:'smooth'}),100);}
function scrollToAbout(){closeDD();goLanding();setTimeout(()=>{var el=document.getElementById('about-section');if(el)el.scrollIntoView({behavior:'smooth'});},100);}

async function subscribe(planName){
  if(!user){openAuth('signup');return;}
  document.querySelectorAll('.gate-plan-btn,.plan-btn').forEach(b=>b.disabled=true);
  try{
    const res=await fetch('/api/subscribe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({plan:planName,email:user.email})});
    const data=await res.json();
    if(data.url)location.href=data.url;else throw new Error(data.error||'Error al crear el checkout');
  }catch(e){alert('Error: '+e.message);document.querySelectorAll('.gate-plan-btn,.plan-btn').forEach(b=>b.disabled=false);}
}

const AI_SYS='Sos el asistente IA de TrendBase, plataforma de tendencias para dropshippers de Argentina, Uruguay y Chile. Ayudás con: productos virales, márgenes estimados, proveedores, estrategias de venta. Respondé en español, conciso y útil. Máximo 3 párrafos.';
async function askAI(msg){
  if(aiLoading)return;
  // Check message limit
  var plan = currentPlan();
  var maxMsg = plan.aiMessages || 0;
  if(maxMsg === 0) { showUpgradeToast('El asistente IA requiere plan Starter o superior.'); return; }
  var todayKey = 'tb_ai_msgs_'+new Date().toISOString().slice(0,10);
  var todayCount = parseInt(localStorage.getItem(todayKey)||'0');
  if(todayCount >= maxMsg) { showUpgradeToast('Alcanzaste el límite de '+maxMsg+' mensajes de IA por día. Upgrades al plan Pro para 15 mensajes/día.'); return; }
  localStorage.setItem(todayKey, todayCount+1);
  const input=document.getElementById('aiInput'),btn=document.getElementById('aiSend'),msgs=document.getElementById('aiMessages');
  const text=msg||input.value.trim();if(!text)return;
  if(input)input.value='';aiLoading=true;if(btn)btn.disabled=true;
  msgs.innerHTML+='<div class="msg msg-user">'+text+'</div>';
  msgs.innerHTML+='<div class="typing" id="typing"><span></span><span></span><span></span></div>';
  msgs.scrollTop=msgs.scrollHeight;aiHistory.push({role:'user',content:text});
  try{
    const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:aiHistory,system:AI_SYS})});
    let data;try{data=await res.json();}catch(je){throw new Error('Error del servidor ('+res.status+')');}
    if(!res.ok)throw new Error(data.error||'Error: '+res.status);
    const reply=data.text||'Sin respuesta.';aiHistory.push({role:'assistant',content:reply});
    document.getElementById('typing').outerHTML='<div class="msg msg-ai">'+reply.replace(/\n/g,'<br>')+'</div>';
  }catch(e){aiHistory.pop();document.getElementById('typing').outerHTML='<div class="msg msg-ai" style="color:var(--red)">\u26A0\uFE0F '+e.message+'</div>';}
  aiLoading=false;if(btn)btn.disabled=false;msgs.scrollTop=msgs.scrollHeight;
}

// Spinner CSS
const style=document.createElement('style');
style.textContent='@keyframes spin{to{transform:rotate(360deg)}}';
document.head.appendChild(style);

init();
