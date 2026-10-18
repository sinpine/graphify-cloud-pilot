# Graphify Cloud public evaluation fixture

Synthetic, non-production Python code for checking symbol search, call paths,
change impact, linked tests and natural-language retrieval in Graphify Cloud.
Contains no private code, personal data, credentials or external service calls.

Run: `python3 -m unittest discover -s tests -v`

Flow: `checkout -> calculate_total -> calculate_subtotal -> normalise_quantity`.
`calculate_total` also calls `apply_discount`. `checkout` creates a `Receipt`.

Graphify use is indexing and read-only queries only. Automatic PR review,
fix suggestions, formal verification, code writes and Checks updates are not
part of this evaluation. No hooks, workflows or scheduled tasks are included.
