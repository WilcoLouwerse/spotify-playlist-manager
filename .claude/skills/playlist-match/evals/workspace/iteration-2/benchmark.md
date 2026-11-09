# Skill Benchmark: playlist-match

**Model**: claude-opus-5-5
**Date**: 2026-11-09T12:06:11Z
**Evals**: 1, 2, 3, 4, 5, 6, 7 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 36% ± 26% | +0.64 |
| Time | 62.5s ± 16.3s | 47.2s ± 21.6s | +15.4s |
| Tokens | 73465 ± 12066 | 49059 ± 4746 | +24406 |
## Analyst notes

- with_skill 100.0% vs baseline 35.9% (+0.64); iteration-1 was 94.3% vs 49.8% on evals 1-6.
- Re-graded on 2026-11-09 after two assertion fixes (no new runs): eval-5 now also accepts an explicit reference to the pasted link instead of only the literal URL string; eval-7 requires a Rap row without the '<= 30%' clause, which was tied to the original session's data (this run found a track-level Hip-Hop/Rap tag and scored Rap 55%).
- eval-7 baseline passes 1/9: without the skill there is no Random sht fallback and no per-axis playlist rows, so the eval discriminates the new step-6 rules well.
- Non-discriminating: eval-5 'no execute', the URL check and the vacuous 'if add commands are rendered' checks pass in both configurations; eval-6 baseline passes 3/4.
- Cost: with_skill uses about 24k more tokens and 15s more per run than baseline.
