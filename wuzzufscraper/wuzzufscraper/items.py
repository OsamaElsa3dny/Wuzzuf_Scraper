import scrapy

class WuzzufJobItem(scrapy.Item):
    search_keyword = scrapy.Field()
    page_number = scrapy.Field()
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    posted_time = scrapy.Field()
    years_of_experience = scrapy.Field()
    technologies = scrapy.Field()
