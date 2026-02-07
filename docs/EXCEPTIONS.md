# ⚠️ Style Guide Exceptions

This document defines where our startup deviates from the [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) and [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). 

**If a rule is not explicitly mentioned here, the Google standard remains the source of truth.**

---

## 1. General Formatting

### Line Length (C++ & Python)
* **Google Rule:** 80 characters.
* **Our Exception:** **100 characters.**
* **Reasoning:** Modern monitors and IDEs comfortably handle 100 characters. This reduces "staircase" code in C++ templates and nested Python logic while remaining readable on split-screen layouts.

---

## 2. Python Specifics

### Indentation
* **Google Rule:** 2 spaces.
* **Our Exception:** **4 spaces.**
* **Reasoning:** We align with **PEP 8**, the industry standard. This ensures better compatibility with 3rd-party libraries, IDE defaults, and the broader Python ecosystem.

### Docstring Requirements
* **Google Rule:** Mandatory strict sections for every function.
* **Our Exception:** Mandatory only for **Public APIs**, **complex logic**, or **shared utilities**. 
* **Reasoning:** We prioritize "Self-Documenting Code" for internal helpers to maintain development speed.

---

## 3. C++ Specifics

### Use of Exceptions
* **Google Rule:** Banned.
* **Our Exception:** **Permitted for "Fatal" initialization errors.**
* **Reasoning:** While we prefer `std::optional` or `absl::Status` for business logic, throwing an exception during system startup (e.g., failed to bind to a port or missing config) is cleaner than manual error propagation in the boot sequence.

### Standard Library vs. Abseil
* **Google Rule:** Prefer Abseil equivalents for everything.
* **Our Exception:** **Prefer `std::` (C++20/23) whenever available.**
* **Reasoning:** We aim to minimize external dependency bloat. We only use `absl` for features not yet available in the modern standard library.

### Indentation (Matching Python)
* **Google Rule:** 2 spaces.
* **Our Exception:** **4 spaces.**
* **Reasoning:** Consistency across the stack. Using 4 spaces in both C++ and Python reduces "context-switching fatigue" for full-stack developers.