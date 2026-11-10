#!/bin/bash
# Usage: ./run_org.sh <run-name> <agent>   e.g. ./run_org.sh haiku-s1 claude:haiku
# Starts the arms that give the agent the company Slack, Notion and pull request history.
set -eu
cd "$(dirname "$0")"
run=$1
agent=$2
mkdir -p runs/logs
for arm in "none available" "none directed" "notes directed"; do
	read -r learner knowledge <<<"$arm"
	.venv/bin/python -m clbench.run --run-name "$run" --learner "$learner" --knowledge "$knowledge" --agent "$agent" \
		>"runs/logs/$run-$learner-org-$knowledge.log" 2>&1 &
done
wait
