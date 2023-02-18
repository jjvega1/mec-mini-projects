import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"

    def start_requests(self):
        yield scrapy.Request('http://quotes.toscrape.com/', self.parse)

    def parse(self, response):

        for i in range(len(response.xpath("//div[@class='quote']"))):
            text = response.xpath(
                '//div/span[@class="text"]/text()')[i].get()  # Quote to match
            tag_num = 1  # get all rows who have at least this many number of tags
            row_num = 0  # iteratre through rows with at least x many tags
            l = []  # initalize empty list to store in yield
            while True:  # infinite loop that will break if we go out of bounds via row_num
                try:
                    # If the tags' ancestors quote matches the text
                    if response.xpath(F"//div[@class='tags']/a[{tag_num}]/parent::*/parent::*/span[@class='text']/text()")[row_num].get() == text:
                        # add it to the list
                        l.append(response.xpath(
                            '//div[@class="tags"]/a[{tag_num}]/text()')[row_num].get())
                        # Increment tag number to check if the current quote has at least one more tag
                        tag_num += 1
                        # reset row number
                        row_num = 0
                        continue
                    else:
                        # If quotes do not match, try the next quote with x amount of tags
                        row_num += 1
                        continue
                except:
                    # We went out of bounds
                    break
            yield {
                'text': text,
                'author': response.xpath('//span/small[@class="author"]/text()')[i].get(),
                'tags': l,
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
