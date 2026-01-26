#!/usr/bin/env python3
"""
Prime Commit Filter
Autonomous repository that preserves only prime-valued commits
"""

import json
import os
import hashlib
from datetime import datetime
from pathlib import Path

def is_prime(n):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(5):  # 5 iterations for good probability
        a = 2 + (hash(str(n) + str(_)) % (n - 3))
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for __ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def hash_to_number(commit_hash):
    """Convert commit hash to integer (last 16 digits)"""
    return int(commit_hash[-16:], 16) % (10**12)

def load_state():
    """Load current state from JSON"""
    if Path("state.json").exists():
        with open("state.json") as f:
            return json.load(f)
    return {
        "generation": 0,
        "total_primes_found": 0,
        "total_composites_filtered": 0,
        "current_streak": 0
    }

def save_state(state):
    """Persist state to JSON"""
    with open("state.json", 'w') as f:
        json.dump(state, f, indent=2)

def log_evolution(state, is_prime_commit, commit_value):
    """Append to evolution_log.md"""
    timestamp = datetime.now().isoformat()
    
    if not Path("evolution_log.md").exists():
        with open("evolution_log.md", 'w') as f:
            f.write("# Prime Commit Filter Evolution\\n\\n")
            f.write("Tracking the journey of prime-valued commits.\\n\\n")
    
    status = "✅ PRIME" if is_prime_commit else "❌ COMPOSITE"
    
    with open("evolution_log.md", 'a') as f:
        f.write(f"\\n## Generation {state['generation']} — {timestamp[:10]}\\n\\n")
        f.write(f"- **Status**: {status}\\n")
        f.write(f"- **Commit Value**: {commit_value}\\n")
        f.write(f"- **Primes Found**: {state['total_primes_found']}\\n")
        f.write(f"- **Composites Filtered**: {state['total_composites_filtered']}\\n")
        f.write(f"- **Current Streak**: {state['current_streak']}\\n")

def evolve_step(state):
    """Core evolution logic"""
    state["generation"] += 1
    
    # Simulate checking current "commit" (use generation number for demo)
    # In real implementation, this would check actual git commits
    simulated_hash = hashlib.sha256(str(state["generation"]).encode()).hexdigest()
    commit_value = hash_to_number(simulated_hash)
    
    is_prime_commit = is_prime(commit_value)
    
    if is_prime_commit:
        state["total_primes_found"] += 1
        state["current_streak"] += 1
        print(f"✅ PRIME FOUND: {commit_value}")
    else:
        state["total_composites_filtered"] += 1
        state["current_streak"] = 0
        print(f"❌ COMPOSITE FILTERED: {commit_value}")
    
    # Create a marker file in data/ for primes
    if is_prime_commit:
        Path("data").mkdir(exist_ok=True)
        marker_file = f"data/prime_{state['generation']:04d}_{commit_value}.txt"
        with open(marker_file, 'w') as f:
            f.write(f"Prime value: {commit_value}\\nGeneration: {state['generation']}\\n")
    
    log_evolution(state, is_prime_commit, commit_value)
    
    return state

def main():
    """"Main evolution loop"""
    print("🧬 Prime Commit Filter - Evolution Step")
    print("=" * 50)
    
    state = load_state()
    
    if state["generation"] >= 365:  # One year of daily runs
        print("⚠️  Max generations reached. Evolution complete.")
        return
    
    state = evolve_step(state)
    save_state(state)
    
    print("=" * 50)
    print(f"✅ Generation {state['generation']} complete\\n")

if __name__ == "__main__":
    main()
