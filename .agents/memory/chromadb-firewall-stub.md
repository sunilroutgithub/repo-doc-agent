---
name: chromadb firewall stub
description: chromadb is blocked by Replit's package firewall; a local installable stub in stubs/chromadb/ satisfies crewai's dependency without hitting the firewall.
---

## Rule
Never attempt to install the real `chromadb` package on Replit. All versions return 403 from the package firewall.

## How it works
- `stubs/chromadb/` is a pip-installable package (`pyproject.toml`, `setuptools.build_meta`) declaring `name=chromadb, version=1.1.1`.
- Source lives under `stubs/chromadb/src/chromadb/` and exports every class crewai's import chain needs.
- `requirements.txt` has `./stubs/chromadb` on the line immediately before `crewai==1.15.8`, so pip installs the stub first and never tries to download the real package.
- All stub classes raise `RuntimeError` if actually called — safe because the crew runs with `memory=False`.

**Why:** crewai 1.x unconditionally imports chromadb at startup through its memory/RAG module chain even when memory is disabled. Replit's package firewall blocks all chromadb wheel downloads with 403.

**How to apply:** If crewai is upgraded and adds new chromadb imports, grep crewai's source for `from chromadb` and add any new class names to the appropriate stub file under `stubs/chromadb/src/`.
