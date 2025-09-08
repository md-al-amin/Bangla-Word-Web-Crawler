#!/usr/bin/env python3
"""
A web crawler that searches for Bangla words across multiple domains.

This program takes a list of domains and a list of Bangla words, crawls the
specified domains, and outputs a CSV file with the URLs where each word was found.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import time
import re
import argparse
from collections import deque
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# --- Configuration & Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Core Web Crawler Class ---
class BanglaWebCrawler:
    def __init__(self, max_pages_per_domain, delay, max_workers):
        self.max_pages_per_domain = max_pages_per_domain
        self.delay = delay
        self.max_workers = max_workers
        self.found_matches = []
        self.lock = threading.Lock()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; BanglaCrawler/1.0)",
            "Accept-Language": "bn-BD,bn;q=0.9,en-US;q=0.8,en;q=0.7"
        })

    def fetch_page(self, url):
        """
        Downloads HTML content of a page with an automatic HTTPS->HTTP fallback.
        """
        parsed_url = urlparse(url)
        initial_scheme = parsed_url.scheme
        fallback_scheme = 'http' if initial_scheme == 'https' else 'https'
        
        # Build the fallback URL
        fallback_url = parsed_url._replace(scheme=fallback_scheme).geturl()

        try:
            r = self.session.get(url, timeout=10)
            r.raise_for_status()
            if "text/html" in r.headers.get("Content-Type", ""):
                return r.text
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {url} ({e}). Attempting fallback to {fallback_scheme}...")
            try:
                r_fallback = self.session.get(fallback_url, timeout=10)
                r_fallback.raise_for_status()
                if "text/html" in r_fallback.headers.get("Content-Type", ""):
                    logger.info(f"Fallback successful for {url}.")
                    return r_fallback.text
            except requests.RequestException as e_fallback:
                logger.error(f"Fallback also failed for {url}: {e_fallback}")
        return None

    def extract_links(self, base_url, html):
        """Extracts all internal links from the HTML."""
        soup = BeautifulSoup(html, "lxml")
        links = set()
        for a in soup.find_all("a", href=True):
            href = urljoin(base_url, a["href"])
            # Ensure the link is within the same domain and strip URL fragments
            if urlparse(href).netloc == urlparse(base_url).netloc:
                links.add(href.split("#")[0])
        return links

    def search_keywords(self, html, keywords):
        """Searches for Bangla keywords as substrings in the text content."""
        found = []
        text = BeautifulSoup(html, "lxml").get_text(" ", strip=True)
        for word in keywords:
            # Using re.search for substring matching to find words like 'অভিলক্ষ্য'
            # even when they are part of a larger string without spaces.
            if re.search(re.escape(word), text):
                found.append(word)
        return found

    def crawl_domain(self, domain, keywords):
        """Crawl the internal pages of a single domain."""
        logger.info(f"Starting to crawl domain: {domain}")
        visited = set()
        # Start with a secure connection attempt
        to_visit = deque([f"https://{domain}"])
        pages_crawled = 0

        while to_visit and pages_crawled < self.max_pages_per_domain:
            url = to_visit.popleft()
            if url in visited:
                continue
            visited.add(url)

            html = self.fetch_page(url)
            if not html:
                continue

            matches = self.search_keywords(html, keywords)
            if matches:
                with self.lock:
                    for word in matches:
                        self.found_matches.append({"URL": url, "Matched Word": word})
                        logger.info(f"Found '{word}' at {url}")

            new_links = self.extract_links(url, html)
            for link in new_links:
                if link not in visited:
                    to_visit.append(link)

            pages_crawled += 1
            time.sleep(self.delay)
        
        logger.info(f"Finished crawling domain: {domain} ({pages_crawled} pages)")

    def run(self, domains, words, output_file):
        """Main method to run the crawler on all domains."""
        logger.info("Starting Bangla Word Web Crawler")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_domain = {executor.submit(self.crawl_domain, domain, words): domain for domain in domains}
            for future in as_completed(future_to_domain):
                future.result()  # Wait for threads to complete

        self.save_results(output_file)
        logger.info("Crawling completed.")

    def save_results(self, output_file):
        """Saves the results to a CSV file."""
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ["URL", "Matched Word"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for match in self.found_matches:
                    writer.writerow(match)
            logger.info(f"Results saved to {output_file}")
            logger.info(f"Total matches found: {len(self.found_matches)}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")

# --- Helper Functions ---
def create_sample_files():
    """Creates sample input files for testing."""
    sample_domains = ["example.com", "wikipedia.org"]
    with open('domain_list.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sample_domains))
    
    sample_words = ["বাংলাদেশ", "আমাদের", "সফটওয়্যার"]
    with open('word_list.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sample_words))
    
    logger.info("Sample files 'domain_list.txt' and 'word_list.txt' created.")

def load_file_content(file_path):
    """Loads a list of strings from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.error(f"Error: The file {file_path} was not found.")
        return None

# --- Main Program Execution ---
def main():
    """Parses command-line arguments and runs the crawler."""
    parser = argparse.ArgumentParser(description="Bangla Web Crawler")
    parser.add_argument("--domains", help="Path to the file containing domains.")
    parser.add_argument("--words", help="Path to the file containing Bangla words.")
    parser.add_argument("--output", default="results.csv", help="Path for the output CSV file.")
    parser.add_argument("--max-pages", type=int, default=100, help="Maximum pages to crawl per domain.")
    parser.add_argument("--workers", type=int, default=10, help="Number of concurrent workers.")
    parser.add_argument("--create-samples", action="store_true", help="Creates sample input files.")
    
    args = parser.parse_args()

    if args.create_samples:
        create_sample_files()
        return

    if not args.domains or not args.words:
        parser.error("The --domains and --words arguments are required unless --create-samples is used.")
    
    domains = load_file_content(args.domains)
    words = load_file_content(args.words)
    
    if not domains or not words:
        return

    crawler = BanglaWebCrawler(
        max_pages_per_domain=args.max_pages,
        delay=1, # Fixed delay to be polite to websites
        max_workers=args.workers
    )
    
    crawler.run(domains, words, args.output)

if __name__ == "__main__":
    main()
