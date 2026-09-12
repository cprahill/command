# Phone control (public HTTPS)

**Open on phone/iPad:** https://grok-command.vercel.app/phone/

Alias: https://grok-command.vercel.app/ctl/

SoT refresh (Mini, 0 LLM):

```
~/Desktop/Christopher/project-first/harness/scripts/phone-status.sh
```

Control (Grok Bot → Mini shell, no spend/send):

```
~/Desktop/Christopher/project-first/harness/scripts/phone-ctl.sh status
~/Desktop/Christopher/project-first/harness/scripts/phone-ctl.sh restart twin
```

Tailscale `http://100.x:8790/phone.html` is Mini/LAN only. Chat apps and cellular often cannot open 100.x. Proof is this HTTPS URL returning 200 with Paper/Services filled — not localhost.
