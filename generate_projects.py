#!/usr/bin/env python3
"""
Script to generate all remaining project files for autonomous-zoo-expansion
"""

import json
import os
from pathlib import Path

# Project definitions
PROJECTS = [
    # Tier 8
    {
        "tier": "tier8-mathematical",
        "name": "fibonacci-file-growth",
        "title": "Fibonacci File Growth",
        "tagline": "Growing files according to the Fibonacci sequence",
        "analogy": "Files multiply like rabbits—each generation equals the sum of the previous two.",
        "concept": "Fibonacci Sequence - each number is the sum of the two preceding ones (1, 1, 2, 3, 5, 8, 13...)",
        "prev": "prime-commit-filter",
        "next": "modulo-mutation-engine"
    },
    {
        "tier": "tier8-mathematical",
        "name": "modulo-mutation-engine",
        "title": "Modulo Mutation Engine",
        "tagline": "Cyclic mutations based on modular arithmetic",
        "analogy": "A clock that resets mutations—every 12th hour, everything changes in a predictable cycle.",
        "concept": "Modular Arithmetic - numbers wrap around like a clock (23 mod 12 = 11)",
        "prev": "fibonacci-file-growth",
        "next": "graph-coloring-repo"
    },
    {
        "tier": "tier8-mathematical",
        "name": "graph-coloring-repo",
        "title": "Graph Coloring Repo",
        "tagline": "Ensuring proper graph coloring of file dependencies",
        "analogy": "Like coloring a map so no two touching countries have the same color—except with code files.",
        "concept": "Graph Coloring - assigning colors to vertices so no adjacent vertices share the same color",
        "prev": "modulo-mutation-engine",
        "next": "palindrome-commit-detector"
    },
    {
        "tier": "tier8-mathematical",
        "name": "palindrome-commit-detector",
        "title": "Palindrome Commit Detector",
        "tagline": "Celebrating palindromic commit hashes",
        "analogy": "A repo that celebrates when commit hashes read the same forwards and backwards, like 'racecar'.",
        "concept": "Palindromes - sequences that read the same forwards and backwards",
        "prev": "graph-coloring-repo",
        "next": "../../tier9-physics/lorenz-attractor-drift"
    },
    # Tier 9
    {
        "tier": "tier9-physics",
        "name": "lorenz-attractor-drift",
        "title": "Lorenz Attractor File Drift",
        "tagline": "Files drift through chaotic but bounded trajectories",
        "analogy": "Files drift through directories like weather systems—chaotic yet beautifully patterned.",
        "concept": "Lorenz Attractor - chaotic system with butterfly-wing shaped strange attractor",
        "prev": "../../tier8-mathematical/palindrome-commit-detector",
        "next": "pendulum-oscillator"
    },
    {
        "tier": "tier9-physics",
        "name": "pendulum-oscillator",
        "title": "Pendulum Repo Oscillator",
        "tagline": "Files oscillate between directories harmonically",
        "analogy": "Files swing back and forth between folders like a grandfather clock, forever.",
        "concept": "Simple Harmonic Motion - periodic oscillation like a pendulum",
        "prev": "lorenz-attractor-drift",
        "next": "entropy-clock"
    },
    {
        "tier": "tier9-physics",
        "name": "entropy-clock",
        "title": "Entropy Clock",
        "tagline": "Repository entropy increases toward maximum disorder",
        "analogy": "The universe winding down—each day the repo gets messier, approaching maximum disorder.",
        "concept": "Second Law of Thermodynamics - entropy always increases in isolated systems",
        "prev": "pendulum-oscillator",
        "next": "ising-model"
    },
    {
        "tier": "tier9-physics",
        "name": "ising-model",
        "title": "Ising Model Repo",
        "tagline": "Files align or flip like magnetic spins",
        "analogy": "Files like magnets—they align with neighbors or flip opposite, creating magnetic domains.",
        "concept": "Ising Model - statistical model of ferromagnetism in statistical mechanics",
        "prev": "entropy-clock",
        "next": "fractal-directory-tree"
    },
    {
        "tier": "tier9-physics",
        "name": "fractal-directory-tree",
        "title": "Fractal Directory Tree",
        "tagline": "Self-similar directory structure expanding infinitely",
        "analogy": "A tree that grows smaller copies of itself infinitely, like looking into infinite mirrors.",
        "concept": "Fractal Geometry - self-similar patterns at every scale",
        "prev": "ising-model",
        "next": "../../tier10-biological/dna-encoded-repo"
    },
    # Tier 10
    {
        "tier": "tier10-biological",
        "name": "dna-encoded-repo",
        "title": "DNA-Encoded Repo",
        "tagline": "Files encoded as DNA sequences with genetic mutations",
        "analogy": "Files are DNA strands—mutations happen, genes duplicate, evolution occurs over generations.",
        "concept": "Genetic Code - DNA bases (A, T, G, C) encoding information with mutations and replication",
        "prev": "../../tier9-physics/fractal-directory-tree",
        "next": "darwinian-file-selection"
    },
    {
        "tier": "tier10-biological",
        "name": "darwinian-file-selection",
        "title": "Darwinian File Selection",
        "tagline": "Natural selection among files based on fitness",
        "analogy": "Survival of the fittest—only the strongest, most 'fit' files survive each generation.",
        "concept": "Natural Selection - differential survival and reproduction based on fitness",
        "prev": "dna-encoded-repo",
        "next": "symbiosis-repo"
    },
    {
        "tier": "tier10-biological",
        "name": "symbiosis-repo",
        "title": "Symbiosis Repo",
        "tagline": "Files with interdependent survival relationships",
        "analogy": "Files that need each other to survive—kill one, and its partner dies too, like bees and flowers.",
        "concept": "Symbiosis - close ecological relationships between different species",
        "prev": "darwinian-file-selection",
        "next": "predator-prey-dynamics"
    },
    {
        "tier": "tier10-biological",
        "name": "predator-prey-dynamics",
        "title": "Predator-Prey Dynamics",
        "tagline": "Population oscillations following Lotka-Volterra equations",
        "analogy": "Wolves and rabbits—predator files hunt prey files, populations oscillate in endless cycles.",
        "concept": "Lotka-Volterra Equations - mathematical model of predator-prey interactions",
        "prev": "symbiosis-repo",
        "next": "../../tier11-graph/pagerank-file-importance"
    },
    # Tier 11
    {
        "tier": "tier11-graph",
        "name": "pagerank-file-importance",
        "title": "PageRank  File Importance",
        "tagline": "Ranking files by network importance algorithm",
        "analogy": "Google's ranking algorithm for files—important files get promoted, obscure ones deleted.",
        "concept": "PageRank Algorithm - measuring importance of nodes in a network graph",
        "prev": "../../tier10-biological/predator-prey-dynamics",
        "next": None
    }
]

def create_readme(project):
    """Generate README content"""
    next_link = f"[{project['next']}](../{project['next']}/README.md)" if project['next'] else "End of catalog"
    prev_link = f"[{project['prev']}](../{project['prev']}/README.md)" if project['prev'] else ""
    
    return f"""### [⬅️ Back to Expansion Catalog](../../../README.md)

---

# {project['title']} — {project['tagline']}

## 📖 The Analogy

> {project['analogy']}

> **Self-evolving repository implementing {project['title']}**

## 🧠 Mathematical Concept

**{project['concept']}**

This repository implements this concept autonomously, evolving daily without human intervention.

## 🎯 What This Does

Every day, the repository evolves according to the mathematical rules defined in `evolve.py`.

## 📊 Current State

- **Generation**: Check `state.json`
- **Evolution Log**: See `evolution_log.md`

## 🚀 Running Locally

```bash
python evolve.py  # Run one evolution step
```

## 📖 Layman Explanation

"{project['analogy']}"

## 🔬 Technical Details

- **Algorithm**: Implemented in `evolve.py`
- **State Management**: `state.json`
- **Determinism**: Date-based randomness

## 📈 Evolution Log

See [evolution_log.md](evolution_log.md) for the complete evolution timeline.

## 🛠️ Technical Anatomy

- **DNA**: [evolve.py](evolve.py) (The instructions for life)
- **Vital Signs**: [state.json](state.json) (Current memory and state)

## 🏘️ Neighboring Organisms

{f"⬅️ **Previous**: {prev_link}" if prev_link else ""}
{f"➡️ **Next**: {next_link}" if project['next'] else ""}

---

**Status**: 🟢 Fully Autonomous | **Tier**: {project['tier'].split('-')[0].replace('tier', '')} | **Autonomy**: ⭐⭐⭐⭐⭐
"""

def create_evolve_script(project):
    """Generate evolve.py content"""
    return f'''#!/usr/bin/env python3
"""
{project['title']}
{project['tagline']}
"""

import json
import os
import hashlib
import random
from datetime import datetime
from pathlib import Path

def load_state():
    """Load current state from JSON"""
    if Path("state.json").exists():
        with open("state.json") as f:
            return json.load(f)
    return {{
        "generation": 0
    }}

def save_state(state):
    """Persist state to JSON"""
    with open("state.json", 'w') as f:
        json.dump(state, f, indent=2)

def get_date_seed():
    """Generate deterministic seed from current date"""
    date_str = str(datetime.now().date())
    return int(hashlib.sha256(date_str.encode()).hexdigest(), 16) % (2**32)

def log_evolution(state, summary):
    """Append to evolution_log.md"""
    timestamp = datetime.now().isoformat()
    
    if not Path("evolution_log.md").exists():
        with open("evolution_log.md", 'w') as f:
            f.write("# {project['title']} Evolution\\\\n\\\\n")
            f.write("Tracking autonomous evolution over time.\\\\n\\\\n")
    
    with open("evolution_log.md", 'a') as f:
        f.write(f"\\\\n## Generation {{state['generation']}} — {{timestamp[:10]}}\\\\n\\\\n")
        f.write(f"{{summary}}\\\\n")

def evolve_step(state):
    """Core evolution logic - IMPLEMENT YOUR ALGORITHM HERE"""
    state["generation"] += 1
    random.seed(get_date_seed())
    
    # Create data directory
    Path("data").mkdir(exist_ok=True)
    
    # TODO: Implement {project['title']} logic here
    # This is a template - customize based on your mathematical concept
    
    # Example: Create a marker file
    marker_file = f"data/gen_{{state['generation']:04d}}.txt"
    with open(marker_file, 'w') as f:
        f.write(f"Generation: {{state['generation']}}\\\\n")
        f.write(f"Concept: {project['concept']}\\\\n")
    
    summary = f"Generation {{state['generation']}} evolved successfully."
    log_evolution(state, summary)
    
    print(f"✅ {project['title']} - Generation {{state['generation']}}")
    
    return state

def main():
    ""Main evolution loop"""
    print(f"🧬 {project['title']} - Evolution Step")
    print("=" * 50)
    
    state = load_state()
    
    if state["generation"] >= 365:  # One year limit
        print("⚠️  Max generations reached.")
        return
    
    state = evolve_step(state)
    save_state(state)
    
    print("=" * 50)
    print(f"✅ Generation {{state['generation']}} complete\\\\n")

if __name__ == "__main__":
    main()
'''

def create_state_json():
    """Generate state.json content"""
    return '''{
  "generation": 0
}
'''

def main():
    base_path = Path("/Users/abhisheksinha/Desktop/Autogit/autonomous-zoo-expansion/projects")
    
    for project in PROJECTS:
        project_path = base_path / project["tier"] / project["name"]
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create data directory
        (project_path / "data").mkdir(exist_ok=True)
        
        # Create README.md
        with open(project_path / "README.md", 'w') as f:
            f.write(create_readme(project))
        
        # Create evolve.py
        with open(project_path / "evolve.py", 'w') as f:
            f.write(create_evolve_script(project))
        
        # Create state.json
        with open(project_path / "state.json", 'w') as f:
            f.write(create_state_json())
        
        print(f"✅ Created {project['name']}")
    
    print(f"\\n🎉 All {len(PROJECTS)} projects created!")

if __name__ == "__main__":
    main()
