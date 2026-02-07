# ACME Corp Coding Standards

## 1. General Principles

- **Clarity over Cleverness:** Code must be readable by a junior developer.
- **No Magic Numbers:** All numbers other than 0 and 1 must be defined as named constants.

## 2. Naming Conventions

- **Python:**
  - Variables and functions must use `snake_case`.
  - Classes must use `PascalCase`.
  - Constants must be `UPPER_CASE`.
- **JavaScript:**
  - Variables and functions must use `camelCase`.
  - Classes must use `PascalCase`.
  - Constants must be `UPPER_CASE`.

## 3. Documentation

- Every function must have a docstring (Python) or JSDoc (JavaScript) explaining its purpose.
- Comments should explain _why_, not _what_.

## 4. Error Handling

- Never use bare `except:` or generic `catch (e)`. Always specify the exception type or log the error.
