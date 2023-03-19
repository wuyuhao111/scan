from information_acquisition import file_scan
from information_acquisition import nmap_scan
from information_acquisition import cms_Discriminate
from agree import rdp_agree
from attack import Weak_password, awvs_scan
from information_acquisition import Cdn_scan
from information_acquisition import Whois_information
from information_acquisition import zym_scan
from attack import sqlmap_scan
from Intranet import up
from waf import see_see_waf
from interface import help
import me_main_r
import sys

if __name__ == '__main__':
    # print_f.put()

    # 单ip扫描
    print("\n请选择多ip扫描还是指定ip扫描：-r为多ip， -p为指定IP")
    print("例子：python me_main.py -p -w 127.0.0.1 或 python me_main.py -r -rw \n")
    how = sys.argv[1]
    # print(how)
    if how == r"-h":
        help.help_use()
    if how == r"-p":
        use = sys.argv[2]
        url = sys.argv[3]
        if use == r"-w":
            Whois_information.cms_cms(url)

        if use == r"-z":
            zym_scan.thread(url)

        if use == r"-wf":
            see_see_waf.see_see_your_waf(url)

        if use == r"-c":
            Cdn_scan.cdn(url)

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

        if use == r"-dp":
            rdp_agree.thread_username_password(url)
    if how == r"-r":
        me_main_r.r()
