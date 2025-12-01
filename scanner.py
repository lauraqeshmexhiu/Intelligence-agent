"""
Repository Scanner Module
Scans Git repositories and extracts metadata
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from git import Repo
from collections import Counter


class RepositoryScanner:
    """Scans a Git repository and extracts metadata"""
    
    def __init__(self, repo_path):
        """
        Initialize scanner with a repository path
        
        Args:
            repo_path: Path to the Git repository
        """
        self.repo_path = Path(repo_path)
        self.repo = Repo(repo_path)
        self.metadata = {}
        
    def scan(self):
        """
        Perform a full scan of the repository
        
        Returns:
            dict: Metadata about the repository
        """
        print(f"Scanning repository: {self.repo_path.name}")
        
        self.metadata = {
            "name": self.repo_path.name,
            "path": str(self.repo_path.absolute()),
            "languages": self._count_languages(),
            "loc_total": 0,  # Will be calculated
            "commits_last_30_days": self._count_recent_commits(),
            "top_authors": self._get_top_authors(),
            "has_readme": self._check_file_exists("README.md"),
            "has_claude": self._check_file_exists("CLAUDE.md"),
            "has_license": self._check_file_exists("LICENSE") or self._check_file_exists("LICENSE.md"),
            "has_tests": self._check_tests(),
            "has_ci": self._check_ci(),
            "has_dockerfile": self._check_file_exists("Dockerfile"),
        }
        
        # Calculate total lines of code
        self.metadata["loc_total"] = sum(self.metadata["languages"].values())
        
        return self.metadata
    
    def _check_file_exists(self, filename):
        """Check if a specific file exists in the repository root"""
        return (self.repo_path / filename).exists()
    
    def _check_tests(self):
        """Check if tests exist in the repository"""
        # Check for tests/ directory
        if (self.repo_path / "tests").exists():
            return True
        
        # Check for test/ directory
        if (self.repo_path / "test").exists():
            return True
        
        # Check for files containing _test or test_
        for root, dirs, files in os.walk(self.repo_path):
            # Skip hidden directories and venv
            if any(part.startswith('.') or part == 'venv' for part in Path(root).parts):
                continue
            
            for file in files:
                if '_test' in file or 'test_' in file:
                    return True
        
        return False
    
    def _check_ci(self):
        """Check if GitHub Actions workflows exist"""
        ci_path = self.repo_path / ".github" / "workflows"
        return ci_path.exists() and any(ci_path.iterdir())
    
    def _count_languages(self):
        """
        Count lines of code by language
        
        Returns:
            dict: Language -> line count mapping
        """
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.c': 'C',
            '.cpp': 'C++',
            '.cs': 'C#',
            '.sh': 'Shell',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.json': 'JSON',
            '.md': 'Markdown',
        }
        
        language_counts = Counter()
        
        # Special case for Dockerfile
        dockerfile_path = self.repo_path / "Dockerfile"
        if dockerfile_path.exists():
            try:
                with open(dockerfile_path, 'r', encoding='utf-8', errors='ignore') as f:
                    language_counts['Dockerfile'] = len(f.readlines())
            except Exception:
                pass
        
        # Walk through repository files
        for root, dirs, files in os.walk(self.repo_path):
            # Skip hidden directories, git, and virtual environments
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', 'node_modules', '__pycache__']]
            
            for file in files:
                file_path = Path(root) / file
                extension = file_path.suffix.lower()
                
                if extension in language_map:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len([line for line in f if line.strip()])  # Count non-empty lines
                            language_counts[language_map[extension]] += lines
                    except Exception:
                        # Skip files that can't be read
                        continue
        
        return dict(language_counts)
    
    def _count_recent_commits(self, days=30):
        """
        Count commits in the last N days
        
        Args:
            days: Number of days to look back
            
        Returns:
            int: Number of commits
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Efficiently count commits after the cutoff date
        commit_list = list(self.repo.iter_commits(after=cutoff_date))
        return len(commit_list)
    
    def _get_top_authors(self, limit=3):
        """
        Get the top N commit authors
        
        Args:
            limit: Number of top authors to return
            
        Returns:
            list: Top author names
        """
        author_counts = Counter()
        
        for commit in self.repo.iter_commits():
            author_counts[commit.author.name] += 1
        
        return [author for author, count in author_counts.most_common(limit)]
    
    def save_metadata(self, output_dir):
        """
        Save metadata to a JSON file
        
        Args:
            output_dir: Directory to save the metadata file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filename = f"{self.metadata['name']}.json"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2)
        
        print(f"Saved metadata to: {filepath}")


def scan_directory(repos_dir, output_dir):
    """
    Scan all repositories in a directory
    
    Args:
        repos_dir: Directory containing Git repositories
        output_dir: Directory to save metadata files
    """
    repos_path = Path(repos_dir)
    
    if not repos_path.exists():
        print(f"Error: Directory {repos_dir} does not exist")
        return
    
    # Find all Git repositories
    repos = []
    for item in repos_path.iterdir():
        if item.is_dir() and (item / ".git").exists():
            repos.append(item)
    
    if not repos:
        print(f"No Git repositories found in {repos_dir}")
        return
    
    print(f"Found {len(repos)} repositories to scan\n")
    
    # Scan each repository
    for repo_path in repos:
        try:
            scanner = RepositoryScanner(repo_path)
            scanner.scan()
            scanner.save_metadata(output_dir)
            print()  # Empty line for readability
        except Exception as e:
            print(f"Error scanning {repo_path.name}: {str(e)}\n")
            continue