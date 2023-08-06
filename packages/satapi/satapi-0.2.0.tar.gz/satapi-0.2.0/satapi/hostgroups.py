# -*- coding: utf-8 -
#
# This file is part of SatAPI released under the GPLv3 license.

from restkit import Resource, BasicAuth

import logging
log = logging.getLogger(__name__)

class hostgroups(Resource):
    def __init__(self, conn):
        resource_url = 'hostgroups'
        search_url = conn.satellite_url + '/' + conn.api_version + '/' + resource_url
        auth = BasicAuth(conn.auth_username, conn.auth_password)
        super(hostgroups, self).__init__(search_url, filters=[auth])

    def search(self, query=''):
        if log.isEnabledFor(logging.DEBUG):
            log.debug("Sending query: %s" % query)

        return self.get('', search=query)
