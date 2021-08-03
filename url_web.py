# -*- coding: utf-8 -*-
# Free sample videos are provided by horscine.org
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video
# files/streams
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
                       'genre': 'Film',
                        'description': 'Voici ma description.'}
                      ],
            'Les autres nouveautés': [{'name': 'La Parade, ou la vie en pull bleu',
                      'thumb': 'https://horscine.org/wp-content/uploads/la-parade-ou-la-vie-en-pull-bleu.jpg',
                      'video': 'https://player.vimeo.com/video/45519017?dnt=1&app_id=122963',
                      'genre': 'Film',
                        'description': 'Voici ma description.'},
                     {'name': 'De rien',
                      'thumb': 'https://horscine.org/wp-content/uploads/de-rien.jpg',
                      'video': 'https://player.vimeo.com/video/367593464?dnt=1&app_id=122963',
                      'genre': 'Film',
                      'description': 'Voici ma description.'},
                     {'name': 'Artist 110',
                      'thumb': 'https://horscine.org/wp-content/uploads/ARTIST110.jpg',
                      'video': 'https://player.vimeo.com/video/202509514?dnt=1&app_id=122963',
                      'genre': 'Film',
                      'description': 'Voici ma description.'}
                     ],
            'Films au hasard': [{'name': "The cavalier's dream",
                      'thumb': 'https://horscine.org/wp-content/uploads/the-cavaliers-dream.jpg',
                      'video': 'https://archive.org/serve/CavaliersDream/Cavalier%27s_Dream.mp4',
                      'genre': 'Film',
                      'description': 'Voici ma description.'},
                     {'name': 'Spring',
                      'thumb': 'https://horscine.org/wp-content/uploads/2020/11/spring.jpg',
                      'video': 'https://player.vimeo.com/video/77059630?dnt=1&app_id=122963',
                      'genre': 'Film',
                      'description': 'Voici ma description.'},
                     {'name': 'The balloonatic',
                      'thumb': 'https://horscine.org/wp-content/uploads/theballoonatic.jpg',
                      'video': 'https://player.vimeo.com/video/1084537?dnt=1&app_id=122963',
                      'genre': 'Food',
                      'description': 'Voici ma description.'}
                     ]}


def get_categories_init():
    """
    À enlever...
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
    """
    Remove non-visible char beginning and end of string.
    Remove carriage return also.
    Remove spaces char beginning and end of string.
    """
    return chaine.replace('\t', '').replace('\n', '').replace('\r', '').strip(' ')

def get_categories(content_bs=None):
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

    if not content_bs:
        url_content= urllib.request.urlopen(URL_ADRESSE).read()
        liste_soup = BeautifulSoup(url_content, 'html.parser')
    else:
        liste_soup = content_bs

    job_section_elements = liste_soup.find_all("section", class_="elementor-section")
    for job_section_element in job_section_elements:
        # Vérifier si une "sous-section" est présente dans la section...
        job_sous_section_elements = job_section_element.find_all("section", class_="elementor-section")
        # Vérifier si la "sous-section" est absente et s'il y a un URL...
        if not job_sous_section_elements and job_section_element.find("a", class_="elementor-post__thumbnail__link"):
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


def get_video_name_from_site(content_bs):
    "Extraire le titre de la vidéo"
    name_element = content_bs.find("h1", class_="entry-title")
    return strip_all(name_element.text)


def get_video_url_from_site(content_bs):
    "Extraire l'URL de la vidéo"
    url_element = content_bs.find("iframe")
    if not url_element:
        retour = ''
    else:
        retour = url_element['src']

    return retour


def get_video_genre_from_site(content_bs):
    "Extraire le genre de la vidéo"
    genre_before_element = content_bs.find("iframe")
    genre_before_iframe_element = genre_before_element.parent
    genre_next_iframe_element = genre_before_iframe_element.findNext('p')
    if not genre_next_iframe_element:
        genre_next_iframe_element = genre_before_iframe_element.parent.findNext('p')

    return genre_next_iframe_element.get_text()

def get_video_description_from_site(content_bs):
    "Extraire la description de la vidéo..."
    description_synopsis = content_bs.find('h2', {'id': "synopsis"})
    description_next_synopsis = description_synopsis.findNext('p')
    return description_next_synopsis.get_text()

def get_video_thumb_from_site(content_bs):
    "Extraire l'image de la vidéo..."
    thumb_element = content_bs.find('meta', {'property': "og:image"})
    return thumb_element['content']

def get_videos_init(category):
    "à enlever"
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

    if category in get_categories(liste_soup):
        job_section_elements = liste_soup.find_all("section", class_="elementor-section")
        for job_section_element in job_section_elements:
            # Vérifier si un lien URL est présent dans cette section...
            job_a_element = job_section_element.find("a", class_="elementor-post__thumbnail__link")
            # Vérifier si une "sous-section" est présente dans la section...
            job_section_souselement = job_section_element.find("section", class_="elementor-section")
            # Vérifier si une vidéo est présente et s'il n'y a pas de "sous-section"...
            if job_a_element and not job_section_souselement:
                title_element = job_section_element.find("h2", class_="elementor-heading-title elementor-size-default")
                # Vérifier le titre de la section est bien "category"...
                if title_element and strip_all(title_element.text) == category:
                    job_a_elements = job_section_element.find_all("a", class_="elementor-post__thumbnail__link")
                    for job_a_element in job_a_elements:
                        image_element  = job_a_element.find("img")
                        video_group_element = dict()
                        if image_element:

                            # On récupère le contenu de la page de la vidéo...
                            url_content= urllib.request.urlopen(job_a_element['href']).read()
                            content_site_video_bs = BeautifulSoup(url_content, 'html.parser')

                            video_name = get_video_name_from_site(content_site_video_bs)
                            video_url = get_video_url_from_site(content_site_video_bs)
                            video_genre = get_video_genre_from_site(content_site_video_bs)
                            video_description = get_video_description_from_site(content_site_video_bs)

                            video_group_element['name'] = video_name
                            video_group_element['thumb'] = image_element['src']
                            video_group_element['video'] = video_url
                            video_group_element['genre'] = video_genre
                            video_group_element['description'] = video_description
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

def get_list_search_results_init(keywordsearch):
    """
    À enlever
    Generate list results
    """

    list_results = list()
    list_results.append({'name': 'De rien',
                      'thumb': 'https://horscine.org/wp-content/uploads/de-rien.jpg',
                      'video': 'https://player.vimeo.com/video/367593464?dnt=1&app_id=122963',
                      'genre': 'Film',
                      'description': 'Voici ma description.'})
    list_results.append({'name': 'The balloonatic',
                      'thumb': 'https://horscine.org/wp-content/uploads/theballoonatic.jpg',
                      'video': 'https://player.vimeo.com/video/1084537?dnt=1&app_id=122963',
                      'genre': 'Food',
                      'description': 'Voici ma description.'})
    return list_results

def get_list_search_results(keywordsearch):
    """
    Generate list results
    """
    # https://horscine.org/?s=test
    NOUV_URL_ADRESSE = URL_ADRESSE + '?s=' + keywordsearch
    url_content= urllib.request.urlopen(NOUV_URL_ADRESSE).read()
    liste_soup = BeautifulSoup(url_content, 'html.parser')

    article_elements = liste_soup.find_all("article", class_="film")

    for article_element in article_elements:

        video_group_element = dict()
        job_h2_element = article_element.find("h2", class_="entry-title")
        href_element  = job_h2_element.find("a", {'rel': "bookmark"})

        # On récupère le contenu de la page de la vidéo...
        url_content= urllib.request.urlopen(href_element['href']).read()
        content_site_video_bs = BeautifulSoup(url_content, 'html.parser')

        video_name = get_video_name_from_site(content_site_video_bs)
        video_thumb = get_video_thumb_from_site(content_site_video_bs)
        video_url = get_video_url_from_site(content_site_video_bs)
        video_genre = get_video_genre_from_site(content_site_video_bs)
        video_description = get_video_description_from_site(content_site_video_bs)

        video_group_element['name'] = video_name
        video_group_element['thumb'] = video_thumb
        video_group_element['video'] = video_url
        video_group_element['genre'] = video_genre
        video_group_element['description'] = video_description
        yield video_group_element
