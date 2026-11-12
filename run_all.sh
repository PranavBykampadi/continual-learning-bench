#!/bin/bash
# Usage: ./run_all.sh <run-name> <agent>   e.g. ./run_all.sh haiku-s1 claude:haiku
# Starts every arm in parallel. Each arm resumes from its own log if you rerun.
set -eu
cd "$(dirname "$0")"
run=$1
agent=$2
mkdir -p runs/logs
for arm in "none rich" "placebo rich" "oracle rich" "history rich" "notes rich" "notes sparse" "notes lenient" "memdir rich"; do
	read -r learner feedback <<<"$arm"
	.venv/bin/python -m clbench.run --run-name "$run" --learner "$learner" --feedback "$feedback" --agent "$agent" \
		>"runs/logs/$run-$learner-$feedback.log" 2>&1 &
done
wait
