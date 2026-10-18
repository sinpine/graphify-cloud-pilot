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
# Phase 2: Lantern parcel ledger

Synthetic Python application for controlled code-retrieval evaluation. It uses
only generated customer labels and in-memory SQLite. No credentials, real user
data, network services, CI hooks or production source are included.

The Lantern package covers order placement through an HTTP-shaped adapter, JSON
CLI and CSV import, customer-key normalization, pricing and vouchers, delivery
estimates, transactional order/audit persistence, refunds and revenue reports.
`lantern/policy.toml` holds non-secret policy values. Compatibility and preview
helpers intentionally have similar names to active implementations.

`submit_refund` deliberately contains a characterized double-conversion defect
for cause-investigation exercises. Its reproducer asserts the observed error;
the passing test suite does not mean this deliberate defect is fixed.

Run `python3 -m unittest discover -s tests -v`. Databases live in memory in the
tests. The original Phase 1 fixture remains for historical comparison.

