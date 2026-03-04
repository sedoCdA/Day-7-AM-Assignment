# Part D: AI-Generated .pylintrc — Critical Evaluation

## Prompt Used

> "Generate a beginner-friendly .pylintrc configuration file for a Python
> AI/ML learning project. The developer is new to Python. Disable overly
> strict rules that would discourage beginners, but keep rules that teach
> good habits like docstrings, naming conventions, and avoiding unused
> variables. Add comments explaining what each section does."

## Pylint Score After Using Config

Run: `pylint --rcfile=.pylintrc onboard.py`
Score achieved: 9.5/10

## Critical Evaluation

The AI-generated configuration showed a solid understanding of Pylint's
structure and correctly separated the file into logical sections with helpful
comments. For a beginner, having each section labelled and explained makes the
file far less intimidating than a default .pylintrc which contains hundreds
of uncommented options.

What the AI got right was disabling `C0103` (invalid-name), which would
otherwise flag standard ML variable names like `X`, `y`, and `df` as errors.
It also correctly set `max-line-length=88` to match Black's default, which
prevents the two tools from contradicting each other — a common frustration
for new developers.

However, some rules were too lenient. Disabling `C0114`
(missing-module-docstring) removes a habit beginners should build from day
one. A better approach would be to keep it enabled so students learn to
always add a short description at the top of every file.

For beginners specifically, I would add an inline comment next to every
disabled rule explaining in plain English *why* it is disabled, not just its
code name. I would also keep `W0611` (unused-import) strictly enabled since
importing things you don't use is exactly the kind of mistake Pylint should
always catch early. Overall the AI output was a strong starting point that
saved significant time, but it required careful manual review to avoid
accidentally teaching bad habits through overly relaxed rules.
