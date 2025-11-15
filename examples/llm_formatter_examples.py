"""
LLM Formatter Examples

Demonstrates how to use the markdown formatters to convert search results
into LLM-friendly format for prompt injection.

These formatters make it easy to inject search results into LLM prompts for
context-aware responses and agent workflows.
"""

from search_tools import (
    ArxivSearch,
    GitHubSearch,
    WikipediaSearch,
    ArxivFormatter,
    GitHubFormatter,
    WikipediaFormatter,
    YahooFinanceFormatter,
    AlphaVantageFormatter,
    FinancialNewsFormatter,
    format_arxiv_results,
    format_github_repos,
    format_stock_quote,
)


def demo_arxiv_formatter():
    """Demonstrate formatting Arxiv results for LLM prompts."""
    print("=" * 80)
    print("ARXIV FORMATTER - Convert Search Results to Markdown")
    print("=" * 80)

    # Search for papers
    arxiv = ArxivSearch()
    results = arxiv.search("large language models", max_results=3)

    # Format for LLM
    markdown = ArxivFormatter.format_results(results, query="large language models")

    # Or use the convenience function
    # markdown = format_arxiv_results(results, query="large language models")

    print("\n" + markdown)

    # Example: How you might use this in an LLM prompt
    llm_prompt = f"""Based on the following research papers, provide a summary of recent developments in large language models:

{markdown}

Please synthesize the key findings and methodologies from these papers."""

    print("\n" + "=" * 80)
    print("EXAMPLE LLM PROMPT")
    print("=" * 80)
    print(llm_prompt[:500] + "...\n")


def demo_github_formatter():
    """Demonstrate formatting GitHub results for LLM prompts."""
    print("\n" + "=" * 80)
    print("GITHUB FORMATTER - Convert Repository Results to Markdown")
    print("=" * 80)

    # Search for repositories
    github = GitHubSearch()
    results = github.search_repositories(
        "machine learning",
        language="python",
        min_stars=10000,
        per_page=3
    )

    # Format for LLM
    markdown = GitHubFormatter.format_repository_results(
        results,
        query="machine learning"
    )

    # Or use the convenience function
    # markdown = format_github_repos(results, query="machine learning")

    print("\n" + markdown)

    # Example LLM prompt
    llm_prompt = f"""Based on these popular machine learning repositories, recommend the best one for a beginner to start learning:

{markdown}

Consider factors like documentation, community support, and learning curve."""

    print("\n" + "=" * 80)
    print("EXAMPLE LLM PROMPT")
    print("=" * 80)
    print(llm_prompt[:500] + "...\n")


def demo_wikipedia_formatter():
    """Demonstrate formatting Wikipedia results for LLM prompts."""
    print("\n" + "=" * 80)
    print("WIKIPEDIA FORMATTER - Convert Articles to Markdown")
    print("=" * 80)

    # Search Wikipedia
    wiki = WikipediaSearch()
    results = wiki.search("quantum computing", limit=3)

    # Format for LLM
    markdown = WikipediaFormatter.format_results(results, query="quantum computing")

    print("\n" + markdown)

    # Get a page summary
    summary = wiki.get_page_summary("Quantum computing")
    if summary:
        summary_md = WikipediaFormatter.format_page_summary(summary)

        llm_prompt = f"""Using the following Wikipedia article, explain quantum computing to a 12-year-old:

{summary_md}

Keep the explanation simple and use analogies."""

        print("\n" + "=" * 80)
        print("EXAMPLE LLM PROMPT WITH SUMMARY")
        print("=" * 80)
        print(llm_prompt[:500] + "...\n")


def demo_stock_market_formatters():
    """Demonstrate formatting stock market data for LLM prompts."""
    print("\n" + "=" * 80)
    print("STOCK MARKET FORMATTERS - Financial Data for LLMs")
    print("=" * 80)

    try:
        from search_tools import YahooFinanceSearch

        yf = YahooFinanceSearch()

        # Get quote
        quote = yf.get_quote("AAPL")
        quote_md = YahooFinanceFormatter.format_quote(quote)

        print("\nStock Quote (Markdown):")
        print(quote_md)

        # Get company info
        info = yf.get_company_info("AAPL")
        info_md = YahooFinanceFormatter.format_company_info(info)

        print("\nCompany Information (Markdown):")
        print(info_md)

        # Compare stocks
        comparison = yf.compare_stocks(['AAPL', 'MSFT', 'GOOGL'])
        comparison_md = YahooFinanceFormatter.format_comparison(comparison)

        print("\nStock Comparison (Markdown):")
        print(comparison_md)

        # Example LLM prompt
        llm_prompt = f"""Based on the following stock comparison, which company represents the best value investment?

{comparison_md}

Consider P/E ratio, market cap, and dividend yield in your analysis."""

        print("\n" + "=" * 80)
        print("EXAMPLE LLM PROMPT")
        print("=" * 80)
        print(llm_prompt + "\n")

    except ImportError:
        print("\nYahooFinanceSearch not available. Install yfinance: pip install yfinance\n")


def demo_combined_search_and_format():
    """Demonstrate combining multiple search results for comprehensive LLM context."""
    print("\n" + "=" * 80)
    print("COMBINED SEARCH - Multi-Source Context for LLMs")
    print("=" * 80)

    topic = "transformer architecture"

    # Gather information from multiple sources
    arxiv = ArxivSearch()
    github = GitHubSearch()
    wiki = WikipediaSearch()

    # Search each source
    papers = arxiv.search(topic, max_results=2)
    repos = github.search_repositories(topic, language="python", per_page=2)
    wiki_results = wiki.search(topic, limit=2)

    # Format each result
    papers_md = ArxivFormatter.format_results(papers, query=topic)
    repos_md = GitHubFormatter.format_repository_results(repos, query=topic)
    wiki_md = WikipediaFormatter.format_results(wiki_results, query=topic)

    # Create comprehensive LLM prompt
    llm_prompt = f"""# Research Assistant: {topic.title()}

I've gathered information from multiple sources to help you understand {topic}:

## Academic Papers
{papers_md}

## Code Repositories
{repos_md}

## General Knowledge
{wiki_md}

Based on all this information, please:
1. Explain what {topic} is and why it's important
2. Summarize the key innovations from the research papers
3. Recommend which GitHub repository would be best for learning
4. Suggest practical applications of this technology
"""

    print("\n" + "=" * 80)
    print("COMPREHENSIVE LLM PROMPT")
    print("=" * 80)
    print(llm_prompt[:1000] + "...\n")


def demo_real_world_agent_workflow():
    """Demonstrate a real-world agent workflow using formatters."""
    print("\n" + "=" * 80)
    print("REAL-WORLD AGENT WORKFLOW")
    print("=" * 80)

    print("""
This example shows how a language agent might use these formatters:

1. USER: "I want to learn about quantum computing"

2. AGENT: Searches multiple sources
   - Arxiv for academic papers
   - GitHub for code examples
   - Wikipedia for overview

3. AGENT: Formats results with appropriate formatters

4. AGENT: Injects formatted context into its prompt

5. AGENT: Generates informed response with citations

Example code:
""")

    code_example = """
# Agent workflow
user_query = "quantum computing"

# Step 1: Gather information
arxiv = ArxivSearch()
github = GitHubSearch()
wiki = WikipediaSearch()

papers = arxiv.search(user_query, max_results=5)
repos = github.search_repositories(user_query, language="python", per_page=5)
articles = wiki.search(user_query, limit=3)

# Step 2: Format for LLM
papers_md = format_arxiv_results(papers, query=user_query)
repos_md = format_github_repos(repos, query=user_query)
wiki_md = WikipediaFormatter.format_results(articles, query=user_query)

# Step 3: Create context-aware prompt
system_prompt = f\"\"\"You are a research assistant helping someone learn about {user_query}.
Use the following sources to provide accurate, well-cited information:

{papers_md}
{repos_md}
{wiki_md}
\"\"\"

# Step 4: Send to LLM
# response = llm.generate(system_prompt, user_query)
"""

    print(code_example)

    print("""
Benefits of this approach:
✓ LLM has access to current, accurate information
✓ Responses can cite specific sources
✓ Information is well-structured and easy to parse
✓ Supports multi-source fact-checking
✓ Enables complex research workflows
""")


def main():
    """Run all formatter demonstrations."""
    print("\n")
    print("*" * 80)
    print("LLM FORMATTER DEMONSTRATIONS")
    print("*" * 80)
    print("\nThese examples show how to convert search results into markdown")
    print("format suitable for injecting into LLM prompts.\n")

    try:
        # Run demos
        demo_arxiv_formatter()
        demo_github_formatter()
        demo_wikipedia_formatter()
        demo_stock_market_formatters()
        demo_combined_search_and_format()
        demo_real_world_agent_workflow()

        print("\n" + "=" * 80)
        print("DEMO COMPLETE")
        print("=" * 80)
        print("\nKey Takeaways:")
        print("1. Each search tool has a corresponding formatter")
        print("2. Formatters convert structured data to markdown")
        print("3. Markdown is easy for LLMs to parse and understand")
        print("4. Combine multiple sources for comprehensive context")
        print("5. Use formatters to build intelligent agent workflows")
        print("\n")

    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
