from sys import argv
from multiprocessing import cpu_count
from parmap import map as parallel_exec
from .inputters.web_inputter import WebInputter
from .readers.gzip_reader import GzipReader
from .outputters.console_outputter import ConsoleOutputter
from .queries.query import Query
from .models.pageview import PageView
from .util import Util


class App:
    @staticmethod
    def main():
        # gets length from argument list
        args_length = len(argv)
        if args_length > 2:
            print('Invalid number of arguments. Must be one at most.')
        else:
            if args_length == 2:
                last_arg = argv[-1]
                # check if last argument is digit
                if last_arg.isdigit():
                    # executes application using argument
                    App._provide_pageviews(int(last_arg))
                else:
                    print('Total hours must be a number.')
            else:
                # executes application
                App._provide_pageviews()

    @staticmethod
    def _provide_pageviews(last_hours=5):
        print(f'Selected total hours was: {last_hours}')
        # gets datetime list from last n hours
        date_times = Util.get_datetime_list(last_hours)
        # initializes WebInputter
        web_inputter = WebInputter()
        # gets half of the cpus, to use
        cpu_to_use = cpu_count() // 2
        print('Downloading and extracting data...')
        # gets lists of PageView in parallel execution
        pageview_lists = parallel_exec(App._process_input,
                                       date_times, web_inputter,
                                       pm_processes=cpu_to_use,
                                       pm_pbar=True)
        # flattens list of lists and gets dictionary from each PageView
        pageviews_flatten = [pageview_dict for pageview_list
                             in pageview_lists
                             for pageview_dict in pageview_list]
        print('Calculating query in progress...')
        # performs query passing flatten PageView list
        pageviews_query = Query.perform_query(pageviews_flatten)
        # initializes ConsoleOutputter
        console_outputter = ConsoleOutputter()
        # displays output
        console_outputter.display_output(pageviews_query)

    @staticmethod
    def _process_input(date_time, web_inputter):
        # transforms input from WebInputter using datetime
        bytes_content = web_inputter.parse_input(date_time)
        # initializes GzipReader passing transformed content
        gzip_reader = GzipReader(bytes_content)
        # gets read lines from GzipReader parsed content
        lines = gzip_reader.read_all_lines()
        # initializes a PageView and gets its dictionary form
        # from each line
        return [PageView.set_pageview_from_line(e).get_dict()
                for e in lines]
