# Bangla Word Web Crawler
This is a powerful and efficient multithreaded web crawler designed specifically for searching Bengali words across multiple websites. It's built to be both fast and respectful of the websites it crawls.

The program takes a list of domains and a list of target words. It then systematically crawls each domain, follows internal links up to a specified limit, and identifies any pages where a target word is found. All matches are logged and saved to a clean CSV file for easy analysis.

## Key Features
**Multithreaded:** Utilizes a `ThreadPoolExecutor` to crawl multiple domains and pages concurrently, drastically reducing the total time required for large-scale searches.

**Polite Crawling:** Includes a configurable delay between requests to prevent overwhelming target servers and to adhere to ethical crawling practices.

**Robust Protocol Handling:** Automatically attempts to switch from HTTPS to HTTP if a request fails, ensuring broader site accessibility.

**Configurable Parameters:** Easily adjust the number of concurrent workers, the maximum number of pages to crawl per domain, and the request delay via command-line arguments.

**UTF-8 Support:** Full support for Bengali script and other Unicode characters, ensuring accurate word matching and output.

**Targeted Internal Search:** Only follows links within the same domain, keeping the crawl focused and relevant to the provided domain list.

**Comprehensive Logging:** All crawling activity, warnings, and errors are logged to a `crawler.log` file, making it easy to monitor and debug the process.

**CSV Output:** All found matches, including the URL and the specific matched word, are saved to a neatly formatted `results.csv` file.

## Prerequisites
To run this program, you need Python 3 installed on your system. The required libraries are listed in the `requirements.txt` file.

## Installing Dependencies
You can install all necessary libraries by running the following command in your terminal:

```
python3 -m pip install -r requirements.txt
```

## requirements.txt
The requirements.txt file specifies the Python libraries your program depends on. The list now includes a few more packages that improve the reliability and functionality of the crawler:

 + **requests==2.31.0:** The primary library for making HTTP requests to websites.

beautifulsoup4==4.12.2: A library for pulling data out of HTML and XML files.

lxml==4.9.3: A high-performance XML and HTML parser that serves as a backend for BeautifulSoup.

html5lib==1.1: A robust, standard-compliant HTML parser that can also be used with BeautifulSoup.

urllib3==2.0.7: An HTTP client library that is a dependency of requests.

certifi==2023.7.22: A curated list of trusted root certificates that requests uses to verify SSL certificates.

charset-normalizer==3.3.2: A library that helps detect the character encoding of text, ensuring proper handling of Bengali text.

idna==3.4: A library for handling internationalized domain names.

soupsieve==2.5: A CSS selector library that improves the performance of BeautifulSoup.

regex==2023.10.3: A more advanced regular expression library for more complex search patterns.
