#!/usr/bin/env python
#-*-coding:utf-8-*-

"""
    @Author: Soyn
    @Brief: The implement of search engine.
    @CretedTime: 3/3/16
    @Note: Refactor at 2/4/16 by Soyn.
"""

def AddToIndex(index, keyword, url):
    """
    @Brief:Format the index list to store the keyword and urls.
    Example:
            {'good', ["http://www.udacity.com"]}
    :param index: index list
    :param keyword: the keyword in url
    :param url: the irl
    :return:
    """
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]

def LookUp(index, keyword):
    """
    @Brief: Look up the urls associated with the keyword in index list.
    :param index: The index dictionary
    :param keyword: The keyword needs to look up.
    :return: The urls.
    """
    if keyword in index:
        return index[keyword]
    return None

def AddPageToIndex(index, url, content):
    """
    @Brief: Mapping the keyword in web page with url.
    :param index: The index dictionary
    :param url: The url.
    :param content: The Web page.
    :return:
    """
    words = content.split()
    for word in words:
        AddToIndex(index, word, url)

def RecordUserClicks(index, keyword, url):
    """
    @Brief: Record the user clicks counts.
    :param index: The index dictionary.
    :param keyword: The keyword user to search.
    :param url: The url refers to the keyword
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
    :param lst: The origin list
    :return: New string.
    """
    s = ""
    for elem in lst:
        s += elem
    return s

def MakeBigIndex(size):
    """
    @Brief: Construct the index automatically.
    :param size: The total size.
    :return: The index list.
    """
    index = {}
    letters = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
    while len(index) < size:
        word = MakeString(letters)
        print word
        AddToIndex(index, word, 'www.github.com')
        #following loop is to generate the specified index.
        for i in range(len(letters) - 1, 0, -1):
            if letters[i] < 'z':
                letters[i] = chr(ord(letters[i]) + 1)
                break
            else:
                letters[i] = 'a'
    return index

def ComputerRank(graph):
    """
    @Brief: Computer the rank of the page.
    :param graph: The graph generated by the seed page.
    :return: The ranks dictionary like:
    {"www.google.com": 4.12345, "www.baidu.com": 0.2222222}
    @Note: rank(page, 0) = 1 / number_of_pages
           rank(page, times) = (1 - damping_factor) + sum(d * rank(page, t - 1) /
           number_of_outlinks from page)
    """
    damping_factor = 0.8
    number_of_loop = 10
    number_of_page = len(graph)

    ranks = {}

    #initialize the ranks with specified value
    for page in graph:
        ranks[page] = 1.0 / number_of_page

    for i in range(0, number_of_loop):
        new_ranks = {}
        for page in graph:
            new_rank = (1 - damping_factor) / damping_factor
            for node in graph:
                if page in graph[node] and len(graph[page]):
                    new_rank += damping_factor * (ranks[node] / len(graph[page]))
            new_ranks[page] = new_rank
        ranks = new_ranks

    return ranks

def LuckyPage(index, ranks, keyword):
    """
    @Brief: Pick up the highest rank page.
    :param index: The index dictinary which stores the page.
    :param ranks: The rank graph.
    :param keyword: The keyword to search.
    :return: The highest rank page's url.
    """

    pages = search_engine.LookUp(index, keyword)
    if not page:
        return None
    best_page = pages[0]

    for candiate in pages:
        if ranks[candiate] > best_page:
            best_page = candiate
    return candiate

def QuickSortPages(pages, ranks):
    """
    @Brief: Sort the pages by rank from top to bottom.
    :param pages: The pages
    :param ranks: The ranks
    :return: Return a list which represented by the pages from top to bottom
    by rank.
    """

    if not page or len(pages) == 1:
        return pages
    else:
        pivot = ranks[pages[0]]
        worse = []
        better = []
        for page in pages[1 : ]:
            if ranks[page] <= pivot:
                worse.append(page)
            else:
                better.append(page)
    return QuickSortPages(better, ranks) + pages[0] + \
           QuickSortPages(worse, ranks)

def OrderedPages(index, ranks, keyword):
    """
    @Brief: Ordered pages using quick sort.
    :param index: The index contains the pages(or urls) correspond
                  to their keyword
    :param ranks: The ranks dictionary.
    :param keyword: Keyword need to search
    :return: Return the ordered list.
    """
    pages = search_engine.LookUp(index, keyword)
    return QuickSortPages(pages, ranks)