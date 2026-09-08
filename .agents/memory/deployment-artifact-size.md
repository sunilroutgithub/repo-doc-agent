---
name: Deployment artifact size
description: Durable guidance for Python dependency footprint and Replit Autoscale promotion.
---

For this Groq-only FastAPI app, CrewAI does not require the direct Torch, Transformers, sentence-transformers, FAISS, SciPy, or CUDA dependency chain. Keeping those roots in requirements can make `.pythonlibs` multi-gigabyte and cause Replit layer archive or Autoscale promotion failures.

**Why:** Recent builds failed while archiving `.pythonlibs` or stopped after image creation, leaving the previous successful deployment serving old code.

**How to apply:** Keep only runtime dependencies needed by the application, remove orphaned installed payloads and pip caches after changing the manifest, run `pip check`, and verify the package layer before publishing.