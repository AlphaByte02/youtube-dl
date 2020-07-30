from __future__ import unicode_literals

import re
import os

from .common import InfoExtractor
from ..utils import (
    url_or_none,
    get_element_by_id
)


class StreamTapeIE(InfoExtractor):
    _VALID_URL =  r'https?://(?:www\.)?streamtape\.com/v/(?P<id>\w+)(?:/(?P<title>\w+)(?:\.(?P<ext>\w+))?)?'
    _TESTS = [{
        'url': 'https://streamtape.com/v/Zzvj220zj8cqzxD',
        'info_dict': {
            'id': 'Zzvj220zj8cqzxD',
            'ext': 'mp4',
            'title': 'TheGodOfHighSchool_Ep_01_SUB_ITA',
            'thumbnail': r're:^https?://.*\.jpg$',
            'description': 'TheGodOfHighSchool_Ep_01_SUB_ITA.mp4 at Streamtape.com',
        }
    }, {
        'url': 'https://streamtape.com/v/Zzvj220zj8cqzxD/TheGodOfHighSchool_Ep_01_SUB_ITA.mp4',
        'info_dict': {
            'id': 'Zzvj220zj8cqzxD',
            'ext': 'mp4',
            'title': 'TheGodOfHighSchool_Ep_01_SUB_ITA',
            'thumbnail': r're:^https?://.*\.jpg$',
            'description': 'TheGodOfHighSchool_Ep_01_SUB_ITA.mp4 at Streamtape.com',
        }
    }]

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id, title, ext = mobj.group('id', 'title', 'ext')

        webpage = self._download_webpage(url, video_id)

        video_url = url_or_none(get_element_by_id('videolink', webpage))

        if not title:
            title, ext = os.path.splitext(self._og_search_title(webpage, default=''))

        if not title:
            title, ext = os.path.splitext(self._html_search_regex(r'<div class="col-12 text-center video-title">\s*<h2>(.+)</h2>\s*</div>', webpage, 'title', default=''))

        thumbnail = self._og_search_thumbnail(webpage, default=None)

        if ext:
            ext = ext.lower().strip(' .')

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'description': self._og_search_description(webpage),
            'thumbnail': thumbnail,
            'ext': ext,
        }
