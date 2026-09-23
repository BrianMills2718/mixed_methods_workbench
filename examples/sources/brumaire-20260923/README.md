# Brumaire public-source trial, frozen 2026-09-23

These four UTF-8 files are the exact document inputs used for the fresh
Qualitative Coding trial on 2026-09-23. They are retained so the trial can be
replayed even if the public pages change. The associated QC synthesis was **not
accepted**: two findings cited passages that did not support their claims.
Do not pass that trial's synthesis handoff to Process Tracing as validated
evidence. This packet freezes inputs, not conclusions.

| File | Source | Input SHA-256 |
| --- | --- | --- |
| `decree.txt` | [Decree of the Council of Five Hundred](https://www.napoleon-series.org/research/government/legislation/c_brumaire.html), in Frank Maloy Anderson, *The Constitutions and Other Select Documents Illustrative of the History of France, 1789–1901* (1904) | `b6e0bc966a4fbffc3eee9649b4107a9be129c95c6a166102354d5baac59aa1e2` |
| `proclamation.txt` | [Proclamation of the Consuls, 21 Brumaire](https://www.napoleon-series.org/research/government/legislation/c_brumaire.html), attributed there to *The Annual Register* for 1799 | `20fc8c306ccf149f2fc1c0d07212143fd0ebb9895d0a5ee188f2785299fe8a5e` |
| `constitution.txt` | [Constitution of Year VIII](https://www.napoleon-series.org/research/government/legislation/c_constitution8.html), Anderson (1904) | `0add2309f80e40955ffc02c43346a4ffa4b38990cefeb42b13c36b4f1c5758c7` |
| `memoir_chapter_xxiv.txt` | Bourrienne, *Memoirs of Napoleon Bonaparte*, [Project Gutenberg volume III](https://www.gutenberg.org/ebooks/3553), chapter XXIV | `7cc1e4659fb45c1b97e53ba40a58474e3c5132fb7dabe1dadd8d96b4d9949645` |

The decree and Constitution are period documents available through a 1904
English-language collection; the site's separate bibliography attributes the
proclamation to *The Annual Register* for 1799. Bourrienne's memoir is a later,
interested account;
it is evidence of what he wrote, not independent confirmation that every event
occurred as he described. None of these texts alone establishes hidden motives,
public demand, or a sufficient causal explanation for the coup.
Project Gutenberg labels its volume public domain in the United States; the
other extracts reproduce the historical text attributed to 1799/1904 sources,
not the host site's editorial introductions or navigation.

## Custody and extraction

The source pages were downloaded on 2026-09-23. The raw HTML downloads are not
redistributed here. The Brumaire decree/proclamation page was 15,730 bytes with
SHA-256 `56faa892c1eb0b903978b17d95845591b898c0314877235e8b18012bb9e4fc05`;
the Constitution page was 35,445 bytes with SHA-256
`9f8d90f1962edbdba02a5d48a58e20facbcbe2a43b62de2074d7e051fcd2b194`.
Visible document text was extracted from the relevant page sections, excluding
site navigation and editorial framing. The decree and proclamation are separate
files because they are different documents on one page.

The [Gutenberg plain-text download](https://www.gutenberg.org/cache/epub/3553/pg3553.txt)
was 298,313 bytes with SHA-256
`d267f1940c9c10ec78b3a2f87b91077db519bc214646221180fdb9893e6cd1bb`.
The retained memoir file is the span from `CHAPTER XXIV.` up to, but excluding,
`CHAPTER XXV.`. Line endings were normalized to LF. Its exact bytes, like the
three official-text extracts, are authoritative for replay.

Verify the frozen inputs from this directory with `sha256sum -c SHA256SUMS`.
A fresh download with a different raw digest is a new
source observation; it does not silently replace this packet.

## Intended analysis boundary

The trial's frozen QC question was: *What do the contemporary decree, consular
proclamation, and constitution say about the change of authority, and how does
Bourrienne later describe its execution?* Its declared use was descriptive
mapping with separate source attribution. A PT rival test still requires a
valid QC handoff and an explicit case-specific rival design. Structural anchor
validation alone is not a semantic-support check.
