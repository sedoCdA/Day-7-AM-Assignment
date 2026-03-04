# Part C: Interview Ready

## Q1 — What is a Python Virtual Environment?

A Python virtual environment is a self-contained folder that holds its own
copy of Python and its own installed packages, completely isolated from your
system-wide Python installation.

Developers use virtual environments so each project can have its own exact
set of dependencies without conflicting with other projects. For example,
Project A might need `numpy==1.21` while Project B needs `numpy==1.26` —
virtual environments let both exist on the same machine without conflict.

Without virtual environments, installing a package for one project could
break another project that depends on a different version — this is called
"dependency hell." It also makes it harder to share your project because
colleagues won't know which packages to install.

**Real-world analogy:** Think of it like a personal work locker vs. a shared
office drawer. Your locker (virtual env) has exactly the tools you need for
your specific job. If everyone shared one drawer (system Python), things
would get cluttered, overwritten, and broken very quickly.

---

## Q2 — Fix & Improve the Code

### Original Code (with problems):
```python
import os, sys, json

def checkVersion():
    v = sys.version_info
    if v.major >= 3 and v.minor>=11:
        return "Good"
    else:
        return "Bad"

result = checkVersion()
temp = 42
print( "Version status:" , result )
```

### The 5 Issues:

1. **Multiple imports on one line** — `import os, sys, json` breaks PEP 8.
   Each import must be on its own line. `json` and `os` are also unused.
2. **camelCase function name** — `checkVersion()` should be `check_version()`
   following Python's PEP 8 snake_case naming convention.
3. **No docstring** — the function has no documentation string, which
   Pylint requires for a score above 8/10.
4. **Missing spaces in comparison** — `v.minor>=11` should be `v.minor >= 11`
   for PEP 8 spacing around operators.
5. **Unused variable** — `temp = 42` is assigned but never used anywhere,
   which Pylint flags as a warning.

### Corrected Code:
```python
"""Module to check the current Python version."""

import sys


def check_version():
    """Return 'Good' if Python 3.11 or higher, otherwise return 'Bad'."""
    v = sys.version_info
    if v.major >= 3 and v.minor >= 11:
        return "Good"
    return "Bad"


result = check_version()
print("Version status:", result)
```

---

## Q3 — Debug: ModuleNotFoundError for numpy

**Scenario:** Developer installed numpy but gets `ModuleNotFoundError: No module named 'numpy'`

### Cause 1: Installed into wrong Python (not the active venv)

`pip install numpy` may have installed numpy into system Python instead
of the active virtual environment.

**Diagnostic command:**
```bash
pip show numpy
# Check the "Location" field — does it match your venv's site-packages folder?
```

---

### Cause 2: Running script with a different Python interpreter

VS Code or the terminal may be pointing to a different Python than the
one where numpy was installed.

**Diagnostic command:**
```bash
which python      # Mac/Linux
where python      # Windows
# Compare this path to where numpy was installed
```

---

### Cause 3: Virtual environment is not activated

The venv was created and numpy installed, but the venv was not activated
before running the script so Python can't see those packages.

**Diagnostic command:**
```bash
python -c "import sys; print(sys.prefix, sys.base_prefix)"
# If both values are identical, you are NOT inside a virtual environment
```
