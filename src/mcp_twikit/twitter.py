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

async def get_twitter_client() -> twikit.Client:
    """Initialize and return an authenticated Twitter client."""
    client = twikit.Client('en-US', user_agent=USER_AGENT)
    
    if COOKIES_PATH.exists():
        client.load_cookies(COOKIES_PATH)
    else:
        try:
            await client.login(
                auth_info_1=USERNAME,
                auth_info_2=EMAIL,
                password=PASSWORD
            )
        except Exception as e:
            logger.error(f"Failed to login: {e}")
            raise
        COOKIES_PATH.parent.mkdir(parents=True, exist_ok=True)
        client.save_cookies(COOKIES_PATH)
    
    return client

# Add an addition tool
@mcp.tool()
async def search_twitter(query: str, sort_by: str = 'Top', count: int = 10, ctx: Context = None) -> str:
    """Search twitter with a query. Sort by 'Top' or 'Latest'"""
    try:
        client = await get_twitter_client()
        tweets = await client.search_tweet(query, product=sort_by, count=count)
        return convert_tweets_to_markdown(tweets)
    except Exception as e:
        logger.error(f"Failed to search tweets: {e}")
        return f"Failed to search tweets: {e}"

@mcp.tool()
async def get_user_tweets(username: str, tweet_type: str = 'Tweets', count: int = 10, ctx: Context = None) -> str:
    """Get tweets from a specific user's timeline.
    
    Args:
        username: Twitter username (with or without @)
        tweet_type: Type of tweets to retrieve - 'Tweets', 'Replies', 'Media', or 'Likes'
        count: Number of tweets to retrieve (default 10)
    """
    
    try:
        client = await get_twitter_client()
        
        # Remove @ if present in username
        username = username.lstrip('@')
        
        # First get user ID from screen name
        user = await client.get_user_by_screen_name(username)
        if not user:
            return f"Could not find user {username}"
            
        # Then get their tweets
        tweets = await client.get_user_tweets(
            user_id=user.id,
            tweet_type=tweet_type,
            count=count
        )
        return convert_tweets_to_markdown(tweets)
    except Exception as e:
        logger.error(f"Failed to get user tweets: {e}")
        return f"Failed to get user tweets: {e}"

@mcp.tool()
async def get_timeline(count: int = 20) -> str:
    """Get tweets from your home timeline (For You).
    
    Args:
        count: Number of tweets to retrieve (default 20)
    """
    try:
        client = await get_twitter_client()
        tweets = await client.get_timeline(count=count)
        return convert_tweets_to_markdown(tweets)
    except Exception as e:
        logger.error(f"Failed to get timeline: {e}")
        return f"Failed to get timeline: {e}"

@mcp.tool() 
async def get_latest_timeline(count: int = 20) -> str:
    """Get tweets from your home timeline (Following).
    
    Args:
        count: Number of tweets to retrieve (default 20)
    """
    try:
        client = await get_twitter_client()
        tweets = await client.get_latest_timeline(count=count)
        return convert_tweets_to_markdown(tweets)
    except Exception as e:
        logger.error(f"Failed to get latest timeline: {e}")
        return f"Failed to get latest timeline: {e}"


def convert_tweets_to_markdown(tweets: list[twikit.Tweet]) -> str:
    markdown_tweets = []
    for tweet in tweets:
        tweet_text = f"**@{tweet.user.screen_name}** - {tweet.created_at}\n{tweet.text}"
        markdown_tweets.append(tweet_text)
    return '\n\n'.join(markdown_tweets)
