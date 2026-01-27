#!/usr/bin/env python3
"""
Script to generate GitHub Actions workflow files for each project in autonomous-zoo-expansion
"""

import os
from pathlib import Path

# Project definitions (same as before)
PROJECTS = [
    {"tier": "tier8-mathematical", "name": "prime-commit-filter", "title": "Prime Commit Filter"},
    {"tier": "tier8-mathematical", "name": "fibonacci-file-growth", "title": "Fibonacci File Growth"},
    {"tier": "tier8-mathematical", "name": "modulo-mutation-engine", "title": "Modulo Mutation Engine"},
    {"tier": "tier8-mathematical", "name": "graph-coloring-repo", "title": "Graph Coloring Repo"},
    {"tier": "tier8-mathematical", "name": "palindrome-commit-detector", "title": "Palindrome Commit Detector"},
    {"tier": "tier9-physics", "name": "lorenz-attractor-drift", "title": "Lorenz Attractor File Drift"},
    {"tier": "tier9-physics", "name": "pendulum-oscillator", "title": "Pendulum Repo Oscillator"},
    {"tier": "tier9-physics", "name": "entropy-clock", "title": "Entropy Clock"},
    {"tier": "tier9-physics", "name": "ising-model", "title": "Ising Model"},
    {"tier": "tier9-physics", "name": "fractal-directory-tree", "title": "Fractal Directory Tree"},
    {"tier": "tier10-biological", "name": "dna-encoded-repo", "title": "DNA-Encoded Repo"},
    {"tier": "tier10-biological", "name": "darwinian-file-selection", "title": "Darwinian File Selection"},
    {"tier": "tier10-biological", "name": "symbiosis-repo", "title": "Symbiosis Repo"},
    {"tier": "tier10-biological", "name": "predator-prey-dynamics", "title": "Predator-Prey Dynamics"},
    {"tier": "tier11-graph", "name": "pagerank-file-importance", "title": "PageRank File Importance"}
]

def create_workflow(project):
    """Generate YAML content for the project's workflow"""
    return f'''
concurrency: autonomous-zoo-expansion-evolution

name: Evolve {project['title']}

on:
  schedule:
    - cron: '30 */6 * * *'  # Run every 6 hours
  workflow_dispatch:

jobs:
  evolve:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          ref: main

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Run evolution script
        id: run_evolve
        run: |
          cd projects/{project['tier']}/{project['name']}
          python3 evolve.py
          echo "SUMMARY=$(tail -n 1 evolution_log.md)" >> $GITHUB_OUTPUT

      - name: Fetch and Rebase
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git fetch origin main
          git pull --rebase --autostash origin main

      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "Evolve {project['title']} - Gen ${{ github.run_number }} [skip ci]"
          branch: main

      - name: Report Failure
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({{
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '🚨 Incident: Evolution Halted for {project['title']}',
              body: 'The evolution script for {project['title']} failed.\\n\\n[View Actions Log](' + context.payload.repository.html_url + '/actions/runs/' + context.runId + ')',
              labels: ['evolution-failure']
            }})
'''

def main():
    repo_path = Path("/Users/abhisheksinha/Desktop/Autogit/autonomous-zoo-expansion")
    workflow_dir = repo_path / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    # Cleanup old project workflows
    for wf in workflow_dir.glob("evolve*.yml"):
        if wf.name != "evolution.yml":
            wf.unlink()
            print(f"🗑️ Deleted old workflow: {wf.name}")

    for project in PROJECTS:
        filename = f"evolve-{project['name']}.yml"
        with open(workflow_dir / filename, 'w') as f:
            f.write(create_workflow(project))
        print(f"✅ Created workflow: {filename}")
    
    print(f"\n🎉 All {len(PROJECTS)} workflow files generated!")

if __name__ == "__main__":
    main()
