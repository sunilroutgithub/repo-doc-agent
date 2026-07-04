# 🤖 Repo Doc Agent

<div align="center">

**An AI-powered agent that automatically generates documentation and tests for Python code**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-green.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-1.3-orange.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

## 🚀 What This Agent Does

This AI agent **automatically**:
1. 📖 Reads Python files from GitHub repositories
2. 📝 Generates professional Google-style docstrings
3. 🧪 Creates comprehensive pytest unit tests
4. 🔄 Opens pull requests with all changes
5. 📚 Creates documentation files and templates

**Cut documentation and testing time by 93%!**

---

## ✨ Features

- ✅ **Automated Documentation** - Generates Google-style docstrings
- ✅ **Test Generation** - Creates pytest unit tests automatically
- ✅ **GitHub Integration** - Reads repos, creates branches, opens PRs
- ✅ **Autonomous Agent** - Works without human intervention
- ✅ **Professional Output** - Production-ready code

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | REST API for the agent |
| **LangChain + LangGraph** | ReAct agent framework |
| **Groq LLM** | Code analysis and generation |
| **PyGithub** | GitHub API integration |
| **Pytest** | Test generation |

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/sunilroutgithub/repo-doc-agent.git
cd repo-doc-agent