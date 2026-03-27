const API = "http://localhost:8000";

const form = document.getElementById("symptom-form");
const symptomsInput = document.getElementById("symptoms");
const submitBtn = document.getElementById("submit-btn");
const btnText = submitBtn.querySelector(".btn-text");
const btnLoader = submitBtn.querySelector(".btn-loader");
const resultSection = document.getElementById("result");
const analysisContent = document.getElementById("analysis-content");
const loadHistoryBtn = document.getElementById("load-history");
const historyList = document.getElementById("history-list");
const charCurrent = document.getElementById("char-current");

// Character counter
symptomsInput.addEventListener("input", () => {
  charCurrent.textContent = symptomsInput.value.length;
});

function setLoading(loading) {
  submitBtn.disabled = loading;
  btnText.classList.toggle("hidden", loading);
  btnLoader.classList.toggle("hidden", !loading);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const symptoms = symptomsInput.value.trim();
  if (!symptoms) return;

  setLoading(true);
  resultSection.classList.add("hidden");

  try {
    const res = await fetch(`${API}/api/check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symptoms }),
    });
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    analysisContent.textContent = data.analysis;
    resultSection.classList.remove("hidden");
    resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    analysisContent.textContent = `Error: ${err.message}`;
    resultSection.classList.remove("hidden");
  } finally {
    setLoading(false);
  }
});

loadHistoryBtn.addEventListener("click", async () => {
  try {
    const res = await fetch(`${API}/api/history`);
    const data = await res.json();
    historyList.innerHTML = "";
    if (data.length === 0) {
      historyList.innerHTML = '<li>No queries yet.</li>';
      return;
    }
    data.forEach((item) => {
      const li = document.createElement("li");
      const date = new Date(item.created_at).toLocaleString();
      li.innerHTML =
        `<span class="hist-symptoms">${escapeHtml(item.symptoms)}</span>` +
        `<span class="hist-date">${date}</span>`;
      historyList.appendChild(li);
    });
  } catch (err) {
    historyList.innerHTML = '<li>Failed to load history.</li>';
  }
});

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
