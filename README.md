<p align="center"><img src="assets/banner.svg" alt="Daily Signal — Amir Al-Rashayda" width="960"></p>

<p align="center"><strong>A living developer journal. Public APIs in, useful daily signals out.</strong></p>
<p align="center"><a href="digests/README.md">Daily issues</a> · <a href="plans/README.md">AI planning journal</a> · <a href="data/latest.json">Open data</a> · <a href="https://github.com/Mr-Amir-Al-Rashayda">My GitHub</a></p>

[Open today's full issue →](digests/2026/11/2026-11-25.md)

## AI next move

**Reviewed 2026-11-26 by local Codex · Proposed, not implemented**

### Make the backup transport send bytes, with a real socket test

**Project:** [cloud-backup-system](https://github.com/Mr-Amir-Al-Rashayda/cloud-backup-system) · **Estimated effort:** About 2-3 hours on Linux or WSL, including focused socket tests

Turn one foundational networking stub into a working, verifiable transport primitive. A reliable send-all function is reusable by both file transfers and protocol headers, and gives the backup project an honest first end-to-end byte-transfer demonstration.

**Why this next:** Fresh November 26 inspection compared current READMEs and relevant code in three eligible projects. Their heads remain unchanged: backup adf40a00b1c806972c8dbd28acc7284f3ba19749, channel solver 7de3a92172110be2615dc561abd009f13610f7de and scheduler e2f991f07db966acf75ec861efc617d0478a7327. The backup send-all function still ignores all arguments and returns success; its test still only initializes the receive buffer. Existing planning packets do not establish implementation or completion. Retain the bounded socket-tested send-all task rather than moving to its dependent formatted-line helper or forcing novelty. The channel CLI and scheduler CLI still offer useful usability improvements at similar estimated effort, but verified byte transmission is the more foundational prerequisite. The backup README explicitly labels skeletons and stubs, so this is not a newly alleged production regression. No C, numerical or scheduler suites ran in this source review. The API digest remains dated November 25; its collection timestamp is preserved.

*Carried forward after reviewing the previous recommendation.*

**Implementation outline**

1. Implement only network\_send\_all against its existing header contract: advance through short writes, retry interrupted sends, and return an error on actual failure or a zero-progress send instead of looping forever or reporting success.
2. Define and document edge cases for zero-length input and invalid arguments. Choose a platform-appropriate SIGPIPE policy so sending to a disconnected peer returns an error instead of unexpectedly terminating the process; retain the project's stated Linux/macOS portability where supported.
3. Extend test\_network with an actual socketpair transfer and an independent receiver, comparing an exact binary payload including zero bytes. Drain large payloads concurrently so the test cannot deadlock on socket-buffer capacity.
4. Add focused short-write and EINTR coverage through a controlled test seam or equivalent deterministic technique, plus disconnected-peer and zero-length cases. Run the existing make test and CI workflow and document that other networking functions remain stubs.

**Acceptance checks**

- [ ] A local socketpair receiver obtains the exact payload and byte count for both a small binary buffer and a payload larger than normal socket-buffer capacity.
- [ ] Deterministic short writes and interrupted calls complete correctly without dropped or duplicated bytes; zero-progress and permanent errors terminate with the documented error result.
- [ ] A disconnected peer does not produce a false success or unexpected SIGPIPE process termination, and the zero-length case behaves as documented.
- [ ] Existing project tests still pass, the new transport tests actually exercise network\_send\_all, and documentation does not claim the remaining listener, receive, or connection stubs are complete.

**Evidence inspected**

- [Source 1](https://github.com/Mr-Amir-Al-Rashayda/cloud-backup-system/blob/adf40a00b1c806972c8dbd28acc7284f3ba19749/src/common/network.c): Read November 26 at unchanged backup head: network\_send\_all discards sockfd, data and count and returns zero unconditionally; network\_send\_line and other transport helpers also remain explicit stubs.
- [Source 2](https://github.com/Mr-Amir-Al-Rashayda/cloud-backup-system/blob/adf40a00b1c806972c8dbd28acc7284f3ba19749/tests/test_network.c): Read November 26: the network test initializes recv\_buf\_t and checks zero len/start. It does not open sockets or invoke network\_send\_all.
- [Source 3](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/Code/ba_core.py): Read November 26 at unchanged solver head: blahut\_arimoto converts W, unpacks W.shape and starts probability calculations without explicit channel-matrix validation.
- [Source 4](https://github.com/Mr-Amir-Al-Rashayda/CPU-Scheduler-Simulation/blob/e2f991f07db966acf75ec861efc617d0478a7327/OS_Amir.py): Read November 26 at unchanged scheduler head: main hardcodes Processes.txt and a quantum of 10, prints metrics, then unconditionally calls generate\_gantt\_chart.
- [Source 5](https://github.com/Mr-Amir-Al-Rashayda/CPU-Scheduler-Simulation/blob/e2f991f07db966acf75ec861efc617d0478a7327/README.md): Read November 26: the README describes a file-driven interactive scheduler workflow with console metrics and a Matplotlib Gantt window.
- [Source 6](https://github.com/Mr-Amir-Al-Rashayda/cloud-backup-system/blob/adf40a00b1c806972c8dbd28acc7284f3ba19749/README.md): Read November 26: the README explicitly labels src as implementation skeletons and stubs and documents reliable framing, make all and make test as part of the coursework project.
- [Source 7](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/README.md): Read November 26: the README explicitly says the supplied solvers assume valid matrices, documents natural-log gap units, and warns that reaching the iteration limit does not ensure convergence.

**Other ideas considered**

- **accelerated-blahut-arimoto — Build the previously proposed validated custom-channel runner:** A validated custom-channel runner would help students supply safe inputs, at an estimated 2-4 hours. Current README and ba\_core.py provide strong evidence, but this repeats an existing unimplemented usability proposal; making the backup transport actually send bytes offers a more foundational functional gain with a precise receiver-based check.
- **CPU-Scheduler-Simulation — Add configurable input and a headless metrics mode:** A configurable headless scheduler would improve repeatable classroom runs, at an estimated 2-4 hours plus metrics verification. Current main and README confirm fixed input and interactive plotting. Its usability benefit is credible, but transport behavior has a narrower directly observable acceptance boundary and remains an unmet prerequisite.


## Project spotlight

### [Course-Prerequisite-Planner-and-Campus-Route-Finder](https://github.com/Mr-Amir-Al-Rashayda/Course-Prerequisite-Planner-and-Campus-Route-Finder)

Explore the source and documentation for this project.

**Stack:** C · **Stars:** 0

## One small portfolio improvement

Add a one-line description to [Parallel-Word-Frequency-Analysis](https://github.com/Mr-Amir-Al-Rashayda/Parallel-Word-Frequency-Analysis). Explain the problem it solves and its main technology. This is a suggestion; no changes were made to that project.

## Around the developer community

Top Hacker News stories at collection time. Community links, not endorsements.

- [A few questions for the guy who went snorkeling in a Home Depot retention pond](https://www.vox.com/down-to-earth/511999/home-depot-retention-pond-snorkel-joseph-ricketts) — 257 points · [73 comments](https://news.ycombinator.com/item?id=50643129)
- [Investigating degraded experiences across GitHub products](https://www.githubstatus.com/incidents/qn8mfv6q5hlx) — 126 points · [62 comments](https://news.ycombinator.com/item?id=50643720)
- [Google releases Cogentic papers on integer factorization, discrete logs and more](https://github.com/google-research/google-research/tree/master/cogentic_research_papers) — 289 points · [230 comments](https://news.ycombinator.com/item?id=50642086)
- [Windows Loudness Equalization, reverse-engineered and ported to PipeWire](https://github.com/xoxorwr/pw-loudness-eq) — 244 points · [138 comments](https://news.ycombinator.com/item?id=50641171)
- [Predicting LoRA size for any dataset](https://engram.com/blog/lora-size) — 44 points · [1 comments](https://news.ycombinator.com/item?id=50635783)

## Read & learn

Popular programming articles on DEV. Original articles stay with their authors.

- [The Third Cup: You Don't Have to Fly That High](https://dev.to/thethirdcup/the-third-cup-you-dont-have-to-fly-that-high-3ehd) · 10 min read
- [Part 7: What Reading the Code Could Never Find](https://dev.to/ndcodes/part-7-what-reading-the-code-could-never-find-8c1) · 12 min read
- [How to Auto-Approve Pull Requests Safely: Testing It on a Real Repo](https://dev.to/anthonymax/how-to-auto-approve-pull-requests-safely-testing-it-on-a-real-repo-3do) · 8 min read
- [10 Rejections. No LinkedIn Premium. 1 Offer. Here's how 👇](https://dev.to/taqui/10-rejections-no-linkedin-premium-1-offer-heres-how-49mh) · 7 min read
- [My AI memory marked 471 notes as verified. Nothing had verified them.](https://dev.to/heinrichneb/my-ai-memory-marked-471-notes-as-verified-nothing-had-verified-them-3m87) · 6 min read

## My public project mix

<img src="assets/languages.svg" alt="Public source repositories grouped by primary language, not code volume" width="960">

## Source freshness

| Source | Status | Last successful fetch (UTC) |
| :-- | :-- | :-- |
| github | live | 2026-11-25 17:57 UTC |
| hacker_news | live | 2026-11-25 17:57 UTC |
| dev | live | 2026-11-25 17:57 UTC |

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
