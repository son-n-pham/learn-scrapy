import scrapy
from ..items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    custom_settings = {
        'FEEDS': {
            'books_data.json': {'format': 'json', 'overwrite': True},
        },
        'ROBOTSTXT_OBEY': True,
    }

    def parse(self, response):
        # Implement standard operation for this parse of this spider
        # q: What should I do with this parse?
        # a: I should go through the list of books on the page and yield a new

        # Use css selector to get all books in a page
        books = response.css("article.product_pod")

        for book in books:

            # Get the link to the book
            link = book.css("h3 a::attr(href)").get()

            # Go to the link of the book
            book = response.follow(link, callback=self.parse_book)

            # Yield the book information
            yield book

        next_page = response.css("li.next a::attr(href)").get()

        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book(self, response):
        book = BookItem()

        book['title'] = response.css(".product_main h1::text").get()
        book['price'] = response.css(
            ".product_main p.price_color::text").get()

        availability = response.css(
            ".product_main p.availability::text").getall()
        availability = [text.strip() for text in availability if text.strip()]
        book['availability'] = ' '.join(availability).strip()

        book['rating'] = response.css(
            ".product_main p.star-rating::attr(class)").get()
        book['upc'] = response.xpath(
            '//th[text()="UPC"]/following-sibling::td/text()').get()
        book['category'] = response.xpath(
            '//*[@id="default"]/div[1]/div/ul/li[3]/a').get()
        book['description'] = response.css(
            "#product_description ~ p::text").get()

        yield book
