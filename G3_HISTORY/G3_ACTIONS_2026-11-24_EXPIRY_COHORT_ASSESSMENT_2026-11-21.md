# G3 Actions 2026-11-24 expiry cohort — bounded assessment

**Status:** `METADATA_INVENTORIED / NO_SCOPE_EXPANSION / NOT_PRESERVED_BY_8_OF_8_RECEIPT`
**Observed at (UTC):** `2026-11-21T10:44:53Z`
**Authority:** `data/artifact-custody-policy-v2.json` · `DURABLE_CUSTODY_POLICY.md`

## Scope and method

This is a **read-only metadata assessment**, not a transfer plan or a custody receipt. It queried the GitHub Actions artifacts endpoint `GET /repos/FedorMilovanov/Research/actions/artifacts?per_page=100&page=1..6` and selected returned artifacts whose API `expires_at` begins `2026-11-24` and whose name begins `g3-`.

Pages 1–6 were selected because they cover the recent creation-time interval around the seven-day 17 Nov. Actions cohort. This bounded scan does **not** establish that no older, differently retained artifact elsewhere in the 2,207-object API inventory also expires on that date. It also does not inspect artifact content, download ZIP bytes, calculate a local hash, perform a ZIP test, write a Drive object, or make a rights/publication judgment.

## Result

- `48` returned artifacts in the bounded pages had `expires_at` on 2026-11-24; `38` were named `g3-*`; `10` were outside the G3 name scope.
- The authorized private-custody receipt covers exactly `8` of those `38` G3 artifacts: IDs `14304199942, 14304253824, 14304413494, 14304577164, 14304975723, 14305021388, 14305050966, 14305250133`.
- The remaining `30` listed below were still `expired=false` in their GitHub API metadata at observation. They are **not** covered by `G3_ACTIONS_PRESERVATION_CUSTODY_RECEIPT_2026-11-21.json` and are not thereby preserved.
- No additional ZIP was downloaded, copied, uploaded, shared, unpacked, repacked, deleted, or otherwise altered in this assessment.

## Separate disposition by category

| Category | Count | Bounded assessment / required next gate |
|---|---:|---|
| IRS raw-acquisition output | 8 | The durable register already records bounded raw IRS object receipts for the filing family; that does **not** preserve these exact ephemeral Actions ZIPs. Any archive preservation of these ZIPs requires a separate authorized scope/receipt. |
| Wayback board output | 4 | Existing durable receipt(s) for specifically named snapshots do **not** prove preservation of these exact workflow ZIPs. Preserve only with a new object-specific authorization. |
| Buck supporting-media output | 4 | Media/rightsholder and item-level evidence controls remain operative. No transport step implies permission to preserve/publish additional media workflow outputs. |
| Buck individual-media output | 14 | The `0/17 ITEM_VERIFIED` and rights/publication firewalls remain. Do not bulk-transfer based on expiry alone. |

## Unpreserved G3 entries in the bounded cohort

`GitHub API SHA-256 digest` is provider metadata only. It is recorded to identify a potential later authorized source object; it is not a local source-byte hash or a Drive readback.

| Category | Artifact ID | Artifact name | Bytes | Workflow run | Expires UTC | Provider SHA-256 digest | API expired at observation |
|---|---:|---|---:|---:|---|---|---|
| Buck individual-media output | `14304194657` | `g3-buck-media-item-12-2ebf700f4cebc18e0cf571f42591c042790a6efb` | 13,027 | `44029722918` | `2026-11-24T06:18:42Z` | `sha256:382375c3b5736ede631e1b144f238e30f4189f09a11ba50d68f397603c24fbc7` | `False` |
| Buck individual-media output | `14304569662` | `g3-buck-media-item-11-eb6f0f19b40f8a4bfe6eb54d2d2c253fdfdb3711` | 13,340 | `44029724045` | `2026-11-24T06:33:43Z` | `sha256:38db275dd731122931df4d02b3846aa68d20a2a1a90fa35d0149a037d5113c30` | `False` |
| Buck individual-media output | `14305028783` | `g3-buck-media-item-13-eb6f0f19b40f8a4bfe6eb54d2d2c253fdfdb3711` | 7,986 | `44029724045` | `2026-11-24T06:32:48Z` | `sha256:f9ee66ad1fa034699e4727db7e8e465f48b95f6f7b534024ed5314bd6a5fd3f3` | `False` |
| Buck individual-media output | `14305055930` | `g3-buck-media-item-13-2ebf700f4cebc18e0cf571f42591c042790a6efb` | 8,009 | `44029722918` | `2026-11-24T06:19:17Z` | `sha256:10d8c7a54ea0583bbefbb5cdcdba6cd896f31023c1c484da770a95a22706f517` | `False` |
| Buck individual-media output | `14305197011` | `g3-buck-media-item-15-2ebf700f4cebc18e0cf571f42591c042790a6efb` | 26,337 | `44029722918` | `2026-11-24T06:25:54Z` | `sha256:f67b187b924a5ba08d57e2e6b6d41e507aadbba1243832facca2e0952c56ee29` | `False` |
| Buck individual-media output | `14305436142` | `g3-buck-media-item-14-2ebf700f4cebc18e0cf571f42591c042790a6efb` | 16,287 | `44029722918` | `2026-11-24T06:24:49Z` | `sha256:725bd1a0e799972d67cd3282f1fac44b469be8cfaa78a932e05d2232a56160e9` | `False` |
| Buck individual-media output | `14305587000` | `g3-buck-media-item-16-eb6f0f19b40f8a4bfe6eb54d2d2c253fdfdb3711` | 33,604 | `44029724045` | `2026-11-24T06:30:26Z` | `sha256:87b7b5802053f8dce1cb298b8d4dec3a3a97b9b7af0c77290bb01bfc60b1a394` | `False` |
| Buck individual-media output | `14305653553` | `g3-buck-media-item-14-eb6f0f19b40f8a4bfe6eb54d2d2c253fdfdb3711` | 16,258 | `44029724045` | `2026-11-24T06:39:54Z` | `sha256:98a9a6aba800acdfc44d8a5dbc673608498c45c4b9944b97122eb72a80715244` | `False` |
| Buck individual-media output | `14305847291` | `g3-buck-media-item-12-eb6f0f19b40f8a4bfe6eb54d2d2c253fdfdb3711` | 13,057 | `44029724045` | `2026-11-24T06:37:36Z` | `sha256:c1460984f42dc8c681b917d9a393762215ab13eb04085613b27f8dd3d0b3e51c` | `False` |
| Buck individual-media output | `14305873841` | `g3-buck-media-item-15-eb6f0f19b40f8a4bfe6eb54d2d2c253fdfdb3711` | 26,318 | `44029724045` | `2026-11-24T06:43:54Z` | `sha256:68c11e8b614880705adf82e423bb261e6b4a323ed86ff4f520b15526786f9cab` | `False` |
| Buck individual-media output | `14306025656` | `g3-buck-media-item-11-2ebf700f4cebc18e0cf571f42591c042790a6efb` | 13,317 | `44029722918` | `2026-11-24T06:37:26Z` | `sha256:e69bb25adb818c7130ddd1485c1cbe22d6952893215a15afcaf09fddfb85641b` | `False` |
| Buck individual-media output | `14306096389` | `g3-buck-media-item-16-2ebf700f4cebc18e0cf571f42591c042790a6efb` | 33,595 | `44029722918` | `2026-11-24T06:44:06Z` | `sha256:6c47666308be96d56ed164d091eac35a3aa81c081ee9c00cbc593454c365f1ae` | `False` |
| Buck individual-media output | `14306366064` | `g3-buck-media-item-17-eb6f0f19b40f8a4bfe6eb54d2d2c253fdfdb3711` | 28,053 | `44029724045` | `2026-11-24T06:45:46Z` | `sha256:aa0337a74b2130021bb7683ffdf7ad91f72ebd9df9be00bc161f196e6b1bc389` | `False` |
| Buck individual-media output | `14306610165` | `g3-buck-media-item-17-2ebf700f4cebc18e0cf571f42591c042790a6efb` | 28,041 | `44029722918` | `2026-11-24T06:43:09Z` | `sha256:31974b18e6bb553eff1ff7c59c6756292365c181146547d514882c4fbbc79ded` | `False` |
| Buck supporting-media output | `14304184814` | `g3-buck-titus-media-evidence-eb6f0f19b40f8a4bfe6eb54d2d2c253fdfdb3711` | 19,325 | `44029724087` | `2026-11-24T06:18:25Z` | `sha256:e8fbc1d9da168ef8aa7d0a29f3ccbd47f8078ea9fccbff65abac6b6d95dbd070` | `False` |
| Buck supporting-media output | `14304577624` | `g3-buck-rss-media-inventory-eb6f0f19b40f8a4bfe6eb54d2d2c253fdfdb3711` | 6,543 | `44029724046` | `2026-11-24T06:20:30Z` | `sha256:6730e0ef3f7d62b3a0ad05e88315d635fef7c9eb7932ea93ee0ee91a03fbcf10` | `False` |
| Buck supporting-media output | `14304877099` | `g3-buck-titus-media-evidence-2ebf700f4cebc18e0cf571f42591c042790a6efb` | 19,321 | `44029723124` | `2026-11-24T06:21:47Z` | `sha256:aa90d0d9843eb7c92111adc8ec61c1f079133638a105c19e1d64b4f4cfab25c3` | `False` |
| Buck supporting-media output | `14305095550` | `g3-buck-rss-media-inventory-2ebf700f4cebc18e0cf571f42591c042790a6efb` | 6,544 | `44029723036` | `2026-11-24T06:17:17Z` | `sha256:dc47f2e89229b531cdb598f0c374a4cd0fd15225661dd16f80e611fabb7cd650` | `False` |
| IRS raw-acquisition output | `14304399916` | `g3-irs-FY2025-44029723055-1` | 156,658 | `44029723055` | `2026-11-24T06:22:25Z` | `sha256:a3e47982279cebf69c3325e1f7e98976df5f3d80065972c5153cd6efb840769b` | `False` |
| IRS raw-acquisition output | `14304634317` | `g3-irs-FY2025-44029724281-1` | 156,655 | `44029724281` | `2026-11-24T06:33:49Z` | `sha256:c6c23454097b6483f72729816f064090c3276154c4c56531c443b7252136346d` | `False` |
| IRS raw-acquisition output | `14304634340` | `g3-irs-FY2022_LATER-44029723055-1` | 105,336 | `44029723055` | `2026-11-24T06:33:59Z` | `sha256:253d7c59c5a1dc912ee7820ba558802e9c3e9ade639255d16c299ce918019c73` | `False` |
| IRS raw-acquisition output | `14305107904` | `g3-irs-FY2024-44029723055-1` | 154,866 | `44029723055` | `2026-11-24T06:29:48Z` | `sha256:70ec92bb891ef295f5cf27a255b58b75b72f146db4c83e114c86ded111eb0a27` | `False` |
| IRS raw-acquisition output | `14305593507` | `g3-irs-FY2023-44029724281-1` | 120,540 | `44029724281` | `2026-11-24T06:39:08Z` | `sha256:16513f6e13362d09cdc2da112e5d30ccd3d698d21241c76ad7a4ed3fbe4a870f` | `False` |
| IRS raw-acquisition output | `14305682843` | `g3-irs-FY2022_LATER-44029724281-1` | 105,342 | `44029724281` | `2026-11-24T06:36:22Z` | `sha256:33b8b26a3b97504089215852509ed3bdeea4813087e027f8bb58ddb19d7ef679` | `False` |
| IRS raw-acquisition output | `14305975444` | `g3-irs-FY2023-44029723055-1` | 120,543 | `44029723055` | `2026-11-24T06:26:20Z` | `sha256:c93798bdc6512d779aa8f3822fa266d6526fbebc8de6d54c444be2027e35b218` | `False` |
| IRS raw-acquisition output | `14306300352` | `g3-irs-FY2024-44029724281-1` | 154,866 | `44029724281` | `2026-11-24T06:38:42Z` | `sha256:e5d3d12bbcaa2345db8671b7dce7715c35f585b67cda07466747a3236bb66451` | `False` |
| Wayback board output | `14303579786` | `g3-wayback-late-board-44029724172-1` | 109,866 | `44029724172` | `2026-11-24T06:15:49Z` | `sha256:d0e7ed3d0cab12364d8dfbbc8ea3166994dee0bd6f485ac57ba53905af07ca7b` | `False` |
| Wayback board output | `14304114428` | `g3-wayback-2025-board-44029724090-1` | 9,095 | `44029724090` | `2026-11-24T06:15:29Z` | `sha256:295ce829d0de40c69dbd9f4986d3daef1c1c257b743e8510a52a64892d391d29` | `False` |
| Wayback board output | `14304373650` | `g3-wayback-late-board-44029722812-1` | 109,866 | `44029722812` | `2026-11-24T06:14:38Z` | `sha256:17aee0a5d1c83dd14a4bf621ecb58563a033a97de4c8cea7c321c29a065eb8c0` | `False` |
| Wayback board output | `14305418221` | `g3-wayback-2025-board-44029723046-1` | 9,095 | `44029723046` | `2026-11-24T06:34:17Z` | `sha256:9ae9ba3c98b4b451d132da818af626dfedc6f6c46d59bb5034a2efbabbb3f432` | `False` |

## Boundary retained

`PUBLICATION_HOLD`, `RIGHTS_HOLD`, `EVIDENCE_HOLD`, and media `CATALOG_ONLY` remain unchanged. This assessment neither establishes an official Georgia filing/detail/body, nor a primary transition/assignment/purchase/donation/closing record, nor legal title, asset scope, or publication authorization. The eight-object custody receipt remains bounded exactly as written.
