# XP Treatment Experiment (With Generative AI)

This repository is for **Team B** – the treatment group. Developers **must** use ChatGPT (GPT-4) and GitHub Copilot.

## Commit Rules
- Every commit **must** explicitly declare AI usage: `[AI:YES]` or `[AI:NO]`.
- Format: `SPRINT<num>-STORY<num>-[AI:YES|NO]-<description>`
- A prompt log must be kept in `docs/prompt_log.md` for each AI interaction.

## AI Tools
- Recommended: ChatGPT (GPT-4) and GitHub Copilot.
- Document all prompts used (for traceability).

## Setup
1. Clone the repository.
2. Backend: `cd backend && pip install -r requirements.txt`
3. Frontend: `cd frontend && npm install`
4. Copy `frontend/.env.example` to `frontend/.env` and set `REACT_APP_API_URL`.
5. Run backend: `uvicorn app.main:app --reload`
6. Run frontend: `npm start`

## Data Collection
- Commits tagged with `[AI:YES]` are automatically identified in the extraction scripts.
- Run `python scripts/extract_commits.py .` after each sprint to export commit data.
- Run `python scripts/compute_metrics.py data/commits.csv` to compute throughput metrics.
