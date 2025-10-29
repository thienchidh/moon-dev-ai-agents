# 📝 Note About Generated Data Files

## src/data/ Directory

The `src/data/` directory contains **generated files** created by the AI agents during execution. These files are NOT manually maintained source code.

### Generated Backtest Files (~3,700 files)

Files in directories like:
- `src/data/rbi/*/backtests/`
- `src/data/rbi/*/backtests_final/`
- `src/data/rbi_pp_multi/*/backtests_package/`

These Python files are **automatically generated** by RBI agents (`rbi_agent.py`, `rbi_agent_pp_multi.py`, etc.) and contain hardcoded paths from when they were created.

### Why Not Fixed?

1. **Auto-generated**: These files are created by AI agents, not written by developers
2. **Will be regenerated**: When you run the agents, new files with correct paths will be created
3. **Volume**: ~4,700 files would need updating, and they'll be replaced anyway
4. **Not source code**: These are output/artifacts, not source files

### What To Do?

#### Option 1: Regenerate (Recommended)
Simply run the RBI agents to generate fresh backtest files with correct paths:
```bash
python src/agents/rbi_agent_pp_multi.py
```

The new files will automatically use relative paths.

#### Option 2: Add to .gitignore (Optional)
If you don't want to track generated backtests in git:
```gitignore
# Generated backtest files
src/data/rbi/*/backtests/
src/data/rbi/*/backtests_final/
src/data/rbi_pp_multi/*/backtests_package/
```

#### Option 3: Bulk Fix Script (If Really Needed)
If you absolutely need to fix existing files without regenerating, here's a script:

```python
# fix_generated_backtests.py
import os
from pathlib import Path

OLD_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading"
NEW_PATTERN = "str(Path(__file__).parent.parent.parent"

def fix_backtest_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if OLD_PATH in content:
        # Calculate depth from file to src/data/rbi
        parts = Path(filepath).parts
        data_idx = parts.index('data')
        depth = len(parts) - data_idx - 2  # -2 for data and rbi
        
        parent_chain = '.parent' * depth
        replacement = f'str(Path(__file__){parent_chain}'
        
        content = content.replace(f'"{OLD_PATH}/src/data/rbi', f'{replacement} / "')
        content = content.replace(f"'{OLD_PATH}/src/data/rbi", f"{replacement} / '")
        
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

# Run on all backtest files
for root, dirs, files in os.walk('src/data/rbi'):
    for file in files:
        if file.endswith('_BT.py') or file.endswith('_BTFinal.py'):
            filepath = os.path.join(root, file)
            if fix_backtest_file(filepath):
                print(f"Fixed: {filepath}")
```

**Warning**: This script is provided for completeness but is **NOT recommended**. It's better to regenerate the files.

### Log Files

Similarly, log files in `src/data/*/logs/` contain historical output and don't need fixing. They'll be replaced with new content during normal operation.

### Summary

✅ **All source code fixed** - src/agents/ and src/scripts/
✅ **All documentation fixed** - docs/ and CLAUDE.md
⏭️ **Generated files** - Will be replaced on next agent run
⏭️ **Log files** - Historical output, not critical

## Recommendation

**Just run the agents!** The next time you execute the RBI agents, they will generate fresh backtest files with correct relative paths. No manual intervention needed.

---

🌙 Moon Dev says: Don't fix what will fix itself! 🚀
