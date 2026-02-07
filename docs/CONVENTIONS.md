# ❗ CODING CONVENTIONS ❗

### 1. Our Philosophy

We prioritize **readability, maintainability, and safety** over cleverness. Our goal is a unified codebase where any engineer can step into any file and feel at home.

### 2. Base Conventions

We adhere to the **Google Style Guides**:

* **C++:** [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
* **Python:** [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### 3. The Toolchain (Automatic Enforcement)

Consistency is enforced automatically. If your code isn't formatted correctly, **the CI will fail.**

* **Formatting:** `clang-format` (C++), `yapf` (Python)
* **Linting:** `cpplint` (C++), `pylint` (Python)
* **Enforcement:** We use `pre-commit` hooks. Run `pre-commit install` after cloning.

### 4. Local Exceptions

*Refer to [EXCEPTIONS.md](https://www.google.com/search?q=./exceptions.md) for deviations from Google's standards (e.g., our 120-character line limit).*

### 5. Manual Review Focus

During Peer Review, we ignore "syntax nits" (let the linter handle that) and focus on:

* **Naming:** Are names descriptive? (Avoid `data`, `val`, `temp`).
* **Memory:** Are we using Modern C++ ownership (`std::unique_ptr`)?
* **Pythonic Logic:** Are we avoiding "magic" methods and overly complex list comprehensions?
* **Testing:** Does every new feature have a corresponding unit test?