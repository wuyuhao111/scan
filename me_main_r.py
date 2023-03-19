from information_acquisition import nmap_scan
from information_acquisition import cms_Discriminate
from agree import rdp_agree
from attack import Weak_password
from information_acquisition import Cdn_scan
from information_acquisition import Whois_information
from information_acquisition import zym_scan
from Intranet import up
import sys


def r():
    use = sys.argv[2]
    print(use)
    if use == r"-rw":
        Whois_information.thread()

    if use == r"-rz":
        zym_scan.thread_r()

    if use == r"-rc":
        Cdn_scan.cdn_r()

    if use == r"-rup":
        Weak_password.thread_ip_username_password()

    if use == r"-rcms":
        cms_Discriminate.thread_cms()

    if use == r"-rnm":
        nmap_scan.thread_r()

    if use == r"-rzym":
        zym_scan.thread_r()

    if use == r"-rin":
        up.thread_r()

    if use == r"-rdp":
        rdp_agree.thread_ip_username_password()
