<p align="center"><img src="assets/banner.svg" alt="Daily Signal — Amir Al-Rashayda" width="960"></p>

<p align="center"><strong>A living developer journal. Public APIs in, useful daily signals out.</strong></p>
<p align="center"><a href="digests/README.md">Daily issues</a> · <a href="plans/README.md">AI planning journal</a> · <a href="data/latest.json">Open data</a> · <a href="https://github.com/Mr-Amir-Al-Rashayda">My GitHub</a></p>

[Open today's full issue →](digests/2026/11/2026-11-06.md)

## AI next move

**Reviewed 2026-11-05 by local Codex · Proposed, not implemented**

### Build a safe custom-channel capacity runner

**Project:** [accelerated-blahut-arimoto](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto) · **Estimated effort:** About 2-4 hours, depending on the existing test setup

Let students and researchers supply a channel matrix and receive a reproducible capacity report instead of editing experiment source. This creates a useful foundation for a future visual Channel Lab while keeping the first change small.

**Why this next:** The current README explicitly says the solvers assume valid inputs, and inspection of both solver functions confirms they immediately unpack the matrix shape and calculate probabilities without explicit validation. A small validated command-line wrapper has a concrete user benefit and can be checked against the existing analytic examples. It is a better first step than a larger visual interface or an Android feature requiring device verification. This is a proposal based on source review; no solver tests or implementation changes were performed during this planning review.

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

- [Source 1](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/Code/ba_core.py): blahut\_arimoto converts W to a NumPy array and unpacks W.shape before computing probabilities; the inspected function has no explicit matrix validity checks.
- [Source 2](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/Code/ba_accelerated.py): accelerated\_ba follows the same direct matrix conversion and returns the final gap and iteration count, which a wrapper can use to report convergence honestly.
- [Source 3](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/README.md): The README documents the valid-channel assumptions, analytic examples, numerical test command, and distinct units for capacity and gap.
- [Source 4](https://github.com/Mr-Amir-Al-Rashayda/NoteSpace): The inspected README describes SQLite notes, tags, search, and sharing through Android email intents. It provides Android unit, lint, and instrumentation verification commands.
- [Source 5](https://github.com/Mr-Amir-Al-Rashayda/daily-code/blob/94a8871/scripts/publish_daily.py): The current daily digest reads top Hacker News stories and programming articles, without a user-interest ranking step.

**Other ideas considered**

- **NoteSpace — Investigate Markdown export for portable notes:** Potentially valuable, but the README alone does not prove export is absent. It needs a source-level review and Android verification before a concrete implementation recommendation.
- **daily-code — Rank reading links by project languages and interests:** A reasonable follow-up, but the digest was just launched and there is no feedback yet about which topics are most useful. The channel runner addresses a verified usability gap today.


## Project spotlight

### [CPU-Scheduler-Simulation](https://github.com/Mr-Amir-Al-Rashayda/CPU-Scheduler-Simulation)

Explore the source and documentation for this project.

**Stack:** Python · **Stars:** 0

## One small portfolio improvement

Add a one-line description to [Asal-Backend-Tasks](https://github.com/Mr-Amir-Al-Rashayda/Asal-Backend-Tasks). Explain the problem it solves and its main technology. This is a suggestion; no changes were made to that project.

## Around the developer community

Top Hacker News stories at collection time. Community links, not endorsements.

- [Gemini Omni 1.2 Flash](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/) — 92 points · [57 comments](https://news.ycombinator.com/item?id=50392118)
- [Dutch 'idealist' bank ASN blocks non-Google Android, including GrapheneOS](https://github.com/PrivSec-dev/banking-apps-compat-report/issues/105) — 407 points · [240 comments](https://news.ycombinator.com/item?id=50390124)
- [Blender's UI and Runtime: Much Faster Than GPUI](https://github.com/ppmpreetham/BUI) — 427 points · [178 comments](https://news.ycombinator.com/item?id=50389333)
- [Claude Code sends your email address to websites](https://github.com/anthropics/claude-code/issues/107757) — 1372 points · [433 comments](https://news.ycombinator.com/item?id=50385272)
- [sshole](https://sshhole.com) — 2827 points · [688 comments](https://news.ycombinator.com/item?id=50378228)

## Read & learn

Popular programming articles on DEV. Original articles stay with their authors.

- [An AI Testing Presentation Became the Final Push for Organizational Change at My Company](https://dev.to/xulingfeng/an-ai-testing-presentation-became-the-final-push-for-organizational-change-at-my-company-12ag) · 13 min read
- [Plan Stamping, for Software](https://dev.to/kenwalger/plan-stamping-for-software-4ein) · 7 min read
- [One Markdown File Can Hijack Your AI Coding Agent: The Hidden Cost of Blindly Trusting AGENTS.md](https://dev.to/johnnylemonny/one-markdown-file-can-hijack-your-ai-coding-agent-the-hidden-cost-of-blindly-trusting-agentsmd-167n) · 8 min read
- [Trocar de provedor não deveria ser uma dor de cabeça](https://dev.to/he4rt/trocar-de-provedor-nao-deveria-ser-uma-dor-de-cabeca-50ee) · 7 min read
- [When an AI Agent Says 'Done,' What Exactly Has Finished?](https://dev.to/suirindo/when-an-ai-agent-says-done-what-exactly-has-finished-5h3p) · 3 min read

## My public project mix

<img src="assets/languages.svg" alt="Public source repositories grouped by primary language, not code volume" width="960">

## Source freshness

| Source | Status | Last successful fetch (UTC) |
| :-- | :-- | :-- |
| github | live | 2026-11-06 15:02 UTC |
| hacker_news | live | 2026-11-06 15:02 UTC |
| dev | live | 2026-11-06 15:02 UTC |

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
