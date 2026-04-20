"""
Quiz source — AI tools awareness question bank.
Mirrors news_fetcher.py's feed catalogue pattern:
  - QUESTION_BANK is the local source for the pilot.
  - Swap get_questions_for_quiz() with a real API call when ready.
"""

import hashlib
import random


def _qid(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:12]


QUESTION_BANK: list[dict] = [
    {
        "question": "Which company developed the Claude AI assistant?",
        "option_a": "OpenAI",
        "option_b": "Google",
        "option_c": "Anthropic",
        "option_d": "Meta",
        "correct": "c",
        "explanation": "Claude is developed by Anthropic, an AI safety company founded in 2021 by former OpenAI researchers including Dario and Daniela Amodei.",
        "category": "text-generation",
    },
    {
        "question": "GitHub Copilot is primarily used as a tool for?",
        "option_a": "Generating images from text prompts",
        "option_b": "AI-powered code completion and generation",
        "option_c": "Video editing with AI",
        "option_d": "Translating documents automatically",
        "correct": "b",
        "explanation": "GitHub Copilot is an AI pair programmer that suggests code completions and generates entire functions, powered by OpenAI Codex and later GPT-4.",
        "category": "coding",
    },
    {
        "question": "Midjourney is best described as a tool for?",
        "option_a": "AI-generated images from text descriptions",
        "option_b": "Writing long-form articles automatically",
        "option_c": "Transcribing audio to text",
        "option_d": "Automating spreadsheet tasks",
        "correct": "a",
        "explanation": "Midjourney is a generative AI image tool that creates high-quality artwork and photorealistic visuals from natural language text prompts.",
        "category": "image-generation",
    },
    {
        "question": "Which AI tool is best known for web search with real-time cited answers?",
        "option_a": "Claude",
        "option_b": "Perplexity AI",
        "option_c": "Stable Diffusion",
        "option_d": "ElevenLabs",
        "correct": "b",
        "explanation": "Perplexity AI is an AI-powered search engine that delivers direct answers with cited web sources, combining LLM capabilities with real-time search.",
        "category": "ai-search",
    },
    {
        "question": "DALL-E is an AI image generation model created by?",
        "option_a": "Google",
        "option_b": "Stability AI",
        "option_c": "Microsoft",
        "option_d": "OpenAI",
        "correct": "d",
        "explanation": "DALL-E is developed by OpenAI. DALL-E 3 is integrated into ChatGPT and is one of the leading text-to-image generation models.",
        "category": "image-generation",
    },
    {
        "question": "What kind of tool is Cursor?",
        "option_a": "A video generation platform",
        "option_b": "An AI-enhanced code editor",
        "option_c": "A voice cloning tool",
        "option_d": "An email automation assistant",
        "correct": "b",
        "explanation": "Cursor is an AI-first code editor built on VS Code that integrates chat, code generation, and intelligent editing directly into the development environment.",
        "category": "coding",
    },
    {
        "question": "Google's AI assistant was renamed from Bard to which name in February 2024?",
        "option_a": "LaMDA",
        "option_b": "Vertex AI",
        "option_c": "Gemini",
        "option_d": "Duet AI",
        "correct": "c",
        "explanation": "Google renamed its AI assistant from Bard to Gemini in February 2024, aligning it with the underlying Gemini family of multimodal AI models.",
        "category": "text-generation",
    },
    {
        "question": "ElevenLabs is primarily known for which AI capability?",
        "option_a": "Generating 3D models from text",
        "option_b": "AI voice synthesis and voice cloning",
        "option_c": "Real-time language translation",
        "option_d": "AI-powered financial forecasting",
        "correct": "b",
        "explanation": "ElevenLabs specializes in AI voice technology — it can clone voices and generate natural-sounding speech in multiple languages, widely used for content and accessibility.",
        "category": "voice-audio",
    },
    {
        "question": "What is Hugging Face primarily known as in the AI ecosystem?",
        "option_a": "An open-source ML model hub and community platform",
        "option_b": "A cloud GPU rental service",
        "option_c": "An AI hardware manufacturer",
        "option_d": "A proprietary LLM provider",
        "correct": "a",
        "explanation": "Hugging Face is the leading open-source AI platform hosting thousands of models, datasets, and demo Spaces, and maintains the widely used Transformers library.",
        "category": "ml-platforms",
    },
    {
        "question": "OpenAI's Whisper model is specialized for which task?",
        "option_a": "Speech recognition and audio transcription",
        "option_b": "Image generation from text",
        "option_c": "Music composition",
        "option_d": "Video subtitle generation",
        "correct": "a",
        "explanation": "Whisper is OpenAI's open-source automatic speech recognition system that transcribes and translates audio in dozens of languages with high accuracy.",
        "category": "voice-audio",
    },
    {
        "question": "What is Meta's flagship open-source large language model family called?",
        "option_a": "Falcon",
        "option_b": "LLaMA",
        "option_c": "Mixtral",
        "option_d": "Phi",
        "correct": "b",
        "explanation": "LLaMA (Large Language Model Meta AI) is Meta's family of open-source foundation models. LLaMA 3 is widely used for research, fine-tuning, and local deployment.",
        "category": "text-generation",
    },
    {
        "question": "Microsoft Copilot is deeply integrated into which platform?",
        "option_a": "Google Workspace",
        "option_b": "Salesforce CRM",
        "option_c": "Microsoft 365 (Word, Excel, Teams, Outlook)",
        "option_d": "Adobe Creative Cloud",
        "correct": "c",
        "explanation": "Microsoft Copilot is embedded across Microsoft 365 apps helping users draft documents, analyze data in Excel, summarise Teams meetings, and compose emails in Outlook.",
        "category": "productivity",
    },
    {
        "question": "Runway is an AI tool primarily used for?",
        "option_a": "Writing marketing copy",
        "option_b": "AI video generation and editing",
        "option_c": "Generating 3D architectural designs",
        "option_d": "Automating customer support",
        "correct": "b",
        "explanation": "Runway is an AI creative suite known for its Gen-2 and Gen-3 text-to-video models, widely used by filmmakers and creators for AI-assisted video production.",
        "category": "video-generation",
    },
    {
        "question": "NotebookLM, developed by Google, is best used for?",
        "option_a": "Writing code using AI",
        "option_b": "Chatting with and summarising your own documents",
        "option_c": "Generating realistic human faces",
        "option_d": "Automating social media posts",
        "correct": "b",
        "explanation": "NotebookLM lets you upload your own documents and ask questions grounded in them, generating summaries and insights from your specific sources rather than generic knowledge.",
        "category": "productivity",
    },
    {
        "question": "LangChain is a framework primarily used for?",
        "option_a": "Training custom vision models",
        "option_b": "Deploying AI models on edge devices",
        "option_c": "Building applications powered by large language models",
        "option_d": "Managing cloud GPU clusters",
        "correct": "c",
        "explanation": "LangChain is an open-source framework that simplifies building LLM-powered applications by providing tools for prompt chaining, data integration, and AI agent creation.",
        "category": "agent-frameworks",
    },
    {
        "question": "Stable Diffusion is best described as?",
        "option_a": "A proprietary text-to-image model by Adobe",
        "option_b": "An open-source text-to-image generation model",
        "option_c": "Google's image generation API",
        "option_d": "An image upscaling tool by NVIDIA",
        "correct": "b",
        "explanation": "Stable Diffusion is an open-source image generation model by Stability AI. Being open-source, it can run locally and has spawned thousands of fine-tuned community variants.",
        "category": "image-generation",
    },
    {
        "question": "AutoGen is a multi-agent AI framework developed by?",
        "option_a": "OpenAI",
        "option_b": "Microsoft Research",
        "option_c": "Google DeepMind",
        "option_d": "Hugging Face",
        "correct": "b",
        "explanation": "AutoGen is an open-source framework from Microsoft Research that enables building multi-agent AI systems where multiple agents collaborate to solve complex tasks.",
        "category": "agent-frameworks",
    },
    {
        "question": "Adobe Firefly is Adobe's AI tool focused on?",
        "option_a": "AI code review and debugging",
        "option_b": "Predictive analytics for marketing",
        "option_c": "Generative AI for creative content — images, text effects, and video",
        "option_d": "Real-time document translation",
        "correct": "c",
        "explanation": "Adobe Firefly is integrated into Photoshop, Illustrator, and Premiere Pro, letting creators generate images, apply generative fills, and create text effects using AI.",
        "category": "image-generation",
    },
    {
        "question": "Which company created the Mistral family of open-source language models?",
        "option_a": "Meta",
        "option_b": "Mistral AI — a French AI startup",
        "option_c": "Amazon AWS",
        "option_d": "Cohere",
        "correct": "b",
        "explanation": "Mistral AI is a French startup founded in 2023 that has released efficient open-source models including Mistral 7B and Mixtral 8x7B, known for strong performance at smaller sizes.",
        "category": "text-generation",
    },
    {
        "question": "Tabnine is an AI tool specifically designed for?",
        "option_a": "Generating marketing emails",
        "option_b": "Code completion across multiple IDEs",
        "option_c": "AI-assisted design prototyping",
        "option_d": "Database query optimization",
        "correct": "b",
        "explanation": "Tabnine is an AI code completion tool that integrates with VS Code, JetBrains, and other IDEs, offering both cloud and local model options for privacy-conscious teams.",
        "category": "coding",
    },
]

# Attach IDs to all questions at module load
for _q in QUESTION_BANK:
    _q["id"]     = _qid(_q["question"])
    _q["source"] = "local"


def get_all_questions() -> list[dict]:
    return list(QUESTION_BANK)


def get_questions_for_quiz(n: int = 7, seed: int | None = None) -> list[dict]:
    """Return n questions for a daily quiz. Seed by date for daily consistency."""
    pool = list(QUESTION_BANK)
    rng = random.Random(seed)
    rng.shuffle(pool)
    return pool[:n]
