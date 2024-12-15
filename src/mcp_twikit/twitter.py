from fastmcp import FastMCP, Context
import twikit
import os
from pathlib import Path
import logging

# Create an MCP server
mcp = FastMCP("mcp-twikit")
logger = logging.getLogger(__name__)
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

USERNAME = os.getenv('TWITTER_USERNAME')
EMAIL = os.getenv('TWITTER_EMAIL')
PASSWORD = os.getenv('TWITTER_PASSWORD')
USER_AGENT = os.getenv('USER_AGENT')
COOKIES_PATH = Path.home() / '.mcp-twikit' / 'cookies.json'

# Add an addition tool
@mcp.tool()
async def search_twitter(query: str, sort_by: str = 'Top', count: int = 10, ctx: Context = None) -> str:
    """Search twitter with a query. Sort by 'Top' or 'Latest'"""
    client = twikit.Client('en-US', user_agent=USER_AGENT)
    logger.info(f"Searching for {query} with sort_by {sort_by} and count {count}")
    if COOKIES_PATH.exists():
        logger.info(f"Loading cookies from {COOKIES_PATH}")
        client.load_cookies(COOKIES_PATH)
    else:
        try:
            logger.info(f"Logging in with {USERNAME} and {EMAIL} and {PASSWORD}")
            await client.login(
                auth_info_1=USERNAME,
                auth_info_2=EMAIL,
                password=PASSWORD
            )
        except Exception as e:
            logger.error(f"Failed to login: {e}")
            return "Failed to login: {e}"
        COOKIES_PATH.parent.mkdir(parents=True, exist_ok=True)
        client.save_cookies(COOKIES_PATH)

    try:
        tweets = await client.search_tweet(query, product=sort_by, count=count)
        return convert_tweets_to_markdown(tweets)
    except Exception as e:
        logger.error(f"Failed to search tweets: {e}")
        return "Failed to search tweets: {e}"

def convert_tweets_to_markdown(tweets: list[twikit.Tweet]) -> str:
    markdown_tweets = []
    for tweet in tweets:
        tweet_text = f"**@{tweet.user.screen_name}** - {tweet.created_at}\n{tweet.text}"
        markdown_tweets.append(tweet_text)
    return '\n\n'.join(markdown_tweets)
