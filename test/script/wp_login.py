#! /usr/bin/env python

import json
import re
import requests
import sys


class WPInteraction(object):
    def __init__(self, ip, domain="example.com",
                 login_id="wp_user", password=""):
        self.ip = ip
        self.domain = domain
        self.login_id = login_id
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({"Host": self.domain})

    def get_login_page(self):
        url = "http://{}".format(self.ip)
        r = self.session.get(url)
        return r.text

    def wp_post_login(self):
        url = "http://{}/wp-login.php".format(self.ip)
        print "url is {}".format(url)
        data = {"log": self.login_id,
                "pwd": self.password}
        print json.dumps(data, indent=4)
        r = self.session.post(url, data=data, allow_redirects=False)
        if r.is_redirect:
            redirected_url = r.headers.get('location')
            r = self.session.get(re.sub(self.domain, self.ip, redirected_url))
        print "status code is {}".format(r.status_code)
        return r.text

    def login_successful(self):
        content = self.wp_post_login()
        return "Dashboard" in content


if __name__ == "__main__":
    print json.dumps(sys.argv)
    ip = sys.argv[1]
    domain = sys.argv[2]
    login_id = sys.argv[3]
    password = sys.argv[4]
    wp = WPInteraction(ip, domain=domain, login_id=login_id, password=password)

    if wp.login_successful():
        print "Wordpress login successful."
        sys.exit(0)
    else:
        print "login failed :("
        sys.exit(1)
