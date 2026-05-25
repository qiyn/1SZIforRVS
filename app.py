import random
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from deap import base, creator, tools, algorithms


# ============================================================
# DEAP CREATOR БАПТАУЫ
# ============================================================

if not hasattr(creator, "FitnessMulti"):
    creator.create(
        "FitnessMulti",
        base.Fitness,
        weights=(-1.0, 1.0, 1.0)
    )

if not hasattr(creator, "Individual"):
    creator.create(
        "Individual",
        list,
        fitness=creator.FitnessMulti
    )


# ============================================================
# БЕТ БАПТАУЛАРЫ
# ============================================================

st.set_page_config(
    page_title="SZIforRVS",
    page_icon="💹",
    layout="wide"
)


# ============================================================
# ЖАЛПЫ CSS: КӨК ТҮС + TIMES NEW ROMAN
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --main-blue: #005dac;
        --dark-blue: #1f2b44;
        --light-bg: #f1f3f7;
        --light-border: #d8dee9;
    }

    html, body, [class*="css"], [class*="st-"], div, span, label, p,
    h1, h2, h3, h4, h5, h6, button, input, textarea, section {
        font-family: "Times New Roman", Times, serif !important;
    }

    .top-blue-line {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 28px;
        background-color: var(--main-blue);
        z-index: 999999;
    }

    .block-container {
        padding-top: 55px;
    }

    [data-testid="stSidebar"] {
        background-color: var(--light-bg) !important;
        border-right: 1px solid var(--light-border) !important;
    }

    [data-testid="stSidebar"] * {
        font-family: "Times New Roman", Times, serif !important;
    }

    .stSlider label,
    .stNumberInput label {
        font-size: 15px !important;
        color: var(--dark-blue) !important;
        font-weight: 500 !important;
    }

    div[data-baseweb="slider"] {
        color: var(--main-blue) !important;
    }

    div[data-baseweb="slider"] * {
        color: var(--main-blue) !important;
        border-color: var(--main-blue) !important;
    }

    div[data-baseweb="slider"] div[role="slider"] {
        background-color: var(--main-blue) !important;
        border: 2px solid var(--main-blue) !important;
        box-shadow: none !important;
        outline: none !important;
    }

    div[data-baseweb="slider"] div[role="slider"]:hover {
        background-color: var(--main-blue) !important;
        border: 2px solid var(--main-blue) !important;
        box-shadow: 0 0 0 4px rgba(0, 93, 172, 0.20) !important;
        outline: none !important;
    }

    div[data-baseweb="slider"] div[role="slider"]:active {
        background-color: var(--main-blue) !important;
        border: 2px solid var(--main-blue) !important;
        box-shadow: 0 0 0 4px rgba(0, 93, 172, 0.25) !important;
        outline: none !important;
    }

    div[data-baseweb="slider"] div[role="slider"]:focus,
    div[data-baseweb="slider"] div[role="slider"]:focus-visible {
        background-color: var(--main-blue) !important;
        border: 2px solid var(--main-blue) !important;
        box-shadow: 0 0 0 4px rgba(0, 93, 172, 0.25) !important;
        outline: none !important;
    }

    div[data-testid="stThumbValue"] {
        color: var(--main-blue) !important;
        font-family: "Times New Roman", Times, serif !important;
        font-weight: 600 !important;
    }

    .stSlider [data-testid="stThumbValue"] {
        color: var(--main-blue) !important;
    }

    div[data-baseweb="slider"] span {
        background-color: var(--main-blue) !important;
        color: var(--main-blue) !important;
    }

    .stNumberInput input {
        font-family: "Times New Roman", Times, serif !important;
        color: var(--dark-blue) !important;
        border-color: var(--light-border) !important;
    }

    .stNumberInput input:focus {
        border-color: var(--main-blue) !important;
        box-shadow: 0 0 0 1px var(--main-blue) !important;
        outline: none !important;
    }

    .stNumberInput button,
    button[kind="stepDown"],
    button[kind="stepUp"] {
        color: var(--main-blue) !important;
        border-color: transparent !important;
        background-color: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .stNumberInput button:hover,
    button[kind="stepDown"]:hover,
    button[kind="stepUp"]:hover {
        color: var(--main-blue) !important;
        border-color: var(--main-blue) !important;
        background-color: rgba(0, 93, 172, 0.08) !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .stNumberInput button:active,
    button[kind="stepDown"]:active,
    button[kind="stepUp"]:active {
        color: var(--main-blue) !important;
        border-color: var(--main-blue) !important;
        background-color: rgba(0, 93, 172, 0.12) !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .stNumberInput button:focus,
    .stNumberInput button:focus-visible,
    button[kind="stepDown"]:focus,
    button[kind="stepUp"]:focus,
    button[kind="stepDown"]:focus-visible,
    button[kind="stepUp"]:focus-visible {
        color: var(--main-blue) !important;
        border-color: var(--main-blue) !important;
        background-color: rgba(0, 93, 172, 0.08) !important;
        box-shadow: 0 0 0 2px rgba(0, 93, 172, 0.20) !important;
        outline: none !important;
    }

    .stButton > button {
        border-radius: 8px !important;
        height: 45px !important;
        font-weight: 700 !important;
        font-family: "Times New Roman", Times, serif !important;
        color: var(--dark-blue) !important;
        border-color: var(--light-border) !important;
        box-shadow: none !important;
    }

    .stButton > button:hover {
        color: var(--main-blue) !important;
        border-color: var(--main-blue) !important;
        background-color: rgba(0, 93, 172, 0.06) !important;
        box-shadow: none !important;
    }

    .stButton > button:active {
        color: var(--main-blue) !important;
        border-color: var(--main-blue) !important;
        background-color: rgba(0, 93, 172, 0.10) !important;
        box-shadow: none !important;
    }

    .stButton > button:focus,
    .stButton > button:focus-visible {
        color: var(--main-blue) !important;
        border-color: var(--main-blue) !important;
        box-shadow: 0 0 0 2px rgba(0, 93, 172, 0.20) !important;
        outline: none !important;
    }

    input:focus,
    textarea:focus,
    select:focus {
        border-color: var(--main-blue) !important;
        box-shadow: 0 0 0 1px var(--main-blue) !important;
        outline: none !important;
    }

    [data-baseweb="input"]:focus-within {
        border-color: var(--main-blue) !important;
        box-shadow: 0 0 0 1px var(--main-blue) !important;
    }

    *:focus {
        outline-color: var(--main-blue) !important;
    }

    *:focus-visible {
        outline-color: var(--main-blue) !important;
    }
    </style>

    <div class="top-blue-line"></div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ЖОҒАРҒЫ ЛОГОТИП ЖӘНЕ ТАҚЫРЫП
# ============================================================

col_logo, col_text = st.columns([1, 5])

with col_logo:
    st.image("logo_su.png", width=100)

with col_text:
    st.markdown(
        """
        <div style="
            text-align: center;
            font-family: 'Times New Roman', Times, serif;
            color: #005dac;
            line-height: 1.20;
        ">
            <div style="
                font-size: 35px;
                margin-bottom: 15px;
                font-family: 'Times New Roman', Times, serif;
            ">
                Қ.И. Сәтбаев атындағы Қазақ ұлттық техникалық зерттеу университеті<br>
                Автоматтандыру және ақпараттық технологиялар институты
            </div>

    <div style="
                font-size: 32px;
                color: #1f2b44;
                font-weight: 500;
                line-height: 1.20;
                text-transform: uppercase;
                margin-top: 10px;
                font-family: 'Times New Roman', Times, serif;
    ">
                «БІЛІМ БЕРУ ЖҮЙЕЛЕРІ ҮШІН ЕСЕПТЕУІШ ЖЕЛІЛЕРІНІҢ 
                ҚАУІПСІЗДІГІН ҚАМТАМАСЫЗ ЕТУ ӘДІСТЕРІ, МОДЕЛЬДЕРІ 
                ЖӘНЕ АҚПАРАТТЫҚ ТЕХНОЛОГИЯЛАРЫ» ТАҚЫРЫБЫ АЯСЫНДАҒЫ 
                ЗЕРТТЕУ ЖҰМЫСЫНЫҢ НӘТИЖЕСІ.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# КӨМЕКШІ ФУНКЦИЯЛАР
# ============================================================

def generate_data(num_szi, num_nodes, seed):
    np.random.seed(seed)

    costs = np.random.randint(100, 1000, num_szi)
    reliabilities = np.random.randint(50, 500, num_szi)
    threat_coverages = np.random.uniform(0.5, 1.0, num_szi)
    node_vulnerabilities = np.random.uniform(0.1, 1.0, num_nodes)

    return costs, reliabilities, threat_coverages, node_vulnerabilities


def calculate_cost(individual, costs):
    return sum(individual[i] * costs[i] for i in range(len(individual)))


def feasible(individual, costs, budget_limit):
    return calculate_cost(individual, costs) <= budget_limit


def repair_individual(individual, costs, budget_limit):
    while not feasible(individual, costs, budget_limit):
        selected_indexes = [
            i for i, gene in enumerate(individual)
            if gene == 1
        ]

        if not selected_indexes:
            break

        index_to_remove = random.choice(selected_indexes)
        individual[index_to_remove] = 0

    return individual


def create_toolbox(
    num_szi,
    num_nodes,
    budget_limit,
    costs,
    reliabilities,
    threat_coverages,
    node_vulnerabilities,
    mutation_gene_probability
):
    toolbox = base.Toolbox()

    def evaluate(individual):
        if not feasible(individual, costs, budget_limit):
            return 10**9, 0, 0

        total_cost = calculate_cost(individual, costs)

        total_reliability = sum(
            individual[i] * reliabilities[i]
            for i in range(num_szi)
        )

        node_protection = np.zeros(num_nodes)

        for i in range(num_szi):
            if individual[i] == 1:
                node_protection += threat_coverages[i] * node_vulnerabilities

        avg_node_protection = np.mean(node_protection)

        return total_cost, total_reliability, avg_node_protection

    def constrained_mutate(individual):
        tools.mutFlipBit(individual, indpb=mutation_gene_probability)
        repair_individual(individual, costs, budget_limit)

        return individual,

    def constrained_mate(ind1, ind2):
        tools.cxTwoPoint(ind1, ind2)

        repair_individual(ind1, costs, budget_limit)
        repair_individual(ind2, costs, budget_limit)

        return ind1, ind2

    toolbox.register("attr_bool", random.randint, 0, 1)

    toolbox.register(
        "individual",
        tools.initRepeat,
        creator.Individual,
        toolbox.attr_bool,
        n=num_szi
    )

    toolbox.register(
        "population",
        tools.initRepeat,
        list,
        toolbox.individual
    )

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", constrained_mate)
    toolbox.register("mutate", constrained_mutate)
    toolbox.register("select", tools.selNSGA2)

    return toolbox


def run_nsga2(
    num_szi,
    num_nodes,
    budget_limit,
    population_size,
    offspring_size,
    generations_count,
    crossover_probability,
    mutation_probability,
    mutation_gene_probability,
    seed
):
    random.seed(seed)

    costs, reliabilities, threat_coverages, node_vulnerabilities = generate_data(
        num_szi,
        num_nodes,
        seed
    )

    toolbox = create_toolbox(
        num_szi,
        num_nodes,
        budget_limit,
        costs,
        reliabilities,
        threat_coverages,
        node_vulnerabilities,
        mutation_gene_probability
    )

    population = toolbox.population(n=population_size)

    for individual in population:
        repair_individual(individual, costs, budget_limit)

    hof = tools.ParetoFront()

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    population, log = algorithms.eaMuPlusLambda(
        population,
        toolbox,
        mu=population_size,
        lambda_=offspring_size,
        cxpb=crossover_probability,
        mutpb=mutation_probability,
        ngen=generations_count,
        stats=stats,
        halloffame=hof,
        verbose=False
    )

    result_rows = []

    for index, individual in enumerate(hof, start=1):
        total_cost, total_reliability, avg_coverage = individual.fitness.values

        if total_cost <= budget_limit:
            selected_tools = [
                f"СҚҚ-{i + 1}"
                for i, gene in enumerate(individual)
                if gene == 1
            ]

            result_rows.append({
                "№": index,
                "Жалпы шығын": total_cost,
                "Сенімділік": total_reliability,
                "Қауіптерді жабу деңгейі": avg_coverage,
                "Таңдалған құралдар": ", ".join(selected_tools),
                "Шешім коды": list(individual)
            })

    results_df = pd.DataFrame(result_rows)

    data_df = pd.DataFrame({
        "Құрал атауы": [f"СҚҚ-{i + 1}" for i in range(num_szi)],
        "Бағасы": costs,
        "Сенімділігі": reliabilities,
        "Қауіпті жабу деңгейі": threat_coverages
    })

    nodes_df = pd.DataFrame({
        "Түйін атауы": [f"Түйін-{i + 1}" for i in range(num_nodes)],
        "Осалдық деңгейі": node_vulnerabilities
    })

    return results_df, data_df, nodes_df, log


# ============================================================
# НЕГІЗГІ ИНТЕРФЕЙС
# ============================================================

st.markdown(
    """
    <div style="
        font-size: 42px;
        font-weight: 800;
        color: #1f2b44;
        margin-top: 35px;
        margin-bottom: 20px;
        font-family: 'Times New Roman', Times, serif;
    ">
        NSGA-II алгоритмі арқылы Парето оңтайландыру
    </div>

    <div style="
        font-size: 16px;
        color: #1f2b44;
        margin-bottom: 22px;
        font-family: 'Times New Roman', Times, serif;
    ">
        Бұл бағдарлама ақпаратты қорғау құралдарын таңдауға көмектеседі.
    </div>

    <div style="
        font-size: 16px;
        color: #1f2b44;
        line-height: 1.9;
        font-family: 'Times New Roman', Times, serif;
        margin-bottom: 25px;
    ">
        Мақсаттар:<br><br>
        1. <b>Жалпы шығынды азайту</b><br>
        2. <b>Сенімділікті арттыру</b><br>
        3. <b>Қауіптерді жабу деңгейін арттыру</b>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# СОЛ ЖАҚ ПАНЕЛЬ
# ============================================================

st.sidebar.header("Алгоритм параметрлері")

num_szi = st.sidebar.slider(
    "Ақпараттық қауіпсіздік құралдар саны",
    min_value=5,
    max_value=30,
    value=5,
    step=1
)

num_nodes = st.sidebar.slider(
    "Желі түйіндерінің саны",
    min_value=2,
    max_value=20,
    value=5,
    step=1
)

budget_limit = st.sidebar.number_input(
    "Бюджет шектеуі",
    min_value=100,
    max_value=50000,
    value=2000,
    step=100
)

st.sidebar.header("Генетикалық алгоритм")

population_size = st.sidebar.slider(
    "Популяция өлшемі",
    min_value=50,
    max_value=500,
    value=100,
    step=50
)

generations_count = st.sidebar.slider(
    "Ұрпақтар саны",
    min_value=10,
    max_value=300,
    value=100,
    step=10
)

crossover_probability = st.sidebar.slider(
    "Будандастыру ықтималдығы",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05
)

offspring_size = population_size * 2
mutation_probability = 0.2
mutation_gene_probability = 0.2
seed = 42


# ============================================================
# БАТЫРМАЛАР
# ============================================================

col_button_1, col_button_2 = st.columns(2)

with col_button_1:
    run_button = st.button(
        "▶️ Алгоритмді іске қосу",
        use_container_width=True
    )

with col_button_2:
    clear_button = st.button(
        "🧹 Нәтижені тазалау",
        use_container_width=True
    )

if clear_button:
    st.session_state.clear()
    st.success("Нәтижелер тазаланды.")


if run_button:
    with st.spinner("NSGA-II алгоритмі орындалып жатыр..."):
        results_df, data_df, nodes_df, log = run_nsga2(
            num_szi=num_szi,
            num_nodes=num_nodes,
            budget_limit=budget_limit,
            population_size=population_size,
            offspring_size=offspring_size,
            generations_count=generations_count,
            crossover_probability=crossover_probability,
            mutation_probability=mutation_probability,
            mutation_gene_probability=mutation_gene_probability,
            seed=seed
        )

        st.session_state["results_df"] = results_df
        st.session_state["data_df"] = data_df
        st.session_state["nodes_df"] = nodes_df
        st.session_state["log"] = log

    st.success("Алгоритм сәтті аяқталды!")


# ============================================================
# НӘТИЖЕЛЕРДІ КӨРСЕТУ
# ============================================================

if "results_df" in st.session_state:
    results_df = st.session_state["results_df"]
    data_df = st.session_state["data_df"]
    nodes_df = st.session_state["nodes_df"]
    log = st.session_state["log"]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Бастапқы деректер",
        "🏆 Парето шешімдері",
        "📈 2D графиктер",
        "🧊 3D график",
        "📉 Жақындау графигі"
    ])

    with tab1:
        st.subheader("Қорғаныс құралдарының бастапқы деректері")
        st.dataframe(data_df, use_container_width=True)

        st.subheader("Желі түйіндерінің осалдық деңгейлері")
        st.dataframe(nodes_df, use_container_width=True)

        st.info(
            """
**Бағасы** — қорғаныс құралын орнатуға кететін шығын.  
**Сенімділігі** — құралдың сапасын немесе тұрақтылығын сипаттайтын шартты көрсеткіш.  
**Қауіпті жабу деңгейі** — құралдың қауіптерді қаншалықты жабатынын көрсетеді.  
**Осалдық деңгейі** — желі түйінінің қауіпке қаншалықты бейім екенін көрсетеді.
"""
        )

    with tab2:
        st.subheader("Парето тиімді шешімдері")

        if len(results_df) == 0:
            st.warning("Бюджет шектеуіне сәйкес Парето шешімдері табылмады.")
        else:
            st.dataframe(results_df, use_container_width=True)

            cheapest = results_df.sort_values(
                by="Жалпы шығын",
                ascending=True
            ).iloc[0]

            best_reliability = results_df.sort_values(
                by="Сенімділік",
                ascending=False
            ).iloc[0]

            best_coverage = results_df.sort_values(
                by="Қауіптерді жабу деңгейі",
                ascending=False
            ).iloc[0]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Ең арзан шешім",
                    int(cheapest["Жалпы шығын"])
                )

            with col2:
                st.metric(
                    "Ең сенімді шешім",
                    int(best_reliability["Сенімділік"])
                )

            with col3:
                st.metric(
                    "Ең жоғары қауіп жабу",
                    round(best_coverage["Қауіптерді жабу деңгейі"], 3)
                )

    with tab3:
        st.subheader("2D Парето графиктері")

        if len(results_df) > 0:
            fig_2d = go.Figure()

            fig_2d.add_trace(
                go.Scatter(
                    x=results_df["Жалпы шығын"],
                    y=results_df["Сенімділік"],
                    mode="markers",
                    marker=dict(
                        size=10,
                        color=results_df["Қауіптерді жабу деңгейі"],
                        colorscale="Viridis",
                        showscale=True,
                        colorbar=dict(title="Қауіп жабу")
                    ),
                    text=results_df["Таңдалған құралдар"],
                    hovertemplate=
                    "Шығын: %{x}<br>" +
                    "Сенімділік: %{y}<br>" +
                    "Құралдар: %{text}<extra></extra>"
                )
            )

            fig_2d.update_layout(
                title="Шығын мен сенімділік арасындағы Парето фронты",
                xaxis_title="Жалпы шығын",
                yaxis_title="Сенімділік",
                font=dict(family="Times New Roman", size=14)
            )

            st.plotly_chart(fig_2d, use_container_width=True)

            fig_coverage = go.Figure()

            fig_coverage.add_trace(
                go.Scatter(
                    x=results_df["Жалпы шығын"],
                    y=results_df["Қауіптерді жабу деңгейі"],
                    mode="markers",
                    marker=dict(
                        size=10,
                        color=results_df["Сенімділік"],
                        colorscale="Viridis",
                        showscale=True,
                        colorbar=dict(title="Сенімділік")
                    ),
                    text=results_df["Таңдалған құралдар"],
                    hovertemplate=
                    "Шығын: %{x}<br>" +
                    "Қауіп жабу: %{y}<br>" +
                    "Құралдар: %{text}<extra></extra>"
                )
            )

            fig_coverage.update_layout(
                title="Шығын мен қауіптерді жабу деңгейінің байланысы",
                xaxis_title="Жалпы шығын",
                yaxis_title="Қауіптерді жабу деңгейі",
                font=dict(family="Times New Roman", size=14)
            )

            st.plotly_chart(fig_coverage, use_container_width=True)

    with tab4:
        st.subheader("Интерактивті 3D Парето графигі")

        if len(results_df) > 0:
            fig_3d = go.Figure(
                data=[
                    go.Scatter3d(
                        x=results_df["Жалпы шығын"],
                        y=results_df["Сенімділік"],
                        z=results_df["Қауіптерді жабу деңгейі"],
                        mode="markers",
                        marker=dict(
                            size=6,
                            color=results_df["Қауіптерді жабу деңгейі"],
                            colorscale="Viridis",
                            opacity=0.85,
                            colorbar=dict(title="Қауіп жабу")
                        ),
                        text=results_df["Таңдалған құралдар"],
                        hovertemplate=
                        "Шығын: %{x}<br>" +
                        "Сенімділік: %{y}<br>" +
                        "Қауіп жабу: %{z}<br>" +
                        "Құралдар: %{text}<extra></extra>"
                    )
                ]
            )

            fig_3d.update_layout(
                title="3D Парето фронты",
                scene=dict(
                    xaxis_title="Жалпы шығын",
                    yaxis_title="Сенімділік",
                    zaxis_title="Қауіптерді жабу деңгейі"
                ),
                font=dict(family="Times New Roman", size=14)
            )

            st.plotly_chart(fig_3d, use_container_width=True)

            st.info(
                """
Бұл графикті тышқанмен айналдыруға, жақындатуға және алыстатуға болады.
Әр нүкте — бір тиімді Парето шешімі.
"""
            )

    with tab5:
        st.subheader("Алгоритмнің жақындау графигі")

        generations = list(range(len(log)))

        avg_costs = [entry["avg"][0] for entry in log]
        avg_reliabilities = [entry["avg"][1] for entry in log]
        avg_coverages = [entry["avg"][2] for entry in log]

        fig_conv = go.Figure()

        fig_conv.add_trace(
            go.Scatter(
                x=generations,
                y=avg_costs,
                mode="lines",
                name="Орташа шығын"
            )
        )

        fig_conv.add_trace(
            go.Scatter(
                x=generations,
                y=avg_reliabilities,
                mode="lines",
                name="Орташа сенімділік"
            )
        )

        fig_conv.add_trace(
            go.Scatter(
                x=generations,
                y=avg_coverages,
                mode="lines",
                name="Қауіп жабудың орташа деңгейі"
            )
        )

        fig_conv.update_layout(
            title="Ұрпақтар бойынша орташа мәндердің өзгеруі",
            xaxis_title="Ұрпақ нөмірі",
            yaxis_title="Орташа мән",
            font=dict(family="Times New Roman", size=14)
        )

        st.plotly_chart(fig_conv, use_container_width=True)

else:
    st.warning(
        "Алдымен сол жақтағы параметрлерді таңдап, "
        "**Алгоритмді іске қосу** батырмасын басыңыз."
    )
