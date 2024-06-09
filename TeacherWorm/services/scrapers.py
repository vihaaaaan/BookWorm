from abc import ABC, abstractmethod
from datetime import datetime
from dateutil import parser
from typing import Optional, List, Dict

import requests
from bs4 import BeautifulSoup
from django.conf import settings

"""
Class Name: BaseScraper

Description:
    A base class for web scrapers, providing methods to fetch a webpage and abstract methods to extract specific elements

Attributes:
    base_url (str): The base URL of the webpage to scrape.
    headers (dict): HTTP headers for the requests.
    page (BeautifulSoup): Parsed HTML page content.

Methods:
    fetch_webpage(): Fetches the webpage and parses it with BeautifulSoup. Must be executed first and return True to use
                     remaining methods.
    get_headline(): Abstract method to get the headline from the webpage.
    get_image(): Abstract method to get the primary image URL from the webpage.
    get_author(): Abstract method to get the author from the webpage.
    get_source_name(): Abstract method to get the source name from the webpage.
    get_pub_date(): Abstract method to get the publication date from the webpage.
    get_text(): Abstract method to get the text from the webpage.
    get_url(): Returns the base URL of the webpage.

Notes:
    Ensure that the `settings.REFERER` and `settings.USER_AGENT` are properly configured in Django settings.
"""
class BaseScraper(ABC):
    def __init__(self, base_url):
        """
        Initializes the BaseScraper with the given base URL.

        Args:
            base_url (str): The base URL of the webpage to scrape.
        """
        self.base_url = base_url
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'referer': settings.REFERER,
            'user-agent': settings.USER_AGENT,
        }
        self.page = None
        self._webpage_fetched = False

    def fetch_webpage(self) -> bool:
        """
        Fetches the webpage and parses it with BeautifulSoup.

        Returns:
            bool: True if the webpage was successfully fetched and parsed, False otherwise.
        """
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 200:
            self.page = BeautifulSoup(response.text, 'html.parser')
            self._webpage_fetched = True
            return True
        else:
            return False

    @abstractmethod
    def get_headline(self) -> Optional[str]:
        """
        Abstract method to get the headline from the webpage.

        Returns:
            Optional[str]: The headline of the webpage, or None if not found.
        """
        pass

    @abstractmethod
    def get_image(self) -> Optional[str]:
        """
        Abstract method to get the primary image URL from the webpage.

        Returns:
            Optional[str]: The primary image URL of the webpage, or None if not found.
        """
        pass

    @abstractmethod
    def get_author(self) -> Optional[List[str]]:
        """
        Abstract method to get the author from the webpage.

        Returns:
            Optional[List[str]]: A list of authors of the webpage, or None if not found.
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """
        Abstract method to get the source name from the webpage.

        Returns:
            str: The source name of the webpage.
        """
        pass

    @abstractmethod
    def get_pub_date(self) -> Optional[datetime]:
        """
        Abstract method to get the publication date from the webpage.

        Returns:
            Optional[datetime]: The publication date of the webpage, or None if not found.
        """
        pass

    @abstractmethod
    def get_text(self) -> Optional[List[Dict[str, str]]]:
        """
        Abstract method to get the text from the webpage.

        Returns:
            Optional[List[Dict[str, str]]]: A list of dictionaries containing the text and type of elements
                                             from the webpage, or None if not found.
        """
        pass

    def get_url(self) -> str:
        """
        Returns the base URL of the webpage.

        Returns:
            str: The base URL of the webpage.
        """
        return self.base_url

    def _ensure_fetched(self):
        """
        Ensures the webpage has been fetched before any extraction methods are called.

        Raises:
            Exception: If the webpage has not been fetched yet.
        """
        if not self._webpage_fetched:
            raise Exception(f'Scraper has not yet fetched webpage for {self.base_url}')


# Create subclass for Yahoo
class YahooScraper(BaseScraper):
    def __init__(self, base_url: str):
        # Initialize the base class with the provided base URL
        super().__init__(base_url)

    def get_headline(self) -> Optional[str]:
        # Ensure the data has been fetched before attempting to extract the headline
        self._ensure_fetched()
        try:
            # Find the headline element and extract its text
            headline = self.page.find('h1').text.strip()
            return headline
        except AttributeError:
            # Return None if the headline element is not found
            return None

    def get_image(self) -> Optional[str]:
        # Ensure the data has been fetched before attempting to extract the image
        self._ensure_fetched()
        try:
            # Find the container with the image and extract the image URL
            container_div = self.page.find('div', class_='caas-img-container')
            img_tag = container_div.find('img', class_='caas-img')
            cover_image_url = img_tag['src']
            return cover_image_url
        except AttributeError:
            # Return None if the image element is not found
            return None

    def get_author(self) -> Optional[List[str]]:
        # Ensure the data has been fetched before attempting to extract the author
        self._ensure_fetched()
        try:
            # Find the author element and extract its text
            author = self.page.find('span', 'caas-author-byline-collapse').text
            authors = [author]
            return authors
        except AttributeError:
            # Return None if the author element is not found
            return None

    def get_source_name(self) -> str:
        # Ensure the data has been fetched before returning the source name
        self._ensure_fetched()
        return "Yahoo News"

    def get_pub_date(self) -> Optional[datetime]:
        # Ensure the data has been fetched before attempting to extract the publication date
        self._ensure_fetched()
        try:
            # Find the publication date element and parse its datetime attribute
            time_tag = self.page.find('time')
            pub_date_str = time_tag['datetime']
            pub_date = parser.parse(pub_date_str)
            return pub_date
        except AttributeError:
            # Return None if the publication date element is not found
            return None

    def get_text(self) -> Optional[List[Dict[str, str]]]:
        # Ensure the data has been fetched before attempting to extract the text
        self._ensure_fetched()
        try:
            # Find all paragraph and subheading elements and extract their text and type
            text_tags = self.page.find_all(['p', 'h2'])
            text = []
            for tag in text_tags:
                text.append({
                    'text': tag.text.strip(),
                    'type': 'plain_text' if tag.name == 'p' else 'subheading' if tag.name == 'h2' else None
                })
            # Return the extracted text or None if no text is found
            if len(text) == 0:
                return None
            else:
                return text
        except AttributeError:
            # Return None if there is an issue finding the text elements
            return None


# Create subclass for CNBC
class CNBCScraper(BaseScraper):
    def __init__(self, base_url: str):
        # Initialize the base class with the provided base URL
        super().__init__(base_url)

    def get_headline(self) -> Optional[str]:
        # Ensure the data has been fetched before attempting to extract the headline
        self._ensure_fetched()
        try:
            # Find the headline element and extract its text
            headline = self.page.find('h1', class_="ArticleHeader-headline").text.strip()
            return headline
        except AttributeError:
            # Return None if the headline element is not found
            return None

    def get_image(self) -> Optional[str]:
        # Ensure the data has been fetched before attempting to extract the image
        self._ensure_fetched()
        try:
            # Find the container with the image and extract the image URL
            container_div = self.page.find('div', class_='InlineImage-imageContainer')
            img_tag = container_div.find('img')
            cover_image_url = img_tag['src']
            return cover_image_url
        except AttributeError:
            # Return None if the image element is not found
            return None

    def get_author(self) -> Optional[List[str]]:
        # Ensure the data has been fetched before attempting to extract the author
        self._ensure_fetched()
        try:
            # Find the author element and extract its text
            author = self.page.find('a', 'Author-authorName').text
            authors = [author]
            return authors
        except AttributeError:
            # Return None if the author element is not found
            return None

    def get_source_name(self) -> str:
        # Ensure the data has been fetched before returning the source name
        self._ensure_fetched()
        return "CNBC"

    def get_pub_date(self) -> Optional[datetime]:
        # Ensure the data has been fetched before attempting to extract the publication date
        self._ensure_fetched()
        try:
            # Find the publication date element and parse its datetime attribute
            time_tag = self.page.find('time')
            pub_date_str = time_tag['datetime']
            pub_date = parser.parse(pub_date_str)
            return pub_date
        except AttributeError:
            # Return None if the publication date element is not found
            return None

    def get_text(self) -> Optional[List[Dict[str, str]]]:
        # Ensure the data has been fetched before attempting to extract the text
        self._ensure_fetched()
        try:
            # Find all paragraph and subheading elements and extract their text and type
            article_body_div = self.page.find('div', class_='ArticleBody-articleBody')
            group_div = article_body_div.find('div', class_='group')
            text_tags = group_div.find_all(
                lambda tag: (tag.name == 'p') or (tag.name == 'h3' and 'ArticleBody-subtitle' in tag.get('class', []))
            )
            text = []
            for tag in text_tags:
                text.append({
                    'text': tag.text.strip(),
                    'type': 'plain_text' if tag.name == 'p' else 'subheading' if tag.name == 'h2' else None
                })
            # Return the extracted text or None if no text is found
            if len(text) == 0:
                return None
            else:
                return text
        except AttributeError:
            # Return None if there is an issue finding the text elements
            return None


# Create subclass for NPR
class NPRScraper(BaseScraper):
    def __init__(self, base_url: str):
        # Initialize the base class with the provided base URL
        super().__init__(base_url)

    def get_headline(self) -> Optional[str]:
        # Ensure the data has been fetched before attempting to extract the headline
        self._ensure_fetched()
        try:
            # Find the headline element and extract its text
            title_div = self.page.find('div', class_='storytitle')
            headline = title_div.find('h1').text.strip()
            return headline
        except AttributeError:
            # Return None if the headline element is not found
            return None

    def get_image(self) -> Optional[str]:
        # Ensure the data has been fetched before attempting to extract the image
        self._ensure_fetched()
        try:
            # Find the container with the image and extract the image URL
            storytext_div = self.page.find('div', 'storytext')
            picture_tag = storytext_div.find('picture')
            img_tag = picture_tag.find('img')
            cover_image_url = img_tag['src']
            return cover_image_url
        except AttributeError:
            # Return None if the image element is not found
            return None

    def get_author(self) -> Optional[List[str]]:
        # Ensure the data has been fetched before attempting to extract the author
        self._ensure_fetched()
        try:
            # Find the author elements and extract their text
            author_tags = self.page.find_all('a', rel='author')
            authors = []
            for author in author_tags:
                author_text = author.text.strip().replace('\n', '')
                if len(author_text) > 0:
                    authors.append(author_text)
            # Return the extracted authors or None if no authors are found
            if len(authors) == 0:
                return None
            else:
                return authors
        except AttributeError:
            # Return None if the author elements are not found
            return None

    def get_source_name(self) -> str:
        # Ensure the data has been fetched before returning the source name
        self._ensure_fetched()
        return "NPR"

    def get_pub_date(self) -> Optional[datetime]:
        # Ensure the data has been fetched before attempting to extract the publication date
        self._ensure_fetched()
        try:
            # Find the publication date element and parse its datetime attribute
            time_tag = self.page.find('time')
            pub_date_str = time_tag['datetime']
            pub_date = parser.parse(pub_date_str)
            return pub_date
        except AttributeError:
            # Return None if the publication date element is not found
            return None

    def get_text(self) -> Optional[List[Dict[str, str]]]:
        # Ensure the data has been fetched before attempting to extract the text
        self._ensure_fetched()
        try:
            # Find all paragraph and subheading elements and extract their text and type
            storytext_div = self.page.find('div', class_='storytext')
            text_tags = storytext_div.find_all(
                lambda tag: (tag.name == 'p') or (tag.name == 'h3' and 'edTag' in tag.get('class', []))
            )
            text = []
            for tag in text_tags:
                text.append({
                    'text': tag.text.strip(),
                    'type': 'plain_text' if tag.name == 'p' else 'subheading' if tag.name == 'h3' else None
                })
            # Return the extracted text or None if no text is found
            if len(text) == 0:
                return None
            else:
                return text
        except AttributeError:
            # Return None if there is an issue finding the text elements
            return None


# Create subclass for BleacherReport
class BleacherReportScraper(BaseScraper):
    def __init__(self, base_url: str):
        # Initialize the base class with the provided base URL
        super().__init__(base_url)

    def get_headline(self) -> Optional[str]:
        # Ensure the data has been fetched before attempting to extract the headline
        self._ensure_fetched()
        try:
            # Find the headline element and extract its text
            title_tag = self.page.find('h1')
            headline = title_tag.text.strip()
            return headline
        except AttributeError:
            # Return None if the headline element is not found
            return None

    def get_image(self) -> Optional[str]:
        # Ensure the data has been fetched before attempting to extract the image
        self._ensure_fetched()
        try:
            # Find the container with the image and extract the image URL
            slideshow_div = self.page.find('div', class_='slideshow')
            img_tag = slideshow_div.find('img')
            cover_image_url = img_tag['src']
            return cover_image_url
        except AttributeError:
            # Return None if the image element is not found
            return None

    def get_author(self) -> Optional[List[str]]:
        # Ensure the data has been fetched before attempting to extract the author
        self._ensure_fetched()
        try:
            # Find the author elements and extract their text
            author_span = self.page.find('span', class_='authorInfo')
            name_spans = author_span.find_all('span', class_='name')
            authors = []
            for author in name_spans:
                author_text = author.text.strip().replace('\n', '')
                if len(author_text) > 0:
                    authors.append(author_text)
            # Return the extracted authors or None if no authors are found
            if len(authors) == 0:
                return None
            else:
                return authors
        except AttributeError:
            # Return None if the author elements are not found
            return None

    def get_source_name(self) -> str:
        # Ensure the data has been fetched before returning the source name
        self._ensure_fetched()
        return "Bleacher Report"

    def get_pub_date(self) -> Optional[datetime]:
        # Ensure the data has been fetched before attempting to extract the publication date
        self._ensure_fetched()
        try:
            # Find the publication date element and parse its datetime attribute
            date_span = self.page.find('span', class_='date')
            pub_date_str = date_span.text
            pub_date = datetime.strptime(pub_date_str, "%B %d, %Y")
            return pub_date
        except AttributeError:
            # Return None if the publication date element is not found
            return None

    def get_text(self) -> Optional[List[Dict[str, str]]]:
        # Ensure the data has been fetched before attempting to extract the text
        self._ensure_fetched()
        try:
            # Find all paragraph and subheading elements and extract their text and type
            text_tags = self.page.find_all(['p', 'h2'])
            text = []
            for tag in text_tags:
                if len(tag.text.strip()) > 0 and tag.text.strip() != self.get_headline():
                    text.append({
                        'text': tag.text.strip(),
                        'type': 'plain_text' if tag.name == 'p' else 'subheading' if tag.name == 'h2' else None
                    })
            # Return the extracted text or None if no text is found
            if len(text) == 0:
                return None
            else:
                return text
        except AttributeError:
            # Return None if there is an issue finding the text elements
            return None
