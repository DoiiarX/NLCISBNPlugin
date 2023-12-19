from calibre.ebooks.metadata.sources.base import Source
from calibre.ebooks.metadata import MetaInformation
import re
import urllib.request
from bs4 import BeautifulSoup

# 常量定义：URL 和头信息
BASE_URL = "http://opac.nlc.cn/F"
PROVIDER_ID = "isbn"
SEARCH_URL_TEMPLATE = BASE_URL + "?func=find-b&find_code=ISB&request={isbn}&local_base=NLC01" + \
                      "&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=" + \
                      "&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5="
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Host': 'opac.nlc.cn',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}

def get_dynamic_url(log):
    '''
    从基础页面获取动态URL。
    :param log: 日志记录器。
    :return: 动态URL或None（获取失败时）。
    '''
    try:
        response = urllib.request.urlopen(urllib.request.Request(BASE_URL, headers=HEADERS), timeout=10)
        response_text = response.read().decode('utf-8')
        dynamic_url_match = re.search(r"http://opac.nlc.cn:80/F/[^\s?]*", response_text)
        if dynamic_url_match:
            dynamic_url = dynamic_url_match.group(0)
            log(dynamic_url)
            return dynamic_url
        else:
            raise ValueError("无法找到动态URL")
    except Exception as e:
        log(f"获取动态URL时出错: {e}")
        return None

def isbn2meta(isbn, log):
    '''
    将ISBN转换为元数据。
    :param isbn: ISBN号码，作为字符串。
    :param log: 日志记录器。
    :return: 解析后的元数据或None（获取失败时）。
    '''
    if not isinstance(isbn, str):
        log("ISBN必须是字符串")
        raise TypeError("ISBN必须是字符串")

    try:
        isbn_match = re.match(r"\d{10,}", isbn).group()
    except AttributeError:
        log(f"无效的ISBN代码: {isbn}")
        raise ValueError(f"无效的ISBN代码: {isbn}")

    if isbn_match != isbn:
        log(f"无效的ISBN代码: {isbn}")
        raise ValueError(f"无效的ISBN代码: {isbn}")

    dynamic_url = get_dynamic_url(log)
    if not dynamic_url:
        return None

    search_url = SEARCH_URL_TEMPLATE.format(isbn=isbn)
    try:
        response = urllib.request.urlopen(urllib.request.Request(search_url, headers=HEADERS), timeout=10)
        response_text = response.read().decode('utf-8')
        soup = BeautifulSoup(response_text, "html.parser")
        return parse_metadata(soup, isbn, log)
    except Exception as e:
        log(f"获取元数据时出错: {e}")
        return None

def parse_metadata(soup, isbn, log):
    '''
    从BeautifulSoup对象中解析元数据。
    :param soup: BeautifulSoup对象。
    :param isbn: ISBN号码，作为字符串。
    :param log: 日志记录器。
    :return: 解析后的元数据或None（解析失败时）。
    '''
    data = {}
    prev_td1 = ''
    prev_td2 = ''

    try:
        table = soup.find("table", attrs={"id": "td"})
        if not table:
            return
    except Exception:
        return

    tr_elements = table.find_all('tr')

    for tr in tr_elements:
        td_elements = tr.find_all('td', class_='td1')
        if len(td_elements) == 2:
            td1 = td_elements[0].get_text(strip=True).replace('\n', '').replace('\xa0', ' ')
            td2 = td_elements[1].get_text(strip=True).replace('\n', '').replace('\xa0', ' ')
            if td1 == '' and td2 == '':
                continue
            if td1:
                data.update({td1: td2.strip()})
            else:
                data.update({prev_td1: '\n'.join([prev_td2, td2]).strip()})
            prev_td1 = td1.strip()
            prev_td2 = td2.strip()

    # 从'出版项'中使用正则表达式提取格式为[2019]的'pubdate'
    pubdate_match = re.search(r',\s*(\d{4})', data.get("出版项", ""))
    pubdate = pubdate_match.group(1) if pubdate_match else ""

    publisher_match = re.search(r':\s*(.+),\s', data.get("出版项", ""))
    publisher = publisher_match.group(1) if publisher_match else ""

    tags = data.get("主题", "").replace('--', '&')
    tags += f' & {data.get("中图分类号", "")}'
    tags += f' & {publisher}'
    tags += f' & {pubdate}'
    tags = tags.split(' & ')

    metadata = {
        "title": data.get("题名与责任", f"{isbn}"),
        "tags": tags,
        "comments": data.get("内容提要", ""),
        'publisher': publisher,
        'pubdate': pubdate,
        'authors': data.get("著者", "").split(' & '),
        "isbn": data.get(f"{isbn}", "")
    }

    return to_metadata(metadata, False, log)

def to_metadata(book, add_translator_to_author, log):
    '''
    将书籍信息转换为元数据对象。
    :param book: 书籍信息字典。
    :param add_translator_to_author: 是否将翻译者添加到作者列表中。
    :param log: 日志记录器。
    :return: 元数据对象。
    '''
    if book:
        authors = (book['authors'] + book['translators']
                   ) if add_translator_to_author and book.get('translators', None) else book['authors']
        mi = MetaInformation(book['title'], authors)
        mi.identifiers = {PROVIDER_ID: book['isbn']}
        # mi.url = book['url']
        # mi.cover = book.get('cover', None)
        mi.publisher = book['publisher']
        pubdate = book.get('pubdate', None)
        if pubdate:
            try:
                if re.compile('^\\d{4}-\\d+$').match(pubdate):
                    mi.pubdate = datetime.strptime(pubdate, '%Y-%m')
                elif re.compile('^\\d{4}-\\d+-\\d+$').match(pubdate):
                    mi.pubdate = datetime.strptime(pubdate, '%Y-%m-%d')
            except:
                log.error('解析出版日期失败 %r' % pubdate)
        mi.comments = book['comments']
        mi.tags = book.get('tags', [])
        mi.isbn = book.get('isbn', '')
        mi.language = 'zh_CN'
        return mi

class NLCISBNPlugin(Source):
    name = '国家图书馆ISBN插件'
    description = '使用ISBN从中国国家图书馆获取元数据的Calibre插件。'
    supported_platforms = ['windows', 'osx', 'linux']
    version = (1, 0, 0)
    author = 'Doiiars'
    capabilities = frozenset(['tags', 'identify', 'comments', 'pubdate'])

    def get_book_url(self, identifiers):
        return None

    def identify(self, log, result_queue, abort, title=None, authors=None, identifiers={}, timeout=30):
        isbn = identifiers.get('isbn', '')
        if not isbn:
            return

        metadata = isbn2meta(isbn, log)
        log('下载元数据:', metadata)
        if metadata:
            result_queue.put(metadata)

    def download_cover(self, log, result_queue, abort, title=None, authors=None, identifiers={}, timeout=30, get_best_cover=False):
        return

if __name__ == "__main__":
    from calibre.ebooks.metadata.sources.test import (
        test_identify_plugin, title_test, authors_test
    )

    test_identify_plugin(
        NLCISBNPlugin.name, [
            ({
                 'identifiers': {
                     'isbn': '9787111544937'
                 },
                 'title': '深入理解计算机系统（原书第3版）'
             }, [title_test('深入理解计算机系统（原书第3版）', exact=True),
                 authors_test(['randal e.bryant', "david o'hallaron", '贺莲', '龚奕利'])]),
            ({
                 'title': '凤凰架构'
             }, [title_test('凤凰架构:构建可靠的大型分布式系统', exact=True),
                 authors_test(['周志明'])])
        ]
    )
