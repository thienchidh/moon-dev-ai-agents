#!/usr/bin/env python3
"""
🌙 Moon Dev's Path Fixer Script 🚀
Fixes all hardcoded MacOS absolute paths to use relative paths with path_utils.
"""

import os
import re
from pathlib import Path

# Base path to replace
OLD_BASE_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading"

# Mapping of old paths to new path_utils functions
PATH_MAPPINGS = {
    f"{OLD_BASE_PATH}/src/data/rbi": "get_rbi_data_dir()",
    f"{OLD_BASE_PATH}/src/data/chat_agent": "get_chat_agent_data_dir()",
    f"{OLD_BASE_PATH}/src/data/web_search_research": "get_web_search_data_dir()",
    f"{OLD_BASE_PATH}/src/data/Arxiv": "get_arxiv_data_dir()",
    f"{OLD_BASE_PATH}/src/data/code_runner": "get_code_runner_data_dir()",
    f"{OLD_BASE_PATH}/src/data/private_data": "get_private_data_dir()",
    f"{OLD_BASE_PATH}/src/data/rbi_pp_multi": "get_rbi_pp_multi_data_dir()",
    f"{OLD_BASE_PATH}/src/data": "get_data_dir()",
    f"{OLD_BASE_PATH}/src/agents": "get_agents_dir()",
    f"{OLD_BASE_PATH}/src/scripts": "get_scripts_dir()",
    f"{OLD_BASE_PATH}/src/strategies": "get_strategies_dir()",
    f"{OLD_BASE_PATH}": "get_project_root()",
}

def needs_path_utils_import(content):
    """Check if file needs path_utils import."""
    return "from path_utils import" not in content and "from src.path_utils import" not in content

def add_path_utils_import(content, imports_needed):
    """Add path_utils imports to file."""
    # Find the best place to add import
    lines = content.split('\n')
    
    # Look for existing imports
    last_import_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            last_import_idx = i
    
    # Create import statement
    import_statement = f"from path_utils import {', '.join(sorted(imports_needed))}"
    
    # Check if we need to add sys.path insert
    has_pathlib = 'from pathlib import Path' in content
    has_sys_path = 'sys.path.insert' in content or 'sys.path.append' in content
    
    if has_pathlib and not has_sys_path:
        # Add sys.path.insert after pathlib import
        for i, line in enumerate(lines):
            if 'from pathlib import Path' in line:
                sys_import = "import sys"
                path_insert = "sys.path.insert(0, str(Path(__file__).parent.parent))"
                
                # Check if sys is already imported
                if 'import sys' not in content:
                    lines.insert(i + 1, sys_import)
                    lines.insert(i + 2, path_insert)
                    lines.insert(i + 3, import_statement)
                    lines.insert(i + 4, "")
                else:
                    lines.insert(i + 1, path_insert)
                    lines.insert(i + 2, import_statement)
                    lines.insert(i + 3, "")
                break
    elif last_import_idx >= 0:
        # Add after last import
        lines.insert(last_import_idx + 1, import_statement)
        lines.insert(last_import_idx + 2, "")
    else:
        # Add at beginning after shebang/docstring
        insert_idx = 0
        if lines and lines[0].startswith('#!'):
            insert_idx = 1
        if insert_idx < len(lines) and (lines[insert_idx].strip().startswith('"""') or lines[insert_idx].strip().startswith("'''")):
            # Skip docstring
            quote = '"""' if lines[insert_idx].strip().startswith('"""') else "'''"
            insert_idx += 1
            while insert_idx < len(lines) and quote not in lines[insert_idx]:
                insert_idx += 1
            insert_idx += 1
        lines.insert(insert_idx, "from pathlib import Path")
        lines.insert(insert_idx + 1, "import sys")
        lines.insert(insert_idx + 2, "sys.path.insert(0, str(Path(__file__).parent.parent))")
        lines.insert(insert_idx + 3, import_statement)
        lines.insert(insert_idx + 4, "")
    
    return '\n'.join(lines)

def fix_file_paths(filepath):
    """Fix hardcoded paths in a Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ⚠️  Could not read {filepath}: {e}")
        return False
    
    original_content = content
    imports_needed = set()
    
    # Replace paths
    for old_path, new_func in sorted(PATH_MAPPINGS.items(), key=lambda x: -len(x[0])):
        # Pattern for string literals
        patterns = [
            f'"{old_path}"',
            f"'{old_path}'",
            f'"{old_path}/',
            f"'{old_path}/",
        ]
        
        for pattern in patterns:
            if pattern in content:
                # Extract the function name
                func_name = new_func.split('(')[0]
                imports_needed.add(func_name)
                
                # Determine if we need to add Path or str()
                if pattern.endswith('"') or pattern.endswith("'"):
                    # Just the base path
                    replacement = f"str({new_func})"
                else:
                    # Path with subdirectory
                    quote = pattern[0]
                    remaining = pattern[len(f'{quote}{old_path}/'):-1]
                    replacement = f"str({new_func} / {quote}{remaining}{quote})"
                
                content = content.replace(pattern, replacement)
    
    # Add imports if needed and changes were made
    if imports_needed and content != original_content and needs_path_utils_import(content):
        content = add_path_utils_import(content, imports_needed)
    
    # Write back if changed
    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"  ⚠️  Could not write {filepath}: {e}")
            return False
    
    return False

def process_directory(directory, extensions=('.py',)):
    """Process all files in directory with given extensions."""
    directory = Path(directory)
    fixed_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        if '.git' in root or '__pycache__' in root or 'node_modules' in root:
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = Path(root) / file
                if fix_file_paths(filepath):
                    fixed_count += 1
                    print(f"  ✅ Fixed: {filepath}")
    
    return fixed_count

def main():
    print("=" * 80)
    print("🌙 Moon Dev's Path Fixer")
    print("=" * 80)
    print()
    
    project_root = Path(__file__).parent
    
    # Process src/agents
    print("📁 Processing src/agents/...")
    count = process_directory(project_root / "src" / "agents")
    print(f"   Fixed {count} files")
    print()
    
    # Process src/scripts
    print("📁 Processing src/scripts/...")
    count = process_directory(project_root / "src" / "scripts")
    print(f"   Fixed {count} files")
    print()
    
    print("=" * 80)
    print("🎉 Path fixing complete!")
    print("=" * 80)
    print()
    print("⚠️  Note: This script does NOT fix:")
    print("   - Data files in src/data/ (backtest scripts)")
    print("   - Documentation files (.md)")
    print("   - Log files (.txt)")
    print()
    print("   These should be updated individually or regenerated.")

if __name__ == "__main__":
    main()
