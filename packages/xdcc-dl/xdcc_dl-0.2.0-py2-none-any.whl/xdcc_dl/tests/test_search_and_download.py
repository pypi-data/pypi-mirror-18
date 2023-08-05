u"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of xdcc_dl.

    xdcc_dl is a program that allows downloading files via hte XDCC
    protocol via file serving bots on IRC networks.

    xdcc_dl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    xdcc_dl is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with xdcc_dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
import os
import unittest
from xdcc_dl.main import generate_random_username
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher
from xdcc_dl.xdcc.MultipleServerDownloader import MultipleServerDownloader


class UnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        if os.path.isfile(u"Ginpachi.txt"):
            os.remove(u"Ginpachi.txt")
        if os.path.isfile(u"Sadaharu.txt"):
            os.remove(u"Sadaharu.txt")

    def test_gin_search_download(self):

        search_results = PackSearcher([u"nibl", u"intel_haruhichan"]).search(u"Gin.txt")
        self.assertEqual(len(search_results), 2)

        search_results[0].set_filename(u"Gintoki.txt", override=True)
        search_results[1].set_filename(u"Sadaharu.txt", override=True)

        download_results = MultipleServerDownloader(generate_random_username(), 2).download(search_results)

        for download in download_results:
            self.assertEqual(download_results[download], u"OK")

        for result in search_results:
            self.assertTrue(os.path.isfile(result.get_filepath()))

