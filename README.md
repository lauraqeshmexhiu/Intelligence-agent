# Repository Intelligence Agent

The Repository Intelligence Agent is a python based CLI tool that:

- Scans local Git repositories
- Extracts useful metadata(LOC, languages, tests , CI, authors, activity etc)
- Generates JSON metadata files
- Uses a LangChain Agent + local Ollama LLM to answer natural langage questions about the repositories

## Features

### Repo scanner -->
The tool collects detailed metadata for each repository, including:

- Repository name & path  
- Lines of code by language  
- Total LOC  
- Top 3 commit authors  
- Number of commits in the last 30 days  
- Presence of:
  - `README.md`  
  - `LICENSE`  
  - `Dockerfile`  
  - `tests/` directory or `_test` files  
  - GitHub Actions workflows (`.github/workflows`) 

###  AI Question Answering (LangChain + Ollama) -->

You can answer questions such as:

- “Which repositories use Docker?”  
- “Which repos are missing tests?”  
- “Which are the most active repos?”


The agent uses:

- Local metadata JSON files  
- Local LangChain tools  
- A local LLM running on Ollama (e.g., `llama3.1`)  


## Running Locally

### 1️⃣ Setup Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/lauraqeshmexhiu/Intelligence-agent.git
   cd Intelligence-agent
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Ollama**  
   Download: https://ollama.com/download

6. **Pull the Llama model**
   ```bash
   ollama pull llama3.1
   ```

---

## 💻 Running the Local CLI

### 🔍 1. Scan repositories

```bash
python main.py scan ../repos
```

This command will:

- Detect all folders inside `../repos` that contain a `.git` directory  
- Scan each repository  
- Generate metadata  
- Save JSON files into the `metadata/` folder  

---

### 💬 2. Ask the agent a question

```bash
python main.py ask metadata "Which repositories don't have tests?"
```
This will:

- Load all repository metadata from the `metadata/` folder  
- Initialize a LangChain agent using your local LLM (Ollama)  
- Allow the model to call the appropriate tools to answer your question  

For example, if you ask *"Which repositories are using Docker?"*,  
the agent will automatically call the `list_repos_using_docker` tool and return the results.







