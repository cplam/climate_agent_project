
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
