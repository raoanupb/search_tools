"""
GitHub Search Examples

Demonstrates how to use the GitHub search tool to find repositories, code,
issues, and users, with ranking by popularity metrics.
"""

from search_tools import GitHubSearch
import os


def demo_repository_search():
    """Demonstrate repository search with popularity ranking."""
    print("=" * 80)
    print("GITHUB REPOSITORY SEARCH")
    print("=" * 80)

    # Get token from environment if available
    token = os.environ.get('GITHUB_TOKEN')
    github = GitHubSearch(token=token)

    # Search for popular Python machine learning repositories
    print("\nSearching for popular Python ML repositories (min 5000 stars)...")
    results = github.search_repositories(
        "machine learning",
        language="python",
        min_stars=5000,
        sort="stars",
        order="desc",
        per_page=5
    )

    print(f"\nFound {results['total_count']:,} repositories total")
    print(f"\nTop 5 results:\n")

    for i, repo in enumerate(results['items'], 1):
        print(f"{i}. {repo['full_name']}")
        print(f"   ⭐ Stars: {repo['stars']:,}")
        print(f"   🔀 Forks: {repo['forks']:,}")
        print(f"   👀 Watchers: {repo['watchers']:,}")
        print(f"   📝 {repo['description'][:100]}...")
        print(f"   🔗 {repo['url']}")
        if repo['topics']:
            print(f"   🏷️  Topics: {', '.join(repo['topics'][:5])}")
        print()

    # Check rate limit
    print(f"Rate limit remaining: {results['rate_limit']['remaining']}/{results['rate_limit']['limit']}")


def demo_code_search():
    """Demonstrate code search."""
    print("\n" + "=" * 80)
    print("GITHUB CODE SEARCH")
    print("=" * 80)

    token = os.environ.get('GITHUB_TOKEN')
    github = GitHubSearch(token=token)

    # Search for specific code patterns
    print("\nSearching for Python transformer implementations...")
    results = github.search_code(
        "class Transformer",
        language="python",
        extension="py",
        per_page=5
    )

    print(f"\nFound {results['total_count']:,} code files total")
    print(f"\nTop 5 results:\n")

    for i, item in enumerate(results['items'], 1):
        repo = item['repository']
        print(f"{i}. {repo['full_name']}/{item['path']}")
        print(f"   ⭐ Repository stars: {repo['stars']:,}")
        print(f"   💻 Language: {repo['language']}")
        print(f"   📝 {repo['description'][:80]}..." if repo['description'] else "")
        print(f"   🔗 {item['url']}")
        print()


def demo_trending_repositories():
    """Demonstrate getting trending repositories."""
    print("\n" + "=" * 80)
    print("GITHUB TRENDING REPOSITORIES")
    print("=" * 80)

    token = os.environ.get('GITHUB_TOKEN')
    github = GitHubSearch(token=token)

    # Get trending Python repositories from the last week
    print("\nGetting trending Python repositories (last 7 days)...")
    trending = github.get_trending_repositories(
        language="python",
        since="weekly"
    )

    print(f"\nTop 10 trending Python repositories:\n")

    for i, repo in enumerate(trending[:10], 1):
        print(f"{i}. {repo['full_name']}")
        print(f"   ⭐ {repo['stars']:,} stars")
        print(f"   📝 {repo['description'][:80]}..." if repo['description'] else "")
        print(f"   📅 Created: {repo['created_at'][:10]}")
        print()


def demo_issue_search():
    """Demonstrate searching for issues (great for finding contribution opportunities)."""
    print("\n" + "=" * 80)
    print("GITHUB ISSUE SEARCH - Finding Contribution Opportunities")
    print("=" * 80)

    token = os.environ.get('GITHUB_TOKEN')
    github = GitHubSearch(token=token)

    # Search for beginner-friendly issues
    print("\nSearching for 'good first issue' in Python projects...")
    results = github.search_issues(
        "language:python",
        state="open",
        labels=["good first issue"],
        sort="created",
        per_page=5
    )

    print(f"\nFound {results['total_count']:,} issues total")
    print(f"\nRecent issues:\n")

    for i, issue in enumerate(results['items'], 1):
        print(f"{i}. #{issue['number']}: {issue['title']}")
        print(f"   📝 State: {issue['state']}")
        print(f"   💬 Comments: {issue['comments']}")
        print(f"   🏷️  Labels: {', '.join(issue['labels'])}")
        print(f"   👤 Created by: {issue['user']['login']}")
        print(f"   🔗 {issue['url']}")
        print()


def demo_user_search():
    """Demonstrate searching for users."""
    print("\n" + "=" * 80)
    print("GITHUB USER SEARCH")
    print("=" * 80)

    token = os.environ.get('GITHUB_TOKEN')
    github = GitHubSearch(token=token)

    # Search for influential machine learning developers
    print("\nSearching for ML developers with 1000+ followers...")
    results = github.search_users(
        "machine learning",
        min_followers=1000,
        sort="followers",
        per_page=5
    )

    print(f"\nFound {results['total_count']:,} users total")
    print(f"\nTop 5 users:\n")

    for i, user in enumerate(results['items'], 1):
        print(f"{i}. {user['login']}")
        print(f"   👥 Followers: {user['followers']:,}")
        print(f"   📚 Public repos: {user['public_repos']}")
        if user['location']:
            print(f"   📍 Location: {user['location']}")
        if user['bio']:
            print(f"   📝 Bio: {user['bio'][:100]}...")
        print(f"   🔗 {user['url']}")
        print()


def demo_repository_details():
    """Demonstrate getting detailed repository information."""
    print("\n" + "=" * 80)
    print("GITHUB REPOSITORY DETAILS")
    print("=" * 80)

    token = os.environ.get('GITHUB_TOKEN')
    github = GitHubSearch(token=token)

    # Get details for a popular repository
    print("\nGetting details for 'huggingface/transformers'...")
    repo = github.get_repository("huggingface", "transformers")

    print(f"\nRepository: {repo['full_name']}")
    print(f"Description: {repo['description']}")
    print(f"⭐ Stars: {repo['stars']:,}")
    print(f"🔀 Forks: {repo['forks']:,}")
    print(f"👀 Watchers: {repo['watchers']:,}")
    print(f"🐛 Open Issues: {repo['open_issues']:,}")
    print(f"💻 Language: {repo['language']}")
    print(f"📜 License: {repo['license']}")
    print(f"🏷️  Topics: {', '.join(repo['topics'][:10])}")
    print(f"📅 Created: {repo['created_at'][:10]}")
    print(f"📅 Updated: {repo['updated_at'][:10]}")
    print(f"🌐 Homepage: {repo['homepage']}")
    print(f"🔗 {repo['url']}")


def demo_advanced_search():
    """Demonstrate advanced search queries."""
    print("\n" + "=" * 80)
    print("GITHUB ADVANCED SEARCH")
    print("=" * 80)

    token = os.environ.get('GITHUB_TOKEN')
    github = GitHubSearch(token=token)

    # Find recently created, popular deep learning repos
    print("\nSearching for recent (2023+) deep learning repos with 100+ stars...")
    results = github.search_repositories(
        "deep learning",
        language="python",
        min_stars=100,
        created_after="2023-01-01",
        sort="stars",
        per_page=5
    )

    print(f"\nFound {results['total_count']:,} repositories")
    print(f"\nTop 5 results:\n")

    for i, repo in enumerate(results['items'], 1):
        print(f"{i}. {repo['full_name']}")
        print(f"   ⭐ {repo['stars']:,} stars (created {repo['created_at'][:10]})")
        print(f"   📝 {repo['description'][:80]}..." if repo['description'] else "")
        print()


def main():
    """Run all GitHub search examples."""
    print("\n")
    print("*" * 80)
    print("GITHUB SEARCH TOOL DEMONSTRATION")
    print("*" * 80)
    print("\nThis script demonstrates GitHub search capabilities with popularity ranking.")
    print("\nNote: Set GITHUB_TOKEN environment variable for higher rate limits.")
    print("Generate token at: https://github.com/settings/tokens\n")

    token = os.environ.get('GITHUB_TOKEN')
    if token:
        print("✓ GitHub token detected - using authenticated requests")
    else:
        print("⚠ No GitHub token - using limited rate limits (60 req/hour)")

    print("\n")

    try:
        # Run demos
        demo_repository_search()
        demo_code_search()
        demo_trending_repositories()
        demo_issue_search()
        demo_user_search()
        demo_repository_details()
        demo_advanced_search()

        print("\n" + "=" * 80)
        print("DEMO COMPLETE")
        print("=" * 80)

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nThis might be due to rate limiting. Try setting GITHUB_TOKEN or wait a bit.")


if __name__ == "__main__":
    main()
