# -*- coding: utf-8 -*-
import scrapy
from UniversityScraper.items import UniversityItem
import logging, re, traceback

class SampleSpider(scrapy.Spider):
	name = 'sampleSpider'
	allowed_domains = ['www.aut.ac.nz']
	start_urls = ['https://www.aut.ac.nz/international/study-options-for-international-students/study-areas-degree-courses-and-programmes']

	def parse(self, response):
		study_options = response.xpath('//div[@class="col-sm-6"]/ul/li/a/@href').extract()
		logging.warn("SampleSpider; Scraping Started...; url= %s",response.url)
		for base_url in study_options:
			if "postgraduate" not in base_url:
				yield scrapy.Request(base_url,callback=self.parse_base_url)

	def parse_base_url(self,response):
		courses = response.xpath('//div[@class="panel panel-default"]/div[@role="tabpanel"]/div/ul/li/a/@href').extract()
		logging.warn("SampleSpider; Scraping Courses Started....; url= %s",response.url)
		for course_url in courses:
			if "bachelor" in course_url or "diploma" in course_url or "postgraduate" in course_url or "doctor" in course_url:
				yield scrapy.Request(course_url,callback=self.parse_course)

	def parse_course(self,response):
		try:
			item = UniversityItem()
			
			#1 CourseName
			course_name = response.xpath('//div[@id="mainContent"]/h1/text()').extract_first()
			item['course_name'] = course_name
			
			#2 Category
			category = response.xpath('//div[@id="breadcrumb"]/a[4]/text()').extract_first()
			item['category'] = category

			#4 Course Website
			course_website = response.url
			item['course_website'] = course_website

			#########Unprocessed Quick Facts Table
			quick_facts = self._get_quick_facts(response)
			
			#5 Duration
			duration = study_mode = ""
			part_time = False
			if "Duration" in quick_facts:
				pre_duration = quick_facts["Duration"].split("/")

				if len(pre_duration) > 1:
					part_time = True
				
				if "to" in pre_duration[0]:
					pre_duration = []
					pre_duration.append(quick_facts["Duration"].split("to")[-1])

				pre_duration_list = pre_duration[0].strip().split(" ")

				duration = pre_duration_list[0] + " " + pre_duration_list[1]
				#21 Study Load
				if part_time:
					study_mode = "Both"
				else:
					study_mode = pre_duration_list[1]
			
			item["study_mode"] = study_mode

			item['duration'] = duration

			#6 Duration Term
			duration_term = ""
			if duration:
				duration_term = duration.split(" ")[-1]
			
			item['duration_term'] = duration_term

			#8 Degree Level
			degree_level = ""
			if "Level" in quick_facts:
				level = quick_facts["Level"]
				if level == '7':
					degree_level = "Undergraduate"
				if level == '9':
					degree_level = "Postgraduate"
				if level == '10':
					degree_level = "Doctorate"
				if level == '4':
					degree_level = "Diploma"
			
			item['degree_level'] = degree_level

			intake_day = intake_month = ""
			if "Starts" in quick_facts:
				intake_pre = quick_facts["Starts"]
				if intake_pre:
					if "Any time" not in intake_pre:
						intake = intake_pre.split(" ")
						#10 Intake Day
						intake_day = intake[0]
						#11 Intake Month
						intake_month = intake[1]
					else:
						#10 Intake Day
						intake_day = "Any time"
						#11 Intake Month
						intake_month = "Any time"
			item["intake_day"] = intake_day
			item["intake_month"] = intake_month
			
			#14 City
			city = ""
			if "Campus" in quick_facts:
				city = quick_facts["Campus"]
			item["city"] = city
			
			#16 International Fee
			international_fee = ""
			if "International" in quick_facts:
				if '\xa0' in quick_facts["International"]:
					international_fee = quick_facts["International"].split("\xa0")[0]
				else:
					international_fee = quick_facts["International"]
			item["international_fee"] = international_fee

			#17 Domestic Fee
			#20 Currency
			domestic_fee = currency = ""
			if "Domestic" in quick_facts:
				domestic_fee = quick_facts["Domestic"]
				currency = quick_facts["Domestic"][0]
			item["domestic_fee"] = domestic_fee
			item["currency"] = currency

			#50 Course Description
			pre_description = response.xpath('//div[@id="mainContent"]/div[1]/div[1]/div/p').extract()
			course_description = ""
			for desc in pre_description:
				course_description += desc
			item["course_description"] = course_description

			#####Get panel data
			panel_data = self._get_panel_data(response)

			#51 Course Structure
			course_structure = panel_data["course_structure"]
			item["course_structure"] = course_structure

			#52 Career
			career = panel_data["career"]
			item["career"] = career

			#### IELTS Data
			ielts = panel_data["ielts"]
			ielts_listening = ielts_writing = ielts_speaking = ielts_reading = ielts_overall = ""
			if ielts:

				ielts_data = re.findall("\d+\.\d+", ielts)
				
				#22 IELTS Listening
				ielts_listening = ielts_data[-1]

				#23 IELTS Speaking
				ielts_speaking = ielts_data[-1]

				#24 IELTS Writing
				if len(ielts_data) == 3:
					ielts_writing = ielts_data[1]
				else:
					ielts_writing = ielts_data[-1]

				#25 IELTS Reading
				ielts_reading = ielts_data[-1]

				#26 IELTS Overall
				ielts_overall = ielts_data[0]

			item["ielts_listening"] = ielts_listening
			item["ielts_writing"] = ielts_writing
			item["ielts_reading"] = ielts_reading
			item["ielts_speaking"] = ielts_speaking
			item["ielts_overall"] = ielts_overall

			yield item

		except Exception as e:
			logging.error("SampleSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
			logging.error("SampleSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())
	
	def _get_quick_facts(self,response):
		#Quick Facts Table
		quick_facts_heading = response.xpath('//div[@class="row"]/div[contains(@class,"heading")]/text()').extract()
		quick_facts_value = response.xpath('//div[@class="row"]/div[contains(@class,"value")]/text()').extract()
		
		quick_facts = {}
		for i in range(0,len(quick_facts_heading)):
			if quick_facts_heading[i].strip(":") not in quick_facts:
				quick_facts[quick_facts_heading[i].strip(":")] = quick_facts_value[i].strip()
		
		#Starts should be extracted separately
		starts = response.xpath('//div[@class="row"]/div[contains(@class,"value")]/div[1]/text()').extract_first()
		
		if starts:
			starts = starts.strip()
		
		quick_facts['Starts'] = starts

		#Fees Extraction
		fees = response.xpath('//div[@class="row feeSection"]/div[contains(@class,"value")]/span/text()').extract()
		
		for i in range(0,len(fees)):
			if i%2==0:
				quick_facts[fees[i]] = fees[i+1]
		return quick_facts

	def _get_panel_data(self,response):
		
		titles = response.xpath('//div[@class="tmp_tabs-wrapper frontend"]/div/ul/li/a/span/span/text()').extract()

		#What You Study

		content = response.xpath('//div[@class="tmp_tabs-wrapper frontend"]/div[2]/div')
		
		ielts_data = structure_data = career_data = ""

		if "Entry requirements" in titles:
			entry_ind = titles.index("Entry requirements")
			ielts_data = content[entry_ind].xpath("ul[2]/li/text()").extract_first()
			if not ielts_data or (ielts_data and "IELTS" not in ielts_data):
				ielts_data = content[entry_ind].xpath("div/ul[2]/li/text()").extract_first()
				if not ielts_data or (ielts_data and "IELTS" not in ielts_data):
					ielts_data = content[entry_ind].xpath("div/ul[3]/li/text()").extract_first()
					if not ielts_data or (ielts_data and "IELTS" not in ielts_data):
						ielts_data = content[entry_ind].xpath("div/div/div/ul[3]/li/text()").extract_first()


		if "What you study" in titles:
			structure_ind = titles.index("What you study")
			structure_data = content[structure_ind].extract()
		
		if "Career opportunities" in titles:
			career_ind = titles.index("Career opportunities")
			career_data = content[career_ind].extract()

		panel_data = {}

		panel_data["ielts"] = ielts_data
		panel_data["course_structure"] = structure_data
		panel_data["career"] = career_data

		return panel_data