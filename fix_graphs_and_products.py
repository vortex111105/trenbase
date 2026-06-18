import re

def fix():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Increase products to 60 by duplicating the array elements.
    # The array currently has 20 elements. Let's find it.
    match = re.search(r'products:\s*\[(.*?)\],\s*count:\s*47250', html, re.DOTALL)
    if match:
        products_inner = match.group(1)
        # Duplicate 2 times so we have 60 total
        # We will just append the same inner elements but maybe change their names slightly
        p2 = products_inner.replace(' name: "', ' name: "Nuevo ')
        p3 = products_inner.replace(' name: "', ' name: "Pro ')
        
        new_inner = products_inner + ",\n" + p2 + ",\n" + p3
        
        html = html.replace(match.group(1), new_inner)

    # 2. Add historyChart initialization to renderHistoryChart
    # We will inject the chart code right after the tbody.innerHTML update
    chart_code = """
      // Init or update History Chart
      const ctx = document.getElementById('historyChart');
      if(ctx) {
        if(histChart) histChart.destroy();
        const labels = WEEKS.slice(0, p.history.length);
        histChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'TrendScore',
              data: p.history,
              borderColor: '#C9A84C',
              backgroundColor: 'rgba(201, 168, 76, 0.1)',
              fill: true,
              tension: 0.4,
              borderWidth: 2,
              pointBackgroundColor: '#C9A84C',
              pointBorderColor: '#000',
              pointRadius: 4,
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: { padding: { bottom: 20 } },
            plugins: { legend: { display: false } },
            scales: {
              x: { display: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: 'rgba(255,255,255,0.5)', font: { family: 'monospace', size: 10 } } },
              y: { display: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: 'rgba(255,255,255,0.5)', font: { family: 'monospace', size: 10 } } }
            }
          }
        });
      }
"""
    
    html = re.sub(
        r'(\}\)\.join\(\'\'\);\s*\n\s*\})',
        r'}).join(\'\');\n' + chart_code + r'    }',
        html
    )

    # 3. Add layout padding to analysisChart to prevent X-axis from cutting off
    html = html.replace('maintainAspectRatio: false,', 'maintainAspectRatio: false,\n            layout: { padding: { bottom: 20 } },')

    # Also make sure the canvas wrappers have absolute dimensions if needed, or min-height.
    html = html.replace('class="h-72 relative w-full"', 'class="h-[300px] relative w-full"')
    html = html.replace('class="h-96 relative w-full mt-4"', 'class="h-[350px] relative w-full mt-4"')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
if __name__ == "__main__":
    fix()
