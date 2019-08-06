# HabrProxy

[![CodeFactor](https://www.codefactor.io/repository/github/k-vinogradov/habrproxy/badge)](https://www.codefactor.io/repository/github/k-vinogradov/habrproxy)
[![Build Status](https://travis-ci.org/k-vinogradov/habrproxy.svg?branch=master)](https://travis-ci.org/k-vinogradov/habrproxy)
[![Maintainability](https://api.codeclimate.com/v1/badges/fb715151eb92fb5c1314/maintainability)](https://codeclimate.com/github/k-vinogradov/habrproxy/maintainability)

This repo contains the solution of the Python challenge by [Ivelum](https://ivelum.com). The original problem description can be found [here](https://github.com/ivelum/job/blob/master/code_challenges/python.md).

**The only purpose of the project is improving of my Python developer skills**

- [HabrProxy](#habrproxy)
  - [Install](#install)
  - [Using](#using)
  - [Original Problem](#original-problem)

## Install

    pip install https://github.com/k-vinogradov/habrproxy/releases/download/0.1.0/habrproxy-0.1.0.tar.gz

## Using

To run habrproxy with default parameters (local port is 8080, remote address is [https://habr.com](https://habr.com), log output level is INFO) just run `habrproxy` and open [http://localhost:8080](http://localhost:8080) with your browser.

Advanced usage:

    ➜ habrproxy --help
    usage: habrproxy [-h] [-r REMOTE_ADDRESS] [-p PORT] [-v]

    Habrproxy

    optional arguments:
    -h, --help            show this help message and exit
    -r REMOTE_ADDRESS, --remote-address REMOTE_ADDRESS
                            Remote address (e.g. http://k-vinogradov.ru)
    -p PORT, --port PORT  Local proxy port number
    -v, --verbose         Enable debug output

## Original Problem

> Реализовать простой http-прокси-сервер, запускаемый локально (порт на ваше
> усмотрение), который показывает содержимое страниц Хабра. Прокси должен
> модицифировать текст на страницах следующим образом: после каждого слова из
> шести букв должен стоять значок «™». Пример:
>
> Исходный текст: [https://habr.com/ru/company/yandex/blog/258673/](https://habr.com/ru/company/yandex/blog/258673/)
>
>     Сейчас на фоне уязвимости Logjam все в индустрии в очередной раз обсуждают
>     проблемы и особенности TLS. Я хочу воспользоваться этой возможностью, чтобы
>     поговорить об одной из них, а именно — о настройке ciphersiutes.
>
> Через ваш прокси™: [http://127.0.0.1:8232/ru/company/yandex/blog/258673/](http://127.0.0.1:8232/ru/company/yandex/blog/258673/)
>
>     Сейчас™ на фоне уязвимости Logjam™ все в индустрии в очередной раз обсуждают
>     проблемы и особенности TLS. Я хочу воспользоваться этой возможностью, чтобы
>     поговорить об одной из них, а именно™ — о настройке ciphersiutes.
>
> Условия:
>
> - Python™ 3.5+
> - страницы должны™ отображаться и работать полностью корректно, в точности так,
>   как и оригинальные (за исключением модифицированного текста™);
> - при навигации по ссылкам, которые ведут на другие™ страницы хабра, браузер
>   должен™ оставаться на адресе™ вашего™ прокси™;
> - можно использовать любые общедоступные библиотеки, которые сочтёте нужным™;
> - чем меньше™ кода, тем лучше. PEP8 — обязательно;
> - если в условиях вам не хватает каких-то данных™, опирайтесь на здравый смысл.
>
> Если задачу™ удалось сделать быстро™, и у вас еще остался энтузиазм - как
> насчет™ написания тестов™?
