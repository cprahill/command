# Phone control (public HTTPS)

**Open on phone/iPad (live now):** https://cprahill.github.io/command/phone/

Vercel alias (quota-blocked 2026-09-12, restore after reset): https://grok-command.vercel.app/phone/

SoT refresh (Mini, 0 LLM):

```
~/Desktop/Christopher/project-first/harness/scripts/phone-status.sh
```

Control (Grok Bot → Mini shell, no spend/send):

```
~/Desktop/Christopher/project-first/harness/scripts/phone-ctl.sh status
~/Desktop/Christopher/project-first/harness/scripts/phone-ctl.sh restart twin
```

Christopher talks to Grok Bot (or Build), not iMessage. This page is status, not an inbox.

Tailscale `http://100.x:8790/phone.html` is Mini/LAN only. Proof is HTTPS 200 with Paper/Services filled — not localhost.
