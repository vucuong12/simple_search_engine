# Welcome to my simple search engine!

- Setup
	- Install python3.5.3 (https://www.python.org/downloads/release/python-353/) 
		- Note: during the installation, remember to choose the option to add  python and PIP to environment PATH.
	- Install package (library) `requests` by running this command line on terminal:
		- `pip3 install request`
	- Install package `Flask`:
		- `pip3 install Flask`
- How to run?
	- Create a web server:
		- Open a terminal, go to the working folder (simple_search_engine)
		- Run `python3 my_search_engine.py` and wait until it finishes crawling and creating a web server.
	- Run a client:
		- Open a web browser (which is a client)
		- Go to the link http://127.0.0.1:5000 and enjoy :)
- What you can modify?
	- Change the HTML files to make your search engine look more beautiful.
	- Change the first page to crawl and the max number of pages to crawl:
		- `crawlWebsites("https://blog.codinghorror.com/", 10)`
	- Etc.