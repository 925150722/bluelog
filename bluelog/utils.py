
import re
from unidecode import unidecode


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_~{|},.]+')


def slugify(text, delim=u'-'):
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).lower().split())
    return unidecode(delim.join(result))
