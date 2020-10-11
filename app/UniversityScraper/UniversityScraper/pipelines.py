# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from scrapy import signals

class UniversityscraperPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        output_file = open(str(spider.name)+'.csv', 'a+b')
        self.files[spider] = output_file
        self.exporter = CsvItemExporter(output_file)
        self.exporter.fields_to_export = ['course_name','category','sub_category','course_website','duration','duration_term','study_mode','degree_level','monthly_intake','intake_day','intake_month','apply_day','apply_month','city','domestic_only','international_fee','domestic_fee','fee_term','fee_year','currency','study_load','ielts_listening','ielts_speaking','ielts_writing','ielts_reading','ielts_overall','pte_listening','pte_speaking','pte_writing','pte_reading','pte_overall','toefl_listening','toefl_speaking','toefl_writing','toefl_reading','toefl_overall','english_test','reading','listening','speaking','writing','overall','academic_level','academic_score','score_type','academic_country','other_test','score','other_requirements','course_description','course_structure','career','scholarship']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        output_file = self.files.pop(spider)
        output_file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
