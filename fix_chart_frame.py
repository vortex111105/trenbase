import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_code = """      let historySlice = p.history || [];
      const currentPeriodLabels = window.WEEKS.slice(0, currentAnalysisPeriod);
      window.renderAnalysisChart(currentPeriodLabels, historySlice.slice(-currentAnalysisPeriod), p.name);"""

new_code = """      let historySlice = p.history || [];
      const actualData = historySlice.slice(-currentAnalysisPeriod);
      // Ensure labels length matches data length so chart stretches to the end
      const currentPeriodLabels = window.WEEKS.slice(0, actualData.length);
      window.renderAnalysisChart(currentPeriodLabels, actualData, p.name);"""

js = js.replace(old_code, new_code)

# Also let's increase the data points of the dummy data just in case? No, slicing the labels is much cleaner and scalable.

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Chart frame issue fixed!")
