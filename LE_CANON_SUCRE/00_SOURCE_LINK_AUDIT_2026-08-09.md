# LE CANON SUCRÉ — source-link & ledger-integrity audit

**Audit date:** 2026-08-09  \
**Scope:** all `LE_CANON_SUCRE/*.md` (governing files + 15 dossiers) and the claim-to-citation ledger.  \
**Validator:** `scripts/validate_le_canon_sucre_source_audit.py` (read-only; does not modify the working tree).  \
**Method:** offline static audit. **Reachability was NOT verified** — the sandbox has no network egress, so this pass confirms structure, integrity and locator precision only. A later online pass must confirm liveness and tighten `accessState` where a URL now returns 404/410.

## Result summary

| Check | Result |
|---|---|
| Ledger source rows parsed (both table layouts) | **99** |
| Hard structural errors | **0** |
| Shared multi-object-page URLs (warnings) | **5** |
| Low-precision portal / route leads (warnings) | **5** |
| Corpus link occurrences swept | **335** |
| Unique hosts | **84** |
| Malformed URLs | **0** |

## What passed

- Every `LCS-*` sourceId is unique; every row carries a parseable `https?` URL with a host.
- Every `evidenceClass` is in the allowed set `{A1,A2,A3,B1,C,D}`.
- `accessState` / `locatorState` / `rightsState` / `publicationState` are present on every main-table row (upgrade-table rows omit `publicationState`, which is expected).
- Every claim decision's `main support` references a sourceId that exists in the ledger; claim-decision IDs (`LCS-C0xx`) are correctly excluded from the source check.
- No malformed URLs anywhere in the corpus.

## Shared multi-object-page URLs (legitimate, not defects)

A single institutional / stamp / interview page legitimately documents several pastries. The ledger represents each pastry's use as a distinct sourceId sharing one URL. These are flagged so a shared URL is never silently mistaken for an edition split — no such split was found.

| sourceIds | shared URL | why shared |
|---|---|---|
| `LCS-PB05`, `LCS-OP06` | `https://www.laposte.fr/.../carnet-de-12-timbres-patisseries-francaises...` | one La Poste pastry-stamp sheet covers both Paris-Brest and Opéra |
| `LCS-BA06`, `LCS-RG01` | `https://elib.spbstu.ru/dl/2/ed-3262_0000697628bx.pdf/en/info` | one SPbPU Bailleux 1860 object record exposes both Baba/Savarin and Religieuse TOC entries |
| `LCS-IS03`, `LCS-2F02` | `https://gourmet.galerieslafayette.com/.../pierre-herme-et-pierre-sang...` | one Hermé interview covers both Ispahan and 2000 Feuilles |
| `LCS-IS04`, `LCS-2F01` | `https://www.pierreherme.com/fr/art-de-la-patisserie` | one Maison page covers multiple signatures |
| `LCS-EA02`, `LCS-EA03` | `https://wordhistories.net/2025/03/25/eclair-cake/` | one article supplies both the Bailleux 1856 and the *Vanity Fair* 1861 éclair locators |

## Low-precision portal / route leads (allowed as locators, not quote-safe pages)

These are correctly used as acquisition/route leads; they are not precise page locators and must not be promoted to quote-safe content.

- `https://www.inpi.fr/ressources/propriete-intellectuelle/rechercher-une-marque-base-marques` — INPI mark-search portal (route to the exact canelé / Tropézienne / Kouign-Amann register objects)
- `https://www.inpi.fr/ressources/propriete-intellectuelle/acces-aux-api-et-ftp` — INPI API/FTP info
- `https://data.inpi.fr/content/editorial/lien-serveur-ftp-PI` — INPI FTP link
- `https://gallica.bnf.fr/accueil/fr/html/aide-a-la-recherche` — Gallica help (tooling reference)
- `https://www.patisseriefrancaise.fr/website/page/actualites_regionale?__ws=...` — dynamic regional page (secondary)

## Follow-up (online pass, when egress is available)

1. Run `scripts/validate_le_canon_sucre_source_audit.py` plus a live HTTP reachability pass over the 99 ledger URLs and the 335 corpus link occurrences.
2. For any URL returning 4xx/5xx, record the dead link in the relevant dossier and, where the source is load-bearing, supply a replacement primary/authorized object or move the row to `HOLD`.
3. Confirm the 5 low-precision portal leads still resolve and keep them as route leads only.

Per `AGENT_RULES.md`, URL reachability and bibliographic presence do not by themselves remove a HOLD; this audit records structure and precision, and the online pass is the only step that may tighten an `accessState`.
