import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix heroCat and heroScore
js = js.replace("document.getElementById('heroCat').textContent = p1.cat;", "const hc = document.getElementById('heroCat'); if(hc) hc.textContent = p1.cat;")
js = js.replace("document.getElementById('heroScore').textContent = p1.score;", "const hs = document.getElementById('heroScore'); if(hs) hs.textContent = p1.score;")

# Fix calcCostVal
js = js.replace("document.getElementById('calcCostVal').textContent = '$' + cost.toFixed(2);", "const ccv = document.getElementById('calcCostVal'); if(ccv) ccv.textContent = '$' + cost.toFixed(2);")
js = js.replace("document.getElementById('calcAdsVal').textContent = '$' + ads.toFixed(2);", "const cav = document.getElementById('calcAdsVal'); if(cav) cav.textContent = '$' + ads.toFixed(2);")
js = js.replace("document.getElementById('calcPriceVal').textContent = '$' + price.toFixed(2);", "const cpv = document.getElementById('calcPriceVal'); if(cpv) cpv.textContent = '$' + price.toFixed(2);")
js = js.replace("document.getElementById('calcResult').innerHTML = resultHTML;", "const cr = document.getElementById('calcResult'); if(cr) cr.innerHTML = resultHTML;")

# Fix innerText in calcROI
js = js.replace("document.getElementById('calcCostVal').innerText = '$' + cost.toFixed(2);", "const ccv2 = document.getElementById('calcCostVal'); if(ccv2) ccv2.innerText = '$' + cost.toFixed(2);")
js = js.replace("document.getElementById('calcAdsVal').innerText = '$' + ads.toFixed(2);", "const cav2 = document.getElementById('calcAdsVal'); if(cav2) cav2.innerText = '$' + ads.toFixed(2);")
js = js.replace("document.getElementById('calcPriceVal').innerText = '$' + price.toFixed(2);", "const cpv2 = document.getElementById('calcPriceVal'); if(cpv2) cpv2.innerText = '$' + price.toFixed(2);")

# Fix pmTitle, etc
js = js.replace("document.getElementById('pmTitle').textContent = p.name;", "const pt = document.getElementById('pmTitle'); if(pt) pt.textContent = p.name;")
js = js.replace("document.getElementById('pmCat').textContent = p.cat;", "const pc = document.getElementById('pmCat'); if(pc) pc.textContent = p.cat;")
js = js.replace("document.getElementById('pmScore').textContent = p.score;", "const ps = document.getElementById('pmScore'); if(ps) ps.textContent = p.score;")
js = js.replace("document.getElementById('pmMargin').textContent = p.margin + '%';", "const pma = document.getElementById('pmMargin'); if(pma) pma.textContent = p.margin + '%';")
js = js.replace("document.getElementById('pmComp').textContent = p.comp;", "const pco = document.getElementById('pmComp'); if(pco) pco.textContent = p.comp;")
js = js.replace("document.getElementById('pmSuppliers').innerHTML = supHTML;", "const psu = document.getElementById('pmSuppliers'); if(psu) psu.innerHTML = supHTML;")

# Fix prov Icons
js = js.replace("document.getElementById('provIcon1').innerText = ", "const pi1 = document.getElementById('provIcon1'); if(pi1) pi1.innerText = ")
js = js.replace("document.getElementById('provName1').innerText = ", "const pn1 = document.getElementById('provName1'); if(pn1) pn1.innerText = ")
js = js.replace("document.getElementById('provDesc1').innerText = ", "const pd1 = document.getElementById('provDesc1'); if(pd1) pd1.innerText = ")

js = js.replace("document.getElementById('provIcon2').innerText = ", "const pi2 = document.getElementById('provIcon2'); if(pi2) pi2.innerText = ")
js = js.replace("document.getElementById('provName2').innerText = ", "const pn2 = document.getElementById('provName2'); if(pn2) pn2.innerText = ")
js = js.replace("document.getElementById('provDesc2').innerText = ", "const pd2 = document.getElementById('provDesc2'); if(pd2) pd2.innerText = ")


with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Safety patches applied!")
