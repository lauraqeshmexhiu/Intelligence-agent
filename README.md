# Repository Intelligence Agent

The Repository Intelligence Agent is a python based CLI tool that:

- Scans local Git repositories
- Extracts useful metadata(LOC, languages, tests , CI, authors, activity etc)
- Generates JSON metadata files
- Uses a LangChain Agent + local Ollama LLM to answer natural langage questions about the repositories

Features: 

Repo scanner
- Detects READMEs, Dockerfiles, LICENSE files  
- Detects test directories and test-style filenames  
- Detects GitHub Actions CI workflows  
- Counts lines of code per language  
- Counts commits in the last 30 days  
- Identifies top commit authors

AI Agent
Powered by LangChain + Ollama (running a local LLM).
Can answer questions such as:

- “Which repositories use Docker?”  
- “Which repos are missing tests?”  
- “Which are the most active repos?”

Running locally

1. Clone repository
2. cd Intelligence-agent
3. python3 -m venv .venv
4. source .venv/bin/activate
5. pip install -r requirements.txt
6. Install Ollama
7. Ollama pull llama3.1

Running Local CLI

1. Scan repositories: python main.py scan ../repos
This will:
- Detect all folders inside /path/to/git-repos that contain a .git directory
- Scan each repository
- Save JSON metadata files into the metadata/ folder

2. python main.py ask metadata "Which repositories are using Docker?"







