# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from dotenv import load_dotenv
import os
import mysql.connector
from pydantic import BaseModel
from itemadapter import ItemAdapter

import re
import bs4 as BeautifulSoup


def extract_number(string, int_or_float='int'):
    if not isinstance(string, str):
        return None
    numbers = re.findall(r"\d+", string)
    if int_or_float == 'int':
        return int(numbers[0]) if numbers else None
    elif int_or_float == 'float':
        return float(numbers[0]) if numbers else None
    else:
        return None


class BookscraperPipeline:

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Strip all white space from strings except field description
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                adapter[field_name] = adapter[field_name].strip()

        # Convert category and rating to lower case
        lowercase_fields = ["category", "rating"]
        for field_name in lowercase_fields:
            adapter[field_name] = adapter[field_name].lower()

        # Convert price to float
        adapter["price"] = extract_number(adapter["price"], 'float')

        # Extract number from availability field
        adapter["availability"] = extract_number(
            adapter["availability"], 'int')

        # Convert star rating to number
        if "zero" in adapter["rating"]:
            adapter["rating"] = 0
        elif "one" in adapter["rating"]:
            adapter["rating"] = 1
        elif "two" in adapter["rating"]:
            adapter["rating"] = 2
        elif "three" in adapter["rating"]:
            adapter["rating"] = 3
        elif "four" in adapter["rating"]:
            adapter["rating"] = 4
        elif "five" in adapter["rating"]:
            adapter["rating"] = 5
        else:
            adapter["rating"] = None

        # Extract text from category a tag
        soup = BeautifulSoup.BeautifulSoup(adapter["category"], "html.parser")
        adapter["category"] = soup.a.text

        return item


load_dotenv()


class SaveToMySQLPipeline:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("MYSQL_PASSWORD"),
        )

        self.cursor = self.connection.cursor()

        # Create book_store database if it does not exist
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS book_store")
        self.cursor.execute("USE book_store")

        # Create books table if it does not exist
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                price FLOAT,
                availability INT,
                rating INT,
                upc VARCHAR(255),
                category VARCHAR(255),
                description TEXT
            )
            """
        )

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.cursor.execute(
            """
            INSERT INTO books (
                title,
                price,
                availability,
                rating,
                upc,
                category,
                description
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                adapter["title"],
                adapter["price"],
                adapter["availability"],
                adapter["rating"],
                adapter["upc"],
                adapter["category"],
                adapter["description"],
            )
        )

        self.connection.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
