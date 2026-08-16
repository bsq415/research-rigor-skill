# Submission Checklist

## Policy and metadata

- [ ] Venue, year, track, deadline, and page rules rechecked from current official sources.
- [ ] Authors, affiliations, funding, conflicts, ethics, and disclosure confirmed by an authorized human.
- [ ] Anonymous and non-anonymous variants are not mixed.
- [ ] Licenses and release permissions are satisfied.

## Scientific integrity

- [ ] Every headline claim maps to sealed fact IDs.
- [ ] Strongest contrary evidence and limitations remain visible.
- [ ] No validation or test selection leak remains.
- [ ] No result is sourced from a partial, superseded, or invalid artifact.
- [ ] Citations and nearest-neighbor positioning were rechecked.
- [ ] Every formal reviewer/editor comment has a terminal remediation row, response anchor, evidence or scope boundary, exact manuscript locator, and no-regression check.
- [ ] Materially changed results are decomposed against the submitted protocol and artifacts.

## Build

- [ ] Exact source archive builds in an isolated directory.
- [ ] Build log has no fatal errors or unresolved references.
- [ ] Page count and required sections pass.
- [ ] Fonts, figures, tables, equations, and references pass mechanical checks.
- [ ] Figure assets pass final-placement checks for physical width, vector/raster format, effective DPI, embedded fonts, line and marker readability, axes, crop, caption, and color-independent encoding.
- [ ] Every rendered page was visually inspected.
- [ ] Rebuilt output agrees with the canonical PDF by approved text or hash checks.
- [ ] The response letter, revision highlights, cover letter, clean manuscript, and marked manuscript are internally consistent where required.
- [ ] `audit_revision_package.py --strict` passes for a formal revision or is explicitly marked not applicable for an initial submission.

## Privacy and packaging

- [ ] Mechanical release scan passes.
- [ ] Human semantic privacy and anonymity review passes.
- [ ] No local path, account, credential, hidden metadata, comment, or tracked change leaks.
- [ ] Upload filenames are conventional and free of internal versions.
- [ ] Source, figures, outputs, and manifest are complete and portable.
- [ ] SHA-256 manifest verifies in strict mode.

## Archive

- [ ] Canonical package is identified.
- [ ] Reproducibility artifacts and concise revision history are retained.
- [ ] Cleanup targets were read-only audited before deletion.
- [ ] Material deletion has explicit approval.
