from io import TextIOWrapper, BytesIO
from gzip import GzipFile
from interface import implements
from .reader import Reader


class GzipReader(implements(Reader)):
    def __init__(self, file_content):
        self.file_content = file_content

    def read_all_lines(self):
        # if no content return empty array
        if self.file_content is None:
            return []
        try:
            # wrap content into BytesIO
            fileBytes = BytesIO(self.file_content)
            lines = []
            # decompress gzipfile to read
            with GzipFile(fileobj=fileBytes) as uncompressed:
                # wrap file into TextIOWrapper to read as text
                wrapper = TextIOWrapper(uncompressed, encoding='utf-8')
                # most efficient way to read text from file
                for line in wrapper:
                    lines.append(line)
            return lines
        except Exception as e:
            print(f'Error in GzipReader due to: {e}')
            return None
