# G3 HISTORY — public content census acquisition status, 2026-09-08

**Status:** ACTIVE / QUANTITATIVE_LANGUAGE_HOLD / PUBLICATION_HOLD  
**Purpose:** preserve the result of the first reproducible live-metadata census attempt without converting access failure into a false zero-content denominator.

## Exact acquisition

Workflow: `G3 public content inventory acquisition`  
Run: `34254408853`  
Research head: `1d5b9ee018deb0dbda8424fbfb873a64f99cc810`  
Artifact: `g3-content-inventory-1d5b9ee018deb0dbda8424fbfb873a64f99cc810`  
Artifact SHA-256: `9e476dcb497229f005c72e6ad6f9a313a96e41b70788b82182e8935b98ee1e37`

The acquisition tool was metadata-only. It requested no article bodies and stored only URL/date/title/author metadata when available.

## Result

The run completed successfully as an acquisition diagnostic, but the live G3 surfaces did **not** expose a usable denominator:

- `https://g3min.org/wp-sitemap.xml` → HTTP 503;
- `https://g3min.org/sitemap_index.xml` → HTTP 503;
- `https://g3min.org/sitemap.xml` → redirected/finalized to the WordPress sitemap surface and returned HTTP 503;
- WordPress REST post metadata endpoint → HTTP 403.

Therefore the emitted counts

- `sitemap_unique_urls = 0`;
- `child_sitemaps_seen = 0`;
- `wp_post_rows = 0`

mean **PUBLIC_METADATA_ACCESS_HOLD**, not “G3 had zero articles/posts.”

## Evidentiary consequence

The qualitative ideological reconstruction may continue to use individually verified primary/archived objects, but no percentage, rate, trend line, or denominator-based statement about G3 content composition may be published from this run.

Explicitly blocked:

> `0 WP rows` = `0 G3 posts`.

> Search results = corpus census.

> A live-site 503/403 can be used as evidence that a historical content category was absent.

## Next acquisition route

Do not repeat the same live WordPress/sitemap request unless the access state materially changes.

The next denominator lane should be archive-first and metadata-only:

1. segmented Wayback CDX URL inventory by year;
2. HTML-document filtering and asset exclusion;
3. normalized canonical URL deduplication;
4. date/capture provenance for every retained URL;
5. separate denominators for articles, conference sessions, podcasts/media, and products;
6. only after denominator closure, apply `IDEOLOGY_CONTENT_CODING_PROTOCOL.md`.

The existing coding rule remains authoritative:

**search results != corpus census.**
