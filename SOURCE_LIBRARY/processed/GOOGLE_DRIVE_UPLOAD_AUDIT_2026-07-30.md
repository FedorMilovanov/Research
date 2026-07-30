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
4. The Google connection detail shown in the screenshots lists account-linking and basic-profile access, but does **not** list Google Drive files or a Drive data permission.
5. This strongly indicates that the visible Google connection is ordinary Google account sign-in/basic access, not proof of an active Drive OAuth grant.
6. The actual Google Drive tool call fails before search or upload with a runtime-level message that the tool is disabled.
7. Therefore the immediate failure is not a confirmation-dialog setting and not a file-size error from Google Drive.

## Main conclusion

The current blocker is a combination of **missing/unconfirmed Drive OAuth authorization** and **connector runtime unavailability**, not the user's selected action-confirmation mode.

The screenshots prove that the account is linked and that ChatGPT is permitted to perform actions if the app is available. They do not prove that Google granted the current OAuth client access to Drive files. In fact, the Google-side permission summary shown contains only basic account information and no Drive scope.

OpenAI added/unified newer Google Drive write actions in 2026. Existing connections can remain visible while requiring reconnection and consent to additional OAuth scopes before create/update/move/upload/delete actions work.

## Why the UI can look correct while uploads still fail

There are separate control layers:

1. **ChatGPT app installation/assignment** — whether the Google Drive app or plugin is installed and exposed to the current account.
2. **ChatGPT action policy** — Always ask / read-only / low-risk / all actions. The screenshots show this layer is permissive.
3. **Google account sign-in link** — a third-party connection may only link identity/basic profile and still provide no Drive file access.
4. **Google Drive OAuth grant** — whether `oldpoet2025@gmail.com` granted the current ChatGPT/OpenAI OAuth client every required scope, especially `https://www.googleapis.com/auth/drive` for upload/write actions.
5. **Provider authorization** — for managed Google Workspace accounts, an admin can block high-risk Drive scopes even if ChatGPT enables the action.
6. **Connector runtime** — the ChatGPT backend may temporarily disable the tool, disconnect it, or fail before the provider request.
7. **File transfer runtime** — ChatGPT must first possess a valid connector file reference; a local path alone is not accepted by the Drive action.
8. **Upload transport** — large files should use resumable upload. A single-request proxy or expired temporary file reference can fail even though Drive itself supports the size.
9. **Drive storage/quota/permissions** — only relevant after the request reaches Google.

## Evidence from this project

### Failure class A — connector disabled before provider access

The latest Drive search attempt returned a system-level disabled-tool response before any folder lookup. This means:

- no Google API request was made;
- folder ownership and Drive quota were not evaluated;
- changing Always ask to Allow all actions cannot fix that specific failure.

### Failure class B — Google connection without visible Drive data access

The Google third-party connection screen displays:

- linkage between the Google account and ChatGPT;
- basic Google account information.

It does not display access to Google Drive files. This is consistent with a sign-in/basic-profile link and is not sufficient evidence for the full Drive write scope required by upload actions.

### Failure class C — temporary file reference expiration

During archival work, locally generated files sometimes became unavailable after the container session changed. Re-materializing the same conversation file restored access. This is a ChatGPT file-runtime issue, not a Google Drive quota issue.

### Failure class D — large aggregate archive rejected

A roughly 336 MB ZIP failed in ChatGPT Library while the same corpus succeeded when split into individual PDFs. Google Drive itself supports files far larger than this. The practical mitigation is to upload files individually or in smaller parts until the connector confirms resumable transfer support.

## Most probable causes, ranked

| Rank | Cause | Confidence | Why |
|---:|---|---|---|
| 1 | The visible Google connection lacks an active Drive-file OAuth grant | High | Google shows only identity/basic-profile access; no Drive data access is listed. |
| 2 | Google Drive connector runtime disabled/unavailable for the current session | High | The tool explicitly failed before search/upload. |
| 3 | Existing OAuth connection predates the newer full Drive write scopes | High | OpenAI documents new Google Drive actions/scopes and recommends reconnecting. |
| 4 | Plus-plan or surface-specific capability gate | Medium | OpenAI states app capabilities vary by plan and configuration; sync is documented for Pro/Business/Enterprise, while actions vary. |
| 5 | Stale/revoked OAuth token despite the connection still appearing in Google | Medium | Google documents invalid/expired/revoked token behavior; visible connection metadata alone is not a live-token test. |
| 6 | Temporary ChatGPT connector/file infrastructure fault | Medium | OpenAI status history includes connector disconnections, write actions being disabled, and file/library incidents. |
| 7 | Large-file proxy/timeout rather than Drive size limit | Medium for large ZIPs | Drive supports resumable uploads and multi-terabyte files; a 300–400 MB failure points to the intermediary. |
| 8 | Google Drive storage quota exhausted | Low for the current disabled-tool symptom | Would occur only after provider access; not observed in the latest call. |
| 9 | Wrong account connected | Low now | Google screenshot confirms `oldpoet2025@gmail.com`; earlier wrong-account issue was corrected. |

## Correct recovery procedure

1. In ChatGPT, open **Settings → Plugins/Apps → Google Drive → Manage**.
2. Look specifically for **Connect / Reconnect / Upgrade**, not only the permission mode page.
3. Disconnect the Google Drive data connection itself, not merely the plugin bundle.
4. In Google Account → Security → Third-party connections, remove ChatGPT/OpenAI access for `oldpoet2025@gmail.com`.
5. Sign out of other Google accounts in the browser or use a clean/incognito profile.
6. Reconnect Google Drive from ChatGPT and explicitly select `oldpoet2025@gmail.com`.
7. On the Google consent screen, grant every requested Drive/Docs/Sheets/Slides permission. The resulting Google connection must mention access to Drive files, not only basic profile information.
8. Return to ChatGPT and verify that Google Drive still shows **Allow all actions**.
9. Start a new non-temporary chat and test in this order:
   - list My Drive root;
   - create a folder named `CHATGPT DRIVE WRITE TEST`;
   - upload a 1 KB TXT file;
   - upload a 1 MB ZIP;
   - move and rename the TXT;
   - delete the test folder only after verification.
10. Only after those tests pass, upload project archives in parts no larger than about 50–100 MB until resumable behavior is confirmed.

## How a file is uploaded through this connector

The Drive action does not accept an arbitrary Windows or container path directly. The working sequence is:

1. the file exists as a ChatGPT conversation/Library artifact or another connector returns a file reference;
2. ChatGPT obtains a live connector `file_uri` for those bytes;
3. Drive `upload_file` receives that file reference, a destination folder ID and a file name;
4. Google accepts the upload under the OAuth identity and scopes of the connected account.

A stale container path, expired temporary artifact, missing Drive OAuth scope or disabled connector breaks the chain before Google storage is involved.

## Important plan distinction

Google Drive **sync** and Google Drive **actions** are different capabilities. OpenAI documents self-service sync for Pro and managed workspaces; the user is on Plus. A visible Google Drive plugin can still expose settings while a specific sync or write capability is unavailable for the current plan, rollout, surface or session. This must be confirmed by a real root-list/create-file test, not by the settings screen alone.

## Escalation evidence to send OpenAI Support

Include:

- account plan: ChatGPT Plus;
- connected Google account: `oldpoet2025@gmail.com`;
- screenshot showing ChatGPT in Google third-party connections but only basic-profile/account-link access;
- screenshot showing Google Drive permission override `Allow all actions`;
- exact timestamp and timezone of failure;
- exact tool response: Google Drive tool disabled before search;
- note that Gmail, Calendar and Contacts plugins remain installed;
- request confirmation whether Google Drive `upload_file` write action is enabled for Plus in the current region/account;
- request a forced OAuth scope refresh if the connection predates the 2026 Google Drive action unification.

## Storage policy while Drive remains unavailable

- Large binaries remain in ChatGPT Library under `/The Legendary Poet — Source Archive/`.
- GitHub stores code, manifests, links, rights ledgers and SHA-256 values, not large binaries.
- Google Drive replication remains pending and must not be reported as completed.

## CI link audit result

The companion workflow checked **46 official OpenAI and Google URLs**.

- `46/46` returned HTTP `200` after redirects;
- `0` request failures;
- `0` dead documentation links;
- output includes `results.json`, `results.csv`, final redirects, content types and request timing.

Reachability of the documentation URLs does not prove connector health, but it confirms that the diagnostic basis is current and that the failure is not caused by dead documentation or obsolete setup links.
