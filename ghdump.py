import argparse
import os
import requests
import subprocess

def fetch_repositories(org_name):
    """
    Fetch all repositories for the given organization using the GitHub API.
    """
    base_url = f"https://api.github.com/orgs/{org_name}/repos"
    page = 1
    repositories = []

    print(f"Fetching repositories for organization: {org_name}")
    while True:
        response = requests.get(base_url, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            print(f"Failed to fetch repositories: {response.json().get('message', 'Unknown error')}")
            break

        repos = response.json()
        if not repos:
            break

        repositories.extend(repos)
        page += 1

    return repositories

def clone_repositories(repositories, output_dir):
    """
    Clone each repository into the specified output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.chdir(output_dir)

    for repo in repositories:
        repo_name = repo["name"]
        clone_url = repo["clone_url"]

        if os.path.exists(repo_name):
            print(f"Repository {repo_name} already exists. Skipping...")
        else:
            subprocess.run(["git", "clone", clone_url])

def main():
    parser = argparse.ArgumentParser(description="Clone all repositories from a GitHub organization.")
    parser.add_argument("org", help="Name of the GitHub organization.")
    parser.add_argument(
        "-o", "--output", default="github_org_repos", 
        help="Directory to store cloned repositories (default: github_org_repos)."
    )
    args = parser.parse_args()

    repositories = fetch_repositories(args.org)
    if repositories:
        print(f"Found {len(repositories)} repositories.")
        clone_repositories(repositories, args.output)
    else:
        print(f"No repositories found for organization: {args.org}")

if __name__ == "__main__":
    main()

