# MCP-Twikit

A Model Context Protocol (MCP) server for Twitter search.

## Installation

```json
{
    "mcpServer": {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/adhikasp/mcp-twikit", "mcp-twikit"],
        "env": {
            "TWITTER_USERNAME": "@example",
            "TWITTER_EMAIL": "me@example.com",
            "TWITTER_PASSWORD": "secret",
        }
    }
}
```

## Example usage

Using [mcp-client-cli](https://github.com/adhikasp/mcp-client-cli)

```
$ llm compare 10 latest tweet from @IndiHomeCare, @di_cbn, @BiznetHome, @ID_MyRepublic. 
What are interesting promo or news coming from them?

Based on the latest tweets, here's a summary of interesting promos and news:

1. MyRepublic (@ID_MyRepublic):
   - Recent Promo: "Double Date 12.12" offer
     * 100 Mbps internet for Rp275,000 per person per month
     * Ideal for sharing with a partner, friend, or family
   - Expansion News: Launched service in Manado and 11 other cities
   - Offering internet speeds up to 500 Mbps

2. IndiHome (@IndiHomeCare):
   - Mostly customer service interactions
   - Mentions of billing adjustments starting from December
   - No specific promos visible in recent tweets

3. CBN (@di_cbn):
   - Primarily focused on customer support
   - Responding to individual customer issues via DM
   - No visible promos or major news

4. Biznet (@BiznetHome):
   - Primarily handling customer support
   - Asking customers to send direct messages for network issue investigations
   - No specific promos or news highlighted

The most interesting content comes from MyRepublic, with their "Double Date 12.12" promo and expansion to new cities. The other providers seem to be primarily focused on customer support and resolving individual customer issues.

Would you like me to dive deeper into any of these tweets or provide more context about the promos?
```