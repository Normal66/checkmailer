# Copyrigth by Constantin Sidorov, 2020
# All rigth reserved

import argparse
from checkmail import BaseMail
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# Разбор аргументов командной строки
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--with-proxy', action='store_true', default=False)
    parser.add_argument('--with-keywords', action='store_true', default=False)
    return parser
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# Вызов проверки почты
def checkmail(_user, _pass, _proxy, _keywords, _useproxy, _usekeyword):
    _Res = {}
    mail = BaseMail(_user, _pass, _proxy, _keywords, _useproxy, _usekeyword)
    mail.do_check_imap()
    _Res['GOOD'] = mail.get_good()
    _Res['BAD'] = mail.get_bad()
    _Res['WELL'] = mail.get_well()
    return _Res
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
    g_KeyWords = []     # Список ключевых слов
    g_Users = {}        # Логины/пароли
    g_Proxy = {}        # Прокси
    g_Good = 0
    g_Bad = 0
    g_Well = []
    # Разбираем аргументы из командной строки
    parser = createParser()
    namespace = parser.parse_args()
    # Заполняем исходные данные
    # Прокси
    if namespace.with_proxy:
        with open("proxy.cfg", 'r', encoding='utf-8') as fin:
            for i in fin.read().splitlines():
                _tmp_proxy = i.split(':')
                g_Proxy[_tmp_proxy[1]] = [_tmp_proxy[0], _tmp_proxy[2], _tmp_proxy[3], _tmp_proxy[4]]
            fin.close()
    # Ключевые слова
    if namespace.with_keywords:
        with open("keywords.cfg", 'r', encoding='utf-8') as fin:
            for n, line in enumerate(fin, 1):
                g_KeyWords.append(line.rstrip('\n'))
            fin.close()
    # Логины - пароли
    with open("users.cfg", 'r', encoding='utf-8') as fin:
        for i in fin.read().splitlines():
            username = i.split(':')[0]
            password = i.split(':')[1]
            g_Users[username] = password
        fin.close()
    # ------------------------------------------------------------------------------------------ #
    # Создание и обработка потоков
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _user, _pass in g_Users.items():
            futures.append(executor.submit(checkmail, _user=_user, _pass=_pass, _proxy=g_Proxy, _kyewords=g_KeyWords, _useproxy=namespace.with_proxy, _usekeywords=namespace.with_keywords))
        for future in concurrent.futures.as_completed(futures):
            _tmp_good, _tmp_bad, _tmp_well = future.result()
            g_Good += _tmp_good
            g_Bad += _tmp_bad
            g_Well.append(_tmp_well)
    # Запись в выходные файлы
    with open("good.txt", 'w', encoding='utf-8') as fout:
        fout.writelines(g_Good)
        fout.close()
    with open("bad.txt", 'w', encoding='utf-8') as fout:
        fout.writelines(g_Bad)
        fout.close()
    with open("weel.txt", 'w', encoding='utf-8') as fout:
        fout.writelines(g_Well)
        fout.close()
    exit()
