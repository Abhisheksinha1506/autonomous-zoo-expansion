### [⬅️ Back to Expansion Catalog](../../../README.md)

---

# Prime Commit Filter — The Selective Bouncer

## 📖 The Analogy

> Think of this repo as a VIP club that only admits prime-numbered guests. Every commit's hash gets converted to a number—if it's prime, the commit stays. If it's composite, it's reverted. Over time, only mathematically 'pure' commits survive.

> **Self-filtering repository that preserves only prime-valued commits**

## 🧠 Mathematical Concept

**Prime Numbers** are integers greater than 1 that have no divisors other than 1 and themselves. They are the building blocks of all numbers.

- **2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31...**
- **Primality Testing**: Checking if a number is prime (various algorithms exist)
- **Prime Density**: Primes become less frequent as numbers grow larger

This repository converts each commit hash to a number and tests primality. Non-prime commits are automatically reverted, creating a "filtered" commit history.

## 🎯 What This Does

Every day, the repository:
1. Examines recent commits
2. Converts commit SHA to a numeric value
3. Tests if the number is prime
4. Reverts composite-numbered commits
5. Logs prime/composite statistics
6. Maintains only prime-valued history

**Result**: The repo's commit history becomes a sequence of primes.

## 📊 Current State

- **Generation**: Check `state.json`
- **Primes Found**: See `evolution_log.md`
- **Current Streak**: Count of consecutive primes

## 🚀 Running Locally

```bash
python evolve.py  # Run one evolution step
```

## 📖 Layman Explanation

"A bouncer who only lets prime-numbered commits into the club, kicking out all the composite ones."

## 🔬 Technical Details

- **Algorithm**: Miller-Rabin primality test (probabilistic)
- **Hash Conversion**: Last 16 digits of SHA-256 → integer
- **Safety**: Keeps at least one commit (initial)
- **Determinism**: Based on commit hashes (immutable)

## 📈 Evolution Log

See [evolution_log.md](evolution_log.md) for the complete prime discovery timeline.

## 🛠️ Technical Anatomy

- **DNA**: [evolve.py](evolve.py) (The instructions for life)
- **Vital Signs**: [state.json](state.json) (Current memory and state)

## 🏘️ Neighboring Organisms

➡️ **Next**: [fibonacci-file-growth](../fibonacci-file-growth/README.md)

---

**Status**: 🟢 Fully Autonomous | **Tier**: 8 | **Autonomy**: ⭐⭐⭐⭐⭐
