#!/usr/bin/env python3
"""
Script to generate GitHub Actions workflows for all projects
"""

import os
from pathlib import Path

# Project definitions
PROJECTS = [
    # Tier 8
    ("tier8-mathematical", "prime-commit-filter", "Prime Commit Filter"),
    ("tier8-mathematical", "fibonacci-file-growth", "Fibonacci File Growth"),
    ("tier8-mathematical", "modulo-mutation-engine", "Modulo Mutation Engine"),
    ("tier8-mathematical", "graph-coloring-repo", "Graph Coloring Repo"),
    ("tier8-mathematical", "palindrome-commit-detector", "Palindrome Commit Detector"),
    # Tier 9
    ("tier9-physics", "lorenz-attractor-drift", "Lorenz Attractor Drift"),
    ("tier9-physics", "pendulum-oscillator", "Pendulum Oscillator"),
    ("tier9-physics", "entropy-clock", "Entropy Clock"),
    ("tier9-physics", "ising-model", "Ising Model"),
    ("tier9-physics", "fractal-directory-tree", "Fractal Directory Tree"),
    # Tier 10
    ("tier10-biological", "dna-encoded-repo", "DNA Encoded Repo"),
    ("tier10-biological", "darwinian-file-selection", "Darwinian File Selection"),
    ("tier10-biological", "symbiosis-repo", "Symbiosis Repo"),
    ("tier10-biological", "predator-prey-dynamics", "Predator-Prey Dynamics"),
    # Tier 11
    ("tier11-graph", "pagerank-file-importance", "PageRank File Importance"),
]

def create_workflow(tier, project_name, display_name):
    """Generate GitHub Actions workflow content"""
    return f"""name: Evolve {display_name}

on:
  schedule:
    - cron: '0 */6 * * *'  # Run every 6 hours
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

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Run evolution script
        working-directory: ./projects/{tier}/{project_name}
        run: python3 evolve.py

      - name: Create Pull Request
        if: success()
        uses: peter-evans/create-pull-request@v6
        with:
          commit-message: "Evolve {display_name} - Gen ${{{{ github.run_number }}}}"
          branch: "evolution/{project_name}"
          title: "{display_name} Evolution: Gen ${{{{ github.run_number }}}}"
          body: |
            🧬 **Autonomous Evolution Update**
            
            Project: {display_name}
            Generation: ${{{{ github.run_number }}}}
            
            This PR contains the latest evolution step generated automatically by GitHub Actions.
          delete-branch: true

      - name: Report Failure
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({{
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '🚨 Evolution Failed: {display_name}',
              body: 'The evolution script for {display_name} failed. Check the [Actions log](' + context.payload.repository.html_url + '/actions/runs/' + context.runId + ') for details.',
              labels: ['evolution-failure', '{tier}']
            }})
"""

def main():
    base_path = Path("/Users/abhisheksinha/Desktop/Autogit/autonomous-zoo-expansion")
    workflows_dir = base_path / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating workflows in {workflows_dir}")
    
    for tier, project_name, display_name in PROJECTS:
        workflow_file = workflows_dir / f"evolve-{project_name}.yml"
        
        with open(workflow_file, 'w') as f:
            f.write(create_workflow(tier, project_name, display_name))
        
        print(f"✅ Created workflow for {display_name}")
    
    print(f"\n🎉 All {len(PROJECTS)} workflows created in .github/workflows/")

if __name__ == "__main__":
    main()
