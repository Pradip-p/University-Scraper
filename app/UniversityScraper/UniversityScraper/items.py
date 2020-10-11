# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UniversityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #1 CourseName
    course_name = scrapy.Field()

    #2 Category
    category = scrapy.Field()

    #3 SubCategory
    sub_category = scrapy.Field()

    #4 Course Website
    course_website = scrapy.Field()

    #5 Duration
    duration = scrapy.Field()

    #6 Duration Term
    duration_term = scrapy.Field()

    #7 Study Mode
    study_mode = scrapy.Field()

    #8 Degree Level
    degree_level = scrapy.Field()

    #9 Monthly Intake
    monthly_intake = scrapy.Field()

    #10 Intake Day
    intake_day = scrapy.Field()

    #11 Intake Month
    intake_month = scrapy.Field()

    #12 Apply Day
    apply_day = scrapy.Field()

    #13 Apply Month
    apply_month = scrapy.Field()

    #14 City
    city = scrapy.Field()

    #15 Domestic Only
    domestic_only = scrapy.Field()

    #16 International Fee
    international_fee = scrapy.Field()

    #17 Domestic Fee
    domestic_fee = scrapy.Field()

    #18 Fee Term
    fee_term = scrapy.Field()

    #19 Fee Year
    fee_year = scrapy.Field()

    #20 Currency
    currency = scrapy.Field()

    #21 Study Load
    study_load = scrapy.Field()

    #22 IELTS Listening
    ielts_listening = scrapy.Field()

    #23 IELTS Speaking
    ielts_speaking = scrapy.Field()

    #24 IELTS Writing
    ielts_writing = scrapy.Field()

    #25 IELTS Reading
    ielts_reading = scrapy.Field()

    #26 IELTS Overall
    ielts_overall = scrapy.Field()

    #27 PTE Listening
    pte_listening = scrapy.Field()

    #28 PTE Speaking
    pte_speaking = scrapy.Field()

    #29 PTE Writing
    pte_writing = scrapy.Field()

    #30 PTE Reading
    pte_reading = scrapy.Field()

    #31 PTE Overall
    pte_overall = scrapy.Field()

    #32 TOEFL Listening
    toefl_listening = scrapy.Field()

    #33 TOEFL Speaking
    toefl_speaking = scrapy.Field()

    #34 TOEFL Writing
    toefl_writing = scrapy.Field()

    #35 TOEFL Reading
    toefl_reading = scrapy.Field()

    #36 TOEFL Overall
    toefl_overall = scrapy.Field()

    #37 English Test
    english_test = scrapy.Field()

    #38 Reading
    reading = scrapy.Field()

    #39 Listening
    listening = scrapy.Field()

    #40 Speaking
    speaking = scrapy.Field()

    #41 Writing
    writing = scrapy.Field()

    #42 Overall
    overall = scrapy.Field()

    #43 Academic Level
    academic_level = scrapy.Field()

    #44 Academic Score
    academic_score = scrapy.Field()

    #45 Score Type
    score_type = scrapy.Field()
    
    #46 Academic Country
    academic_country = scrapy.Field()

    #47 Other Test
    other_test = scrapy.Field()

    #48 Score
    score = scrapy.Field()

    #49 Other Requirements
    other_requirements = scrapy.Field()

    #50 Course Description
    course_description = scrapy.Field()

    #51 Course Structure
    course_structure = scrapy.Field()

    #52 Career
    career = scrapy.Field()

    #53 Scholarship
    scholarship = scrapy.Field()