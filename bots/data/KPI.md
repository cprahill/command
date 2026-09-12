# Workforce KPI (paper + ops)
Score nightly. Higher = better. Birth parents = top 2 living by `score`.

| Signal | Weight | How |
|--------|--------|-----|
| jobs_pass_7d | 40 | drills PASS last 7 days |
| verify_green_streak | 20 | consecutive verify_books / seat checks OK |
| equity_delta_7d | 25 | paper $ contributed (trade seats); 0 if N/A |
| idle_penalty | -15 | hours since last proven write / report |
| lesson_filed | 5 | LESSONS append this week |

`score = 40*pass_rate + 20*streak_norm + 25*equity_norm - 15*idle_norm + 5*lesson`

**Terminate** if: score bottom 20% for 3 nights OR fail same drill twice without lesson OR idle > 48h with no report.
**Birth** if: living < cap AND two parents score ≥ P75 AND hybrid ROLE drafted + Critic-style PASS on ROLE.md.
**Cap:** start 4 living seats (paper-desk, trade-dev, swarm-mr, swarm-event). Cap rises only when Christopher dests.
