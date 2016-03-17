#!/usr/bin/env python
#-*-coding:utf-8-*-

"""
    @Author: Soyn
    @Brief: A simple web crawl and search engine implement.
    More details in Udacity CS101.
    @CreateTime: 3/3/16.S
"""

def GetPage(url):
    """
    @Brief: To get the web page content
    :param url: the link
    :return: the content by string in the url
    """
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def GetNextTarget(page):
    """
    @Brief: To extract a link from o page.
    :param page: the web page.
    :return:
    @url: the url we extracts from the page, if not found return None.
    @end_quote: the url's end quote's position in the page, if
    not found return -1.

    """
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0

    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1 : end_quote]
    return url, end_quote


def GetAllTheLinks(page):

    """
    @Brief: Extract all the links from the web page.
    :param page: the web page.
    :return: the the list of url.
    """
    links = []
    while True:
        url, end_position = GetNextTarget(page)
        if url:
            links.append(url)
            page = page[end_position :]
        else:
            break
    return links



def Union(first_list, second_list):
    """
    @Brief: To union two lists into one list.
    :param first_list:
    :param second_list:
    :return: None
    """
    for e in second_list:
        if e not in first_list:
            first_list.append(e)

def CrawlWeb(seed, max_depth):
    """
    @Brief: To crawl the page from the seed.
    @Soyn: Add the code to keep track of the crawl searches depth.(5/3/16).
    :param seed: the seed page.
    :return: the links are crawled.
    """
    to_crawl = [seed]
    crawled = []
    next_depth = []
    depth = 0
    index = {}
    graph = {}  # the graph for ranking
    while to_crawl and depth < max_depth:
        page = to_crawl.pop()
        if page not in crawled:
            content = GetPage(page)
            AddPageToIndex(index, page, content)
            outlinks = GetAllTheLinks(page)
            Union(next_depth, outlinks)
            crawled.append(page)
        if not to_crawl:
            to_crawl, next_depth = next_depth, []
            depth += 1
    return index, graph




def AddToIndex(index, keyword, url):
    """
    @Brief: Format the index list to store the keyword, urls, and counts.
    Example format data structure: ['good',[["http://www.udacity.com", 0],
    ["http://www.google.com"]]]
    :param index: index list
    :param keyword: the keyword in url
    :param url:
    :return:
    """
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url, 0]

def LookUp(index, keyword):
    """
    @Breif: Look up the urls assiciated with the keyword in index list.
    :param index:
    :param keyword:
    :return:
    """
    if keyword in index:
        return index[keyword]
    return None

def AddPageToIndex(index, url, content):
    """
    @Brief: Create the index list which map the keywords
    in content into the url
    :param index: the index list
    :param url: the url
    :param content: web page
    :return:
    """
    words = content.split()
    for word in words:
        AddToIndex(index, word, url)

def RecordUserClick(index, keyword, url):
    """
    @Brief: Record the user clicks counts.
    :param index: the index list
    :param keyword: the keyword user to search
    :param url: the url refers to the keyword
    :return:
    """
    urls = LookUp(index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] += 1

def MakeString(lst):
    """
    @Brief: Make a new string from the element in lst.
    :param lst: the origin list.
    :return: new string
    """
    s = ''
    for elem in lst:
        s += elem

    return s

def MakeBigIndex(size):
    """
    @Brief: construct the index automatically.
    :param size: the total size
    :return: the index list.
    """
    index = {}
    letters = ['a', 'a', 'a', 'a', 'a', 'a', 'a']
    while len(index) < size:
        word = MakeString(letters)
        AddToIndex(index, word, 'some string')
        # following loop is to generate the specified index.
        for i in range(len(letters) - 1, 0, -1):
            if letters[i] < 'z':
                letters[i] = chr(ord(letters[i]) + 1)
                break
            else:
                letters[i] = 'a'
    return index

def ComputeRanks(graph):
    """
    @Brief: Compute the rank of page
    :param graph: the graph generated by the seed page.
    :return: return the rank dictionary like:
    {"www.google.com": 4.12345,
     "www.baidu.com": 0.222222......}
    @Note: rank(page, 0) = 1 / number_of_pahes
           rank(page, times) = (1 - damping_factor) +
           sum(d * rank(page, t - 1) / number of outlinks from page)
    """
    damping_factor = 0.8
    number_of_loop = 10
    number_of_page = len(graph)

    ranks = {}

    # initialize the ranks
    for page in graph:
        print page
        ranks[page] = 1.0 / number_of_page

    for i in range(0, number_of_loop):
        new_ranks = {}
        for page in graph:
            new_rank = (1 - damping_factor) / damping_factor
            for node in graph:
                if page in graph[node]:
                    new_rank += d * (ranks[node] / len(graph[page]))
            new_ranks[page] = new_rank
        ranks = new_ranks
    return ranks

