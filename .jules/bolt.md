## 2024-04-15 - Optimize URL parameter encoding with list-type fields
**Learning:** Python's `urllib.parse.urlencode` accepts a `doseq=True` parameter that natively and optimally handles dict values that are lists by emitting repeating keys (e.g., `fields[]=a&fields[]=b`). A custom iteration with `urlencode` + `&`.join for this exact behavior is significantly slower.
**Action:** Always utilize `doseq=True` in `urlencode` rather than writing a custom loop when query string values can contain lists.
