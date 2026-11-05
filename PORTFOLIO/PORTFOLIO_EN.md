# Portfolio (EN) — working draft

> CI census updated: 221,596 GitHub Actions runs currently available via the API for ten repositories in 2026 through 2026-11-03 21:05:16 UTC. Other portfolio metrics retain their 2026-11-01 snapshot. Previously deleted runs are not recoverable. See CI_RUNS_2026-11-03.csv and tools/measure_ci_runs.py.

> For an international audience: website, PDF, LinkedIn "About", or a cold outreach one-pager.
> All figures verified on 1 November 2026 and reproducible from `VERIFICATION_LOG.md`. Deliberately explicit about AI use, third-party open source, and what is *not* mine.

---

## 1. Header

**Fedor Milovanov**
Product engineer, technical editor, AI-assisted production lead and visual-direction reviewer

St Petersburg, Russia (remote, UTC+3) · [gospod-bog.ru](https://gospod-bog.ru) · [thelegendarypoet.ru](https://thelegendarypoet.ru) · [milovicake.ru](https://milovicake.ru) · [YouTube @TheLegendaryPoet](https://www.youtube.com/@TheLegendaryPoet) · [GitHub](https://github.com/FedorMilovanov) · [email]

**One line.** I build products and media with AI agents, set functional and visual direction, define contracts, verify the results, and take responsibility for release.

**Headline options**
- I build systems you can trust an AI agent to work in: contracts, gates, evidence, rollback.
- Five live products, a media line (music, clips, visuals) and 241 CI workflow files in the dated snapshot — one person plus agents.
- From research corpus to music video: product, content, engineering and media in one pair of hands.

---

## 2. Summary

For ten years my work was text and meaning: editing, research, teaching. Since early 2026 I do the same thing with a team of AI agents — I design the architecture, write machine-checkable contracts, brief the agents, accept the work against evidence, and ship it.

Ten months of that produced five live products on my own domains, two internal platforms (a media pipeline and a multi-channel publisher), and a documented media workflow: a Russian poetry YouTube channel with songs built in Suno from my lyrics and prompts, AI-generated visuals and clips, and Telegram publishing. Audience and video-count snapshots are deliberately omitted without a reproducible current check.

Code and part of the media are AI-generated under my direction. Requirements, architecture, editorial decisions, acceptance, publication and accountability are mine. The verification layer is the interesting part — and so is the honest boundary: the speech engine on my site is someone else's open-source project, not mine.

---

## 3. Numbers

**Products and engineering**

| | |
|---|---|
| 5 products live in production | 4 own domains |
| 766,175 lines of application code under management (512,322 in six product repos; 824,453 including research validators) | 241 CI workflow files · 221,596 runs |
| 1,390 test and QA files | 20,990 commits in ten months |
| Public editorial prose (exact word count unverified) | 2,076 research documents (Nov 1, 2026 snapshot) |

**Media**

| | |
|---|---|
| Music: poem → song → clip, with a repeatable protocol | Visual canon and storyboard per song |
| Publishing with exact object identity across platforms | Counters (subscribers, views) are not claimed: not verifiable from outside |

**How to read this honestly.** "766k lines" is volume taken to production and kept alive, not hand-typed text. The difference is contracts and acceptance. And the voice on my site is an open-source engine — my part is the browser integration and the Russian stress layer.

---

## 4. Selected work

### 4.1 Theological research library — [gospod-bog.ru](https://gospod-bog.ru)

A public library built on years of exegetical research: 111 pages, 57 article routes, twelve series, ten interactive biblical atlases, genealogy, glossary, Pagefind search, an offline reader, and speech synthesis in the browser.

**The engineering story.** Three truths never conflated: source, build, production. Route ownership comes from machine registries; `document-authority.json` decides which document may override anything at all; a live `release.json` pins the commit SHA and CI verifies that SHAs quoted in documentation match real bytes.

**The honest boundary.** Alpha Cephei's Vosk TTS **source code** is Apache-2.0; the Russian 0.9 voice-model **weights** are third-party assets whose modified redistribution rights have not yet been independently cleared (`MODEL_RIGHTS_HOLD`). Neither code nor voice was trained or authored by me. Mine: the browser integration (on-demand ONNX model, IndexedDB cache, lazy init), the Russian stress layer over three sources, and differential tests against the Python package.

**Scale.** 3,308 files · 84,800 LOC · 77 workflows · 140,004 CI runs.

### 4.2 Poetry platform — [thelegendarypoet.ru](https://thelegendarypoet.ru)

React 19, TypeScript, Vite 7, Tailwind 4, Framer Motion: twelve poets, long-form documented essays, a music section with three published tracks (SHA-256 and waveform each), and a community layer as a Cloudflare Worker with D1 and Turnstile — HMAC-signed requests, moderation, bot protection — deliberately separate from the static site.

**The engineering story.** `route-contract.json` is the single machine manifest for routes, redirects, sitemap, QA and budgets. A release workflow refuses to publish a track without a master file, hash and duration.

**Scale.** 49,063 LOC · 23 workflows · 27,586 CI runs.

### 4.3 AI media pipeline — `mp3telegrambot`

Link in, Russian media package out: MP3 with cover art, topic, timecodes, quotes, summary, Shorts — plus translation through Yandex LiveDub with semantic QA and automatic repair of confirmed bad segments.

**The engineering story.** Fail-closed startup: if the local Bot API is unreachable, the process dies before downloading a feature-length video, with no silent cloud fallback. Hash-locked dependencies, secret scanning in CI.

**Scale.** 936 modules · 208,644 LOC of Python · 579 test files · 20 workflows.

### 4.4 Multi-channel publishing platform — `video-channel-manager`

Read-only audit snapshots, versioned change plans, exact remote IDs, per-target single-writer locks, operation journals, backups, postcondition reads after every write, guarded rollback, SHA-256 media fingerprints.

**The engineering story.** The AI analyses; a deterministic executor acts. Agents never receive provider tokens. Ambiguous states are marked `never_replay`. The repository also holds the frozen 111-pair YouTube↔VK mapping and the dated channel snapshots.

**Scale.** 919 modules · 219,040 LOC of Python · 461 tests · 31 workflows.
Supply chain: 241 workflows, 754/754 external actions pinned to a full 40-character SHA (local `./.github/actions` excluded — they are pinned by the commit itself), 241/241 declare least-privilege permissions, zero `write-all`, and both `pull_request_target` workflows are fork-guarded with no checkout of PR code.

Across nine repositories: 3,834 pull requests, 2,877 merged (75%), 16 open issues in total, 391 verification reports, and one full test run of 4,487 tests.

### 4.5 Commercial site, zero dependencies — [milovicake.ru](https://milovicake.ru)

Catalogue, price calculator, delivery, reviews, PWA, video gallery, and 14 geo landings generated from a single CSV with an idempotency check.

**The engineering story.** QA is the product: JS validation, accessibility, release identity by SHA, Lighthouse regressions and aggregation, security audit, suburb idempotency, Playwright desktop/mobile/responsive matrix, plus contracts proving the live 404 is a real 404 and that prices and hours match reality.

**Scale.** 34 pages · 48,384 LOC · 111 PRs · 3,745 CI runs.

### 4.6 Editorial library, 157 sourced articles — [french.milovicake.ru](https://french.milovicake.ru)

An Astro SSG library on the French pastry tradition: chefs, techniques, recipes, market analysis, and a curated fifteen-piece collection with its own entity model.

**The engineering story.** Fail-closed SEO: the build fails if titles collide, canonicals are wrong, JSON-LD disagrees with visible content, or a generated illustration lacks honest provenance. IndexNow fires only after a verified deploy.

**Scale.** 157 articles · ≈146,000 words · 7 workflows.

### 4.7 Channel and AI production — [@TheLegendaryPoet](https://www.youtube.com/@TheLegendaryPoet)

**What exists.** Russian poetry set to music; long clips, short formats, poet playlists, community posts and quizzes. Music, visuals and editing are AI-assisted; the process is written down as protocols and a visual canon. Audience counters are deliberately not part of the portfolio — see [MEDIA_PRACTICE.md](MEDIA_PRACTICE.md).

**The production line.** A Suno department with a protocol that forbids rewriting the poem, resolves homographs instead of guessing, and defines pronunciation repair and review cases. A clips department with a visual canon, scene-by-scene storyboarding against the song's meaning, motion prompts only for approved frames, and acceptance rules. Three tracks published on the site with hashes and waveforms. Distribution with exact YouTube↔VK pairs, native VK uploads, RuTube, Telegram channels publishing on schedule, and prepared Reel jobs held at "rights not granted".

**The engineering story.** Exact object identity instead of "roughly that video". Dated `yt-dlp` snapshots. An explicit rule that an existing upload grants no rights to the media. A ban on downloading other people's video for re-upload. Every publication has a state and a postcondition.

**How to read this.** What is auditable here is the process, not the audience: dated snapshots, protocol files, acceptance rules, and the state of every publication. Counting subscribers would add a number nobody can verify and nothing that says how the work is done.

### 4.8 Research infrastructure — `AuditRepo` and `Research`

Two systems that exist because agents generate reports faster than humans can read them. AuditRepo: passes → evidence → verification → dedup and root-cause → compact working MASTER → decision → verify → retire. Research: an evidence model with source classes A1–D, independent axes for access, locator, rights and publication, and typed HOLD flags. One root-authority document per repository; never selected by a date in a filename; read-only validators.

**Scale.** 2,786 files and 120 MB of evidence · 2,076 documents and ≈3.9M words.

---

### Visual direction and design review: five live cases (5 Nov 2026)

My contribution to the visual layer is to **define each product's character**, brief the composition, typography and responsive behavior, compare alternatives, critique inconsistencies and review the revised output. The goal is fit for the audience and content, not ornament for its own sake. Some code, imagery, layouts and visual alternatives were created with AI and other tools. These cases **do not imply** that I hand-designed every asset, have professional Figma proficiency, or conducted formal UX studies.

The [published visual-direction cases](https://fedormilovanov.github.io/portfolio/en/#visual) show **live products**, dated desktop/mobile screenshots and unresolved trade-offs:

- **Theological library:** quiet academic typography, paper-like surface and original languages; long-form reading comfort and mobile interaction consistency still need review.
- **The Legendary Poet:** a dark, museum-like atmosphere with arched portraits and cool blue light; its oversized heading competes with content above the fold, while small-screen navigation needs legibility checks.
- **Milovi Cake:** product photography and warm premium colors; third-party messaging and rating badges sometimes interrupt palette consistency.
- **Pâtisserie Russe / Milovi School:** an editorial identity with large serif display type and process photography; consent notices can obscure the mobile opening composition.
- **Milovi Cake wedding page:** restrained ivory tones and a soft composition; the cake image is labeled as a **style visualization**, not evidence of a delivered order.

**Evidence and boundaries:** [EN case studies](https://fedormilovanov.github.io/portfolio/en/#visual) · [RU case studies](https://fedormilovanov.github.io/portfolio/#visual) · [portfolio website PR #4](https://github.com/FedorMilovanov/FedorMilovanov.github.io/pull/4) (published 5 Nov 2026). There are no substantiated design-to-conversion metrics or verified before/after comparisons, and none are claimed.

## 5. Stack

**Languages.** TypeScript, JavaScript, Python, Astro, SQL.
**Frontend.** Astro, React 19, Next.js App Router, Vite, Tailwind, Framer Motion, dependency-free vanilla.
**Backend and data.** Flask/Waitress, Telegram Bot API and Mini Apps, MongoDB Atlas, Cloudflare Workers and D1, SQLAlchemy and Alembic, Playwright.
**AI.** Gemini API for video analysis, Yandex LiveDub, Suno for music, image and video generation for clips, ONNX Runtime Web with the open-source `vosk-tts` for in-browser speech, agent pipelines for task design, contracts and acceptance.
**Media and distribution.** YouTube Data API, VK API, RuTube, Telegram Bot API, `yt-dlp`, ffmpeg, SHA-256 media fingerprints, waveforms.
**Infrastructure.** GitHub Actions (241 workflow files in the 1 Nov 2026 snapshot), GitHub Pages, Vercel, Render, Docker, IndexNow, Pagefind, Lighthouse CI, service workers.

---

## 6. How I work

1. **Contract before code.** A machine-readable source of truth first, then an implementation that must conform.
2. **Fail closed.** An unsupported claim gets removed or narrowed. A build that cannot prove itself does not ship.
3. **Separate truths.** Source ≠ build ≠ production. `merge ≠ deploy`.
4. **Postconditions over hope.** Read back after every write, verify live bytes after every deploy, confirm the object exists after every publication.
5. **One owner per surface.** One branch, one PR, one accountable person.
6. **Exact identity.** Not "that video" but a specific ID on a specific platform. An existing upload grants no media rights.
7. **Humans own the editorial line.** Agents do not silently fix facts, interpretations, punctuation or pick the final frame.

---

## 7. What I am looking for

- **AI reliability and agent governance.** Teams shipping agent-built software who need contracts, gates, evals and acceptance criteria.
- **AI media production.** Studios, labels and publishers who want a repeatable pipeline from text to song to clip to distribution — with rights and identity handled properly.
- **Editorial technology.** Publishers, museums, edtech and non-profits turning expertise into verifiable digital libraries.
- **Rescue work.** A codebase generated in a week that nobody dares to touch.

Working languages: Russian (native), English (working — actively improving).

---

## 8. Honest FAQ

**"So an AI wrote this?"**
A large share of the code and part of the media, yes — under my direction. Mine are the requirements, architecture, contracts, editorial decisions, acceptance, publication and accountability. That is exactly why I built a verification methodology.

**"Is the voice on your site yours?"**
No. The Vosk TTS source code is Alpha Cephei's Apache-2.0 project, while the Russian 0.9 voice-model weights are a separate third-party asset under an outstanding redistribution-rights check (`MODEL_RIGHTS_HOLD`). I built the browser integration and Russian stress layer, not the voice model.

**"Is the music yours?"**
The tracks are produced in Suno from my lyrics, prompts, selection and mastering. I am not a composer or performer; I am the editorial author and producer of the production. The poems are public domain; the audio and clips are my derivative works.

**"Are you a senior software engineer?"**
No, and I do not claim to be one inside a large team. I am a product engineer and technical editor who builds end-to-end with agents, reads code, debugs production, and owns the outcome.

**"Why so many commits?"**
Work happens in small verifiable steps under CI. The number itself means nothing; five live products and a channel that publishes does.

**"What was the hardest part?"**
Stopping the agent from lying. It says "done" with complete confidence when it is not done.

---

## 9. To fill in

- [ ] A profile README and repository descriptions, per `PROFILE_README.md`.
- [ ] One public write-up on how AI-assisted builds and AI media are verified.
- [ ] A photo and three screenshots or recordings per project and for the channel.
- [ ] Contact details: email, Telegram, LinkedIn.
- [ ] English READMEs for `mp3telegrambot` and `video-channel-manager`.
- [ ] One 1,200-word write-up: "How I make AI-built products and AI-made media trustworthy".
