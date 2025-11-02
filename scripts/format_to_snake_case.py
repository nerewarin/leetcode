#!/usr/bin/env python3
"""
Pre-commit compatible Python filename formatter.
Located in scripts/format_to_snake_case.py
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def to_snake_case(filename):
    """Convert filename to snake_case."""
    # Remove .py extension for processing
    name_without_ext = filename[:-3] if filename.endswith(".py") else filename
    extension = ".py" if filename.endswith(".py") else ""

    # Replace hyphens and spaces with underscores
    name = name_without_ext.replace("-", "_").replace(" ", "_")

    # Insert underscores between lowercase/uppercase transitions
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)

    # Insert underscores between uppercase/lowercase transitions
    name = re.sub(r"([A-Z])([A-Z][a-z])", r"\1_\2", name)

    # Convert to lowercase
    snake_name = name.lower()

    # Remove multiple consecutive underscores
    snake_name = re.sub(r"_+", "_", snake_name)

    # Remove leading/trailing underscores
    snake_name = snake_name.strip("_")

    return snake_name + extension


def should_skip_file(filename):
    """Check if file should be skipped from renaming."""
    # Skip __init__.py and other Python special files
    special_files = {"__init__.py", "__main__.py", "__version__.py"}
    if filename in special_files:
        return True

    # Skip files that start and end with double underscores
    if filename.startswith("__") and filename.endswith("__.py"):
        return True

    return False


def is_gitignored(file_path):
    """Check if a file is gitignored using git check-ignore."""
    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", str(file_path)],
            capture_output=True,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        # If git is not available or command fails, assume not ignored
        return False


def get_gitignore_patterns(root_dir):
    """Get all .gitignore patterns from the repository."""
    gitignore_patterns = []
    gitignore_path = Path(root_dir) / ".gitignore"

    if gitignore_path.exists():
        with open(gitignore_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    gitignore_patterns.append(line)

    return gitignore_patterns


def check_snake_case_compliance(filenames):
    """
    Check if filenames comply with snake_case naming.

    Returns:
        tuple: (bool, list) - (is_compliant, list_of_violations)
    """
    violations = []

    for filename in filenames:
        if filename.endswith(".py"):
            file_path = Path(filename)

            # Skip gitignored files
            if is_gitignored(file_path):
                continue

            # Extract just the filename from path
            filename_only = file_path.name

            # Skip special files
            if should_skip_file(filename_only):
                continue

            expected_name = to_snake_case(filename_only)
            if filename_only != expected_name:
                violations.append((filename, expected_name))

    return len(violations) == 0, violations


def git_rename(old_path, new_path):
    """Use git mv to properly track the rename."""
    try:
        subprocess.run(["git", "mv", str(old_path), str(new_path)], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def format_python_files(root_dir, dry_run=False, verbose=False, staged_only=False):
    """Find all Python files and convert their names to snake_case."""
    root_path = Path(root_dir)
    changes = []
    skipped = []

    if staged_only:
        # Get only staged Python files
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--cached"],
                capture_output=True,
                text=True,
                check=True,
            )
            staged_files = [f.strip() for f in result.stdout.split("\n") if f.strip()]
            python_files = [Path(f) for f in staged_files if f.endswith(".py") and Path(f).exists()]
        except subprocess.CalledProcessError:
            raise RuntimeError("Failed to get staged files from git")
    else:
        # Find all .py files recursively
        python_files = list(root_path.rglob("*.py"))

    if verbose:
        print(f"Found {len(python_files)} Python files to process")

    for file_path in python_files:
        # Skip hidden directories and __pycache__
        if any(part.startswith(".") or part == "__pycache__" for part in file_path.parts):
            continue

        # Skip gitignored files
        if is_gitignored(file_path):
            if verbose:
                print(f"⏭️  Skipping gitignored file: {file_path}")
            skipped.append((file_path, "gitignored"))
            continue

        original_name = file_path.name

        # Skip special Python files
        if should_skip_file(original_name):
            if verbose:
                print(f"⏭️  Skipping special file: {original_name}")
            skipped.append((file_path, "special file"))
            continue

        new_name = to_snake_case(original_name)

        # Skip if no change needed
        if original_name == new_name:
            if verbose:
                print(f"✓ No change needed: {original_name}")
            continue

        new_path = file_path.parent / new_name

        # Check if target file already exists
        if new_path.exists():
            print(f"⚠️  Skipping: Target file already exists: {new_path}")
            skipped.append((file_path, f"target exists: {new_path}"))
            continue

        changes.append((file_path, new_path))

        if dry_run:
            print(f"📋 Would rename: {file_path} -> {new_name}")
        else:
            try:
                # Try git mv first, fall back to regular rename
                if staged_only and not git_rename(file_path, new_path):
                    file_path.rename(new_path)
                elif not staged_only:
                    file_path.rename(new_path)
                print(f"✅ Renamed: {original_name} -> {new_name}")
            except OSError as e:
                print(f"⚠️  Skipping: Error renaming {file_path}: {e}")
                skipped.append((file_path, f"rename error: {e}"))

    return changes, skipped


def main():
    parser = argparse.ArgumentParser(description="Convert Python filenames to snake_case")
    parser.add_argument(
        "root_dir",
        nargs="?",
        default=".",
        help="Root directory to search (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without actually renaming",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check only mode - exit with code 1 if non-snake_case files found",
    )
    parser.add_argument("--staged", action="store_true", help="Format only staged git files")

    # Handle the case where pre-commit passes filenames
    args, unknown_args = parser.parse_known_args()

    # If we have unknown args and --check flag, treat unknown args as filenames to check
    if unknown_args and args.check:
        filenames_to_check = unknown_args
    else:
        filenames_to_check = None

    if not os.path.exists(args.root_dir):
        print(f"Error: Directory '{args.root_dir}' does not exist")
        return 1

    try:
        if args.check:
            # Check mode for pre-commit
            if filenames_to_check:
                # Check only the specific files passed by pre-commit
                is_compliant, violations = check_snake_case_compliance(filenames_to_check)
            else:
                # Check all Python files in the repository
                root_path = Path(args.root_dir)
                python_files = [
                    p
                    for p in root_path.rglob("*.py")
                    if not any(part.startswith(".") or part == "__pycache__" for part in p.parts)
                ]
                # Convert to strings for compatibility
                python_files_str = [str(p) for p in python_files]
                is_compliant, violations = check_snake_case_compliance(python_files_str)

            if is_compliant:
                print("✅ All Python filenames are in snake_case")
                return 0
            else:
                print("❌ Python files with non-snake_case names found:")
                for original, expected in violations:
                    print(f"   {original} -> {expected}")
                print(f"\nFound {len(violations)} files that need renaming.")
                print("Run: python scripts/format_to_snake_case.py to fix automatically.")
                return 1
        else:
            # Auto-format mode
            print("Python Filename Formatter - Converting to snake_case")
            print("=" * 50)

            changes, skipped = format_python_files(args.root_dir, args.dry_run, args.verbose, args.staged)

            print("=" * 50)
            if args.dry_run:
                print(f"Dry run complete. Would rename {len(changes)} files.")
                if skipped:
                    print(f"Skipped {len(skipped)} files:")
                    for file_path, reason in skipped:
                        print(f"  {file_path} - {reason}")
                if changes:
                    print("\nTo apply these changes, run without --dry-run")
                    return 1
                return 0
            else:
                print(f"✅ Operation complete. Renamed {len(changes)} files.")
                if skipped:
                    print(f"⚠️  Skipped {len(skipped)} files:")
                    for file_path, reason in skipped:
                        print(f"  {file_path} - {reason}")
                if changes and args.staged:
                    print("\nNote: Files were renamed using 'git mv' and are staged for commit.")
                return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
