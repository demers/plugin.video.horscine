import url_web

import unittest

class GetWebTests(unittest.TestCase):

    def test_get_categories(self):
        categories_returned = url_web.get_categories()
        categories_expected = ['Le film de la semaine', 'Les autres nouveautés', 'Films au hasard']
        self.assertCountEqual(categories_expected, categories_returned)

    def test_get_videos_first(self):
        videos_returned = url_web.get_videos(list(url_web.get_categories())[0]) # Le film de la semaine
        videos_expected = [{'name': 'Emmanuel au milieu du désert', 'thumb': 'https://horscine.org/wp-content/uploads/emmanuel-au-milieu-du-desert.jpg', 'video': 'https://player.vimeo.com/video/300929489?dnt=1&app_id=122963&h=04ebfe8f68', 'genre': 'Avertissement : le film est réservé à un public adulte puisqu’il contient des scènes de sexe explicites.', 'description': 'Quand le vernis rose s’écaille à cause de la terre bêchée, comment expérimenter une homosexualité à la fois radicale et rurale ? Comment réinventer sa sexualité au milieu d’un désert ?'}]
        self.assertIn('name', videos_returned[0])
        self.assertIn('thumb', videos_returned[0])
        self.assertIn('video', videos_returned[0])
        self.assertIn('genre', videos_returned[0])
        self.assertIn('description', videos_returned[0])
        self.assertEqual(5, len(videos_returned[0]))

    def test_get_videos_second(self):
        videos_returned = url_web.get_videos(list(url_web.get_categories())[1]) # Les autres nouveautés
        videos_expected = [{'name': 'La Parade, ou la vie en pull bleu', 'thumb': 'https://horscine.org/wp-content/uploads/la-parade-ou-la-vie-en-pull-bleu.jpg', 'video': 'https://player.vimeo.com/video/45519017?dnt=1&app_id=122963', 'genre': 'Film'}, {'name': 'De rien', 'thumb': 'https://horscine.org/wp-content/uploads/de-rien.jpg', 'video': 'https://player.vimeo.com/video/367593464?dnt=1&app_id=122963', 'genre': 'Film'}, {'name': 'Artist 110', 'thumb': 'https://horscine.org/wp-content/uploads/ARTIST110.jpg', 'video': 'https://player.vimeo.com/video/202509514?dnt=1&app_id=122963', 'genre': 'Film'}]
        # self.assertCountEqual(videos_expected, videos_returned)
        self.assertEqual(10, len(videos_returned))

    def test_get_videos_third(self):
        videos_returned = url_web.get_videos(list(url_web.get_categories())[2]) # Films au hasard
        videos_expected = [{'name': "The cavalier's dream", 'thumb': 'https://horscine.org/wp-content/uploads/the-cavaliers-dream.jpg', 'video': 'https://archive.org/serve/CavaliersDream/Cavalier%27s_Dream.mp4', 'genre': 'Film'}, {'name': 'Spring', 'thumb': 'https://horscine.org/wp-content/uploads/2020/11/spring.jpg', 'video': 'https://player.vimeo.com/video/77059630?dnt=1&app_id=122963', 'genre': 'Film'}, {'name': 'The balloonatic', 'thumb': 'https://horscine.org/wp-content/uploads/theballoonatic.jpg', 'video': 'https://player.vimeo.com/video/1084537?dnt=1&app_id=122963', 'genre': 'Food'}]
        # self.assertCountEqual(videos_expected, videos_returned)
        self.assertEqual(9, len(videos_returned))

class SearchTests(unittest.TestCase):


    def test_list_search_results_movie_keyword(self):

        search_results_returned = url_web.get_list_search_results('lampe')
        search_results_expected = list()
        search_results_expected.append({'name': 'Danse serpentine par Mme Bob Walter',
                                        'thumb': 'https://horscine.org/wp-content/uploads/danse-serpentine-par-mme-bob-walter.jpg',
                                        'video': 'https://archive.org/embed/danse-serpentine-par-mme-bob-walter',
                                        'genre': 'D’Alice Guy – expérimental – 1 min 34 – 1897 – Domaine public',
                                        'description': 'Une émule de Loïe Fuller interprète la chorégraphie danse serpentine.'})

        self.assertCountEqual(search_results_expected, search_results_returned)


class ConvertTests(unittest.TestCase):

    def test_convert_video_path_vimeo(self):
        urlvimeo = url_web.convert_video_path('https://player.vimeo.com/video/123456?dnt=1&app_id=122963')

        self.assertEqual(urlvimeo, 'plugin://plugin.video.vimeo/play/?video_id=123456')

    def test_convert_video_path_youtube(self):
        urlyoutube = url_web.convert_video_path('https://www.youtube.com/watch?v=yHafN0M2kl0')

        self.assertEqual(urlyoutube, 'plugin://plugin.video.youtube/play/?video_id=yHafN0M2kl0')

    def test_convert_video_path_archive(self):
        urlarchive = url_web.convert_video_path('https://archive.org/embed/lhomme-de-la-rue')

        self.assertEqual(urlarchive, 'https://archive.org/download/lhomme-de-la-rue/lhomme-de-la-rue-DP.ia.mp4')

    def test_convert_video_path_invidious(self):
        urlarchive = url_web.convert_video_path('https://invidious.fdn.fr/watch?v=8Y-ObRQk5TA')

        self.assertEqual(urlarchive, 'plugin://plugin.video.invidious/play/?video_id=8Y-ObRQk5TA')

    def test_convert_video_path_peertube(self):
        urlarchive = url_web.convert_video_path('https://videos.lemnoslife.com/w/wd7TbkF35EY6DZ34E73Zio')

        self.assertEqual(urlarchive, 'plugin://plugin.video.peertube/?action=play_video&instance=videos.lemnoslife.com&id=wd7TbkF35EY6DZ34E73Zio')

    def test_convert_video_path_other(self):
        urlother = url_web.convert_video_path('https://gateway.pinata.cloud/ipfs/QmNjJBXWy9rd4ivxWPg8TGwDWv7fni1sQt89TdyEZjP3A4')

        self.assertEqual(urlother, 'https://gateway.pinata.cloud/ipfs/QmNjJBXWy9rd4ivxWPg8TGwDWv7fni1sQt89TdyEZjP3A4')


if __name__ == '__main__':
    unittest.main()

