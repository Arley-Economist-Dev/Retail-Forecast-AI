/**
 * Retail Forecast AI - Client Frontend Logic with Internationalization (i18n)
 * Auto-detects user locale/entry point (English default, Spanish for Hispanic locales/timezones)
 * and allows manual switching at any time.
 */

const translations = {
  en: {
    tagline: "Nixtla NeuralForecast & LLM Inventory Strategist",
    badge_cpu: "CPU Optimized",
    title_parameters: "Inference Parameters",
    btn_use_demo: "Use Retail Demo",
    label_dataset: "CSV Dataset (Nixtla Standard)",
    drag_drop_text: "Drag your CSV file here or",
    browse_text: "browse",
    required_cols_note: "Required columns: unique_id, ds, y",
    label_active_series: "Active Series / SKU",
    label_horizon: "Forecast Horizon",
    horizon_min: "3 days",
    horizon_mid: "30 days",
    horizon_max: "60 days",
    days_suffix: "days",
    label_model: "Nixtla Architecture",
    model_nhits_sub: "Multiscale / Fast CPU",
    model_nbeats_sub: "Pure Decomposition",
    label_fill_gaps: "Impute temporal gaps with 0 (Retail Standard)",
    btn_train_infer: "Train & Forecast",
    btn_processing: "Processing...",
    title_mlops_guarantees: "MLOps Quality Guarantees",
    guarantee_contract: "Strict contract: unique_id, ds, y",
    guarantee_cpu: "PyTorch CPU inference (No OOM on Render)",
    guarantee_llm: "LLM Demand Strategist (Gemini / Groq / Fallback)",
    kpi_hist_mean: "Historical Mean",
    kpi_fore_mean: "Projected Mean",
    kpi_delta: "Projected Delta",
    kpi_volatility: "Volatility (CV)",
    units_per_period: "units/period",
    coeff_variation: "Coeff. of Variation",
    vol_low: "Low Volatility",
    vol_mod: "Moderate Volatility",
    vol_high: "High Volatility",
    trend_prefix: "Trend: ",
    trend_alcista: "BULLISH (UPWARD)",
    trend_bajista: "BEARISH (DOWNWARD)",
    trend_estable: "STABLE",
    chart_title: "Historical vs Forecast",
    chart_initial_msg: "Upload a CSV or click 'Use Retail Demo' to visualize the time series",
    btn_export_csv: "Export Predictions",
    report_title: "Strategic Demand & Inventory Briefing",
    report_subtitle: "Synthesized by LLM Demand Planning Specialist",
    footer_credits: "Engineered with MLOps & Enterprise Retail Software Architecture",
    alert_csv_extension_error: "The selected file must have a .csv extension",
    alert_file_ready: "File loaded: {filename}. Adjust parameters and click 'Train & Forecast'.",
    alert_loading_demo: "Loading synthetic Retail dataset...",
    alert_demo_ready: "Retail demo dataset ready. Click 'Train & Forecast' to view predictions.",
    alert_demo_error: "Could not load sample dataset: ",
    alert_no_file: "Please upload a CSV file or click 'Use Retail Demo'.",
    alert_training_progress: "Training {model} on CPU and computing {horizon}-day forecast...",
    alert_success: "Inference completed successfully in {time}s via {model}.",
    alert_error_prefix: "Pipeline error: ",
    chart_historical_label: "Historical Sales",
    chart_forecast_label: "Neural Forecast",
    chart_upper_label: "Upper Interval (CI)",
    chart_lower_label: "Lower Interval (CI)",
    chart_y_axis: "Units / Demand",
  },
  es: {
    tagline: "Nixtla NeuralForecast & Estratega de Inventario con LLM",
    badge_cpu: "CPU Optimizado",
    title_parameters: "Parámetros de Inferencia",
    btn_use_demo: "Usar Demo Retail",
    label_dataset: "Dataset CSV (Estándar Nixtla)",
    drag_drop_text: "Arrastra tu archivo CSV aquí o",
    browse_text: "explora",
    required_cols_note: "Columnas requeridas: unique_id, ds, y",
    label_active_series: "Serie / SKU Activo",
    label_horizon: "Horizonte de Predicción",
    horizon_min: "3 días",
    horizon_mid: "30 días",
    horizon_max: "60 días",
    days_suffix: "días",
    label_model: "Arquitectura Nixtla",
    model_nhits_sub: "Multiescala / CPU Rápido",
    model_nbeats_sub: "Descomposición Pura",
    label_fill_gaps: "Imputar gaps temporales con 0 (Estándar Retail)",
    btn_train_infer: "Entrenar e Inferir",
    btn_processing: "Procesando...",
    title_mlops_guarantees: "Garantías de Calidad MLOps",
    guarantee_contract: "Contrato estricto: unique_id, ds, y",
    guarantee_cpu: "Inferencia en PyTorch CPU (No OOM en Render)",
    guarantee_llm: "Estrategia con LLM (Gemini / Groq / Fallback)",
    kpi_hist_mean: "Media Histórica",
    kpi_fore_mean: "Media Proyectada",
    kpi_delta: "Delta Proyectado",
    kpi_volatility: "Volatilidad (CV)",
    units_per_period: "unidades/periodo",
    coeff_variation: "Coef. de Variación",
    vol_low: "Baja Volatilidad",
    vol_mod: "Volatilidad Moderada",
    vol_high: "Alta Volatilidad",
    trend_prefix: "Tendencia: ",
    trend_alcista: "ALCISTA",
    trend_bajista: "BAJISTA",
    trend_estable: "ESTABLE",
    chart_title: "Histórico vs Pronóstico",
    chart_initial_msg: "Carga un CSV o presiona 'Usar Demo Retail' para visualizar la serie",
    btn_export_csv: "Exportar Predicciones",
    report_title: "Informe Estratégico de Demanda & Inventario",
    report_subtitle: "Generado por LLM Demand Planning Specialist",
    footer_credits: "Diseñado bajo principios de MLOps & Arquitectura de Software en Retail",
    alert_csv_extension_error: "El archivo seleccionado debe tener extensión .csv",
    alert_file_ready: "Archivo listo: {filename}. Configura tus parámetros y presiona 'Entrenar e Inferir'.",
    alert_loading_demo: "Cargando dataset sintético de Retail...",
    alert_demo_ready: "Dataset demo retail listo. Presiona 'Entrenar e Inferir' para ver los resultados.",
    alert_demo_error: "Error al cargar datos demo: ",
    alert_no_file: "Por favor carga un archivo CSV o utiliza el botón 'Usar Demo Retail'.",
    alert_training_progress: "Entrenando modelo {model} en CPU y generando predicción para horizonte de {horizon} días...",
    alert_success: "Inferencia completada con éxito en {time}s mediante {model}.",
    alert_error_prefix: "Fallo en el pipeline: ",
    chart_historical_label: "Ventas Históricas",
    chart_forecast_label: "Pronóstico Red Neuronal",
    chart_upper_label: "Límite Superior (IC)",
    chart_lower_label: "Límite Inferior (IC)",
    chart_y_axis: "Unidades / Demanda",
  },
};

document.addEventListener("DOMContentLoaded", () => {
  // Current language state
  let currentLang = detectUserLanguage();

  // DOM Elements
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const fileLabel = document.getElementById("file-label");
  const horizonSlider = document.getElementById("horizon-slider");
  const horizonValue = document.getElementById("horizon-value");
  const btnSampleData = document.getElementById("btn-sample-data");
  const btnRunForecast = document.getElementById("btn-run-forecast");
  const btnRunText = document.getElementById("btn-run-text");
  const fillGapsCheck = document.getElementById("fill-gaps");
  const statusAlert = document.getElementById("status-alert");
  const seriesSelectorContainer = document.getElementById("series-selector-container");
  const seriesSelect = document.getElementById("series-select");
  const kpiGrid = document.getElementById("kpi-grid");
  const aiReportCard = document.getElementById("ai-report-card");
  const markdownContent = document.getElementById("markdown-content");
  const btnExportCsv = document.getElementById("btn-export-csv");
  const chartSubheading = document.getElementById("chart-subheading");
  const langBtnEn = document.getElementById("lang-btn-en");
  const langBtnEs = document.getElementById("lang-btn-es");

  // State
  let currentFile = null;
  let chartInstance = null;
  let lastForecastData = null;

  // Initialize Language
  applyLanguage(currentLang);

  langBtnEn.addEventListener("click", () => setLanguage("en"));
  langBtnEs.addEventListener("click", () => setLanguage("es"));

  function detectUserLanguage() {
    // 1. Stored preference
    const saved = localStorage.getItem("retail_forecast_lang");
    if (saved && (saved === "en" || saved === "es")) {
      return saved;
    }

    // 2. Geolocation / Timezone heuristic
    try {
      const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
      const spanishTimezones = [
        "Madrid", "Bogota", "Mexico_City", "Buenos_Aires", "Santiago",
        "Lima", "Caracas", "Montevideo", "Guayaquil", "La_Paz",
        "Asuncion", "Costa_Rica", "Guatemala", "Panama", "Santo_Domingo",
        "Tegucigalpa", "Managua", "San_Salvador"
      ];
      if (spanishTimezones.some((tz) => timeZone.includes(tz))) {
        return "es";
      }
    } catch (e) {
      // Ignore
    }

    // 3. Browser locale check
    const browserLang = (navigator.language || navigator.userLanguage || "en").toLowerCase();
    if (browserLang.startsWith("es")) {
      return "es";
    }

    // Default to English as requested
    return "en";
  }

  function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem("retail_forecast_lang", lang);
    applyLanguage(lang);

    // Re-render chart if active to update labels
    if (lastForecastData) {
      renderResults(lastForecastData);
    }
  }

  function applyLanguage(lang) {
    const t = translations[lang] || translations.en;
    document.documentElement.lang = lang;

    // Update buttons highlight
    if (lang === "es") {
      langBtnEs.className = "px-2.5 py-1 rounded-lg font-bold transition text-white bg-indigo-600 shadow-sm";
      langBtnEn.className = "px-2.5 py-1 rounded-lg font-medium transition text-slate-400 hover:text-white";
    } else {
      langBtnEn.className = "px-2.5 py-1 rounded-lg font-bold transition text-white bg-indigo-600 shadow-sm";
      langBtnEs.className = "px-2.5 py-1 rounded-lg font-medium transition text-slate-400 hover:text-white";
    }

    // Translate DOM elements with data-i18n
    document.querySelectorAll("[data-i18n]").forEach((elem) => {
      const key = elem.getAttribute("data-i18n");
      if (t[key]) {
        elem.innerHTML = t[key];
      }
    });

    // Update dynamic label for horizon
    horizonValue.textContent = `${horizonSlider.value} ${t.days_suffix}`;

    // Update file label if not set
    if (!currentFile) {
      fileLabel.innerHTML = `<span data-i18n="drag_drop_text">${t.drag_drop_text}</span> <span class="text-indigo-400" data-i18n="browse_text">${t.browse_text}</span>`;
    }

    // Re-initialize Lucide icons
    if (window.lucide) {
      window.lucide.createIcons();
    }
  }

  // Horizon Slider Event
  horizonSlider.addEventListener("input", (e) => {
    const t = translations[currentLang];
    horizonValue.textContent = `${e.target.value} ${t.days_suffix}`;
  });

  // Drag and Drop Events
  dropZone.addEventListener("click", () => fileInput.click());

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("border-indigo-500", "bg-indigo-500/10");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("border-indigo-500", "bg-indigo-500/10");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("border-indigo-500", "bg-indigo-500/10");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  async function handleFileSelected(file) {
    const t = translations[currentLang];
    if (!file.name.endsWith(".csv")) {
      showAlert(t.alert_csv_extension_error, "error");
      return;
    }
    currentFile = file;
    fileLabel.innerHTML = `<span class="text-indigo-400 font-bold">${file.name}</span> (${(file.size / 1024).toFixed(1)} KB)`;
    showAlert(t.alert_file_ready.replace("{filename}", file.name), "info");

    // Scan for available SKUs/unique_ids in the CSV to populate dropdown immediately
    await inspectCsvSeries(file);
  }

  // Load bundled Sample Data
  btnSampleData.addEventListener("click", async () => {
    const t = translations[currentLang];
    try {
      showAlert(t.alert_loading_demo, "info");
      const res = await fetch("/api/v1/sample-data");
      if (!res.ok) throw new Error(t.alert_demo_error);
      const blob = await res.blob();
      currentFile = new File([blob], "sample_retail_sales.csv", { type: "text/csv" });
      fileLabel.innerHTML = `<span class="text-emerald-400 font-bold">sample_retail_sales.csv</span> (Demo Multi-SKU)`;
      showAlert(t.alert_demo_ready, "success");

      // Scan and populate series selector
      await inspectCsvSeries(currentFile);
    } catch (err) {
      showAlert(`${t.alert_demo_error}${err.message}`, "error");
    }
  });

  async function inspectCsvSeries(file) {
    try {
      // Read first chunk of file to discover unique_ids
      const textChunk = await file.slice(0, 150000).text();
      const lines = textChunk.split(/\r?\n/).filter((l) => l.trim().length > 0);
      if (lines.length > 1) {
        const headers = lines[0].split(",").map((h) => h.trim().toLowerCase());
        const uidIndex = headers.indexOf("unique_id");
        if (uidIndex !== -1) {
          const uniqueIds = new Set();
          for (let i = 1; i < lines.length; i++) {
            const cols = lines[i].split(",");
            if (cols.length > uidIndex) {
              const val = cols[uidIndex].trim();
              if (val) uniqueIds.add(val);
            }
          }
          const seriesList = Array.from(uniqueIds).sort();
          if (seriesList.length > 1) {
            seriesSelectorContainer.classList.remove("hidden");
            seriesSelect.innerHTML = seriesList
              .map((s) => `<option value="${s}">${s}</option>`)
              .join("");
          } else {
            seriesSelectorContainer.classList.add("hidden");
          }
        }
      }
    } catch (e) {
      console.warn("Could not preview CSV series:", e);
    }
  }

  // Series Selection Change (if multi-series)
  seriesSelect.addEventListener("change", () => {
    if (currentFile) {
      runForecasting();
    }
  });

  // Run Forecast Button Event
  btnRunForecast.addEventListener("click", () => {
    runForecasting();
  });

  // Main Forecast Execution
  async function runForecasting() {
    const t = translations[currentLang];
    if (!currentFile) {
      showAlert(t.alert_no_file, "error");
      return;
    }

    const selectedModel = document.querySelector('input[name="model-radio"]:checked').value;
    const horizon = parseInt(horizonSlider.value, 10);
    const fillGaps = fillGapsCheck.checked;
    const selectedSeries = seriesSelect.value || null;

    // UI Loading State
    setLoading(true);
    showAlert(
      t.alert_training_progress.replace("{model}", selectedModel).replace("{horizon}", horizon),
      "info"
    );

    const formData = new FormData();
    formData.append("file", currentFile);
    formData.append("horizon", horizon);
    formData.append("model", selectedModel);
    formData.append("fill_gaps", fillGaps);
    formData.append("lang", currentLang); // Pass detected or chosen language to API
    if (selectedSeries) {
      formData.append("selected_series", selectedSeries);
    }

    try {
      const response = await fetch("/api/v1/forecast", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        const errorMsg = data.detail || (data.message ? data.message : "Error during processing.");
        throw new Error(errorMsg);
      }

      lastForecastData = data;
      renderResults(data);
      showAlert(
        t.alert_success.replace("{time}", data.execution_time_seconds).replace("{model}", data.model_used),
        "success"
      );

    } catch (error) {
      console.error("Forecasting Error:", error);
      showAlert(`${t.alert_error_prefix}${error.message}`, "error");
    } finally {
      setLoading(false);
    }
  }

  // Render KPIs, Chart and Markdown Report
  function renderResults(data) {
    const t = translations[currentLang];
    const stats = data.statistics;

    // Update Series Dropdown if multiple exist
    if (data.available_series && data.available_series.length > 1) {
      seriesSelectorContainer.classList.remove("hidden");
      seriesSelect.innerHTML = data.available_series
        .map((s) => `<option value="${s}" ${s === data.series_id ? "selected" : ""}>${s}</option>`)
        .join("");
    } else {
      seriesSelectorContainer.classList.add("hidden");
    }

    // Populate KPIs
    kpiGrid.classList.remove("hidden");
    document.getElementById("kpi-hist-mean").textContent = stats.historical_mean.toLocaleString();
    document.getElementById("kpi-fore-mean").textContent = stats.forecast_mean.toLocaleString();

    const pctChangeElem = document.getElementById("kpi-pct-change");
    const trendTagElem = document.getElementById("kpi-trend-tag");
    const isUp = stats.percentage_change > 0;
    pctChangeElem.textContent = `${stats.percentage_change > 0 ? "+" : ""}${stats.percentage_change}%`;
    pctChangeElem.className = `text-xl font-bold mt-1 ${isUp ? "text-emerald-400" : "text-rose-400"}`;

    let trendLabel = stats.trend_direction;
    if (currentLang === "en") {
      if (stats.trend_direction === "ALCISTA") trendLabel = t.trend_alcista;
      else if (stats.trend_direction === "BAJISTA") trendLabel = t.trend_bajista;
      else trendLabel = t.trend_estable;
    }
    trendTagElem.textContent = `${t.trend_prefix}${trendLabel}`;
    trendTagElem.className = `text-[10px] font-semibold ${isUp ? "text-emerald-400" : "text-rose-400"}`;

    document.getElementById("kpi-cv").textContent = stats.historical_cv.toFixed(3);
    const cvDesc = stats.historical_cv < 0.2 ? t.vol_low : (stats.historical_cv < 0.5 ? t.vol_mod : t.vol_high);
    document.getElementById("kpi-cv-desc").textContent = cvDesc;

    // Update Chart Subheading
    chartSubheading.textContent = `SKU: ${data.series_id} | ${data.model_used} | ${stats.start_date} → ${stats.end_date}`;

    // Render Chart
    renderChart(data.historical, data.forecast);

    // Render Markdown Report (Dynamic language reactive switching)
    aiReportCard.classList.remove("hidden");

    // Ensure executive_reports dictionary exists
    if (!data.executive_reports) {
      data.executive_reports = {};
      data.executive_reports[currentLang] = data.executive_summary_markdown;
    }

    const targetReport = data.executive_reports[currentLang];
    if (targetReport) {
      if (window.marked) {
        markdownContent.innerHTML = window.marked.parse(targetReport);
      } else {
        markdownContent.innerText = targetReport;
      }
    } else if (data.statistics) {
      // Asynchronously fetch on-the-fly interpretation for alternate language
      markdownContent.innerHTML = `<p class="text-slate-400 italic">${
        currentLang === "es"
          ? "Actualizando informe ejecutivo en español..."
          : "Updating executive briefing in English..."
      }</p>`;

      fetch("/api/v1/interpret", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          stats: data.statistics,
          horizon: data.horizon || 14,
          model: data.model_used || "NHITS",
          lang: currentLang,
        }),
      })
        .then((res) => res.json())
        .then((resData) => {
          data.executive_reports[currentLang] = resData.executive_summary_markdown;
          if (window.marked) {
            markdownContent.innerHTML = window.marked.parse(resData.executive_summary_markdown);
          } else {
            markdownContent.innerText = resData.executive_summary_markdown;
          }
        })
        .catch((err) => {
          console.error("Translation fetch error:", err);
          if (window.marked) {
            markdownContent.innerHTML = window.marked.parse(data.executive_summary_markdown);
          } else {
            markdownContent.innerText = data.executive_summary_markdown;
          }
        });
    }

    // Show Export CSV button
    btnExportCsv.classList.remove("hidden");
  }

  // Chart.js Visualization
  function renderChart(historical, forecast) {
    const t = translations[currentLang];
    const ctx = document.getElementById("forecastChart").getContext("2d");

    // Prepare labels (chronological timestamps)
    const histLabels = historical.map((d) => d.ds);
    const foreLabels = forecast.map((d) => d.ds);
    const allLabels = [...histLabels, ...foreLabels];

    // Data points alignment
    const histSeriesData = historical.map((d) => d.y);
    const lastHistVal = histSeriesData[histSeriesData.length - 1];

    const foreSeriesData = [
      ...new Array(histLabels.length - 1).fill(null),
      lastHistVal,
      ...forecast.map((d) => d.y_hat),
    ];

    const upperBand = [
      ...new Array(histLabels.length - 1).fill(null),
      lastHistVal,
      ...forecast.map((d) => d.y_hat_upper),
    ];

    const lowerBand = [
      ...new Array(histLabels.length - 1).fill(null),
      lastHistVal,
      ...forecast.map((d) => d.y_hat_lower),
    ];

    if (chartInstance) {
      chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels: allLabels,
        datasets: [
          {
            label: t.chart_historical_label,
            data: histSeriesData,
            borderColor: "#6366f1", // Indigo
            backgroundColor: "rgba(99, 102, 241, 0.1)",
            borderWidth: 2,
            pointRadius: 2,
            pointHoverRadius: 5,
            fill: false,
            tension: 0.1,
          },
          {
            label: t.chart_forecast_label,
            data: foreSeriesData,
            borderColor: "#06b6d4", // Cyan
            borderDash: [6, 4],
            borderWidth: 2.5,
            pointRadius: 3,
            pointHoverRadius: 6,
            pointBackgroundColor: "#06b6d4",
            fill: false,
            tension: 0.1,
          },
          {
            label: t.chart_upper_label,
            data: upperBand,
            borderColor: "transparent",
            backgroundColor: "rgba(6, 182, 212, 0.12)",
            fill: "+1",
            pointRadius: 0,
            tension: 0.1,
          },
          {
            label: t.chart_lower_label,
            data: lowerBand,
            borderColor: "transparent",
            backgroundColor: "transparent",
            fill: false,
            pointRadius: 0,
            tension: 0.1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: "index",
          intersect: false,
        },
        plugins: {
          legend: {
            position: "top",
            labels: {
              color: "#94a3b8",
              font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 },
              filter: (item) => !item.text.includes("(CI)") && !item.text.includes("(IC)"),
            },
          },
          tooltip: {
            backgroundColor: "rgba(15, 23, 42, 0.95)",
            titleColor: "#f8fafc",
            bodyColor: "#cbd5e1",
            borderColor: "#334155",
            borderWidth: 1,
            padding: 10,
            cornerRadius: 8,
          },
        },
        scales: {
          x: {
            grid: { color: "rgba(51, 65, 85, 0.3)" },
            ticks: {
              color: "#64748b",
              maxTicksLimit: 12,
              font: { family: "'Plus Jakarta Sans', sans-serif", size: 10 },
            },
          },
          y: {
            grid: { color: "rgba(51, 65, 85, 0.3)" },
            ticks: {
              color: "#64748b",
              font: { family: "'Plus Jakarta Sans', sans-serif", size: 10 },
            },
            title: {
              display: true,
              text: t.chart_y_axis,
              color: "#64748b",
              font: { size: 10 },
            },
          },
        },
      },
    });
  }

  // Export Forecast to CSV
  btnExportCsv.addEventListener("click", () => {
    if (!lastForecastData || !lastForecastData.forecast) return;

    const rows = [
      ["unique_id", "ds", "y_hat", "y_hat_lower", "y_hat_upper", "model_used"],
    ];

    lastForecastData.forecast.forEach((pt) => {
      rows.push([
        pt.unique_id,
        pt.ds,
        pt.y_hat,
        pt.y_hat_lower || "",
        pt.y_hat_upper || "",
        lastForecastData.model_used,
      ]);
    });

    const csvContent = "data:text/csv;charset=utf-8," + rows.map((e) => e.join(",")).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `forecast_${lastForecastData.series_id}_${lastForecastData.model_used}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });

  // UI Helpers
  function setLoading(isLoading) {
    const t = translations[currentLang];
    if (isLoading) {
      btnRunForecast.disabled = true;
      btnRunText.textContent = t.btn_processing;
      if (window.lucide) window.lucide.createIcons();
    } else {
      btnRunForecast.disabled = false;
      btnRunText.textContent = t.btn_train_infer;
      if (window.lucide) window.lucide.createIcons();
    }
  }

  function showAlert(message, type = "info") {
    statusAlert.classList.remove("hidden", "bg-emerald-500/10", "border-emerald-500/20", "text-emerald-300",
      "bg-rose-500/10", "border-rose-500/20", "text-rose-300", "bg-indigo-500/10", "border-indigo-500/20", "text-indigo-300");

    let styleClasses = "bg-indigo-500/10 border border-indigo-500/20 text-indigo-300";
    let iconName = "info";

    if (type === "success") {
      styleClasses = "bg-emerald-500/10 border border-emerald-500/20 text-emerald-300";
      iconName = "check-circle-2";
    } else if (type === "error") {
      styleClasses = "bg-rose-500/10 border border-rose-500/20 text-rose-300";
      iconName = "alert-circle";
    }

    statusAlert.className = `rounded-xl p-4 text-xs flex items-center space-x-3 transition ${styleClasses}`;
    statusAlert.innerHTML = `
      <i data-lucide="${iconName}" class="w-4 h-4 flex-shrink-0"></i>
      <span>${message}</span>
    `;

    if (window.lucide) {
      window.lucide.createIcons();
    }
  }
});
