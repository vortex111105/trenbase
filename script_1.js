
    // System Configurations & Data fallbacks
    const PLANS = {
      free:    { maxProducts: 20,    ai: false, advFilters: false, history: 7,  analysis: false, comparator: false, aiMessages: 0  },
      starter: { maxProducts: 150,   ai: true,  advFilters: true,  history: 90, analysis: true,  comparator: false, aiMessages: 10 },
      pro:     { maxProducts: 99999, ai: true,  advFilters: true,  history: 90, analysis: true,  comparator: true,  aimessages: 15 },
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

    const PRICES={
      USD:{starter:'$19/mes',pro:'$49/mes',period:'USD'}
    };

    const WEEKS=['Sem 1','Sem 2','Sem 3','Sem 4','Sem 5','Sem 6','Sem 7','Sem 8','Sem 9','Sem 10','Sem 11','Sem 12','Sem 13','Sem 14','Sem 15','Hoy'];
    const LEADERS=['🇦🇷 Argentina','🇺🇾 Uruguay','🇨🇱 Chile','🇦🇷 Argentina','🇨🇱 Chile','🇺🇾 Uruguay','🇦🇷 Argentina','🇨🇱 Chile'];

    let PRODUCTS = [];
    let ALL_PRODUCTS = []; // Dropshipping (From API)
    let selectedProducts = new Set();
    
    function toggleSelection(idx, e) {
      e.stopPropagation();
      if(selectedProducts.has(idx)) {
        selectedProducts.delete(idx);
      } else {
        selectedProducts.add(idx);
      }
      updateMasterCheckbox();
    }
    
    function toggleAllSelection(e) {
      e.stopPropagation();
      const dbToUse = (typeof businessMode !== 'undefined' && businessMode === 'ecommerce') ? ECOMMERCE_PRODUCTS : ALL_PRODUCTS;
      const checked = e.target.checked;
      
      let allFiltered = dbToUse.filter(p => {
        if(filter.plt && !p.plts.includes(filter.plt)) return false;
        if(filter.region && !p.regions.includes(filter.region)) return false;
        if(filter.cat && p.cat !== filter.cat) return false;
        if(filter.comp && p.comp !== filter.comp) return false;
        return true;
      });
      const maxP = currentPlan().maxProducts;
      allFiltered = allFiltered.slice(0, maxP);

      if(checked) {
        allFiltered.forEach(p => selectedProducts.add(dbToUse.indexOf(p)));
      } else {
        selectedProducts.clear();
      }
      renderProducts(false);
    }
    
    function updateMasterCheckbox() {
      const cb = document.getElementById('masterCheckbox');
      if(!cb) return;
      cb.checked = selectedProducts.size > 0;
    }
    
    // Base de datos realista para Marca Propia (B2B / Private Label)
    const ECOMMERCE_PRODUCTS = [
      { name: 'Suplemento Ashwagandha KSM-66 (Marca Blanca)', cat: 'Salud', score: 98, change: '+15%', changeNum: 15, plts: ['IG', 'TK'], margin: 65, marginStr: '65%', hot: true, regions: ['AR', 'CL', 'UY'], comp: 'Media', priceMin: 25, priceStr: '$25.00', history: [80, 85, 90, 95, 98], rank: 1, suppliers: [{ name: 'Alibaba OEM BioTech', price: '$8.50 (MOQ 100)' }] },
      { name: 'Set Skincare Ácido Hialurónico (Personalizable)', cat: 'Belleza', score: 95, change: '+12%', changeNum: 12, plts: ['IG', 'TK'], margin: 70, marginStr: '70%', hot: true, regions: ['AR', 'UY'], comp: 'Alta', priceMin: 35, priceStr: '$35.00', history: [70, 75, 85, 90, 95], rank: 2, suppliers: [{ name: 'Guangzhou Cosmetology', price: '$10.50 (MOQ 50)' }] },
      { name: 'Ropa Deportiva Seamless (Etiqueta Propia)', cat: 'Moda', score: 92, change: '+8%', changeNum: 8, plts: ['IG'], margin: 55, marginStr: '55%', hot: false, regions: ['CL'], comp: 'Alta', priceMin: 40, priceStr: '$40.00', history: [80, 82, 85, 88, 92], rank: 3, suppliers: [{ name: 'Yiwu Textile Factory', price: '$18.00 (MOQ 200)' }] },
      { name: 'Gomitas de Magnesio para Dormir (OEM)', cat: 'Salud', score: 90, change: '+20%', changeNum: 20, plts: ['TK'], margin: 60, marginStr: '60%', hot: true, regions: ['AR', 'CL'], comp: 'Baja', priceMin: 22, priceStr: '$22.00', history: [50, 60, 70, 80, 90], rank: 4, suppliers: [{ name: 'NutriGummy B2B', price: '$8.80 (MOQ 150)' }] },
      { name: 'Manta Pesada Terapéutica (Premium)', cat: 'Hogar', score: 88, change: '+5%', changeNum: 5, plts: ['IG', 'TK'], margin: 50, marginStr: '50%', hot: false, regions: ['UY', 'CL'], comp: 'Media', priceMin: 80, priceStr: '$80.00', history: [85, 86, 87, 88, 88], rank: 5, suppliers: [{ name: 'Shenzhen HomeGoods', price: '$40.00 (MOQ 20)' }] },
      { name: 'Botella de Agua Acero Inoxidable (Logo Custom)', cat: 'Deporte', score: 85, change: '+2%', changeNum: 2, plts: ['IG'], margin: 75, marginStr: '75%', hot: false, regions: ['AR', 'CL', 'UY'], comp: 'Alta', priceMin: 20, priceStr: '$20.00', history: [80, 81, 83, 84, 85], rank: 6, suppliers: [{ name: 'Zhejiang Drinkware', price: '$5.00 (MOQ 300)' }] },
      { name: 'Kit de Blanqueamiento Dental (Marca Blanca)', cat: 'Belleza', score: 82, change: '-3%', changeNum: -3, plts: ['TK'], margin: 80, marginStr: '80%', hot: false, regions: ['CL'], comp: 'Alta', priceMin: 45, priceStr: '$45.00', history: [90, 88, 85, 84, 82], rank: 7, suppliers: [{ name: 'SmileTech OEM', price: '$9.00 (MOQ 100)' }] },
      { name: 'Cinturón de Levantamiento de Pesas (Cuero)', cat: 'Deporte', score: 80, change: '+10%', changeNum: 10, plts: ['IG'], margin: 50, marginStr: '50%', hot: true, regions: ['AR', 'UY'], comp: 'Baja', priceMin: 50, priceStr: '$50.00', history: [60, 65, 70, 75, 80], rank: 8, suppliers: [{ name: 'Sialkot Sports Factory', price: '$25.00 (MOQ 50)' }] },
      { name: 'Café de Especialidad en Grano (White Label)', cat: 'Alimentos', score: 78, change: '+18%', changeNum: 18, plts: ['IG'], margin: 40, marginStr: '40%', hot: true, regions: ['AR', 'CL'], comp: 'Media', priceMin: 18, priceStr: '$18.00', history: [40, 50, 60, 70, 78], rank: 9, suppliers: [{ name: 'Finca Colombia B2B', price: '$10.80 (MOQ 50kg)' }] },
      { name: 'Velas de Soja Aromáticas (Packaging Custom)', cat: 'Hogar', score: 75, change: '+0%', changeNum: 0, plts: ['IG', 'TK'], margin: 65, marginStr: '65%', hot: false, regions: ['UY'], comp: 'Alta', priceMin: 15, priceStr: '$15.00', history: [75, 75, 75, 75, 75], rank: 10, suppliers: [{ name: 'Artisan Decor China', price: '$5.25 (MOQ 200)' }] }
    ];

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
      
      // Auto-Upgrade interceptor for LemonSqueezy redirects
      if(window.location.search.includes('payment=success') || window.location.search.includes('subscribed=1') || window.location.search.includes('success=true')) {
        if(!user) {
          // If returned but not logged in, wait or just set plan
          plan = 'pro';
          localStorage.setItem('tb_plan', 'pro');
        } else {
          plan = 'pro';
          localStorage.setItem('tb_plan', 'pro');
          // Limpiar la URL para que no quede el parametro
          window.history.replaceState({}, document.title, window.location.pathname);
          // Opcional: entrar directo al dash
          setTimeout(() => enterDash(), 500);
        }
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

    // Fade in effect instead of sticky pin for cleaner reading
    const protocolCards = gsap.utils.toArray('.protocol-card');
    protocolCards.forEach((card, index) => {
      gsap.from(card, {
        opacity: 0,
        y: 50,
        duration: 1,
        ease: "power2.out",
        scrollTrigger: {
          trigger: card,
          start: 'top 70%',
        }
      });
    });

    // Navigation toggles: Landing ⇆ Dashboard
    function goLanding() {
      document.getElementById('view-landing').classList.add('active-view');
      document.getElementById('view-dash').classList.remove('active-view');
      
      document.getElementById('landing-nav').classList.remove('!hidden');
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
      
      document.getElementById('landing-nav').classList.add('!hidden');
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
      
      // MOCK DATABASE PARA TRENDBASE V1.0
      const mockData = {
        products: [
          { name: "Cama Relajante para Mascotas", cat: "Mascotas", score: 98, change: "up", change_num: 25.4, margin: 65, price_min: 35, price_str: "$35 - $50", hot: true, comp: "Baja", plts: ["TikTok", "Facebook"], regions: ["MX", "CO", "AR"], history: [40, 55, 70, 98], rank: 1, suppliers: [{name:"AliExpress", price: 12}] },
          { name: "Cepillo Quita Pelos Mágico", cat: "Mascotas", score: 95, change: "up", change_num: 18.2, margin: 70, price_min: 25, price_str: "$25 - $30", hot: true, comp: "Media", plts: ["TikTok", "Instagram"], regions: ["BR", "CO"], history: [30, 60, 80, 95], rank: 2, suppliers: [{name:"AliExpress", price: 6}] },
          { name: "Proyector Galaxia Inteligente", cat: "Tecnología", score: 92, change: "up", change_num: 12.5, margin: 55, price_min: 45, price_str: "$45 - $60", hot: false, comp: "Alta", plts: ["TikTok", "Amazon"], regions: ["US", "MX"], history: [80, 85, 90, 92], rank: 3, suppliers: [{name:"AliExpress", price: 18}] },
          { name: "Rizador de Pelo Automático", cat: "Belleza", score: 88, change: "up", change_num: 8.4, margin: 60, price_min: 40, price_str: "$40 - $55", hot: false, comp: "Media", plts: ["Instagram", "Pinterest"], regions: ["AR", "CL"], history: [50, 65, 75, 88], rank: 4, suppliers: [{name:"AliExpress", price: 15}] },
          { name: "Humidificador Anti-gravedad", cat: "Hogar", score: 85, change: "down", change_num: -2.1, margin: 50, price_min: 30, price_str: "$30 - $45", hot: false, comp: "Muy Alta", plts: ["TikTok", "Shopee"], regions: ["BR", "MX"], history: [95, 90, 88, 85], rank: 5, suppliers: [{name:"AliExpress", price: 14}] },
          { name: "Collar GPS para Perros", cat: "Mascotas", score: 97, change: "up", change_num: 32.1, margin: 75, price_min: 60, price_str: "$60 - $80", hot: true, comp: "Baja", plts: ["Facebook", "TikTok"], regions: ["CO", "CL", "MX"], history: [20, 45, 80, 97], rank: 6, suppliers: [{name:"AliExpress", price: 15}] },
          { name: "Rascador para Gatos de Pared", cat: "Mascotas", score: 84, change: "up", change_num: 15.0, margin: 55, price_min: 20, price_str: "$20 - $35", hot: false, comp: "Baja", plts: ["Instagram"], regions: ["AR", "MX"], history: [50, 60, 70, 84], rank: 7, suppliers: [{name:"AliExpress", price: 9}] },
          { name: "Luz LED Inteligente WiFi", cat: "Tecnología", score: 82, change: "up", change_num: 5.5, margin: 45, price_min: 15, price_str: "$15 - $25", hot: false, comp: "Alta", plts: ["TikTok"], regions: ["US", "BR"], history: [75, 78, 80, 82], rank: 8, suppliers: [{name:"AliExpress", price: 8}] },
          { name: "Limpiador Facial Ultrasónico", cat: "Belleza", score: 91, change: "up", change_num: 21.0, margin: 80, price_min: 35, price_str: "$35 - $60", hot: true, comp: "Media", plts: ["TikTok", "Pinterest"], regions: ["MX", "CO"], history: [40, 60, 85, 91], rank: 9, suppliers: [{name:"AliExpress", price: 7}] },
          { name: "Dispensador de Agua Automático", cat: "Hogar", score: 79, change: "down", change_num: -5.0, margin: 40, price_min: 12, price_str: "$12 - $20", hot: false, comp: "Muy Alta", plts: ["Facebook"], regions: ["CL", "AR"], history: [85, 82, 80, 79], rank: 10, suppliers: [{name:"AliExpress", price: 6}] },
          { name: "Juguete Interactivo para Gatos", cat: "Mascotas", score: 94, change: "up", change_num: 19.5, margin: 68, price_min: 18, price_str: "$18 - $30", hot: true, comp: "Media", plts: ["TikTok"], regions: ["MX", "BR", "CO"], history: [30, 50, 80, 94], rank: 11, suppliers: [{name:"AliExpress", price: 5}] },
          { name: "Cámara de Seguridad Mini", cat: "Tecnología", score: 89, change: "up", change_num: 11.2, margin: 50, price_min: 25, price_str: "$25 - $40", hot: false, comp: "Alta", plts: ["Facebook"], regions: ["AR", "MX"], history: [70, 75, 80, 89], rank: 12, suppliers: [{name:"AliExpress", price: 12}] },
          { name: "Rodillo de Masaje Facial", cat: "Belleza", score: 86, change: "up", change_num: 7.1, margin: 75, price_min: 15, price_str: "$15 - $25", hot: false, comp: "Media", plts: ["Instagram"], regions: ["CL", "CO"], history: [60, 70, 80, 86], rank: 13, suppliers: [{name:"AliExpress", price: 3}] },
          { name: "Aspiradora Inalámbrica Portátil", cat: "Hogar", score: 93, change: "up", change_num: 14.8, margin: 45, price_min: 45, price_str: "$45 - $70", hot: true, comp: "Alta", plts: ["TikTok"], regions: ["BR", "MX"], history: [60, 75, 85, 93], rank: 14, suppliers: [{name:"AliExpress", price: 25}] },
          { name: "Correa Retráctil con Linterna", cat: "Mascotas", score: 87, change: "up", change_num: 9.3, margin: 60, price_min: 22, price_str: "$22 - $35", hot: false, comp: "Baja", plts: ["Facebook"], regions: ["AR", "CO"], history: [55, 65, 75, 87], rank: 15, suppliers: [{name:"AliExpress", price: 8}] },
          { name: "Auriculares Bluetooth Invisibles", cat: "Tecnología", score: 81, change: "down", change_num: -1.5, margin: 40, price_min: 18, price_str: "$18 - $28", hot: false, comp: "Muy Alta", plts: ["TikTok"], regions: ["MX", "BR"], history: [85, 83, 82, 81], rank: 16, suppliers: [{name:"AliExpress", price: 10}] },
          { name: "Depiladora Láser Casera", cat: "Belleza", score: 96, change: "up", change_num: 28.5, margin: 85, price_min: 65, price_str: "$65 - $100", hot: true, comp: "Baja", plts: ["TikTok", "Instagram"], regions: ["AR", "MX", "CL"], history: [35, 60, 80, 96], rank: 17, suppliers: [{name:"AliExpress", price: 20}] },
          { name: "Organizador de Cables Magnético", cat: "Tecnología", score: 76, change: "up", change_num: 2.1, margin: 55, price_min: 8, price_str: "$8 - $15", hot: false, comp: "Baja", plts: ["Pinterest"], regions: ["US", "MX"], history: [60, 65, 70, 76], rank: 18, suppliers: [{name:"AliExpress", price: 3}] },
          { name: "Fuente de Agua para Mascotas", cat: "Mascotas", score: 90, change: "up", change_num: 16.4, margin: 62, price_min: 30, price_str: "$30 - $45", hot: true, comp: "Media", plts: ["TikTok"], regions: ["BR", "CO"], history: [50, 65, 80, 90], rank: 19, suppliers: [{name:"AliExpress", price: 11}] },
          { name: "Lámpara Atrapamosquitos UV", cat: "Hogar", score: 88, change: "up", change_num: 10.5, margin: 58, price_min: 25, price_str: "$25 - $40", hot: false, comp: "Media", plts: ["Facebook"], regions: ["MX", "AR"], history: [60, 70, 80, 88], rank: 20, suppliers: [{name:"AliExpress", price: 10}] }
        ],
        count: 47250
      };

      setTimeout(() => {
        setProducts(mockData.products, mockData);
      }, 800); // Simulate network latency
    }

    function setProducts(products, data) {
      const loadingEl = document.getElementById('productsLoading');
      const kpiEl = document.getElementById('kpiProductos');
      
      const mapped = products.map(p => ({
        name: p.name, cat: p.cat, score: p.score, change: p.change,
        changeNum: p.change_num !== undefined ? p.change_num : p.changeNum,
        plts: p.plts || [], margin: p.margin,
        marginStr: p.margin_str || p.marginStr || (p.margin ? `${p.margin}% ROI` : 'N/A'),
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
    function getProductImage(name) {
      return `https://tse2.mm.bing.net/th?q=${encodeURIComponent(name + ' producto aliexpress')}&w=300&h=300&c=7&rs=1&p=0`;
    }

    function renderLandingProducts() {
      const container = document.getElementById('landingProducts');
      if(!container) return;
      
      const list = (PRODUCTS || []).slice(0, 8);
      container.innerHTML = list.map((p, i) => {
        const image = p.img || getProductImage(p.name);
        return `
          <div onclick="openProduct(${i})" class="bg-white/5 border border-white/10 rounded-[2rem] overflow-hidden hover-lift shadow-sm cursor-pointer p-4 space-y-4">
            <div class="aspect-video w-full rounded-2xl overflow-hidden bg-black/20 relative">
              <img src="${image}" class="w-full h-full object-cover">
              <span class="absolute top-3 left-3 text-[9px] font-mono font-bold uppercase bg-champagne text-obsidian px-2 py-0.5 rounded">${p.cat}</span>
            </div>
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-mono text-champagne font-bold">Score: ${p.score}</span>
                <span class="text-[10px] font-mono neon-badge-green font-bold text-xs font-bold">${p.change}</span>
              </div>
              <h4 class="text-sm font-bold text-white truncate">${p.name}</h4>
              <div class="flex justify-between items-center text-[10px] text-white/50 border-t border-white/5 pt-2">
                <span>Margen: <b class="neon-badge-green font-bold text-xs font-mono">${p.marginStr}</b></span>
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

      // Select database based on Business Mode
      const dbToUse = (typeof businessMode !== 'undefined' && businessMode === 'ecommerce') ? ECOMMERCE_PRODUCTS : ALL_PRODUCTS;

      // Filter products
      let allFiltered = dbToUse.filter(p => {
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
        const idx = dbToUse.indexOf(p);
        const compClass = p.comp === 'Baja' ? 'neon-badge-green font-bold text-xs bg-green-500/10 border-green-500/20' : p.comp === 'Alta' ? 'neon-badge-red font-bold text-xs bg-red-500/10 border-red-500/20' : 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
        return `
          <tr onclick="openProduct(${idx})" class="hover:bg-white/5 transition cursor-pointer text-xs">
            <td class="p-4 text-center">
              <input type="checkbox" onclick="toggleSelection(${idx}, event)" ${selectedProducts.has(idx) ? 'checked' : ''} class="accent-champagne w-3 h-3 rounded bg-transparent border-white/20">
            </td>
            <td class="p-4 text-center font-mono text-white/40">${start + i + 1}</td>
            <td class="p-4">
              <div class="flex items-center gap-3">
                <img src="${getProductImage(p.name)}" alt="${p.name}" class="w-8 h-8 rounded border border-white/10 bg-black/20 object-cover" loading="lazy">
                <span class="font-bold text-white">${p.name}</span>
              </div>
            </td>
            <td class="p-4 font-mono text-champagne">${p.score}</td>
            <td class="p-4 font-mono neon-badge-green font-bold text-xs">${p.change}</td>
            <td class="p-4 font-mono neon-badge-green font-bold text-xs">${p.marginStr}</td>
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
      
      setTimeout(() => {
        renderAnalysisCatChart();
        populateAnalysisSelect();
        const sel = document.getElementById('analysisProductSel');
        if(sel && sel.options.length > 1) {
          sel.selectedIndex = 1;
          renderAnalysisHistory();
        }
      }, 100);
    }

    function renderAnalysisKPIs() {
      const el = document.getElementById('analysisKpis');
      if(!el) return;
      
      const prods = PRODUCTS;
      let avgMargin = Math.round(prods.reduce((a,p) => a + p.margin, 0) / prods.length) || 0;
      if (typeof businessMode !== 'undefined' && businessMode === 'ecommerce') {
        avgMargin += 35; // Simulate higher margin for B2B/Wholesale
      }
      const cats = {}; prods.forEach(p => { cats[p.cat] = (cats[p.cat] || 0) + 1; });
      const topCat = Object.entries(cats).sort((a,b) => b[1] - a[1])[0];
      const lowComp = prods.filter(p => p.comp === 'Baja').length;
      
      el.innerHTML = `
        <div class="glass-panel rounded-2xl p-5">
          <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Productos Analizados</div>
          <div class="text-3xl font-extrabold text-white mt-1">${prods.length}</div>
          <div class="text-[9px] neon-badge-green font-bold text-xs font-mono mt-1">${prods.filter(p=>p.hot).length} HOT ahora</div>
        </div>
        <div class="glass-panel rounded-2xl p-5">
          <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Categoría Líder</div>
          <div class="text-lg font-bold text-champagne truncate mt-1">${topCat ? topCat[0] : 'Ninguna'}</div>
          <div class="text-[9px] text-white/40 font-mono mt-1">${topCat ? Math.round(topCat[1]/prods.length*100) : 0}% del total</div>
        </div>
        <div class="glass-panel rounded-2xl p-5">
          <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Margen Promedio</div>
          <div class="text-3xl font-extrabold neon-badge-green font-bold text-xs mt-1">${avgMargin}%</div>
          <div class="text-[9px] neon-badge-green font-bold text-xs font-mono mt-1">Sólido vs mes anterior</div>
        </div>
        <div class="glass-panel rounded-2xl p-5">
          <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Baja Competencia</div>
          <div class="text-3xl font-extrabold text-white mt-1">${lowComp}</div>
          <div class="text-[9px] text-champagne font-mono mt-1">Score top: ${prods[0] ? prods[0].score : 0}</div>
        </div>
      `;
      
      const elOpp = document.getElementById('opportunityList');
      if(elOpp) {
        const topOpps = [...prods].sort((a,b) => b.score - a.score).slice(0, 4);
        elOpp.innerHTML = topOpps.map(p => `
          <div class="py-3 flex justify-between items-center cursor-pointer hover:bg-white/5 px-2 -mx-2 rounded-lg transition" onclick="openProduct(${PRODUCTS.indexOf(p)})">
            <span class="text-xs text-white truncate w-32">${p.name}</span>
            <span class="text-[10px] font-bold neon-badge-green font-bold text-xs bg-green-500/10 px-2 py-1 rounded">Score ${p.score}</span>
          </div>
        `).join('');
      }
      
      const elMarg = document.getElementById('topMarginList');
      if(elMarg) {
        const topMargs = [...prods].sort((a,b) => b.margin - a.margin).slice(0, 4);
        elMarg.innerHTML = topMargs.map(p => `
          <div class="py-3 flex justify-between items-center cursor-pointer hover:bg-white/5 px-2 -mx-2 rounded-lg transition" onclick="openProduct(${PRODUCTS.indexOf(p)})">
            <span class="text-xs text-white truncate w-32">${p.name}</span>
            <span class="text-[10px] font-bold text-champagne bg-champagne/10 px-2 py-1 rounded">${p.marginStr || (p.margin+'%')}</span>
          </div>
        `).join('');
      }
      
      const elReg = document.getElementById('regionHeatmap');
      if(elReg) {
        const regions = {};
        prods.forEach(p => { if(p.regions) p.regions.forEach(r => regions[r] = (regions[r] || 0) + 1) });
        const sortedRegs = Object.entries(regions).sort((a,b) => b[1] - a[1]).slice(0, 4);
        const maxR = sortedRegs[0] ? sortedRegs[0][1] : 1;
        elReg.innerHTML = sortedRegs.map(r => `
          <div class="mb-2">
            <div class="flex justify-between text-[10px] text-white/50 mb-1">
              <span>${r[0]}</span><span>${Math.round(r[1]/prods.length*100)}%</span>
            </div>
            <div class="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
              <div class="h-full bg-champagne" style="width: ${(r[1]/maxR)*100}%"></div>
            </div>
          </div>
        `).join('');
      }

      const elCat = document.getElementById('analysisCatChart');
      if(elCat) {
        const sortedCats = Object.entries(cats).sort((a,b) => b[1] - a[1]).slice(0, 4);
        elCat.innerHTML = sortedCats.map(c => `
          <div class="flex justify-between items-center bg-black/20 p-2 rounded-lg border border-white/5 mb-2">
            <span class="text-[10px] text-white/80">${c[0]}</span>
            <span class="text-[10px] font-mono text-champagne">${c[1]} prod</span>
          </div>
        `).join('');
      }
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
            <div class="font-bold neon-badge-green font-bold text-xs font-mono">${p.marginStr}</div>
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
        UY: { count:0, name:'Uruguay', flag:'🇺🇾', color:'neon-badge-green font-bold text-xs', bg:'bg-green-400/5', border:'border-green-500/20' },
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
          <span class="font-bold neon-badge-green font-bold text-xs font-mono">${p.marginStr}</span>
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
      sel.innerHTML = PRODUCTS.slice(0, 100).map((p, i) => `<option value="${i}">${p.name}</option>`).join('');
      if(PRODUCTS.length > 0) {
        sel.value = "0";
        renderAnalysisHistory();
      }
    }

    var currentAnalysisPeriod = 30;
    var analysisChartInst = null;

    function setAnalysisPeriod(days) {
      currentAnalysisPeriod = days;
      document.getElementById('ap7').className = 'px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase transition hover:bg-white/5 text-white/40 hover:text-white';
      document.getElementById('ap30').className = 'px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase transition hover:bg-white/5 text-white/40 hover:text-white';
      document.getElementById('ap90').className = 'px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase transition hover:bg-white/5 text-white/40 hover:text-white';
      
      const btn = document.getElementById('ap' + days);
      if(btn) btn.className = 'px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase transition ap-active bg-white/10 text-white';
      
      renderAnalysisHistory();
    }

    function playSimulatedAd() {
      alert("¡Pro Feature! En la versión completa, esto abrirá el video original de TikTok/Facebook Ads en una ventana emergente.");
    }

    let businessMode = 'dropshipping';
    function setBusinessMode(mode) {
      businessMode = mode;
      const dropBtn = document.getElementById('mode-drop');
      const ecomBtn = document.getElementById('mode-ecom');
      
      const thMargen = document.getElementById('th-margen');
      const thVenta = document.getElementById('th-venta');
      const thCosto = document.getElementById('th-costo');

      if (dropBtn && ecomBtn) {
        if (mode === 'dropshipping') {
          dropBtn.className = "px-3 py-1.5 rounded-lg text-[10px] font-bold transition bg-champagne text-obsidian";
          ecomBtn.className = "px-3 py-1.5 rounded-lg text-[10px] font-bold transition text-white/50 hover:text-white";
          if(thMargen) thMargen.innerText = 'Margen';
          if(thVenta) thVenta.innerText = 'Venta Est.';
          if(thCosto) thCosto.innerText = 'Costo Est.';
          toast('Modo Dropshipping: Todo el catálogo actualizado', 'info', 3000);
        } else {
          ecomBtn.className = "px-3 py-1.5 rounded-lg text-[10px] font-bold transition bg-champagne text-obsidian";
          dropBtn.className = "px-3 py-1.5 rounded-lg text-[10px] font-bold transition text-white/50 hover:text-white";
          if(thMargen) thMargen.innerText = 'Margen (Mayorista)';
          if(thVenta) thVenta.innerText = 'Mínimo (MOQ)';
          if(thCosto) thCosto.innerText = 'Fábrica Est.';
          toast('Modo Marca Propia: Catálogo B2B y MOQs cargados', 'info', 3000);
        }
      }
      PRODUCTS = mode === 'ecommerce' ? ECOMMERCE_PRODUCTS : ALL_PRODUCTS;
      populateAnalysisSelect();
      renderProducts(false); // Update products grid
      renderAnalysisKPIs();
      renderAnalysisHistory();
      
      // Auto-scroll so the user notices the supplier change in Analysis
      const elCost1 = document.getElementById('provCost1');
      if(elCost1) elCost1.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    function exportDataCSV() {
      if (!PRODUCTS || PRODUCTS.length === 0) {
        toast('No hay datos para exportar', 'error');
        return;
      }
      
      let itemsToExport = PRODUCTS;
      if (selectedProducts.size > 0) {
        itemsToExport = Array.from(selectedProducts).map(idx => PRODUCTS[idx]);
      }
      
      toast(`Generando CSV de ${itemsToExport.length} productos...`, 'info', 1500);
      
      const headers = ['Nombre', 'Categoría', 'Score', 'Margen', 'Competencia', 'Precio Venta', 'Proveedor (Costo)'];
      const rows = itemsToExport.map(p => [
        `"${p.name}"`, 
        `"${p.cat}"`, 
        p.score, 
        `"${p.marginStr}"`, 
        `"${p.comp}"`, 
        `"${p.priceStr}"`, 
        `"${p.suppliers && p.suppliers[0] ? p.suppliers[0].price : '—'}"`
      ]);
      
      const csvContent = "data:text/csv;charset=utf-8," + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement('a');
      link.setAttribute('href', encodedUri);
      const filename = businessMode === 'ecommerce' ? 'TrendBase_MarcaPropia_Report.csv' : 'TrendBase_Dropshipping_Report.csv';
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      setTimeout(() => toast('Descarga completada', 'success', 2000), 500);
    }

    function renderAnalysisHistory() {
      const sel = document.getElementById('analysisProductSel');
      if(!sel || sel.value === '') return;
      
      const idx = parseInt(sel.value);
      const p = PRODUCTS[idx];
      if(!p) return;

      const tbody = document.getElementById('analysisTbody');
      if(!tbody) return;

      let historySlice = p.history || [];
      const currentPeriodLabels = WEEKS.slice(0, currentAnalysisPeriod);
      renderAnalysisChart(currentPeriodLabels, historySlice.slice(-currentAnalysisPeriod), p.name);

      // Update Saturation Meter
      const satScore = Math.floor(Math.random() * 80) + 10;
      const satStoresCount = p.storeCount || 0;
      
      let satColor = 'neon-badge-green font-bold text-xs';
      let satBgColor = 'bg-green-500/10';
      let satStatusText = 'Oportunidad Temprana';
      let needleAngle = -90 + (180 * (satScore / 100)); // -90 to 90
      
      if(satScore > 75) {
        satColor = 'neon-badge-red font-bold text-xs'; satBgColor = 'bg-red-500/10'; satStatusText = 'Saturado';
      } else if(satScore > 40) {
        satColor = 'text-yellow-400'; satBgColor = 'bg-yellow-500/10'; satStatusText = 'Tendencia Activa';
      }
      
      const elSatText = document.getElementById('satText');
      const elSatStatus = document.getElementById('satStatus');
      const elSatNeedle = document.getElementById('satNeedle');
      const elSatGlow = document.getElementById('satGlow');
      const elSatCount = document.getElementById('satStoreCount');
      
      if(elSatText && elSatNeedle) {
        elSatText.innerText = satScore + '%';
        elSatText.className = `text-3xl font-extrabold ${satColor} transition-colors duration-500`;
        elSatStatus.innerText = satStatusText;
        elSatStatus.className = `text-xs font-bold ${satColor} uppercase tracking-widest mt-1 transition-colors duration-500`;
        elSatNeedle.style.transform = `translateX(-50%) rotate(${needleAngle}deg)`;
        elSatGlow.className = `absolute -right-6 -top-6 w-32 h-32 ${satBgColor} blur-3xl rounded-full transition-colors duration-500`;
        if(elSatCount) elSatCount.innerText = satStoresCount + ' tiendas';
      }

      let labelsSlice = WEEKS.slice(0, historySlice.length);
      
      if (currentAnalysisPeriod === 30) {
        historySlice = historySlice.slice(-4);
        labelsSlice = labelsSlice.slice(-4);
      } else if (currentAnalysisPeriod === 7) {
        historySlice = historySlice.slice(-2);
        labelsSlice = labelsSlice.slice(-2);
      }

      tbody.innerHTML = historySlice.map((score, i) => {
        const prev = i > 0 ? historySlice[i-1] : score;
        const diff = score - prev;
        const changeClass = diff >= 0 ? 'neon-badge-green font-bold text-xs' : 'neon-badge-red font-bold text-xs';
        return `
          <tr class="text-xs">
            <td class="p-3 font-mono text-white/50">${labelsSlice[i]}</td>
            <td class="p-3 font-bold text-white font-mono">${score}</td>
            <td class="p-3 font-mono font-bold ${changeClass}">${diff >= 0 ? '+' : ''}${diff}</td>
            <td class="p-3 text-white/70">${LEADERS[i % LEADERS.length]}</td>
          </tr>
        `;
      }).join('');
      
      // --- MOCK DYNAMIC WIDGETS ---
      // Proveedores
      let baseCost1 = 4.20; let baseCost2 = 5.10; let link1 = '#'; let link2 = '#';
      if(p.suppliers && p.suppliers.length > 0) {
         baseCost1 = parseFloat(String(p.suppliers[0].price).replace(/[^0-9.]/g, '')) || baseCost1;
         link1 = p.suppliers[0].url || link1;
         if(p.suppliers.length > 1) {
             baseCost2 = parseFloat(String(p.suppliers[1].price).replace(/[^0-9.]/g, '')) || baseCost2;
             link2 = p.suppliers[1].url || link2;
         } else {
             baseCost2 = baseCost1 * 1.2;
             link2 = link1;
         }
      }
      
      let cost1 = baseCost1;
      let cost2 = baseCost2;
      
      if (businessMode === 'ecommerce') {
        document.getElementById('provIcon1').className = "w-8 h-8 rounded bg-[#ff6a00] flex items-center justify-center text-white font-bold text-[9px]";
        document.getElementById('provIcon1').innerText = "B2B";
        document.getElementById('provName1').innerText = "Alibaba (Fábrica)";
        document.getElementById('provDesc1').innerText = "MOQ: 500 uds · Envío Marítimo";
        
        document.getElementById('provIcon2').className = "w-8 h-8 rounded bg-purple-600 flex items-center justify-center text-white font-bold text-[9px]";
        document.getElementById('provIcon2').innerText = "WL";
        document.getElementById('provName2').innerText = "Agente White Label";
        document.getElementById('provDesc2').innerText = "Envío Local: 2-4 días";
      } else {
        document.getElementById('provIcon1').className = "w-8 h-8 rounded bg-[#10b981] flex items-center justify-center text-white font-bold text-[9px]";
        document.getElementById('provIcon1').innerText = "DRP";
        document.getElementById('provName1').innerText = "Dropi (Latam)";
        document.getElementById('provDesc1').innerText = "Integración nativa · Pago Contra Entrega";
        
        document.getElementById('provIcon2').className = "w-8 h-8 rounded bg-[#3b82f6] flex items-center justify-center text-white font-bold text-[9px]";
        document.getElementById('provIcon2').innerText = "DDL";
        document.getElementById('provName2').innerText = "Dropdeal (Argentina)";
        document.getElementById('provDesc2').innerText = "Sincronización Tiendanube / Mercado Libre";
      }

      const elCost1 = document.getElementById('provCost1');
      if(elCost1) elCost1.innerText = `~$${cost1.toFixed(2)}`;
      const elCost2 = document.getElementById('provCost2');
      if(elCost2) elCost2.innerText = `~$${cost2.toFixed(2)}`;
      
      const elLink1 = document.getElementById('provLink1');
      if(elLink1) {
        elLink1.href = link1 !== '#' ? link1 : 'https://es.aliexpress.com/wholesale?SearchText=' + encodeURIComponent(p.name);
      }
      const elLink2 = document.getElementById('provLink2');
      if(elLink2) {
        elLink2.href = link2 !== '#' ? link2 : 'https://cjdropshipping.com/search/' + encodeURIComponent(p.name);
      }

      // --- SMART WIDGET MAPPING ---
      const nameLower = (p.name || '').toLowerCase();
      const catLower = (p.cat || '').toLowerCase();
      
      let nicheIdx = idx % 5; // fallback
      if (nameLower.includes('piel') || nameLower.includes('rostro') || nameLower.includes('led') || nameLower.includes('depil') || catLower.includes('belleza')) nicheIdx = 0; // Beauty
      else if (nameLower.includes('gym') || nameLower.includes('fit') || nameLower.includes('yoga') || nameLower.includes('postura') || catLower.includes('deporte')) nicheIdx = 1; // Fitness
      else if (nameLower.includes('perro') || nameLower.includes('gato') || nameLower.includes('mascota') || catLower.includes('mascota')) nicheIdx = 2; // Pets
      else if (nameLower.includes('proyector') || nameLower.includes('luz') || nameLower.includes('smart') || nameLower.includes('tech') || catLower.includes('tecno')) nicheIdx = 3; // Tech
      else if (nameLower.includes('cocina') || nameLower.includes('licuadora') || nameLower.includes('limpieza') || catLower.includes('hogar')) nicheIdx = 4; // Home/Kitchen

      // Audiencia
      const interestsMatrix = [
        ["Mascarillas LED", "Skincare Rutina", "Dermaplaning", "Estética"],
        ["Calistenia", "Suplementos Pre-workout", "Crossfit", "Recuperación Muscular"],
        ["Adiestramiento Canino", "Mascotas Ansiosas", "Juguetes Interactivos"],
        ["Smart Home", "Setup Gamer", "Domótica", "Productividad Apple"],
        ["Air Fryer Recetas", "Meal Prep", "Utensilios Profesionales"]
      ];
      const interests = interestsMatrix[nicheIdx] || interestsMatrix[0];
      const elAudInterests = document.getElementById('audInterests');
      if(elAudInterests) {
        elAudInterests.innerHTML = interests.map(i => `<span class="px-2 py-1 text-[9px] uppercase bg-black/40 border border-white/5 rounded-full text-white/60">${i}</span>`).join('');
      }

      const genderFemalePct = [85, 20, 60, 15, 70][nicheIdx] || 50;
      const genderMalePct = 100 - genderFemalePct;
      const elGenderLabels = document.getElementById('audGenderLabels');
      if(elGenderLabels) {
        elGenderLabels.innerHTML = `<span>Mujeres (${genderFemalePct}%)</span><span>Hombres (${genderMalePct}%)</span>`;
      }
      const elGenderBars = document.getElementById('audGenderBars');
      if(elGenderBars) {
        elGenderBars.innerHTML = `<div class="h-full bg-pink-500" style="width:${genderFemalePct}%"></div><div class="h-full bg-blue-500" style="width:${genderMalePct}%"></div>`;
      }

      const agesMatrix = [
        ["18-24", "25-34 (Top)", "35-44"],
        ["25-34", "35-44 (Top)", "45-54"],
        ["18-24 (Top)", "25-34", "35-44"],
        ["25-34", "35-44", "45-54 (Top)"],
        ["25-34", "35-44 (Top)", "45-54"]
      ];
      const ages = agesMatrix[nicheIdx] || agesMatrix[0];
      const elAges = document.getElementById('audAges');
      if(elAges) {
        elAges.innerHTML = ages.map(a => {
          if (a.includes('(Top)')) {
            return `<span class="px-2 py-1 bg-champagne/20 border border-champagne/50 rounded text-[10px] font-mono text-champagne font-bold">${a}</span>`;
          }
          return `<span class="px-2 py-1 bg-white/10 rounded text-[10px] font-mono text-white">${a}</span>`;
        }).join('');
      }

      const vViews = ["1.2M", "850K", "2.4M", "500K", "3.1M"];
      const elView1 = document.getElementById('adView1');
      if(elView1) elView1.innerText = `${vViews[(idx+2) % vViews.length]} Vistas`;
      const elView2 = document.getElementById('adView2');
      if(elView2) elView2.innerText = `${vViews[(idx+4) % vViews.length]} Vistas`;

      const videoImg1 = [
        "https://images.unsplash.com/photo-1611162617474-5b21e879e113?q=80&w=200&auto=format&fit=crop", // Beauty
        "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?q=80&w=200&auto=format&fit=crop", // Fit
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=200&auto=format&fit=crop", // Pets
        "https://images.unsplash.com/photo-1512496015851-a1dc8a477d24?q=80&w=200&auto=format&fit=crop", // Tech
        "https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=200&auto=format&fit=crop"  // Home
      ];
      const videoImg2 = [
        "https://images.unsplash.com/photo-1522337660859-02fbefca4702?q=80&w=200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1608231387042-66d1773070a5?q=80&w=200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1588195538326-c5b1e9f80a1b?q=80&w=200&auto=format&fit=crop"
      ];
      const elImg1 = document.getElementById('adImg1');
      if(elImg1) elImg1.src = videoImg1[nicheIdx] || videoImg1[0];
      const elImg2 = document.getElementById('adImg2');
      if(elImg2) elImg2.src = videoImg2[nicheIdx] || videoImg2[0];
      
      // Init Calculator Baseline
      const basePrice = parseFloat(p.priceStr.replace(/[^0-9.]/g, '')) || 25;
      const elPrice = document.getElementById('calcPrice');
      if(elPrice) {
        elPrice.value = basePrice;
        calcROI();
      }
    }
    
    function renderAnalysisChart(labels, data, name) {
      const ctx = document.getElementById('analysisChart');
      if(!ctx) return;
      if (analysisChartInst) analysisChartInst.destroy();
      
      analysisChartInst = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'TrendScore: ' + name,
            data: data,
            borderColor: '#C9A84C',
            backgroundColor: 'rgba(201, 168, 76, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 2,
            pointBackgroundColor: '#C9A84C',
            pointBorderColor: '#000',
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: { display: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: 'rgba(255,255,255,0.5)', font: { family: 'monospace', size: 10 } } },
            y: { display: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: 'rgba(255,255,255,0.5)', font: { family: 'monospace', size: 10 } } }
          }
        }
      });
    }

    function calcROI() {
      const cost = parseFloat(document.getElementById('calcCost').value) || 0;
      const price = parseFloat(document.getElementById('calcPrice').value) || 0;
      const ads = parseFloat(document.getElementById('calcAds').value) || 0;
      
      const elCostVal = document.getElementById('calcCostVal');
      const elPriceVal = document.getElementById('calcPriceVal');
      const elAdsVal = document.getElementById('calcAdsVal');
      
      if(elCostVal) elCostVal.innerText = '$' + cost.toFixed(2);
      if(elPriceVal) elPriceVal.innerText = '$' + price.toFixed(2);
      if(elAdsVal) elAdsVal.innerText = '$' + ads.toFixed(2);

      const el = document.getElementById('calcResult');
      if(!el) return;
      
      const sel = document.getElementById('analysisProductSel');
      let baseCost = 0;
      if(sel && sel.value !== '') {
        const p = PRODUCTS[parseInt(sel.value)];
        if(p && p.suppliers && p.suppliers[0]) {
           baseCost = parseFloat(p.suppliers[0].price.replace(/[^0-9.]/g, '')) || 0;
        }
      }
      
      const totalCost = baseCost + cost + ads;
      const netPerSale = price - totalCost;
      const margin = price > 0 ? Math.round((netPerSale / price) * 100) : 0;
      
      const colorClass = netPerSale > 0 ? 'neon-badge-green font-bold text-xs' : 'neon-badge-red font-bold text-xs';
      const bgClass = netPerSale > 0 ? 'bg-green-500/10 border-green-500/20' : 'bg-red-500/10 border-red-500/20';
      
      el.innerHTML = `
        <div class="flex justify-between items-center bg-black/40 border border-white/5 rounded-2xl p-4">
          <div>
            <div class="text-[9px] text-white/50 uppercase font-mono tracking-wider">Ganancia Neta por Venta</div>
            <div class="text-3xl font-extrabold ${colorClass} mt-1">$${netPerSale.toFixed(2)}</div>
            <div class="text-[9px] text-white/40 mt-1">Costo Producto Fábrica: $${baseCost.toFixed(2)}</div>
          </div>
          <div class="text-right">
             <div class="px-3 py-1.5 rounded-lg border ${bgClass} ${colorClass} text-xs font-bold font-mono">
               ${margin}% Margen
             </div>
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
            <div class="glass-panel rounded-2xl p-5 space-y-3">
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
            <div id="pfSaved" class="hidden text-center text-xs neon-badge-green font-bold text-xs font-bold">✓ Perfil Guardado</div>
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
    function toggleSidebarMenu(listId, iconId) {
      const list = document.getElementById(listId);
      const icon = document.getElementById(iconId);
      if(list.classList.contains('hidden')) {
        list.classList.remove('hidden');
        icon.style.transform = 'rotate(180deg)';
      } else {
        list.classList.add('hidden');
        icon.style.transform = 'rotate(0deg)';
      }
    }

    async function connectStore(platform) {
      const profile = getProfile();
      // Desconectar si ya está conectada
      if (profile.store === platform) {
        if (!confirm(`¿Desconectar tu tienda ${platform === 'shopify' ? 'Shopify' : 'TiendaNube'}?`)) return;
        profile.store = null;
        profile.storeCredentials = null;
        profile.storeName = null;
        profile.lastSync = null;
        profile.lastOrderId = null;
        saveProfile(profile);
        renderNegocio();
        toast('Tienda desconectada', 'info');
        return;
      }

      const isShopify = platform === 'shopify';
      const overlay = document.createElement('div');
      overlay.id = 'storeModal';
      overlay.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm';

      overlay.innerHTML = `
        <div class="glass-panel rounded-[2.5rem] w-full max-w-lg overflow-hidden shadow-2xl">
          <div class="flex items-center justify-between border-b border-white/10 px-8 py-5">
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
              <i data-lucide="link-2" class="w-4 h-4 text-champagne"></i>
              Conectar ${isShopify ? 'Shopify' : 'TiendaNube'}
            </h3>
            <button onclick="document.getElementById('storeModal').remove()" class="text-white/60 hover:text-white text-lg leading-none">✕</button>
          </div>

          <!-- Instrucciones -->
          <div class="mx-8 mt-6 bg-champagne/5 border border-champagne/20 rounded-2xl p-4 text-xs text-white/60 leading-relaxed">
            ${isShopify ? `
              <p class="font-bold text-champagne mb-2">¿Cómo obtener tu token?</p>
              <ol class="space-y-1 list-decimal list-inside">
                <li>Entrá a tu Admin de Shopify → <strong>Configuración → Apps</strong></li>
                <li>Click en <strong>"Desarrollar apps"</strong> → Crear una app</li>
                <li>En permisos de Admin API activá: <strong>read_orders, read_products, read_inventory</strong></li>
                <li>Click en <strong>Instalar app</strong> → copiá el <strong>Admin API access token</strong></li>
              </ol>
            ` : `
              <p class="font-bold text-champagne mb-2">¿Cómo obtener tu token?</p>
              <ol class="space-y-1 list-decimal list-inside">
                <li>Entrá a tu Admin de TiendaNube → <strong>Preferencias → API</strong></li>
                <li>Copiá tu <strong>ID de Usuario</strong> y tu <strong>Token de Acceso</strong></li>
              </ol>
            `}
          </div>

          <div class="px-8 py-6 space-y-4">
            ${isShopify ? `
              <div>
                <label class="block text-[10px] text-white/40 uppercase tracking-wider mb-1.5">Dominio de tu tienda</label>
                <input type="text" id="storeField1" class="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-champagne font-mono" placeholder="mitienda.myshopify.com">
              </div>
              <div>
                <label class="block text-[10px] text-white/40 uppercase tracking-wider mb-1.5">Admin API Access Token</label>
                <input type="password" id="storeField2" class="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-champagne font-mono" placeholder="shpat_...">
              </div>
            ` : `
              <div>
                <label class="block text-[10px] text-white/40 uppercase tracking-wider mb-1.5">ID de Usuario</label>
                <input type="text" id="storeField1" class="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-champagne font-mono" placeholder="123456">
              </div>
              <div>
                <label class="block text-[10px] text-white/40 uppercase tracking-wider mb-1.5">Token de Acceso API</label>
                <input type="password" id="storeField2" class="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-champagne font-mono" placeholder="abc123...">
              </div>
            `}

            <div id="storeConnectError" class="hidden text-xs neon-badge-red font-bold text-xs bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3"></div>
          </div>

          <div class="px-8 pb-8 flex gap-3">
            <button onclick="document.getElementById('storeModal').remove()" class="flex-1 px-4 py-3 rounded-xl text-xs font-bold text-white/60 hover:text-white bg-white/5 transition">Cancelar</button>
            <button id="storeConnectBtn" onclick="saveStoreConnection('${platform}')" class="flex-1 px-4 py-3 rounded-xl text-xs font-bold text-obsidian bg-champagne hover:bg-white transition shadow-[0_0_15px_rgba(201,168,76,0.3)]">
              Probar y conectar
            </button>
          </div>
        </div>
      `;
      document.body.appendChild(overlay);
      lucide.createIcons();
    }

    async function saveStoreConnection(platform) {
      const field1 = document.getElementById('storeField1')?.value?.trim();
      const field2 = document.getElementById('storeField2')?.value?.trim();
      const errEl = document.getElementById('storeConnectError');
      const btn = document.getElementById('storeConnectBtn');

      if (!field1 || !field2) {
        errEl.textContent = 'Completá ambos campos.';
        errEl.classList.remove('hidden');
        return;
      }

      btn.disabled = true;
      btn.textContent = 'Verificando y conectando...';
      errEl.classList.add('hidden');

      const credentials = platform === 'shopify'
        ? { domain: field1, token: field2 }
        : { userId: field1, token: field2 };

      // --- SIMULATE CONNECTION FOR DEMO PURPOSES ---
      setTimeout(() => {
        // Éxito — guardar credenciales en perfil local
        const profile = getProfile();
        profile.store = platform;
        profile.storeCredentials = credentials;
        profile.storeName = field1.split('.')[0].toUpperCase();
        profile.lastSync = null;
        profile.lastOrderId = null;
        saveProfile(profile);

        document.getElementById('storeModal').remove();
        renderNegocio();
        toast(`¡${profile.storeName} conectada! Sincronizando datos…`, 'success', 4000);

        // Sincronización inicial
        setTimeout(() => syncWithStore(), 1000);
      }, 1500);
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
        <!-- Conexión de Tiendas (Integraciones) -->
        <div class="bg-white/5 border border-white/10 rounded-[2rem] p-6 mb-6">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center gap-2">
                <i data-lucide="link-2" class="w-4 h-4 text-champagne"></i> Mi Tienda Online
                ${profile.store ? `<span class="text-[9px] font-mono bg-green-500/15 neon-badge-green font-bold text-xs border border-green-500/20 px-2 py-0.5 rounded-full">● CONECTADA</span>` : ''}
              </h3>
              <p class="text-xs text-white/40 mt-1">
                ${profile.storeName
                  ? `<span class="text-white/70 font-bold">${profile.storeName}</span> · Última sync: ${profile.lastSync ? new Date(profile.lastSync).toLocaleString('es-AR', {day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}) : 'Nunca'}`
                  : 'Conectá tu tienda para sincronizar ventas y stock automáticamente.'}
              </p>
            </div>
            ${profile.store ? `
              <button onclick="syncWithStore()" id="syncStoreBtn" class="flex items-center gap-2 px-4 py-2 bg-champagne/10 border border-champagne/20 text-champagne text-xs font-bold rounded-xl hover:bg-champagne/20 transition">
                <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i> Sincronizar ahora
              </button>
            ` : ''}
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-black/30 border border-white/5 rounded-2xl p-4 flex items-center justify-between hover:border-champagne/30 transition cursor-pointer group">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded-xl bg-[#96bf48]/10 flex items-center justify-center border border-[#96bf48]/20">
                  <i data-lucide="shopping-bag" class="w-5 h-5 text-[#96bf48]"></i>
                </div>
                <div>
                  <div class="text-xs font-bold text-white">Shopify</div>
                  <div class="text-[10px] ${profile.store==='shopify'?'neon-badge-green font-bold text-xs':'text-white/40'} font-mono">${profile.store==='shopify'?'Conectado':'Desconectado'}</div>
                </div>
              </div>
              <button onclick="connectStore('shopify')" class="text-[10px] font-bold ${profile.store==='shopify'?'bg-red-500/10 neon-badge-red font-bold text-xs hover:bg-red-500/20':'bg-white/5 text-white hover:bg-white/10 group-hover:bg-champagne group-hover:text-black'} px-3 py-1.5 rounded-lg transition">${profile.store==='shopify'?'Desconectar':'Conectar'}</button>
            </div>
            
            <div class="bg-black/30 border border-white/5 rounded-2xl p-4 flex items-center justify-between hover:border-champagne/30 transition cursor-pointer group">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
                  <i data-lucide="cloud" class="w-5 h-5 text-blue-400"></i>
                </div>
                <div>
                  <div class="text-xs font-bold text-white">TiendaNube</div>
                  <div class="text-[10px] ${profile.store==='tiendanube'?'neon-badge-green font-bold text-xs':'text-white/40'} font-mono">${profile.store==='tiendanube'?'Conectado':'Desconectado'}</div>
                </div>
              </div>
              <button onclick="connectStore('tiendanube')" class="text-[10px] font-bold ${profile.store==='tiendanube'?'bg-red-500/10 neon-badge-red font-bold text-xs hover:bg-red-500/20':'bg-white/5 text-white hover:bg-white/10 group-hover:bg-champagne group-hover:text-black'} px-3 py-1.5 rounded-lg transition">${profile.store==='tiendanube'?'Desconectar':'Conectar'}</button>
            </div>
          </div>
        </div>

        <!-- KPIs Financieros -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div class="glass-panel rounded-2xl p-5">
            <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Ingresos totales</div>
            <div class="text-2xl font-extrabold neon-badge-green font-bold text-xs mt-1">$${totalRevenue.toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-white/40 font-mono mt-1">${totalSold} unidades vendidas</div>
          </div>
          <div class="glass-panel rounded-2xl p-5">
            <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Ganancia Neta</div>
            <div class="text-2xl font-extrabold mt-1 ${totalProfit>=0?'neon-badge-green font-bold text-xs':'neon-badge-red font-bold text-xs'}">$${totalProfit.toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-white/40 font-mono mt-1">ROI: ${roi}%</div>
          </div>
          <div class="glass-panel rounded-2xl p-5">
            <div class="text-[9px] text-white/40 uppercase font-mono tracking-wider">Inversión Stock</div>
            <div class="text-2xl font-extrabold text-white mt-1">$${(totalInverted+totalAds).toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-white/40 font-mono mt-1">Stock + Publicidad</div>
          </div>
          <div class="glass-panel rounded-2xl p-5">
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
                      <td class="p-4 text-right font-mono neon-badge-green font-bold text-xs font-bold">${p.sold}</td>
                      <td class="p-4 text-right font-mono font-bold ${profit>=0?'neon-badge-green font-bold text-xs':'neon-badge-red font-bold text-xs'}">$${profit.toFixed(0)}</td>
                      <td class="p-4 text-right">
                        <div class="flex gap-2 justify-end">
                          <button onclick="quickSale(${i})" class="bg-green-600/10 hover:bg-green-600/20 neon-badge-green font-bold text-xs border border-green-500/20 px-2.5 py-1 rounded-lg text-[10px] font-bold">+1 Venta</button>
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
        <div class="glass-panel rounded-[2.5rem] w-full max-w-md overflow-hidden shadow-2xl p-8">
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
              ${idx !== undefined ? `<button onclick="deleteNegocioProduct(${idx})" class="py-3 px-4 border border-red-500/20 neon-badge-red font-bold text-xs rounded-xl hover:bg-red-500/10 transition">Eliminar</button>` : ''}
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

    function toast(msg, type='info', dur=3000) {
      const container = document.getElementById('toast-container');
      if(!container) return;
      const t = document.createElement('div');
      const typeClass = type === 'success' ? 'toast-success' : type === 'error' ? 'toast-error' : 'toast-info';
      const icon = type === 'success' ? '<i data-lucide="check-circle" class="w-4 h-4"></i>' : type === 'error' ? '<i data-lucide="alert-circle" class="w-4 h-4"></i>' : '<i data-lucide="info" class="w-4 h-4"></i>';
      t.className = `toast ${typeClass}`;
      t.innerHTML = `${icon} <span>${msg}</span>`;
      container.appendChild(t);
      if(window.lucide) window.lucide.createIcons();
      setTimeout(() => {
        t.classList.add('toast-out');
        setTimeout(() => t.remove(), 300);
      }, dur);
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
      
      const checkoutLink = "https://trendbase.lemonsqueezy.com/checkout/buy/a011b894-15b6-4913-918d-34676d498cba";
      const finalUrl = checkoutLink + "?checkout[email]=" + encodeURIComponent(user.email);
      
      // Mostrar un mensaje mientras redirige para mejor UX
      showToast('Redirigiendo a la pasarela de pago seguro...', 'success');
      
      setTimeout(() => {
        location.href = finalUrl;
      }, 1000);
    }

    // ── PRODUCTS DETAIL POPUP & SUPPLIERS ────────────────────────────────────
    // Remove duplicate let
    // currentProd is already defined globally
    function openProduct(idx) {
      currentProd = idx;
      const p = PRODUCTS[idx];
      if(!p) return;

      document.getElementById('pmTitle').textContent = p.name;
      document.getElementById('pmImgWrap').innerHTML = `<img src="${p.img || getProductImage(p.name)}" class="w-full h-full object-cover">`;
      document.getElementById('pmScore').textContent = p.score;
      document.getElementById('pmChange').textContent = p.change;
      document.getElementById('pmMargin').textContent = p.marginStr;
      document.getElementById('pmCat').textContent = p.cat;
      document.getElementById('pmPrice').textContent = p.priceStr;
      
      const compBadge = document.getElementById('pmComp');
      compBadge.textContent = p.comp;
      const compColor = p.comp === 'Baja' ? 'bg-green-500/10 neon-badge-green font-bold text-xs border-green-500/20' : p.comp === 'Alta' ? 'bg-red-500/10 neon-badge-red font-bold text-xs border-red-500/20' : 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
      compBadge.className = `text-xs font-bold font-mono px-2 py-0.5 rounded border uppercase ${compColor}`;

      const pmTag = document.getElementById('pmTag');
      pmTag.textContent = p.hot ? 'HOT' : 'TENDENCIA';
      pmTag.className = `text-xs font-mono font-bold px-2 py-0.5 rounded uppercase ${p.hot ? 'bg-champagne text-obsidian' : 'bg-white/10 text-white'}`;

      document.getElementById('pmPlats').innerHTML = p.plts.map(pl => `<span class="px-2 py-0.5 rounded bg-white/5 border border-white/10 text-[9px] font-mono font-bold">${PLT[pl] ? PLT[pl].label : pl}</span>`).join('');
      document.getElementById('pmCountries').innerHTML = (p.regions || []).map(r => `<span class="px-2 py-0.5 rounded bg-white/5 border border-white/10 text-[9px] font-mono font-bold">${r==='AR'?'🇦🇷 AR':r==='UY'?'🇺🇾 UY':'🇨🇱 CL'}</span>`).join('');
      
      // Dynamic Sell-On logic based on regions
      let sellOnHTML = `<a href="https://www.shopify.com/?ref=trendbase" target="_blank" class="px-2 py-0.5 rounded bg-champagne/10 border border-champagne/20 text-champagne text-[9px] font-bold hover:-translate-y-0.5 transition inline-block"><i data-lucide="shopping-cart" class="w-3 h-3 inline-block mr-1"></i> Shopify</a>`;
      sellOnHTML += ` <a href="https://www.tiendanube.com/?ref=trendbase" target="_blank" class="px-2 py-0.5 rounded bg-blue-500/10 border border-blue-500/20 text-blue-400 text-[9px] font-bold hover:-translate-y-0.5 transition inline-block"><i data-lucide="cloud" class="w-3 h-3 inline-block mr-1"></i> TiendaNube</a>`;
      if (p.regions && p.regions.includes('AR')) sellOnHTML += ` <a href="https://listado.mercadolibre.com.ar/${encodeURIComponent(p.name)}" target="_blank" class="px-2 py-0.5 rounded bg-yellow-500/10 border border-yellow-500/20 text-yellow-500 text-[9px] font-bold hover:-translate-y-0.5 transition inline-block">Mercado Libre AR</a>`;
      if (p.regions && p.regions.includes('CL')) {
        sellOnHTML += ` <a href="https://listado.mercadolibre.cl/${encodeURIComponent(p.name)}" target="_blank" class="px-2 py-0.5 rounded bg-yellow-500/10 border border-yellow-500/20 text-yellow-500 text-[9px] font-bold hover:-translate-y-0.5 transition inline-block">Mercado Libre CL</a>`;
        sellOnHTML += ` <a href="https://www.falabella.com/falabella-cl/search?Ntt=${encodeURIComponent(p.name)}" target="_blank" class="px-2 py-0.5 rounded bg-green-500/10 border border-green-500/20 text-green-500 text-[9px] font-bold hover:-translate-y-0.5 transition inline-block">Falabella</a>`;
      }
      if (p.regions && p.regions.includes('UY')) sellOnHTML += ` <a href="https://listado.mercadolibre.com.uy/${encodeURIComponent(p.name)}" target="_blank" class="px-2 py-0.5 rounded bg-yellow-500/10 border border-yellow-500/20 text-yellow-500 text-[9px] font-bold hover:-translate-y-0.5 transition inline-block">Mercado Libre UY</a>`;
      if (p.plts && p.plts.includes('AM')) sellOnHTML += ` <a href="https://www.amazon.com/s?k=${encodeURIComponent(p.name)}" target="_blank" class="px-2 py-0.5 rounded bg-white/10 border border-white/20 text-white text-[9px] font-bold hover:-translate-y-0.5 transition inline-block">Amazon</a>`;
      
      document.getElementById('pmSellOn').innerHTML = sellOnHTML;
      lucide.createIcons();
      
      renderSuppliersTab(p, document.getElementById('pmSuppliers'));
      
      document.getElementById('pmSaveBtn').innerHTML = saved.includes(idx) ? '<i data-lucide="bookmark-check" class="w-4 h-4 inline-block mr-1"></i> Guardado' : '<i data-lucide="bookmark" class="w-4 h-4 inline-block mr-1"></i> Guardar';
      
      switchModalTab('info', document.querySelector('.modal-tab'));
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
        el.innerHTML = '<div class="text-center py-12 text-white/40 text-xs font-mono">No tenés productos guardados todavía. Empieza a buscar en Tendencias.</div>';
        return;
      }

      // --- KANBAN LOGIC (MOCKED FOR DEMO) ---
      const cols = [
        { id: 'to-test', title: '📌 Por Testear', items: [] },
        { id: 'testing', title: '🧪 Testeando', items: [] },
        { id: 'winner', title: '🔥 Ganador (Escalando)', items: [] },
        { id: 'discarded', title: '🗑️ Descartado', items: [] }
      ];

      saved.forEach(idx => {
        const p = ALL_PRODUCTS[idx];
        if(p) {
          // Fake status distribution based on product index
          const statusIdx = idx % 4;
          cols[statusIdx].items.push({ idx, p });
        }
      });

      el.innerHTML = `
        <div class="flex overflow-x-auto gap-4 pb-4 snap-x">
          ${cols.map(col => `
            <div class="min-w-[260px] w-[260px] flex-shrink-0 flex flex-col gap-3 snap-start">
              <div class="flex justify-between items-center text-white font-bold text-xs bg-white/5 p-3 rounded-xl border border-white/10">
                <span>${col.title}</span>
                <span class="bg-black/50 text-white/50 px-2 py-0.5 rounded-full text-[10px]">${col.items.length}</span>
              </div>
              <div class="flex flex-col gap-3 min-h-[500px]">
                ${col.items.map(item => `
                  <div onclick="openProduct(${item.idx})" class="glass-panel rounded-2xl overflow-hidden hover-lift p-3 space-y-3 cursor-pointer group">
                    <div class="aspect-video w-full rounded-xl overflow-hidden bg-black/20 relative">
                      <img src="${item.p.img || getProductImage(item.p.name)}" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition">
                      <span class="absolute top-2 left-2 text-[8px] font-mono font-bold uppercase bg-champagne text-obsidian px-1.5 py-0.5 rounded">${item.p.cat}</span>
                    </div>
                    <div>
                      <h4 class="text-xs font-bold text-white leading-tight mb-2">${item.p.name}</h4>
                      <div class="flex justify-between items-center text-[9px] text-white/50 border-t border-white/5 pt-2">
                        <span>Margen: <b class="neon-badge-green font-bold text-xs font-mono">${item.p.marginStr}</b></span>
                        <span>Comp: <b class="text-white font-mono">${item.p.comp}</b></span>
                      </div>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          `).join('')}
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
        const changeClass = diff >= 0 ? 'neon-badge-green font-bold text-xs' : 'neon-badge-red font-bold text-xs';
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
      { name:'AliExpress', icon:'🛒', url:'https://www.aliexpress.com/wholesale?SearchText=', ship:'10-25 días · Envío gratis', note:'El más popular para dropshipping', color:'#FF4747', aff:'&af=trendbase' },
      { name:'Alibaba', icon:'🏭', url:'https://www.alibaba.com/trade/search?SearchText=', ship:'20-35 días · Mayorista', note:'Precios más bajos, mínimo por lote', color:'#FF6A00', aff:'' },
      { name:'CJ Dropshipping', icon:'🚀', url:'https://cjdropshipping.com/list.html?searchKey=', ship:'7-12 días · Bodega LATAM', note:'Bodega en Brasil y México', color:'#00A87E', aff:'' },
      { name:'Dropdeal', icon:'📦', url:'https://dropdeal.com/search?q=', ship:'5-10 días · Envío LATAM', note:'Especializado en Latinoamérica', color:'#8b5cf6', aff:'&ref=trendbase' },
      { name:'Droppi', icon:'🇨🇴', url:'https://droppi.com/search?q=', ship:'2-5 días · Contra Entrega', note:'Pago Contra Entrega en Colombia', color:'#f59e0b', aff:'&ref=trendbase' },
      { name:'Rocketfy', icon:'🚀', url:'https://rocketfy.co/search?q=', ship:'3-6 días · Nacional', note:'Envíos Nacionales en LATAM', color:'#ec4899', aff:'&ref=trendbase' },
      { name:'TiendaMia', icon:'🌎', url:'https://tiendamia.com/search?q=', ship:'10-15 días · Importación', note:'Importación fácil sin trámites', color:'#3b82f6', aff:'&ref=trendbase' },
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
                <a href="${s.url + q + (s.aff || '')}" target="_blank" class="glass-btn rounded-xl transition rounded-2xl p-4 flex flex-col justify-between transition duration-200 hover:-translate-y-1">
                  <div>
                    <div class="text-sm font-bold text-white mb-1">${s.icon} ${s.name}</div>
                    <div class="text-[8px] font-mono text-white/40 mb-2">${s.ship}</div>
                    <div class="text-[9px] text-white/60 leading-relaxed">${s.note}</div>
                  </div>
                  <div class="text-xs font-extrabold neon-badge-green font-bold text-xs font-mono mt-4">~USD ${estPrice}</div>
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
      msgs.innerHTML += `<div id="typing" class="p-3 glass-panel rounded-2xl flex items-center gap-1 self-start"><span class="w-1.5 h-1.5 rounded-full bg-white/30 animate-bounce"></span><span class="w-1.5 h-1.5 rounded-full bg-white/30 animate-bounce" style="animation-delay: 0.2s"></span><span class="w-1.5 h-1.5 rounded-full bg-white/30 animate-bounce" style="animation-delay: 0.4s"></span></div>`;
      msgs.scrollTop = msgs.scrollHeight;
      
      aiHistory.push({ role:'user', content:text });
      try {
        const res = await fetch('/api/chat', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ messages: aiHistory, system: AI_SYS })
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
          typingEl.outerHTML = `<div class="msg msg-ai neon-badge-red font-bold text-xs bg-red-500/10 border border-red-500/20 p-3 rounded-2xl max-w-[85%] self-start">⚠️ ${e.message}</div>`;
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
      }catch(e){aiHistory.pop();document.getElementById('typing').outerHTML='<div class="msg msg-ai bg-red-500/10 neon-badge-red font-bold text-xs p-3 rounded-2xl max-w-[85%] self-start border border-red-500/20">\u26A0\uFE0F '+e.message+'</div>';}
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
            (p.commission ? '<span class="bg-green-500/20 neon-badge-green font-bold text-xs px-1.5 py-0.5 rounded font-mono font-bold mr-1">'+p.commission+'% comisión</span>' : '') +
            (p.rating ? '⭐ '+p.rating+'%' : '') + '</div>';
            
          const price = document.createElement('div');
          price.className = 'font-mono font-bold neon-badge-green font-bold text-xs shrink-0';
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

    // ── DEMO VIDEO ───────────────────────────────────────────────────────────
    function playDemoVideo() {
      const poster = document.getElementById('videoPoster');
      const video = document.getElementById('demoVideo');
      if (!poster || !video) return;
      poster.style.transition = 'opacity 0.5s';
      poster.style.opacity = '0';
      setTimeout(() => {
        poster.style.display = 'none';
        video.style.display = 'block';
        if(typeof video.play === 'function') video.play();
      }, 500);
    }

    // Listen for CTA messages from the demo player iframe
    window.addEventListener('message', e => {
      if (e.data === 'signup') openAuth('signup');
      if (e.data === 'dashboard') enterDash();
    });

    // ── STORE SYNC ───────────────────────────────────────────────────────────

    async function syncWithStore() {
      const profile = getProfile();
      if (!profile.store || !profile.storeCredentials) return;

      const btn = document.getElementById('syncStoreBtn');
      if (btn) { btn.disabled = true; btn.innerHTML = '<i data-lucide="loader" class="w-3.5 h-3.5 animate-spin inline-block mr-1"></i> Sincronizando…'; lucide.createIcons(); }

      try {
        const res = await fetch('/api/store-sync', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            platform: profile.store,
            credentials: profile.storeCredentials,
            action: 'sync',
            sinceId: profile.lastOrderId || null,
          }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Error al sincronizar');

        // --- Actualizar Mi Negocio con datos reales ---
        const negProducts = getNegocioProducts();
        const newNotifs = [];

        // Map store products to tb_negocio by fuzzy name match
        (data.products || []).forEach(sp => {
          const match = negProducts.find(np =>
            np.name.toLowerCase().includes(sp.name.toLowerCase().slice(0, 8)) ||
            sp.name.toLowerCase().includes(np.name.toLowerCase().slice(0, 8))
          );
          if (match) {
            const prevStock = match.stock - match.sold;
            match.stock = sp.stock + match.sold; // total = actual disponible + vendido hasta ahora
            const newAvailable = sp.stock;
            // Low stock alert
            if (newAvailable <= 5 && newAvailable < prevStock) {
              newNotifs.push({
                id: Date.now() + Math.random(),
                type: 'low_stock',
                icon: '⚠️',
                msg: `Stock bajo: <strong>${match.name}</strong> tiene solo ${newAvailable} unidad${newAvailable !== 1 ? 'es' : ''}`,
                ts: new Date().toISOString(),
                read: false,
              });
            }
          }
        });

        // Map new orders → update sold count
        const prevOrderId = profile.lastOrderId;
        const newOrders = prevOrderId
          ? (data.orders || []).filter(o => o.id !== prevOrderId)
          : (data.orders || []);

        newOrders.forEach(order => {
          (order.items || []).forEach(item => {
            const match = negProducts.find(np =>
              np.name.toLowerCase().includes(item.name.toLowerCase().slice(0, 8)) ||
              item.name.toLowerCase().includes(np.name.toLowerCase().slice(0, 8))
            );
            if (match) {
              match.sold = (match.sold || 0) + item.qty;
            }
          });
        });

        if (newOrders.length > 0) {
          const total = newOrders.reduce((s, o) => s + o.total, 0);
          newNotifs.push({
            id: Date.now() + Math.random(),
            type: 'new_orders',
            icon: '🛒',
            msg: `${newOrders.length} pedido${newOrders.length !== 1 ? 's' : ''} nuevo${newOrders.length !== 1 ? 's' : ''} — <strong>$${Math.round(total).toLocaleString()}</strong> en ventas`,
            ts: new Date().toISOString(),
            read: false,
          });
        }

        // Check TrendBase products for trending matches
        if (PRODUCTS && PRODUCTS.length) {
          const userCats = [...new Set(negProducts.map(p => p.cat).filter(Boolean))];
          const matchingTrend = PRODUCTS.find(tp =>
            tp.score >= 85 && tp.hot &&
            !negProducts.some(np => np.name.toLowerCase().includes(tp.name.toLowerCase().slice(0, 6)))
          );
          if (matchingTrend) {
            newNotifs.push({
              id: Date.now() + Math.random(),
              type: 'trending',
              icon: '✨',
              msg: `Nuevo trending: <strong>${matchingTrend.name}</strong> (Score ${matchingTrend.score}) — podría ser tu próximo producto`,
              ts: new Date().toISOString(),
              read: false,
            });
          }
        }

        saveNegocioProducts(negProducts);

        // Save sync state
        profile.lastSync = new Date().toISOString();
        if (data.lastOrderId) profile.lastOrderId = data.lastOrderId;
        saveProfile(profile);

        // Push notifications
        if (newNotifs.length) {
          pushNotifications(newNotifs);
        }

        renderNegocio();
        if (newOrders.length > 0) {
          toast(`Sync completo: ${newOrders.length} pedido${newOrders.length !== 1 ? 's' : ''} nuevo${newOrders.length !== 1 ? 's' : ''}`, 'success');
        } else {
          toast('Sincronización completada — todo al día', 'success', 2500);
        }

      } catch (err) {
        toast('Error al sincronizar: ' + err.message, 'error');
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '<i data-lucide="refresh-cw" class="w-3.5 h-3.5 inline-block mr-1"></i> Sincronizar ahora';
          lucide.createIcons();
        }
      }
    }

    // Auto-sync cada 30 minutos si hay tienda conectada
    setInterval(() => {
      const profile = getProfile();
      if (profile.store && profile.storeCredentials) syncWithStore();
    }, 30 * 60 * 1000);

    // ── NOTIFICATIONS ────────────────────────────────────────────────────────

    function getNotifications() {
      try { return JSON.parse(localStorage.getItem('tb_notifs') || '[]'); } catch { return []; }
    }
    function saveNotifications(arr) {
      // Keep max 50
      try { localStorage.setItem('tb_notifs', JSON.stringify(arr.slice(0, 50))); } catch {}
    }

    function pushNotifications(newNotifs) {
      const existing = getNotifications();
      const merged = [...newNotifs, ...existing];
      saveNotifications(merged);
      renderNotifBell();
    }

    function renderNotifBell() {
      const bell = document.getElementById('notifBell');
      const badge = document.getElementById('notifBadge');
      if (!bell) return;
      const notifs = getNotifications();
      const unread = notifs.filter(n => !n.read).length;
      bell.classList.remove('hidden');
      if (unread > 0) {
        badge.textContent = unread > 9 ? '9+' : unread;
        badge.classList.remove('hidden');
      } else {
        badge.classList.add('hidden');
      }
      renderNotifList();
    }

    function renderNotifList() {
      const list = document.getElementById('notifList');
      if (!list) return;
      const notifs = getNotifications();
      if (!notifs.length) {
        list.innerHTML = '<div class="px-4 py-6 text-center text-white/30 text-xs">Sin notificaciones</div>';
        return;
      }
      list.innerHTML = notifs.map(n => `
        <div class="px-4 py-3 flex gap-3 items-start hover:bg-white/5 transition cursor-default ${n.read ? 'opacity-50' : ''}">
          <span class="text-base leading-none mt-0.5">${n.icon || '🔔'}</span>
          <div class="flex-1 min-w-0">
            <p class="text-xs text-white leading-snug" style="overflow-wrap:break-word">${n.msg}</p>
            <p class="text-[10px] text-white/30 font-mono mt-1">${new Date(n.ts).toLocaleString('es-AR', {day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'})}</p>
          </div>
          ${!n.read ? '<span class="w-1.5 h-1.5 rounded-full bg-champagne mt-1.5 flex-shrink-0"></span>' : ''}
        </div>
      `).join('');
    }

    function toggleNotifPanel() {
      const panel = document.getElementById('notifPanel');
      if (!panel) return;
      panel.classList.toggle('hidden');
      if (!panel.classList.contains('hidden')) {
        renderNotifList();
        // Close dropdown if open
        document.getElementById('userDD')?.classList.add('hidden');
      }
    }

    function markAllRead() {
      const notifs = getNotifications().map(n => ({ ...n, read: true }));
      saveNotifications(notifs);
      renderNotifBell();
    }

    // Close notif panel when clicking outside
    document.addEventListener('click', e => {
      const bell = document.getElementById('notifBell');
      if (bell && !bell.contains(e.target)) {
        document.getElementById('notifPanel')?.classList.add('hidden');
      }
    });

    // Run app engine init
    init();

    // Init notifications on load
    setTimeout(renderNotifBell, 1000);

    // --- MISSING UI FUNCTIONS ---
    function toggleMobileMenu() {
      const menu = document.getElementById('mobileMenuDrawer');
      if(menu) {
        if(menu.classList.contains('hidden')) {
          menu.classList.remove('hidden');
        } else {
          menu.classList.hidden = true;
          menu.classList.add('hidden');
        }
      }
    }

    function scrollToPlans() {
      const planSection = document.getElementById('pricing');
      if(planSection) {
        planSection.scrollIntoView({ behavior: 'smooth' });
      }
    }

    function showUpgrade() {
      toast('¡Función Premium! Mejorá tu plan para acceder.', 'warning');
      scrollToPlans();
    }

    // --- MARKETING TAB FUNCTIONS ---
    function generateMarketingCopy() {
      const elContent = document.getElementById('mkt-content');
      const elLoading = document.getElementById('mkt-loading');
      const elBtn = document.getElementById('mktGenerateBtn');
      if(typeof PRODUCTS === 'undefined' || typeof currentProd === 'undefined') return;
      const p = PRODUCTS[currentProd];
      if(!p) return;

      if(elContent) elContent.classList.add('hidden');
      if(elLoading) elLoading.classList.remove('hidden');
      if(elBtn) elBtn.disabled = true;

      // Simulamos la llamada a la IA de Anthropic para generar el copy
      setTimeout(() => {
        if(elLoading) elLoading.classList.add('hidden');
        if(elContent) elContent.classList.remove('hidden');
        if(elBtn) elBtn.disabled = false;
        
        const elTitulo = document.getElementById('mkt-ml-titulo');
        const elDesc = document.getElementById('mkt-ml-desc');
        const elPrecio = document.getElementById('mkt-precio');
        const elDif = document.getElementById('mkt-diferencial');
        const elTiktok = document.getElementById('mkt-tiktok');
        const elIg = document.getElementById('mkt-instagram');
        const elKw = document.getElementById('mkt-keywords');

        if(elTitulo) elTitulo.innerText = `${p.name} - Calidad Premium Envío Rápido`;
        if(elDesc) elDesc.innerText = `Descubre por qué miles de clientes en LATAM eligen nuestro ${p.name}. Diseñado para brindar la máxima satisfacción y durabilidad. ¡Compra ahora con descuento!`;
        if(elPrecio) elPrecio.innerText = `Precio sugerido: ${p.priceStr || '$20'}`;
        if(elDif) elDif.innerText = `Margen: ${p.marginStr || (p.margin+'%')}`;
        
        if(elTiktok) elTiktok.innerText = `✨ ¿Buscando el mejor ${p.name}? ✨\n\nNo busques más. La solución definitiva ya está aquí.\n\n👉 Click en el link de nuestro perfil y llévatelo HOY mismo. #tendencia #viral`;
        if(elIg) elIg.innerText = `Eleva tu estilo de vida con nuestro nuevo ${p.name}. Calidad garantizada que se adapta a ti. 🌟\n\nConsíguelo con envío a todo el país.\nLink en bio 🛒`;
        if(elKw) elKw.innerHTML = `<span class="bg-white/10 px-2 py-1 rounded text-xs">#${p.name.replace(/\s+/g,'').toLowerCase()}</span> <span class="bg-white/10 px-2 py-1 rounded text-xs">#viral</span> <span class="bg-white/10 px-2 py-1 rounded text-xs">#oferta</span>`;

      }, 1500);
    }

    function clearMarketingCache() {
      const elContent = document.getElementById('mkt-content');
      if(elContent) elContent.classList.add('hidden');
      toast('Caché limpiado. Generá de nuevo.', 'info');
    }

    function copyMktSection(id1, id2) {
      const el1 = document.getElementById('mkt-' + id1);
      const el2 = document.getElementById('mkt-' + id2);
      if(!el1 || !el2) return;
      const text = el1.innerText + '\n' + el2.innerText;
      navigator.clipboard.writeText(text);
      toast('¡Copiado al portapapeles!', 'success');
    }

    function copyMktField(id) {
      const el = document.getElementById(id);
      if(!el) return;
      navigator.clipboard.writeText(el.innerText);
      toast('¡Copiado al portapapeles!', 'success');
    }


  