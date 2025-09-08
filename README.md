# Bangla Word Web Crawler
This is a powerful and efficient multithreaded web crawler designed specifically for searching Bengali words across multiple websites. It's built to be both fast and respectful of the websites it crawls.

The program takes a list of domains and a list of target words. It then systematically crawls each domain, follows internal links up to a specified limit, and identifies any pages where a target word is found. All matches are logged and saved to a clean CSV file for easy analysis.

## Key Features
**Multithreaded:** Utilizes a ThreadPoolExecutor to crawl multiple domains and pages concurrently, drastically reducing the total time required for large-scale searches.
**Polite Crawling:** Includes a configurable delay between requests to prevent overwhelming target servers and to adhere to ethical crawling practices.
**Robust Protocol Handling:** Automatically attempts to switch from HTTPS to HTTP if a request fails, ensuring broader site accessibility.
**Configurable Parameters:** Easily adjust the number of concurrent workers, the maximum number of pages to crawl per domain, and the request delay via command-line arguments.
**UTF-8 Support:** Full support for Bengali script and other Unicode characters, ensuring accurate word matching and output.
**Targeted Internal Search:** Only follows links within the same domain, keeping the crawl focused and relevant to the provided domain list.
**Comprehensive Logging:** All crawling activity, warnings, and errors are logged to a crawler.log file, making it easy to monitor and debug the process.
**CSV Output:** All found matches, including the URL and the specific matched word, are saved to a neatly formatted results.csv file.
