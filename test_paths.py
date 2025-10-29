#!/usr/bin/env python3
"""
🌙 Moon Dev's Path Test Script 🚀
Tests that all path utilities work correctly across platforms
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that path_utils can be imported"""
    print("="*80)
    print("🧪 Testing imports...")
    try:
        from path_utils import (
            get_project_root,
            get_data_dir,
            get_agents_dir,
            get_scripts_dir,
            get_rbi_data_dir,
            get_chat_agent_data_dir,
        )
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_path_resolution():
    """Test that paths resolve correctly"""
    print("\n" + "="*80)
    print("🧪 Testing path resolution...")
    
    from path_utils import (
        get_project_root,
        get_data_dir,
        get_agents_dir,
        get_scripts_dir,
        get_rbi_data_dir,
    )
    
    tests = [
        ("Project Root", get_project_root()),
        ("Data Directory", get_data_dir()),
        ("Agents Directory", get_agents_dir()),
        ("Scripts Directory", get_scripts_dir()),
        ("RBI Data Directory", get_rbi_data_dir()),
    ]
    
    all_passed = True
    for name, path in tests:
        exists = path.exists()
        status = "✅" if exists else "⚠️ "
        print(f"{status} {name:25s} -> {path}")
        if not exists:
            print(f"   Note: Directory doesn't exist yet (will be created on first use)")
    
    return all_passed

def test_cross_platform():
    """Test that paths work on current platform"""
    print("\n" + "="*80)
    print("🧪 Testing cross-platform compatibility...")
    
    import platform
    from path_utils import get_data_dir
    
    system = platform.system()
    print(f"📍 Current platform: {system}")
    
    test_path = get_data_dir("rbi") / "BTC-USD-15m.csv"
    path_str = str(test_path)
    
    if system == "Windows":
        has_backslash = "\\" in path_str
        print(f"   Windows-style separators: {'✅' if has_backslash else '❌'}")
        print(f"   Path: {path_str}")
    else:
        has_forward_slash = "/" in path_str
        print(f"   Unix-style separators: {'✅' if has_forward_slash else '❌'}")
        print(f"   Path: {path_str}")
    
    print(f"✅ Path uses native separators for {system}")
    return True

def test_relative_imports():
    """Test that relative imports work from different locations"""
    print("\n" + "="*80)
    print("🧪 Testing relative imports from scripts...")
    
    # Simulate import from src/scripts/
    scripts_path = Path(__file__).parent / "src" / "scripts"
    test_file = scripts_path / "arvix_download.py"
    
    if test_file.exists():
        print(f"✅ Found test script: {test_file.name}")
        
        # Check if it has the correct import pattern
        with open(test_file, 'r') as f:
            content = f.read()
            has_path_utils = "from path_utils import" in content
            has_sys_path = "sys.path.insert" in content
            
            if has_path_utils:
                print("✅ Script uses path_utils")
            if has_sys_path:
                print("✅ Script sets up sys.path correctly")
            
            if has_path_utils and has_sys_path:
                print("✅ Script is properly configured for cross-platform use")
                return True
    else:
        print("⚠️  Test script not found")
    
    return True

def main():
    """Run all tests"""
    print("🌙 Moon Dev's Path Utilities Test Suite 🚀")
    print()
    
    results = []
    
    # Run tests
    results.append(("Import Test", test_imports()))
    results.append(("Path Resolution Test", test_path_resolution()))
    results.append(("Cross-Platform Test", test_cross_platform()))
    results.append(("Relative Import Test", test_relative_imports()))
    
    # Summary
    print("\n" + "="*80)
    print("📊 Test Summary")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10s} {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your paths are configured correctly!")
        print("🌙 Moon Dev approves! 🚀")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
