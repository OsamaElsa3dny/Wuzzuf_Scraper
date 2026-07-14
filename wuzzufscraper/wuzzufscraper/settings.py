
BOT_NAME = "wuzzufscraper"

SPIDER_MODULES = ["wuzzufscraper.spiders"]
NEWSPIDER_MODULE = "wuzzufscraper.spiders"

ITEM_PIPELINES = {
    'wuzzufscraper.pipelines.CleanData': 100,  # Runs first
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 2
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
FEED_FORMAT = 'csv'
FEED_URI = 'wuzzuf_jobs.csv'
