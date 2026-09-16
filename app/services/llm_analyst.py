"""LLM strategic analyst service for retail demand forecasting and inventory recommendations."""

import logging
from app.config import settings
from app.schemas.forecast import SeriesDescriptiveStats

logger = logging.getLogger(__name__)


class LLMAnalystService:
    """Interprets forecast statistics and synthesizes strategic retail insights via Gemini or Groq."""

    @classmethod
    def generate_executive_briefing(
        cls,
        stats: SeriesDescriptiveStats,
        horizon: int,
        model_used: str,
        lang: str = "en",
    ) -> str:
        """Generates a structured Markdown report using Gemini, Groq, or heuristic fallback in English or Spanish."""
        provider = settings.LLM_PROVIDER.lower()
        lang = lang.lower() if lang else "en"
        if lang not in ["en", "es"]:
            lang = "en"

        # Decide provider based on keys if auto
        if provider == "auto":
            if settings.GEMINI_API_KEY:
                provider = "gemini"
            elif settings.GROQ_API_KEY:
                provider = "groq"
            else:
                provider = "heuristic"

        logger.info(f"Generating executive report using provider='{provider}', lang='{lang}'")

        if provider == "gemini" and settings.GEMINI_API_KEY:
            try:
                return cls._call_gemini(stats, horizon, model_used, lang)
            except Exception as exc:
                logger.error(f"Gemini API error: {exc}. Falling back to heuristic briefing.")

        if provider == "groq" and settings.GROQ_API_KEY:
            try:
                return cls._call_groq(stats, horizon, model_used, lang)
            except Exception as exc:
                logger.error(f"Groq API error: {exc}. Falling back to heuristic briefing.")

        # Resilient fallback if no key or API failed
        return cls._generate_heuristic_report(stats, horizon, model_used, lang)

    @classmethod
    def _build_prompt(
        cls, stats: SeriesDescriptiveStats, horizon: int, model_used: str, lang: str = "en"
    ) -> str:
        if lang == "es":
            return f"""
Actúa como un Senior Demand Planning & Inventory Strategist en Retail de clase mundial.
Analiza los resultados del modelo de pronóstico neuronal {model_used} para el SKU/Categoría: '{stats.unique_id}'.

MÉTRICAS Y ESTADÍSTICAS DEL PROCESO:
- Horizonte Proyectado: {horizon} pasos ({stats.inferred_frequency})
- Rango Histórico: {stats.start_date} a {stats.end_date} ({stats.total_historical_points} registros)
- Media Histórica: {stats.historical_mean:.2f} unidades/periodo
- Media Proyectada: {stats.forecast_mean:.2f} unidades/periodo
- Volumen Total Proyectado ({horizon} periodos): {stats.forecast_sum:.2f} unidades
- Desviación Estándar Histórica: {stats.historical_std:.2f}
- Coeficiente de Variación (CV): {stats.historical_cv:.3f}
- Rango Histórico: Mín={stats.historical_min:.2f} | Máx={stats.historical_max:.2f}
- Cambio Porcentual Proyectado vs Histórico: {stats.percentage_change:+.2f}%
- Dirección de la Tendencia: {stats.trend_direction}

INSTRUCCIONES DE FORMATO:
Genera un informe ejecutivo estructurado en Markdown claro, profesional y orientado a la toma de decisiones inmediata de compras, logística e inventario.
Debe contener obligatoriamente las siguientes secciones:

### 1. 📊 Diagnóstico de Demanda y Tendencia
- Interpretación del cambio porcentual ({stats.percentage_change:+.2f}%) y la dirección {stats.trend_direction}.
- Análisis de la volatilidad basado en el Coeficiente de Variación ({stats.historical_cv:.3f}) indicando si la demanda es predecible, errática o intermitente.

### 2. ⚠️ Matriz de Riesgos Operativos
- **Riesgo de Quiebre de Stock (Stockout):** Severidad (Alta/Media/Baja) y justificación.
- **Riesgo de Sobrestock / Obsolescencia:** Impacto potencial en capital de trabajo y capacidad de almacenamiento.

### 3. 📦 Recomendaciones de Inventario & Safety Stock
- Políticas de inventario sugeridas (días de cobertura recomendados para cubrir {horizon} días).
- Ajuste del stock de seguridad en base a la volatilidad ({stats.historical_cv:.3f}).
- Alertas para el equipo de compras (Lead time vs ritmo de ventas proyectado).

### 4. 🎯 Estrategias Comerciales y de Distribución
- Acciones accionables para el equipo comercial (ej. promociones si la tendencia es a la baja, o fijación de precios y asignación por canal si es al alza).

Sé conciso, técnico y directo en ESPAÑOL. Usa viñetas e íconos en Markdown.
"""

        # Default: English prompt
        return f"""
Act as a world-class Senior Demand Planning & Retail Inventory Strategist.
Analyze the results from the {model_used} neural forecasting model for SKU/Category: '{stats.unique_id}'.

FORECAST & HISTORICAL METRICS:
- Forecast Horizon: {horizon} steps ({stats.inferred_frequency})
- Historical Period: {stats.start_date} to {stats.end_date} ({stats.total_historical_points} data points)
- Historical Mean: {stats.historical_mean:.2f} units/period
- Projected Mean: {stats.forecast_mean:.2f} units/period
- Total Projected Volume ({horizon} periods): {stats.forecast_sum:.2f} units
- Historical Standard Deviation: {stats.historical_std:.2f}
- Coefficient of Variation (CV): {stats.historical_cv:.3f}
- Historical Range: Min={stats.historical_min:.2f} | Max={stats.historical_max:.2f}
- Projected Percentage Delta vs Baseline: {stats.percentage_change:+.2f}%
- Inferred Trend: {stats.trend_direction}

FORMAT REQUIREMENTS:
Generate an executive briefing in Markdown that is sharp, professional, and directly actionable for supply chain, procurement, and commercial teams.
Must include the following sections:

### 1. 📊 Demand & Trend Diagnostics
- Interpretation of projected percentage change ({stats.percentage_change:+.2f}%) and direction {stats.trend_direction}.
- Volatility assessment based on Coefficient of Variation ({stats.historical_cv:.3f}), categorizing demand as smooth, erratic, or intermittent.

### 2. ⚠️ Operational Risk Matrix
- **Stockout Risk:** Severity (High/Medium/Low) and operational rationale.
- **Overstock & Carrying Cost Risk:** Working capital and warehouse space impact.

### 3. 📦 Inventory & Safety Stock Recommendations
- Target Days of Supply (DOS) recommended to cover {horizon} periods.
- Dynamic safety stock buffer adjustment based on volatility ({stats.historical_cv:.3f}).
- Procurement alerts (Supplier Lead Time vs projected run-rate).

### 4. 🎯 Commercial & Distribution Strategy
- Actionable advice for retail/category managers (e.g., promotional clearance if downward, allocation priority if upward).

Be concise, quantitative, and clear in ENGLISH. Use markdown bullet points and icons.
"""

    @classmethod
    def _call_gemini(
        cls, stats: SeriesDescriptiveStats, horizon: int, model_used: str, lang: str = "en"
    ) -> str:
        """Call Google Gemini API using google-generativeai SDK."""
        import google.generativeai as genai

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        prompt = cls._build_prompt(stats, horizon, model_used, lang)
        response = model.generate_content(prompt)
        return response.text

    @classmethod
    def _call_groq(
        cls, stats: SeriesDescriptiveStats, horizon: int, model_used: str, lang: str = "en"
    ) -> str:
        """Call Groq API using groq SDK."""
        from groq import Groq

        client = Groq(api_key=settings.GROQ_API_KEY)
        prompt = cls._build_prompt(stats, horizon, model_used, lang)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a Chief Supply Chain Officer and Retail Demand Planner."
                    if lang == "en"
                    else "Eres un Director de Cadena de Suministro y Demand Planner de Retail.",
                },
                {"role": "user", "content": prompt},
            ],
            model=settings.GROQ_MODEL,
            temperature=0.3,
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content

    @classmethod
    def _generate_heuristic_report(
        cls, stats: SeriesDescriptiveStats, horizon: int, model_used: str, lang: str = "en"
    ) -> str:
        """High-grade statistical & domain rules-based executive briefing when API keys are unconfigured."""
        if lang == "es":
            cv_desc = (
                "Baja / Muy Predecible"
                if stats.historical_cv < 0.2
                else ("Moderada" if stats.historical_cv < 0.5 else "Alta / Errática")
            )
            stockout_risk = (
                "ALTO"
                if stats.percentage_change > 10.0
                else ("MEDIO" if stats.percentage_change > 0 else "BAJO")
            )
            overstock_risk = (
                "ALTO"
                if stats.percentage_change < -10.0
                else ("MEDIO" if stats.percentage_change < 0 else "BAJO")
            )
            safety_buffer_days = round(max(3, stats.historical_cv * 14), 1)

            return f"""### 📊 Diagnóstico de Demanda y Tendencia
* **Comportamiento Proyectado:** La serie **{stats.unique_id}** presenta una tendencia **{stats.trend_direction}**, con una variación estimada de **{stats.percentage_change:+.2f}%** respecto a la línea base histórica.
* **Ritmo de Venta:** Se proyecta una venta media de **{stats.forecast_mean:.1f} unidades/{stats.inferred_frequency}** (acumulando **{stats.forecast_sum:.1f} unidades** en los próximos {horizon} periodos).
* **Volatilidad y Estabilidad:** Coeficiente de variación (CV) de **{stats.historical_cv:.3f}** (*Volatilidad {cv_desc}*). La dispersión histórica osciló entre un mínimo de **{stats.historical_min:.1f}** y un pico de **{stats.historical_max:.1f}**.

---

### ⚠️ Matriz de Riesgos Operativos
* **Riesgo de Quiebre de Stock (Stockout):** **{stockout_risk}**
  * *Impacto:* {"El incremento en la demanda proyectada puede agotar existencias si los proveedores tienen tiempos de entrega superiores a 5 días." if stats.percentage_change > 0 else "La demanda se mantiene dentro o por debajo de las cotas habituales, minimizando el riesgo de desabastecimiento inmediato."}
* **Riesgo de Sobrestock y Costo de Posesión:** **{overstock_risk}**
  * *Impacto:* {"Alerta de acumulación de producto terminado. Se recomienda no emitir órdenes de compra automáticas sin revisar la rotación de tienda." if stats.percentage_change < -5 else "Bajo riesgo de inventario ocioso; el ritmo de colocación proyectado absorberá el stock programado."}

---

### 📦 Recomendaciones de Inventario & Safety Stock
1. **Días de Cobertura Recomendados:** Mantener inventario objetivo para **{horizon + int(safety_buffer_days)} días** de consumo ({stats.forecast_sum + (stats.forecast_mean * safety_buffer_days):.0f} unidades estimadas).
2. **Buffer de Seguridad Dinámico:** Establecer un colchón de seguridad de al menos **{safety_buffer_days} días de venta** (aprox. **{stats.historical_std * 1.65:.1f} unidades** con 95% de nivel de servicio).
3. **Punto de Reorden (ROP):** Reabastecer cuando el inventario disponible sea igual a `(Lead Time × {stats.forecast_mean:.1f}) + Buffer`.

---

### 🎯 Estrategias Comerciales y de Distribución
* {"Aprovechar el impulso de demanda para asegurar asignaciones prioritarias desde el Centro de Distribución (CEDI) hacia el punto de venta." if stats.percentage_change > 0 else "Evaluar promociones cruzadas o bundle discounts para acelerar la rotación del SKU y evitar obsolescencia."}
* Monitorear semanalmente la desviación entre el pronóstico de **{model_used}** y las ventas reales para retroalimentar la frecuencia de reabastecimiento.

> *(Nota MLOps: Informe generado por motor analítico de demanda. Para habilitar insights potenciados por LLM en tiempo real, configura la variable de entorno `GEMINI_API_KEY` o `GROQ_API_KEY` en Render).*
"""

        # English Version
        cv_desc = (
            "Low / Highly Predictable"
            if stats.historical_cv < 0.2
            else ("Moderate" if stats.historical_cv < 0.5 else "High / Erratic")
        )
        stockout_risk = (
            "HIGH"
            if stats.percentage_change > 10.0
            else ("MEDIUM" if stats.percentage_change > 0 else "LOW")
        )
        overstock_risk = (
            "HIGH"
            if stats.percentage_change < -10.0
            else ("MEDIUM" if stats.percentage_change < 0 else "LOW")
        )
        safety_buffer_days = round(max(3, stats.historical_cv * 14), 1)

        trend_en = (
            "UPWARD (BULLISH)"
            if "ALCISTA" in stats.trend_direction.upper()
            else (
                "DOWNWARD (BEARISH)"
                if "BAJISTA" in stats.trend_direction.upper()
                else "STABLE / FLAT"
            )
        )

        return f"""### 📊 Demand & Trend Diagnostics
* **Projected Trajectory:** SKU **{stats.unique_id}** indicates a **{trend_en}** demand pattern, projecting a **{stats.percentage_change:+.2f}%** delta compared to the historical baseline.
* **Run-Rate:** Forecasted run-rate sits at **{stats.forecast_mean:.1f} units/{stats.inferred_frequency}** (total cumulative demand of **{stats.forecast_sum:.1f} units** across the next {horizon} periods).
* **Demand Stability:** Historical Coefficient of Variation (CV) is **{stats.historical_cv:.3f}** (*{cv_desc} Volatility*), spanning historical extremes from **{stats.historical_min:.1f}** to a peak of **{stats.historical_max:.1f}**.

---

### ⚠️ Operational Risk Matrix
* **Stockout & Service Level Risk:** **{stockout_risk}**
  * *Operational Impact:* {"Elevated projected demand surge can trigger stockouts if supplier lead times exceed 5-7 business days." if stats.percentage_change > 0 else "Demand run-rate remains safely within historical boundaries, minimizing near-term stockout threats."}
* **Overstock & Holding Cost Risk:** **{overstock_risk}**
  * *Operational Impact:* {"Potential inventory build-up risk. Avoid blanket replenishment orders without checking sell-through velocity." if stats.percentage_change < -5 else "Low risk of stranded capital; projected depletion rate will absorb scheduled arrivals."}

---

### 📦 Inventory & Safety Stock Guidelines
1. **Target Days of Supply (DOS):** Maintain stock for **{horizon + int(safety_buffer_days)} days** of cover (approx. **{stats.forecast_sum + (stats.forecast_mean * safety_buffer_days):.0f} units**).
2. **Dynamic Safety Stock Buffer:** Maintain a buffer of at least **{safety_buffer_days} days of demand** (approx. **{stats.historical_std * 1.65:.1f} units** at a 95% cycle service level).
3. **Reorder Point (ROP):** Trigger PO generation when `On-Hand + On-Order <= (Lead Time × {stats.forecast_mean:.1f}) + Buffer`.

---

### 🎯 Commercial & Channel Actions
* {"Prioritize fulfillment allocation from central DC to regional stores to capture demand upside." if stats.percentage_change > 0 else "Coordinate promotional bundling or price elasticity tests with the merchandising team to preserve SKU inventory turns."}
* Review model performance weekly comparing **{model_used}** predictions against actual POS scanner data.

> *(MLOps Note: Executive summary powered by demand analytics engine. To enable real-time generative LLM insights, configure `GEMINI_API_KEY` or `GROQ_API_KEY` in your environment).*
"""
