# Groq-hosted models available for inference.
# Groq retiró Llama 3.3 70B y Llama 3.1 8B el 2026-08-16.
# Los nombres LLAMA_* se conservan por compatibilidad; hoy apuntan a GPT-OSS.

# High-capacity model optimized for complex reasoning,
# structured data extraction, and higher-quality responses.
LLAMA_70B = "openai/gpt-oss-120b"

# Lightweight model optimized for low latency and
# cost-efficient inference in simpler tasks.
LLAMA_8B = "openai/gpt-oss-20b"