# -*- coding: utf-8 -*-
# Free sample videos are provided by horscine.org
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video
# files/streams
# from some web-site or online service.

# Import librairies to manage urls

import sys

# Python 3 versus Python 2
# if ((3, 0) <= sys.version_info <= (3, 9)):
    # # import urllib.parse
    # from urllib.parse import urlparse
    # # import urllib.request
    # from urllib.request import urlopen
# elif ((2, 0) <= sys.version_info <= (2, 9)):
    # from urlparse import urlparse
    # from urllib2 import urlopen

from urllib.parse import urlparse
from urllib.parse import quote
from urllib.request import Request, urlopen

import os.path

# Import libraries to analyse Web pages
from bs4 import BeautifulSoup

# import arrow
import os

import json
import hashlib

import datetime

# Variable disponible tout au long de l'exécution du script
CATEGORIES_WITH_URL = []

URL_PREFIXE = 'https://horscine.org'
URL_ADRESSE_PRINCIPALE = URL_PREFIXE + '/index.php'
URL_ADRESSE = URL_ADRESSE_PRINCIPALE

URL_ADRESSE_RSS = 'https://horscine.org/film/feed/rss2/'

ADDON_ID = 'plugin.video.horscine'

RSS_TEXTE = 'Derniers ajouts'

FICHIER_CATEGORIES = 'get_categories.json'
FICHIER_VIDEOS = 'get_videos_'  # On ajoutera sha1 et .json
FICHIER_VIDEOS_DOMAINS = 'list_url_domains.json'

NOMBRE_JOURS_DELAI_CATEGORIES = 13
NOMBRE_JOURS_DELAI_VIDEOS = 2

def strip_all(chaine):
    """
    Remove non-visible char beginning and end of string.
    Remove carriage return also.
    Remove spaces char beginning and end of string.
    """
    return chaine.replace('\t', '').replace('\n', '').replace('\r', '').strip(' ')

def read_url(url_text):
    "Chargement d'une page Web de façon sécuritaire"
    req = Request(url_text, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        url_content = urlopen(req).read()
    except:
        url_content = None

    return url_content

# def add_rss_category(content_bs, categories_url):
    # "Cherche une categorie rss et retourne la nouvelle liste"

    # retour_categories_url = categories_url
    # job_rss_element = content_bs.find('link', {'type': "application/rss+xml"})
    # if job_rss_element and job_rss_element.has_attr('href'):
        # url_rss = verify_url_prefixe(job_rss_element['href'], URL_PREFIXE)
        # retour_categories_url.append((RSS_TEXTE, url_rss))
    # return retour_categories_url

# def verify_url_prefixe(chaine_url, prefixe_url):
def verify_url(chaine_url, prefixe_url):
    "Ajouter domaine http au début si non présent et modifier &"

    chaine_url_and = chaine_url.replace('&#038;', '&')
    chaine_url_and_return = chaine_url_and

    if chaine_url_and[0:4] != 'http':
        chaine_url_and_return = prefixe_url + chaine_url_and

    return chaine_url_and_return

def get_video_content(chaine_url):
    # Chargement de la page des vidéos...
    url_content = read_url(chaine_url)

    return BeautifulSoup(url_content, 'html.parser')

def get_categories(content_bs=None):

    # Variable disponible tout au long de l'exécution du script
    global CATEGORIES_WITH_URL

    retour_categories_url = []

    # CATEGORIES_WITH_URL = retour_categories_url
    CATEGORIES_WITH_URL = (RSS_TEXTE, URL_ADRESSE_RSS)
    # return [category_tuple[0] for category_tuple in retour_categories_url]
    return RSS_TEXTE

# def get_categories(content_bs=None):
    # """
    # Get the list of video categories.

    # Here you can insert some parsing code that retrieves
    # the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    # from some site or API.

    # .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        # instead of returning lists.

    # :return: The list of video categories
    # :rtype: types.GeneratorType
    # """

    # chemin_fichier_cat = get_addondir() + FICHIER_CATEGORIES

    # retour_categories = []
    # # if not content_bs and not check_file_older_than(chemin_fichier_cat, NOMBRE_JOURS_DELAI_CATEGORIES):
    # if not check_file_older_than(chemin_fichier_cat, NOMBRE_JOURS_DELAI_CATEGORIES):
        # retour_categories = load_dict(chemin_fichier_cat)
    # else:
        # if not content_bs:
            # # url_content= urllib.request.urlopen(URL_ADRESSE).read()
            # # url_content= urlopen(URL_ADRESSE).read()
            # url_content= read_url(URL_ADRESSE)
            # liste_soup = BeautifulSoup(url_content, 'html.parser')
        # else:
            # liste_soup = content_bs

        # job_section_elements = liste_soup.find_all("section", class_="elementor-section")
        # for job_section_element in job_section_elements:
            # # Vérifier si une "sous-section" est présente dans la section...
            # job_sous_section_elements = job_section_element.find_all("section", class_="elementor-section")
            # # Vérifier si la "sous-section" est absente et s'il y a un URL...
            # if not job_sous_section_elements and job_section_element.find("a", class_="elementor-post__thumbnail__link"):
                # title_element = job_section_element.find("h2", class_="elementor-heading-title elementor-size-default")
                # # yield strip_all(title_element.text)
                # retour_categories.append(strip_all(title_element.text))
        # save_dict(retour_categories, chemin_fichier_cat)
    # return retour_categories

def get_video_name_from_site(content_bs):
    "Extraire le titre de la vidéo"
    name_element = content_bs.find("h1", class_="elementor-heading-title")
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
    meta_element = content_bs.find("div", class_="film__meta")
    if meta_element:
        return strip_all(meta_element.get_text())
    else:
        return ''

# ACORRIGER
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

# def get_all_sections(content_bs=None):
    # "Extraire les sections BeautifulSoup de la page Hors-Cine"

    # if not content_bs:
        # # url_content= urllib.request.urlopen(URL_ADRESSE).read()
        # url_content= urlopen(URL_ADRESSE).read()
        # liste_soup = BeautifulSoup(url_content, 'html.parser')
    # else:
        # liste_soup = content_bs

    # list_categories = get_categories(liste_soup)
    # job_section_elements = liste_soup.find_all("section", class_="elementor-section")
    # for job_section_element in job_section_elements:
        # # Vérifier si un lien URL est présent dans cette section...
        # job_a_element = job_section_element.find("a")
        # # Vérifier si une "sous-section" est présente dans la section...
        # job_section_souselement = job_section_element.find("section")
        # # Vérifier si une vidéo est présente et s'il n'y a pas de "sous-section"...
        # if job_a_element and not job_section_souselement:
            # title_element = job_section_element.find("h2")
            # if title_element and strip_all(title_element.text) in list_categories:
                # yield job_section_element
    # return
    # yield


# def get_section_category(category, content_bs=None):
    # "Extraire la section BeautifulSoup de la page Hors-Cine de la catégorie en paramètre"

    # if not content_bs:
        # # url_content= urllib.request.urlopen(URL_ADRESSE).read()
        # url_content= urlopen(URL_ADRESSE).read()
        # liste_soup = BeautifulSoup(url_content, 'html.parser')
    # else:
        # liste_soup = content_bs

    # retour_element = None
    # job_section_elements = liste_soup.find_all("section", class_="elementor-section")
    # if category in get_categories(liste_soup):
        # for job_section_element in job_section_elements:
            # # Vérifier si un lien URL est présent dans cette section...
            # job_a_element = job_section_element.find("a", class_="elementor-post__thumbnail__link")
            # # Vérifier si une "sous-section" est présente dans la section...
            # job_section_souselement = job_section_element.find("section", class_="elementor-section")
            # # Vérifier si une vidéo est présente et s'il n'y a pas de "sous-section"...
            # if job_a_element and not job_section_souselement:
                # title_element = job_section_element.find("h2", class_="elementor-heading-title elementor-size-default")
                # if title_element and strip_all(title_element.text) == category:
                    # retour_element = job_section_element
                    # # Quand la catégorie est trouvée, il n'est plus nécessaire de rester dans la boucle...
                    # break
    # return retour_element

# def get_href_section(section_element):
    # "Get URL to href element in the section element"

    # if section_element != None:
        # job_a_elements = section_element.find_all("a", class_="elementor-post__thumbnail__link")
        # for job_a_element in job_a_elements:
            # if job_a_element.find('img'):
                # yield job_a_element['href']

# def exists_video_section_element(section_element):
    # "Check if exists video URL in the section element"

    # retour_bool = False
    # if section_element != None:
        # job_a_elements = section_element.find_all("a")
        # for job_a_element in job_a_elements:
            # if job_a_element.find('img', {'alt': "image du film"}):
                # retour_bool = True
    # return retour_bool


def get_url_videos_site(section_element):
    "Get URL to video sites in the section element"

    if section_element != None:
        job_a_elements = section_element.find_all("a")
        for job_a_element in job_a_elements:
            if job_a_element.find('img', {'alt': "image du film"}):
                yield job_a_element['href']

def get_content_video_site(url):
    "Get content_bs containing iframe video section"

    # url_content = urllib.request.urlopen(url).read()
    url_content = urlopen(url).read()
    liste_soup = BeautifulSoup(url_content, 'html.parser')

    content_site_element = liste_soup.find("iframe")
    if content_site_element:
        yield liste_soup
    else:
        for video_site in get_url_videos_site(liste_soup):

            # url_content = urllib.request.urlopen(video_site).read()
            url_content = urlopen(video_site).read()
            liste_soup2 = BeautifulSoup(url_content, 'html.parser')
            content_site_element = liste_soup2.find("iframe")
            if content_site_element:
                yield liste_soup2

def append_video(video_element, liste_videos):
    "Ajoute une vidéo dans le dictionnaire sans répétition seulement"

    test_ajout = True

    # Si le champ est vide, on n'ajoute pas...
    if not video_element['video']:
        test_ajout = False

    if test_ajout:
        # On vérifie l'URL est la même...
        for element in liste_videos:
            if element['video'] == video_element['video']:
                test_ajout = False

    if test_ajout:
        liste_videos.append(video_element)


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

    retour_videos = []
    url_category = ''


    # Vérifier si la variable de la liste des catégories n'est pas vide.
    if not CATEGORIES_WITH_URL:
        get_categories()
    if category in dict(CATEGORIES_WITH_URL):
        url_category = (dict(CATEGORIES_WITH_URL))[category]

    # Chargement seulement si l'URL existe...
    if url_category:

        # Chargement de la page des vidéos...
        url_content = read_url(url_category)

        liste_soup_category = BeautifulSoup(url_content, 'html5lib')

        articles_soupe = liste_soup_category.findAll('item')
        for article in articles_soupe:
            video_group_element = dict()
            # On cherche l'URL d'un item du fil RSS...
            guid_soup = article.find('guid')
            if guid_soup:
                article_link = strip_all(guid_soup.text)
                url_content = read_url(verify_url(article_link, URL_PREFIXE))
                if url_content:
                    liste_soup_video = BeautifulSoup(url_content, 'html.parser')
                    video_group_element['name'] = get_video_name_from_site(liste_soup_video)
                    video_group_element['video'] = get_video_url_from_site(liste_soup_video)
                    video_group_element['thumb'] = get_video_thumb_from_site(liste_soup_video)
                    video_group_element['genre'] = get_video_genre_from_site(liste_soup_video)
                    video_group_element['description'] = get_video_description_from_site(liste_soup_video)
                    append_video(video_group_element, retour_videos)

    return retour_videos

# def get_videos(category):
    # chemin_fichier_videos = get_addondir() + FICHIER_VIDEOS + hashlib.sha1(category.encode('utf-8')).hexdigest() + '.json'
    # retour_videos = []

    # if not check_file_older_than(chemin_fichier_videos, NOMBRE_JOURS_DELAI_VIDEOS):
        # retour_videos = load_dict(chemin_fichier_videos)
    # else:

        # # url_content= urllib.request.urlopen(URL_ADRESSE).read()
        # url_content= urlopen(URL_ADRESSE).read()
        # liste_soup = BeautifulSoup(url_content, 'html.parser')

        # job_section_element = get_section_category(category, liste_soup)

        # if not exists_video_section_element(job_section_element):
            # list_url_videos_site = []
            # for url_section in get_href_section(job_section_element):
                # # url_content = urllib.request.urlopen(url_section).read()
                # url_content = urlopen(url_section).read()
                # subsection_bs = BeautifulSoup(url_content, 'html.parser')
                # list_videos_subsection = get_url_videos_site(subsection_bs)
                # list_url_videos_site = list_url_videos_site + list(get_url_videos_site(subsection_bs))
        # else:
            # list_url_videos_site = get_url_videos_site(job_section_element)

        # for video_site in list_url_videos_site:

            # for content_site_element in get_content_video_site(video_site):
                # video_name = get_video_name_from_site(content_site_element)
                # video_url = get_video_url_from_site(content_site_element)
                # video_genre = get_video_genre_from_site(content_site_element)
                # video_description = get_video_description_from_site(content_site_element)
                # video_thumb = get_video_thumb_from_site(content_site_element)

                # video_group_element = dict()
                # video_group_element['name'] = video_name
                # video_group_element['thumb'] = video_thumb
                # video_group_element['video'] = video_url
                # video_group_element['genre'] = video_genre
                # video_group_element['description'] = video_description

                # # yield video_group_element
                # retour_videos.append(video_group_element)

        # save_dict(retour_videos, chemin_fichier_videos)
    # return retour_videos

def check_invidious(url_test):
    "Verify if web site is using Invidious"
    peertube_url = 'https://' + url_test
    url_content = urlopen(peertube_url).read()
    content_site_peertube = BeautifulSoup(url_content, 'html.parser')
    # site_id_bs = content_site_peertube.find('meta', {'property': "og:site_name"})
    site_id_bs = content_site_peertube.find('link', {'title': "Invidious"})
    return site_id_bs

def check_peertube(url_test):
    "Verify if web site is using Peertube"
    peertube_url = 'https://' + url_test
    url_content = urlopen(peertube_url).read()
    content_site_peertube = BeautifulSoup(url_content, 'html.parser')
    site_id_bs = content_site_peertube.find('meta', {'property': "og:platform"})
    site_id = ''
    if site_id_bs:
        # Vérifier si c'est un site Peertube
        site_id = site_id_bs['content'].lower()
    return site_id.lower() == 'peertube'

def convert_video_path(path_video):
    """
    Convert path string to exact path string
    considering video type (Vimeo, Youtube, other).
    """

    # Extract domain name
    # domain = urllib.parse.urlparse(path_video).netloc
    domain = urlparse(path_video).netloc

    # Extract path from URL
    # urlpath = urllib.parse.urlparse(path_video).path
    urlpath = urlparse(path_video).path

    # Pas de changement si on ne détecte pas le type de serveur...
    return_path = path_video

    # Vimeo
    if domain.lower() == 'player.vimeo.com':

        # On enlève les paramètres GET et on enlève le dernier "/"...
        if urlpath.endswith('/'):
            urlpath_noslash = urlpath[:-1]
        else:
            urlpath_noslash = urlpath

        last_part = os.path.basename(os.path.normpath(urlpath_noslash))

        return_path = 'plugin://plugin.video.vimeo/play/?video_id=' + last_part

    # Youtube
    elif domain.lower() == 'www.youtube.com':
        id_youtube = urlparse(path_video).query.split('=')[1]

        return_path = 'plugin://plugin.video.youtube/play/?video_id=' + id_youtube

    # Archive.org
    elif domain.lower() == 'archive.org':
        # On récupère le contenu de la page de la vidéo...
        # url_content= urllib.request.urlopen(path_video).read()
        url_content= urlopen(path_video).read()
        content_site_video_bs = BeautifulSoup(url_content, 'html.parser')
        new_url_video = content_site_video_bs.find('meta', {'property': "og:video"})
        if new_url_video:
            return_path = new_url_video['content']
        else:
            return_path = path_video

    # Invidious
    # https://github.com/lekma/plugin.video.invidious
    elif check_invidious(domain.lower()):
        # On enlève les paramètres GET et on enlève le dernier "/"...
        if urlpath.endswith('/'):
            urlpath_noslash = urlpath[:-1]
        else:
            urlpath_noslash = urlpath
        id_invidious = urlparse(path_video).query.split('=')[1]

        return_path = 'plugin://plugin.video.invidious/play/?video_id=' + id_invidious

    # Peertube
    elif check_peertube(domain.lower()):
        if urlpath.endswith('/'):
            urlpath_noslash = urlpath[:-1]
        else:
            urlpath_noslash = urlpath
        last_part = os.path.basename(os.path.normpath(urlpath_noslash))

        return_path = 'plugin://plugin.video.peertube/?action=play_video&instance=' + domain.lower() + '&id=' + last_part

    else:

        chemin_fichier_url_domains = get_addondir() + FICHIER_VIDEOS_DOMAINS

        present_in_file = False
        if os.path.exists(chemin_fichier_url_domains):
            file = open(chemin_fichier_url_domains, 'r')
            if path_video in file.read():
                present_in_file = True
            file.close()

        if not present_in_file:
            try:
                file = open(chemin_fichier_url_domains, 'a')
            except IOError:
                file.close()
            finally:
                file.write(path_video + "\n")
                file.close()

    return return_path


def is_iterator(obj):
    "Verify if obj is an iterator type."
    if (
            hasattr(obj, '__iter__') and
            hasattr(obj, '__next__') and      # or __next__ in Python 3
            callable(obj.__iter__) and
            obj.__iter__() is obj
        ):
        return True
    else:
        return False


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
        __addondir__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))

        reponse = __addondir__

    except ImportError:
        # reponse = '/home/ubuntu/.kodi/userdata/addon_data/plugin.video.horscine/'
        reponse = '/home/ubuntu/.kodi/userdata/addon_data/' + ADDON_ID + '/'

    if not os.path.exists(reponse):
        os.mkdir(reponse)

    return reponse

# def check_file_older_than(fichier, jours_max, hasard_actif=False):
    # """
    # Verify if file is old than a certain number of days jours_max.
    # If file does not exist, the answer is true.
    # If hasard_actif, le number of days is between 1 and jours_max
    # """

    # fichier_date = fichier + '.date'

    # if hasard_actif:
        # jours = get_random_day(jours_max)
    # else:
        # jours = jours_max

    # retour_bool = False
    # if not (os.path.isfile(fichier) and os.path.isfile(fichier_date)):
        # retour_bool = True
    # else:
        # criticalTime = datetime.datetime.today() - datetime.timedelta(days=jours)
        # try:
            # file_date = open(fichier_date, 'r')
        # except IOError:
            # return retour_bool

        # finally:
            # content_time = strip_all(file_date.read())
            # try:
                # itemTime = datetime.datetime.strptime(content_time, "%Y-%m-%d")
            # except TypeError:
                # import time
                # itemTime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(content_time, "%Y-%m-%d")))

            # if itemTime < criticalTime:
                # retour_bool = True
            # file_date.close()
    # return retour_bool

# def save_dict(data_dict, fichier):
    # """
    # Save data structure dict in a file.
    # """
    # fichier_date = fichier + '.date'
    # retour_reussite = True
    # try:
        # file = open(fichier, 'w')
        # file_date = open(fichier_date, 'w')
    # except IOError:
        # retour_reussite = False
        # return retour_reussite
    # finally:
        # file.write(json.dumps(data_dict, indent=4))
        # file_date.write(datetime.datetime.now().strftime("%Y-%m-%d"))
        # file.close()
        # file_date.close()
        # return retour_reussite


# def load_dict(fichier):
    # """
    # Load data structure dict save in a file
    # """
    # struct_dict = dict()
    # try:
        # file = open(fichier, 'r')
    # except IOError:
        # file.close()
        # return struct_dict
    # finally:
        # struct_dict = json.loads(file.read())
        # file.close()
        # return struct_dict


def get_list_search_results(keywordsearch):
    """
    Generate list results
    """

    # https://horscine.org/?s=test
    NOUV_URL_ADRESSE = URL_ADRESSE + '?s=' + keywordsearch
    # url_content= urllib.request.urlopen(NOUV_URL_ADRESSE).read()
    # url_content= urlopen(NOUV_URL_ADRESSE).read()
    url_content= read_url(NOUV_URL_ADRESSE)
    liste_soup = BeautifulSoup(url_content, 'html.parser')

    article_elements = liste_soup.find_all("article", class_="film")

    for article_element in article_elements:

        video_group_element = dict()
        job_h2_element = article_element.find("h2", class_="entry-title")
        href_element  = job_h2_element.find("a", {'rel': "bookmark"})

        # On récupère le contenu de la page de la vidéo...
        # url_content= urllib.request.urlopen(href_element['href']).read()
        # url_content= urlopen(href_element['href']).read()
        url_content= read_url(href_element['href'])
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
