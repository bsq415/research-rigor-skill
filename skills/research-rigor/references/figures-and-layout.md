# Figures and Layout Protocol

Use this protocol when creating or revising plots, diagrams, tables, equations,
captions, response letters, or final manuscript pages. Venue instructions and the
official template override provisional defaults in this file.

## Design from the final placement

Do not design a figure at arbitrary screen size and shrink it at the end.

1. obtain the current official template and determine the real single-column,
   double-column, or page width;
2. choose the intended placement before plotting;
3. create or export at that physical size;
4. calculate raster effective resolution at the placed size;
5. insert the asset into the actual manuscript;
6. render the final PDF and judge legibility there, not in the source editor.

When venue rules are silent, use these only as provisional starting points that
still require human final-size review:

- axis and legend text approximately 7--8 pt at final size;
- plot lines approximately 1 pt or thicker;
- markers approximately 4 pt or larger and distinguishable without color;
- 300 dpi or more for continuous-tone raster images;
- 600 dpi or more for rasterized line art or plots.

Never upscale a low-resolution asset and describe it as higher resolution.
Effective DPI is `pixel width / placed width in inches`, not the export dialog's
nominal setting.

## Choose a format deliberately

| Content | Preferred form | Avoid |
|---|---|---|
| Curves, scatter plots, diagrams, line art, text-heavy schematics | Venue-supported vector PDF, EPS, or SVG | Screenshots, JPEG, or a raster image enlarged after export |
| Photos, microscopy, scans, natural images | TIFF or high-quality PNG at required effective DPI | Lossy recompression and undocumented enhancement |
| Heatmaps and dense raster fields | High-resolution PNG or TIFF, sometimes mixed vector/raster PDF | Millions of vector cells that make the PDF unusable |
| Composite figure | Vector container with deliberate raster panels | Copy-paste from presentation software without checking fonts and crop boxes |

EPS is useful for workflows and publishers that support it; it is not a universal
requirement. PDF is usually the more direct vector route for modern PDF-based
LaTeX builds. Always verify the venue's accepted formats and conversion path.

For vector assets:

- embed fonts and reject Type 3 fonts unless the venue explicitly permits them;
- preserve selectable text where possible;
- verify symbols survive the manuscript toolchain;
- crop the bounding box without clipping labels or markers;
- avoid transparency or layers that render differently across viewers unless
  tested in the final PDF.

For raster assets:

- retain the original uncompressed or lossless source;
- record pixel dimensions, placed dimensions, and effective DPI;
- use lossless formats for plots and text;
- do not use interpolation, sharpening, or denoising to create scientific detail
  that is absent from the source;
- disclose scientifically material image processing.

## Make every figure answer a claim

Before drawing, write one sentence:

> This figure lets the reader decide whether [claim] holds under [denominator and
> conditions].

If that sentence cannot be completed, the figure is probably decorative or
underspecified.

For result plots:

- preserve the source data and generation command beside the rendered asset;
- show uncertainty, sample count, valid denominator, and pairing where relevant;
- include the strongest baseline and the ablation that isolates the claimed
  mechanism;
- use panels only when each panel has a distinct decision role;
- make the innovation visible through a mechanism, boundary, or trade-off, not
  merely by placing the proposed curve highest;
- explain genuine non-monotonicity, saturation, or failure instead of smoothing
  it away.

For architecture diagrams:

- encode the actual signal, causal, data, or control path;
- omit tiny formulas better explained in text;
- show the actors or operating context needed to understand the problem;
- prefer a compact single-column diagram when it remains legible;
- use a double-column figure only when information density justifies the space.

## Protect visual integrity

An axis does not always need to start at zero, but its scale must not manufacture
the impression of a large effect.

- Use zero or a meaningful physical baseline when the visual claim is absolute
  magnitude or gap size.
- For convergence, cost, and performance comparisons, provide a full-range view
  when a narrow range would exaggerate separation.
- If a truncated axis is necessary to reveal structure, label it clearly and add
  a full-range panel, inset, or supplementary view when practical.
- Use log scales only for a scientifically justified multiplicative range and
  label them explicitly.
- Do not hide unfavorable regions through limits, selective panels, omitted
  runs, or legend placement.
- Keep comparable panels on consistent scales unless a visible annotation states
  otherwise.
- Do not manually smooth, enforce monotonicity, or redraw sampled points.

Color is supplementary encoding. Use line style, marker, shape, texture, or
direct labels as a second channel. Check grayscale and common color-vision
deficiencies. Keep the legend away from data and use the same method styling
across the paper.

## Size text, lines, and panels at final scale

Check all of the following after placement:

- axis labels, ticks, legends, annotations, and in-figure formulas are readable;
- line styles remain distinct and thin lines do not disappear;
- markers do not merge or conceal uncertainty intervals;
- panel tags follow one convention and do not collide with data;
- multi-panel spacing is compact but not crowded;
- identical quantities use identical units and notation;
- titles are omitted when the caption already identifies the panel;
- white space is intentional rather than an artifact of a bad crop box.

If a legend requires text smaller than the safe final-size target, reduce the
number of series, use direct labels, split the question, or move secondary curves
to supplementary material. Shrinking is not a substitute for information design.

## Write concise, useful captions

A caption should identify:

- what is shown;
- the key conditions or dataset split;
- the metric and unit when not obvious;
- uncertainty or aggregation when necessary;
- panel mappings.

Move implementation detail, long derivations, and repeated conclusions into the
main text. Keep captions self-contained enough to interpret the figure, but do
not turn them into a second results section.

Every figure must be cited before or near its placement, and the prose should say
what decision the reader can draw rather than merely “Fig. X shows the results.”

## Audit tables, equations, and prose layout

For tables:

- state metric direction, unit, split, denominator, and aggregation;
- align decimal precision with measurement uncertainty;
- use consistent missing-value meanings;
- avoid scaling the font below the venue's readable minimum;
- do not bold a winner that fails a fairness or validity gate.

For equations and algorithms:

- introduce each display with a complete sentence;
- number distinct referenced quantities separately;
- preserve label and cross-reference logic rather than typing numbers manually;
- check long expressions for column overflow;
- retain the algorithm or complexity detail needed to reproduce the method;
- do not remove necessary content solely to create empty page space.

For manuscript pages:

- obey the required paper size, margins, page count, and body/reference split;
- scan logs for errors, unresolved references, rerun notices, overfull and
  underfull boxes, duplicate labels, and missing glyphs;
- check consistent paragraph indentation, headings, abbreviations, units, and
  journal reference styling;
- look for sentence fragments, orphaned words, awkward column breaks, detached
  captions, float collisions, and large accidental whitespace;
- verify anonymous and identified variants are never mixed.

## Lay out response and cover letters

Use a readable single-column page, conventional margins, page numbers for a
multi-page response, and a stable hierarchy:

`Reviewer heading → Comment → Response → Changes in the manuscript`

Visually distinguish quoted comments from responses without making either tiny.
Keep tables within margins, repeat table headers when necessary, and place a
supporting figure close to the response that interprets it. A cover letter should
normally fit on one uncluttered page; if it does not, shorten the summary rather
than reducing readability.

## Record and verify each figure

Create one `07_FIGURE_AUDIT.csv` row per submitted figure. Record final asset and
render paths, format, physical width, effective DPI or vector status, font and
crop checks, axis decision, caption check, uncertainty treatment, and final-size
inspection.

Run the package audit in strict mode for a formal revision:

```powershell
python "<SKILL_DIR>/scripts/audit_revision_package.py" <project-directory> --strict
```

When Poppler-compatible tools are available, useful read-only checks include:

```powershell
pdfinfo manuscript.pdf
pdffonts manuscript.pdf
pdftoppm -png -r 180 manuscript.pdf rendered/page
```

Inspect the font table for embedded fonts and Type 3 entries. Treat 180 dpi page
renders as convenient visual-review copies, not as replacement figure assets or
proof that the original images meet their required effective DPI.

Finally render every manuscript, response-letter, and cover-letter page to an
image at a useful inspection resolution. Inspect the pages in order and also
zoom each figure at its actual placed size. Text extraction, build success, and
font reports do not replace visual inspection.
