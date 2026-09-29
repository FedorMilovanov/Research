# Steven J. Lawson — OnePassion live DNS / web-infrastructure continuity audit

**Snapshot:** 2026-09-29  
**Status:** `DOMAIN DNS ACTIVE / MAIL INFRASTRUCTURE ACTIVE / PUBLIC WEB ENDPOINT CURRENTLY UNREACHABLE TO TEST CLIENTS / DOMAIN ABANDONMENT NOT SUPPORTED`

## 1. Why this matters

The broader OnePassion audit established a strong post-September-2024 public-ministry dormancy pattern:

- podcast feeds stop;
- public events were cancelled;
- OnePlace marks the ministry unavailable;
- no new OnePassion-produced public teaching series has been located;
- the main website is not presently retrievable through the available normal web clients.

A failed website request can be misleading, however. It can mean:

- the domain expired;
- DNS was removed;
- hosting was shut down;
- the application is offline;
- the origin rejects automated clients;
- TLS/WAF configuration blocks the request;
- the site was intentionally disabled while other infrastructure remains.

Therefore a separate DNS check was run before characterizing the domain as abandoned.

---

## 2. Live DNS result — 2026-09-29

A direct DNS lookup of:

> `onepassionministries.org`

returned active records.

### A records

- `141.193.213.11`
- `141.193.213.10`

### AAAA

- no IPv6 record located

### MX

Google mail infrastructure remains configured:

- priority 1 — `aspmx.l.google.com`
- priority 5 — `alt1.aspmx.l.google.com`
- priority 5 — `alt2.aspmx.l.google.com`
- priority 10 — `aspmx2.googlemail.com`
- priority 10 — `aspmx3.googlemail.com`

### TXT

The domain retains verification records including:

- Google site verification tokens;
- `NETORGFT11382225.onmicrosoft.com`.

### Nameservers

- `ns49.domaincontrol.com`
- `ns50.domaincontrol.com`

### SOA

- primary nameserver: `ns49.domaincontrol.com`
- hostmaster: `dns.jomax.net`
- serial observed: `2024021308`

The DNS inspection was run live on Sept. 29, 2026.

---

## 3. Web retrieval state

On the same date, attempts to retrieve:

- `https://onepassionministries.org`
- `https://www.onepassionministries.org`
- `http://onepassionministries.org`

through the available web clients did not produce a normal public site response.

The HTTPS forms were reported as unreachable by one renderer; HTTP returned a nonstandard failure response in that client.

### Guardrail

This is **not** enough to say:

- the website no longer exists;
- the hosting account was cancelled;
- the domain is parked;
- the organization abandoned its domain.

The live DNS/MX evidence points the other way: the domain remains actively configured at the infrastructure level.

---

## 4. Evidentiary synthesis

The most precise current model is:

> **PUBLIC CONTENT DELIVERY: DORMANT/NOT NORMALLY RETRIEVABLE.**  
> **DNS DOMAIN: ACTIVE.**  
> **MAIL ROUTING: ACTIVE CONFIGURATION PRESENT.**  
> **DOMAIN OWNERSHIP/ADMINISTRATION: APPARENTLY MAINTAINED, THOUGH CURRENT OWNER/OPERATOR NOT IDENTIFIED BY DNS ALONE.**

This reinforces the distinction already established in `57_`:

- OnePassion's public ministry operation appears dormant;
- OnePassion's nonprofit/legal and technical infrastructure did not simply vanish.

---

## 5. Why the MX/TXT layer matters

Keeping active Google MX records and verification TXT records does not prove that staff are actively reading OnePassion email accounts.

It does show that the domain has not merely collapsed to an empty DNS state.

Likewise, the Microsoft verification token may reflect an older or current tenant relationship; it does not prove current use of Microsoft 365.

Safe wording:

> As of Sept. 29, 2026, OnePassion's public website was not normally retrievable through the tested web clients, but the domain itself remained actively configured with A records, Google mail routing and verification records. The evidence therefore supports public-web dormancy, not abandonment of the domain or disappearance of the organization.

---

## 6. What this does NOT answer

DNS does not identify:

- current OnePassion president;
- current board members;
- who controls the domain registrar account;
- who reads OnePassion email;
- whether paid staff remain;
- whether the website is intentionally disabled;
- whether the current A-record hosts still contain the historical site;
- whether internal OnePassion activity continues.

Those remain governance/operational questions.

---

## 7. Next acquisition targets

1. Historical DNS/hosting changes around Sept.–Oct. 2024 and May 2025.
2. Archived site snapshots after Lawson's resignation for any leadership/footer changes.
3. Certificate-transparency history for subdomains that may reveal active admin/service endpoints.
4. Any public OnePassion email or board communication after Sept. 2024.
5. Direct identification of the replacement president and Jan. 2025 board.

## Research conclusion

> **THE LIVE DNS CHECK CORRECTS AN IMPORTANT POSSIBLE OVERSTATEMENT. ONEPASSION'S WEBSITE IS NOT CURRENTLY RETRIEVABLE THROUGH NORMAL TEST CLIENTS, BUT `ONEPASSIONMINISTRIES.ORG` REMAINS AN ACTIVELY CONFIGURED DOMAIN WITH LIVE A RECORDS, GOOGLE MX ROUTING, VERIFICATION TXT RECORDS AND MAINTAINED NAMESERVERS. THIS SUPPORTS THE EXISTING MODEL OF PUBLIC-MINISTRY DORMANCY PLUS CONTINUING CORPORATE/TECHNICAL INFRASTRUCTURE — NOT A CLAIM THAT ONEPASSION OR ITS DOMAIN SIMPLY DISAPPEARED.**
