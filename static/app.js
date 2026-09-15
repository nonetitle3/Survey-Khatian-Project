const $ = (id) => document.getElementById(id);
const els = { division: $("division"), district: $("district"), upazila: $("upazila"), survey: $("survey"), mouza: $("mouza"), search: $("search"), searchBtn: $("searchBtn"), rows: $("rows"), count: $("count"), preview: $("preview"), details: $("khatianDetails"), pdfFrame: $("pdfFrame"), pdfPreviewBtn: $("pdfPreviewBtn"), download: $("download"), print: $("print") };
let currentPdf = "";

async function api(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
function fill(select, items, placeholder) {
  select.innerHTML = `<option value="">${placeholder}</option>` + items.map(x => `<option value="${x.id}">${x.name}</option>`).join("");
  select.disabled = false;
}
function resetSelect(select, text) { select.innerHTML = `<option value="">${text}</option>`; select.disabled = true; }
function escapeHtml(s) { return String(s ?? "").replace(/[&<>'"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c])); }

async function loadDivisions() { fill(els.division, await api("/api/divisions"), "বিভাগ নির্বাচন করুন"); }
async function loadDistricts() { resetSelect(els.upazila,"উপজেলা নির্বাচন করুন"); resetSelect(els.survey,"সার্ভে নির্বাচন করুন"); resetSelect(els.mouza,"মৌজা নির্বাচন করুন"); els.search.disabled=true; els.searchBtn.disabled=true; if (els.division.value) fill(els.district, await api(`/api/districts?division_id=${encodeURIComponent(els.division.value)}`),"জেলা নির্বাচন করুন"); else resetSelect(els.district,"জেলা নির্বাচন করুন"); }
async function loadUpazilas() { resetSelect(els.survey,"সার্ভে নির্বাচন করুন"); resetSelect(els.mouza,"মৌজা নির্বাচন করুন"); els.search.disabled=true; els.searchBtn.disabled=true; if (els.district.value) fill(els.upazila, await api(`/api/upazilas?district_id=${encodeURIComponent(els.district.value)}`),"উপজেলা নির্বাচন করুন"); else resetSelect(els.upazila,"উপজেলা নির্বাচন করুন"); }
async function loadSurveys() { resetSelect(els.mouza,"মৌজা নির্বাচন করুন"); els.search.disabled=true; els.searchBtn.disabled=true; if (els.upazila.value) fill(els.survey, await api(`/api/surveys?upazila_id=${encodeURIComponent(els.upazila.value)}`),"সার্ভে নির্বাচন করুন"); else resetSelect(els.survey,"সার্ভে নির্বাচন করুন"); }
async function loadMouzas() { els.search.disabled=true; els.searchBtn.disabled=true; if (els.upazila.value && els.survey.value) fill(els.mouza, await api(`/api/mouzas?upazila_id=${encodeURIComponent(els.upazila.value)}&survey_id=${encodeURIComponent(els.survey.value)}`),"মৌজা নির্বাচন করুন"); else resetSelect(els.mouza,"মৌজা নির্বাচন করুন"); }
async function loadKhatians() { if (!els.mouza.value) return; const q=encodeURIComponent(els.search.value.trim()); const rows=await api(`/api/khatians?mouza_id=${encodeURIComponent(els.mouza.value)}&q=${q}`); els.count.textContent=`${rows.length} টি`; els.rows.innerHTML=rows.length?rows.map(r=>`<tr><td>${escapeHtml(r.khatian_no)}</td><td>${escapeHtml(r.owner)}</td><td>${escapeHtml(r.dag_no)}</td><td>${escapeHtml(r.land_area)}</td><td><button onclick="previewKhatian('${r.id}')">তথ্য দেখুন</button></td></tr>`).join(""):`<tr><td colspan="5" class="empty">কোনো ফলাফল পাওয়া যায়নি</td></tr>`; }

window.previewKhatian = async function(id) {
  els.preview.showModal();
  els.details.innerHTML = "তথ্য লোড হচ্ছে...";
  try {
    const r = await api(`/api/khatians/${encodeURIComponent(id)}`);
    currentPdf = `/api/khatians/${encodeURIComponent(id)}/pdf`;
    els.details.innerHTML = `
      <div class="kp-header"><div><div class="kp-title">খতিয়ান নং</div><div class="kp-number">${escapeHtml(r.khatian_no)}</div></div><div class="kp-badge">মোট জমি <strong>${escapeHtml(r.total_land)}</strong></div></div>
      <div class="kp-grid">
        <div class="kp-card"><h3>প্রশাসনিক তথ্য</h3><div class="kp-list">
          <div><span>বিভাগ:</span> <strong>${escapeHtml(r.division)}</strong></div>
          <div><span>জেলা:</span> <strong>${escapeHtml(r.district)}</strong></div>
          <div><span>উপজেলা:</span> <strong>${escapeHtml(r.upazila)}</strong></div>
          <div><span>সার্ভে:</span> <strong>${escapeHtml(r.survey)}</strong></div>
          <div><span>মৌজা:</span> <strong>${escapeHtml(r.mouza)}</strong></div>
          <div><span>জে এল নং:</span> <strong>${escapeHtml(r.jl_no)}</strong></div>
        </div></div>
        <div class="kp-card"><h3>জমির বিবরণ</h3><div class="kp-list">
          <div><span>দাগ নম্বর:</span> <strong>${escapeHtml(r.dag_no)}</strong></div>
          <div><span>মোট জমি:</span> <strong>${escapeHtml(r.total_land)}</strong></div>
          <div><span>মালিক:</span> <strong>${escapeHtml(r.owner)}</strong></div>
          <div><span>অভিভাবক:</span> <strong>${escapeHtml(r.guardian)}</strong></div>
        </div></div>
      </div>
      <div class="kp-card kp-details"><h3>বিস্তারিত তথ্য</h3><div class="kp-bullets">
        <div><span class="kp-title">মালিক</span><div class="kp-bullet"><span class="kp-dot"></span><strong>${escapeHtml(r.owner)}</strong></div></div>
        <div><span class="kp-title">অভিভাবক</span><div class="kp-bullet"><span class="kp-dot"></span><strong>${escapeHtml(r.guardian)}</strong></div></div>
      </div><div style="margin-top:16px"><span class="kp-title">দাগ নম্বর</span><br><span class="kp-dag">${escapeHtml(r.dag_no)}</span></div></div>
      <div class="kp-note">এই Preview স্থানীয়/অনুমোদিত project data থেকে তৈরি।</div>`;
  } catch (err) {
    els.details.innerHTML = `<div class="empty">খতিয়ানের তথ্য লোড করা যায়নি।</div>`;
    console.error(err);
  }
};

els.pdfPreviewBtn.addEventListener("click", () => { if (!currentPdf) return; els.pdfFrame.hidden = false; els.pdfFrame.src = currentPdf; els.pdfPreviewBtn.disabled = true; });
els.download.addEventListener("click", () => { if (currentPdf) window.location.href = currentPdf; });
els.print.addEventListener("click", () => { if (!els.pdfFrame.hidden) els.pdfFrame.contentWindow?.print(); else window.print(); });
els.division.addEventListener("change", loadDistricts); els.district.addEventListener("change", loadUpazilas); els.upazila.addEventListener("change", loadSurveys); els.survey.addEventListener("change", loadMouzas); els.mouza.addEventListener("change",()=>{els.search.disabled=!els.mouza.value;els.searchBtn.disabled=!els.mouza.value;loadKhatians()}); els.searchBtn.addEventListener("click",loadKhatians); els.search.addEventListener("keydown",e=>{if(e.key==="Enter")loadKhatians()}); $("close").addEventListener("click",()=>{els.pdfFrame.hidden=true;els.pdfFrame.src="about:blank";els.pdfPreviewBtn.disabled=false;els.preview.close()}); $("resetBtn").addEventListener("click",()=>location.reload());
loadDivisions().catch(console.error);
