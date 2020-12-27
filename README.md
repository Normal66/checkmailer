# checkmailer
Зависимости:
pip install PySocks
ver 1.00
Аргументы командной строки
--with-proxy	# использовать прокси-сервер
--with-keywords	# использовать ключевые слова

Файлы входных данных:
------------------------------------------------------------------------------------------------
users.cfg - список почтовых логинов/паролей в формате:
login:password
где:
login - полное имя почтового адреса (unknown@undefined.xx )
password - пароль
-------------------------------------------------------------------------------------------------
keywords.cfg - список ключевых слов для проверки в формате:
key1
key2
key3
...
keyN
-------------------------------------------------------------------------------------------------
proxy.cfg - список прокси-серверов в формате:
U:proxy_address:proxy_port:login:password
где:
U - цифра, признак использования логина и пароля для подключения к данному прокси-серверу.
	0 - Не использовать логин/пароль, 1 - Использовать логин/пароль
1:10.10.10.1:3128:user1:pass1
0:10.10.10.2:8080:none:none
-------------------------------------------------------------------------------------------------
Файлы выходнх данных:
good.txt
bad.txt
wells.txt
