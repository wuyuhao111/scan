from information_acquisition import file_scan
from information_acquisition import nmap_scan
from information_acquisition import cms_Discriminate
from interface import print_f
from attack import Weak_password, awvs_scan
from information_acquisition import Cnd_scan
from information_acquisition import Whois_information
from information_acquisition import zym_scan
from attack import sqlmap_scan
from Intranet import up
from waf import see_see_waf
from interface import help
import sys

if __name__ == '__main__':
    print_f.put()
    help.help_use()

    # 单ip扫描
    use = sys.argv[1]
    url = sys.argv[2]
    if use == r"-w":
        Whois_information.cms_cms(url)

    if use == r"-z":
        zym_scan.thread(url)

    if use == r"-wf":
        see_see_waf.see_see_your_waf(url)

    if use == r"-c":
        Cnd_scan.cdn(url)

    if use == r"-a":
        for api in open('../dictionary/key.txt', 'r', encoding="utf-8"):
            api = api.replace("\n", "")
            awvs_scan.awvs_awvs(url, api)

    if use == r"-s":
        sqlmap_scan.sqlmap(url)

    if use == r"-up":
        Weak_password.thread_username_password(url)

    if use == r"-cms":
        cms_Discriminate.cms(url)

    if use == r"-f":
        file_scan.thread(url)

    if use == r"-nm":
        nmap_scan.thread(url)

    if use == r"-zym":
        zym_scan.thread(url)

    if use == r"-in":
        up.thread(url)
