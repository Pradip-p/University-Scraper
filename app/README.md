>> Dependencies: 
- Python 3.7

1. Install VirtualEnv Wrapper
- For Windows:
	> pip install virtualenvwrapper-win
- For Unix:
	> pip install virtualenvwrapper

2. Virtual environment
- mkvirtualenv uniscrapyenv
> This creates a new virtual environment and automatically activates it

	To deactivate:
	- deactivate uniscrapyenv

	To again enter the environment
	- workon uniscrapyenv

3. Download the application provided and install all the requirements

- Activate virtual enviroment
	> workon uniscrapyenv

- pip install -r requirements.txt [File is attached in the application]

4. Now navigate to UniversityScraper folder which should contain scrapy.cfg file
	> cd UnivesityScraper

5. Run
	> scrapy crawl <spider-name> --loglevel=WARNING --logfile=<spider-name>.log
eg. scrapy crawl sampleSpider --loglevel=WARNING --logfile=sampleSpider.log


