const signals = [];

const domainInput = document.getElementById("domainInput");
const textInput = document.getElementById("textInput");
const addBtn = document.getElementById("addBtn");
const analyzeBtn = document.getElementById("analyzeBtn");
const chipsNode = document.getElementById("signals");
const resultsNode = document.getElementById("results");
const topDimensionsNode = document.getElementById("topDimensions");
const vectorBarsNode = document.getElementById("vectorBars");
const recsNode = document.getElementById("recommendations");

function renderSignals() {
  chipsNode.innerHTML = "";
  signals.forEach((s) => {
    const chip = document.createElement("div");
    chip.className = "chip";
    chip.textContent = `${s.domain}: ${s.text}`;
    chipsNode.appendChild(chip);
  });
}

addBtn.addEventListener("click", () => {
  const domain = domainInput.value.trim();
  const text = textInput.value.trim();
  if (!domain || !text) return;

  signals.push({ domain, text });
  domainInput.value = "";
  textInput.value = "";
  renderSignals();
});

function renderResult(data) {
  const { profile, recommendations } = data;

  topDimensionsNode.innerHTML = "";
  profile.top_dimensions.forEach((dim) => {
    const el = document.createElement("div");
    el.className = "dim";
    el.textContent = dim;
    topDimensionsNode.appendChild(el);
  });

  vectorBarsNode.innerHTML = "";
  Object.entries(profile.vector).forEach(([name, value]) => {
    const row = document.createElement("div");
    row.className = "bar";
    row.innerHTML = `
      <div class="bar-head"><span>${name}</span><span>${Math.round(value * 100)}%</span></div>
      <div class="track"><div class="fill" style="width:${Math.round(value * 100)}%"></div></div>
    `;
    vectorBarsNode.appendChild(row);
  });

  recsNode.innerHTML = "";
  recommendations.forEach((rec) => {
    const card = document.createElement("article");
    card.className = "rec";
    card.innerHTML = `
      <h4>${rec.title}</h4>
      <p class="meta">${rec.entity_type} • ${rec.domains.join(", ")}</p>
      <p>Similarity: ${Math.round(rec.similarity * 100)}%</p>
      <p class="meta">Matched on: ${rec.matched_dimensions.join(", ")}</p>
    `;
    recsNode.appendChild(card);
  });

  resultsNode.classList.remove("hidden");
}

analyzeBtn.addEventListener("click", async () => {
  if (signals.length === 0) return;

  const resp = await fetch("/api/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ signals }),
  });

  if (!resp.ok) {
    alert("Could not analyze taste right now.");
    return;
  }

  renderResult(await resp.json());
});
