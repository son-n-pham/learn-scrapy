# learn-scrapy

This is the repo to learn scripy

Step that I do:

- Create scrapy project:

```
scrapy startproject bookscraper
```

- Go to spiders folder, create a spider to scrap books from books.toscrape.com

```
scrapy genspider bookspider books.toscrape.com
```

- Open scrapy.cfg, add shell = ipython in the [settings] section. This is to have ipython shell as the shell for using scrapy shell. scrapy shell is the shell of scrapy for a quick experiment before putting the code into the spider script.

- In spiders folder, there are created spider with function parse to download and extract the contents in the web out. The parse function is called by scrapy when the spider is run. The parse function is called for each response downloaded by the spider. The response is the object that scrapy get from the web. The response object has the following attributes:

```python
response.url # The url of the response
response.status # The status of the response
response.headers # The headers of the response
response.body # The body of the response
response.text # The text of the response
```

- response also has below common methods used in spider py file:

  ```python
  response.xpath(xpath_expression) # Returns an XPathSelector object
  response.css(css_expression) # Returns a CssSelector object
  response.xpath(xpath_expression).extract() # Returns a list of strings, one for each matching element
  response.css(css_expression).extract() # Returns a list of strings, one for each matching element
  response.css(css_expression).get() # Returns the first matching element as a string
  response.xpath(xpath_expression).get() # Returns the first matching element as a string
  ```

- Once having a spider, run the below command to execute the spider:

  ```
  scrapy crawl bookspider
  ```

- We can also export the result to csv or json file with -o

  ```
  scrapy crawl bookspider -o books.json
  ```

- items.py is used to setup the data structure that will be used to store the data. The data structure is defined by the class Item. The class Item is a subclass of dict. The class Item has a method to define the fields of the data structure. The fields are defined by Field object. The Field object has the following parameters:

  - required: whether the field is required or not
  - default: the default value of the field
  - serializer: the function to serialize the field
  - deserializer: the function to deserialize the field
  - input_processor: the function to process the input of the field
  - output_processor: the function to process the output of the field (after serialization) of the field

- In the spider, we need to import the Item class and the Field class from the items.py file. Then, we need to instantiate the Item class to create an object of the Item class. The object of the Item class is used to store the data.

- In the spider, we need to define the parse function. The parse function is called by scrapy when the spider is run. The parse function is called for each response downloaded by the spider. The response is the object that scrapy get from the web. The response object has the following attributes:

  ```python
  response.url # The url of the response
  response.status # The status of the response
  response.headers # The headers of the response
  response.body # The body of the response
  response.text # The text of the response
  ```

- The pipeplines.py is used to setup the pipeline. The pipeline is used to process the data after the spider is run. The pipeline is used to process the data after the spider is run. The pipeline is a class that has the following methods:

  - open_spider(self, spider): This method is called when the spider is opened
  - close_spider(self, spider): This method is called when the spider is closed
  - process_item(self, item, spider): This method is called for each item that is yielded by the spider. The method returns the item or raise DropItem exception to drop the item.

- To use pipelines.py, we need to enable it in the setting.py file. The pipelines.py is enabled by adding the following line in the ITEM_PIPELINES section:

  ```python
  ITEM_PIPELINES = {
      'bookscraper.pipelines.BookscraperPipeline': 300,
  }
  ```

- Work with database MySQL:
  - Install MySQL Community
  - pip install mysql mysql-connector-python
