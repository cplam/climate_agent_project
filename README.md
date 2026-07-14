
# 🌦️ Climate AI Agent

**Climate AI Agent** is a multi‑agent system powered by large language models (DeepSeek V3 / GPT‑5) that automates the entire climate science workflow: from a natural‑language question to data acquisition, analysis, visualisation, and report generation.

Simply ask a climate‑related question (e.g., *“Analyse the global average temperature change over the last 10 years”*) and the system will:

1. **Decompose the task** (Planner Agent)  
2. **Acquire or simulate data** (Data Fetcher Agent)  
3. **Generate analysis code** (Coder Agent)  
4. **Optionally execute the code** to produce charts and numerical results  
5. **Write a structured scientific report** (Reporter Agent)

All outputs (data, figures, reports) are saved in the `outputs/` directory for easy inspection and sharing.

---

## 📦 Project Structure

```
climate_agent_project/
├── config/                     # Configuration files (agent roles, data source APIs)
├── src/
│   ├── agents/                 # Multi‑agent core (planner, data, coder, reporter)
│   ├── tools/                  # Toolset (data download, statistics, visualisation)
│   ├── memory/                 # Vector memory module (optional)
│   └── utils/                  # Utilities (LLM client, logger)
├── benchmarks/                 # Benchmark suite (ClimaBench)
├── tests/                      # Unit tests
├── notebooks/                  # Jupyter notebooks for exploratory analysis
├── outputs/                    # All runtime outputs (data, figures, reports, logs)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Quick Start

### 1. Clone the repository and enter the directory
```bash
git clone <your-repo-url>
cd climate_agent_project
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate          # Linux/macOS
# or venv\Scripts\activate       # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your API key
By default, the project uses the **Aihubmix** proxy to access DeepSeek models.  
Edit `src/utils/llm_client.py` and replace `DEEPSEEK_API_KEY` with your own valid key:

```python
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

> If you are using the official DeepSeek API, change `BASE_URL` to `https://api.deepseek.com/v1` and set `DEFAULT_MODEL` to `deepseek-chat`.

### 5. Run an example
Launch a complete climate analysis task with the following command:
```bash
python3 -c "from src.utils.llm_client import DeepSeekClient; from src.agents.orchestrator import OrchestratorAgent; agent = OrchestratorAgent(DeepSeekClient()); print(agent.process('Analyse the global average temperature change over the last 10 years')['report']['report'])"
```

You can replace the question with any climate‑related query, e.g.:
- “Analyse the trend of Arctic sea ice extent”
- “Evaluate summer precipitation changes in eastern China over the past decade”
- “Compare global temperature anomalies across different datasets”

---

## 🧪 Enable Code Execution (to produce real charts and numbers)

For safety, code execution is turned **off** by default. To actually run the generated code and obtain figures and numerical results, set the environment variable before running:

```bash
export EXECUTE_CODE=1
python3 -c "your_command_here"
```

After a successful run:
- A trend chart will be saved in `outputs/figures/temperature_trend.png`
- The report will contain concrete values (e.g., trend slope, R², p‑value)

---

## 📊 Outputs Explained

After execution, the `outputs/` directory will contain:

| Path | Contents |
|------|----------|
| `outputs/data/` | Downloaded or simulated data (CSV/NetCDF) |
| `outputs/figures/` | Visualisation charts (PNG) |
| `outputs/reports/` | Complete Markdown scientific report |
| `outputs/logs/` | Runtime logs (for debugging) |

---

## 🛠️ Customisation & Extension

- **Add a new data source**: implement the interface in `src/tools/data_sources/` and update `config/data_sources.yaml`.
- **Tweak agent behaviour**: edit `config/agent_config.yaml` to modify system prompts or model parameters.
- **Connect to real climate data**: configure the CDS API key in `src/tools/data_sources/cds_api.py` (you need a Copernicus account). The system will then automatically download ERA5 data instead of using simulations.

---

## 🧪 Testing & Benchmarking

Run unit tests:
```bash
pytest tests/
```

Run the benchmark suite (ClimaBench):
```bash
python3 benchmarks/clima_bench.py
```

---

## ❓ Frequently Asked Questions

### Q: The report always uses the default template – no dynamic content is generated.
- Ensure the API key in `src/utils/llm_client.py` is valid and the model name is correct (`gpt-5` or `deepseek-chat`).
- Check network connectivity to `aihubmix.com/v1` or the official DeepSeek endpoint.
- Try simplifying the prompts (the system already falls back to defaults, but dynamic generation requires a successful model response).

### Q: I get `ModuleNotFoundError` when executing code.
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Some optional dependencies (e.g., `cartopy`) require extra system libraries – you can ignore them if you don't use map plotting.

### Q: How do I switch to a different model?
- Change `DEFAULT_MODEL` in `llm_client.py` to another supported model name (e.g., `deepseek-v3`, `gpt-4`, depending on your proxy/service).

---

## 🤝 Contributing

Issues and pull requests are welcome! Help us improve this climate‑science agent toolkit.

## 📄 License

MIT License
```