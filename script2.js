    // System Configurations & Data fallbacks
    const PLANS = {
      free:    { maxProducts: 20,    ai: false, advFilters: false, history: 7,  analysis: false, comparator: false, aiMessages: 0  },
      starter: { maxProducts: 150,   ai: true,  advFilters: true,  history: 90, analysis: true,  comparator: false, aiMessages: 10 },
      pro:     { maxProducts: 99999, ai: true,  advFilters: true,  history: 90, analysis: true,  comparator: true,  aiMessages: 15 },
    };
    function currentPlan(){ return PLANS[plan] || PLANS.free; }

    // ── IMÁGENES DE PRODUCTOS (Unsplash Source — gratis, sin API key) ────────
    // Usa keywords del producto generadas por IA; fallback por categoría
    const CAT_IMG_KW = {
      'Tecnología': 'technology gadget device',
      'Belleza':    'beauty cosmetics skincare',
      'Hogar':      'home decor interior',
      'Moda':       'fashion clothing accessories',
      'Deportes':   'fitness sport exercise',
    };
    function productImg(p, size='600x400') {
      const kw = (p.imgKw || CAT_IMG_KW[p.cat] || 'product').trim().replace(/\s+/g, ',');
      return `https://source.unsplash.com/featured/${size}/?${encodeURIComponent(kw)}`;
    }

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

    const PRICES={
      AR:{starter:'$9.999/mes',pro:'$19.999/mes',period:'ARS'},
      UY:{starter:'$390/mes',pro:'$790/mes',period:'UYU'},
      CL:{starter:'$4.990/mes',pro:'$9.990/mes',period:'CLP'}
    };

    const WEEKS=['Sem 1','Sem 2','Sem 3','Sem 4','Sem 5','Sem 6','Sem 7','Sem 8','Sem 9','Sem 10','Sem 11','Sem 12','Sem 13','Sem 14','Sem 15','Hoy'];
    const LEADERS=['🇦🇷 Argentina','🇺🇾 Uruguay','🇨🇱 Chile','🇦🇷 Argentina','🇨🇱 Chile','🇺🇾 Uruguay','🇦🇷 Argentina','🇨🇱 Chile'];

    let PRODUCTS = [];
    let ALL_PRODUCTS = [];
    let productsLoaded = false;
    let user=null,plan='free',currentProd=null,authMode='login',aiHistory=[],aiLoading=false;
    let saved=JSON.parse(localStorage.getItem('tb_saved')||'[]');
    let filter={plt:'',region:'',cat:'',minMargin:0,comp:'',minPrice:0};
    let histChart=null,analysisChart=null,currentPage=1;
    const PAGE_SIZE=20;
    let loadRetries = 0;
    let aiSummaryLoaded = false;

    // Load Session & Profile state
    function init(){
      console.log("TrendBase v2.1 loaded");
      if(typeof initGSAPAnimations !== 'undefined') initGSAPAnimations();
      const sess = localStorage.getItem('tb_session');
      if(sess) {
        try {
          const s = JSON.parse(sess);
          user = { email: s.email };
          plan = localStorage.getItem('tb_plan') || 'free';
        } catch(e){}
      }
      
      // Load products
      loadProducts();
      renderPublicLeaderboard();
      updateNav();
      savedCount();
      
      // Initialize telemetry typewriter
      setTimeout(() => {
        typeNextMessage();
      }, 500);
    }

    // Floating Island Navbar Scrolling Effect
    window.addEventListener('scroll', () => {
      const navContainer = document.getElementById('nav-container');
      if (window.scrollY > 50) {
        navContainer.classList.remove('bg-transparent');
        navContainer.classList.add('bg-obsidian/85', 'backdrop-blur-xl', 'py-3');
      } else {
        navContainer.classList.remove('bg-obsidian/85', 'backdrop-blur-xl', 'py-3');
        navContainer.classList.add('bg-transparent');
      }
    });

    // Stacking sticky cards for Protocol using ScrollTrigger
    const protocolCards = gsap.utils.toArray('.protocol-card');
    protocolCards.forEach((card, index) => {
      if (index < protocolCards.length - 1) {
        gsap.to(card, {
          scale: 0.9,
          filter: 'blur(10px)',
          opacity: 0.5,
          scrollTrigger: {
            trigger: card,
            start: 'top top',
            end: 'bottom top',
            scrub: true,
            pin: true,
            pinSpacing: false
          }
        });
      }
    });

    // Navigation toggles: Landing ⇆ Dashboard
    function goLanding() {
      document.getElementById('view-landing').classList.add('active-view');
      document.getElementById('view-dash').classList.remove('active-view');
      
      document.getElementById('landing-nav').classList.remove('hidden');
      document.getElementById('landing-nav').classList.add('flex');
      document.getElementById('dash-nav').classList.add('hidden');
      document.getElementById('dash-nav').classList.remove('flex');

      document.getElementById('main-header').classList.remove('top-0', 'w-full', 'max-w-none', 'rounded-none');
      document.getElementById('main-header').classList.add('top-6', 'navbar-pill');
      document.getElementById('nav-container').classList.remove('rounded-none');
      document.getElementById('nav-container').classList.add('rounded-full');
    }

    function enterDash() {
      document.getElementById('view-landing').classList.remove('active-view');
      document.getElementById('view-dash').classList.add('active-view');
      
      document.getElementById('landing-nav').classList.add('hidden');
      document.getElementById('landing-nav').classList.remove('flex');
      document.getElementById('dash-nav').classList.remove('hidden');
      document.getElementById('dash-nav').classList.add('flex');

      document.getElementById('main-header').classList.add('top-0', 'w-full', 'max-w-none', 'rounded-none');
      document.getElementById('main-header').classList.remove('top-6', 'navbar-pill');
      document.getElementById('nav-container').classList.add('rounded-none');
      document.getElementById('nav-container').classList.remove('rounded-full');

      // Go to tendencies by default
      goSection('tendencias');
    }

    // Dashboard sections navigation
    function goSection(sec) {
      document.querySelectorAll('.dash-section').forEach(s => s.classList.remove('active-section'));
      const activeSec = document.getElementById(`sec-${sec}`);
      if(activeSec) activeSec.classList.add('active-section');

      // Sidebar links active highlight
      document.querySelectorAll('aside button').forEach(b => b.classList.remove('active-sidebar-item'));
      const activeBtn = document.getElementById(`sb-${sec}`);
      if(activeBtn) activeBtn.classList.add('active-sidebar-item');

      // Sync views
      if(sec === 'guardados') renderSaved();
      if(sec === 'perfil') renderPerfil();
      if(sec === 'negocio') renderNegocio();
      if(sec === 'analisis') renderAnalysis();
    }

    function updateMobileNav(sec) {
      document.querySelectorAll('#mobileNav button').forEach(b => {
        b.classList.remove('text-champagne');
        b.classList.add('text-white/60');
      });
      const activeMobileBtn = document.getElementById(`mbn-${sec}`);
      if(activeMobileBtn) {
        activeMobileBtn.classList.add('text-champagne');
        activeMobileBtn.classList.remove('text-white/60');
      }
    }

    function updateNav() {
      const authBtns = document.getElementById('navAuthBtns');
      const userBadge = document.getElementById('navUser');
      const currencyBadge = document.getElementById('currencyBadge');

      if(user) {
        authBtns.classList.add('hidden');
        userBadge.classList.remove('hidden');
        currencyBadge.classList.remove('hidden');
        document.getElementById('userEmailLabel').textContent = user.email;
        document.getElementById('userPlanLabel').textContent = plan.toUpperCase();
        document.getElementById('userAvatar').textContent = user.email[0].toUpperCase();
      } else {
        authBtns.classList.remove('hidden');
        userBadge.classList.add('hidden');
        currencyBadge.classList.add('hidden');
      }
    }

    // ── PRODUCTS FETCH & SETUP ───────────────────────────────────────────────
    async function loadProducts() {
      const loadingEl = document.getElementById('productsLoading');
      const kpiEl = document.getElementById('kpiProductos');
      try {
        const res = await fetch('/api/products');
        const text = await res.text();
        let data;
        try { data = JSON.parse(text); } catch(e) { throw new Error('Respuesta inválida del servidor'); }
        if(!res.ok) throw new Error(data.error || 'Error ' + res.status);

        if(!data.products || !data.products.length || data.stale || data.generating) {
          triggerGeneration(0);
          if(data.products && data.products.length) {
            setProducts(data.products, data);
          }
          return;
        }
        setProducts(data.products, data);
      } catch(e) {
        console.error('Error cargando productos:', e.message);
        if(loadRetries < 3) { loadRetries++; setTimeout(loadProducts, 4000); }
      }
    }

    function setProducts(products, data) {
      const loadingEl = document.getElementById('productsLoading');
      const kpiEl = document.getElementById('kpiProductos');
      
      const mapped = products.map(p => ({
        name: p.name, cat: p.cat, score: p.score, change: p.change,
        changeNum: p.change_num !== undefined ? p.change_num : p.changeNum,
        plts: p.plts || [], margin: p.margin,
        marginStr: p.margin_str || p.marginStr,
        hot: p.hot, regions: p.regions || [],
        comp: p.comp, priceMin: p.price_min || p.priceMin,
        priceStr: p.price_str || p.priceStr,
        history: p.history || [], rank: p.rank || 0,
        imgKw: p.img_kw || p.imgKw || '',
        suppliers: p.suppliers || [],
      }));

      ALL_PRODUCTS = mapped;
      PRODUCTS = mapped;
      productsLoaded = true;
      if(loadingEl) loadingEl.style.display='none';
      if(kpiEl) kpiEl.textContent = (data && data.count ? data.count : PRODUCTS.length) + '+';
      
      updateNav();
      renderLandingProducts();
      renderProducts(true);
      populateAnalysisSelect();
      populateComparators();
      
      const freshEl = document.getElementById('freshness');
      if(freshEl && data) {
        const mins = Math.floor((data.age||0)/60);
        freshEl.textContent = data.stale ? '⟳ Actualizando...' : (mins < 2 ? '✓ Recién actualizado' : 'Hace ' + mins + ' min');
      }
    }

    async function triggerGeneration(batchIndex) {
      try {
        const res = await fetch('/api/generate?secret=trendbase2025&batch=' + batchIndex);
        const data = await res.json();
        if(data.nextBatch !== null && data.nextBatch !== undefined) {
          setTimeout(() => triggerGeneration(data.nextBatch), 1000);
        } else if(data.done) {
          setTimeout(() => loadProducts(), 1000);
        }
      } catch(e) {}
    }

    // ── RENDER PRODUCTS ──────────────────────────────────────────────────────
    function renderLandingProducts() {
      const container = document.getElementById('landingProducts');
      if(!container) return;
      
      const list = (PRODUCTS || []).slice(0, 8);
      container.innerHTML = list.map((p, i) => {
        const image = p.img || productImg(p);
        return `
          <div onclick="openProduct(${i})" class="bg-white/5 border border-white/10 rounded-[2rem] overflow-hidden hover-lift shadow-sm cursor-pointer p-4 space-y-4">
            <div class="aspect-video w-full rounded-2xl overflow-hidden bg-black/20 relative">
              <img src="${image}" class="w-full h-full object-cover" loading="lazy" decoding="async">
              <span class="absolute top-3 left-3 text-[9px] font-mono font-bold uppercase bg-champagne text-obsidian px-2 py-0.5 rounded">${p.cat}</span>
            </div>
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-mono text-champagne font-bold">Score: ${p.score}</span>
                <span class="text-[10px] font-mono text-green-400 font-bold">${p.change}</span>
              </div>
              <h4 class="text-sm font-bold text-white truncate">${p.name}</h4>
              <div class="flex justify-between items-center text-[10px] text-white/50 border-t border-white/5 pt-2">
                <span>Margen: <b class="text-green-400 font-mono">${p.marginStr}</b></span>
                <span>Comp: <b class="text-white font-mono">${p.comp}</b></span>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderProducts(resetPage=false) {
      const tbody = document.getElementById('productsTbody');
      if(!tbody) return;
      if(resetPage) currentPage = 1;

      // Filter products
      let allFiltered = ALL_PRODUCTS.filter(p => {
        if(filter.plt && !p.plts.includes(filter.plt)) return false;
        if(filter.region && !p.regions.includes(filter.region)) return false;
        if(filter.cat && p.cat !== filter.cat) return false;
        if(filter.comp && p.comp !== filter.comp) return false;
        return true;
      });

      const maxP = currentPlan().maxProducts;
      allFiltered = allFiltered.slice(0, maxP);

      const countLabel = document.getElementById('tableProductCount');
      if(countLabel) countLabel.textContent = `${allFiltered.length} productos`;

      const start = (currentPage - 1) * PAGE_SIZE;
      const list = allFiltered.slice(start, start + PAGE_SIZE);

      tbody.innerHTML = list.map((p, i) => {
        const idx = ALL_PRODUCTS.indexOf(p);
        const compClass = p.comp === 'Baja' ? 'text-green-400 bg-green-500/10 border-green-500/20' : p.comp === 'Alta' ? 'text-red-400 bg-red-500/10 border-red-500/20' : 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
        return `
          <tr onclick="openProduct(${idx})" class="hover:bg-white/5 transition cursor-pointer text-xs">
            <td class="p-4 text-center font-mono text-white/40">${start + i + 1}</td>
            <td class="p-4 font-bold text-white">${p.name}</td>
            <td class="p-4 font-mono text-champagne">${p.score}</td>
            <td class="p-4 font-mono text-green-400">${p.change}</td>
            <td class="p-4 font-mono text-green-400">${p.marginStr}</td>
            <td class="p-4">
              <span class="px-2 py-0.5 rounded border text-[9px] font-bold ${compClass}">${p.comp}</span>
            </td>
            <td class="p-4 font-mono text-white/70">${p.priceStr}</td>
            <td class="p-4 font-mono text-white/40">${p.suppliers && p.suppliers[0] ? p.suppliers[0].price : '—'}</td>
            <td class="p-4 text-right">
              <button onclick="event.stopPropagation(); toggleSave(${idx})" class="text-white/40 hover:text-champagne transition"><i data-lucide="bookmark" class="w-4 h-4"></i></button>
            </td>
          </tr>
        `;
      }).join('');

      renderPagination(Math.ceil(allFiltered.length / PAGE_SIZE), allFiltered.length);
      lucide.createIcons();
    }

    function renderPagination(totalPages, total) {
      const el = document.getElementById('pagination');
      if(!el) return;
      if(totalPages <= 1) { el.innerHTML = ''; return; }
      
      let html = '';
      html += `<button class="px-3 py-1.5 rounded-lg border border-white/10 hover:bg-white/5 text-white/60 transition" ${currentPage === 1 ? 'disabled style="opacity:0.4"' : ''} onclick="goPage(${currentPage - 1})">‹</button>`;
      for(let i = 1; i <= totalPages; i++) {
        html += `<button class="px-3 py-1.5 rounded-lg border border-white/10 transition ${i === currentPage ? 'bg-champagne text-obsidian font-bold' : 'hover:bg-white/5 text-white/80'}" onclick="goPage(${i})">${i}</button>`;
      }
      html += `<button class="px-3 py-1.5 rounded-lg border border-white/10 hover:bg-white/5 text-white/60 transition" ${currentPage === totalPages ? 'disabled style="opacity:0.4"' : ''} onclick="goPage(${currentPage + 1})">›</button>`;
      el.innerHTML = html;
    }

    function goPage(p) {
      currentPage = p;
      renderProducts();
    }

    // ── FILTERS & CATEGORIES ─────────────────────────────────────────────────
    function filterCat(cat) {
      filter.cat = cat;
      filter.plt = ''; // reset platform when category changes
      // update highlights in sidebar
      document.querySelectorAll('aside button').forEach(b => {
        if(b.id && b.id.startsWith('sb-cat')) b.classList.remove('text-champagne', 'bg-white/5');
        if(b.id && b.id.startsWith('sb-plt')) b.classList.remove('text-champagne', 'bg-white/5');
      });
      const btnId = cat === '' ? 'sb-cat-all' : `sb-cat-${cat.toLowerCase()}`;
      const activeBtn = document.getElementById(btnId);
      if(activeBtn) activeBtn.classList.add('text-champagne', 'bg-white/5');
      renderProducts(true);
    }

    function filterPlt(plt) {
      filter.plt = plt;
      filter.cat = ''; // reset category when platform changes
      document.querySelectorAll('aside button').forEach(b => {
        if(b.id && b.id.startsWith('sb-cat')) b.classList.remove('text-champagne', 'bg-white/5');
        if(b.id && b.id.startsWith('sb-plt')) b.classList.remove('text-champagne', 'bg-white/5');
      });
      const activeBtn = document.getElementById(`sb-plt-${plt.toLowerCase()}`);
      if(activeBtn) activeBtn.classList.add('text-champagne', 'bg-white/5');
      
      document.querySelectorAll('.dash-section').forEach(el=>el.classList.remove('active-section'));
      document.getElementById('sec-tendencias').classList.add('active-section');
      
      renderProducts(true);
    }

    function filterRegion(reg) {
      filter.region = reg;
      renderProducts(true);
    }

    function filterSort(sortVal) {
      if(sortVal === 'score') {
        PRODUCTS.sort((a,b) => b.score - a.score);
      } else if(sortVal === 'change') {
        PRODUCTS.sort((a,b) => b.changeNum - a.changeNum);
      } else if(sortVal === 'margin') {
        PRODUCTS.sort((a,b) => b.margin - a.margin);
      }
      renderProducts(true);
    }

    // ── ANALYSIS ENGINE ──────────────────────────────────────────────────────
    function renderAnalysis() {
      var prods = PRODUCTS || ALL_PRODUCTS || [];
      if(!prods.length) return;
      
      renderAnalysisKPIs();
      renderOpportunities();
      renderRegionHeatmap();
      renderTopMargin();
      
      setTimeout(() => {
        renderAnalysisCatChart();
        renderAnalysisChart();
      }, 100);
    }

    function renderAnalysisKPIs() {
      const el = document.getElementById('analysisKpis');
      if(!el) return;
      
      const prods = PRODUCTS;
      const avgMargin = Math.round(prods.reduce((a,p) => a + p.margin, 0) / prods.length) || 0;
      const cats = {}; prods.forEach(p => { cats[p.cat] = (cats[p.cat] || 0) + 1; });
      const topCat = Object.entries(cats).sort((a,b) => b[1] - a[1])[0];
      const lowComp = prods.filter(p => p.comp === 'Baja').length;
      
      el.innerHTML = `
        <div class="bg-white/5 border border-white/10 rounded-2xl p-5">
          <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Productos Analizados</div>
          <div class="text-3xl font-extrabold text-white mt-1">${prods.length}</div>
          <div class="text-[9px] text-green-400 font-mono mt-1">${prods.filter(p=>p.hot).length} HOT ahora</div>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-2xl p-5">
          <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Categoría Líder</div>
          <div class="text-lg font-bold text-champagne truncate mt-1">${topCat ? topCat[0] : 'Ninguna'}</div>
          <div class="text-[9px] text-white/40 font-mono mt-1">${topCat ? Math.round(topCat[1]/prods.length*100) : 0}% del total</div>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-2xl p-5">
          <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Margen Promedio</div>
          <div class="text-3xl font-extrabold text-green-400 mt-1">${avgMargin}%</div>
          <div class="text-[9px] text-green-400 font-mono mt-1">Sólido vs mes anterior</div>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-2xl p-5">
          <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Baja Competencia</div>
          <div class="text-3xl font-extrabold text-white mt-1">${lowComp}</div>
          <div class="text-[9px] text-champagne font-mono mt-1">Score top: ${prods[0] ? prods[0].score : 0}</div>
        </div>
      `;
    }

    function opportunityScore(p) {
      const compScore = p.comp === 'Baja' ? 3 : p.comp === 'Media' ? 2 : 1;
      return Math.round((p.score * p.margin * compScore) / 100);
    }

    function renderOpportunities() {
      const el = document.getElementById('opportunityList');
      if(!el) return;
      const sorted = [...PRODUCTS].sort((a,b) => opportunityScore(b) - opportunityScore(a)).slice(0, 5);
      
      el.innerHTML = sorted.map(p => `
        <div class="py-3 flex justify-between items-center text-xs">
          <div>
            <div class="font-bold text-white">${p.name}</div>
            <div class="text-[10px] text-white/50">${p.cat} · comp: ${p.comp}</div>
          </div>
          <div class="text-right">
            <div class="font-bold text-green-400 font-mono">${p.marginStr}</div>
            <div class="text-[9px] text-white/40 font-mono">Score: ${p.score}</div>
          </div>
        </div>
      `).join('');
    }

    function renderRegionHeatmap() {
      const el = document.getElementById('regionHeatmap');
      if(!el) return;
      
      const regions = {
        AR: { count:0, name:'Argentina', flag:'🇦🇷', color:'text-blue-400', bg:'bg-blue-400/5', border:'border-blue-400/20' },
        UY: { count:0, name:'Uruguay', flag:'🇺🇾', color:'text-green-400', bg:'bg-green-400/5', border:'border-green-500/20' },
        CL: { count:0, name:'Chile', flag:'🇨🇱', color:'text-yellow-400', bg:'bg-yellow-400/5', border:'border-yellow-400/20' }
      };

      PRODUCTS.forEach(p => {
        (p.regions || []).forEach(r => {
          if(regions[r]) regions[r].count++;
        });
      });
      const total = PRODUCTS.length || 1;

      el.innerHTML = Object.entries(regions).map(([k, r]) => {
        const pct = Math.round(r.count / total * 100);
        return `
          <div class="p-4 border rounded-2xl ${r.border} ${r.bg} text-left">
            <div class="flex items-center justify-between mb-2">
              <span class="text-lg">${r.flag}</span>
              <span class="text-sm font-extrabold ${r.color}">${pct}%</span>
            </div>
            <div class="text-[10px] font-bold text-white">${r.name}</div>
            <div class="text-[8px] text-white/40 uppercase font-mono mt-0.5">${r.count} productos</div>
          </div>
        `;
      }).join('');
    }

    function renderTopMargin() {
      const el = document.getElementById('topMarginList');
      if(!el) return;
      const sorted = [...PRODUCTS].sort((a,b) => b.margin - a.margin).slice(0, 5);
      
      el.innerHTML = sorted.map((p, i) => `
        <div class="py-3 flex justify-between items-center text-xs">
          <span class="font-mono text-white/40">#0${i+1}</span>
          <div class="flex-1 px-3 truncate">
            <div class="font-bold text-white truncate">${p.name}</div>
            <div class="text-[10px] text-white/50">${p.cat}</div>
          </div>
          <span class="font-bold text-green-400 font-mono">${p.marginStr}</span>
        </div>
      `).join('');
    }

    function renderAnalysisCatChart() {
      const el = document.getElementById('analysisCatChart');
      if(!el) return;
      
      const cats = {};
      PRODUCTS.forEach(p => { if(p.cat) cats[p.cat] = (cats[p.cat] || 0) + 1; });
      const total = PRODUCTS.length || 1;
      const sorted = Object.entries(cats).sort((a,b) => b[1] - a[1]);
      
      el.innerHTML = sorted.map(([name, count]) => {
        const pct = Math.round(count / total * 100);
        return `
          <div class="space-y-1 text-xs">
            <div class="flex justify-between font-medium">
              <span class="text-white/70">${name}</span>
              <span class="text-champagne font-mono font-bold">${pct}%</span>
            </div>
            <div class="h-2 bg-white/5 rounded-full overflow-hidden">
              <div class="h-full bg-champagne rounded-full" style="width: ${pct}%"></div>
            </div>
          </div>
        `;
      }).join('');
    }

    function populateAnalysisSelect() {
      const sel = document.getElementById('analysisProductSel');
      if(!sel) return;
      sel.innerHTML = '<option value="">— Seleccioná un producto —</option>' + PRODUCTS.slice(0, 100).map((p, i) => `<option value="${i}">${p.name}</option>`).join('');
    }

    function renderAnalysisHistory() {
      const sel = document.getElementById('analysisProductSel');
      if(!sel || sel.value === '') return;
      
      const idx = parseInt(sel.value);
      const p = PRODUCTS[idx];
      if(!p) return;

      const tbody = document.getElementById('analysisTbody');
      if(!tbody) return;

      tbody.innerHTML = (p.history || []).map((score, i) => {
        const prev = p.history[i-1] || score;
        const diff = score - prev;
        const changeClass = diff >= 0 ? 'text-green-400' : 'text-red-400';
        return `
          <tr class="text-xs">
            <td class="p-3 font-mono text-white/50">${WEEKS[i]}</td>
            <td class="p-3 font-bold text-white font-mono">${score}</td>
            <td class="p-3 font-mono font-bold ${changeClass}">${diff >= 0 ? '+' : ''}${diff}</td>
            <td class="p-3 text-white/70">${LEADERS[i % LEADERS.length]}</td>
          </tr>
        `;
      }).join('');
    }

    function calcROI() {
      const cost = parseFloat(document.getElementById('calcCost').value) || 0;
      const price = parseFloat(document.getElementById('calcPrice').value) || 0;
      const ads = parseFloat(document.getElementById('calcAds').value) || 0;
      const sales = parseInt(document.getElementById('calcSales').value) || 0;
      const el = document.getElementById('calcResult');
      if(!el) return;
      if(!cost || !price) { el.innerHTML = '<p class="text-xs text-white/40">Completa los campos.</p>'; return; }
      
      const netPerSale = price - cost - ads;
      const monthlyProfit = netPerSale * sales;
      const margin = Math.round((netPerSale / price) * 100);
      const roi = cost > 0 ? Math.round((netPerSale / cost) * 100) : 0;
      const breakeven = netPerSale > 0 ? Math.ceil(cost / netPerSale) : 0;
      
      el.innerHTML = `
        <div class="grid grid-cols-2 gap-2 mt-4 text-xs font-mono">
          <div class="bg-white/5 rounded-xl p-3 text-center">
            <div class="text-[9px] text-white/40 uppercase">Ganancia/venta</div>
            <div class="font-bold mt-1 text-green-400">$${netPerSale.toFixed(2)}</div>
          </div>
          <div class="bg-white/5 rounded-xl p-3 text-center">
            <div class="text-[9px] text-white/40 uppercase">Margen neto</div>
            <div class="font-bold mt-1 text-white">${margin}%</div>
          </div>
          <div class="bg-white/5 rounded-xl p-3 text-center">
            <div class="text-[9px] text-white/40 uppercase">ROI</div>
            <div class="font-bold mt-1 text-white">${roi}%</div>
          </div>
          <div class="bg-white/5 rounded-xl p-3 text-center">
            <div class="text-[9px] text-white/40 uppercase">Ganancia/mes</div>
            <div class="font-bold mt-1 text-green-400">$${monthlyProfit.toFixed(0)}</div>
          </div>
          <div class="col-span-2 bg-green-500/10 border border-green-500/20 rounded-xl p-3 text-center">
            <div class="text-[9px] text-white/40 uppercase">Break-even</div>
            <div class="font-bold mt-1 text-green-400">${breakeven} ventas</div>
          </div>
        </div>
      `;
    }

    function populateComparators() {
      var options = '<option value="">Selecciona</option>' + PRODUCTS.slice(0, 100).map(function(p, i){return `<option value="${i}">${p.name}</option>`;}).join('');
      // Standard loader configs
    }

    // ── PUBLIC LEADERBOARD ───────────────────────────────────────────────────
    async function renderPublicLeaderboard() {
      const el = document.getElementById('publicLeaderboard');
      if(!el) return;
      try {
        const res = await fetch('/api/leaderboard');
        const data = await res.json();
        const tops = data.top_products || [];
        const total = data.total_sales || 0;

        const cSales = document.getElementById('cStatSales');
        const cUsers = document.getElementById('cStatUsers');
        const cTop = document.getElementById('cStatTop');
        if(cSales) cSales.textContent = total;
        if(cUsers) cUsers.textContent = tops.length;
        if(cTop && tops[0]) cTop.textContent = tops[0].name.split(' ').slice(0, 3).join(' ') + '...';

        if(!tops.length) {
          el.innerHTML = '<div class="col-span-3 text-center py-6 text-white/40 text-xs font-mono">Sé el primero en registrar una venta 🚀</div>';
          return;
        }

        const medals = ['🥇', '🥈', '🥉'];
        el.innerHTML = tops.slice(0, 6).map((p, i) => {
          const barPct = Math.round(p.count / tops[0].count * 100);
          return `
            <div class="bg-white/5 border border-white/10 rounded-2xl p-5 space-y-3">
              <div class="flex items-center gap-3">
                <span class="text-xl">${medals[i] || '#' + (i + 1)}</span>
                <div class="flex-1 min-w-0">
                  <div class="font-bold text-sm text-white truncate">${p.name}</div>
                  <div class="text-[10px] text-white/40">${p.count} ventas</div>
                </div>
              </div>
              <div class="h-1 bg-white/5 rounded-full overflow-hidden">
                <div class="h-full bg-champagne" style="width: ${barPct}%"></div>
              </div>
            </div>
          `;
        }).join('');
      } catch(e) {
        if(el) el.innerHTML = '<div class="col-span-3 text-center py-6 text-white/40 text-xs font-mono">Registrá ventas para activar el Leaderboard 🚀</div>';
      }
    }

    // ── PERFIL ───────────────────────────────────────────────────────────────
    function getProfile() {
      try { return JSON.parse(localStorage.getItem('tb_profile')||'{}'); } catch(e){ return {}; }
    }
    function saveProfile(data) {
      try { localStorage.setItem('tb_profile', JSON.stringify(data)); } catch(e){}
      fetch('/api/track', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ type:'profile', user_id: getUserId(), ...data })
      }).catch(()=>{});
    }

    function renderPerfil() {
      const el = document.getElementById('perfilContent');
      if(!el) return;
      const p = getProfile();
      el.innerHTML = `
        <div class="max-w-xl bg-white/5 border border-white/10 rounded-[2.5rem] p-8 space-y-6">
          <div class="flex items-center gap-4 border-b border-white/5 pb-6">
            <div class="w-16 h-16 rounded-full bg-champagne text-obsidian flex items-center justify-center text-2xl font-extrabold" id="avatarCircle">
              ${(p.name||'?')[0].toUpperCase()}
            </div>
            <div>
              <div class="text-lg font-bold text-white">${p.name || 'Tu Nombre'}</div>
              <div class="text-xs text-white/40 mt-1">${p.country || 'País no definido'} · Plan ${plan.toUpperCase()}</div>
            </div>
          </div>

          <div class="space-y-4 text-xs font-mono">
            <div>
              <label class="text-[9px] text-white/40 uppercase tracking-wider block mb-1">Nombre o Apodo</label>
              <input id="pfName" value="${p.name || ''}" placeholder="Ej: Ignacio" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
            </div>

            <div>
              <label class="text-[9px] text-white/40 uppercase tracking-wider block mb-1">País</label>
              <select id="pfCountry" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
                <option value="">Selecciona tu país</option>
                <option value="Argentina" ${p.country==='Argentina'?'selected':''}>🇦🇷 Argentina</option>
                <option value="Uruguay" ${p.country==='Uruguay'?'selected':''}>🇺🇾 Uruguay</option>
                <option value="Chile" ${p.country==='Chile'?'selected':''}>🇨🇱 Chile</option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-[9px] text-white/40 uppercase tracking-wider block mb-1">Moneda de venta</label>
                <select id="pfSellCurrency" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
                  <option value="ARS" ${(p.sellCurrency||'ARS')==='ARS'?'selected':''}>ARS</option>
                  <option value="UYU" ${p.sellCurrency==='UYU'?'selected':''}>UYU</option>
                  <option value="CLP" ${p.sellCurrency==='CLP'?'selected':''}>CLP</option>
                </select>
              </div>
              <div>
                <label class="text-[9px] text-white/40 uppercase tracking-wider block mb-1">Moneda de compra</label>
                <select id="pfBuyCurrency" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
                  <option value="USD" ${(p.buyCurrency||'USD')==='USD'?'selected':''}>USD</option>
                  <option value="ARS" ${p.buyCurrency==='ARS'?'selected':''}>ARS</option>
                  <option value="UYU" ${p.buyCurrency==='UYU'?'selected':''}>UYU</option>
                  <option value="CLP" ${p.buyCurrency==='CLP'?'selected':''}>CLP</option>
                </select>
              </div>
            </div>

            <div>
              <label class="text-[9px] text-white/40 uppercase tracking-wider block mb-1">Meta mensual de ventas</label>
              <input id="pfGoal" type="number" value="${p.goal || 10}" class="w-24 bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
            </div>

            <button onclick="savePerfil()" class="btn-magnetic w-full py-3.5 bg-champagne text-obsidian font-extrabold uppercase tracking-wider rounded-xl">
              Guardar Perfil
            </button>
            <div id="pfSaved" class="hidden text-center text-xs text-green-400 font-bold">✓ Perfil Guardado</div>
          </div>
        </div>
      `;
    }

    function savePerfil() {
      const name = document.getElementById('pfName').value.trim();
      const country = document.getElementById('pfCountry').value;
      const goal = parseInt(document.getElementById('pfGoal').value) || 10;
      const sellCurrency = document.getElementById('pfSellCurrency').value;
      const buyCurrency = document.getElementById('pfBuyCurrency').value;
      
      saveProfile({ name, country, goal, sellCurrency, buyCurrency });
      
      const av = document.getElementById('avatarCircle');
      if(av && name) av.textContent = name[0].toUpperCase();
      
      const saved = document.getElementById('pfSaved');
      if(saved) {
        saved.classList.remove('hidden');
        setTimeout(() => saved.classList.add('hidden'), 2000);
      }
    }

    // ── MI NEGOCIO ───────────────────────────────────────────────────────────
    function getSalesData() {
      try { return JSON.parse(localStorage.getItem('tb_sales')||'{}'); } catch(e){ return {}; }
    }
    function saveSalesData(data) {
      try { localStorage.setItem('tb_sales', JSON.stringify(data)); } catch(e){}
    }
    function getUserId() {
      let uid = localStorage.getItem('tb_uid');
      if(!uid) { uid = 'u_'+Math.random().toString(36).slice(2)+Date.now().toString(36); localStorage.setItem('tb_uid', uid); }
      return uid;
    }
    function getNegocioProducts() {
      try { return JSON.parse(localStorage.getItem('tb_negocio')||'[]'); } catch(e){ return []; }
    }
    function saveNegocioProducts(arr) {
      try { localStorage.setItem('tb_negocio', JSON.stringify(arr)); } catch(e){}
    }

    function renderNegocio() {
      const el = document.getElementById('negocioContent');
      if(!el) return;
      const products = getNegocioProducts();

      // Financial calculations
      let totalInverted=0, totalRevenue=0, totalAds=0, totalStock=0, totalSold=0;
      products.forEach(p => {
        const costConverted = p.cost * p.fx;
        totalInverted += costConverted * p.stock;
        totalRevenue += p.price * p.sold;
        totalAds += p.ads;
        totalStock += p.stock;
        totalSold += p.sold;
      });

      const totalProfit = totalRevenue - totalInverted - totalAds;
      const roi = totalInverted > 0 ? Math.round(totalProfit / (totalInverted + totalAds) * 100) : 0;
      const stockValue = products.reduce((a, p) => a + p.cost * (p.fx || 1100) * (p.stock - p.sold), 0);

      const profile = getProfile();
      const sellCurrency = profile.sellCurrency || 'ARS';
      const buyCurrency = profile.buyCurrency || 'USD';

      el.innerHTML = `
        <!-- KPIs Financieros -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="bg-white/5 border border-white/10 rounded-2xl p-5">
            <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Ingresos totales</div>
            <div class="text-2xl font-extrabold text-green-400 mt-1">$${totalRevenue.toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-white/40 font-mono mt-1">${totalSold} unidades vendidas</div>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-2xl p-5">
            <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Ganancia Neta</div>
            <div class="text-2xl font-extrabold mt-1 ${totalProfit>=0?'text-green-400':'text-red-400'}">$${totalProfit.toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-white/40 font-mono mt-1">ROI: ${roi}%</div>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-2xl p-5">
            <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Inversión Stock</div>
            <div class="text-2xl font-extrabold text-white mt-1">$${(totalInverted+totalAds).toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-white/40 font-mono mt-1">Stock + Publicidad</div>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-2xl p-5">
            <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Valor en Stock</div>
            <div class="text-2xl font-extrabold text-white mt-1">$${stockValue.toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-white/40 font-mono mt-1">${totalStock-totalSold} unidades disponibles</div>
          </div>
        </div>

        <!-- Tabla Negocio -->
        <div class="bg-white/5 border border-white/10 rounded-[2rem] overflow-hidden">
          <div class="p-6 border-b border-white/10 bg-black/20">
            <h3 class="text-xs font-mono text-champagne uppercase tracking-widest">Mis Productos de Venta</h3>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left">
              <thead>
                <tr class="border-b border-white/10 text-white/40 font-mono uppercase text-[9px]">
                  <th class="p-4">Producto</th>
                  <th class="p-4 text-right">Costo</th>
                  <th class="p-4 text-right">Venta</th>
                  <th class="p-4 text-right">Stock</th>
                  <th class="p-4 text-right">Vendido</th>
                  <th class="p-4 text-right">Ganancia</th>
                  <th class="p-4 text-right"></th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                ${products.length ? products.map((p, i) => {
                  const costSell = p.cost * p.fx;
                  const profit = (p.price - costSell) * p.sold - p.ads;
                  return `
                    <tr class="hover:bg-white/5 transition text-xs">
                      <td class="p-4 font-bold text-white">${p.name}</td>
                      <td class="p-4 text-right font-mono">${p.cost} ${buyCurrency} <br> <span class="text-[9px] text-white/40">$${costSell.toFixed(0)} ARS</span></td>
                      <td class="p-4 text-right font-mono font-bold">$${p.price.toLocaleString()}</td>
                      <td class="p-4 text-right font-mono">${p.stock - p.sold}/${p.stock}</td>
                      <td class="p-4 text-right font-mono text-green-400 font-bold">${p.sold}</td>
                      <td class="p-4 text-right font-mono font-bold ${profit>=0?'text-green-400':'text-red-400'}">$${profit.toFixed(0)}</td>
                      <td class="p-4 text-right">
                        <div class="flex gap-2 justify-end">
                          <button onclick="quickSale(${i})" class="bg-green-600/10 hover:bg-green-600/20 text-green-400 border border-green-500/20 px-2.5 py-1 rounded-lg text-[10px] font-bold">+1 Venta</button>
                          <button onclick="quickStock(${i})" class="bg-white/5 hover:bg-white/10 px-2.5 py-1 border border-white/10 rounded-lg text-[10px] font-bold">Stock</button>
                          <button onclick="showAddProductModal(${i})" class="bg-white/5 hover:bg-white/10 px-2.5 py-1 border border-white/10 rounded-lg text-[10px] font-bold">Editar</button>
                        </div>
                      </td>
                    </tr>
                  `;
                }).join('') : `<tr><td colspan="7" class="p-8 text-center text-white/40 font-mono">No has agregado productos. Haz click en "+ Cargar Producto" para iniciar.</td></tr>`}
              </tbody>
            </table>
          </div>
        </div>
      `;
    }

    var editingNegocioIdx = null;

    function showAddProductModal(idx) {
      editingNegocioIdx = idx !== undefined ? idx : null;
      const products = getNegocioProducts();
      const p = idx !== undefined ? products[idx] : {};
      
      const overlay = document.createElement('div');
      overlay.id = 'negocioModal';
      overlay.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm';

      overlay.innerHTML = `
        <div class="bg-obsidian border border-white/10 rounded-[2.5rem] w-full max-w-md overflow-hidden shadow-2xl p-8">
          <div class="flex items-center justify-between border-b border-white/10 pb-4 mb-6">
            <h3 class="text-base font-bold text-white">${idx !== undefined ? 'Editar' : 'Agregar'} Producto</h3>
            <button onclick="document.getElementById('negocioModal').remove()" class="text-white/60 hover:text-white">✕</button>
          </div>

          <div class="space-y-4 text-xs font-mono">
            <div>
              <label class="text-[9px] text-white/40 uppercase block mb-1">Nombre del producto</label>
              <input id="np-name" value="${p.name || ''}" placeholder="Ej: Mini proyector" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-[9px] text-white/40 uppercase block mb-1">Costo Unitario (USD)</label>
                <input id="np-cost" type="number" step="0.01" value="${p.cost || ''}" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
              </div>
              <div>
                <label class="text-[9px] text-white/40 uppercase block mb-1">Venta Unitario (ARS)</label>
                <input id="np-price" type="number" value="${p.price || ''}" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-[9px] text-white/40 uppercase block mb-1">Stock Comprado</label>
                <input id="np-stock" type="number" value="${p.stock || ''}" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
              </div>
              <div>
                <label class="text-[9px] text-white/40 uppercase block mb-1">Vendidos</label>
                <input id="np-sold" type="number" value="${p.sold || 0}" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-[9px] text-white/40 uppercase block mb-1">Inversión Ads</label>
                <input id="np-ads" type="number" value="${p.ads || 0}" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
              </div>
              <div>
                <label class="text-[9px] text-white/40 uppercase block mb-1">Tipo de cambio FX</label>
                <input id="np-fx" type="number" value="${p.fx || 1100}" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
              </div>
            </div>

            <div>
              <label class="text-[9px] text-white/40 uppercase block mb-1">Proveedor</label>
              <select id="np-supplier" class="w-full bg-obsidian border border-white/10 rounded-xl px-4 py-3 text-white outline-none focus:border-champagne">
                <option value="AliExpress" ${(p.supplier||'AliExpress')==='AliExpress'?'selected':''}>AliExpress</option>
                <option value="CJ Dropshipping" ${p.supplier==='CJ Dropshipping'?'selected':''}>CJ Dropshipping</option>
                <option value="Alibaba" ${p.supplier==='Alibaba'?'selected':''}>Alibaba</option>
                <option value="Local" ${p.supplier==='Local'?'selected':''}>Proveedor local</option>
              </select>
            </div>

            <div class="flex gap-3 pt-4 border-t border-white/5">
              <button onclick="saveNegocioProduct()" class="flex-1 py-3 bg-champagne text-obsidian font-extrabold uppercase rounded-xl">Guardar</button>
              ${idx !== undefined ? `<button onclick="deleteNegocioProduct(${idx})" class="py-3 px-4 border border-red-500/20 text-red-400 rounded-xl hover:bg-red-500/10 transition">Eliminar</button>` : ''}
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(overlay);
    }

    function saveNegocioProduct() {
      const products = getNegocioProducts();
      const p = {
        name: document.getElementById('np-name').value.trim(),
        cost: parseFloat(document.getElementById('np-cost').value) || 0,
        price: parseFloat(document.getElementById('np-price').value) || 0,
        stock: parseInt(document.getElementById('np-stock').value) || 0,
        sold: parseInt(document.getElementById('np-sold').value) || 0,
        ads: parseFloat(document.getElementById('np-ads').value) || 0,
        fx: parseFloat(document.getElementById('np-fx').value) || 1100,
        supplier: document.getElementById('np-supplier').value,
        status: 'activo'
      };

      if(!p.name) return alert('Ingresá el nombre');
      
      if(editingNegocioIdx !== null) {
        products[editingNegocioIdx] = p;
      } else {
        products.push(p);
      }
      
      saveNegocioProducts(products);
      document.getElementById('negocioModal').remove();
      renderNegocio();
    }

    function deleteNegocioProduct(idx) {
      if(!confirm('¿Eliminar producto?')) return;
      const products = getNegocioProducts();
      products.splice(idx, 1);
      saveNegocioProducts(products);
      document.getElementById('negocioModal').remove();
      renderNegocio();
    }

    function quickSale(idx) {
      const products = getNegocioProducts();
      if(!products[idx]) return;
      if(products[idx].sold >= products[idx].stock) {
        showToast('Sin stock disponible', 'error');
        return;
      }
      products[idx].sold = (products[idx].sold || 0) + 1;
      saveNegocioProducts(products);
      
      // Sync to Supabase
      fetch('/api/track', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ type:'sale', user_id:getUserId(), product_name:products[idx].name, product_cat:'', product_score:0 })
      }).catch(()=>{});

      renderNegocio();
      showToast('¡Venta registrada! +1 ' + products[idx].name, 'success');
    }

    function quickStock(idx) {
      const products = getNegocioProducts();
      if(!products[idx]) return;
      const qty = parseInt(prompt('¿Cuántas unidades agregás al stock?', '10'));
      if(isNaN(qty) || qty <= 0) return;
      products[idx].stock = (products[idx].stock || 0) + qty;
      saveNegocioProducts(products);
      renderNegocio();
      showToast('+' + qty + ' unidades de stock agregadas', 'success');
    }

    function showToast(msg, type) {
      const t = document.createElement('div');
      const bg = type === 'success' ? 'bg-green-600' : 'bg-red-600';
      t.className = `fixed bottom-24 left-1/2 -translate-x-1/2 ${bg} text-white px-5 py-3 rounded-full text-xs font-bold font-mono shadow-2xl z-[9999] whitespace-nowrap`;
      t.textContent = msg;
      document.body.appendChild(t);
      setTimeout(() => {
        t.style.opacity = '0';
        t.style.transition = 'opacity 0.3s';
        setTimeout(() => t.remove(), 300);
      }, 2000);
    }

    // ── GUEST / AUTH LOGIN LOGIC ─────────────────────────────────────────────
    function openAuth(m='login') {
      document.getElementById('authModal').classList.remove('hidden');
      setAuthMode(m);
    }
    function closeAuth() {
      document.getElementById('authModal').classList.add('hidden');
    }
    function setAuthMode(m) {
      authMode = m;
      document.getElementById('tabLogin').classList.toggle('bg-white/10', m==='login');
      document.getElementById('tabLogin').classList.toggle('text-white', m==='login');
      document.getElementById('tabSignup').classList.toggle('bg-white/10', m==='signup');
      document.getElementById('tabSignup').classList.toggle('text-white', m==='signup');
      
      document.getElementById('authTitle').textContent = m==='login' ? 'Bienvenido de vuelta' : 'Creá tu cuenta gratis';
      document.getElementById('authSubtitle').textContent = m==='login' ? 'Ingresá para acceder al dashboard' : 'Empezá gratis, suscribite cuando quieras';
      document.getElementById('authSubmit').textContent = m==='login' ? 'Iniciar sesión' : 'Crear cuenta';
      
      document.getElementById('authErr').classList.add('hidden');
      document.getElementById('authOk').classList.add('hidden');
    }

    async function doAuth() {
      const email = document.getElementById('authEmail').value.trim();
      const pass = document.getElementById('authPass').value;
      const btn = document.getElementById('authSubmit');
      
      document.getElementById('authErr').classList.add('hidden');
      document.getElementById('authOk').classList.add('hidden');
      
      if(!email || !pass) {
        document.getElementById('authErr').textContent = 'Completá email y contraseña';
        document.getElementById('authErr').classList.remove('hidden');
        return;
      }
      if(pass.length < 6) {
        document.getElementById('authErr').textContent = 'Contraseña mínimo 6 caracteres';
        document.getElementById('authErr').classList.remove('hidden');
        return;
      }
      
      btn.disabled = true;
      btn.textContent = 'Procesando...';
      try {
        const res = await fetch('/api/auth', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ action:authMode, email, password:pass })
        });
        const data = await res.json();
        if(!res.ok) throw new Error(data.error || 'Error de autenticación');

        if(authMode === 'signup') {
          document.getElementById('authOk').textContent = '¡Cuenta creada! Iniciando sesión...';
          document.getElementById('authOk').classList.remove('hidden');
          setTimeout(() => setAuthMode('login'), 1500);
        } else {
          user = { email };
          plan = 'free';
          localStorage.setItem('tb_session', JSON.stringify({ email, access_token: data.access_token || '' }));
          localStorage.setItem('tb_plan', 'free');
          closeAuth();
          updateNav();
          enterDash();
        }
      } catch(e) {
        document.getElementById('authErr').textContent = e.message;
        document.getElementById('authErr').classList.remove('hidden');
      }
      btn.disabled = false;
      btn.textContent = authMode === 'login' ? 'Iniciar sesión' : 'Crear cuenta';
    }

    async function loginGoogle() {
      try {
        const res = await fetch('/api/auth', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ action:'google' })
        });
        const data = await res.json();
        if(data.url) location.href = data.url;
      } catch(e) {
        document.getElementById('authErr').textContent = 'Error al conectar con Google';
        document.getElementById('authErr').classList.remove('hidden');
      }
    }

    function logout() {
      user = null;
      plan = 'free';
      localStorage.removeItem('tb_session');
      localStorage.removeItem('tb_plan');
      updateNav();
      goLanding();
    }

    function toggleDD() {
      document.getElementById('userDD').classList.toggle('hidden');
    }
    function closeDD() {
      document.getElementById('userDD').classList.add('hidden');
    }

    async function subscribe(planName) {
      if(!user) { openAuth('signup'); return; }
      const btn = event?.target;
      if(btn) { btn.disabled = true; btn.textContent = 'Redirigiendo...'; }
      try {
        const res = await fetch('/api/subscribe', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ plan: planName, email: user.email })
        });
        const data = await res.json();
        if(data.url) {
          location.href = data.url;
        } else {
          throw new Error(data.error || 'No se pudo generar el link de pago');
        }
      } catch(e) {
        showToast('Error al procesar el pago: ' + e.message, 'error');
        if(btn) { btn.disabled = false; btn.textContent = planName === 'pro' ? 'Comenzar con Pro' : 'Probar 7 días gratis'; }
      }
    }

    // ── PRODUCTS DETAIL POPUP & SUPPLIERS ────────────────────────────────────
    // Remove duplicate let
    // currentProd is already defined globally
    function openProduct(idx) {
      currentProd = idx;
      const p = PRODUCTS[idx];
      if(!p) return;

      document.getElementById('pmTitle').textContent = p.name;
      document.getElementById('pmImgWrap').innerHTML = `<img src="${p.img || productImg(p)}" class="w-full h-full object-cover" loading="lazy" decoding="async">`;
      document.getElementById('pmScore').textContent = p.score;
      document.getElementById('pmChange').textContent = p.change;
      document.getElementById('pmMargin').textContent = p.marginStr;
      document.getElementById('pmCat').textContent = p.cat;
      document.getElementById('pmPrice').textContent = p.priceStr;
      
      const compBadge = document.getElementById('pmComp');
      compBadge.textContent = p.comp;
      const compColor = p.comp === 'Baja' ? 'bg-green-500/10 text-green-400 border-green-500/20' : p.comp === 'Alta' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
      compBadge.className = `text-xs font-bold font-mono px-2 py-0.5 rounded border uppercase ${compColor}`;

      const pmTag = document.getElementById('pmTag');
      pmTag.textContent = p.hot ? 'HOT' : 'TENDENCIA';
      pmTag.className = `text-xs font-mono font-bold px-2 py-0.5 rounded uppercase ${p.hot ? 'bg-champagne text-obsidian' : 'bg-white/10 text-white'}`;

      document.getElementById('pmPlats').innerHTML = p.plts.map(pl => `<span class="px-2 py-0.5 rounded bg-white/5 border border-white/10 text-[9px] font-mono font-bold">${PLT[pl] ? PLT[pl].label : pl}</span>`).join('');
      document.getElementById('pmCountries').innerHTML = (p.regions || []).map(r => `<span class="px-2 py-0.5 rounded bg-white/5 border border-white/10 text-[9px] font-mono font-bold">${r==='AR'?'🇦🇷 AR':r==='UY'?'🇺🇾 UY':'🇨🇱 CL'}</span>`).join('');
      
      renderSuppliersTab(p, document.getElementById('pmSuppliers'));
      
      document.getElementById('pmSaveBtn').innerHTML = saved.includes(idx) ? '<i data-lucide="bookmark-check" class="w-4 h-4 inline-block mr-1"></i> Guardado' : '<i data-lucide="bookmark" class="w-4 h-4 inline-block mr-1"></i> Guardar';
      
      switchModalTab('info', document.querySelector('.modal-tab'));
      _resetMktTab();
      document.getElementById('prodModal').classList.remove('hidden');
      lucide.createIcons();
    }

    function closeProdModal(e) {
      if(e.target === document.getElementById('prodModal')) closeProdModalDirect();
    }
    function closeProdModalDirect() {
      document.getElementById('prodModal').classList.add('hidden');
    }

    function saveCurrentProduct() {
      if(currentProd === null) return;
      toggleSave(currentProd);
      document.getElementById('pmSaveBtn').innerHTML = saved.includes(currentProd) ? '<i data-lucide="bookmark-check" class="w-4 h-4 inline-block mr-1"></i> Guardado' : '<i data-lucide="bookmark" class="w-4 h-4 inline-block mr-1"></i> Guardar';
      lucide.createIcons();
    }

    function toggleSave(idx) {
      const i = saved.indexOf(idx);
      if(i === -1) saved.push(idx);
      else saved.splice(i, 1);
      localStorage.setItem('tb_saved', JSON.stringify(saved));
      savedCount();
      renderProducts(false);
      renderLandingProducts();
    }
    function savedCount() {
      const countLabel = document.getElementById('savedCountSidebar');
      if(countLabel) countLabel.textContent = saved.length;
    }

    function renderSaved() {
      const el = document.getElementById('savedContent');
      if(!el) return;
      if(!saved.length) {
        el.innerHTML = '<div class="text-center py-12 text-white/40 text-xs font-mono">No tenés productos guardados todavía.</div>';
        return;
      }
      el.innerHTML = `
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          ${saved.map(idx => {
            const p = ALL_PRODUCTS[idx];
            if(!p) return '';
            return `
              <div onclick="openProduct(${idx})" class="bg-white/5 border border-white/10 rounded-[2rem] overflow-hidden hover-lift p-4 space-y-4 cursor-pointer">
                <div class="aspect-video w-full rounded-2xl overflow-hidden bg-black/20 relative">
                  <img src="${p.img || productImg(p)}" class="w-full h-full object-cover">
                  <span class="absolute top-3 left-3 text-[9px] font-mono font-bold uppercase bg-champagne text-obsidian px-2 py-0.5 rounded">${p.cat}</span>
                </div>
                <div class="space-y-2">
                  <h4 class="text-sm font-bold text-white truncate">${p.name}</h4>
                  <div class="flex justify-between items-center text-[10px] text-white/50 border-t border-white/5 pt-2">
                    <span>Margen: <b class="text-green-400 font-mono">${p.marginStr}</b></span>
                    <span>Comp: <b class="text-white font-mono">${p.comp}</b></span>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    function switchModalTab(tab, btn) {
      document.querySelectorAll('.modal-tab').forEach(t => {
        t.classList.remove('text-champagne', 'border-b-2', 'border-champagne');
        t.classList.add('text-white/50');
      });
      btn.classList.add('text-champagne', 'border-b-2', 'border-champagne');
      btn.classList.remove('text-white/50');
      
      document.querySelectorAll('.modal-tab-content').forEach(c => c.classList.add('hidden'));
      document.getElementById('tab-' + tab).classList.remove('hidden');

      if(tab === 'history' && currentProd !== null) {
        renderHistoryChart();
      }
    }

    function renderHistoryChart() {
      const p = PRODUCTS[currentProd];
      if(!p) return;
      
      const tbody = document.getElementById('historyTbody');
      if(!tbody) return;
      tbody.innerHTML = p.history.map((score, i) => {
        const prev = p.history[i-1] || score;
        const diff = score - prev;
        const changeClass = diff >= 0 ? 'text-green-400' : 'text-red-400';
        return `
          <tr class="border-b border-white/5 text-xs">
            <td class="p-3 font-mono text-white/50">${WEEKS[i]}</td>
            <td class="p-3 font-bold text-white font-mono">${score}</td>
            <td class="p-3 font-mono font-bold ${changeClass}">${diff >= 0 ? '+' : ''}${diff}</td>
            <td class="p-3 text-white/70">${LEADERS[i % LEADERS.length]}</td>
          </tr>
        `;
      }).join('');
    }

    const SUPPLIERS_BUY = [
      { name:'AliExpress', icon:'🛒', url:'https://www.aliexpress.com/wholesale?SearchText=', ship:'10-25 días · Envío gratis', note:'El más popular para dropshipping', color:'#FF4747' },
      { name:'Alibaba', icon:'🏭', url:'https://www.alibaba.com/trade/search?SearchText=', ship:'20-35 días · Mayorista', note:'Precios más bajos, mínimo por lote', color:'#FF6A00' },
      { name:'CJ Dropshipping', icon:'🚀', url:'https://cjdropshipping.com/search/', ship:'7-12 días · Bodega LATAM', note:'Bodega en Brasil y México', color:'#00A87E' },
    ];

    function renderSuppliersTab(p, el) {
      if(!el) return;
      const q = encodeURIComponent(p.name || '');
      el.innerHTML = `
        <div class="space-y-4">
          <div class="text-[9px] font-mono text-white/40 uppercase tracking-widest border-b border-white/5 pb-2">Dónde comprar (Est. AliExpress)</div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            ${SUPPLIERS_BUY.map(s => {
              const estPrice = (p.score * 0.08).toFixed(2);
              return `
                <a href="${s.url + q}" target="_blank" class="bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl p-4 flex flex-col justify-between transition duration-200">
                  <div>
                    <div class="text-sm font-bold text-white mb-1">${s.icon} ${s.name}</div>
                    <div class="text-[8px] font-mono text-white/40 mb-2">${s.ship}</div>
                    <div class="text-[9px] text-white/60 leading-relaxed">${s.note}</div>
                  </div>
                  <div class="text-xs font-extrabold text-green-400 font-mono mt-4">~USD ${estPrice}</div>
                </a>
              `;
            }).join('')}
          </div>
        </div>
      `;
      // Load real AE products
      loadAEProducts(p.name, el);
    }

    function markAsSold() {
      if(currentProd === null) return;
      const p = PRODUCTS[currentProd];
      if(!p) return;
      
      const sales = getSalesData();
      const key = (p.name || '').toLowerCase().trim();
      sales[key] = (sales[key] || 0) + 1;
      saveSalesData(sales);

      // Save to business negocio
      const negProducts = getNegocioProducts();
      const negIdx = negProducts.findIndex(np => (np.name || '').toLowerCase().trim() === key);
      if(negIdx >= 0) {
        negProducts[negIdx].sold = (negProducts[negIdx].sold || 0) + 1;
        saveNegocioProducts(negProducts);
      } else {
        negProducts.push({
          name: p.name, cost: Math.max(3, p.score * 0.08), price: Math.max(10, p.score * 0.25) * 1100,
          stock: 10, sold: 1, ads: 0, fx: 1100, supplier: 'AliExpress', status: 'activo'
        });
        saveNegocioProducts(negProducts);
      }

      // Sync to Supabase track
      fetch('/api/track', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ type:'sale', user_id:getUserId(), product_name:p.name, product_cat:p.cat, product_score:p.score })
      }).catch(()=>{});

      const confirm = document.getElementById('soldConfirm');
      if(confirm) {
        confirm.classList.remove('hidden');
        setTimeout(() => confirm.classList.add('hidden'), 3000);
      }
      
      renderPublicLeaderboard();
    }

    function analyzeProduct() {
      if(currentProd === null) return;
      const p = PRODUCTS[currentProd];
      closeProdModalDirect();
      enterDash();
      setTimeout(() => {
        goSection('analisis');
        askAI(`Analizá el producto "${p.name}" con TrendScore ${p.score}, margen ${p.marginStr} y competencia ${p.comp}. ¿Por qué está en tendencia y cómo lo venderías en LATAM?`);
      }, 300);
    }

    // ── MARKETING IA ────────────────────────────────────────────────────────
    let _mktCache = {};

    function _mktCacheKey(name) { return 'mkt_' + name.toLowerCase().replace(/\s+/g,'_'); }

    function generateMarketingCopy() {
      if (currentProd === null) return;
      const p = PRODUCTS[currentProd];
      const plan = currentPlan();

      if (!plan || plan.id === 'free') {
        document.getElementById('mkt-gate')?.classList.remove('hidden');
        document.getElementById('mkt-generate-wrap')?.classList.add('hidden');
        return;
      }

      const cacheKey = _mktCacheKey(p.name);
      const cached = localStorage.getItem(cacheKey);
      if (cached) {
        try {
          const { data, ts } = JSON.parse(cached);
          if (Date.now() - ts < 86400000) { _renderMkt(data, true); return; }
        } catch(e) {}
      }

      _setMktState('loading');
      const btn = document.getElementById('mktGenerateBtn');
      if (btn) btn.disabled = true;

      fetch('/api/describe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product: p, plan: plan.id })
      }).then(r => r.json()).then(res => {
        if (btn) btn.disabled = false;
        if (res.error) { _setMktState('error', res.error); return; }
        const copy = res.copy;
        localStorage.setItem(cacheKey, JSON.stringify({ data: { copy, model: res.model }, ts: Date.now() }));
        _renderMkt({ copy, model: res.model }, false);
      }).catch(err => {
        if (btn) btn.disabled = false;
        _setMktState('error', err.message || 'Error de red');
      });
    }

    function _setMktState(state, msg) {
      ['mkt-loading','mkt-content','mkt-error','mkt-generate-wrap','mkt-gate'].forEach(id => {
        document.getElementById(id)?.classList.add('hidden');
      });
      if (state === 'loading') {
        document.getElementById('mkt-loading')?.classList.remove('hidden');
      } else if (state === 'error') {
        const msgEl = document.getElementById('mkt-error-msg');
        if (msgEl) msgEl.textContent = msg || 'Error al generar';
        document.getElementById('mkt-error')?.classList.remove('hidden');
        document.getElementById('mkt-generate-wrap')?.classList.remove('hidden');
      } else if (state === 'idle') {
        document.getElementById('mkt-generate-wrap')?.classList.remove('hidden');
      }
    }

    function _renderMkt({ copy, model }, fromCache) {
      _setMktState('');
      document.getElementById('mkt-content')?.classList.remove('hidden');
      const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val || ''; };
      set('mkt-ml-titulo', copy.ml_titulo);
      set('mkt-ml-desc', copy.ml_descripcion);
      set('mkt-tiktok', copy.tiktok_script);
      set('mkt-instagram', copy.instagram_caption);
      set('mkt-precio', copy.precio_sugerido_ars);
      set('mkt-diferencial', copy.punto_diferencial);
      set('mkt-model-name', (model || 'Claude Haiku').replace('claude-','').replace('-',' '));
      const kwWrap = document.getElementById('mkt-keywords');
      if (kwWrap && Array.isArray(copy.keywords_seo)) {
        kwWrap.innerHTML = copy.keywords_seo.map(k =>
          `<span class="text-xs bg-blue-500/15 border border-blue-500/25 text-blue-300 px-2.5 py-1 rounded-full">${k}</span>`
        ).join('');
      }
      const badge = document.getElementById('mkt-model-badge');
      if (badge && fromCache) badge.innerHTML += ' <span class="ml-1 text-white/25">(caché)</span>';
      if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    function clearMarketingCache() {
      if (currentProd === null) return;
      const p = PRODUCTS[currentProd];
      localStorage.removeItem(_mktCacheKey(p.name));
      _setMktState('idle');
      document.getElementById('mkt-content')?.classList.add('hidden');
    }

    function copyMktField(id) {
      const el = document.getElementById(id);
      if (!el) return;
      const text = id === 'mkt-keywords'
        ? Array.from(el.querySelectorAll('span')).map(s => s.textContent).join(', ')
        : el.textContent;
      navigator.clipboard.writeText(text).then(() => toast('¡Copiado al portapapeles!', 'success', 2000));
    }

    function copyMktSection() {
      const t1 = document.getElementById('mkt-ml-titulo')?.textContent || '';
      const t2 = document.getElementById('mkt-ml-desc')?.textContent || '';
      navigator.clipboard.writeText(t1 + '\n\n' + t2).then(() => toast('Título y descripción copiados', 'success', 2000));
    }

    function _resetMktTab() {
      ['mkt-loading','mkt-content','mkt-error','mkt-gate'].forEach(id => {
        document.getElementById(id)?.classList.add('hidden');
      });
      document.getElementById('mkt-generate-wrap')?.classList.remove('hidden');
      const btn = document.getElementById('mktGenerateBtn');
      if (btn) btn.disabled = false;
    }

    // ── ANTHROPIC CLAUDE CHAT IA ─────────────────────────────────────────────
    const AI_SYS = 'Sos el asistente IA de TrendBase, plataforma de tendencias para dropshippers de Argentina, Uruguay y Chile. Ayudás con: productos virales, márgenes estimados, proveedores, estrategias de venta. Respondé en español, conciso y útil. Máximo 3 párrafos.';
    
    async function askAI(msg) {
      if(aiLoading) return;
      const input = document.getElementById('aiInput');
      const text = msg || input.value.trim();
      if(!text) return;
      
      if(input) input.value = '';
      aiLoading = true;
      
      const msgs = document.getElementById('aiMessages');
      msgs.innerHTML += `<div class="msg msg-user bg-champagne text-obsidian p-3 rounded-2xl max-w-[85%] self-end font-bold font-mono">${text}</div>`;
      msgs.innerHTML += `<div id="typing" class="p-3 bg-white/5 border border-white/5 rounded-2xl flex items-center gap-1 self-start"><span class="w-1.5 h-1.5 rounded-full bg-white/30 animate-bounce"></span><span class="w-1.5 h-1.5 rounded-full bg-white/30 animate-bounce" style="animation-delay: 0.2s"></span><span class="w-1.5 h-1.5 rounded-full bg-white/30 animate-bounce" style="animation-delay: 0.4s"></span></div>`;
      msgs.scrollTop = msgs.scrollHeight;
      
      aiHistory.push({ role:'user', content:text });
      try {
        const res = await fetch('/api/chat', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ messages: aiHistory, system: AI_SYS, plan: plan || 'free' })
        });
        const data = await res.json();
        if(!res.ok) throw new Error(data.error || 'Error del servidor de IA');
        
        const reply = data.text || 'Sin respuesta.';
        aiHistory.push({ role:'assistant', content:reply });
        
        const typingEl = document.getElementById('typing');
        if(typingEl) {
          typingEl.outerHTML = `<div class="msg msg-ai bg-white/5 border border-white/5 text-white/80 p-3 rounded-2xl max-w-[85%] self-start leading-relaxed">${reply.replace(/\n/g, '<br>')}</div>`;
        }
      } catch(e) {
        aiHistory.pop();
        const typingEl = document.getElementById('typing');
        if(typingEl) {
          typingEl.outerHTML = `<div class="msg msg-ai text-red-400 bg-red-500/10 border border-red-500/20 p-3 rounded-2xl max-w-[85%] self-start">⚠️ ${e.message}</div>`;
        }
      }
      aiLoading = false;
      msgs.scrollTop = msgs.scrollHeight;
    }

    // ── CURRENCY SWITCHER ────────────────────────────────────────────────────
    const prices = {
      AR: { free: "$0", starter: "$9.999", pro: "$19.999", period: "ARS/mes" },
      UY: { free: "$0", starter: "$390", pro: "$790", period: "UYU/mes" },
      CL: { free: "$0", starter: "$4.990", pro: "$9.990", period: "CLP/mes" }
    };

    function changeCurrency(country) {
      document.querySelectorAll('.currency-toggle-btn').forEach(btn => {
        btn.classList.remove('active-toggle', 'bg-obsidian', 'text-white');
        btn.classList.add('bg-slate/10', 'text-slate');
      });
      const activeBtn = document.getElementById(`btn-currency-${country}`);
      if(activeBtn) {
        activeBtn.classList.add('active-toggle', 'bg-obsidian', 'text-white');
        activeBtn.classList.remove('bg-slate/10', 'text-slate');
      }

      document.getElementById('price-free').innerText = prices[country].free;
      document.getElementById('price-period-free').innerText = prices[country].period;

      document.getElementById('price-starter').innerText = prices[country].starter;
      document.getElementById('price-period-starter').innerText = prices[country].period;

      document.getElementById('price-pro').innerText = prices[country].pro;
      document.getElementById('price-period-pro').innerText = prices[country].period;
    }

    // ── SHUFFLER / TYPEWRITER ANIMATION LOGIC ────────────────────────────────
    let currentShufflerIndex = 0;
    const shufflerCards = [
      document.getElementById('shuffler-card-0'),
      document.getElementById('shuffler-card-1'),
      document.getElementById('shuffler-card-2')
    ];

    setInterval(() => {
      shufflerCards.forEach((card, idx) => {
        if(!card) return;
        let order = (idx - currentShufflerIndex + 3) % 3;
        if (order === 0) {
          card.style.zIndex = '10';
          card.style.transform = 'translateY(8px) scale(0.9)';
          card.style.opacity = '0.6';
        } else if (order === 1) {
          card.style.zIndex = '20';
          card.style.transform = 'translateY(4px) scale(0.95)';
          card.style.opacity = '0.8';
        } else if (order === 2) {
          card.style.zIndex = '30';
          card.style.transform = 'translateY(0px) scale(1)';
          card.style.opacity = '1';
        }
      });
      currentShufflerIndex = (currentShufflerIndex + 1) % 3;
    }, 3000);

    const typewriterFeed = document.getElementById('typewriter-console');
    const messages = [
      "[$] Monitoreando tendencias de Argentina...",
      "[$] Analizando engagement de TikTok en ARS...",
      "[$] Encontrados 14 productos calientes en Mercado Libre.",
      "[$] Sincronizando datos de Uruguay en UYU...",
      "[$] Evaluando costos de flete internacional CLP...",
      "[$] TrendBase Engine listo."
    ];
    let msgIdx = 0;
    let charIdx = 0;
    let currentMsg = '';

    function typeNextMessage() {
      if(!typewriterFeed) return;
      if (msgIdx >= messages.length) {
        msgIdx = 0;
        typewriterFeed.innerHTML = '';
      }
      currentMsg = messages[msgIdx];
      charIdx = 0;
      typeCharacter();
    }

    function typeCharacter() {
      if(!typewriterFeed) return;
      if (charIdx < currentMsg.length) {
        typewriterFeed.innerHTML += currentMsg.charAt(charIdx);
        charIdx++;
        setTimeout(typeCharacter, 45);
      } else {
        typewriterFeed.innerHTML += '<br>';
        msgIdx++;
        setTimeout(typeNextMessage, 1500);
      }
    }

    const cursor = document.getElementById('scheduler-cursor');
    const days = document.querySelectorAll('.scheduler-day');
    const actionBtn = document.getElementById('scheduler-action');
    const statusLabel = document.getElementById('scheduler-status');

    function animateCursorScheduler() {
      const containerEl = document.getElementById('scheduler-container');
      if(!containerEl || !cursor || !actionBtn) return;
      const containerRect = containerEl.getBoundingClientRect();
      const targetDay = days[2];
      if(!targetDay) return;
      const dayRect = targetDay.getBoundingClientRect();
      const btnRect = actionBtn.getBoundingClientRect();

      gsap.to(cursor, {
        x: dayRect.left - containerRect.left + dayRect.width / 2,
        y: dayRect.top - containerRect.top + dayRect.height / 2,
        duration: 1.5,
        ease: 'power2.inOut',
        onComplete: () => {
          gsap.to(cursor, {
            scale: 0.8,
            duration: 0.15,
            yoyo: true,
            repeat: 1,
            onComplete: () => {
              targetDay.classList.add('bg-champagne/20', 'border-champagne');
              if(statusLabel) statusLabel.innerText = "MARGEN ESTIMADO: 45%-60%";
              
              gsap.to(cursor, {
                x: btnRect.left - containerRect.left + btnRect.width / 2,
                y: btnRect.top - containerRect.top + btnRect.height / 2,
                duration: 1.5,
                ease: 'power2.inOut',
                onComplete: () => {
                  gsap.to(cursor, {
                    scale: 0.8,
                    duration: 0.15,
                    yoyo: true,
                    repeat: 1,
                    onComplete: () => {
                      actionBtn.classList.add('bg-champagne', 'text-obsidian');
                      actionBtn.innerText = "RETORNO ESTIMADO: +210%";
                      
                      gsap.to(cursor, {
                        opacity: 0,
                        duration: 0.5,
                        delay: 2,
                        onComplete: () => {
                          targetDay.classList.remove('bg-champagne/20', 'border-champagne');
                          actionBtn.classList.remove('bg-champagne', 'text-obsidian');
                          actionBtn.innerText = "CALCULAR RETORNO ESTIMADO";
                          if(statusLabel) statusLabel.innerText = "READY";
                          gsap.set(cursor, { x: -30, y: -30, opacity: 1, scale: 1 });
                          setTimeout(animateCursorScheduler, 1000);
                        }
                      });
                    }
                  });
                }
              });
            }
          });
        }
      });
    }
    setTimeout(animateCursorScheduler, 2000);

    // AI_SYS already defined
    async function askAI(msg){
      if(aiLoading)return;
      var planData = currentPlan();
      var maxMsg = planData.aiMessages || 0;
      if(maxMsg === 0) { showToast('El asistente IA requiere plan Starter o superior.', 'error'); return; }
      var todayKey = 'tb_ai_msgs_'+new Date().toISOString().slice(0,10);
      var todayCount = parseInt(localStorage.getItem(todayKey)||'0');
      if(todayCount >= maxMsg) { showToast('Alcanzaste el límite de mensajes IA diarios. Upgradeá al plan Pro.', 'error'); return; }
      localStorage.setItem(todayKey, todayCount+1);

      const input=document.getElementById('aiInput'),btn=document.getElementById('aiSend'),msgs=document.getElementById('aiMessages');
      const text=msg||input.value.trim();if(!text)return;
      if(input)input.value='';aiLoading=true;if(btn)btn.disabled=true;
      
      msgs.innerHTML+='<div class="msg msg-user bg-champagne text-obsidian p-3 rounded-2xl max-w-[85%] self-end font-bold">'+text+'</div>';
      msgs.innerHTML+='<div class="typing" id="typing"><span class="text-white/40">Generando respuesta...</span></div>';
      msgs.scrollTop=msgs.scrollHeight;aiHistory.push({role:'user',content:text});
      try{
        const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:aiHistory,system:AI_SYS})});
        let data;try{data=await res.json();}catch(je){throw new Error('Error del servidor ('+res.status+')');}
        if(!res.ok)throw new Error(data.error||'Error: '+res.status);
        const reply=data.text||'Sin respuesta.';aiHistory.push({role:'assistant',content:reply});
        document.getElementById('typing').outerHTML='<div class="msg msg-ai bg-white/5 text-white/80 p-3 rounded-2xl max-w-[85%] self-start border border-white/5">'+reply.replace(/\\n/g,'<br>')+'</div>';
      }catch(e){aiHistory.pop();document.getElementById('typing').outerHTML='<div class="msg msg-ai bg-red-500/10 text-red-400 p-3 rounded-2xl max-w-[85%] self-start border border-red-500/20">\u26A0\uFE0F '+e.message+'</div>';}
      aiLoading=false;if(btn)btn.disabled=false;msgs.scrollTop=msgs.scrollHeight;
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
          div.className = 'flex items-center gap-3 p-3 bg-white/5 border border-white/10 rounded-xl hover:border-champagne transition no-underline text-white';
          
          const img = document.createElement('img');
          img.src = '/api/imgproxy?url=' + encodeURIComponent(p.image);
          img.className = 'w-12 h-12 object-cover rounded-lg shrink-0';
          img.onerror = () => img.style.display = 'none';
          
          const info = document.createElement('div');
          info.className = 'flex-1 min-w-0 text-xs';
          info.innerHTML = '<div class="font-bold truncate">'+p.title+'</div>' +
            '<div class="text-[10px] text-white/40 mt-0.5">' +
            (p.commission ? '<span class="bg-green-500/20 text-green-400 px-1.5 py-0.5 rounded font-mono font-bold mr-1">'+p.commission+'% comisión</span>' : '') +
            (p.rating ? '⭐ '+p.rating+'%' : '') + '</div>';
            
          const price = document.createElement('div');
          price.className = 'font-mono font-bold text-green-400 shrink-0';
          price.textContent = p.price;
          
          div.appendChild(img);div.appendChild(info);div.appendChild(price);
          return div;
        });
        const wrap = document.createElement('div');
        wrap.className = 'col-span-full mt-4 space-y-2';
        wrap.innerHTML = '<h4 class="text-xs font-mono font-bold text-champagne uppercase tracking-wider mb-2">Productos reales en AliExpress</h4>';
        const list = document.createElement('div');
        list.className = 'grid gap-2';
        items.forEach(i => list.appendChild(i));
        wrap.appendChild(list);
        container.appendChild(wrap);
      } catch(e) {}
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
          showToast('¡Excelente! Si querés compartir tu experiencia, escribinos a hola@trendbase.app 🙌', 'success');
        }, 500);
      }
    }

    function showUpgradeToast(msg) {
      let t=document.getElementById('upgradeToast');
      if(!t){
        t=document.createElement('div');
        t.id='upgradeToast';
        t.className='fixed bottom-8 left-1/2 -translate-x-1/2 bg-obsidian border border-champagne text-white px-6 py-4 rounded-2xl text-xs font-bold font-mono shadow-2xl z-[9999] flex items-center gap-4';
        document.body.appendChild(t);
      }
      t.innerHTML=msg+'<button onclick="scrollToPlans()" class="bg-champagne text-obsidian px-3 py-1.5 rounded-lg text-[10px] font-extrabold uppercase tracking-wider hover:bg-white transition whitespace-nowrap">Ver planes</button>';
      t.style.display='flex';
      clearTimeout(t._to);
      t._to=setTimeout(()=>t.style.display='none',5000);
    }

    function initGSAPAnimations() {
      if (typeof gsap === 'undefined') return;
      gsap.from(".hero-fade-item", {
        y: 40,
        opacity: 0,
        duration: 1.2,
        stagger: 0.15,
        ease: "power3.out",
        delay: 0.2
      });

      const featureCards = gsap.utils.toArray('.bg-white\\/5.border.border-white\\/10');
      if(featureCards.length) {
        featureCards.forEach(card => {
          gsap.from(card, {
            scrollTrigger: {
              trigger: card,
              start: "top 85%"
            },
            y: 40,
            opacity: 0,
            duration: 0.8,
            ease: "power2.out"
          });
        });
      }
    }

    // Run app engine init
    init();


// --- INTEGRACIONES TIENDAS ---

async function saveIntegration() {
  const platform = document.getElementById('int-platform').value;
  const url = document.getElementById('int-url').value;
  const token = document.getElementById('int-token').value;

  if (!url || !token) {
    if (typeof showToast === 'function') showToast('Por favor completa URL y Token', 'error');
    else if (typeof toast === 'function') toast('Por favor completa URL y Token', 'error', 3000);
    else alert('Por favor completa URL y Token');
    return;
  }

  // Guardar localmente
  localStorage.setItem('trendbase_store_platform', platform);
  localStorage.setItem('trendbase_store_url', url);
  localStorage.setItem('trendbase_store_token', token);

  // Si hay usuario logueado, guardarlo en Supabase metadata
  if (typeof user !== 'undefined' && user) {
    try {
      await fetch('/api/auth', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          action: 'update_metadata', 
          email: user.email, 
          metadata: { store_platform: platform, store_url: url, store_token: token } 
        })
      });
    } catch(e) {
      console.error('No se pudo guardar en la nube', e);
    }
  }

  document.getElementById('integrationsModal').classList.add('hidden');
  
  if (typeof showToast === 'function') showToast('¡Tienda conectada exitosamente!', 'success');
  else if (typeof toast === 'function') toast('¡Tienda conectada exitosamente!', 'success', 3000);
  else alert('¡Tienda conectada exitosamente!');
}

function loadIntegration() {
  const p = localStorage.getItem('trendbase_store_platform');
  const u = localStorage.getItem('trendbase_store_url');
  const t = localStorage.getItem('trendbase_store_token');
  
  if (p) document.getElementById('int-platform').value = p;
  if (u) document.getElementById('int-url').value = u;
  if (t) document.getElementById('int-token').value = t;
}

// Cargar al inicio si el modal existe
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('integrationsModal')) {
    loadIntegration();
  }
});

async function exportToStore() {
  if (typeof currentProd === 'undefined' || currentProd === null) return;
  const p = PRODUCTS[currentProd];
  
  const platform = localStorage.getItem('trendbase_store_platform');
  const url = localStorage.getItem('trendbase_store_url');
  const token = localStorage.getItem('trendbase_store_token');

  if (!platform || !url || !token) {
    document.getElementById('integrationsModal').classList.remove('hidden');
    if (typeof showToast === 'function') showToast('Debes conectar tu tienda primero', 'error');
    else if (typeof toast === 'function') toast('Debes conectar tu tienda primero', 'error', 3000);
    return;
  }

  const btn = event.target.closest('button');
  const originalText = btn.innerHTML;
  btn.innerHTML = '<i class="w-3.5 h-3.5 animate-spin data-lucide=\'loader\'"></i> Exportando...';
  btn.disabled = true;
  if(typeof lucide !== 'undefined') lucide.createIcons();

  try {
    // Get product price from UI or DB
    const priceEl = document.getElementById('calcPrice');
    const priceVal = priceEl ? priceEl.value : p.priceMin || p.price_min;

    const res = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        platform, url, token,
        product: {
          name: p.name,
          cat: p.cat,
          price: priceVal,
          description: "Producto exportado con IA desde TrendBase.",
          img: typeof productImg === 'function' ? productImg(p) : (p.imgKw || p.img_kw || p.img)
        }
      })
    });

    const data = await res.json();
    if (data.success) {
      if (typeof showToast === 'function') showToast('🚀 Producto creado en tu tienda', 'success');
      else if (typeof toast === 'function') toast('🚀 Producto creado en tu tienda', 'success', 3000);
      else alert('¡Producto exportado con éxito!');
    } else {
      throw new Error(data.error || 'Error desconocido');
    }
  } catch (err) {
    if (typeof showToast === 'function') showToast('Error al exportar: ' + err.message, 'error');
    else if (typeof toast === 'function') toast('Error al exportar: ' + err.message, 'error', 4000);
    else alert('Error: ' + err.message);
  } finally {
    btn.innerHTML = originalText;
    btn.disabled = false;
    if(typeof lucide !== 'undefined') lucide.createIcons();
  }
}
