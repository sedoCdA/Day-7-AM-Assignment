# Day 7 — Python Development Environment Setup

## Repository Structure

| File | Description |
|------|-------------|
| `onboard.py` | Part A: 6-check onboarding script |
| `onboard_advanced.py` | Part B: Extended with argparse, disk check, timing |
| `requirements.txt` | All dependencies |
| `setup_report.txt` | Generated report from running onboard.py |
| `interview_answers.md` | Part C: Conceptual + coding answers |
| `.pylintrc` | Part D: AI-generated Pylint config |
| `ai_evaluation.md` | Part D: Critical evaluation of AI output |

## Quick Start
```bash
python -m venv onboarding_env
source onboarding_env/bin/activate  # Windows: onboarding_env\Scripts\activate
pip install -r requirements.txt
python onboard.py
```

## Advanced Usage (Part B)
```bash
python onboard_advanced.py            # basic run
python onboard_advanced.py --verbose  # show extra details
python onboard_advanced.py --fix      # auto-install missing packages
```

## Code Quality

- Black formatted
- Pylint score ≥ 8/10
- All functions have docstrings
