# TRADING.md — Agentic RH desk playbook

Last updated: 2026-09-14 22:10 CT  
Scope: Robinhood **Agentic** account only. Individual account is off-limits. Closed pot — no deposits.

Not financial advice. Live numbers belong in chat, not this public repo.

---

## Walls (the only hard rules)

1. Trade **only** the Agentic RH account.
2. **Never** touch the Individual / default account.
3. Closed pot: cash + assets already on Agentic. No ACH, wires, refills.

Everything else (old $100 cap, “don’t sell crypto because spread”) is operator judgment, not a wall.

---

## Mission

- Floor: **+$300 profit in 30 days** (clock started 2026-09-14).
- Aim: **+$1,000 profit** by ~2026-10-13.
- Baseline AV is the 2026-09-14 21:56 CT mark in the session log — do not rebase quietly.

Straight talk: +$1k is ~+44% on a ~$2.25k book with **no options enrolled**. That is a stretch, not a promise. Do not manufacture it with lottery tickets.

---

## Quant layer (from X / Grok-bot research)

Source of truth for *how* to size, not *what* to buy:

- [@velesxbt](https://x.com/velesxbt/article/2095813892794408990) — Alpha Arena: 6 models, $10k real, 4 blew up (GPT-5 −63%). Winners were not “smarter.” They had a quant layer.
- Pipeline: **Grok (analyst) → quant (risk) → broker**. Quant has last word.
- [Grok Bots + AI Trading Workflows](https://theaileverage.beehiiv.com/p/grok-bots-ai-trading-workflows-for-beginners) — four-bot desk: Scout → News → Risk → Head. Human in the loop.

### Knobs we actually use

| Knob | Default on this desk |
|---|---|
| Max risk / single name | 20% of AV on a *new* add; core TSLA may sit higher but do not push it back over ~70% |
| Ticket size | $300–$500, not $100 habit |
| Daily kill | −$150 session (realized + unrealized from session start) → no new orders |
| Turnover | At most **one** new risk ticket per cycle unless flattening |
| Min conviction | Need a one-line edge **and** an invalidation. No “it’ll come back.” |
| Fees / spread | RH crypto MM book ~1.9% — do not *reload* it. If we won’t trade it, we sell it. |

Half-Kelly in spirit: size down when VIX/oil/10Y are violent. Never full-Kelly a $2.2k book.

### What blew up the other bots (do not copy)

- Overtrading (turnover tax)
- No daily kill
- Betting full conviction with no vol scale
- Moving stops / “it’ll come back” ([@ApexGoldAlgo](https://x.com/ApexGoldAlgo/status/2098593969001083376))
- Small account + oversized risk to “make the number”

---

## X tape we keep (week of 2026-09-14)

- [@itsjcmerlo](https://x.com/itsjcmerlo/status/2099473148953448746): buy-dip premarket = extremely risky; buy through Wed = very risky; **wait until FOMC = risk-neutral**.
- [@septinvesting66](https://x.com/septinvesting66/status/2099233041713373233): trim high-beta before Wed 2pm ET; no new longs Mon–Tue in rate-sensitive names.
- [@1ChartMaster](https://x.com/1ChartMaster/status/2086787063815229930): buy *tight-risk* spots (flag / MA), **trim into vertical strength**.
- [@CyclesFan](https://x.com/CyclesFan/status/2099589881148194901): QQQ bounced off lower BB Mon; reaction to Wed hike likely the real tell.

Ignore: miracle $75→$5k threads, prop-firm affiliate spam, “AI printed $1k/day” without a fill log.

---

## This week’s regime

- FOMC **Tue–Wed 2026-09-15/16**. Decision **Wed 2:00pm ET** + SEP + Warsh presser.
- Hike to 3.75–4.00% priced ~87–93% (FedWatch / Reuters poll 2026-09-14).
- Oil ~$100+, 10Y near 5%, chips sold Monday, VIX mid-teens.
- Tuesday is positioning. **Wednesday is the event.**

---

## Book rules (names we own)

**TSLA (core)**  
EV share rebound, Roadster **Oct 1**, earnings ~Oct 21. Valuation is the tax.  
- Do not add if it is already ≥50% of AV.  
- Add **1 share only** if dumped sub-Mon-low with a real bid.  
- Invalidation: gap through $350 on hike rhetoric → no add, consider another trim.

**RKLB**  
Electron flying, Neutron still “pad in Q4” not a dated launch. Chart $151 → ~$63.  
- Let the queued RTH sell print.  
- Do **not** buy it back at the open unless it gaps $3+ for no news.

**NNE**  
Pre-revenue microreactor, beta ~5.4, 52w $14.71–$60.87. MOUs ≠ revenue.  
- Hold the small sleeve.  
- Add only if it tags the 52w low and holds. Trim a rip with no contract.

**Crypto on RH**  
MM routing ~1.9% round-trip. Sold the BTC sleeve when told to stop complaining. Do not reload RH crypto to look busy. Dust can sit.

**Options**  
Not enrolled on Agentic. Covered calls need 100 shares (we don’t have them). CSPs need strike×100 cash (we don’t). Long premium with $900 is a lottery ticket. Enroll L2 later if we want defined-risk *after* cash exists — not as the +$1k plan.

---

## Tuesday open checklist

1. Read live book (cash, positions, MVs). Numbers only.
2. Confirm RKLB queued market sell fill. Do not cancel unless thesis flipped.
3. Thesis ≤5 lines: edge, invalidation, size.
4. At most **one** new risk ticket (plus the already-queued RKLB sell).
5. Log: ticker, side, notional, reason, remaining daily-loss room.
6. If ES −0.8%+ and bid is gone in first 30 min → stand down to Wed 1:50pm ET.

### Deploy bias for the cash pile

| Bias | Action |
|---|---|
| Base | Hold most cash through Tue. Probe only if a *liquid* name is offered cheap. |
| Probe | $300–$450 in one liquid name — or +1 TSLA only sub-$350. |
| Avoid | RH crypto reload, NNE add, RKLB bounce-fade, options. |

---

## Session log format

```
DATE / CT
Cash / Equity / Crypto / AV
Positions (ticker qty mark)
Order: id side qty px notional state
Day P&L vs −$150 kill
Progress vs +$300 / +$1,000
```

---

## Sources

- Veles, *4 of 6 AI Trading Bots Blew Up* — https://x.com/velesxbt/article/2095813892794408990
- AI Leverage, *Grok Bots + AI Trading Workflows* — https://theaileverage.beehiiv.com/p/grok-bots-ai-trading-workflows-for-beginners
- Strategy Arena Grok paper strategies — https://strategyarena.io/en/grok-trading
- HyperGrok desk pattern — https://github.com/galleonlabs/hypergrok-trading-desk
- Reuters Fed poll 2026-09-14; CME FedWatch ~87–93% hike Wed
