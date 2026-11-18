<p align="center"><img src="assets/banner.svg" alt="Daily Signal — Amir Al-Rashayda" width="960"></p>

<p align="center"><strong>A living developer journal. Public APIs in, useful daily signals out.</strong></p>
<p align="center"><a href="digests/README.md">Daily issues</a> · <a href="plans/README.md">AI planning journal</a> · <a href="data/latest.json">Open data</a> · <a href="https://github.com/Mr-Amir-Al-Rashayda">My GitHub</a></p>

[Open today's full issue →](digests/2026/11/2026-11-18.md)

## AI next move

**Reviewed 2026-11-19 by local Codex · Proposed, not implemented**

### Make the backup transport send bytes, with a real socket test

**Project:** [cloud-backup-system](https://github.com/Mr-Amir-Al-Rashayda/cloud-backup-system) · **Estimated effort:** About 2-3 hours on Linux or WSL, including focused socket tests

Turn one foundational networking stub into a working, verifiable transport primitive. A reliable send-all function is reusable by both file transfers and protocol headers, and gives the backup project an honest first end-to-end byte-transfer demonstration.

**Why this next:** Reviewed November 19 in Asia/Hebron after the November 18 22:06 UTC trigger. Fresh READMEs and source inspection confirm all three candidate heads are unchanged. The backup network\_send\_all still discards its arguments and returns success; its test checks only buffer initialization. This is an explicitly documented coursework stub, not a newly claimed production regression. Earlier send-all, failure-testing and formatted-line proposals are not evidence of completed implementation. A real, verified byte-transfer primitive remains the prerequisite with the strongest immediate functional value and a bounded contract. The validated channel runner and a headless scheduler CLI remain useful alternatives at similar effort, but neither unblocks backup transport. No numerical, scheduler or C project suites were run during this source review. The public API snapshot remains dated November 18; this review does not relabel its collection time.

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

- [Source 1](https://github.com/Mr-Amir-Al-Rashayda/cloud-backup-system/blob/adf40a00b1c806972c8dbd28acc7284f3ba19749/src/common/network.c): Read November 19 at unchanged backup head: network\_send\_all discards sockfd, data and count and returns zero unconditionally; network\_send\_line and other transport helpers also remain explicit stubs.
- [Source 2](https://github.com/Mr-Amir-Al-Rashayda/cloud-backup-system/blob/adf40a00b1c806972c8dbd28acc7284f3ba19749/tests/test_network.c): Read November 19: the network test initializes recv\_buf\_t and checks zero len/start. It does not open sockets or invoke network\_send\_all.
- [Source 3](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/Code/ba_core.py): Read November 19 at unchanged solver head: blahut\_arimoto converts W, unpacks W.shape and starts probability calculations without explicit channel-matrix validation.
- [Source 4](https://github.com/Mr-Amir-Al-Rashayda/CPU-Scheduler-Simulation/blob/e2f991f07db966acf75ec861efc617d0478a7327/OS_Amir.py): Read November 19 at unchanged scheduler head: main hardcodes Processes.txt and a quantum of 10, prints metrics, then unconditionally calls generate\_gantt\_chart.
- [Source 5](https://github.com/Mr-Amir-Al-Rashayda/CPU-Scheduler-Simulation/blob/e2f991f07db966acf75ec861efc617d0478a7327/README.md): Read November 19: the README describes a file-driven interactive scheduler workflow with console metrics and a Matplotlib Gantt window.
- [Source 6](https://github.com/Mr-Amir-Al-Rashayda/cloud-backup-system/blob/adf40a00b1c806972c8dbd28acc7284f3ba19749/README.md): Read November 19: the README explicitly labels src as implementation skeletons and stubs and documents reliable framing, make all and make test as part of the coursework project.
- [Source 7](https://github.com/Mr-Amir-Al-Rashayda/accelerated-blahut-arimoto/blob/7de3a92172110be2615dc561abd009f13610f7de/README.md): Read November 19: the README explicitly says the supplied solvers assume valid matrices, documents natural-log gap units, and warns that reaching the iteration limit does not ensure convergence.

**Other ideas considered**

- **accelerated-blahut-arimoto — Build the previously proposed validated custom-channel runner:** A validated custom-channel runner would help students supply safe inputs, at an estimated 2-4 hours. Current README and ba\_core.py provide strong evidence, but this repeats an existing unimplemented usability proposal; making the backup transport actually send bytes offers a more foundational functional gain with a precise receiver-based check.
- **CPU-Scheduler-Simulation — Add configurable input and a headless metrics mode:** A configurable headless scheduler would improve repeatable classroom runs, at an estimated 2-4 hours plus metrics verification. Current main and README confirm fixed input and interactive plotting. Its usability benefit is credible, but transport behavior has a narrower directly observable acceptance boundary and remains an unmet prerequisite.


## Project spotlight

### [Shell-Medical-Test-Management-System](https://github.com/Mr-Amir-Al-Rashayda/Shell-Medical-Test-Management-System)

Shell-based coursework for storing, searching and managing laboratory test records from the command line.

**Stack:** Shell · **Stars:** 0

## One small portfolio improvement

Add a one-line description to [CPU-Scheduler-Simulation](https://github.com/Mr-Amir-Al-Rashayda/CPU-Scheduler-Simulation). Explain the problem it solves and its main technology. This is a suggestion; no changes were made to that project.

## Around the developer community

Top Hacker News stories at collection time. Community links, not endorsements.

- [Pre-auth RCE in Nginx HTTP/2 handling](https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities) — 135 points · [37 comments](https://news.ycombinator.com/item?id=50547374)
- [Quad9 Is Leaving France: Why DNS Resolvers Are the Wrong Place to Fight Piracy](https://techstackups.com/articles/quad9-leaves-france-dns-blocking/) — 292 points · [78 comments](https://news.ycombinator.com/item?id=50545958)
- [Deutsche Bank](https://www.inside-db.com/) — 71 points · [18 comments](https://news.ycombinator.com/item?id=50547620)
- ['Human' Is Cambridge Dictionary's Word of the Year 2026](https://www.cam.ac.uk/news/cambridge-dictionary-reveals-word-of-the-year-2026) — 85 points · [62 comments](https://news.ycombinator.com/item?id=50546914)
- [U.S. AirForce is looking for old storage Media (CF or PC cards)](https://sam.gov/workspace/contract/opp/8948e8601e964c6aba9c801eee16b1be/view) — 34 points · [8 comments](https://news.ycombinator.com/item?id=50547583)

## Read & learn

Popular programming articles on DEV. Original articles stay with their authors.

- [Is Coding with AI Actually Faster and Cheaper?](https://dev.to/sylwia-lask/is-coding-with-ai-actually-faster-and-cheaper-2810) · 6 min read
- [Rust Doesn't Have a Garbage Collector. It Has Something Stranger.](https://dev.to/smtahosin/rust-doesnt-have-a-garbage-collector-it-has-something-stranger-2oan) · 7 min read
- [Part 6: The Walkthrough That Only Worked on My Machine](https://dev.to/ndcodes/part-6-the-walkthrough-that-only-worked-on-my-machine-15e8) · 12 min read
- [What would you add to the list?](https://dev.to/canro91/what-would-you-add-to-the-list-3fbh) · 1 min read
- [How is AI making your life easier?](https://dev.to/rasheedmozaffar/how-is-ai-making-your-life-easier-2mcg) · 3 min read

## My public project mix

<img src="assets/languages.svg" alt="Public source repositories grouped by primary language, not code volume" width="960">

## Source freshness

| Source | Status | Last successful fetch (UTC) |
| :-- | :-- | :-- |
| github | live | 2026-11-18 16:26 UTC |
| hacker_news | live | 2026-11-18 16:26 UTC |
| dev | live | 2026-11-18 16:26 UTC |

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
