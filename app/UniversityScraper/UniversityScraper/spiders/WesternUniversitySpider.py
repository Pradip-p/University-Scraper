# -*- coding: utf-8 -*-
import scrapy
from UniversityScraper.items import UniversityItem
import logging, re, traceback

import requests
from lxml import html


class WesternUniversitySpider(scrapy.Spider):
	name = 'WesternUniversitySpider'
	allowed_domains = ['grad.uwo.ca']
	start_urls = ['https://grad.uwo.ca/admissions/programs/index.cfm']

	def parse(self, response):
		all_programs = response.xpath("//table[@class='no-borders']/tr/td[1]/ul[@class='squarelist']/li/a/@href").extract()
		logging.info("western_university: Scraping Started; URL: {}".format(response.url))
		for course in all_programs:
			course_url = 'https://grad.uwo.ca/admissions/programs/' + str(course) #Because href format: href="program.cfm?p=135"
			yield scrapy.Request(course_url, callback=self.parse_course)

	def parse_course(self, response):
		logging.info("western_university: Scraping Course page; URL: {}".format(response.url))
		try:
			item = UniversityItem()
			#1 CourseName
			course_name = response.xpath("//*[@id='lowlevel']/div[3]/h1/text()").extract_first()
			item['course_name'] = course_name

			#4 Course Website
			course_website = response.url
			item['course_website'] = course_website
			
			# Duration & Duration Term
			duration_words = response.xpath('//h2[contains(text(), "Program Length")]/following-sibling::ul[1]/li[1]/text()').extract_first()
			if duration_words: #Expected format: "12 Terms (4 years)"
				words = ['years', 'semesters', 'trimesters', 'months', 'weeks', 'days', 'hours', \
					'year', 'semester', 'trimester', 'month', 'week', 'day', 'hour']
				a = re.findall("\d+\s\w+|\d+.\d+\s\w+", duration_words)
				dur = ()
				for i in a:
					x = i.split(' ')
					if len(x) == 2 and str(x[1]).lower() in words: #If this format: ['4', 'years'] 
						dur = (x[1], x[0]) # ('year', 1)
					elif len(x) == 2 and str(x[1]).lower() in ['term', 'terms']: #if this format: ['12', 'Terms']
						dur = (x[1], x[0])
				if len(dur) == 2:
					#5 Duration
					item['duration'] = dur[1]
					#6 Duration Term
					item['duration_term'] = dur[0]

			#7 Study mode: N/A in course page. Only study load present

			#8 Degree Level
			degree_level = response.xpath("//*[@id='lowlevel']/div[3]/strong/text()").extract_first()
			item['degree_level'] = degree_level

			#12 Apply Day
			check = response.xpath('//h2[contains(text(), "Application Deadline")]/text()').extract_first()
			if check: #Application deadline section is present
				apply_day = ''
				a = response.xpath('//h2[contains(text(), "Application Deadline")]/following-sibling::ul[1]/li/strong/text()').extract()
				b = response.xpath('//h2[contains(text(), "Application Deadline")]/following-sibling::ul[1]/li/text()').extract()
				if a: #if in this format: <li><strong>January 1</strong></li>
					if len(a) == 1:
						apply_day = a[0]
					else:
						apply_day = ','.join(a)
				else:
					if b: #if in this format: <li>January 1</li>
						if len(b) == 1:
							apply_day = b[0]
						else:
							apply_day = ','.join(b)

				c = re.findall("\w+\s*\d{1,2}", apply_day)
				if c:
					days = '' 
					months = ''
					x = list(set(c)) #To avoid repeatition
					for i in x: #['February 28', 'March 30'] or just ['January 31']
						l = i.split(' ')
						if len(l) == 2:
							months = str(l[0]) + ',' + months
							days = str(l[1]) + ',' + days

					#12 Apply day
					item['apply_day'] = days						
					#13 Apply month
					item['apply_month'] = months
							
			#Fee structures
			fee_str = self._get_fee_structure(course_name)
			if fee_str:
				#16 International Fee
				item['international_fee']= fee_str.get('int')

				#17 Domestic Fee
				item['domestic_fee'] = fee_str.get('dom')

				#18 Fee Term
				item['fee_term'] = fee_str.get('term')

			#20 Currency
			item['currency'] = "CAD"
			
			#21 Study Load 
			loads = response.xpath("//h2[contains(text(), 'Program Design')]/following-sibling::ul[1]/li/text()").extract()
			match = ""
			for i in loads:
				clean_i = str(i.strip()).lower()
				full = re.search("full-time|full time", clean_i)
				part = re.search("|part-time|part time", clean_i)
				if full:
					full = full.group(0)
				if part:
					part = part.group(0)
				if full and part:
					match = "both"
				elif full:
					match = full
				elif part:
					match = part
				else:
					continue
			if match:
				item['study_load'] = match

			#22 to 36: toefl and IELTS
			eng_url = "https://grad.uwo.ca/admissions/international.html"
			eng = self._get_english_req(eng_url)
			ielts = eng.get('ielts')
			toefl = eng.get('toefl')

			#22 IELTS Listening
			item["ielts_listening"] = ielts.get('listening')

			#23 IELTS Speaking
			item["ielts_speaking"] = ielts.get('speaking')

			#24 IELTS Writing
			item["ielts_writing"] = ielts.get('writing')

			#25 IELTS Reading
			item["ielts_reading"] = ielts.get('reading')

			#26 IELTS Overall
			item["ielts_overall"] = ielts.get('overall')

			#27 to 31 PTE Not found in the english requirement link

			#32 toefl Listening
			item["toefl_listening"] = toefl.get('listening')

			#33 toefl Speaking
			item["toefl_speaking"] = toefl.get('speaking')

			#34 toefl Writing
			item["toefl_writing"] = toefl.get('writing')

			#35 toefl Reading
			item["toefl_reading"] = toefl.get('reading')

			#36 toefl Overall
			item["toefl_overall"] = toefl.get('overall')

			#50 Course Description
			desc = response.xpath("//div[@class='grey-box']/following-sibling::p[1]/text()").extract()
			item['course_description'] = ' '.join(desc)

			#52 Career: Not found in any course pages			
			yield item			

		except Exception as ex:
			logging.error("western_university; msg=Crawling Failed; URL= %s;Error=%s",response.url,traceback.format_exc())


	def _get_english_req(self, eng_url):
		'''
		Params: URL to the english requirement page
		Returns: Dict that contains inner dict with 'toefl' and 'ielts' keys
		'''
		page = requests.get(eng_url)
		response = html.fromstring(page.content)
		eng = {}
		#toefl data
		try:
			toefl_text = response.xpath("//ul[@class='squarelist'][1]/li[1]")[0].text_content()
			toefls = re.findall("\d+", toefl_text)			
			toefl_o = toefls[0]
			toefls_a = toefls[1]
			eng['toefl'] = {
				'listening': toefls_a,
				'speaking': toefls_a,
				'writing': toefls_a,
				'reading': toefls_a,
				'overall': toefl_o,
			}
		except Exception as ex:
			logging.error("western_university: Cannot fetch toefl: {}".format(ex))
		#IELTS Data
		try:
			ielts_text = response.xpath("//ul[@class='squarelist'][1]/li[2]")[0].text_content()
			ielts = re.findall('\d+.\d+|\d+', ielts_text)
			i = ielts[0]
			eng['ielts'] = {
				'listening': i,
				'speaking': i,
				'writing': i,
				'reading': i,
				'overall': i,
			}
		except Exception as ex:
			logging.error("western_university: Cannot fetch IELTS: {}".format(ex))					
		return eng	

	def _get_fee_structure(self, course_name):
		'''
		param: Course name, str
		returns: dict
		International fee link: https://www.registrar.uwo.ca/student_finances/fees_refunds/pdfsfeeschedule/Fall%20Winter%202020-2021%20UGRD%20fee%20schedule%20INTL.pdf
		Domestic fee link: https://www.registrar.uwo.ca/student_finances/fees_refunds/pdfsfeeschedule/Fall%20Winter%202020-2021%20UGRD%20fee%20schedule%20CDN.pdf
		'''
		fee_str = [
			{	#Arts, Social Science, FIMS-MIT, MOS
				'category': {'art', 'social', 'fims-mit'},
				'int': 33526.00,
				'dom': 6050.00,
				'term': 'year',
			},
			{	#Bio/Med Sci, Science
				'category': {'biology', 'medicine', 'medical', 'science', 'biochemistry', 'astronomy', 'biophysics'},
				'int': 33526.00,
				'dom': 6050.00,
				'term': 'year',
			},
			{	#Health Science, Kinesiology, Music
				'category': {'health', 'kinesiology', 'music'},
				'int': 33526.00,
				'dom': 6050.00,
				'term': 'year',
			},
			{	#Engineering
				'category': {'engineering'},
				'int': 46269.00,
				'dom': 12294.00,
				'term': 'year',
			},
			{	#Nursing
				'category': {'nursing'},
				'int': 43023.00,
				'dom': 6050.00,
				'term': 'year',
			},
			{	#Business
				'category': {'business', 'management'},
				'int': 50000.00 ,
				'dom': 25200.00,
				'term': 'year',
			},
			{	#Dentistry
				'category': {'dentistry'},
				'int': 95747.00,
				'dom': 35341.00,
				'term': 'year',
			},
			{	#Education
				'category': {'education'},
				'int': 34305.00,
				'dom': 7271.00,
				'term': 'year',
			},	
			{	#Law
				'category': {'law'},
				'int': 34305.00,
				'dom': 7271.00,
				'term': 'year',
			},																																												
		]
		course_name = course_name.lower() #Course name: Civil and Environmental Engineering
		course_name = set(course_name.split(' '))#{'civil', 'and', 'engineering', 'environmental'}
		match = {}
		for i in fee_str:
			d = i.get('category')
			intersec = course_name.intersection(d)
			if intersec:
				match = {
					'int': i.get('int'),
					'dom': i.get('dom'),
					'term': i.get('term'),
				}
				break #For loop gets terminated after first match is found
		return match

			
