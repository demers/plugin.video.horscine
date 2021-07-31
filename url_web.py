# -*- coding: utf-8 -*-
# Free sample videos are provided by horscine.org
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.

# Import librairies to manage urls
from urllib.parse import urlparse
import os.path

# Import libraries to analyse Web pages
from bs4 import BeautifulSoup
import urllib.request
# liste_soup = beautiful(browser.page_source)
# if liste_soup.find("td", {"class", "cPhoto"}) != None:
    # img = browser.find_element_by_xpath('//td[@class="cPhoto"]/img')
    # src = img.get_attribute('src')
# else:
    # src = ''
    # reponse = False

URL_ADRESSE = 'https://horscine.org/index.php'

VIDEOS = {'Le film de la semaine': [{'name': "L'homme de la rue",
                       'thumb': 'https://horscine.org/wp-content/uploads/Affiche-lhomme-de-la-rue.jpg',
                       'video': 'https://archive.org/serve/lhomme-de-la-rue/lhomme-de-la-rue-DP.ia.mp4',
                       'genre': 'Film'}
                      ],
            'Les autres nouveautés': [{'name': 'La Parade, ou la vie en pull bleu',
                      'thumb': 'https://horscine.org/wp-content/uploads/la-parade-ou-la-vie-en-pull-bleu.jpg',
                      'video': 'https://player.vimeo.com/video/45519017?dnt=1&app_id=122963',
                      'genre': 'Film'},
                     {'name': 'De rien',
                      'thumb': 'https://horscine.org/wp-content/uploads/de-rien.jpg',
                      'video': 'https://player.vimeo.com/video/367593464?dnt=1&app_id=122963',
                      'genre': 'Film'},
                     {'name': 'Artist 110',
                      'thumb': 'https://horscine.org/wp-content/uploads/ARTIST110.jpg',
                      'video': 'https://player.vimeo.com/video/202509514?dnt=1&app_id=122963',
                      'genre': 'Film'}
                     ],
            'Films au hasard': [{'name': "The cavalier's dream",
                      'thumb': 'https://horscine.org/wp-content/uploads/the-cavaliers-dream.jpg',
                      'video': 'https://archive.org/serve/CavaliersDream/Cavalier%27s_Dream.mp4',
                      'genre': 'Film'},
                     {'name': 'Spring',
                      'thumb': 'https://horscine.org/wp-content/uploads/2020/11/spring.jpg',
                      'video': 'https://player.vimeo.com/video/77059630?dnt=1&app_id=122963',
                      'genre': 'Film'},
                     {'name': 'The balloonatic',
                      'thumb': 'https://horscine.org/wp-content/uploads/theballoonatic.jpg',
                      'video': 'https://player.vimeo.com/video/1084537?dnt=1&app_id=122963',
                      'genre': 'Food'}
                     ]}

def get_categories_init():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or API.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: types.GeneratorType
    """
    return VIDEOS.keys()

def strip_all(chaine):
    return chaine.replace('\t', '').replace('\n', '').strip(' ')

def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or API.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: types.GeneratorType
    """

    url_content= urllib.request.urlopen(URL_ADRESSE).read()

    liste_soup = BeautifulSoup(url_content, 'html.parser')
    job_section_elements = liste_soup.find_all("section", class_="elementor-section")
    for job_section_element in job_section_elements:
        # job_a_elements = job_section_element.find_all("a", class_="elementor-post__thumbnail__link")
        # if len(job_a_elements) > 1:
        # print(list(job_section_element.find("a", class_="elementor-post__thumbnail__link")))
        if len(job_section_element.find_all("a", class_="elementor-post__thumbnail__link")) > 1:
            title_element = job_section_element.find("h2", class_="elementor-heading-title elementor-size-default")
            yield strip_all(title_element.text)


    # for job_element in job_elements:
        # print(job_element.text)
        # title_element = job_element.find("h2", class_="elementor-heading-title")
        # print(title_element)


    # if liste_soup.find("h2", {"class", "elementor-heading-title elementor-size-default"}) != None:
        # img = browser.find_element_by_xpath('//h2[@class="cPhoto"]/img')
        # src = img.get_attribute('src')
    # else:
        # src = ''
        # reponse = False

def get_videos_init(category):
    return VIDEOS[category]

def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or API.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    url_content= urllib.request.urlopen(URL_ADRESSE).read()

    liste_soup = BeautifulSoup(url_content, 'html.parser')

    list_videos_group = []
    if category in get_categories():
        job_section_elements = liste_soup.find_all("section", class_="elementor-section")
        for job_section_element in job_section_elements:
            # job_a_elements = job_section_element.find_all("a", class_="elementor-post__thumbnail__link")
            job_a_element = job_section_element.find("a", class_="elementor-post__thumbnail__link")
            job_section_souselement = job_section_element.find("section", class_="elementor-section")
            # Vérifier si une vidéo est présentée dans cette section...
            # if len(job_section_element.find_all("a", class_="elementor-post__thumbnail__link")) > 1:
            # if len(job_a_elements) > 1:
            if job_a_element and not job_section_souselement:
                title_element = job_section_element.find("h2", class_="elementor-heading-title elementor-size-default")
                if title_element and strip_all(title_element.text) == category:
                    job_a_elements = job_section_element.find_all("a", class_="elementor-post__thumbnail__link")
                    for job_a_element in job_a_elements:
                        image_element  = job_a_element.find("img")
                        if image_element:
                            video_group_element = dict()
                            video_group_element['name'] = category
                            video_group_element['thumb'] = image_element['src']
                            video_group_element['video'] = job_a_element['href']
                            video_group_element['genre'] = 'Film'
                            yield video_group_element

    else:
        return
        yield

def convert_video_path(path_video):
    """
    Convert path string to exact path string
    considering video type (Vimeo, Youtube, other).
    """

    # Extract domain name
    domain = urlparse(path_video).netloc

    # Extract path from URL
    urlpath = urlparse(path_video).path

    return_path = ''
    # Vimeo
    if domain.lower() == 'player.vimeo.com':

        without_extra_slash = os.path.normpath(urlpath)
        last_part = os.path.basename(without_extra_slash)

        return_path = 'plugin://plugin.video.vimeo/play/?video_id=' + last_part

    # Youtube
    elif domain.lower() == 'www.youtube.com':
        id_youtube = urlparse(path_video).query.split('=')[1]

        return_path = 'plugin://plugin.video.youtube/play/?video_id=' + id_youtube
    else:
        # No change
        return_path = path_video

    return return_path

def get_list_search_results(keywordsearch):
    """
    Generate list results
    """

    list_results = list()
    list_results.append({'name': 'De rien',
                      'thumb': 'https://horscine.org/wp-content/uploads/de-rien.jpg',
                      'video': 'https://player.vimeo.com/video/367593464?dnt=1&app_id=122963',
                      'genre': 'Film'})
    list_results.append({'name': 'The balloonatic',
                      'thumb': 'https://horscine.org/wp-content/uploads/theballoonatic.jpg',
                      'video': 'https://player.vimeo.com/video/1084537?dnt=1&app_id=122963',
                      'genre': 'Food'})
    return list_results

