# Citation and numeric manuscript checks

Use these tools after drafting or substantive revision. Existing lifecycle and
revision audits check records and claim links; they do not query bibliographic
databases or compare every LaTeX numeric occurrence. Keep their checks too.

## Citation authenticity

```text
python "<SKILL_DIR>/scripts/verify_citations.py" refs.bib --online --output evidence/citations.json
python "<SKILL_DIR>/scripts/verify_citations.py" refs.bib --online --provider semantic-scholar --output evidence/citations-s2.json
```

Crossref resolves DOI entries or searches literal titles; arXiv resolves arXiv
IDs; Semantic Scholar provides an optional DOI/arXiv route. Queries send only
bibliographic fields, never manuscript prose. Do not send private/unpublished
titles without authorization. Offline records/cache support local checks and
must not be described as fresh live lookup. Cache is local, 24-hour reuse;
provider requests are serial, paced and bounded, without automatic retries.

The report separates `verified_metadata`, `metadata_mismatch`, and `unresolved`.
HTTP errors, rate limits, database absence, missing metadata, ambiguous titles,
BibTeX macros and unsupported author forms remain unresolved; they do not prove
fabrication. A DOI resolving to the wrong title is a mismatch. Compare author
list/order, year and title, not just identifier existence. Initials and different
publication versions need human review; record why a year is legitimate. Do not
auto-correct a bibliography or abbreviate its title based on fuzzy matching.

Literal nested-brace/quoted BibTeX fields are supported; this is not a complete
BibTeX compiler. `@string`/concatenation need resolved input or review. Metadata
existence does not establish citation relevance, a quoted claim or the paper's
scientific truth. Read the primary source for those decisions.

Provider references: [Crossref API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/),
[arXiv API](https://info.arxiv.org/help/api/user-manual.html),
[Semantic Scholar API](https://api.semanticscholar.org/api-docs/graph).

## Numeric consistency

```text
python "<SKILL_DIR>/scripts/audit_manuscript_numbers.py" paper/main.tex --init-map number-map.csv --output evidence/number-inventory.json
python "<SKILL_DIR>/scripts/audit_manuscript_numbers.py" paper/main.tex --facts .research/06_RESULT_FACTS.csv --map number-map.csv --strict --output evidence/numbers.json
```

The first command inventories numeric literals in the main file and literal
`input/include` sources, excluding comments. The map identifies file, line,
occurrence and exact literal. Set `role=fact`, `fact_id`, field (`estimate`,
`ci_low`, `ci_high`, `denominator`, etc.), scale, display decimals and predeclared
tolerance. Percentages need explicit scale 100 when facts store proportions.
Use `role=non_result` with a reason for years, equation constants, citation keys,
units/layout sizes or configuration counts that are not result facts.

Strict mode rejects unclassified occurrences, stale locations/literals, missing
facts and mismatches; it never accepts a number merely because it appears
somewhere in the facts table. Hash the source, facts and mapping. Rounding is
decimal half-up; document any other display convention. Never widen a tolerance
to disguise a changed result. After manuscript edits, review the mapping again.

This checks source literals, not arbitrary TeX computation, generated macro
expansion, image labels or every rendered glyph. Enumerate/generated macros from
the facts layer and inspect rendered tables/figures separately. A zero exit code
with only justified non-results is not evidence of result consistency; require
`verification_complete=true` and assess the mapping's scientific meaning.

Resolve a mismatch at its source. Do not alter sealed raw results to agree with
prose; regenerate downstream tables/figures and reopen affected claims.
