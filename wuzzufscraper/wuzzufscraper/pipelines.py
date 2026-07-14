
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import regex as re
import pymssql


class CleanData:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Company name
        if not adapter.get('company_name'):
            raise DropItem("Missing 'company_name' field")
        adapter['company_name'] = re.sub(r' -', '', adapter['company_name'])

        # Job Title
        if not adapter.get('job_title'):
            raise DropItem("Missing 'job_title' field")
        adapter['job_title'] = adapter['job_title']

        # Search Key Word
        if not adapter.get('search_keyword'):
            raise DropItem("Missing 'search_keyword' field")
        adapter['search_keyword'] = adapter['search_keyword']

        # Location
        if not adapter.get('location'):
            raise DropItem("Missing 'location' field")
        adapter['location'] = re.sub(r',', '', adapter['location'])

        # Technologies
        if not adapter.get('technologies'):
            raise DropItem("Missing 'technologies' field")

        if isinstance(adapter['technologies'], list):
            # Convert list to comma-separated string
            tech_string = ', '.join(str(t) for t in adapter['technologies'])
            adapter['technologies'] = re.sub(r',\s*·\s*,', ',', tech_string)
        else:
            # Handle case where it's already a string
            adapter['technologies'] = re.sub(r',\s*·\s*,', ',', str(adapter['technologies']))

        return item
class MSSQL:
    def __init__(self,db_settings):
        self.db_settings=db_settings

    def from_crawler(cls, crawler):
        return cls(db_settings={
            "server": crawler.settings.get('DESKTOP-B8DNKVM\SQLEXPRESS'),
            "database": crawler.settings.get('ScrappedJob'),
            "user": crawler.settings.get('sa'),
            "password": crawler.settings.get('123456789')
        })

    def open_spider(self, spider):
        self.conn = pymssql.connect(**self.db_settings)
        self.cursor = self.conn.cursor()

    def open_spider(self, spider):
        self.conn = pymssql.connect(**self.db_settings)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute("""
        INSERT INTO jobs (search_keyword, page_number, job_title, company_name, job_location, posted_time , years_of_experience , technologies)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s )
            """, (
        item.get('search_keyword'),
        item.get('page_number'),
        item.get('job_title'),
        item.get('company_name'),
        item.get('job_location'),
        item.get('posted_time'),
        item.get('years_of_experience'),
        item.get('technologies')
         ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
