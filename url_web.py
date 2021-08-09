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

ADDON_ID = 'plugin.video.horscine'

URL_ADRESSE = 'https://horscine.org/index.php'

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


def get_video_name_from_site(content_bs):
    "Extraire le titre de la vidéo"
    name_element = content_bs.find("h1", class_="entry-title")
    if name_element:
        return strip_all(name_element.text)
    else:
        return ''


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
    if genre_before_element:
        genre_before_iframe_element = genre_before_element.parent
        genre_next_iframe_element = genre_before_iframe_element.findNext('p')
        if not genre_next_iframe_element:
            genre_next_iframe_element = genre_before_iframe_element.parent.findNext('p')

        return genre_next_iframe_element.get_text()
    else:
        return ''


def get_video_description_from_site(content_bs):
    "Extraire la description de la vidéo..."
    description_synopsis = content_bs.find('h2', {'id': "synopsis"})
    if description_synopsis:
        description_next_synopsis = description_synopsis.findNext('p')
        return description_next_synopsis.get_text()
    else:
        return ''


def get_video_thumb_from_site(content_bs):
    "Extraire l'image de la vidéo..."
    thumb_element = content_bs.find('meta', {'property': "og:image"})
    if thumb_element:
        return thumb_element['content']
    else:
        return ''

def get_all_sections(content_bs=None):
    "Extraire les sections BeautifulSoup de la page Hors-Cine"

    if not content_bs:
        url_content= urllib.request.urlopen(URL_ADRESSE).read()
        liste_soup = BeautifulSoup(url_content, 'html.parser')
    else:
        liste_soup = content_bs

    list_categories = get_categories(liste_soup)
    job_section_elements = liste_soup.find_all("section", class_="elementor-section")
    for job_section_element in job_section_elements:
        # Vérifier si un lien URL est présent dans cette section...
        job_a_element = job_section_element.find("a", class_="elementor-post__thumbnail__link")
        # Vérifier si une "sous-section" est présente dans la section...
        job_section_souselement = job_section_element.find("section", class_="elementor-section")
        # Vérifier si une vidéo est présente et s'il n'y a pas de "sous-section"...
        if job_a_element and not job_section_souselement:
            title_element = job_section_element.find("h2", class_="elementor-heading-title elementor-size-default")
            if title_element and strip_all(title_element.text) in list_categories:
                yield job_section_element
    return
    yield


def get_section_category(category, content_bs=None):
    "Extraire la section BeautifulSoup de la page Hors-Cine de la catégorie en paramètre"

    if not content_bs:
        url_content= urllib.request.urlopen(URL_ADRESSE).read()
        liste_soup = BeautifulSoup(url_content, 'html.parser')
    else:
        liste_soup = content_bs

    retour_element = None
    job_section_elements = liste_soup.find_all("section", class_="elementor-section")
    if category in get_categories(liste_soup):
        for job_section_element in job_section_elements:
            # Vérifier si un lien URL est présent dans cette section...
            job_a_element = job_section_element.find("a", class_="elementor-post__thumbnail__link")
            # Vérifier si une "sous-section" est présente dans la section...
            job_section_souselement = job_section_element.find("section", class_="elementor-section")
            # Vérifier si une vidéo est présente et s'il n'y a pas de "sous-section"...
            if job_a_element and not job_section_souselement:
                title_element = job_section_element.find("h2", class_="elementor-heading-title elementor-size-default")
                if title_element and strip_all(title_element.text) == category:
                    retour_element = job_section_element
    return retour_element

def get_url_videos_site(section_element):
    "Get URL to video sites in the section element"

    if section_element != None:
        # job_a_elements = section_element.find_all("a", class_="elementor-post__thumbnail__link")
        job_a_elements = section_element.find_all("a")
        for job_a_element in job_a_elements:
            if job_a_element.find('img', {'alt': "image du film"}):
                yield job_a_element['href']

def get_content_video_site(url):
    "Get content_bs containing iframe video section"

    url_content = urllib.request.urlopen(url).read()
    liste_soup = BeautifulSoup(url_content, 'html.parser')

    content_site_element = liste_soup.find("iframe")
    if content_site_element:
        yield liste_soup
    else:
        for video_site in get_url_videos_site(liste_soup):

            url_content = urllib.request.urlopen(video_site).read()
            liste_soup2 = BeautifulSoup(url_content, 'html.parser')
            content_site_element = liste_soup2.find("iframe")
            if content_site_element:
                yield liste_soup2

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

    # if category in get_categories(liste_soup):
        # job_section_elements = liste_soup.find_all("section", class_="elementor-section")
        # for job_section_element in job_section_elements:
            # # Vérifier si un lien URL est présent dans cette section...
            # job_a_element = job_section_element.find("a", class_="elementor-post__thumbnail__link")
            # # Vérifier si une "sous-section" est présente dans la section...
            # job_section_souselement = job_section_element.find("section", class_="elementor-section")
            # # Vérifier si une vidéo est présente et s'il n'y a pas de "sous-section"...
            # if job_a_element and not job_section_souselement:
                # title_element = job_section_element.find("h2", class_="elementor-heading-title elementor-size-default")
                # # Vérifier le titre de la section est bien "category"...
                # if title_element and strip_all(title_element.text) == category:

    job_section_element = get_section_category(category, liste_soup)

    # if exists_video_section_element(job_section_element):

    for video_site in get_url_videos_site(job_section_element):

        for content_site_element in get_content_video_site(video_site):
            video_name = get_video_name_from_site(content_site_element)
            video_url = get_video_url_from_site(content_site_element)
            video_genre = get_video_genre_from_site(content_site_element)
            video_description = get_video_description_from_site(content_site_element)
            video_thumb = get_video_thumb_from_site(content_site_element)

            video_group_element = dict()
            video_group_element['name'] = video_name
            video_group_element['thumb'] = video_thumb
            video_group_element['video'] = video_url
            video_group_element['genre'] = video_genre
            video_group_element['description'] = video_description
            yield video_group_element

        # On récupère le contenu de la page de la vidéo de la section...
        # url_content= urllib.request.urlopen(video_url).read()
        # content_site_video_bs = BeautifulSoup(url_content, 'html.parser')
        # content_site_element = content_site_video_bs.find("iframe")

    # job_a_elements = job_section_element.find_all("a", class_="elementor-post__thumbnail__link")
    # for job_a_element in job_a_elements:
        # image_element  = job_a_element.find("img")
        # video_group_element = dict()
        # if image_element:

            # # On récupère le contenu de la page de la vidéo de la section...
            # url_content= urllib.request.urlopen(job_a_element['href']).read()
            # content_site_video_bs = BeautifulSoup(url_content, 'html.parser')

            # list_content_site_videos_bs = dict()
            # if content_site_video_bs.find("iframe"):
                # list_content_site_videos_bs.append(content_site_video_bs)
            # else:
                # list_content_site_videos_bs = content_site_video_bs.find_all("a", string = "Voir le film")
                # if list_content_site_videos_bs:
                    # for href_element in list_content_site_videos_bs:
                        # print(len(href_element))
                        # # On récupère le contenu de la sous-page de la vidéo...
                        # url_content= urllib.request.urlopen(href_element['href']).read()
                        # content_site_video_2_bs = BeautifulSoup(url_content, 'html.parser')
                        # if content_site_video_2_bs.find("iframe"):
                            # list_content_site_videos_bs.append(content_site_video_2_bs)

            # for content_site_element in list_content_site_videos_bs:

                # video_name = get_video_name_from_site(content_site_element)
                # video_url = get_video_url_from_site(content_site_element)
                # video_genre = get_video_genre_from_site(content_site_element)
                # video_description = get_video_description_from_site(content_site_element)

                # video_group_element['name'] = video_name
                # video_group_element['thumb'] = image_element['src']
                # video_group_element['video'] = video_url
                # video_group_element['genre'] = video_genre
                # video_group_element['description'] = video_description
                # yield video_group_element

    # else:
        # return
        # yield

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

        # On enlève les paramètres GET et on enlève le dernier "/"...
        without_extra_slash = os.path.normpath(urlpath[:urlpath.find('?', 0)])
        last_part = os.path.basename(without_extra_slash)

        return_path = 'plugin://plugin.video.vimeo/play/?video_id=' + last_part

    # Youtube
    elif domain.lower() == 'www.youtube.com':
        id_youtube = urlparse(path_video).query.split('=')[1]

        return_path = 'plugin://plugin.video.youtube/play/?video_id=' + id_youtube

    # Invidious
    # https://github.com/lekma/plugin.video.invidious
    elif domain.lower() == 'invidious.fdn.fr':
        # On enlève les paramètres GET et on enlève le dernier "/"...
        without_extra_slash = os.path.normpath(urlpath[:urlpath.find('?', 0)])
        last_part = os.path.basename(without_extra_slash)

        return_path = 'plugin://plugin.video.invidious/play/?video_id=' + last_part

    # Archive.org
    elif domain.lower() == 'archive.org':
        # On récupère le contenu de la page de la vidéo...
        url_content= urllib.request.urlopen(path_video).read()
        content_site_video_bs = BeautifulSoup(url_content, 'html.parser')
        new_url_video = content_site_video_bs.find('meta', {'property': "og:video"})
        if new_url_video:
            return_path = new_url_video['content']
        else:
            return_path = path_video

    # https://framagit.org/StCyr/plugin.video.peertube
    # Une instance de Peertube
    # elif domain.lower() == 'aperi.tube':
        # without_extra_slash = os.path.normpath(urlpath[:urlpath.find('?', 0)])
        # last_part = os.path.basename(without_extra_slash)

        # return_path = 'plugin://plugin.video.peertube/?action=play_video&instance=aperi.tube&id=' + last_part

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

def get_addondir():
    """
    Get addon dir with standard functions.
    """
    # Ça devrait donner ce chemin:
    #   /home/ubuntu/.kodi/userdata/addon_data/plugin.video.horscine/

    try:
        import xbmc
        import xbmcaddon

        __addon__ = xbmcaddon.Addon(id=ADDON_ID)
        __addondir__ = xbmc.translatePath(__addon__.getAddonInfo('profile')) #.decode('utf-8'))

        reponse = __addondir__

    except ImportError:
        reponse = '/home/ubuntu/.kodi/userdata/addon_data/plugin.video.horscine/'

    return reponse

def get_list_search_results(keywordsearch):
    """
    Generate list results
    """

    # f = open('myfile', 'w')
    # f.write(get_addondir())
    # f.close()

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
