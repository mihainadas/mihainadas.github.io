import unittest
from scripts.build_redirects import destination_file,render,build
class RedirectTests(unittest.TestCase):
    def test_all_published_pages_match_the_curated_map(self):build(check=True)
    def test_root_and_deep_destinations(self):
        self.assertEqual(destination_file('/'),'index.html')
        self.assertEqual(destination_file('/ro/cercetare/'),'ro/cercetare/index.html')
        self.assertEqual(destination_file('/2026/10/09/note.html'),'2026/10/09/note.html')
    def test_paths_cannot_escape_or_take_over_the_notebook_project(self):
        for route in ['/../outside.html','//evil.test/a.html','/notebooks/perceptron_en.html','/feed.xml','/a/?x=1']:
            with self.subTest(route=route),self.assertRaises(ValueError):destination_file(route)
    def test_destination_cannot_become_an_open_redirect(self):
        for target in ['https://evil.test/','http://nadas.ro/','https://nadas.ro.evil.test/','https://nadas.ro//x?target=a','https://nadas.ro/../outside/']:
            with self.subTest(target=target),self.assertRaises(ValueError):render(target)
    def test_refresh_works_without_javascript_and_matches_canonical(self):
        markup=render('https://nadas.ro/research/')
        head=markup.split('</head>')[0]
        self.assertIn('<meta http-equiv="refresh" content="0;url=https://nadas.ro/research/">',head)
        self.assertIn('<link rel="canonical" href="https://nadas.ro/research/">',head)
        self.assertNotIn('noindex',markup)
if __name__=='__main__':unittest.main()
