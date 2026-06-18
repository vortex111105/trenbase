import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

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
            legend: { display: false }
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
    # insert before window.calcROI
    js = js.replace("function calcROI() {", chart_func + "\nfunction calcROI() {")
    # also we need to make sure the call to renderAnalysisChart inside app.js uses window.renderAnalysisChart
    js = js.replace("renderAnalysisChart(currentPeriodLabels", "window.renderAnalysisChart(currentPeriodLabels")
    # and fix analysisChartInst to use window.
    js = js.replace("var analysisChartInst = null;", "window.analysisChartInst = null;")
    
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Added renderAnalysisChart.")
else:
    print("Already added.")
