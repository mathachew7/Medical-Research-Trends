document.addEventListener("DOMContentLoaded", () => {
  const pubCount = document.getElementById("pubCount");
  const topCategory = document.getElementById("topCategory");
  const growthRate = document.getElementById("growthRate");
  const categoryGrowth = document.getElementById("categoryGrowth");
  const topKeywordsList = document.getElementById("topKeywordsList");
  const coOccurCloud = document.getElementById("coOccurCloud");
  const abstractList = document.getElementById("abstractList");
  const trendCtx = document.getElementById("trendChart")?.getContext("2d");
  const pieCtx = document.getElementById("pieChart")?.getContext("2d");
  const forecastCtx = document.getElementById("forecastChart")?.getContext("2d");
  const startYear = document.getElementById("startYear");
  const endYear = document.getElementById("endYear");
  const applyFilterBtn = document.getElementById("applyFilterBtn");
  const categoryDropdown = document.getElementById("categoryDropdown");

  let trendData = [];
  let trendChart;

  const palette = [
    "#60a5fa", "#38bdf8", "#34d399", "#f472b6", "#facc15",
    "#f87171", "#c084fc", "#fbbf24", "#2dd4bf", "#a5b4fc",
    "#818cf8", "#4ade80", "#fb923c", "#f97316", "#a78bfa"
  ];

  async function loadTrends() {
    const res = await fetch("/trends");
    const { trends } = await res.json();
    trendData = trends.filter(d => d.Year <= 2024);
    const categories = Object.keys(trendData[0]).filter(k => k !== "Year");
    populateCategoryDropdown(categories);
    renderTrendChart(trendData, categories);
  }

  async function loadStats() {
    const res = await fetch("/stats");
    const stats = await res.json();

    pubCount.textContent = Number(stats.total_publications || 0).toLocaleString();
    topCategory.textContent = stats.top_category || "--";
    growthRate.textContent = stats.growth_rate.startsWith("-") ? stats.growth_rate : "+" + stats.growth_rate;
    categoryGrowth.textContent = stats.category_growth.startsWith("-") ? stats.category_growth : "+" + stats.category_growth;

    topKeywordsList.innerHTML = "";
    (stats.top_keywords || []).forEach(k => {
      const li = document.createElement("li");
      li.textContent = `${k.term} (${k.count})`;
      topKeywordsList.appendChild(li);
    });

    // Donut chart
    if (pieCtx && trendData.length > 0) {
      const latest = trendData.find(d => d.Year === 2024);
      const labels = Object.keys(latest).filter(k => k !== "Year");
      const values = labels.map(label => latest[label]);

      new Chart(pieCtx, {
        type: 'doughnut',
        data: {
          labels,
          datasets: [{
            data: values,
            backgroundColor: palette.slice(0, labels.length)
          }]
        },
        options: {
          cutout: "60%",
          layout: {
            padding: 0
          },
          plugins: {
            legend: {
              position: "right",
              labels: {
                color: "#ccc",
                usePointStyle: true,
                boxWidth: 10
              }
            },
            tooltip: {
              callbacks: {
                label: ctx => `${ctx.label}: ${ctx.raw.toLocaleString()}`
              }
            }
          }
        }
      });
    }
  }

  async function loadForecast() {
    const res = await fetch("/forecast");
    const data = await res.json();
    new Chart(forecastCtx, {
      type: "bar",
      data: {
        labels: data.years,
        datasets: [{
          label: "Forecasted Publications",
          data: data.counts,
          backgroundColor: "#60a5fa"
        }]
      },
      options: {
        plugins: { legend: { display: false } },
        scales: {
          x: { title: { display: true, text: "Year", color: "#ccc" }, ticks: { color: "#ccc" }, grid: { display: false } },
          y: { title: { display: true, text: "Count", color: "#ccc" }, ticks: { color: "#ccc" }, grid: { display: false } }
        }
      }
    });
  }

  async function loadAbstracts() {
    const res = await fetch("/recent_abstracts");
    const data = await res.json();
    abstractList.innerHTML = "";
    data.forEach(ref => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${ref.Year}</strong> - <a href="https://pubmed.ncbi.nlm.nih.gov/${ref.PMID}/" target="_blank" class="text-blue-400 underline">${ref.PMID}</a>`;
      abstractList.appendChild(li);
    });
  }

  async function loadCoOccurrence() {
    const res = await fetch("/co_occurrence");
    const data = await res.json();
    coOccurCloud.innerHTML = "";
    (data.terms || []).forEach(term => {
      const span = document.createElement("span");
      span.textContent = term;
      span.className = "bg-blue-800 px-2 py-1 rounded";
      coOccurCloud.appendChild(span);
    });
  }

  function populateCategoryDropdown(categories) {
    categoryDropdown.innerHTML = "";
    categories.forEach(cat => {
      const label = document.createElement("label");
      label.className = "flex items-center p-2 hover:bg-gray-800 cursor-pointer";
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.className = "category-check form-checkbox text-blue-600 mr-2";
      checkbox.value = cat;
      checkbox.checked = true;
      label.appendChild(checkbox);
      label.appendChild(document.createTextNode(cat));
      categoryDropdown.appendChild(label);
    });
  }

  function getSelectedCategories() {
    return Array.from(document.querySelectorAll(".category-check:checked")).map(cb => cb.value);
  }

  function renderTrendChart(data, selectedCategories) {
    const years = data.map(d => d.Year);
    const datasets = selectedCategories.map((cat, i) => ({
      label: cat,
      data: data.map(d => d[cat]),
      borderColor: palette[i % palette.length],
      backgroundColor: palette[i % palette.length],
      fill: false,
      tension: 0.4
    }));

    if (trendChart) trendChart.destroy();
    trendChart = new Chart(trendCtx, {
      type: "line",
      data: { labels: years, datasets },
      options: {
        responsive: true,
        plugins: {
          title: { display: false },
          legend: {
            labels: {
              color: "#ccc",
              usePointStyle: true,
              boxWidth: 14
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: "Year", color: "#ccc" },
            ticks: { color: "#ccc" },
            grid: { display: false }
          },
          y: {
            title: { display: true, text: "Publications", color: "#ccc" },
            ticks: { color: "#ccc" },
            grid: { display: false }
          }
        }
      }
    });
  }

  applyFilterBtn.addEventListener("click", () => {
    const selectedCats = getSelectedCategories();
    const sYear = parseInt(startYear.value);
    const eYear = parseInt(endYear.value);
    const filtered = trendData.filter(d => d.Year >= sYear && d.Year <= eYear);
    renderTrendChart(filtered, selectedCats);
  });

  loadTrends().then(() => loadStats());
  loadForecast();
  loadAbstracts();
  loadCoOccurrence();
});
