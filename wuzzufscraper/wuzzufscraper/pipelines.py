# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import regex as re
import pymssql
class CleanData:
    def process_item(self, item, spider):
        '''
        Checking the existence of each parameter for each item, if not found , an exception will be raised,
        otherwise,pre-processing will be made to ensure validation.
        '''
        # Job Title
        if(not item.get('job_title')):
            raise DropItem("Missing 'job title' field")
        item['job_title']=item['job_title'].strip()
        item['job_title']=item['job_title'].astype(str)
        # Search Key Word
        if (not item.get('search_keyword')):
            raise DropItem("Missing 'search_keyword' field")
        item['search_keyword']=item['search_keyword'].strip()
        item['search_keyword']=item['search_keyword'].astype(str)
        # Location
        if (not item.get('location')):
            raise DropItem("Missing 'location' field")
        item['location'] = item['location'].strip()
        item['location'] = item['location'].astype(str)
        # Page Number
        page_number=re.findall(r'\d',item['page_number'])
        if (len(page_number)==0):
            raise DropItem("Missing 'page_number' field")
        item['page_number'] = page_number
        # Posted Time
        number=re.findall(r'\d',item['posted_time'])[0]
        month_day=re.findall(r'\b[a-zA-Z]+\b',item['posted_time'])[0]
        if (len(number)==0 or len(month_day)==0):
            raise DropItem("Missing 'posted_time' field")
        item['posted_time']=number*(30**(month_day=='month'))
        # Years of experience
        years = re.findall(r'\d+',item['years_of_experience'])
        if(len(years)==0):
            raise DropItem("Missing 'years_of_experience' field")
        item['years_of_experience'] = years[0]
        # Technologies
        if (not item.get('technologies')):
            raise DropItem("Missing 'technologies' field")
        item['technologies'] = item['technologies'].strip()
        item['technologies'] = item['technologies'].astype(str)
        return item
    class MSSQL:
        def __init__(self,db_settings):
            self.db_settings=db_settings

        def from_crawler(cls, crawler):
            # Before running make sure to change this into your own server and database credentials , or don't use this class
            # if you don't want to save the data into your own database server (recommended) as it has no use anymore.
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