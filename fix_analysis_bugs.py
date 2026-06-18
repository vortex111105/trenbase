import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Fix the bubbles background (bg-gray-50 -> bg-white saas-shadow)
js = js.replace('bg-gray-50 border border-gray-100 rounded-2xl p-5', 'bg-white border border-gray-100 rounded-3xl p-6 saas-shadow-sm transition hover:-translate-y-1 hover:shadow-md')

# 2. Add the missing renderAnalysisChart function!
chart_func = """
    window.renderAnalysisChart = function(labels, data, name) {
      const ctx = document.getElementById('analysisChart');
      if(!ctx) return;
      if (window.analysisChartInst) window.analysisChartInst.destroy();
      
      window.analysisChartInst = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'TrendScore: ' + name,
            data: data,
            borderColor: '#000000',
            backgroundColor: 'rgba(0, 0, 0, 0.05)',
            fill: true,
            tension: 0.4,
            borderWidth: 2,
            pointBackgroundColor: '#000000',
            pointBorderColor: '#ffffff',
            pointRadius: 4,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(0,0,0,0.8)',
              titleFont: { family: 'monospace', size: 11 },
              bodyFont: { family: 'monospace', size: 11 },
              padding: 10,
              cornerRadius: 8,
              displayColors: false
            }
          },
          scales: {
            x: { display: true, grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: 'rgba(0,0,0,0.5)', font: { family: 'monospace', size: 10 } } },
            y: { display: true, grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: 'rgba(0,0,0,0.5)', font: { family: 'monospace', size: 10 } } }
          }
        }
      });
    }
"""

if 'window.renderAnalysisChart =' not in js:
    # Let's just append it to the end of the file since it's added to window!
    js += '\n' + chart_func + '\n'
    
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Fixed bubbles and added chart function!")
