import re

def update_dashboard():
    with open('index.html', 'r') as f:
        content = f.read()

    new_html = """      el.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <!-- Card 1: Performance Summary -->
          <div class="bg-white/70 backdrop-blur-xl border border-white shadow-[0_8px_30px_rgb(0,0,0,0.06)] rounded-[32px] p-6 flex flex-col justify-between min-h-[220px]">
            <h3 class="text-sm font-bold text-stone-800">Performance Summary</h3>
            <div class="mt-4 space-y-4">
              <div>
                <div class="text-[10px] text-stone-500 uppercase font-mono mb-1">Total Revenue</div>
                <div class="flex items-baseline gap-3">
                  <div class="text-3xl font-extrabold text-stone-900 tracking-tight">$${totalRevenue.toLocaleString()}</div>
                  <div class="text-xs font-bold text-green-600 flex items-center"><i data-lucide="arrow-up-right" class="w-3 h-3"></i> +12.4%</div>
                </div>
              </div>
              <div>
                <div class="text-[10px] text-stone-500 uppercase font-mono mb-1">New MRR</div>
                <div class="flex items-baseline gap-3">
                  <div class="text-3xl font-extrabold text-stone-900 tracking-tight">$${totalProfit.toLocaleString()}</div>
                  <div class="text-xs font-bold ${totalProfit>=0?'text-green-600':'text-red-600'} flex items-center"><i data-lucide="${totalProfit>=0?'arrow-up-right':'arrow-down-right'}" class="w-3 h-3"></i> ROI ${roi}%</div>
                </div>
              </div>
              <div class="flex items-end justify-between">
                <div>
                  <div class="text-[10px] text-stone-500 uppercase font-mono mb-1">Active Users</div>
                  <div class="text-2xl font-extrabold text-stone-900 tracking-tight">${totalSold}</div>
                </div>
                <div class="text-xs font-bold text-red-600 flex items-center"><i data-lucide="arrow-down-right" class="w-3 h-3"></i> -1.1%</div>
              </div>
            </div>
          </div>

          <!-- Card 2: Key Metrics -->
          <div class="bg-white/70 backdrop-blur-xl border border-white shadow-[0_8px_30px_rgb(0,0,0,0.06)] rounded-[32px] p-6 flex flex-col justify-between min-h-[220px]">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-sm font-bold text-stone-800">Key Metrics</h3>
              <i data-lucide="more-horizontal" class="w-4 h-4 text-stone-400"></i>
            </div>
            <div class="space-y-6">
              <div>
                <div class="text-[10px] text-stone-500 uppercase font-mono mb-1">Project Pulse (Stock Val)</div>
                <div class="text-lg font-bold text-stone-900">$${stockValue.toLocaleString()} ${sellCurrency}</div>
                <div class="w-full bg-stone-200 h-2 rounded-full mt-2 overflow-hidden flex">
                  <div class="bg-stone-500 h-full" style="width: 40%"></div>
                  <div class="bg-stone-400 h-full ml-1" style="width: 20%"></div>
                  <div class="bg-stone-300 h-full ml-1" style="width: 24%"></div>
                </div>
                <div class="flex justify-between text-[8px] font-mono text-stone-400 mt-1">
                  <span>|</span><span>84% Complete</span>
                </div>
              </div>
              <div>
                <div class="text-[10px] text-stone-500 uppercase font-mono mb-1">Client Health</div>
                <div class="text-2xl font-bold text-stone-900 flex items-center gap-2">
                  ${profile.store ? '<i data-lucide="check-circle" class="w-5 h-5 text-green-600"></i> Healthy' : '<i data-lucide="alert-circle" class="w-5 h-5 text-yellow-600"></i> Disconnected'}
                </div>
              </div>
            </div>
          </div>

          <!-- Card 3: Recent Activity -->
          <div class="bg-white/70 backdrop-blur-xl border border-white shadow-[0_8px_30px_rgb(0,0,0,0.06)] rounded-[32px] p-6 flex flex-col justify-between min-h-[220px]">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-sm font-bold text-stone-800">Recent Activity</h3>
              <i data-lucide="more-horizontal" class="w-4 h-4 text-stone-400"></i>
            </div>
            
            <div class="space-y-4">
              <div class="flex items-center justify-between group cursor-pointer border-b border-stone-200 pb-2">
                <div>
                  <div class="text-[10px] text-stone-500 font-mono">Onboarded:</div>
                  <div class="text-xs font-bold text-stone-800">Shopify</div>
                </div>
                <button onclick="connectStore('shopify')" class="text-[10px] font-bold ${profile.store==='shopify'?'text-red-600':'text-stone-800'}">${profile.store==='shopify'?'Disconnect':'Connect'}</button>
              </div>

              <div class="flex items-center justify-between group cursor-pointer border-b border-stone-200 pb-2">
                <div>
                  <div class="text-[10px] text-stone-500 font-mono">Milestone:</div>
                  <div class="text-xs font-bold text-stone-800">TiendaNube</div>
                </div>
                <button onclick="connectStore('tiendanube')" class="text-[10px] font-bold ${profile.store==='tiendanube'?'text-red-600':'text-stone-800'}">${profile.store==='tiendanube'?'Disconnect':'Connect'}</button>
              </div>
              
              <div class="flex items-center justify-between group cursor-pointer">
                <div>
                  <div class="text-[10px] text-stone-500 font-mono">Task:</div>
                  <div class="text-xs font-bold text-stone-800">Project Review</div>
                </div>
                <button onclick="syncWithStore()" class="text-[10px] font-bold text-stone-800 hover:text-champagne">Sync</button>
              </div>
            </div>
          </div>
        </div>
"""

    start_str = "      el.innerHTML = `\n        <!-- Conexión de Tiendas"
    end_str = "        <!-- Tabla Negocio -->"
    
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx] + new_html + "\n" + content[end_idx:]
        with open('index.html', 'w') as f:
            f.write(new_content)
        print("Dashboard replaced successfully.")
    else:
        print("Could not find boundaries.", start_idx, end_idx)
        
update_dashboard()
