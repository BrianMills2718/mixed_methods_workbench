# Brumaire independently acquired source packet

These four UTF-8 files are the inputs for the next **new** Brumaire QC project.
They replace the earlier site-extracted trial packet for any connected QC → PT
proof. Verify their exact bytes with `sha256sum -c SHA256SUMS`.

| File | Independent source and extraction | Input SHA-256 |
| --- | --- | --- |
| `decree.txt` | Frank Maloy Anderson, *The Constitutions and Other Select Documents Illustrative of the History of France, 1789–1901* (1904), [digitized scan](https://upload.wikimedia.org/wikipedia/commons/a/aa/The_Constitutions_and_other_select_documents_illustrative_of_the_history_of_France%2C_1789-1907_-_%28IA_constitutionsoth01ande_0%29.pdf), scan pages 301–302. Text extracted from that scan and checked against the rendered pages; Anderson's editorial introduction was excluded. | `562fbc29d2e8944bf071ba263ffdc3b19ea561452e4f5bb04e3c0303d8058bb4` |
| `proclamation.txt` | *The Annual Register* for 1799, volume 41, [Internet Archive scan](https://archive.org/details/s25id13211630), scan page 584 / printed page 254. Transcribed from the page image; adjacent state papers were excluded. | `c8eca7523b4303b05169c918a23ed0e130a6568f449d75228779a14049785590` |
| `constitution.txt` | Anderson, second edition (1908), [Wikisource document 58](https://en.wikisource.org/wiki/Constitution_of_the_Year_VIII), transcribed from scan pages 300–311. The exact rendered article text was extracted from the page; all 95 numbered articles are present. Anderson's editorial introduction was excluded. | `f9b4b6da73a353ce07ab32cef88df40b4cf25b9c350722773996de14f35f7670` |
| `memoir_chapter_xxiv.txt` | Bourrienne, *Memoirs of Napoleon Bonaparte*, [Project Gutenberg volume III](https://www.gutenberg.org/ebooks/3553), chapter XXIV. A fresh download reproduced the earlier chapter hash exactly. | `7cc1e4659fb45c1b97e53ba40a58474e3c5132fb7dabe1dadd8d96b4d9949645` |

## Custody and rights boundary

The Anderson scan SHA-256 is
`f6004cc141e707d8c1edc6cde50a65efafa82b9ecc5e3e4457cce5bc22485317`.
The [Library of Congress record](https://www.loc.gov/item/04025396/) identifies
the 1904 edition and states that books in its digitized collection are public
domain and free to reuse. The scanned *Annual Register* PDF SHA-256 is
`749497504ddc2e3d553d8892e7651a31df2130d7eaa15d345ffe3d1323125bee`;
its Internet Archive OCR SHA-256 is
`9eccaf9f09ace6d5297a9c2d6836fb75a4324be9bcdf9fe88002a41578fc760c`.
The Wikisource rendered Constitution HTML SHA-256 was
`bca9f259059c9ec0a5c3ef5320369a0328250ce9464792bd83b181381d07baaf`
at extraction. Attribution for its transcription: [Wikisource contributors to
document 58](https://en.wikisource.org/w/index.php?title=The_Constitutions_and_Other_Select_Documents_Illustrative_of_the_History_of_France,_1789%E2%80%931907/58&action=history);
reuse of contributor text follows [Wikisource's CC BY-SA terms](https://en.wikisource.org/wiki/Wikisource:Copyright_policy).
The Gutenberg plain-text download
SHA-256 was
`d267f1940c9c10ec78b3a2f87b91077db519bc214646221180fdb9893e6cd1bb`.

The old packet was extracted from pages on the Napoleon Series. Its
[copyright notice](https://www.napoleon-series.org/about/copyright/) restricts
redistribution of its articles, so the old packet is retained solely as a
historical run input and is **not** the source basis for a review candidate.
These independent scans remove that site's rendering from the new acquisition
chain. The Anderson and Gutenberg rights statements establish U.S. reuse; this
packet does not claim a worldwide license for every English translation or
authorize public deployment of a review page.

## Analytical boundary

The question remains: what do the contemporary decree, proclamation, and
constitution say about changing authority, and how does Bourrienne later
describe the execution? The memoir is later interested testimony. These four
texts do not establish hidden motives, public demand, or causal sufficiency.
The new input hashes differ from the rejected project, so its saved coding and
synthesis context must not be resumed or relabeled as this corpus. A new native
QC project, supported handoff, and native PT test are required.
