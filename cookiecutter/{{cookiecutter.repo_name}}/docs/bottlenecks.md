# Common Bottlenecks and Self-Recovery Protocols

This file documents the three most common ways learners get stuck, plus
**self-recovery protocols** that do not require external infrastructure.
Read it before you hit Week 70, because Phase 7 and Phase 8 are where the
course is most likely to break its learners.

This document is **deliberately explicit about failure modes** because the
honest version of those failure modes is what makes them survivable.

---

## Bottleneck 1 — A kid on a laptop hitting Week 84 with no GPU budget

Weeks 75, 84, 87, and 89 (`deploy_benchmark` mode) require actual GPU access.
The deliverables say "vLLM deployment", "index benchmark", "live inference
dashboard", "SGLang comparison." None of these are feasible on a CPU-only
laptop, and the course does not pretend otherwise.

The realistic hardware path in 2026:

| Tier | What it runs | Cost | Good for |
|---|---|---|---|
| Laptop / Colab Free | Tiny models (≤1B), toy benchmarks | $0 | Weeks 82–83 (theory), Week 84 with smallest models |
| Modal free credits | L4 / A10 spot, fast cold start | $0 to start; $30/mo free tier | Weeks 84, 87, 89 with 7B–13B models |
| Modal paid | L40S / A100 40GB on demand | $0.0005–$0.002 per second | Full Phase 8 deployment week |
| Lambda / RunPod | Reserved H100s, lower per-second | $1.50–$3/hr reserved | If you know you'll be doing this for a month+ |
| Owned GPU | Used RTX 3090 / 4090 (24GB) | $800–$1,500 one-time | Long horizon, no cloud surprises |

### Modal is the default redirect

[Modal](https://modal.com) is the cheapest *and* fastest path for a learner
without a GPU. The free tier gives $30 in credits per month, which is enough
to run every Phase 8 deliverable on a 7B–13B model.

Setup takes ~10 minutes:

```bash
pip install modal
modal token new                         # paste API key from modal.com
modal run --detach --gpu a10 hello.py    # 12-second cold start on A10
```

The CLI has a built-in `--detach` flag so jobs survive terminal close, and
the per-second billing means a 4-hour benchmark costs ~$1.40 on an A10.

A complete `vLLM` deployment on Modal for Week 84:

```python
import modal

stub = modal.Stub("vllm-week-84")
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm>=0.6", "torch>=2.3")
)

@stub.function(image=image, gpu="a10", timeout=600)
def serve():
    from vllm import LLM, SamplingParams
    llm = LLM(model="meta-llama/Llama-3.1-8B-Instruct")
    out = llm.generate(["hello"], SamplingParams(max_tokens=20))
    print(out[0].outputs[0].text)
```

Run it: `modal run --detach vllm_week_84.py`. The exit code and logs land
in your terminal; the A10 cost is billed by the second.

### What if you actually cannot afford a GPU?

Some learners cannot afford even Modal credits. The honest protocol:

1. **Run Weeks 82–83, 85–86, 88, 90–93 in `read_diagram` mode.** Those weeks
   do not need a GPU. The deliverables are notes, schemas, methodology docs,
   comparison tables. Do them well.
2. **Skip Weeks 75, 84, 87, 89.** Don't burn hours failing. Document the
   skip in your journal (`evidence/weeks/week_NNN/README.md` — "skipped
   due to GPU budget; will revisit on first commodity access") and use the
   Recovery Week after Week 94 (the 94 recovery window is one of the
   planned ones) to backfill if you find a resource.
3. **Watch instead of run.** Many platforms publish recorded GPU benchmarks.
   Lmsys, vLLM Office Hours, and Modal's blog have honest numbers. Reading
   the numbers and writing down *why* they look the way they do is the same
   intellectual work as running the benchmark, with $0 hardware cost.

The course does not gate graduation on Phase 8 having been run on a GPU.
The **Gate 8** requirement is "Deployed vLLM or SGLang, benchmark
methodology, observability dashboard, quantization report, speculative
decoding report, inference cost model." A documented "I cannot afford the
GPU; here is the methodology I would use, here are public numbers I
interpreted" is a passing gate evidence with the right framing.

---

## Bottleneck 2 — Someone burning 25 hours on Week 74

Week 74 says "training architecture map" for DDP / FSDP / tensor / pipeline
parallelism / ZeRO. The deliverable is **a diagram and a written plan**, not
an implementation. There is no `repo/training_cluster/` to build.

A learner who interprets "training architecture map" as "implement FSDP on
a 70B model cluster" burns 25+ hours and burns weeks 75–76 in the process.
This is the most common pacing failure in Phase 7.

### What the deliverable actually wants

The Week 74 deliverable is **a 2-4 page document** with:

1. A diagram of how the four parallelism dimensions (data, tensor, pipeline,
   ZeRO optimizer state) decompose across N GPUs.
2. A decision rule: "for a 7B model on 8 A100s, do X. For a 70B model on
   64 H100s, do Y."
3. Citations to the canonical papers (DeepSpeed ZeRO, Megatron-LM, FSDP
   paper, GPipe).
4. A latency estimate using the roofline model from Week 83.

This is exactly the kind of artifact that fits in `read_diagram` mode and
keeps the weekly budget. The Misra-Gries and Space-Saving sketches from
Week 42 are similar — the point is to **explain the system**, not to
rebuild it.

### The pattern

Several Phase 7 and Phase 8 weeks follow this template:

| Week | Deliverable | Looks like | Is actually |
|---|---|---|---|
| 71 | LLM data pipelines / dataset card | "Crawl + clean + dedup a corpus" | A 1-page dataset card describing sources, filters, dedup policy |
| 72 | Fine-tuning plan | "Run LoRA on Llama 3" | A 4-page plan with hyperparams, eval, and rollback criteria |
| 73 | Alignment / preference eval plan | "Implement DPO from scratch" | An evaluation plan comparing SFT vs DPO vs PPO outputs |
| 74 | Distributed training architecture map | "Run FSDP on 70B" | A 2-4 page architecture document with diagrams |
| 91 | Quality/throughput table | "Benchmark AWQ vs GPTQ" | A 2-column table comparing 3-4 configurations from public data |
| 92 | Speculative / latency lab | "Build Medusa head" | Notes on Medusa/EAGLE/StreamingLLM trade-offs with worked examples |
| 93 | Disaggregated serving plan | "Deploy DistServe" | A 6-page plan covering prefill/decode split, KV transfer, autoscaling |

When the week says "X plan" or "Y comparison", the deliverable is the
document. When the week says "X implementation" or "Y service", you should
expect 100-200 lines of code.

### Self-recovery

If you find yourself 15+ hours into a `read_diagram` week and you're
writing code, stop. Use a recovery week to catch up, and write the document
before you write the code. The course still rewards the document — it's
evidence, it's public, and it's reviewable in interviews.

If you're 8+ hours into an `implement` week and you don't have a working
artifact, you have probably mis-scoped the deliverable. Trim until you
have something that runs, then iterate.

---

## Bottleneck 3 — Self-graded gates that feel like suggestions

The 10 milestone gates (Weeks 6, 18, 30, 45, 57, 69, 81, 93, 102, 108)
are checked by `make gate`. That command looks at file paths. There is no
human reviewer, no mentor, no graded rubric. If the file exists, the gate
passes.

This is the acknowledged ceiling of a solo-authored open-source
curriculum. It is not the same as having a teacher, and pretending
otherwise would be dishonest.

### What self-graded gates are actually good for

- **Process enforcement.** Forces the learner to *finish the evidence
  trail* before moving forward. Many learners skip writing the design
  doc or the retrospective if there is no external pressure.
- **Defensive structure.** Without a gate, a learner in Week 60 with
  missing evidence in Week 30 will pretend the missing evidence is
  "done." The gate forces them to either remediate or skip with eyes
  open.
- **Self-discipline.** The gate is a yardstick *for you*, not a teacher.
  Use it to benchmark yourself against the standards you want to defend
  in interviews.

### What they are not good for

- **Catching factually wrong work.** A gate that checks "does the file
  exist" does not check "is the math right." Wrong proofs ship just as
  easily as right ones.
- **Calibrating against the field.** You do not know if your Week 57
  design doc is actually Staff-level or if it's a Senior's first draft.
- **Replacing mentorship.** "I passed my own gate" is not a credential.

### Self-recovery

Replace the missing external review with the strongest internal review you
can approximate:

1. **Public commit history.** When you finish a deliverable, push it.
   The future-you reviewer is more honest than the present-you one.
2. **The learning partner as reviewer.** Use `make review` after every
   week's gate-check. The OpenRouter-backed partner is at least an
   external perspective, and the AGENTS.md system prompt explicitly
   tells it not to be a cheerleader.
3. **The Darbar weekly minimum.** One coding drill a week, even if it's
   easy. It forces you to maintain the pattern of "check my work against
   a measurable signal." It's the closest the course has to a continuous
   assessment.
4. **The behavioral story bank.** Maintain a CARL-format story file
   throughout (`docs/behavioral_stories.md`, suggested format). When you
   need to defend a design decision in an interview, you reach for that
   story. The gate that forces you to keep the bank up to date is more
   useful than the gate that checks a single file.

If you want a real external review, the honest options today are:

- A peer reading group (Discord, Matrix, similar — the course does not
  ship one because it is not resourced to maintain it)
- Posting your week's deliverable to the appropriate subreddit
  (r/MachineLearning for the LLM/inference weeks, r/ExperimentationDev
  for ML lifecycle weeks) and asking for feedback
- Paying for a code review from a freelancer (~$50/hr on Toptal/Upwork
  for someone who has actually shipped inference work)

These are *options*, not requirements. The course does not gate on them.

---

## The three self-recovery protocols

When you hit any of the above bottlenecks (or one not listed here),
follow this protocol before doing anything else:

### Step 1: Stop and write the blocker

Open `journal/weeks/week_NNN.md` and the corresponding
`evidence/weeks/week_NNN/README.md`. Write down in one paragraph what is
blocked, why, and what you have already tried. The act of writing the
blocker usually surfaces the solution.

### Step 2: Match the week to its mode

Look at the Mode column in the curriculum table (parent README) for this
week. Ask the question:

- **`implement`:** does my code run? If no, can I trim the scope to
  make it run? If still no, is the scope too big for the budget?
- **`read_diagram`:** do I have a written deliverable? If no, am I
  writing code instead? Stop coding, start writing.
- **`deploy_benchmark`:** do I have GPU access? If no, see Bottleneck 1
  redirect to Modal or to the `read_diagram` fallback.

### Step 3: Use a recovery week instead of grinding

Recovery weeks are planned buffer periods after Weeks 6, 14, 22, 30, 38,
46, 54, 62, 70, 78, 86, 94, and 102. They are not additional curriculum.
They are explicit "slow down here" weeks. If you hit a bottleneck in
Week 71, you have a planned recovery in Week 78 to deal with it.

If you finish a delivery week without needing a recovery, **use the
recovery week anyway** for retrospective polish. That is what they are
for. The course explicitly does not punish using them.

### Step 4: Adjust the plan, not the budget

If the budget is genuinely insufficient (e.g., Week 74 turned into a 25
hour nightmare), the answer is not "work 30 hours next week to catch up."
The answer is "use a recovery week and reduce optional depth for the
following two weeks." Stretching weeks past their budget is what kills
the next four weeks; using the recovery system is what protects them.

---

## When to quit vs. when to push through

The course is honest about its three stackable exit points (30, 69, 108).
It is also honest about the fact that not everyone finishes.

**Push through** when:

- You have finished at least the prior week's evidence
- The blocker is a skill gap, not a budget gap
- You have at least two full weeks of runway left before the gate
- The week's mode is `implement` and you have working code at 70%

**Switch to a recovery week** when:

- You have missed two consecutive weeks of core evidence
- The blocker is a hardware/resource gap (no GPU, no money)
- The week's mode is `read_diagram` and you don't have a written
  deliverable
- You have burned 2x the weekly budget on the current week

**Stop at the next exit point** when:

- You have not started the current phase (no journal entries for the
  last 6 weeks)
- You have missed a gate twice and still don't have remediation
- Life happened (job change, family, health) and the 10-15 hour budget
  is genuinely unavailable

The exits are not failure modes. They are release checkpoints. Stopping
at Week 30 with a defensible Foundations release is more valuable than
burning out at Week 72 with no release evidence.

---

*Bottlenecks are bottlenecks because they cluster in time and surprise
learners who weren't warned. This appendix is the warning. The
self-recovery protocols above are the course's contract with you: the
structure will catch you when you stumble, but only if you use it.*
