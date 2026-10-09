"""One command for SimGate: write a brief, plan it, queue it, watch it.

    research/simgate serve              # the web app, http://localhost:8765
    research/simgate worker             # runs queued studies, two at a time
    research/simgate new my_question    # a brief to fill in
    research/simgate plan my_question   # Claude plans it; code checks the plan
    research/simgate queue my_question --proposer rules hybrid llm
    research/simgate status             # studies, arms and jobs
    research/simgate doctor             # is this machine ready?

A brief is named by its path under research/briefs, without .md
(categories/lead_vehicle). The worker and the web app share research/jobs/;
nothing here starts a simulation except the worker.
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import jobs
import web
from read_state import ROOT


def status(ids: bool = False) -> None:
    state = web.state()
    gpu = state["gpu"]
    if gpu:
        print(
            f"GPU {gpu['name']}: {gpu['used_mib']}/{gpu['total_mib']} MiB, {gpu['util']}%"
        )
    print(
        f"simulations running {state['simulations']}/{state['slots']}; "
        f"worker {'on' if state['worker'] else 'off'}"
        + ("; a run_pool script is dispatching" if state["pool"] else "")
    )
    for study in state["studies"]:
        print(
            f"\n{study['name']}  ({study['budget']} runs, goal {study['goal']['type']})"
        )
        for proposer, arm in study["arms"].items():
            if "error" in arm:
                print(f"  {proposer:8} {arm['error']}")
                continue
            print(
                f"  {proposer:8} kept {arm['kept']:>3}  failures {arm['failures']:>3}  "
                f"goal at {arm['runs_to_goal'] or '-':>4}  hardest {arm['hardest']}"
                + ("  running" if arm["running"] else "")
            )
    pending = [j for j in state["jobs"] if j["state"] in ("queued", "running")]
    if pending:
        print("\njobs")
        for job in pending:
            print(
                f"  {job['state']:8} {job['kind']:5} {job['brief']} ({job['proposer']})"
            )


def main() -> int:
    parser = argparse.ArgumentParser(prog="simgate", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    serve = sub.add_parser("serve", help="the web app")
    serve.add_argument("--port", type=int, default=8765)
    sub.add_parser("worker", help="run queued studies as GPU slots free up")
    new = sub.add_parser("new", help="write a brief to fill in")
    new.add_argument("name")
    plan = sub.add_parser("plan", help="plan a brief (Claude) and check the plan")
    plan.add_argument("brief")
    queue = sub.add_parser("queue", help="queue a planned brief for the worker")
    queue.add_argument("brief")
    queue.add_argument("--proposer", nargs="+", default=["llm"], choices=jobs.PROPOSERS)
    queue.add_argument(
        "--replicate",
        nargs="+",
        type=int,
        default=[1],
        help="independent repeats of each arm (2 3 queues two more)",
    )
    status_cmd = sub.add_parser("status", help="studies, their arms, and the job queue")
    status_cmd.add_argument("--ids", action="store_true", help="show job ids")
    sub.add_parser("doctor", help="is this machine ready to run SimGate?")
    batch = sub.add_parser("batch", help="queue a hand-made queue for the loop")
    batch.add_argument("queue", help="a queue folder under research/harness")
    front = sub.add_parser("front", help="move a queued job to the front")
    front.add_argument("job", help="a job id, or a unique part of one (status --ids)")
    export = sub.add_parser("export", help="a read-only snapshot of the web app")
    export.add_argument("out", type=Path, nargs="?", default=ROOT / "research" / "site")
    args = parser.parse_args()

    if args.command == "serve":
        web.serve(args.port)
    elif args.command == "worker":
        jobs.work()
    elif args.command == "new":
        web.save_brief(
            args.name,
            web.TEMPLATE.format(
                title=args.name.replace("_", " ").capitalize(),
                question="What do you want to know, in your own words?",
                scope="Which scenes (a category: lead_vehicle, cut_in_merge, "
                "intersection, pedestrian_crossing), which knobs and ranges.",
                budget=50,
                counts="What counts as a failure, and what ranks next.",
            ),
        )
        print(
            f"research/briefs/{args.name}.md written; edit it, then: simgate plan {args.name}"
        )
    elif args.command == "plan":
        brief = jobs.brief_path(args.brief)
        return subprocess.run(
            [
                "uv",
                "run",
                "python",
                "research/harness/study.py",
                str(brief),
                "--plan-only",
            ],
            cwd=ROOT,
            check=False,
        ).returncode
    elif args.command == "queue":
        for replicate in args.replicate:
            for proposer in args.proposer:
                job = web.queue(
                    {"brief": args.brief, "proposer": proposer, "replicate": replicate}
                )
                print(f"queued {job['id']}")
        if not web._worker_alive():
            print("no worker is running: start one with `simgate worker`")
    elif args.command == "status":
        status(args.ids)
    elif args.command == "batch":
        print(f"queued {jobs.add_batch(args.queue)['id']}")
    elif args.command == "front":
        matches = [
            j["id"]
            for j in jobs.jobs()
            if args.job in j["id"] and j["state"] == "queued"
        ]
        if len(matches) != 1:
            raise SystemExit(f"{len(matches)} queued jobs match {args.job!r}")
        jobs.prioritize(matches[0])
        print(f"{matches[0]} is next")
    elif args.command == "doctor":
        import doctor

        return doctor.main()
    elif args.command == "export":
        web.export(args.out)
        print(f"{args.out}/index.html written; serve the repository to view it")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except web.Refused as exc:
        raise SystemExit(f"refused: {exc}")
