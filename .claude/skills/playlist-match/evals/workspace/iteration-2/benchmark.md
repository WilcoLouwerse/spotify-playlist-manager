# Skill Benchmark: playlist-match

**Model**: claude-opus-5-5
**Date**: 2026-11-09T11:56:02Z
**Evals**: 1, 2, 3, 4, 5, 6, 7 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 96% ± 6% | 36% ± 26% | +0.60 |
| Time | 62.5s ± 16.3s | 47.2s ± 21.6s | +15.4s |
| Tokens | 73465 ± 12066 | 49059 ± 4746 | +24406 |
## Analyst notes

- with_skill 96.4% vs baseline 35.9% (+0.60); iteration-1 was 94.3% vs 49.8% on evals 1-6.
- eval-5 with_skill fail is a grader false negative: the run recognised the pasted URL as the analysed track and kept it for the add flow, but did not echo the URL string, and grade.py checks for a literal 'spotify.com/track'.
- eval-7 with_skill fail: the run found a track-level Shazam tag Hip-Hop/Rap, so Rap landed at 55% instead of <= 30%. Both new rules held (Random sht first at 85%, every genre axis has a playlist row); the '<= 30%' clause is tied to the data of the original session.
- eval-7 baseline passed 1/9: without the skill there is no Random sht fallback and no per-axis playlist rows, so the eval discriminates the new step-6 rules well.
- Non-discriminating: eval-5 'no execute' and the vacuous 'if add commands are rendered' checks pass in both configurations; eval-6 baseline passes 3/4.
- Cost: with_skill uses about 24k more tokens and 15s more per run than baseline.
