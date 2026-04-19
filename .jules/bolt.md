## 2024-04-15 - Optimize URL parameter encoding with list-type fields
**Learning:** Python's `urllib.parse.urlencode` accepts a `doseq=True` parameter that natively and optimally handles dict values that are lists by emitting repeating keys (e.g., `fields[]=a&fields[]=b`). A custom iteration with `urlencode` + `&`.join for this exact behavior is significantly slower.
**Action:** Always utilize `doseq=True` in `urlencode` rather than writing a custom loop when query string values can contain lists.
## 2026-04-17 - Optimize list filtering by avoiding list.remove in a loop\n**Learning:** Python list `.remove()` operation has O(n) complexity. Using it inside a loop to filter elements results in O(n²) complexity, which becomes a severe bottleneck for large lists.\n**Action:** Use O(n) list comprehensions to build a new list of valid items instead of mutating the original list with `.remove()` when filtering.

## 2024-04-18 - Optimize parsing of API datetime fields
**Learning:** Using `dateutil.parser.parse` directly on strings is notably slow due to its extensive flexibility and generic fallback parsing mechanisms. Using the standard library `datetime.fromisoformat` first provides a massive parsing speedup (often ~10x) for compliant ISO strings, which is critical when deserializing large JSON models with many date fields.
**Action:** Add a fast path using `datetime.fromisoformat(string.replace('Z', '+00:00'))` before falling back to `dateutil.parser.parse` for datetime parsing routines.
## 2024-04-19 - Optimize regex matching in loops
**Learning:** Calling `re.search(pattern, string)` with string patterns repeatedly inside large loops forces redundant pattern compilation overhead. Pre-compiling patterns into `re.Pattern` objects using `re.compile()` and calling `.search(string)` directly provides up to a ~4x performance boost.
**Action:** Always pre-compile regular expressions using `re.compile()` when they are defined as class constants and used in iterative parsing routines.
