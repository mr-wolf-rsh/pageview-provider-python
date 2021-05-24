
class PageView():
    def __init__(self, domain_code, page_title,
                 count_views, total_response_size):
        self.domain_code = domain_code
        self.page_title = page_title
        self.count_views = count_views
        self.total_response_size = total_response_size

    @staticmethod
    def set_pageview_from_line(pageview_line):
        # splits string from spaces
        pageview_values = pageview_line.split(' ')

        # unpack values to match constructor
        return PageView(*pageview_values)

    def get_dict(self):
        # returns class PageView dictionary form
        return self.__dict__

    def __str__(self):
        # returns values in this string format
        return f'{self.domain_code} {self.page_title} {self.count_views}'
