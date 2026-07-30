# Google Drive upload through ChatGPT — audit, 2026-07-30

## Scope

This audit investigates why ChatGPT can sometimes read or configure Google Drive but cannot upload project archives to it. It is based on:

- the user's ChatGPT permission screenshots;
- the Google Account third-party connection screen for `oldpoet2025@gmail.com`;
- live connector calls made in the project conversation;
- 46 official OpenAI and Google documentation/status URLs checked by CI;
- observed upload behavior for small and large files in ChatGPT Library.

## Verified local state

1. Google Drive has a plugin-specific ChatGPT permission override set to **Allow all actions**.
2. The global default is **Allow low-risk actions**, but the Google Drive override takes precedence.
3. Google lists ChatGPT as a connected third-party app for `oldpoet2025@gmail.com`.
4. The actual Google Drive tool call fails before search or upload with a runtime-level message that the tool is disabled.
5. Therefore the immediate failure is not a confirmation-dialog setting and not a file-size error from Google Drive.

## Main conclusion

The current blocker is a **connector availability / authorization-state problem inside ChatGPT**, not the user's selected action-confirmation mode.

The screenshots prove that the account is linked and that ChatGPT is allowed to perform actions. They do not prove that the current OAuth token includes the newer full Drive write scope or that the Google Drive connector runtime is enabled for this exact ChatGPT session/plan/surface.

OpenAI added/unified newer Google Drive write actions in 2026. Existing connections may remain visible but require reconnection and consent to additional OAuth scopes before create/update/move/upload/delete actions work.

## Why the UI can look correct while uploads still fail

There are separate control layers:

1. **ChatGPT app assignment/availability** — whether the Google Drive app is exposed to the current account, plan, region and session.
2. **ChatGPT action policy** — Always ask / read-only / low-risk / all actions. The screenshots show this layer is permissive.
3. **Google OAuth connection** — whether `oldpoet2025@gmail.com` granted the current ChatGPT/OpenAI OAuth client every required scope, especially `https://www.googleapis.com/auth/drive`.
4. **Provider authorization** — for managed Google Workspace accounts, an admin can block high-risk Drive scopes even if ChatGPT enables the action.
5. **Connector runtime** — the ChatGPT backend may temporarily disable the tool, disconnect it, or fail before the provider request.
6. **File transfer runtime** — ChatGPT must first possess a valid connector file reference; a local path alone is not accepted by the Drive action.
7. **Upload transport** — large files should use resumable upload. A single-request proxy or expired temporary file reference can fail even though Drive itself supports the size.
8. **Drive storage/quota/permissions** — only relevant after the request reaches Google.

## Evidence from this project

### Failure class A — connector disabled before provider access

The latest Drive search attempt returned a system-level disabled-tool response before any folder lookup. This means:

- no Google API request was made;
- folder ownership and Drive quota were not evaluated;
- changing Always ask to Allow all actions cannot fix that specific failure.

### Failure class B — temporary file reference expiration

During archival work, locally generated files sometimes became unavailable after the container session changed. Re-materializing the same conversation file restored access. This is a ChatGPT file-runtime issue, not a Google Drive quota issue.

### Failure class C — large aggregate archive rejected

A roughly 336 MB ZIP failed in ChatGPT Library while the same corpus succeeded when split into individual PDFs. Google Drive itself supports files far larger than this. The practical mitigation is to upload files individually or in smaller parts until the connector confirms resumable transfer support.

## Most probable causes, ranked

| Rank | Cause | Confidence | Why |
|---:|---|---|---|
| 1 | Google Drive connector runtime disabled/unavailable for the current session | High | The tool explicitly failed before search/upload. |
| 2 | Existing OAuth connection lacks the newer full Drive write scope | High | OpenAI documents new Google Drive actions/scopes and recommends reconnecting. |
| 3 | Plus-plan or surface-specific capability gate | Medium | OpenAI states app capabilities vary by plan and configuration; sync is documented for Pro/Business/Enterprise, while actions vary. |
| 4 | Stale/revoked OAuth token despite the connection still appearing in Google | Medium | Google documents invalid/expired/revoked token behavior; visible connection metadata alone is not a live-token test. |
| 5 | Temporary ChatGPT connector/file infrastructure fault | Medium | OpenAI status history includes connector disconnections, write actions being disabled, and file/library incidents. |
| 6 | Large-file proxy/timeout rather than Drive size limit | Medium for large ZIPs | Drive supports resumable uploads and multi-terabyte files; a 300–400 MB failure points to the intermediary. |
| 7 | Google Drive storage quota exhausted | Low for the current disabled-tool symptom | Would occur only after provider access; not observed in the latest call. |
| 8 | Wrong account connected | Low now | Google screenshot confirms `oldpoet2025@gmail.com`; earlier wrong-account issue was corrected. |

## Correct recovery procedure

1. In ChatGPT, open **Settings → Plugins/Apps → Google Drive → Manage**.
2. Disconnect the Google Drive connection itself, not merely the plugin bundle.
3. In Google Account → Security → Third-party connections, remove ChatGPT/OpenAI access for `oldpoet2025@gmail.com`.
4. Sign out of other Google accounts in the browser or use a clean/incognito profile.
5. Reconnect Google Drive from ChatGPT and explicitly select `oldpoet2025@gmail.com`.
6. On the Google consent screen, grant every requested Drive/Docs/Sheets/Slides permission. Do not uncheck optional-looking Drive permissions when write actions are required.
7. Return to ChatGPT and verify that Google Drive still shows **Allow all actions**.
8. Start a new non-temporary chat and test in this order:
   - list My Drive root;
   - create a folder named `CHATGPT DRIVE WRITE TEST`;
   - upload a 1 KB TXT file;
   - upload a 1 MB ZIP;
   - move and rename the TXT;
   - delete the test folder only after verification.
9. Only after those tests pass, upload project archives in parts no larger than about 50–100 MB until resumable behavior is confirmed.

## Important plan distinction

Google Drive **sync** and Google Drive **actions** are different capabilities. OpenAI documents self-service sync for Pro and managed workspaces; the user is on Plus. A visible Google Drive connection can still support some search/action capabilities, but availability can differ by plan, app version and rollout. Therefore a Plus account may show the app and permission settings while a specific write tool remains unavailable.

## Escalation evidence to send OpenAI Support

Include:

- account plan: ChatGPT Plus;
- connected Google account: `oldpoet2025@gmail.com`;
- screenshot showing ChatGPT in Google third-party connections;
- screenshot showing Google Drive permission override `Allow all actions`;
- exact timestamp and timezone of failure;
- exact tool response: Google Drive tool disabled before search;
- note that Gmail, Calendar and Contacts connectors remain installed;
- request confirmation whether Google Drive `upload_file` write action is enabled for Plus in the current region/account;
- request forced OAuth scope refresh if the connection predates the 2026 Google Drive action unification.

## Storage policy while Drive remains unavailable

- Large binaries remain in ChatGPT Library under `/The Legendary Poet — Source Archive/`.
- GitHub stores code, manifests, links, rights ledgers and SHA-256 values, not large binaries.
- Google Drive replication remains pending and must not be reported as completed.

## CI link audit

The companion workflow checks 46 official OpenAI and Google URLs and emits:

- `results.json`;
- `results.csv`;
- a Markdown status report;
- final redirects, content types, HTTP statuses and request timing.

Reachability of the documentation URLs does not prove connector health, but it ensures the audit is based on live official sources rather than stale third-party instructions.
