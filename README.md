# COMMAND

Public command center for Grok Bot on phone/iPad. Not Baja.

| Path | Role |
|------|------|
| `/harness/` | **Live system board** — COM, services, $0/$500. https://cprahill.github.io/command/harness/ |
| `/phone/` | Mini status + Bot phrases. https://cprahill.github.io/command/phone/ |
| `/bots/` | Workforce KPI cards |
| `/paper/` | Paper desk (fake money) |
| `/neural/` | 3D harness mesh |
| `/` | Hub |

Live Mini (LAN/Tailscale only): harness `:8790` · paper `:8791` · twin `:8787`.

Proof: HTTPS 200 on `/harness/` from cellular, matching Mini `status.json`. No wallets.
