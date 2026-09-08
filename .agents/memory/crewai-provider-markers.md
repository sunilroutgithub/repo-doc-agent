---
name: CrewAI provider markers
description: Durable guidance for CrewAI cache-breakpoint compatibility with non-Anthropic providers.
---

CrewAI can add `cache_breakpoint` to messages while building agent prompts. For Groq, removing or replacing the marker function at message creation is not reliable enough; strip the field in the provider-specific LLM formatting path immediately before LiteLLM receives the messages.

**Why:** Groq rejects the Anthropic-specific field, and the marker can still be present in the final request despite an earlier global no-op patch.

**How to apply:** Prefer a scoped `LLM` subclass or provider adapter that removes `cache_breakpoint` from every formatted message for Groq only. Keep other providers' behavior unchanged.