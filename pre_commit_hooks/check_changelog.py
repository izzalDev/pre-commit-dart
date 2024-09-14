#!/usr/bin/env python3
import re
import sys

# Path to pubspec.yaml and CHANGELOG.md
pubspec_file = "pubspec.yaml"
changelog_file = "CHANGELOG.md"

# Function to extract the current version from pubspec.yaml
def get_current_version(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('version:'):
                    return line.split()[1]
    except FileNotFoundError:
        print(f"File not found: {filename}")
        sys.exit(1)
    return None

# Function to normalize version format
def normalize_version(version):
    return re.sub(r'^v|[\+].*', '', version)

# Function to check if there's a corresponding changelog entry
def check_changelog_entry(version, filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            # Pattern to match both `## [1.0.0]` and `## 1.0.0`
            pattern = rf"##\s*(?:\[\s*{re.escape(version)}\s*\]|\s*{re.escape(version)})"
            return re.search(pattern, content) is not None
    except FileNotFoundError:
        print(f"File not found: {filename}")
        sys.exit(1)

# Main logic
current_version = get_current_version(pubspec_file)

if current_version is None:
    print(f"Version not found in {pubspec_file}")
    sys.exit(1)

normalized_version = normalize_version(current_version)

if check_changelog_entry(normalized_version, changelog_file):
    print(f"Changelog entry found for version {current_version}.")
else:
    print(f"No changelog entry found for version {current_version} in {changelog_file}.")
    sys.exit(1)
