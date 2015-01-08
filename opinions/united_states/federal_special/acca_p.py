"""Scraper for Army Court of Criminal Appeals
CourtID: acca
Reviewer: None
History:
  2015-01-08: Created by mlr
"""

from datetime import datetime
import re

from juriscraper.OpinionSite import OpinionSite


class Site(OpinionSite):
    def __init__(self):
        super(Site, self).__init__()
        self.court_id = self.__module__
        self.url = 'https://www.jagcnet.army.mil/85257546006DF36B/ODD?OpenView&Count=-1'
        self.docket_case_name_splitter = re.compile('(.*\d{7,8})(.*)')

    def _download(self, **kwargs):
        # DoD uses an annoying certificate that isn't installed. Thus, we
        # disable certificate verification in requests.
        return super(Site, self)._download(request_dict={'verify': False})

    def _get_download_urls(self):
        path = '//table//table//tr[position() > 2]/td[5]//a[2]/@href'
        return list(self.html.xpath(path))

    def _get_case_names(self):
        path = '//table//table//tr[position() > 2]/td[5]//a[2]/text()'
        case_names = []
        for t in self.html.xpath(path):
            m = self.docket_case_name_splitter.search(t)
            case_names.append(m.group(2))
        return case_names

    def _get_case_dates(self):
        path = '//table//table//tr[position() > 2]/td[4]//text()'
        return [datetime.strptime(date_string, '%m/%d/%Y').date()
                for date_string in self.html.xpath(path)]

    def _get_precedential_statuses(self):
        return ['Published'] * len(self.case_names)

    def _get_docket_numbers(self):
        path = '//table//table//tr[position() > 2]/td[5]//a[2]/text()'
        docket_numbers = []
        for t in self.html.xpath(path):
            m = self.docket_case_name_splitter.search(t)
            docket_numbers.append(m.group(1))
        return docket_numbers