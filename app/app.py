# =============================================================================
# SmartConsumer Insight Engine — MVP Streamlit App
# Hackathon Elas+ Tech | Ada Tech | Subtema 2: Consumo Inteligente
#
# Decisões técnicas:
#   - SQLite in-memory: zero dependências externas, replica pipeline real de dados
#   - Plotly Express/GO: gráficos interativos prontos para apresentação
#   - Scikit-learn LinearRegression: modelo simples, interpretável e suficiente
#     para demonstrar o pipeline preditivo em MVP
#   - st.cache_data: evita re-processar dados a cada interação do usuário
#   - CSS injetado via st.markdown: design system customizado sem framework
# =============================================================================

try:
    import streamlit as st
except ImportError:
    raise ImportError("Streamlit is not installed. Please run 'pip install streamlit' to resolve this.")
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np
import io

# ── Configuração global da página ────────────────────────────────────────────
st.set_page_config(
    page_title="SmartConsumer Insight Engine",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design System: CSS customizado ───────────────────────────────────────────
# Paleta inspirada nas referências: violeta profundo + ciano elétrico + branco.
# Cards com glassmorphism leve, tipografia DM Sans (Google Fonts), espaçamento
# generoso e bordas suaves para aparência enterprise/fintech.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset e base ─────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background principal ─────────────────────── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1040 40%, #24243e 100%);
    min-height: 100vh;
}

/* ── Sidebar ──────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
}
section[data-testid="stSidebar"] * { color: #e0d9ff !important; }
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #a78bfa !important;
}

/* ── Títulos e texto global ───────────────────── */
h1, h2, h3, h4 { color: #ffffff !important; font-weight: 700; }
p, li, label   { color: #c4b8f0 !important; }

/* ── Metric cards nativos do Streamlit ────────── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 16px;
    padding: 20px 24px !important;
    backdrop-filter: blur(8px);
    transition: transform .2s ease, box-shadow .2s ease;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(139,92,246,0.25);
}
[data-testid="stMetricLabel"]  { color: #a78bfa !important; font-size: .8rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; }
[data-testid="stMetricValue"]  { color: #ffffff !important; font-size: 2rem !important; font-weight: 700; }
[data-testid="stMetricDelta"]  { color: #34d399 !important; }

/* ── Caixas de alerta personalizadas ─────────── */
.alert-danger {
    background: rgba(239,68,68,.12);
    border-left: 4px solid #ef4444;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin-bottom: 12px;
    color: #fca5a5 !important;
}
.alert-warning {
    background: rgba(245,158,11,.12);
    border-left: 4px solid #f59e0b;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin-bottom: 12px;
    color: #fcd34d !important;
}
.alert-success {
    background: rgba(52,211,153,.12);
    border-left: 4px solid #34d399;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin-bottom: 12px;
    color: #6ee7b7 !important;
}

/* ── Seção de título hero ─────────────────────── */
.hero-header {
    background: linear-gradient(90deg, rgba(139,92,246,.3) 0%, rgba(6,182,212,.2) 100%);
    border: 1px solid rgba(139,92,246,.3);
    border-radius: 20px;
    padding: 32px 40px;
    margin-bottom: 32px;
    text-align: center;
}
.hero-header h1 {
    font-size: 2.4rem !important;
    background: linear-gradient(90deg, #a78bfa, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.hero-header p { color: #94a3b8 !important; font-size: 1rem; }

/* ── Predição em destaque ─────────────────────── */
.prediction-box {
    background: linear-gradient(135deg, rgba(139,92,246,.25), rgba(6,182,212,.15));
    border: 1px solid rgba(139,92,246,.4);
    border-radius: 20px;
    padding: 32px;
    text-align: center;
}
.prediction-value {
    font-size: 3.5rem;
    font-weight: 700;
    font-family: 'DM Mono', monospace;
    background: linear-gradient(90deg, #a78bfa, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.prediction-label { color: #94a3b8 !important; font-size: .9rem; letter-spacing: .1em; text-transform: uppercase; }

/* ── Divider ──────────────────────────────────── */
hr { border-color: rgba(255,255,255,0.08) !important; margin: 24px 0 !important; }

/* ── Tabelas ──────────────────────────────────── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* ── Inputs ───────────────────────────────────── */
[data-baseweb="input"] > div {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(167,139,250,0.3) !important;
    border-radius: 10px !important;
    color: white !important;
}
.stNumberInput input { color: white !important; }
.stSlider > div > div { background: rgba(167,139,250,0.3) !important; }

/* ── Botão de upload ──────────────────────────── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04);
    border: 2px dashed rgba(139,92,246,.4);
    border-radius: 16px;
    padding: 16px;
}

/* ── Section headers ──────────────────────────── */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #e0d9ff !important;
    padding: 8px 0 16px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 24px;
    letter-spacing: -.01em;
}

/* ── Badge de categoria ───────────────────────── */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: .75rem;
    font-weight: 600;
    background: rgba(139,92,246,.2);
    color: #a78bfa !important;
    border: 1px solid rgba(139,92,246,.3);
    margin-right: 6px;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)


# ── Paleta de cores Plotly alinhada ao design system ─────────────────────────
PLOTLY_COLORS   = ["#8b5cf6", "#06b6d4", "#f472b6", "#34d399", "#f59e0b",
                   "#a78bfa", "#67e8f9", "#fb7185", "#6ee7b7", "#fcd34d"]
PLOTLY_TEMPLATE = "plotly_dark"

def apply_chart_style(fig: go.Figure) -> go.Figure:
    """Aplica estilo coeso a todos os gráficos Plotly."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(family="DM Sans, sans-serif", color="#c4b8f0"),
        margin=dict(t=40, b=40, l=20, r=20),
        legend=dict(
            bgcolor="rgba(255,255,255,0.05)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1,
        ),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)")
    return fig


# ── Mapeamento flexível de colunas ────────────────────────────────────────────
# Estratégia: aceitar múltiplas convenções de nomes de coluna (inglês/português,
# snake_case/CamelCase) para tornar o MVP robusto com datasets variados.
COL_ALIASES = {
    "category":         ["category", "categoria", "Category", "Categoria"],
    "payment_method":   ["payment_method", "metodo_pagamento", "Payment_Method",
                         "PaymentMethod", "payment method"],
    "total_spent":      ["total_spent", "total_gasto", "Total_Spent", "TotalSpent",
                         "total", "valor_total", "amount", "Amount"],
    "quantity":         ["quantity", "quantidade", "Quantity", "Quantidade", "qty"],
    "unit_price":       ["unit_price", "preco_unitario", "UnitPrice", "Unit_Price",
                         "price", "Price", "preco"],
}

def resolve_column(df: pd.DataFrame, key: str) -> str | None:
    """Retorna o nome real da coluna no DataFrame, ou None se não encontrada."""
    for alias in COL_ALIASES[key]:
        if alias in df.columns:
            return alias
    # busca case-insensitive como fallback
    lower_map = {c.lower(): c for c in df.columns}
    for alias in COL_ALIASES[key]:
        if alias.lower() in lower_map:
            return lower_map[alias.lower()]
    return None


# ── Camada SQL (SQLite in-memory) ─────────────────────────────────────────────
@st.cache_data(show_spinner="⚡ Processando dados via SQL...")
def load_and_query(csv_bytes: bytes) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Decisão técnica: SQLite em memória simula um pipeline real de dados sem
    necessidade de servidor. O `@st.cache_data` garante que o processamento
    pesado ocorra apenas quando o arquivo muda (hash de bytes).
    """
    df_raw = pd.read_csv(io.BytesIO(csv_bytes))
    df_raw.columns = df_raw.columns.str.strip()

    con = sqlite3.connect(":memory:")
    df_raw.to_sql("spending", con, if_exists="replace", index=False)

    col_total    = resolve_column(df_raw, "total_spent")
    col_category = resolve_column(df_raw, "category")

    if not col_total or not col_category:
        con.close()
        return df_raw, pd.DataFrame()

    # Query SQL principal: participação percentual por categoria
    query_pct = f"""
        SELECT
            "{col_category}"          AS category,
            SUM("{col_total}")        AS total_spent,
            ROUND(
                100.0 * SUM("{col_total}") / SUM(SUM("{col_total}")) OVER (),
                2
            )                         AS pct_share
        FROM spending
        GROUP BY "{col_category}"
        ORDER BY total_spent DESC;
    """
    df_pct = pd.read_sql(query_pct, con)
    con.close()
    return df_raw, df_pct


# ── Modelo ML: Regressão Linear ───────────────────────────────────────────────
@st.cache_data(show_spinner="🤖 Treinando modelo preditivo...")
def train_model(csv_bytes: bytes):
    """
    LinearRegression como baseline: simples, interpretável e ótimo para portfólio
    pois demonstra o pipeline completo (features → treino → métrica → predição).
    Random Forest poderia melhorar o R², mas sacrifica explicabilidade no MVP.
    """
    df, _ = load_and_query(csv_bytes)
    col_qty   = resolve_column(df, "quantity")
    col_price = resolve_column(df, "unit_price")
    col_total = resolve_column(df, "total_spent")

    if not all([col_qty, col_price, col_total]):
        return None, None, None

    df_model = df[[col_qty, col_price, col_total]].dropna()
    X = df_model[[col_qty, col_price]].values
    y = df_model[col_total].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    r2 = r2_score(y_test, model.predict(X_test))
    return model, r2, (col_qty, col_price, col_total)


# ── Gerador de recomendações dinâmicas ────────────────────────────────────────
def generate_recommendations(df_pct: pd.DataFrame, df_raw: pd.DataFrame,
                              col_category: str, col_payment: str | None,
                              col_total: str) -> list[dict]:
    """
    Algoritmo de alertas baseado em regras estatísticas:
      - Vilão: categoria com >30% do gasto total → alerta vermelho
      - Crédito: se cartão de crédito representa >60% de uma categoria → alerta laranja
      - Concentração: top-2 categorias somam >70% → recomendação de diversificação
    """
    recs = []
    if df_pct.empty:
        return recs

    top = df_pct.iloc[0]
    pct = top["pct_share"]

    # Regra 1 – Vilão do orçamento
    if pct > 30:
        saving = top["total_spent"] * 0.15
        recs.append({
            "type": "danger",
            "icon": "🔴",
            "title": f"Vilão identificado: {top['category']}",
            "body": f"Representa {pct:.1f}% do gasto total. Reduzir 15% nessa categoria "
                    f"economizaria aproximadamente R$ {saving:,.2f}.",
        })

    # Regra 2 – Concentração do portfólio de gastos
    if len(df_pct) >= 2:
        top2_pct = df_pct.iloc[:2]["pct_share"].sum()
        if top2_pct > 65:
            recs.append({
                "type": "warning",
                "icon": "🟡",
                "title": "Alta concentração de gastos",
                "body": f"As 2 maiores categorias ({df_pct.iloc[0]['category']} e "
                        f"{df_pct.iloc[1]['category']}) somam {top2_pct:.1f}% do orçamento. "
                        "Diversifique para maior resiliência financeira.",
            })

    # Regra 3 – Gatilho do Crédito
    if col_payment:
        df_credit = df_raw[df_raw[col_payment].str.lower().str.contains("credit|crédito|credito", na=False)]
        if not df_credit.empty:
            credit_pct = len(df_credit) / len(df_raw) * 100
            if credit_pct > 50:
                recs.append({
                    "type": "warning",
                    "icon": "💳",
                    "title": "Dependência de cartão de crédito",
                    "body": f"{credit_pct:.1f}% das transações usam crédito. Isso pode "
                            "mascarar o valor real dos gastos mensais e dificultar o controle "
                            "da fatura. Considere limitar o crédito a categorias estratégicas.",
                })

    # Regra 4 – Efeito Sazonal (se houver coluna de data)
    date_cols = [c for c in df_raw.columns if "date" in c.lower() or "data" in c.lower()]
    if date_cols:
        try:
            df_raw["_date_parsed"] = pd.to_datetime(df_raw[date_cols[0]], errors="coerce")
            nov = df_raw[df_raw["_date_parsed"].dt.month == 11]
            avg_month = df_raw[col_total].mean()
            if not nov.empty and nov[col_total].mean() > avg_month * 1.2:
                recs.append({
                    "type": "warning",
                    "icon": "📅",
                    "title": "Pico sazonal em Novembro (Black Friday)",
                    "body": "O consumo de novembro está 20%+ acima da média mensal. "
                            "Planeje um limite de gasto antes da Black Friday.",
                })
        except Exception:
            pass

    # Regra 5 – Recomendação positiva
    if pct < 50:
        recs.append({
            "type": "success",
            "icon": "✅",
            "title": "Portfólio de gastos relativamente equilibrado",
            "body": "Nenhuma categoria domina mais de 50% do orçamento. "
                    "Continue monitorando para manter esse padrão saudável.",
        })

    return recs


# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 💡 SmartConsumer")
    st.markdown("**Insight Engine** — v1.0")
    st.markdown("---")
    st.markdown("### 📂 Fonte de Dados")

    uploaded = st.file_uploader(
        "Faça upload do CSV de transações",
        type=["csv"],
        help="Colunas esperadas: category, payment_method, total_spent, quantity, unit_price",
    )

    use_demo = st.checkbox("Usar dados de demonstração", value=True)

    st.markdown("---")
    st.markdown("### ℹ️ Sobre o Projeto")
    st.markdown("""
**Hackathon Elas+ Tech**  
Ada Tech · Subtema 2: Consumo Inteligente

**Pipeline:**  
`CSV → SQLite → Stats → ML → Insights`

**Equipe:**  
Jéssica · Juscélia · Katherina · Rozvania
    """)

    st.markdown("---")
    st.caption("⚠️ Simulação educacional. Não é aconselhamento financeiro.")


# ═════════════════════════════════════════════════════════════════════════════
# DADOS: demo ou upload
# ═════════════════════════════════════════════════════════════════════════════
def make_demo_csv() -> bytes:
    """
    Gera dataset sintético realista para demonstração sem upload.
    Reflete os padrões mencionados no README: alimentação dominante (≈68%),
    pico de novembro, dependência de crédito em lazer.
    """
    np.random.seed(42)
    n = 500
    categories = ["Alimentação", "Lazer", "Transporte", "Saúde", "Educação", "Shopping"]
    weights    = [0.38, 0.22, 0.14, 0.10, 0.08, 0.08]
    payments   = ["Credit Card", "Debit Card", "Mobile App", "Cash"]

    cat_arr = np.random.choice(categories, n, p=weights)
    pay_arr = []
    for c in cat_arr:
        if c == "Lazer":
            pay_arr.append(np.random.choice(payments, p=[0.65, 0.15, 0.12, 0.08]))
        elif c == "Alimentação":
            pay_arr.append(np.random.choice(payments, p=[0.40, 0.30, 0.20, 0.10]))
        else:
            pay_arr.append(np.random.choice(payments, p=[0.35, 0.30, 0.20, 0.15]))

    qty        = np.random.randint(1, 10, n)
    unit_price = np.random.uniform(10, 300, n).round(2)
    total      = (qty * unit_price * np.random.uniform(0.9, 1.1, n)).round(2)

    months = np.random.choice(range(1, 13), n,
                               p=[0.07,0.07,0.08,0.08,0.08,0.08,0.09,0.08,0.08,0.09,0.14,0.06])
    days   = np.random.randint(1, 28, n)
    dates  = pd.to_datetime({"year": 2023, "month": months, "day": days})

    df = pd.DataFrame({
        "date":           dates.dt.strftime("%Y-%m-%d"),
        "category":       cat_arr,
        "payment_method": pay_arr,
        "quantity":       qty,
        "unit_price":     unit_price,
        "total_spent":    total,
    })
    return df.to_csv(index=False).encode()


# Decide a fonte de dados
if uploaded:
    csv_bytes = uploaded.read()
    data_label = f"📄 {uploaded.name}"
elif use_demo:
    csv_bytes = make_demo_csv()
    data_label = "🎲 Dados de Demonstração Sintéticos"
else:
    st.markdown("""
    <div class="hero-header">
        <h1>💡 SmartConsumer Insight Engine</h1>
        <p>Faça upload de um CSV ou ative os dados de demonstração na barra lateral para começar.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── Carrega e processa ────────────────────────────────────────────────────────
df_raw, df_pct = load_and_query(csv_bytes)
model, r2_val, model_cols = train_model(csv_bytes)

col_category = resolve_column(df_raw, "category")
col_payment  = resolve_column(df_raw, "payment_method")
col_total    = resolve_column(df_raw, "total_spent")
col_qty      = resolve_column(df_raw, "quantity")
col_price    = resolve_column(df_raw, "unit_price")


# ═════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero-header">
    <h1>💡 SmartConsumer Insight Engine</h1>
    <p>Fonte ativa: <strong>{data_label}</strong> &nbsp;·&nbsp;
       {len(df_raw):,} transações carregadas &nbsp;·&nbsp;
       Pipeline E2E: Ingestão → SQL → ML → Recomendações</p>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 1 — KPIs EXECUTIVOS
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-title">📊 Visão Geral — KPIs Executivos</p>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

total_geral = df_raw[col_total].sum() if col_total else 0
media_transacao = df_raw[col_total].mean() if col_total else 0
n_categorias = df_raw[col_category].nunique() if col_category else 0

if col_payment and col_total:
    credit_mask = df_raw[col_payment].str.lower().str.contains("credit|crédito|credito", na=False)
    pct_credito = credit_mask.mean() * 100
else:
    pct_credito = 0

k1.metric("💰 Gasto Total", f"R$ {total_geral:,.2f}", help="Soma de todas as transações")
k2.metric("🧾 Ticket Médio", f"R$ {media_transacao:,.2f}", delta=None)
k3.metric("🏷️ Categorias Ativas", f"{n_categorias}", help="Categorias distintas no dataset")
k4.metric("💳 Uso de Crédito", f"{pct_credito:.1f}%", delta="risco" if pct_credito > 55 else "ok",
          delta_color="inverse" if pct_credito > 55 else "normal")

st.markdown("<br>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 2 — ANÁLISE SQL + VILÃO DO ORÇAMENTO
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-title">🦹 Vilão do Orçamento — Resultado da Query SQL</p>',
            unsafe_allow_html=True)

if df_pct.empty:
    st.warning("Não foi possível identificar as colunas 'category' e 'total_spent' no CSV.")
else:
    col_chart1, col_table = st.columns([3, 2])

    with col_chart1:
        # Gráfico de rosca: participação por categoria
        fig_donut = px.pie(
            df_pct,
            names="category",
            values="total_spent",
            hole=0.62,
            color_discrete_sequence=PLOTLY_COLORS,
            title="Participação (%) por Categoria — Query SQL",
        )
        fig_donut.update_traces(
            textposition="outside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
        )
        # Anotação central com o vilão
        top_cat  = df_pct.iloc[0]["category"]
        top_pct  = df_pct.iloc[0]["pct_share"]
        fig_donut.add_annotation(
            text=f"<b>{top_pct:.0f}%</b><br><span style='font-size:10px'>{top_cat}</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color="#ffffff"),
            align="center",
        )
        apply_chart_style(fig_donut)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_table:
        st.markdown("**Tabela SQL — `pct_share` por Categoria**")
        display_pct = df_pct.copy()
        display_pct["total_spent"]  = display_pct["total_spent"].map("R$ {:,.2f}".format)
        display_pct["pct_share"]    = display_pct["pct_share"].map("{:.2f}%".format)
        display_pct.columns         = ["Categoria", "Total Gasto", "% do Total"]
        st.dataframe(display_pct, use_container_width=True, hide_index=True,
                     height=min(50 + 38 * len(display_pct), 380))

        # Destaque do Vilão
        st.markdown(f"""
        <div style="
            background: rgba(239,68,68,.15);
            border: 1px solid rgba(239,68,68,.4);
            border-radius: 14px;
            padding: 16px 20px;
            margin-top: 16px;
        ">
            <div style="color:#ef4444; font-size:.75rem; font-weight:700;
                        letter-spacing:.08em; text-transform:uppercase;">🦹 Vilão do Orçamento</div>
            <div style="font-size:1.6rem; font-weight:700; color:#fff; margin: 6px 0;">
                {top_cat}
            </div>
            <div style="color:#fca5a5; font-size:.9rem;">
                Representa <strong>{top_pct:.1f}%</strong> do faturamento total.<br>
                Alinhado com o insight do README: <em>"Alimentação representa a maior fatia
                em 68% dos perfis."</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 3 — GATILHO DO CRÉDITO
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-title">💳 Gatilho do Crédito — Comportamento de Pagamento</p>',
            unsafe_allow_html=True)

if col_payment and col_category and col_total:
    # Agrupa por categoria + método de pagamento
    df_pay = (
        df_raw
        .groupby([col_category, col_payment])[col_total]
        .sum()
        .reset_index()
    )
    df_pay.columns = ["Categoria", "Metodo", "Total"]

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        fig_bar = px.bar(
            df_pay,
            x="Categoria",
            y="Total",
            color="Metodo",
            barmode="group",
            title="Gasto por Categoria × Método de Pagamento",
            color_discrete_sequence=PLOTLY_COLORS,
            labels={"Total": "Total Gasto (R$)", "Metodo": "Método"},
        )
        apply_chart_style(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_g2:
        # Foco em cartão de crédito vs demais
        credit_mask = df_raw[col_payment].str.lower().str.contains("credit|crédito|credito", na=False)
        df_raw["_payment_group"] = np.where(credit_mask, "💳 Crédito", "Outros Métodos")

        df_credit_cat = (
            df_raw
            .groupby([col_category, "_payment_group"])[col_total]
            .sum()
            .reset_index()
        )
        df_credit_cat.columns = ["Categoria", "Método", "Total"]

        fig_credit = px.bar(
            df_credit_cat,
            x="Categoria",
            y="Total",
            color="Método",
            barmode="stack",
            title="Crédito vs. Outros — Impacto por Categoria",
            color_discrete_map={"💳 Crédito": "#8b5cf6", "Outros Métodos": "#06b6d4"},
            labels={"Total": "Total (R$)"},
        )
        apply_chart_style(fig_credit)
        st.plotly_chart(fig_credit, use_container_width=True)

    # Insight textual do Gatilho
    if col_category:
        lazer_mask = df_raw[col_category].str.lower().str.contains("lazer|leisure|entretain|entertainment", na=False)
        df_lazer   = df_raw[lazer_mask]
        if not df_lazer.empty and col_payment in df_lazer.columns:
            credit_lazer = df_lazer[df_lazer[col_payment].str.lower().str.contains(
                "credit|crédito|credito", na=False)][col_total].sum()
            total_lazer  = df_lazer[col_total].sum()
            pct_lazer_credit = (credit_lazer / total_lazer * 100) if total_lazer > 0 else 0
            st.markdown(f"""
            <div style="background:rgba(139,92,246,.12); border:1px solid rgba(139,92,246,.3);
                        border-radius:14px; padding:16px 20px; margin-top:8px;">
                <span style="color:#a78bfa; font-weight:700;">🎯 Insight — Gatilho do Crédito em Lazer</span><br>
                <span style="color:#c4b8f0;">
                    <strong style="color:#fff;">{pct_lazer_credit:.1f}%</strong> dos gastos em Lazer
                    são feitos via cartão de crédito (R$ {credit_lazer:,.2f} de R$ {total_lazer:,.2f}).
                    Usuários tendem a gastar mais quando não sentem o dinheiro saindo imediatamente.
                </span>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Colunas de método de pagamento e/ou categoria não encontradas. "
            "Verifique o CSV para análise de crédito.")

st.markdown("<br>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 4 — CALCULADORA PREDITIVA (ML)
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-title">🤖 Calculadora Preditiva — Regressão Linear (Scikit-learn)</p>',
            unsafe_allow_html=True)

if model is None:
    st.warning("Modelo não pôde ser treinado. Verifique se o CSV contém 'quantity', "
               "'unit_price' e 'total_spent'.")
else:
    ml_left, ml_right = st.columns([2, 3])

    with ml_left:
        st.markdown("**Configure a transação para prever o gasto:**")

        qty_input   = st.number_input("🛒 Quantidade de itens",
                                       min_value=1, max_value=100, value=3, step=1)
        price_input = st.number_input("💲 Preço Unitário (R$)",
                                       min_value=1.0, max_value=5000.0, value=89.90, step=0.50,
                                       format="%.2f")

        # Predição em tempo real — sem botão, reage a cada mudança de input
        prediction = model.predict([[qty_input, price_input]])[0]
        prediction = max(0, prediction)  # garante valor não-negativo

        st.markdown(f"""
        <div class="prediction-box" style="margin-top:24px;">
            <div class="prediction-label">Gasto Previsto</div>
            <div class="prediction-value">R$ {prediction:,.2f}</div>
            <div style="color:#64748b; font-size:.8rem; margin-top:12px;">
                Baseado em {qty_input} item(ns) × R$ {price_input:.2f}<br>
                Modelo: Regressão Linear · R² = {r2_val:.3f}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Aviso interpretativo sobre R²
        if r2_val < 0.5:
            st.caption("ℹ️ R² baixo indica que o modelo captura tendência geral. "
                       "Em produção, incluir 'category' como feature melhoraria a acurácia.")
        elif r2_val >= 0.8:
            st.caption("✅ Boa acurácia preditiva. O modelo é confiável para estimativas de planejamento.")

    with ml_right:
        # Scatter: valores reais vs preditos
        if col_qty and col_price and col_total:
            df_model_viz = df_raw[[col_qty, col_price, col_total]].dropna().copy()
            df_model_viz["Previsto"] = model.predict(df_model_viz[[col_qty, col_price]].values)
            df_model_viz.columns     = ["Quantidade", "Preco_Unit", "Real", "Previsto"]

            fig_scatter = px.scatter(
                df_model_viz,
                x="Real",
                y="Previsto",
                opacity=0.55,
                title=f"Real vs. Previsto — R² = {r2_val:.3f}",
                labels={"Real": "Valor Real (R$)", "Previsto": "Valor Previsto (R$)"},
                color_discrete_sequence=["#8b5cf6"],
            )
            # Linha perfeita (y=x)
            max_val = df_model_viz[["Real", "Previsto"]].max().max()
            fig_scatter.add_trace(go.Scatter(
                x=[0, max_val], y=[0, max_val],
                mode="lines",
                line=dict(color="#06b6d4", dash="dash", width=2),
                name="Predição Perfeita",
            ))
            # Ponto do usuário
            fig_scatter.add_trace(go.Scatter(
                x=[qty_input * price_input],
                y=[prediction],
                mode="markers",
                marker=dict(color="#f472b6", size=14, symbol="star"),
                name="Sua Previsão",
            ))
            apply_chart_style(fig_scatter)
            st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 5 — RECOMENDAÇÕES ESTRATÉGICAS (STORYTELLING)
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-title">💼 Recomendações Estratégicas — Storytelling com Dados</p>',
            unsafe_allow_html=True)

recs = generate_recommendations(df_pct, df_raw, col_category or "", col_payment, col_total or "")

if not recs:
    st.info("Carregue dados para gerar recomendações automáticas.")
else:
    for rec in recs:
        css_class = f"alert-{rec['type']}"
        st.markdown(f"""
        <div class="{css_class}">
            <strong>{rec['icon']} {rec['title']}</strong><br>
            {rec['body']}
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 6 — ANÁLISE TEMPORAL (se houver data)
# ═════════════════════════════════════════════════════════════════════════════
date_cols = [c for c in df_raw.columns if "date" in c.lower() or "data" in c.lower()]
if date_cols and col_total:
    st.markdown('<p class="section-title">📅 Tendência Temporal — Efeito Sazonal</p>',
                unsafe_allow_html=True)
    try:
        df_raw["_date"] = pd.to_datetime(df_raw[date_cols[0]], errors="coerce")
        df_time = (
            df_raw.dropna(subset=["_date"])
            .groupby(df_raw["_date"].dt.to_period("M"))[col_total]
            .sum()
            .reset_index()
        )
        df_time.columns   = ["Mês", "Total"]
        df_time["Mês_str"] = df_time["Mês"].astype(str)

        fig_line = px.area(
            df_time,
            x="Mês_str",
            y="Total",
            title="Evolução Mensal dos Gastos (com destaque sazonal)",
            labels={"Mês_str": "Mês", "Total": "Total Gasto (R$)"},
            color_discrete_sequence=["#8b5cf6"],
        )
        fig_line.update_traces(
            line=dict(width=2.5),
            fillcolor="rgba(139,92,246,0.15)",
        )
        apply_chart_style(fig_line)
        st.plotly_chart(fig_line, use_container_width=True)
    except Exception:
        pass


# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 7 — DADOS BRUTOS (debug / transparência)
# ═════════════════════════════════════════════════════════════════════════════
with st.expander("🔍 Explorar Dados Brutos (Transparência do Pipeline)"):
    st.markdown(f"**Shape:** {df_raw.shape[0]} linhas × {df_raw.shape[1]} colunas")
    st.markdown(f"**Colunas detectadas:** {', '.join(df_raw.columns.tolist())}")
    st.dataframe(df_raw.head(50), use_container_width=True)


# ── Rodapé ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#475569; font-size:.8rem; padding: 8px 0 16px;">
    SmartConsumer Insight Engine · Hackathon Elas+ Tech · Ada Tech<br>
    Jéssica · Juscélia · Katherina · Rozvania &nbsp;|&nbsp;
    <em>Simulação educacional — não constitui aconselhamento financeiro real.</em>
</div>
""", unsafe_allow_html=True)