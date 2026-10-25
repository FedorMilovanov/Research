# Review log — SUNO_HYMNS project bootstrap

Date: 2026-10-25  
Branch: arena/dutch-hymns-suno-research-20261025  
Base snapshot originally inspected: f38b194a99fdc6cc66b86fcc4c1b217da7e945a0

## Changes identified by the second audit

1. **Two poems called Hert-sterckte in Jehova.** The critical edition distinguishes item 34 (I, dated 28 December 1673 with its own melody directions) and item 35 (II). The current Russian track follows the later Rutgers hymnbook chain for II; I has been added as a separate candidate.
2. **Date emendation for II.** The digital material reads 4 January 1674, but records that the original print erroneously says 1664 and the online colophon records a 1664→1674 correction. The specific date claim now carries EVIDENCE_HOLD until the original page image is checked.
3. **First edition versus critical edition.** The 1676 book is a primary historical witness and DBNL marks the underlying work Auteursrechtvrij; the digital rendering is diplomatic, with omissions and explicit editorial corrections. The 2005 critical edition by Ros and Strengholt is explicitly copyright-protected. The source registry now separates historical evidence class, access state and reproduction rights.
4. **Utrecht Hymni 1615 access layer.** The accessible DBNL item is the 1967 facsimile edited by Jan van Biezen and Marie Veldhuyzen, not an independent direct scan of the 1615 original. The facsimile is copyright-protected.
5. **Revius distinction.** The 1630 first-edition object has not been independently acquired; the exact sonnet page currently used comes from W.A.P. Smit's 1930–1935 scholarly edition. Composition date and original melody remain unverified.
6. **Status hygiene.** Production asset preparation, exact prompt capture, actual metadata readback, rights and public publication are recorded separately.
7. **Broader backlog.** Added directly locatable first-edition candidates with tune directions and a separate discovery queue for the broader Uyt-spanningen contents. Discovery items remain candidates; not all are necessarily hymns or appropriate for a full-length SUNO adaptation.
8. **Machine checks.** Added author, claim and songbook registries plus a read-only cross-reference/state validator. These are project-local tooling; they do not alter root authority or global evidence policy.

## Still open after this commit

- Inspect the actual 1676 page image for the 1664 misprint and resolve the date HOLD only with recorded visual evidence.
- Acquire / inspect the 1630 Revius leaf if a claim requires original punctuation, physical layout or edition variants.
- Recover exact lyric versions and verbatim SUNO prompts from an authoritative record.
- Read actual media metadata and identify the final Revius cover.
- Verify YouTube/Telegram publication URLs before any publication-status change.
- Continue rights review before redistributing a modern critical edition, facsimile, translation or recording.


The follow-up state pass removed source- and book-level EVIDENCE_HOLD where the uncertainty was narrower than the whole object. The 1664→1674 dispute remains on the specific claim CLM-HERT-II-DATE-1674. The DUTCH-001 tune/date and Revius 1630 first-edition claims are marked as needing primary-witness collation where the exact accessed text is a later scholarly edition.
