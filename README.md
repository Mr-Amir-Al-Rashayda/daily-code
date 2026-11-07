<p align="center"><img src="assets/banner.svg" alt="Daily Signal — Amir Al-Rashayda" width="960"></p>

<p align="center"><strong>A living developer journal. Public APIs in, useful daily signals out.</strong></p>
<p align="center"><a href="digests/README.md">Daily issues</a> · <a href="plans/README.md">AI planning journal</a> · <a href="data/latest.json">Open data</a> · <a href="https://github.com/Mr-Amir-Al-Rashayda">My GitHub</a></p>

[Open today's full issue →](digests/2026/11/2026-11-07.md)

## AI next move

**Reviewed 2026-11-06 by local Codex · Proposed, not implemented**

### Build a safe custom-channel capacity runner

**Project:** [accelerated-blahut-arimoto](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto) · **Estimated effort:** About 2-4 hours, depending on the existing test setup

Let students and researchers supply a channel matrix and receive a reproducible capacity report instead of editing experiment source. This creates a useful foundation for a future visual Channel Lab while keeping the first change small.

**Why this next:** Carried forward after reviewing three candidates again today. The channel-capacity repository is still at revision 7de3a92172110be2615dc561abd009f13610f7de, and a fresh read of ba\_core.py confirms matrix shape is unpacked without explicit validity checks. The proposed wrapper is not shown as implemented in that inspected revision. NoteSpace sharing code was also inspected today: NoteShareUtils builds an email intent, making portable export a plausible alternative, but adding it requires broader Android integration review and device verification. Daily Signal still collects unranked top stories, yet no evidence of preferred reading topics or ranking effectiveness has emerged. The validated runner remains the most concrete small improvement; fresh source inspection supports keeping it rather than inventing another task. No solver or Android tests were run during this proposal review.

*Carried forward after reviewing the previous recommendation.*

**Implementation outline**

1. Add a small wrapper that accepts a JSON matrix and validates nonempty two-dimensional shape, finite nonnegative entries, and row sums close to one. Reject invalid matrices with clear messages instead of silently normalizing them.
2. Expose standard and relaxed solver modes through one command, with explicit tolerance and iteration limits. Label tolerance and gap in nats and capacity in bits per channel use.
3. Write a machine-readable result containing the selected method, capacity, final gap, iterations, and a convergence flag based on the requested tolerance. Do not claim acceleration from symmetric examples or a successful run when the final gap exceeds tolerance.
4. Add documented BSC and asymmetric-channel JSON examples and focused tests. Preserve the existing research code and clearly identify the new wrapper as a usability extension.

**Acceptance checks**

- [ ] Malformed, empty, ragged, negative, nonfinite, and nonnormalized matrices fail with a concise actionable message.
- [ ] A BSC with crossover probability 0.1 reports approximately 0.531004 bits per channel use within a documented numerical tolerance.
- [ ] A deliberately small iteration limit produces an explicit unconverged result when its final gap exceeds the requested tolerance.
- [ ] The existing numerical validation suite still passes, and README commands reproduce a result without editing Python source.

**Evidence inspected**

- [Source 1](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/Code/ba_core.py): Re-read on November 6: blahut\_arimoto converts W to a NumPy array, unpacks W.shape, and computes distributions without explicit matrix validity checks. The repository head remains unchanged since the prior review.
- [Source 2](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/README.md): The current README still documents valid-channel assumptions, natural-log gap units, analytic examples, and the need to inspect gap when the iteration limit is reached.
- [Source 3](https://github.com/Mr-Amir-Al-Rashayda/NoteSpace/blob/93fd4608182e68168c514ea42c8d7f8510a17287/app/src/main/java/edu/birzeit/project/utils/NoteShareUtils.java): The inspected sendByEmail method formats content, optional tags, and date into an ACTION\_SENDTO mailto intent. This helper does not itself write an export file; this is not an audit of every app feature.
- [Source 4](https://github.com/Mr-Amir-Al-Rashayda/NoteSpace/blob/93fd4608182e68168c514ea42c8d7f8510a17287/README.md): The README describes Android notes, owner-scoped SQLite storage, and email sharing, with unit, lint, and instrumentation verification commands.
- [Source 5](https://github.com/Mr-Amir-Al-Rashayda/daily-code/blob/59f6efbae0d0a55981a7a475f82014bb94aa9fa0/scripts/publish_daily.py): The current inspected collector still takes the first readable top Hacker News stories and DEV programming articles without project-language or interest scoring.

**Other ideas considered**

- **NoteSpace — Add portable note export after an Android integration review:** The email-sharing helper is now verified, but an export feature still requires checking note ownership, storage integration, and the rest of the app before implementation, followed by Android verification. The numerical wrapper has a smaller confirmed scope today.
- **daily-code — Rank reading links by project languages and interests:** Fresh source inspection confirms that stories are not ranked by personal interests. This remains useful, but topic preferences and a way to assess ranking quality are still unspecified; the capacity-runner gap is better evidenced and directly testable.


## Project spotlight

### [Data-Cleaning-and-Feature-Engineering-for-the-Titanic-Dataset-](https://github.com/Mr-Amir-Al-Rashayda/Data-Cleaning-and-Feature-Engineering-for-the-Titanic-Dataset-)

Explore the source and documentation for this project.

**Stack:** Jupyter Notebook · **Stars:** 0

## One small portfolio improvement

Add a one-line description to [AVL-Tree-and-Hash-Table](https://github.com/Mr-Amir-Al-Rashayda/AVL-Tree-and-Hash-Table). Explain the problem it solves and its main technology. This is a suggestion; no changes were made to that project.

## Around the developer community

Top Hacker News stories at collection time. Community links, not endorsements.

- [Need for Speed Underground 2 online in the browser](https://nfsu2.xyz/) — 198 points · [56 comments](https://news.ycombinator.com/item?id=50403052)
- [Libghostty 1.0](https://mitchellh.com/writing/libghostty-1-0) — 790 points · [125 comments](https://news.ycombinator.com/item?id=50399933)
- [Running a law firm on Free software](https://decoded.legal/blog/2026/11/running-a-law-firm-on-free-software-2026-edition/) — 38 points · [4 comments](https://news.ycombinator.com/item?id=50403066)
- [Upload Your RAM](https://uploadyourram.org) — 190 points · [143 comments](https://news.ycombinator.com/item?id=50403214)
- [Every Mac comes with an (undocumented) family member classifier](https://8rank.ai/game/apple-intelligence-personal-knowledge-graph) — 237 points · [118 comments](https://news.ycombinator.com/item?id=50403097)

## Read & learn

Popular programming articles on DEV. Original articles stay with their authors.

- [Being, Doing, Having: Why 50 Years of Senior Craft Lives in Context, Not Code](https://dev.to/gde/being-doing-having-why-50-years-of-senior-craft-lives-in-context-not-code-29dl) · 29 min read
- [Your Code Can Be Perfect. Your Product Can Still Fail.](https://dev.to/holasoymalva/your-code-can-be-perfect-your-product-can-still-fail-gag) · 6 min read
- [Claude Code Diff Verification in 2026: How to Make Your Agent Assert Its Own Edits Did Not Break the Build](https://dev.to/jsmanifest/claude-code-diff-verification-in-2026-how-to-make-your-agent-assert-its-own-edits-did-not-break-bci) · 18 min read
- [Stop Swapping Models: Optimizing the Agent Environment Cuts 70% More Cost](https://dev.to/reidmarlow/stop-swapping-models-optimizing-the-agent-environment-cuts-70-more-cost-36cf) · 5 min read
- [Floating Versions Are an Open Door: Pin Your Actions and Dependencies](https://dev.to/gioboa/floating-versions-are-an-open-door-pin-your-actions-and-dependencies-4jlh) · 5 min read

## My public project mix

<img src="assets/languages.svg" alt="Public source repositories grouped by primary language, not code volume" width="960">

## Source freshness

| Source | Status | Last successful fetch (UTC) |
| :-- | :-- | :-- |
| github | live | 2026-11-07 14:00 UTC |
| hacker_news | live | 2026-11-07 14:00 UTC |
| dev | live | 2026-11-07 14:00 UTC |

## How it works

GitHub Actions runs daily at **07:17 UTC** (09:17 in Hebron during standard time; 10:17 during daylight time). Python collects public repository metadata, Hacker News stories, and DEV programming articles, then builds this README, accessible SVG graphics, a JSON snapshot, and a dated Markdown issue.

Updates contain real source data. An issue is generated at most once per date. Each API is fetched independently with timeouts and retries. If an API fails, its last successful snapshot is marked **cached**. If every API fails, the existing dashboard is preserved and the run fails visibly. GitHub may delay scheduled runs. The previous random commit batches have been replaced by one useful daily briefing.

### Run it yourself

```sh
python3 scripts/publish_daily.py
python3 -m unittest discover -s tests -v
```

Python 3.10+ and an IANA timezone database are required (included on GitHub's Ubuntu runner). Windows users may need `pip install tzdata`. No paid APIs or external API keys are required. The workflow uses its built-in token only for GitHub requests and pushing to this repository.

### Local AI planner

Local Codex reviews real project documentation and code, compares three possible tasks, and publishes one evidence-backed recommendation with an implementation outline and acceptance checks. It reads the planning journal before deciding, so an unfinished useful task can be carried forward instead of inventing a new one every day. Proposals are dated and never presented as completed work.

The AI review runs daily at **23:00 Asia/Hebron (11 PM)** through a local Codex scheduled task. **This computer must be awake and Codex running.** It uses the existing Codex session, with no separate model API key. The GitHub-hosted daily brief continues independently. If the local planner misses a run, the last proposal keeps its original review date. See [PLANNER.md](PLANNER.md) for the procedure and publication format.

**API references:** [GitHub](https://docs.github.com/en/rest/repos/repos), [Hacker News](https://github.com/HackerNews/API), [DEV / Forem](https://developers.forem.com/api).

**Controls:** Run the workflow manually from Actions; check its refresh option to rebuild today's issue after recovering an API. Disable the workflow there to stop updates. Other projects are only read; portfolio suggestions do not edit them. The original Python exercises remain in [examples/](examples/).
