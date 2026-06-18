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
        800px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), 
        rgba(255,255,255,0.6), 
        transparent 40%
      );
      opacity: 0;
      transition: opacity 0.5s ease;
      pointer-events: none;
      z-index: 0;
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

# 2. Add class to specific elements
# Features Cards
html = html.replace('bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] flex flex-col', 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] flex flex-col spotlight-card')

# Wait, in index.html, what are the exact classes for Features?
# Let's search and replace carefully.
# The Features card: 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[2.5rem] p-8 flex flex-col justify-between h-[500px]'
html = html.replace('bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[2.5rem] p-8 flex', 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[2.5rem] p-8 flex spotlight-card')

# Protocol Bubbles: 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[3rem] p-10 md:p-16 grid'
html = html.replace('bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[3rem] p-10', 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[3rem] p-10 spotlight-card')

# Dropshipping vs Ecommerce: 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] p-10 rounded-[3rem] relative group overflow-hidden'
html = html.replace('p-10 rounded-[3rem] relative group overflow-hidden', 'p-10 rounded-[3rem] relative group overflow-hidden spotlight-card')

# Wall of Love: 'bg-[#141416] shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] border border-white/5 rounded-[2.5rem] p-10 relative'
html = html.replace('bg-[#141416] shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] border border-white/5 rounded-[2.5rem] p-10 relative', 'bg-[#141416] shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] border border-white/5 rounded-[2.5rem] p-10 relative spotlight-card')

# FAQ: 'bg-[#141416] border border-white/5 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] rounded-3xl p-6 md:p-8 cursor-pointer'
html = html.replace('bg-[#141416] border border-white/5 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] rounded-3xl p-6 md:p-8 cursor-pointer', 'bg-[#141416] border border-white/5 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] rounded-3xl p-6 md:p-8 cursor-pointer spotlight-card')

# Stats: 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[2.5rem] p-8 saas-shadow'
html = html.replace('rounded-[2.5rem] p-8 saas-shadow', 'rounded-[2.5rem] p-8 saas-shadow spotlight-card')


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
