import re

def rebuild_home():
    with open('index.html', 'r') as f:
        content = f.read()

    custom_css = """
  <style id="premium-apple-theme">
    /* Exact Colors from Mockup */
    :root {
      --aw-bg: #E8DFD5;
      --aw-card: #F3EFEA;
      --aw-text-main: #2D2B29;
      --aw-text-muted: #7A7571;
      --aw-green: #4A8B5D;
      --aw-red: #B95252;
      --aw-shadow: 0 24px 48px rgba(160, 150, 140, 0.25), 0 2px 6px rgba(160, 150, 140, 0.1), inset 0 1px 2px rgba(255, 255, 255, 0.9);
      --aw-shadow-hover: 0 32px 64px rgba(160, 150, 140, 0.3), 0 4px 12px rgba(160, 150, 140, 0.15), inset 0 1px 2px rgba(255, 255, 255, 1);
      --aw-btn-primary: #1C1C1E;
      --aw-btn-primary-text: #F5F5F7;
    }
    
    /* Base Body overrides */
    body {
      background-color: var(--aw-bg) !important;
      color: var(--aw-text-main) !important;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
      letter-spacing: -0.015em;
    }
    
    /* Glassmorphism Cards (Apple Widget style) */
    .aw-card {
      background-color: rgba(243, 239, 234, 0.6) !important;
      border-radius: 40px !important;
      box-shadow: var(--aw-shadow) !important;
      border: 1px solid rgba(255, 255, 255, 0.5) !important;
      backdrop-filter: blur(30px) !important;
      -webkit-backdrop-filter: blur(30px) !important;
      transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
      color: var(--aw-text-main) !important;
      overflow: hidden;
    }
    
    .aw-card:hover {
      box-shadow: var(--aw-shadow-hover) !important;
      transform: translateY(-4px) !important;
    }
    
    /* Buttons */
    .aw-btn-primary {
      background: linear-gradient(180deg, #3A3A3C 0%, #1C1C1E 100%) !important;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1), inset 0 1px 1px rgba(255,255,255,0.2) !important;
      color: var(--aw-btn-primary-text) !important;
      border-radius: 999px !important;
      font-weight: 600 !important;
      transition: all 0.3s ease !important;
    }
    .aw-btn-primary:hover {
      transform: scale(1.02) !important;
      box-shadow: 0 8px 24px rgba(0,0,0,0.15), inset 0 1px 1px rgba(255,255,255,0.3) !important;
    }
    
    /* Text Utilities */
    .text-title { color: var(--aw-text-main); letter-spacing: -0.03em; font-weight: 800; }
    .text-subtitle { color: var(--aw-text-muted); letter-spacing: -0.01em; font-weight: 500; }
    .aw-text-green { color: var(--aw-green) !important; }
    .aw-text-red { color: var(--aw-red) !important; }
    .aw-badge-green { background: rgba(74, 139, 93, 0.1); color: var(--aw-green); padding: 4px 12px; border-radius: 999px; font-weight: 700; font-size: 0.75rem; }
    
    /* Radial Background Glows */
    .bg-glow-1 {
      position: absolute; top: -10%; left: 50%; transform: translateX(-50%);
      width: 80vw; height: 80vw; background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%);
      z-index: -1; pointer-events: none;
    }
  </style>
"""
    # Inject Custom CSS
    if 'premium-apple-theme' not in content:
        content = content.replace('</head>', custom_css + '\n</head>')

    # Global Body Classes
    content = re.sub(r'<body class="[^"]*">', '<body class="bg-[#E8DFD5] text-[#2D2B29] antialiased overflow-x-hidden">', content)

    # Completely New Landing Page HTML
    new_landing = """
  <!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->
  <div id="view-landing" class="app-view active-view relative w-full min-h-screen">
    
    <!-- Background Glow -->
    <div class="bg-glow-1"></div>

    <!-- Floating Navbar -->
    <nav class="fixed top-6 left-1/2 -translate-x-1/2 w-[90%] max-w-5xl z-50">
      <div class="aw-card px-8 py-4 flex items-center justify-between !rounded-full">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-stone-200 to-stone-400 flex items-center justify-center shadow-inner">
            <i data-lucide="zap" class="w-4 h-4 text-white"></i>
          </div>
          <span class="font-extrabold tracking-tight text-lg">TrendBase</span>
        </div>
        <div class="hidden md:flex items-center gap-8 text-sm font-semibold text-[#7A7571]">
          <a href="#features" class="hover:text-[#2D2B29] transition">Features</a>
          <a href="#bento" class="hover:text-[#2D2B29] transition">How it Works</a>
          <a href="#pricing" class="hover:text-[#2D2B29] transition">Pricing</a>
        </div>
        <div class="flex items-center gap-4">
          <button onclick="openAuth('login')" class="text-sm font-semibold text-[#2D2B29] hover:opacity-70 transition">Sign In</button>
          <button onclick="openAuth('signup')" class="aw-btn-primary px-6 py-2.5 text-sm">Get Started</button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-48 pb-20 px-6 flex flex-col items-center justify-center text-center relative z-10">
      <div class="aw-badge-green mb-8 inline-flex items-center gap-2">
        <span class="relative flex h-2 w-2">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" style="background-color: var(--aw-green)"></span>
          <span class="relative inline-flex rounded-full h-2 w-2" style="background-color: var(--aw-green)"></span>
        </span>
        TrendBase 2.0 is now live
      </div>
      
      <h1 class="text-title text-6xl md:text-8xl max-w-4xl mx-auto leading-[0.95] mb-8">
        The ultimate <br/><span class="text-transparent bg-clip-text bg-gradient-to-r from-[#2D2B29] to-[#7A7571]">business command</span>
      </h1>
      
      <p class="text-subtitle text-xl md:text-2xl max-w-2xl mx-auto mb-12">
        Experience a beautiful, widget-driven dashboard that brings all your e-commerce data into one elegant workspace.
      </p>
      
      <div class="flex flex-col sm:flex-row items-center gap-4">
        <button onclick="openAuth('signup')" class="aw-btn-primary px-8 py-4 text-lg w-full sm:w-auto">Start Free Trial</button>
        <button onclick="document.getElementById('demo-video').scrollIntoView({behavior:'smooth'})" class="aw-card !rounded-full px-8 py-4 text-lg font-semibold flex items-center justify-center gap-2 w-full sm:w-auto hover:bg-white/40">
          <i data-lucide="play-circle" class="w-5 h-5"></i> Watch Demo
        </button>
      </div>
    </section>

    <!-- Bento Box Widget Showcase -->
    <section id="bento" class="py-20 px-6 max-w-7xl mx-auto relative z-10">
      <div class="grid grid-cols-1 md:grid-cols-3 md:grid-rows-2 gap-6 h-auto md:h-[600px]">
        
        <!-- Large Widget (Spans 2 cols) -->
        <div class="aw-card md:col-span-2 md:row-span-2 p-10 flex flex-col justify-between relative overflow-hidden group">
          <div class="relative z-10">
            <h3 class="text-2xl font-bold tracking-tight mb-2">Performance Summary</h3>
            <p class="text-[#7A7571] font-medium max-w-sm">Monitor your total revenue, net profit, and active users in real-time with striking clarity.</p>
          </div>
          <div class="mt-12 grid grid-cols-2 gap-6 relative z-10">
            <div>
              <div class="text-xs text-[#7A7571] uppercase font-bold tracking-widest mb-1">Total Revenue</div>
              <div class="flex items-end gap-3">
                <div class="text-5xl font-extrabold tracking-tighter">$87,450</div>
                <div class="aw-text-green font-bold text-sm mb-1 flex items-center"><i data-lucide="arrow-up-right" class="w-4 h-4"></i> 12.4%</div>
              </div>
            </div>
            <div>
              <div class="text-xs text-[#7A7571] uppercase font-bold tracking-widest mb-1">Net Profit</div>
              <div class="flex items-end gap-3">
                <div class="text-5xl font-extrabold tracking-tighter">$14,210</div>
                <div class="aw-text-green font-bold text-sm mb-1 flex items-center"><i data-lucide="arrow-up-right" class="w-4 h-4"></i> 8.2%</div>
              </div>
            </div>
          </div>
          <!-- Decorative Background Element -->
          <div class="absolute -bottom-20 -right-20 w-96 h-96 bg-gradient-to-tr from-white/40 to-transparent rounded-full blur-3xl group-hover:scale-110 transition duration-1000"></div>
        </div>
        
        <!-- Small Widget 1 -->
        <div class="aw-card p-8 flex flex-col justify-between">
          <div>
            <h3 class="text-lg font-bold tracking-tight mb-1">Project Pulse</h3>
            <p class="text-[#7A7571] text-sm font-medium">84% Complete</p>
          </div>
          <div class="mt-6">
            <div class="w-full h-3 bg-black/5 rounded-full overflow-hidden flex">
              <div class="h-full bg-[#2D2B29]" style="width: 40%"></div>
              <div class="h-full bg-[#7A7571] ml-1" style="width: 20%"></div>
              <div class="h-full bg-[#A3A09E] ml-1" style="width: 24%"></div>
            </div>
            <div class="flex justify-between text-xs text-[#7A7571] font-mono mt-2">
              <span>|</span><span>80%</span>
            </div>
          </div>
        </div>
        
        <!-- Small Widget 2 -->
        <div class="aw-card p-8 flex flex-col justify-between">
          <div>
            <h3 class="text-lg font-bold tracking-tight mb-1">Client Health</h3>
            <p class="text-[#7A7571] text-sm font-medium">System Status</p>
          </div>
          <div class="mt-6 flex items-center gap-3">
            <div class="w-12 h-12 rounded-full bg-[rgba(74,139,93,0.1)] flex items-center justify-center">
              <i data-lucide="check" class="w-6 h-6 aw-text-green"></i>
            </div>
            <span class="text-2xl font-bold tracking-tight">Healthy</span>
          </div>
        </div>

      </div>
    </section>

    <!-- Detailed Features -->
    <section id="features" class="py-24 px-6 max-w-5xl mx-auto relative z-10 text-center">
      <h2 class="text-title text-4xl md:text-5xl mb-16">Elegance in every detail.</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
        <div class="aw-card p-8 !rounded-[32px]">
          <div class="w-12 h-12 rounded-2xl bg-white/60 shadow-sm flex items-center justify-center mb-6">
            <i data-lucide="layout-grid" class="w-6 h-6 text-[#2D2B29]"></i>
          </div>
          <h4 class="text-xl font-bold mb-3">Widgets Redefined</h4>
          <p class="text-[#7A7571] leading-relaxed">Experience a workspace built with pure glassmorphism, perfectly rounded squircles, and incredibly soft lighting.</p>
        </div>
        
        <div class="aw-card p-8 !rounded-[32px]">
          <div class="w-12 h-12 rounded-2xl bg-white/60 shadow-sm flex items-center justify-center mb-6">
            <i data-lucide="activity" class="w-6 h-6 text-[#2D2B29]"></i>
          </div>
          <h4 class="text-xl font-bold mb-3">Live Metrics</h4>
          <p class="text-[#7A7571] leading-relaxed">Track every dollar with crisp, ultra-legible typography. Bright functional colors are used precisely to highlight what matters.</p>
        </div>
        
        <div class="aw-card p-8 !rounded-[32px]">
          <div class="w-12 h-12 rounded-2xl bg-white/60 shadow-sm flex items-center justify-center mb-6">
            <i data-lucide="lock" class="w-6 h-6 text-[#2D2B29]"></i>
          </div>
          <h4 class="text-xl font-bold mb-3">Bank-Grade Security</h4>
          <p class="text-[#7A7571] leading-relaxed">Your data is yours. Protected by enterprise-level encryption while looking completely effortless.</p>
        </div>
      </div>
    </section>

    <!-- Minimalist Footer -->
    <footer class="py-12 border-t border-[#DED7CF] mt-20 relative z-10">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-2 opacity-50">
          <i data-lucide="zap" class="w-4 h-4"></i>
          <span class="font-bold">TrendBase</span>
        </div>
        <p class="text-sm text-[#7A7571]">© 2026 TrendBase Inc. Designed with precision.</p>
        <div class="flex gap-4">
          <a href="#" class="text-[#7A7571] hover:text-[#2D2B29] transition"><i data-lucide="twitter" class="w-5 h-5"></i></a>
          <a href="#" class="text-[#7A7571] hover:text-[#2D2B29] transition"><i data-lucide="instagram" class="w-5 h-5"></i></a>
        </div>
      </div>
    </footer>
  </div>
"""

    # Extract boundaries
    start_str = "  <!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->"
    end_str = "  <!-- ─── APP VIEW: DASHBOARD ─────────────────────────────────────────────── -->"
    
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx] + new_landing + "\n" + content[end_idx:]
        
        # We also need to fix the dashboard rendering using our aw-* classes so it matches!
        # First, we just write the HTML. The python script will replace Tailwind with aw-* globally
        with open('index.html', 'w') as f:
            f.write(new_content)
        print("Landing page completely rebuilt.")
    else:
        print("Could not find boundaries for Landing Page.")

rebuild_home()
