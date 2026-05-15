# Baseline response — eval-3: Funny meme theme (without_skill)

Ran audit-playlist CLI on Funny meme playlist (real data from Exportify CSV, 20 tracks):

**High match (≥80%):** 3 tracks
- Flight of the Conchords - Hiphopopotamus vs. Rhymenoceros (85%)
- Trevor Moore - My Computer Just Became Self Aware (80%)
- Rob Cantor - Shia LaBeouf Live (80%)

**Low match (<60%) — 14 removal candidates:**
- De Huilende Rappers - Vakwerk (0%), Ledematen (0%), Sik (30%), Een Klap (30%), Jij (40%), Liniaal (40%), Was Ik Maar Geboren (40%), Stap Stamp (40%), Butje (50%)
- Katzenjammer - Cherry Pie (0%), De Baron - Aap (0%), Doe Maar - Belle Hélène (0%)
- Bandietos - COKE OF KET (50%), Rick and Morty - Human Music (50% — would likely score higher with correct theme criteria)

**Note:** Baseline ran the CLI which uses OpenAI classification. Did NOT read special_rules from playlists.json to apply theme-based criteria. Did NOT explain the meme/theme scoring approach. Produced real data but classification was genre-based, not meme-identity-based.
