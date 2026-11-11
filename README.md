<p align="center"><img src="assets/banner.svg" alt="Daily Signal — Amir Al-Rashayda" width="960"></p>

<p align="center"><strong>A living developer journal. Public APIs in, useful daily signals out.</strong></p>
<p align="center"><a href="digests/README.md">Daily issues</a> · <a href="plans/README.md">AI planning journal</a> · <a href="data/latest.json">Open data</a> · <a href="https://github.com/Mr-Amir-Al-Rashayda">My GitHub</a></p>

[Open today's full issue →](digests/2026/11/2026-11-11.md)

## AI next move

**Reviewed 2026-11-09 by local Codex · Proposed, not implemented**

### Build a safe custom-channel capacity runner

**Project:** [accelerated-blahut-arimoto](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto) · **Estimated effort:** About 2-4 hours, depending on the existing test setup

Let students and researchers supply a channel matrix and receive a reproducible capacity report instead of editing experiment source. This creates a useful foundation for a future visual Channel Lab while keeping the first change small.

**Why this next:** Carried forward after reviewing the three recent proposals and rechecking three candidate projects on November 9. The channel-capacity repository remains at 7de3a92172110be2615dc561abd009f13610f7de; its README still states that inputs are assumed valid, and the current ba\_core.py still converts and unpacks W before any explicit validation. The documented entry points and inspected solver do not show the proposed custom-matrix runner. NoteSpace remains at its previous revision, with the inspected sharing helper constructing email intents; portable export needs wider Android review and device verification. Daily Signal still collects unranked community links, and there is no new evidence of topic preferences or ranking quality. The validated runner remains the most useful small, testable next step. No implementation or completion is inferred from the earlier proposals; source inspection, not solver or Android test execution, supports this decision.

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

- [Source 1](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/Code/ba_core.py): Re-read on November 9 at the unchanged project head: blahut\_arimoto converts W, unpacks W.shape, and computes probability distributions without explicit matrix validity checks.
- [Source 2](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/README.md): Current README rechecked on November 9: valid channel matrices are an assumption, gap tolerance is in nats, and reaching the iteration limit requires checking the final gap. The documented examples use Python source entry points.
- [Source 3](https://github.com/Mr-Amir-Al-Rashayda/NoteSpace/blob/93fd4608182e68168c514ea42c8d7f8510a17287/app/src/main/java/edu/birzeit/project/utils/NoteShareUtils.java): Re-read on November 9 at unchanged NoteSpace revision 93fd4608182e68168c514ea42c8d7f8510a17287: sendByEmail creates an ACTION\_SENDTO mailto intent with formatted note text. This helper alone does not establish whether another app path implements file export.
- [Source 4](https://github.com/Mr-Amir-Al-Rashayda/NoteSpace/blob/93fd4608182e68168c514ea42c8d7f8510a17287/README.md): The README describes Android notes, owner-scoped SQLite storage, and email sharing, with unit, lint, and instrumentation verification commands.
- [Source 5](https://github.com/Mr-Amir-Al-Rashayda/daily-code/blob/69d665c226c27c17c11f5cda09282f0be586bfb1/scripts/publish_daily.py): Current source rechecked on November 9: Hacker News uses the first five readable top stories and DEV uses programming-tag articles; neither collector applies personal-interest or project-language relevance scoring.

**Other ideas considered**

- **NoteSpace — Add portable note export after an Android integration review:** The email-sharing helper is now verified, but an export feature still requires checking note ownership, storage integration, and the rest of the app before implementation, followed by Android verification. The numerical wrapper has a smaller confirmed scope today.
- **daily-code — Rank reading links by project languages and interests:** Fresh source inspection confirms that stories are not ranked by personal interests. This remains useful, but topic preferences and a way to assess ranking quality are still unspecified; the capacity-runner gap is better evidenced and directly testable.


## Project spotlight

### [Medical-Test-Management-System](https://github.com/Mr-Amir-Al-Rashayda/Medical-Test-Management-System)

Explore the source and documentation for this project.

**Stack:** Python · **Stars:** 0

## One small portfolio improvement

Add a one-line description to [Data-Cleaning-and-Feature-Engineering-for-the-Titanic-Dataset-](https://github.com/Mr-Amir-Al-Rashayda/Data-Cleaning-and-Feature-Engineering-for-the-Titanic-Dataset-). Explain the problem it solves and its main technology. This is a suggestion; no changes were made to that project.

## Around the developer community

Top Hacker News stories at collection time. Community links, not endorsements.

- [Google SWE points 48 AI agents at NASA Lidar, finds unmapped Maya pyramid in 72h](https://pietromiotti.com/latest/maya-site/?maya) — 442 points · [159 comments](https://news.ycombinator.com/item?id=50452455)
- [Can a Linear Program Do Weight-Space Programming?](https://nathan.rs/posts/weight-space-lp/) — 98 points · [15 comments](https://news.ycombinator.com/item?id=50452655)
- [Pharo in the Browser with WebAssembly](https://massimo-nocentini.github.io/pharo-vm/world.html) — 26 points · [5 comments](https://news.ycombinator.com/item?id=50453763)
- [Atuin Threads: All your agent sessions on every machine](https://blog.atuin.sh/threads-agent-sessions/) — 17 points · [10 comments](https://news.ycombinator.com/item?id=50453637)
- [Using voltage glitching to unleash the A100 in my mining card](https://blog.kate.land/posts/using-voltage-glitching-to-unlock-the-a100/) — 104 points · [43 comments](https://news.ycombinator.com/item?id=50451903)

## Read & learn

Popular programming articles on DEV. Original articles stay with their authors.

- [We Keep Hearing About AI Productivity. The QA Group Chat Told a Different Story.](https://dev.to/xulingfeng/we-keep-hearing-about-ai-productivity-the-qa-group-chat-told-a-different-story-2nma) · 12 min read
- [AI can write code, but the magic of a first project is unmatched! 🗽](https://dev.to/necoz/ai-can-write-code-but-the-magic-of-a-first-project-is-unmatched-30c4) · 1 min read
- [You're Spawning Goroutines Wrong: The Visual Architecture Guide That Fixes Go Concurrency Forever](https://dev.to/smtahosin/youre-spawning-goroutines-wrong-the-visual-architecture-guide-that-fixes-go-concurrency-forever-1he0) · 12 min read
- [Part 5: The Control That Protected an Empty Bucket](https://dev.to/ndcodes/part-5-the-control-that-protected-an-empty-bucket-e1j) · 12 min read
- [DuckDB 2.0's quack server lets ten writers share one file for under 2ms a query](https://dev.to/alexgeorgiev17/duckdb-20s-quack-server-lets-ten-writers-share-one-file-for-under-2ms-a-query-1ged) · 7 min read

## My public project mix

<img src="assets/languages.svg" alt="Public source repositories grouped by primary language, not code volume" width="960">

## Source freshness

| Source | Status | Last successful fetch (UTC) |
| :-- | :-- | :-- |
| github | live | 2026-11-11 15:10 UTC |
| hacker_news | live | 2026-11-11 15:10 UTC |
| dev | live | 2026-11-11 15:10 UTC |

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
