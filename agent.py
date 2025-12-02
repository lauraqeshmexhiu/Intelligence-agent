import json
from pathlib import Path
from typing import List, Dict, Any

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent


# -------- Global metadata cache -------- #

METADATA: List[Dict[str, Any]] = []


# -------- Load metadata -------- #

def load_metadata(metadata_dir: str | Path) -> List[Dict[str, Any]]:
    global METADATA
    metadata_dir = Path(metadata_dir)
    repos = []

    for file_path in metadata_dir.glob("*.json"):
        with file_path.open("r", encoding="utf-8") as f:
            repos.append(json.load(f))

    METADATA = repos
    return repos


# -------- Tools -------- #

@tool
def list_repos_using_docker() -> str:
    """List repos that have a Dockerfile."""
    if not METADATA:
        return "No metadata loaded."
    names = [r["name"] for r in METADATA if r.get("has_dockerfile")]
    return "Repositories using Docker:\n- " + "\n- ".join(names) if names else "None"


@tool
def list_repos_missing_tests() -> str:
    """List repos missing test files."""
    if not METADATA:
        return "No metadata loaded."
    names = [r["name"] for r in METADATA if not r.get("has_tests")]
    return "Repositories missing tests:\n- " + "\n- ".join(names) if names else "None"


@tool
def list_most_active_repos() -> str:
    """List repos with the most commits in the last 30 days, in a user-friendly format."""
    if not METADATA:
        return "No metadata loaded."

    sorted_repos = sorted(
        METADATA,
        key=lambda r: r.get("commits_last_30_days", 0),
        reverse=True,
    )

    if not sorted_repos:
        return "No active repositories found."

    # Format into a user-friendly sentence
    repo_strings = [
        f"{r['name']} ({r.get('commits_last_30_days', 0)} commits)" for r in sorted_repos
    ]
    return f"The most active repositories are: {', '.join(repo_strings)}."


TOOLS = [list_repos_using_docker, list_repos_missing_tests, list_most_active_repos]


# -------- Agent Builder (LangChain v1) -------- #

def create_repo_agent(metadata_dir: str | Path):
    # Load metadata first
    load_metadata(metadata_dir)

    # Chat model
    llm = ChatOllama(model="llama3.1", temperature=0.0)

    # agent builder
    agent_graph = create_agent(
        model=llm,
        tools=TOOLS,
        system_prompt="You are an assistant for answering questions about code repositories. "
                     "You have access to tools that can help you find information about repositories. "
                     "ALWAYS use the available tools to answer questions about repositories rather than "
                     "making up information. Use the tools to get accurate, up-to-date information."
    )

    return agent_graph


def run_agent_question(metadata_dir: str | Path, question: str) -> str:
    agent_graph = create_repo_agent(metadata_dir)
    response = agent_graph.invoke({"messages": [{"role": "user", "content": question}]})
    # Get the last message from the agent
    return response["messages"][-1].content
