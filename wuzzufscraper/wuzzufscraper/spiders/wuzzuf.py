import scrapy
import re
import time
import logging
from wuzzufscraper.items import WuzzufJobItem
class WuzzufJobsSpider(scrapy.Spider):
    name = 'wuzzuf_jobs'
    allowed_domains = ['wuzzuf.net']
    keywords = ['software', 'python', 'backend', 'frontend', 'Data scientist', 'Data engineer', 'Machine learning','Ai', 'Cloud', 'Devops', 'full stack', 'Data Analyst', 'Web Application Developer','Mobile Application Developer']
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 5,
        'COOKIES_ENABLED': True,
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    def start_requests(self):
        for keyword in self.keywords:
            url = f'https://wuzzuf.net/search/jobs/?q={keyword}&a=navbg'
            yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword, 'page': 0})
    def parse(self, response):
        keyword = response.meta['keyword']
        page_number = response.meta['page'] + 1
        job_listings = response.css('div.css-1gatmva')
        self.logger.info(f"Scraping '{keyword}' - Page {page_number} - {response.url}")
        self.logger.info(f"Found {len(job_listings)} job listings.")
        if not job_listings:
            self.logger.info(f"No listings found for '{keyword}' on page {page_number}. Done with this keyword.")
            return
        for job in job_listings:
            job_title = job.css('h2.css-m604qf a::text').get()
            if job_title:
                job_title = job_title.strip()
            company_name = job.css('a.css-17s97q8::text').get()
            if company_name:
                company_name = company_name.strip()
            location = job.css('span.css-5wys0k::text').get()
            if location:
                location = location.strip()
            posted_time = job.css('div.css-do6t5g::text').get()
            if posted_time:
                posted_time = posted_time.strip()
            years_of_exp = None
            exp_level = job.css('div.css-y4udm8 a::text').get()
            if exp_level:
                exp_level = exp_level.strip()
                self.logger.debug(f"Experience level: {exp_level}")
            all_text = ' '.join(job.css('*::text').getall())
            yrs_pattern = re.search(r'(\d+)\s*-\s*(\d+)\s*Yrs\s*of\s*Exp', all_text, re.IGNORECASE)
            if yrs_pattern:
                min_exp = yrs_pattern.group(1)
                max_exp = yrs_pattern.group(2)
                years_of_exp = f"{min_exp}-{max_exp} years"
            else:
                yrs_pattern = re.search(r'(\d+)\s*-\s*(\d+)\s*[Yy](?:ea)?rs?', all_text)
                if yrs_pattern:
                    min_exp = yrs_pattern.group(1)
                    max_exp = yrs_pattern.group(2)
                    years_of_exp = f"{min_exp}-{max_exp} years"
                else:
                    yrs_pattern = re.search(r'(\d+)\+?\s*[Yy](?:ea)?rs?', all_text)
                    if yrs_pattern:
                        min_exp = yrs_pattern.group(1)
                        years_of_exp = f"{min_exp}+ years"
            if not years_of_exp and exp_level:
                if exp_level.lower() == 'entry level':
                    years_of_exp = "0-2 years"
                elif exp_level.lower() == 'experienced':
                    years_of_exp = "3+ years"
                elif exp_level.lower() == 'manager':
                    years_of_exp = "5+ years"
                elif exp_level.lower() == 'senior':
                    years_of_exp = "7+ years"
            technologies = []
            tech_elements = job.css('a.css-5x9pm1::text').getall()
            for tech in tech_elements:
                tech = tech.strip()
                if tech and tech not in ['.', '...', ',', '-']:
                    technologies.append(tech)

            job_item = WuzzufJobItem(
                search_keyword=keyword,
                page_number=page_number,
                job_title=job_title,
                company_name=company_name,
                location=location,
                posted_time=posted_time,
                years_of_experience=years_of_exp,
                technologies=technologies,
            )
            yield job_item
        next_start = page_number
        next_url = f"https://wuzzuf.net/search/jobs/?q={keyword}&a=navbg&start={next_start}"
        self.logger.info(f"Scheduling next page for '{keyword}': {next_url}")
        time.sleep(10)
        yield scrapy.Request(
            url=next_url,
            callback=self.parse,
            meta={'keyword': keyword, 'page': page_number},
            headers={'Referer': response.url}
        )