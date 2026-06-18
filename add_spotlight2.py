import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS
css = """
    /* Spotlight Effect */
    .spotlight-card {
      position: relative;
      overflow: hidden;
    }
    .spotlight-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: radial-gradient(
        600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), 
        rgba(255,255,255,0.4), 
        transparent 40%
      );
      opacity: 0;
      transition: opacity 0.5s ease;
      pointer-events: none;
      z-index: 0;
    }
    /* Darker spotlight for dark mode cards (FAQ) */
    .spotlight-dark::before {
      background: radial-gradient(
        600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), 
        rgba(255,255,255,0.08), 
        transparent 40%
      );
    }
    .spotlight-card:hover::before {
      opacity: 1;
    }
    .spotlight-card > * {
      position: relative;
      z-index: 1;
    }
  </style>
"""
html = html.replace('</style>', css)

# 2. Inject classes
# Features
html = html.replace('class="bg-gray-50 rounded-[2.5rem] p-8 flex flex-col justify-between h-[500px] border border-gray-200 shadow-xl overflow-hidden relative group"', 'class="bg-gray-50 rounded-[2.5rem] p-8 flex flex-col justify-between h-[500px] border border-gray-200 shadow-xl overflow-hidden relative group spotlight-card"')

# Protocol Bubbles
html = html.replace('class="bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[3rem] p-10 md:p-16 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center"', 'class="bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[3rem] p-10 md:p-16 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center spotlight-card"')

# Ecommerce vs Dropshipping
html = html.replace('class="bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] p-10 rounded-[3rem] relative group overflow-hidden"', 'class="bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] p-10 rounded-[3rem] relative group overflow-hidden spotlight-card"')

# Wall of Love (Card 1, Card 3)
html = html.replace('class="bg-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-white/80 rounded-[2.5rem] p-10 relative"', 'class="bg-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-white/80 rounded-[2.5rem] p-10 relative spotlight-card"')
# Wall of Love (Card 2)
html = html.replace('class="bg-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-white/80 rounded-[2.5rem] p-10 relative transform md:-translate-y-4"', 'class="bg-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-white/80 rounded-[2.5rem] p-10 relative transform md:-translate-y-4 spotlight-card"')

# FAQ (Dark mode cards)
html = html.replace('class="group bg-[#141416] border border-white/5 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] rounded-3xl p-6 md:p-8 cursor-pointer hover:bg-[#1C1C1E] transition duration-300"', 'class="group bg-[#141416] border border-white/5 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] rounded-3xl p-6 md:p-8 cursor-pointer hover:bg-[#1C1C1E] transition duration-300 spotlight-card spotlight-dark"')


# 3. Add JS at the end
js = """
  <!-- Spotlight JS -->
  <script>
    document.querySelectorAll('.spotlight-card').forEach(card => {
      card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      });
    });
  </script>
</body>
"""
html = html.replace('</body>', js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
