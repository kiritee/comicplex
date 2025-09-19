# Contributing to ComicPlex


First off, thank you for considering contributing to **ComicPlex**! 🚀


We welcome bug reports, feature requests, and pull requests.


---


## 🛠 Development Setup


1. **Fork & clone the repo**
```bash
git clone https://github.com/kiritee/comicplex.git
cd comicplex
```


2. **Install dependencies**
- Runtime only:
```bash
pip install -r requirements.txt
```
- Development:
```bash
pip install -r requirements-dev.txt
```


3. **Run tests**
```bash
pytest
```


4. **Run style checks**
```bash
black src tests
ruff check src tests
mypy src
```


---


## 📂 Project Structure
```
comicplex/
├── src/comicplex/ # main package code
├── tests/ # unit tests
├── docs/ # documentation
├── requirements.txt # runtime deps
├── requirements-dev.txt # dev deps
├── pyproject.toml # packaging config
└── CONTRIBUTING.md # this file
```


---


## ✅ Pull Request Guidelines
- Keep PRs focused — small, logical changes are easier to review.
- Include tests for new features or bug fixes.
- Run `black`, `ruff`, and `mypy` before submitting.
- Update docs if your change affects user-facing behavior.


---


## 💡 Suggestions
- File an issue first for major features so we can discuss design.
- Tag PRs with labels like `feature`, `bug`, or `docs`.


Thank you for helping make **ComicPlex** better! 🙌