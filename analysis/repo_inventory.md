
====================================================================================================
REPO: ctfcup2023-quals
--- ROOT README.md (2987 chars) ---
# Отборочный этап VII Кубка CTF России
Исходные коды, разборы, сплоиты и файлы для деплоя заданий с отборочного тура VII Кубка CTF России, который проходил 28-29 октября 2023 года онлайн. Задания разрабатывала команда [C4T BuT S4D](https://github.com/C4T-BuT-S4D).

[Сайт соревнования](https://ctfcup.ru/)

- Организаторы: **АРСИБ** и **ВОД «Наставники России»**
- Генеральный партнер: **RDP**
- Официальные партнеры: **Сбер** и **Газпромбанк**
- Специальный партнер: **Positive Technologies**
- Технологические партнеры: **EdgeCenter**, **UserGate** и **C4T BuT S4D**

# Результаты

![Top](scoreboard/top.png)

[Весь скорборд](scoreboard/full.png)

# Информация
- Руководитель проекта: [@deviantwish](https://github.com/deviantwish)
- Технический директор: [@bysmaks](https://github.com/bysmaks)
- Тимлид: [@jnovikov](https://github.com/jnovikov)
- DevOps: [@pomo-mondreganto](https://github.com/pomo-mondreganto)

# Задания
| Название | Категория | Автор|
|------|-----------|-------|
| [gamer2](tasks/forensic/gamer) | forensics | [@qumusabel](https://github.com/qumusabel) |
| [zion](tasks/forensic/zion) | forensics | [@asokol123](https://github.com/asokol123) |
| [zion-revenge](tasks/forensic/zion-revenge) | forensics | [@asokol123](https://github.com/asokol123) |
| [monitoring](tasks/reverse/monitoring) | reverse | [@renbou](https://github.com/renbou) |
| [magick_lock](tasks/reverse/magick_lock) | reverse | [@falamous](https://github.com/falamous) |
| [time_capsule](tasks/reverse/time_capsule) | reverse | [@falamous](https://github.com/falamous) |
| [2fac](tasks/reverse/2fac) | reverse | [@qumusabel](https://github.com/qumusabel) |
| [novosti](tasks/web/novosti) | web | [@renbou](https://github.com/renbou) |
| [waf](tasks/web/waf) | web | [@jnovikov](https://github.com/jnovikov) |
| [scanner](tasks/web/scanner) | web | [@jnovikov](https://github.com/jnovikov) |
| [mistakes](tasks/web/mistakes) | web | [@Slonser](https://github.com/Slonser) |
| [murdata](tasks/crypto/murdata) | crypto | [@jnovikov](https://github.com/jnovikov) |
| [geometry](tasks/crypto/geometry) | crypto | [@falamous](https://github.com/falamous) |
| [lateralus](tasks/crypto/lateralus) | crypto | [@falamous](https://github.com/falamous) |
| [more_heap](tasks/pwn/more_heap) | pwn | [@user39043346](https://github.com/user39043346) |
| [some_storage](tasks/pwn/some_storage) | pwn | [@user39043346](https://github.com/user39043346) |
| [spy](tasks/pwn/spy) | pwn | [@b1r1b1r1](https://github.com/b1r1b1r1) |
| [gamer1](tasks/msc/gamer) | misc | [@qumusabel](https://github.com/qumusabel) |
| [Floating in Delirium](tasks/ppc/floating_in_delirium) | misc | [@falamous](https://github.com/falamous) |
| [checkpoint](tasks/ppc/checkpoint) | ppc | [@renbou](https://github.com/renbou) |
| [slons](tasks/ppc/slons) | ppc | [@Slonser](https://github.com/Slonser)|

# Таски от партнера - Positive Technologies

[Mystery_ldap](tasks/pt/Mystery_ldap/)
[NFS](tasks/pt/NFS/)
[stealer](tasks/pt/stealer/)
DIR: .git | files=6
DIR: .git\hooks | files=14
DIR: .git\info | files=1
DIR: .git\logs | files=1
DIR: .git\logs\refs | files=0
DIR: .git\objects | files=0
DIR: .git\objects\info | files=0
DIR: .git\objects\pack | files=3
DIR: .git\refs | files=0
DIR: .git\refs\heads | files=1
DIR: .git\refs\remotes | files=0
DIR: .git\refs\tags | files=0
DIR: scoreboard | files=2
DIR: tasks | files=0
DIR: tasks\crypto | files=1
DIR: tasks\crypto\geometry | files=2
DIR: tasks\crypto\lateralus | files=1
DIR: tasks\crypto\murdata | files=2
DIR: tasks\forensic | files=1
DIR: tasks\forensic\gamer | files=1
DIR: tasks\forensic\zion | files=2
DIR: tasks\forensic\zion-revenge | files=4
DIR: tasks\misc | files=1
DIR: tasks\misc\gamer | files=1
DIR: tasks\ppc | files=1
DIR: tasks\ppc\checkpoint | files=2
DIR: tasks\ppc\floating_in_delirium | files=1
DIR: tasks\ppc\slons | files=1
DIR: tasks\pt | files=1
DIR: tasks\pt\Mystery_ldap | files=1
DIR: tasks\pt\NFS | files=2
DIR: tasks\pt\stealer | files=1
DIR: tasks\pwn | files=1
DIR: tasks\pwn\more_heap | files=2
DIR: tasks\pwn\some_storage | files=2
DIR: tasks\pwn\spy | files=2
DIR: tasks\reverse | files=1
DIR: tasks\reverse\2fac | files=1
DIR: tasks\reverse\magick_lock | files=1
DIR: tasks\reverse\monitoring | files=2
DIR: tasks\reverse\time_capsule | files=2
DIR: tasks\web | files=1
DIR: tasks\web\mistakes | files=2
DIR: tasks\web\novosti | files=2
DIR: tasks\web\scanner | files=2
DIR: tasks\web\waf | files=3

====================================================================================================
REPO: ctfcup2025-ad
--- ROOT README.md (638 chars) ---
# Общее
- Соревнование проходило с 06.12.25, с 10:00 по 19:00 по времени мск;  
- Игровые сервисы выкатывались каждый на отдельную виртуальную машину 4CPU,4RAM, сервисы запускались в k3s.

### Сервисы
`veladora`, go, [revervand](https://github.com/revervand), http-only  
`archive`, cpp, [revervand](https://github.com/revervand), tls1.3  
`warehouse`, go, [kot](https://github.com/kot), tls1.3  
`prototyper`, python, [rx00](https://github.com/rx00), tls1.3  

Чексистем и инфра-мастер – [dlukshto](https://github.com/capitanbanana).


# Скорборд

![scoreboard](https://github.com/HazyCorp/ctfcup-2025-public/blob/master/scoreboard.png)

DIR: .git | files=6
DIR: .git\hooks | files=14
DIR: .git\info | files=1
DIR: .git\logs | files=1
DIR: .git\logs\refs | files=0
DIR: .git\objects | files=0
DIR: .git\objects\info | files=0
DIR: .git\objects\pack | files=3
DIR: .git\refs | files=0
DIR: .git\refs\heads | files=1
DIR: .git\refs\remotes | files=0
DIR: .git\refs\tags | files=0
DIR: checkers | files=0
DIR: checkers\archive | files=6
DIR: checkers\prototype | files=10
DIR: checkers\prototype\__pycache__ | files=12
DIR: checkers\veladora | files=4
DIR: checkers\warehouse | files=5
DIR: services | files=0
DIR: services\archive | files=1
DIR: services\archive\deploy | files=0
DIR: services\archive\src | files=0
DIR: services\archive\utils | files=1
DIR: services\prototype | files=4
DIR: services\prototype\deploy | files=0
DIR: services\prototype\src | files=2
DIR: services\prototype\utils | files=0
DIR: services\veladora | files=4
DIR: services\veladora\deploy | files=0
DIR: services\veladora\src | files=3
DIR: services\veladora\utils | files=0
DIR: services\warehouse | files=3
DIR: services\warehouse\deploy | files=0
DIR: services\warehouse\src | files=0
DIR: services\warehouse\utils | files=0
DIR: sploits | files=1
DIR: sploits\archive | files=2
DIR: sploits\prototype | files=3
DIR: sploits\prototype\__pycache__ | files=1
DIR: sploits\veladora | files=3
DIR: sploits\warehouse | files=2
DIR: writeups | files=1
DIR: writeups\archive | files=1
DIR: writeups\prototype | files=1
DIR: writeups\veladora | files=1
DIR: writeups\warehouse | files=1

====================================================================================================
REPO: ctfcup2025-quals
--- ROOT README.md (4532 chars) ---
# Отборочный этап IX Кубка CTF России

Исходные коды, разборы, эксплоиты и файлы для деплоя заданий с отборочного тура IX Кубка CTF России, который проходил 2-3 ноября 2025 года в онлайн-формате.

[Сайт соревнований](https://ctfcup.ru/)

Официальный партнер - Газпромбанк, Сбер

Технологические партнеры - Yandex Cloud, cloud.ru, НТЦ Вулкац, Edge, Цинтера, КЦ доменов ru/рф

Партнеры - Газинформ, Третье тысячелетие

Партнеры призового фонда - ГК Гарда, Сёрчинформ

Информационный партнер - Информагентство ТАСС, журнал Хакер

При поддержке "Движение первых"


 Таск                                                                                      | Категория | Баллы | Кол-во решений | Автор |
| ---------------------------------------------------------------------------------------- | --------- | ----- | -------------- | ----- |
| [miracle](tasks/crypto/miracle/Readme.md)                                                | crypto    | 100   | 80             | @al5c2rd   |
| [cursed](tasks/crypto/cursed/Readme.md)                                                  | crypto    | 395   | 42             | @al5c2rd   |
| [annabelle](tasks/reverse/annabelle/Readme.md)                                           | reverse   | 793   | 25             | @al5c2rd   |
| [nanomachines](tasks/reverse/nanomachines/Readme.md)                                     | reverse   | 1000  | 1              | @al5c2rd   |
| [Wincrack](tasks/reverse/Wincrack/README.md)                                             | reverse   | 919   | 16             | @revker    |
| [bad parser](tasks/pwn/bad_parser/README.md)                                             | pwn       | 997   | 4              | @revker    |
| [play with ker](tasks/pwn/play_with_ker/README.md)                                       | pwn       | 995   | 5              | @revker    |
| [safelang](tasks/pwn/safelang/Readme.md)                                                 | pwn       | 100   | 156            | @al5c2rd   |
| [safelang-revenge](tasks/pwn/safelang-revenge/Readme.md)                                 | pwn       | 100   | 108            | @al5c2rd   |
| [safelang-revenge-revenge](tasks/pwn/safelang-revenge-revenge/Readme.md)                 | pwn       | 100   | 70             | @al5c2rd   |
| [goose](tasks/web/goose/Readme.md)                                                       | web       | 100   | 215            | @al5c2rd   |
| [goose-revenge](tasks/web/goose-revenge/Readme.md)                                       | web       | 100   | 96             | @al5c2rd   |
| [trustmebroker](tasks/web/trustmebroker/README.md)                                       | web       | 983   | 8              | @nime_boy  |
| [BimboIncident](tasks/forensic/BimboIncident/README.md)                                  | forensics | 1000  | 1              | @revker    |
| [brokilon](tasks/forensic/brokilon/README.md)                                            | forensics | 983   | 8              | @revker    |
| [Funeral](tasks/forensic/Funeral/README.md)                                              | forensics | 239   | 47             | @revker    |
| [babyrev](tasks/beginners/babyrev/README.md)                                             | beginners | 100   | 173            | @revker    |
| [babypwn](tasks/beginners/babypwn/README.md)                                             | beginners | 100   | 143            | @revker    |
| [babymisc](tasks/beginners/babymisc/README.md)                                           | beginners | 100   | 408            | @revker    |
| [babyfor](tasks/beginners/babyfor/README.md)                                             | beginners | 100   | 201            | @revker    |
| [babycrypto](tasks/beginners/babycrypto/README.md)                                       | beginners | 100   | 435            | @revker    |
| [babyppc](tasks/beginners/geo/README.md)                                                 | beginners | 100   | 344            | @al5c2rd   |
| [babyosint](tasks/beginners/babyosint/README.md)                                         | beginners | 100   | 402            | @by_sm     |
| [babyweb](tasks/beginners/babyweb/README.md)                                             | beginners | 100   | 106            | @by_sm     |


## Результаты

![Top-10](scoreboard/top.png)

[Полный список](scoreboard/full.png)

## Инфраструктура

Инфраструктура была предоставлена компаниями yandex.cloud / cloud.ru

- DevOps: [@devijoe](https://github.com/DeviJoe)
- Checksystem: [CTFd](https://ctfd.io)

DIR: .git | files=6
DIR: .git\hooks | files=14
DIR: .git\info | files=1
DIR: .git\logs | files=1
DIR: .git\logs\refs | files=0
DIR: .git\objects | files=0
DIR: .git\objects\info | files=0
DIR: .git\objects\pack | files=3
DIR: .git\refs | files=0
DIR: .git\refs\heads | files=1
DIR: .git\refs\remotes | files=0
DIR: .git\refs\tags | files=0
DIR: scoreboard | files=2
DIR: tasks | files=0
DIR: tasks\beginners | files=0
DIR: tasks\beginners\babycrypto | files=1
DIR: tasks\beginners\babyfor | files=1
DIR: tasks\beginners\babymisc | files=1
DIR: tasks\beginners\babyosint | files=1
DIR: tasks\beginners\babyppc | files=1
DIR: tasks\beginners\babypwn | files=1
DIR: tasks\beginners\babyrev | files=1
DIR: tasks\beginners\babyweb | files=1
DIR: tasks\crypto | files=2
DIR: tasks\crypto\cursed | files=2
DIR: tasks\crypto\miracle | files=1
DIR: tasks\forensic | files=1
DIR: tasks\forensic\BimboIncident | files=1
DIR: tasks\forensic\brokilon | files=1
DIR: tasks\forensic\Funeral | files=1
DIR: tasks\pwn | files=1
DIR: tasks\pwn\bad_parser | files=1
DIR: tasks\pwn\play_with_ker | files=1
DIR: tasks\pwn\safelang | files=2
DIR: tasks\pwn\safelang-revenge | files=2
DIR: tasks\pwn\safelang-revenge-revenge | files=2
DIR: tasks\reverse | files=0
DIR: tasks\reverse\annabelle | files=1
DIR: tasks\reverse\nanomachines | files=1
DIR: tasks\reverse\Wincrack | files=1
DIR: tasks\web | files=0
DIR: tasks\web\goose | files=2
DIR: tasks\web\goose-revenge | files=2
DIR: tasks\web\trustmebroker | files=1

====================================================================================================
REPO: ctfcup2025-superfinals
DIR: .git | files=5
DIR: .git\hooks | files=14
DIR: .git\info | files=1
DIR: .git\logs | files=1
DIR: .git\logs\refs | files=0
DIR: .git\objects | files=0
DIR: .git\objects\info | files=0
DIR: .git\objects\pack | files=3
DIR: .git\refs | files=0
DIR: .git\refs\heads | files=1
DIR: .git\refs\remotes | files=0
DIR: .git\refs\tags | files=0

====================================================================================================
REPO: ctfcup22-quals
--- ROOT README.md (4460 chars) ---
# Отборочный этап VI Кубка CTF России

Исходные коды, разборы, эксплоиты и файлы для деплоя заданий с отборочного тура VI Кубка CTF России, который проходил 19-20 ноября 2022 года в онлайн-формате.

[Сайт соревнований](https://ctfcup.ru/)

Генеральный партнер соревнований - **Газпромбанк**\
Официальный партнер - **СБЕР**\
Стратегический партнер - **RDP**\
Технологические партнеры - **EdgeCenter** и **UserGate**\
Партнеры - **PositiveTechnologies**, **НТЦ Вулкан**, **Координационный центр доменов .RU/.РФ**

 Таск                                                                                      | Категория | Баллы | Кол-во решений | Автор |
| ---------------------------------------------------------------------------------------- | --------- | ----- | -------------- | ----- |
| [Good pad / bad pad](tasks/crypto/good_pad_bad_pad/README.md)                            | crypto    | 1000  | 0              | @bork_dog      |
| [Important task](tasks/crypto/important_task/README.md)                                  | crypto    | 213   | 38             | @bork_dog      |
| [Dinosaurs](tasks/crypto/dinosaurs/README.md)                                            | crypto    | 1000  | 1              | @bork_dog      |
| [The time has come](tasks/crypto/the_time_has_come/README.md)                            | crypto    | 909   | 2              | @bork_dog      |
| [Stolen blueprints](tasks/crypto/stolen_blueprints/README.md)                            | crypto    | 333   | 21             | @bork_dog      |
| [onlytweets](tasks/web/onlytweets/README.md)                                             | web       | 833   | 3              | @jnovikov      |
| [warmup](tasks/web/warmup/README.md)                                                     | web       | 357   | 19             | @jnovikov      |
| [legacy](tasks/web/legacy/README.md)                                                     | web       | 455   | 13             | @jnovikov      |
| [simple](tasks/web/simple/README.md)                                                     | web       | 833   | 3              | @shipko        |
| [malware_autopsy](tasks/forensics/malware_autopsy/README.md)                              | forensic  | 213   | 38             | @swissarmy     |
| [fallen_angel](tasks/forensics/fallen_angel/README.md)                                    | forensic  | 78    | 120            | @swissarmy     |
| [french_connection](tasks/forensics/french_connection/README.md)                          | forensic  | 1000  | 1              | @slyshay6      |
| [Red firmware I](tasks/forensics/Red_firmware_I/README.md)                                | forensic  | 244   | 32             | @greg0r0       |
| [Simple Encoder](tasks/reverse/simple_encoder/README.md)                                 | reverse   | 526   | 10             | @greg0r0       |
| [unicorn_plc](tasks/reverse/unicorn_plc/README.md)                                       | reverse   | 769   | 4              | @greg0r0       |
| [crackme2077](tasks/reverse/crackme2077/README.md)                                       | reverse   | 1000  | 1              | @revker        |
| [bebrus](tasks/reverse/bebrus/README.md)                                                 | reverse   | 667   | 6              | @revker        |
| [watcher](tasks/pwn/watcher/README.md)                                                   | pwn       | 1000  | 1              | @revker        |
| [SHELLyha](tasks/pwn/shellyha/README.md)                                                 | pwn       | 833   | 3              | @revker        |
| [ozne](tasks/pwn/ozne/README.md)                                                         | pwn       | 909   | 2              | @revker        |
| [babystack](tasks/pwn/babystack/README.md)                                     | pwn       | 667   | 6              | @revker        |
| [classic_matreshka](tasks/warmup/classic_matreshka/README.md)                                    | warmup    | 50    | 193            | @RegularITCat  |
| [gpb_math_pong](tasks/warmup/math_pong/README.md)                                        | warmup    | 92    | 100            | @RegularITCat  |
## Результаты

![Top-10](scoreboard/top.png)

[Полный список](scoreboard/full.png)

## Инфраструктура

Инфраструктура была предоставлена компанией [EdgeCenter](https://edgecenter.ru)

- DevOps: [@Rubikoid](https://github.com/@Rubikoid)
- Checksystem: [yatb](https://github.com/kksctf/yatb)
DIR: .git | files=6
DIR: .git\hooks | files=14
DIR: .git\info | files=1
DIR: .git\logs | files=1
DIR: .git\logs\refs | files=0
DIR: .git\objects | files=0
DIR: .git\objects\info | files=0
DIR: .git\objects\pack | files=3
DIR: .git\refs | files=0
DIR: .git\refs\heads | files=1
DIR: .git\refs\remotes | files=0
DIR: .git\refs\tags | files=0
DIR: scoreboard | files=2
DIR: tasks | files=0
DIR: tasks\crypto | files=0
DIR: tasks\crypto\dinosaurs | files=3
DIR: tasks\crypto\good_pad_bad_pad | files=3
DIR: tasks\crypto\important_task | files=3
DIR: tasks\crypto\stolen_blueprints | files=3
DIR: tasks\crypto\the_time_has_come | files=3
DIR: tasks\forensics | files=0
DIR: tasks\forensics\fallen_angel | files=3
DIR: tasks\forensics\french_connection | files=3
DIR: tasks\forensics\malware_autopsy | files=3
DIR: tasks\forensics\Red_firmware_I | files=3
DIR: tasks\pwn | files=0
DIR: tasks\pwn\babystack | files=3
DIR: tasks\pwn\ozne | files=3
DIR: tasks\pwn\shellyha | files=3
DIR: tasks\pwn\watcher | files=3
DIR: tasks\reverse | files=0
DIR: tasks\reverse\bebrus | files=3
DIR: tasks\reverse\crackme2077 | files=3
DIR: tasks\reverse\simple_encoder | files=3
DIR: tasks\reverse\unicorn_plc | files=3
DIR: tasks\warmup | files=0
DIR: tasks\warmup\classic_matreshka | files=3
DIR: tasks\warmup\math_pong | files=3
DIR: tasks\web | files=0
DIR: tasks\web\legacy | files=3
DIR: tasks\web\onlytweets | files=3
DIR: tasks\web\simple | files=3
DIR: tasks\web\warmup | files=3