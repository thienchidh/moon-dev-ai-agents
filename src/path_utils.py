#!/usr/bin/env python3
"""
🌙 Moon Dev's Path Utilities 🚀
Cross-platform path handling utilities for the trading agents project.
Ensures compatibility across Windows, macOS, and Linux.
"""

import os
from pathlib import Path

# Get the project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

def get_project_root():
    """
    Get the absolute path to the project root directory.
    
    Returns:
        Path: Absolute path to project root
    """
    return PROJECT_ROOT

def get_data_dir(subdir=None):
    """
    Get the path to the data directory or a subdirectory within it.
    
    Args:
        subdir (str, optional): Subdirectory path within data/ (e.g., 'rbi', 'chat_agent')
    
    Returns:
        Path: Absolute path to the data directory or subdirectory
    """
    data_path = PROJECT_ROOT / "src" / "data"
    if subdir:
        data_path = data_path / subdir
    return data_path

def get_agents_dir():
    """
    Get the path to the agents directory.
    
    Returns:
        Path: Absolute path to agents directory
    """
    return PROJECT_ROOT / "src" / "agents"

def get_scripts_dir():
    """
    Get the path to the scripts directory.
    
    Returns:
        Path: Absolute path to scripts directory
    """
    return PROJECT_ROOT / "src" / "scripts"

def get_strategies_dir():
    """
    Get the path to the strategies directory.
    
    Returns:
        Path: Absolute path to strategies directory
    """
    return PROJECT_ROOT / "src" / "strategies"

def ensure_dir_exists(path):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path (str or Path): Directory path to create
    
    Returns:
        Path: Absolute path to the directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

# Common data subdirectories
def get_rbi_data_dir():
    """Get path to RBI agent data directory."""
    return get_data_dir("rbi")

def get_chat_agent_data_dir():
    """Get path to chat agent data directory."""
    return get_data_dir("chat_agent")

def get_web_search_data_dir():
    """Get path to web search research data directory."""
    return get_data_dir("web_search_research")

def get_arxiv_data_dir():
    """Get path to Arxiv papers data directory."""
    return get_data_dir("Arxiv")

def get_code_runner_data_dir():
    """Get path to code runner data directory."""
    return get_data_dir("code_runner")

def get_private_data_dir():
    """Get path to private data directory."""
    return get_data_dir("private_data")

def get_rbi_pp_multi_data_dir():
    """Get path to RBI PP Multi data directory."""
    return get_data_dir("rbi_pp_multi")

# Example usage in code:
# from src.path_utils import get_data_dir, get_rbi_data_dir
# 
# # Instead of: "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
# # Use: get_rbi_data_dir() / "BTC-USD-15m.csv"
# data_file = get_rbi_data_dir() / "BTC-USD-15m.csv"
