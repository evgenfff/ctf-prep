

#### [model-switched] msg_16db5e0190016etRXqdO4BKW6V
switch: default -> max


#### [user] msg_16db5e006001xOcPhGtzA4jqxl
хочу поучаствовать в турнире по кибербезопасности https://ctfcup.ru/, мне очень важно пройти отборочный тур, который будет через неделю, а в идеале, очень-очень хотелось бы выиграть финальный тур в москве, чтобы получить призовой фонд. нужно максимально подготовиться, вот прям максимально насколько это возможно. у меня есть задания с прошлых годов https://github.com/acisoru, можешь тщательно и детально изучить полностью сайт этого турнира и все содержимое гитхаб репозитория с заданиями, чтобы дать точный план, документацию, примеры и основные моменты, на которых надо поймать фулл фокус? это очень важно для меня

**A** (msg_16db5e0330): Начну с полного изучения сайта турнира и GitHub-организации с заданиями. Затем соберу всё в структурированный план подготовки.

**A** (msg_16db5f4c60): Сайт — интерактивный (JS), нашёл основную структуру. Теперь достану расписание/правила и список репозиториев.

**A** (msg_16db6135b0): Отлично: в организации 50+ репозиториев, из них ~12 — именно Кубок CTF. Сейчас вытащу расписание/регламент из JS-бандла сайта и дерево файлов ключевых репозиториев.

**A** (msg_16db662700): Ключевые даты уже подтверждены: **отбор 31 октября 23:00 — 1 ноября 12:00 (13 часов), финал 5–7 декабря в Москве**. Теперь достану регламент и полный список задач прошлых лет.

**A** (msg_16db6c2650): Регламент найден. Сейчас скачаю PDF, установлю инструмент извлечения текста и склонирую ключевые репозитории для детального разбора.

**A** (msg_16db8e2780): Регламент даёт критически важные факты: команда **5–7 человек**, отбор **24 часа**, в очный этап проходят **топ-10 в каждом зачёте**, финал — Attack-Defense, а призовой фонд — **1 млн ₽, по 250 тыс. на зачёт**. Регистрация закрывается **завтра в 12:00 МСК**. Теперь разбираю задачи прошлых лет.

**A** (msg_16dba41670): Картина проясняется: отбор — 24-часовой jeopardy, очный полуфинал — Attack-Defense, а секретный финал в 2025 был похож на multi-machine pentest. Сейчас изучу задачи 2022–2023 и материалы финалов, чтобы выделить повторяющиеся приёмы.

**A** (msg_16dbb62280): Нашёл важное: финал 2025 — это цепочка из 3 машин (web/bot, Windows-драйвер, Asterisk/Linux) плюс 4-я машина. То есть для победы нужен не только Attack-Defense, но и полноценный pentest. Соберу материалы по всем годам и финалам.


#### [compaction] msg_16dbc4dc3001nHqrV41teBaK8M
## Objective
- Пользователь хочет максимально подготовиться к X Кубку CTF России: пройти отборочный тур через неделю и выиграть финал в Москве с призовым фондом.
- Нужно детально изучить ctfcup.ru и GitHub-репозитории acisoru с заданиями прошлых лет, затем выдать точный план, документацию, примеры и ключевые акценты подготовки.

## Requirements
- Изучить полностью сайт турнира и всё содержимое GitHub-репозитория с заданиями.
- Подготовка должна быть максимально полной, с планом, документацией, примерами и фокусными темами.
- Приоритет: пройти отбор; идеально — выиграть финал и получить призовой фонд.
- Ответ и документация должны быть на русском.

## Decisions
- Основной фокус анализа: репозитории именно Кубка CTF России (`ctfcup2025-quals`, `ctfcup2025-ad`, `ctfcup2025-superfinals`, `ctfcup2025-school-final`, `ctfcup2023-quals`, `ctfcup22-quals`, `ctfcup-21-quals`, `ctfcup-2020-quals` и др.).
- Смежные репозитории (MIA CTF, VrnCTF, NSK CTF, GoCTF, LetoCTF, OmCTF, CenterCTF) рассматриваются как дополнительная тренировочная база, но не как основной источник.
- Создаётся локальная папка `ctf-prep` с анализами и будущими документами; репозитории клонируются в `ctf-prep/repos`.
- Ближайшая цель — успеть с регистрацией и сформировать команду, затем 7-дневный спринт к отбору; после отбора — отдельный 4-недельный план к финалу.

## Work State
### Completed
- Изучен сайт `https://ctfcup.ru/`: JS-бандл, robots.txt, sitemap, архив 2025.
- Найден и скачан официальный PDF положения 2026: `C:\Users\Eugene\AppData\Local\Temp\polozhenie2026.pdf`; текст извлечён в `C:\Users\Eugene\AppData\Local\Temp\polozhenie2026_fitz.txt`.
- Установлены `pypdf` и `PyMuPDF` для извлечения PDF.
- Получен и проанализирован список репозиториев организации acisoru (50+).
- Склонированы репозитории:
  - `ctf-prep/repos/ctfcup2025-quals`
  - `ctf-prep/repos/ctfcup2025-ad`
  - `ctf-prep/repos/ctfcup2025-superfinals` (рабочее дерево неполное из-за Windows-путей с `C:\...`; файлы доступны через GitHub raw/API)
  - `ctf-prep/repos/ctfcup2023-quals`
  - `ctf-prep/repos/ctfcup22-quals`
- Созданы аналитические файлы:
  - `ctf-prep/analysis/repo_inventory.md`
  - `ctf-prep/analysis/2025_tasks.md`
  - `ctf-prep/analysis/2025_summary.md`
  - `ctf-prep/analysis/2022_2023_summary.md`
- Разобраны задачи 2025 отбора (24 задания), 2023 (21 + 3 PT), 2022 (23), 2021 (30), 2020 (25).
- Разобраны форматы и материалы финалов: `ctfcup2025-ad` (4 сервиса AD) и `ctfcup2025-superfinals` (3 машины + 4-я).
- Прочитаны writeup'ы AD-сервисов: Veladora (IDOR/predictable payment ID/conversation injection), Archive (CVE-2023-34399 boost serialization), Warehouse (UUIDv1 API key + SSRF), Prototype (MinIO CVE-2025-62506 + HMAC salt overflow).
- Прочитаны материалы суперфинала: machine-1 (Telegram bot webhook -> local Bot API file read -> SSH -> vim cap_setuid), machine-2 (Windows TOCTOU/UAF/predictable encryption -> driver OOB -> crash dump -> NT hash), machine-3 (web LFI -> Asterisk SIP -> binary overflow -> SUID -> pickle), machine-4 (crypto/PPC/OSINT -> Turing machine -> SUID).
- Найдены ключевые даты, ссылки регистрации и призовой фонд.

### Active
- Формирование итогового пакета документации в `ctf-prep`: README, регламент, анализ задач, 7-дневный план, playbook отбора, AD- и pentest-подготовка, шпаргалки, setup toolkit.
- Нужно дополнить анализ деталями по ключевым задачам 2025: `safelang`, `goose`, `trustmebroker`, `Funeral`, `brokilon`, `Wincrack`, `bad_parser`, `play_with_ker`, `miracle`.
- Нужно собрать единую таблицу задач по годам/категориям/сложности и приоритетов решения.

### Blocked
- Нет блокеров по анализу; для части superfinals нельзя сделать обычный git checkout на Windows из-за путей вида `machines/machine-2/root/C:\Windows\Drivers/...`, использовать raw GitHub/API.

## Next Move
1. Создать `ctf-prep/README.md` с немедленными действиями: регистрация до 12:00 25.10.2026, требования к составу команды, ссылки Timepad.
2. Создать `01_regulations_2026.md` с выжимкой из PDF: даты, форматы, состав команды, квоты, призовой фонд, ссылки.
3. Создать `02_past_tasks_analysis.md` — сводная матрица задач 2020–2025, повторяющиеся техники и приоритеты.
4. Создать `03_qualifier_playbook.md` — стратегия 24 часов, роли, триаж, таймлайн, динамическая система очков, чек-лист флагов.
5. Создать `04_seven_day_plan.md` — почасовой план с 24.10 по 31.10, конкретные задачи для тренировки.
6. Создать `05_final_attack_defense.md` и `06_final_secret_pentest.md` — AD-playbook и multi-machine pentest по материалам 2025.
7. Создать `07_cheatsheets/` и `08_toolkit_setup.md` — команды, payload'ы, шаблоны, установка WSL/Kali/Docker/инструментов.
8. В чате выдать краткое резюме с самым срочным действием (регистрация/команда) и ссылками на созданные файлы.

## Relevant Files
- `C:\Users\Eugene\AppData\Local\Temp\polozhenie2026_fitz.txt`: полный текст официального положения 2026, ключевой источник фактов.
- `C:\Users\Eugene\Documents\Проект по умолчанию\ctf-prep\analysis\2025_summary.md`: краткий разбор всех задач отбора 2025.
- `C:\Users\Eugene\Documents\Проект по умолчанию\ctf-prep\analysis\2022_2023_summary.md`: разбор задач 2022–2023.
- `C:\Users\Eugene\Documents\Проект по умолчанию\ctf-prep\analysis\2025_tasks.md`: подробные README и solve-файлы задач 2025.
- `C:\Users\Eugene\Documents\Проект по умолчанию\ctf-prep\analysis\repo_inventory.md`: инвентарь склонированных репозиториев.
- `C:\Users\Eugene\Documents\Проект по умолчанию\ctf-prep\repos\ctfcup2025-quals`: основной набор задач отбора 2025.
- `C:\Users\Eugene\Documents\Проект по умолчанию\ctf-prep\repos\ctfcup2025-ad`: сервисы, чекеры, сплойты и writeup'ы AD-финала.
- `C:\Users\Eugene\Documents\Проект по умолчанию\ctf-prep\repos\ctfcup2025-superfinals`: материалы секретного финала (читать через raw GitHub из-за Windows-путей).
- `C:\Users\Eugene\Documents\Проект по умолчанию\ctf-prep\repos\ctfcup2023-quals`: задачи 2023, полезны для web/pwn/crypto.
- `C:\Users\Eugene\Documents\Проект по умолчанию\ctf-prep\repos\ctfcup22-quals`: задачи 2022, полезны для crypto/forensics/pwn.
- `C:\Users\Eugene\AppData\Local\Temp\ctfcup_strings.txt`: извлечённые строки JS-бандла сайта.
- `C:\Users\Eugene\AppData\Local\Temp\ctfcup.js`: JS-бандл сайта с ссылками на Timepad и архив.
- `C:\Users\Eugene\AppData\Local\Temp\opencode\extract_js.py`: скрипт извлечения строк сайта.
- `C:\Users\Eugene\AppData\Local\Temp\opencode\summary2025.py`: скрипт генерации `2025_summary.md`.
- `C:\Users\Eugene\AppData\Local\Temp\opencode\summary_old.py`: скрипт генерации `2022_2023_summary.md`.

## Important Context
- Официальные даты 2026:
  - Отбор: **31.10.2026 12:00 — 01.11.2026 12:00 МСК**, 24 часа, jeopardy/task-based.
  - Финал: **04–06.12.2026**, Москва.
  - Школьный/СПО AD: 04.12.2026, 10:00–19:00.
  - Академический/смешанный AD-полуфинал: 05.12.2026, 10:00–18:00.
  - Секретный финал 3.0: 06.12.2026, 10:00–19:00.
- Регистрация заканчивается **25.10.2026 в 12:00 МСК**. Ссылки:
  - Академический: `https://aciso.timepad.ru/event/4167286/`
  - СПО: `https://aciso.timepad.ru/event/4167329/`
  - Смешанный: `https://aciso.timepad.ru/event/4167370/`
  - Школьный: `https://aciso.timepad.ru/event/4167419/`
- Состав команды:
  - Академический: 5–7 человек, студенты одного вуза, возраст до 27 лет (на финале <28).
  - Смешанный: 5–7 человек, 14–27 лет, разные организации/молодые специалисты.
  - Школьный/СПО: 3–5 человек.
- Квоты: в очный этап проходят **топ-10 в каждом зачёте** (до 40 команд). В финал 3.0 — **по 2 команды** от академического и смешанного зачётов (4 команды).
- Призовой фонд: **1 000 000 ₽**, делится по 250 000 ₽ на каждый из 4 зачётов, включая НДФЛ 13%; выплата капитану.
- Формат отбора: динамическая система очков; initial 1000, minimum 100, decay 50, формула `ceil((((minimum - initial) / (decay ** 2)) * (solve_count ** 2)) + initial)`.
- В 2025 отборе было 24 задания; топ-10 общий cutoff ~3810 очков. Для академического зачёта cutoff мог быть ниже, но целевой ориентир — 3000+.
- 2025 задачи и очки: beginners по 100 (8 шт.), safelang-серия по 100 (3 шт.), goose/goose-revenge по 100 (2 шт.), Funeral 239, miracle 100, cursed 395, annabelle 793, Wincrack 919, bad_parser 997, play_with_ker 995, trustmebroker 983, BimboIncident 1000, brokilon 983.
- Ключевые техники 2025:
  - babycrypto: кастомный алгоритм + brute seed 100k.
  - babyfor: HTTP-трафик -> битый ZIP -> PPTX -> скрытая картинка.
  - babymisc: integer overflow.
  - babypwn: перезапись младшего байта адреса возврата на `win`.
  - babyrev: IDA + дамп таблицы + XOR 0x42.
  - babyweb: доверие `X-Forwarded-For` + закомментированный код.
  - miracle: рюкзачная криптосистема, meet-in-the-middle.
  - cursed: p-адики, матричный дискретный лог, LLL/BKZ subset sum.
  - safelang: Rust lifetime extension (cve-rs), heap leak/arbitrary R/W, ROP.
  - goose: NoSQL injection (`$regex`) + слепая экстракция флага.
  - trustmebroker: SSRF через headless PDF + обход HTML-фильтра.
  - Funeral: firmware update, binwalk, ext4, cron, AES-ECB, UDP dump.
  - brokilon: registry fileless malware.
  - Wincrack: Windows TLS callback, антидебаг, PEB seed, кастомное шифрование.
  - bad_parser: TOCTOU -> mmap OOB -> libc leak -> overwrite TLS/printf.
  - play_with_ker: kernel heap OOB -> file spray -> KASLR leak via `cpu_entry_area` -> `modprobe_path`.
- 2025 AD сервисы:
  - `veladora` (Go/Gin): IDOR, предсказуемый payment ID, внедрение в диалог произвольного пользователя.
  - `archive` (C++/boost): CVE-2023-34399, отрицательный индекс при десериализации.
  - `warehouse` (Go, 4 микросервиса): UUIDv1 API key + SSRF через gateway, утечка email.
  - `prototype` (Python/Flask/MinIO): CVE-2025-62506, эскалация до admin в MinIO; unintended — переполнение SHA256 солью.
- 2025 superfinal:
  - Machine 1: Telegram bot, webhook без secret_token -> подделка админа -> local Bot API `file://` -> SSH -> `vim.nox cap_setuid` -> root.
  - Machine 2: Windows Sectrans, TOCTOU path traversal, UAF ключа, предсказуемое шифрование -> PowerShell history -> драйвер `HWMonitor.sys` OOB -> BSOD -> MEMORY.DMP -> NT hash -> Pass-the-Hash.
  - Machine 3: web LFI -> `sip.conf` -> Asterisk -> `search_engine` overflow -> `system` -> SUID `time` -> `system_monitor` pickle -> root.
  - Machine 4: crypto/PPC/OSINT -> пароль архива -> Turing machine reversing -> `su flaguser` -> SUID `update_validator` -> `/root/updateKey` -> root.
- В 2021 отборе были задачи web (SSRF, PHP, PDF, JSON config), reverse, pwn (heap, kernel), forensics, crypto (padding oracle, ECC), OSINT.
- В 2022 отборе: crypto (Bleichenbacher, CRC preimage, timing attack, Trithemius), web (SSRF/CRLF/Redis/Celery, WAF bypass duplicate Content-Type, CSP bypass, prototype pollution), pwn (kernel ROP, heap, shellcode), forensics (memory dump, firmware, malware).
- В 2023 отборе: crypto (DH на группе симметрий, Fibonacci mod p^2, murmur3 HLE), web (prototype pollution, CSP bypass, SSRF+Redis+Celery RCE, WAF bypass), pwn (heap 2free, vtable/shellcode, GOT/_fini_array), reverse (Android, polynomial GCD, Bun JS deobfuscation, custom VM), forensics (RAM dump, TLS key, MPEG-TS), PT tasks (LDAP, NFS, stealer).
- В 2025 отборе у всех задач есть README и solve; репозиторий содержит деплой и эксплоиты, что позволяет воспроизводить задачи локально.
- Сайт `ctfcup.ru` — React SPA; PDF положения: `https://ctfcup.ru/doc/polozhenie-x-kubok-ctf-2026.pdf`.
- Архив 2025: `https://2025.ctfcup.ru/`; финал 2025 проходил 5–7 декабря на ВДНХ, павильон «Умный город».
- Победители 2025: академический зачёт — `C4T BuT S4D`; смешанный — `v3rb0s1ty`.
- Timepad для академического зачёта показывает время `31 октября 23:00 — 1 ноября 12:00` (13 ч), но официальное положение и остальные страницы — `12:00—12:00` (24 ч). Нужно ориентироваться на положение и уточнить у оргкомитета.
- На Windows не удалось полностью checkout `ctfcup2025-superfinals` из-за путей с `C:\...`; использовать GitHub raw/API.
- В рабочей папке создана `ctf-prep`, но итоговые документы ещё не написаны.

**A** (msg_16dbd4f730): Начинаю финальную сборку пакета. Сначала запущу параллельно подготовку шпаргалок, пока сам пишу стратегические документы.


#### [synthetic] msg_16dbe18110018mrZd1Mt76XdB9
<subagent sessionID="ses_e9241e7fbffeQIOa435W2fUQeO" state="completed" description="Шпаргалки crypto и forensics">
Готово. Созданы два файла:

- `ctf-prep/07_cheatsheets/crypto.md` — **549 строк**
- `ctf-prep/07_cheatsheets/forensics.md` — **400 строк**

**Crypto:** карта «когда открывать», RSA-атаки (малый `e`, Hastad, common modulus, Wiener, факторизация, partial key, Coppersmith, LLL), классика (XOR, Vigenere, ECB/CBC, padding oracle, CRC, nonce reuse, GCM), современная криптография (ECC, DH, Pohlig–Hellman, p-адики, matrix DLP, knapsack, Bleichenbacher, timing), PRNG, хэши/HMAC, инструменты, таблица 11 задач Кубка, чек-лист на 15 минут и грабли.

**Forensics:** карта артефактов, диск/образ (E01, VMDK, SleuthKit, карвинг), память (Volatility 3, Linux/Windows-дампы), сеть (tshark, TLS 1.3, DNS/SMB/USB HID), Windows-артефакты, Linux/прошивки, malware, стеганография, мобильные, таблица 10 задач Кубка, чек-лист на 20 минут и грабли.

Проверено: Markdown-таблицы не битые, все задачи из списка присутствуют, флаги не выдумывались. Попутно исправлены неточности: убран неверный режим hashcat `17200`, исправлены `windows.shimcaches`, `memprocfs -device`, нумерация байтов USB HID и связка PECmd/SRUM.
</subagent>


#### [compaction] msg_16dc7e8b300155ec2zqFq6ad6T
## Objective
- Максимально подготовиться к X Кубку CTF России 2026: пройти отборочный тур, выиграть финал в Москве и получить призовой фонд.
- Изучить ctfcup.ru и GitHub-репозитории acisoru с заданиями прошлых лет, выдать точный план, документацию, примеры и ключевые акценты подготовки.

## Requirements
- Изучить сайт турнира и всё содержимое репозиториев с заданиями.
- Подготовка должна быть максимально полной: план, документация, примеры, фокусные темы.
- Приоритет: пройти отбор; идеально — выиграть финал и получить призовой фонд.
- Ответ и документация — на русском языке.

## Decisions
- Основной фокус: репозитории Кубка CTF России (`ctfcup2025-quals`, `ctfcup2025-ad`, `ctfcup2025-superfinals`, `ctfcup2023-quals`, `ctfcup22-quals`, `ctfcup-21-quals`, `ctfcup-2020-quals`).
- Смежные репозитории (MIA CTF, VrnCTF, NSK CTF, GoCTF, LetoCTF, OmCTF, CenterCTF) — дополнительная тренировочная база.
- Создана локальная папка `ctf-prep`; репозитории клонированы в `ctf-prep/repos`.
- Документация структурирована как пакет: README + 00–12 + `07_cheatsheets/` + `templates/`.
- Для `ctfcup2025-superfinals` на Windows использовать `git show HEAD:<path>` или GitHub raw из-за путей `C:\...`.

## Work State
### Completed
- Изучен сайт `https://ctfcup.ru/`, JS-бандл, robots.txt, sitemap, архив 2025.
- Скачан и проанализирован официальный PDF положения 2026: `C:\Users\Eugene\AppData\Local\Temp\polozhenie2026.pdf`.
- Установлены `pypdf` и `PyMuPDF`; получен список 50+ репозиториев acisoru.
- Склонированы: `ctfcup2025-quals`, `ctfcup2025-ad`, `ctfcup2025-superfinals` (неполный checkout), `ctfcup2023-quals`, `ctfcup22-quals`.
- Разобраны задачи 2025 (24), 2023 (21 + 3 PT), 2022 (23), 2021 (30), 2020 (25).
- Разобраны AD-сервисы 2025: Veladora, Archive, Warehouse, Prototype; прочитаны writeup'ы.
- Разобраны машины суперфинала 2025 (machine-1…4) через `git show`.
- Созданы аналитические файлы: `repo_inventory.md`, `2025_tasks.md`, `2025_summary.md`, `2022_2023_summary.md`.
- Созданы основные документы:
  - `ctf-prep/README.md`
  - `ctf-prep/00_urgent_checklist.md`
  - `ctf-prep/01_regulations_2026.md`
  - `ctf-prep/02_past_tasks_analysis.md`
  - `ctf-prep/03_qualifier_playbook.md`
  - `ctf-prep/04_seven_day_plan.md`
  - `ctf-prep/05_final_attack_defense.md`
  - `ctf-prep/06_final_secret_pentest.md`
  - `ctf-prep/08_toolkit_setup.md`
  - `ctf-prep/09_team_roles.md`
  - `ctf-prep/10_checklists.md`
  - `ctf-prep/11_training_targets.md`
  - `ctf-prep/12_glossary.md`
- Созданы шаблоны: `templates/exploit_template.py`, `web_exploit.py`, `ad_exploit.py`, `writeup_template.md`, `service_patch_checklist.md`.
- Созданы все 8 шпаргалок:
  - `07_cheatsheets/pwn.md` (~597 строк)
  - `07_cheatsheets/reverse.md` (~678 строк)
  - `07_cheatsheets/web.md` (~550 строк)
  - `07_cheatsheets/ad.md` (~347 строк)
  - `07_cheatsheets/crypto.md` (~550 строк)
  - `07_cheatsheets/forensics.md` (~401 строка)
  - `07_cheatsheets/misc_osint_ppc.md` (~449 строк)
  - `07_cheatsheets/privesc.md` (~516 строк)
- Исправлены: китайский текст в `templates/web_exploit.py`; формула payment ID Veladora в `05_final_attack_defense.md`.
- Проверены факты: babyweb `/purchase-details?secret=premium`, goose `SECRET_KEY="kluchik"` и `/strings`, формат флагов AD `TEAM\d{3}_[A-Z0-9]{32}`, onlytweets HEAD/CSRF.

### Active
- Финальный QA-проход шпаргалок: проверить `ad.md`, `reverse.md`, `privesc.md` на выдуманные детали, битые команды и незаполненные плейсхолдеры.
- Создать `ctf-prep/07_cheatsheets/README.md` — индекс всех 8 шпаргалок.
- Подготовить краткое итоговое резюме пользователю с самым срочным действием (регистрация/команда) и ссылками на файлы.

### Blocked
- `ctfcup2025-superfinals` не чекаутится на Windows из-за путей `C:\...`; читать через `git show HEAD:<path>`.
- Расхождение Timepad: академический зачёт показывает `31 октября 23:00 — 1 ноября 12:00`, положение — `12:00—12:00`; нужно письменное подтверждение оргкомитета.

## Next Move
1. Создать `ctf-prep/07_cheatsheets/README.md` с описанием и порядком использования всех 8 шпаргалок.
2. Провести QA `ad.md`, `reverse.md`, `privesc.md`: сверить эндпоинты/техники с репозиториями, убрать неточности и плейсхолдеры.
3. Проверить, что `README.md` ссылается на все созданные документы, и обновить карту файлов при необходимости.
4. Выдать пользователю краткое резюме: регистрация до 12:00 25.10, состав команды, 3 самых срочных действия и ключевые файлы.
5. При наличии времени — прогнать `04_seven_day_plan.md` и `11_training_targets.md` на соответствие фактическим путям задач.

## Relevant Files
- `ctf-prep/README.md`: главный хаб, срочные действия и карта документов.
- `ctf-prep/00_urgent_checklist.md`: пошаговый чек-лист регистрации и сборов.
- `ctf-prep/01_regulations_2026.md`: факты положения 2026, даты, квоты, приз.
- `ctf-prep/02_past_tasks_analysis.md`: матрица задач 2020–2025 и прогноз 2026.
- `ctf-prep/03_qualifier_playbook.md`: стратегия 24-часового отбора.
- `ctf-prep/04_seven_day_plan.md`: план 24–30.10 с конкретными задачами.
- `ctf-prep/05_final_attack_defense.md`: AD-playbook и разбор 4 сервисов 2025.
- `ctf-prep/06_final_secret_pentest.md`: multi-machine pentest и цепочки 2025.
- `ctf-prep/07_cheatsheets/`: 8 рабочих шпаргалок (web, pwn, crypto, reverse, forensics, misc, AD, privesc).
- `ctf-prep/08_toolkit_setup.md`: установка WSL/Kali/Docker и инструментов.
- `ctf-prep/09_team_roles.md`: роли, связь, договор о призе.
- `ctf-prep/10_checklists.md`: печатные чек-листы T-7/T-1/T-0.
- `ctf-prep/11_training_targets.md`: конкретные задачи с путями и временем.
- `ctf-prep/templates/`: скелеты эксплойтов, writeup и чек-лист патча.
- `C:\Users\Eugene\AppData\Local\Temp\polozhenie2026.pdf`: официальное положение 2026.

## Important Context
- Официальные даты 2026:
  - Отбор: **31.10.2026 12:00 — 01.11.2026 12:00 МСК**, 24 часа, jeopardy.
  - Финал: **04–06.12.2026**, Москва.
  - 04.12 — школьный/СПО AD, 10:00–19:00; 05.12 — академический/смешанный AD, 10:00–18:00; 06.12 — секретный финал 3.0, 10:00–19:00.
- Регистрация до **25.10.2026 12:00 МСК**:
  - Академический: `https://aciso.timepad.ru/event/4167286/`
  - СПО: `https://aciso.timepad.ru/event/4167329/`
  - Смешанный: `https://aciso.timepad.ru/event/4167370/`
  - Школьный: `https://aciso.timepad.ru/event/4167419/`
- Состав: академический/смешанный — 5–7 человек; СПО/школьный — 3–5. Академический: студенты одного вуза, до 27 лет (на финале <28). Смешанный: 14–27, разные организации.
- Квоты: топ-10 в каждом зачёте (до 40 команд); в финал 3.0 — по 2 команды от академического и смешанного (4 команды).
- Призовой фонд: **1 000 000 ₽**, по 250 000 ₽ на 4 зачёта, включая НДФЛ 13%; получает капитан.
- Scoring: initial 1000, minimum 100, decay 50; `score = ceil(1000 − 0.36 × n²)`.
- 2025: 24 задачи, cutoff топ-10 ≈3810; цель 4000+.
- 2025 очки: beginners по 100 (8), safelang ×3 по 100, goose ×2 по 100, Funeral 239, miracle 100, cursed 395, annabelle 793, Wincrack 919, bad_parser 997, play_with_ker 995, trustmebroker 983, BimboIncident 1000, brokilon 983.
- Ключевые техники 2025: cve-rs lifetime, kernel heap OOB, TOCTOU/mmap OOB, Windows TLS callback, fileless malware, SSRF через headless PDF, NoSQLi.
- AD 2025: veladora (IDOR/предсказуемый payment ID/инъекция в диалог), archive (CVE-2023-34399), warehouse (UUIDv1 API key + SSRF), prototype (MinIO CVE-2025-62506 + переполнение соли HMAC).
- Superfinal 2025: machine-1 Telegram webhook → Bot API `file://` → SSH → `vim.nox cap_setuid`; machine-2 TOCTOU/UAF → `HWMonitor.sys` OOB → MEMORY.DMP → NT hash → PTH; machine-3 LFI → `sip.conf` → Asterisk overflow → SUID `time` → pickle; machine-4 crypto/PPC/OSINT → архив → Turing machine → `su flaguser` → SUID `update_validator`.


#### [synthetic] msg_16dbe1816001O3eRYwlJ1UasbH
<subagent sessionID="ses_e9241e7f5ffeaS4L4WPcUxx7tr" state="completed" description="Шпаргалки misc и privesc">
Готово. Оба документа созданы, проверены на объём и кодировку.

| Файл | Строк | Лимит |
|---|---:|---:|
| `ctf-prep/07_cheatsheets/misc_osint_ppc.md` | 448 | 300–450 |
| `ctf-prep/07_cheatsheets/privesc.md` | 515 | 350–550 |

`privesc.md` был сокращён с 885 до 515 строк без потери обязательных разделов. Оба файла — UTF-8 без BOM, блоки кода сбалансированы, других файлов не изменял.

**Ключевые приёмы в `misc_osint_ppc.md`:**
- OSINT: Google/Яндекс dorks, поиск по никам, email, Telegram, GitHub, метаданным и геолокации.
- Misc/stego: `file`, `strings`, `binwalk`, `exiftool`, `zsteg`, `steghide`, QR/аудио, вложенные архивы.
- PPC: шаблоны pwntools, `recvuntil`, парсинг, float-допуски, переполнение int, отрицательная ставка.
- Разбор задач 2025 и 2022–2023: `checkpoint`, `floating_in_delirium`, `slons`, `gamer`, `math_pong`, `classic_matreshka`.
- Чек-лист «10 минут на misc» и 12 типовых ошибок.

**Ключевые приёмы в `privesc.md`:**
- Linux: `sudo`/GTFOBins, SUID/SGID, capabilities, cron wildcard, systemd, PATH, NFS `no_root_squash`, Docker/LXD, kernel CVE.
- Windows: ACL, unquoted service path, Potato-семейство, SeBackup/SeRestore, AlwaysInstallElevated, SAM/LSASS/NTDS, Pass-the-Hash, WinRM/RDP.
- Pivoting: chisel, ligolo-ng, SSH-туннели, proxychains, socat, `netsh portproxy`.
- Post-exploitation: поиск флагов, сбор лута, persistence и cleanup.
- Цепочки суперфинала 2025: Telegram webhook + Bot API `file://` + vim `cap_setuid`; Sectrans TOCTOU/UAF + HWMonitor.sys + MEMORY.DMP + PTH; LFI `%252e%252e%252f` + Asterisk overflow + SUID `time` + pickle; crypto/PPC/OSINT + машина Тьюринга + SUID `update_validator`.
- Два чек-листа по 15 минут и 16 типовых ошибок.
</subagent>


#### [synthetic] msg_16dbe1820001qF11IoosIuJlHS
<subagent sessionID="ses_e9241e7fcffeGKQgluXiXZhGbJ" state="completed" description="Шпаргалки web и AD">
Готово. Созданы два файла, остальные не затрагивал.

| Файл | Строк | Статус |
|---|---:|---|
| `ctf-prep/07_cheatsheets/web.md` | 550 | в диапазоне 350–550 |
| `ctf-prep/07_cheatsheets/ad.md` | 346 | в диапазоне 300–500 |

**web.md** — разведка, SQLi/NoSQLi/SSTI/command/LDAP/XPath, JWT/OAuth/сессии/IDOR/race/reset/2FA, SSRF (включая Puppeteer и metadata), LFI/RFI/wrappers/upload/ZIP slip/XXE, десериализация PHP/Python/Java/Node/.NET, XSS/CSP/CSRF/CORS/prototype pollution/postMessage, CRLF/smuggling/cache poisoning/HTTP2/WebSocket, таблица 12 задач 2022–2025 с реальными payload, 30-минутный чек-лист и типовые грабли.

**ad.md** — роли, таймлайн 10:00–19:00, 15-минутный цикл, первые 30 минут (VPN/доступы/snapshot/инвентарь/checker), аудит сервисов, безопасные патчи, ротация секретов, WAF/логи/rollback, шаблон многопоточного эксплойта, отправка флагов, детальный разбор veladora, archive, warehouse и prototype по реальным эндпоинтам и CVE, чек-листы защиты/атаки и типовые ошибки.
</subagent>


#### [synthetic] msg_16dcf0ba7001ZYNQEpFhj1ZGBx
The previous response was interrupted. Continue from where you left off without repeating completed content.


#### [synthetic] msg_16dbe181c001jwKa1xP4VmDBML
<subagent sessionID="ses_e9241e7fdffeHU9FHSYu3bcgub" state="completed" description="Шпаргалки pwn и reverse">
Готово.

| Файл | Строк |
|---|---:|
| `ctf-prep/07_cheatsheets/pwn.md` | 596 |
| `ctf-prep/07_cheatsheets/reverse.md` | 595 |

Проверено: все 23 названия задач сверены с репозиториями, code fences и таблицы целы, реальные флаги не включены — только placeholder `ctfcup{}`.

**5 важнейших приёмов**

1. **Триаж и точное окружение** — `checksec`, `seccomp-tools`, определение libc/loader, `patchelf`/`pwninit`; без этого локальный эксплойт падает по чужой причине.
2. **Leak-first** — сначала canary/libc/heap/KASLR, затем второй стадией ROP; не хардкодить адреса и не надеяться на ASLR.
3. **Heap + FSOP** — tcache poisoning с safe-linking, unsorted-bin leak, overlap/off-by-one; для glibc 2.34+ — FSOP через `_IO_2_1_stdout_`/`_wide_data`.
4. **Kernel pwn** — распаковка `bzImage`/`vmlinux`/`cpio`, KASLR leak, `modprobe_path`, `userfaultfd`, обход SMEP/SMAP/KPTI.
5. **Reverse: от рантайма к логике** — DIE/`rabin2`/строки → x64dbg/Frida/gdb → VM dispatch и lift handler'ов → angr/Z3 там, где есть арифметика, а не крипта.
</subagent>


#### [compaction] msg_16dd367d1002EcRE3u0FZtyxLo
## Objective
- Максимально подготовиться к X Кубку CTF России 2026: пройти отбор, выиграть финал в Москве и получить призовой фонд.
- Изучить `ctfcup.ru` и GitHub-репозитории `acisoru` с заданиями прошлых лет; выдать точный план, документацию, примеры и ключевые акценты подготовки.

## Requirements
- Изучить сайт турнира и всё содержимое репозиториев с заданиями.
- Подготовка должна быть максимально полной: план, документация, примеры, фокусные темы.
- Приоритет: пройти отбор; идеально — выиграть финал и получить призовой фонд.
- Ответ и документация — на русском языке.

## Decisions
- Основной фокус: репозитории Кубка CTF России (`ctfcup2025-quals`, `ctfcup2025-ad`, `ctfcup2025-superfinals`, `ctfcup2023-quals`, `ctfcup22-quals`, `ctfcup-21-quals`, `ctfcup-2020-quals`).
- Смежные репозитории (MIA CTF, VrnCTF, NSK CTF, GoCTF, LetoCTF, OmCTF, CenterCTF) — дополнительная тренировочная база.
- Документация структурирована как пакет: README + 00–12 + `07_cheatsheets/` + `templates/`.
- Для `ctfcup2025-superfinals` на Windows использовать `git show HEAD:<path>` или GitHub raw из-за путей `C:\...`.

## Work State
### Completed
- Изучены сайт `https://ctfcup.ru/`, JS-бандл, robots.txt, sitemap, архив 2025 и официальное положение 2026.
- Склонированы и разобраны репозитории 2020–2025; созданы `analysis/repo_inventory.md`, `analysis/2025_tasks.md`, `analysis/2025_summary.md`, `analysis/2022_2023_summary.md`.
- Созданы основные документы `ctf-prep/README.md`, `00_urgent_checklist.md`–`12_glossary.md`, шаблоны в `templates/` и 8 шпаргалок.
- Создан `ctf-prep/07_cheatsheets/README.md` — индекс всех шпаргалок, порядок использования для отбора и финала, соглашения по плейсхолдерам.
- QA шпаргалок: исправлены `ad.md` (UUIDv1 brute `prefix + 0..49`, `username.lower()` в payment ID), `reverse.md` (`plb.exe` вместо неверного `pcf`, MITM 28+28 для `miracle`, убрано ошибочное утверждение про timing в `watcher`), `privesc.md` (`accesschk -accepteula`).
- Главный `README.md` дополнен ссылкой на индекс шпаргалок; в `04_seven_day_plan.md` добавлено предупреждение: 25.10 до 12:00 регистрация важнее тренировки.
- Проверены все `.md`: UTF-8 без BOM, без `U+FFFD`, блоки кода сбалансированы.
- Сверены с репозиториями факты по Veladora, Archive, Warehouse, Prototype, задачам reverse 2022–2025 и цепочкам superfinal machine-1…4.
- Проверена страница Timepad академического зачёта: она открыта, но показывает `31 октября 23:00 — 1 ноября 12:00` и финал `5–7 декабря 2026`.

### Active
- Финальная сверка дат и времени финала во всех документах.
- Подготовка краткого итогового ответа пользователю с самым срочным действием и ссылками на файлы.

### Blocked
- Расхождение Timepad и положения: академическая страница показывает старт `31.10 23:00` вместо `12:00` и финал `5–7 декабря` вместо `4–6 декабря`; нужно письменное подтверждение оргкомитета.
- `ctfcup2025-superfinals` не чекаутится на Windows из-за путей `C:\...`; читать через `git show HEAD:<path>`.
- Официальные часы финала в PDF (`04.12 09:00–19:30`, `05.12 09:00–19:30`, `06.12 09:00–20:00`) пока не перенесены в README, `01`, `05`, `06`, `10` и `ad.md` — там ещё стоят `10:00–19:00` / `10:00–18:00`.

## Next Move
1. Исправить время финала во всех документах на официальное: `04.12 09:00–19:30`, `05.12 09:00–19:30`, `06.12 09:00–20:00`; проверить `README.md`, `01_regulations_2026.md`, `05_final_attack_defense.md`, `06_final_secret_pentest.md`, `10_checklists.md`, `07_cheatsheets/ad.md`.
2. Добавить во `01_regulations_2026.md` и `README.md` явное предупреждение о расхождении Timepad: финал `5–7 декабря` против официального `4–6 декабря`, старт `23:00` против `12:00`.
3. Проверить, что все ссылки в `07_cheatsheets/README.md` и главном `README.md` ведут на существующие файлы.
4. Выдать пользователю краткое резюме: регистрация до 12:00 25.10, состав команды, 3 самых срочных действия и ключевые файлы.

## Relevant Files
- `ctf-prep/README.md`: главный хаб, срочные действия, карта документов.
- `ctf-prep/00_urgent_checklist.md`: пошаговый чек-лист регистрации и сборов.
- `ctf-prep/01_regulations_2026.md`: факты положения 2026, даты, квоты, приз.
- `ctf-prep/04_seven_day_plan.md`: план 24–31.10 с конкретными задачами.
- `ctf-prep/07_cheatsheets/README.md`: индекс и порядок использования шпаргалок.
- `ctf-prep/07_cheatsheets/ad.md`: AD-playbook и разбор 4 сервисов 2025.
- `ctf-prep/07_cheatsheets/reverse.md`: reverse-шпаргалка и разбор задач.
- `ctf-prep/07_cheatsheets/privesc.md`: Linux/Windows privesc и цепочки superfinal.
- `ctf-prep/03_qualifier_playbook.md`: стратегия 24-часового отбора.
- `ctf-prep/05_final_attack_defense.md`: полный AD-playbook.
- `ctf-prep/06_final_secret_pentest.md`: multi-machine pentest.
- `ctf-prep/11_training_targets.md`: конкретные задачи с путями и временем.
- `ctf-prep/analysis/2025_summary.md`: сырой разбор задач 2025.
- `ctf-prep/repos/ctfcup2025-ad`: исходники AD-сервисов 2025.
- `C:\Users\Eugene\AppData\Local\Temp\polozhenie2026.pdf`: официальное положение 2026.

## Important Context
- Официальные даты 2026:
  - Отбор: **31.10.2026 12:00 — 01.11.2026 12:00 МСК**, 24 часа, jeopardy.
  - Финал: **04–06.12.2026**, Москва.
  - 04.12 — школьный/СПО AD, **09:00–19:30**.
  - 05.12 — академический/смешанный AD, **09:00–19:30**.
  - 06.12 — секретный финал 3.0, **09:00–20:00**.
  - Вручение призов — 06.12.2026.
- Регистрация до **25.10.2026 12:00 МСК**:
  - Академический: `https://aciso.timepad.ru/event/4167286/`
  - СПО: `https://aciso.timepad.ru/event/4167329/`
  - Смешанный: `https://aciso.timepad.ru/event/4167370/`
  - Школьный: `https://aciso.timepad.ru/event/4167419/`
- Состав: академический/смешанный — 5–7 человек; СПО/школьный — 3–5. Академический: студенты одного вуза, до 27 лет включительно; на финале возраст не должен превышать 28 лет. Смешанный: 14–27, разные организации.
- Квоты: топ-10 в каждом зачёте (до 40 команд); в финал 3.0 — по 2 команды от академического и смешанного (4 команды).
- Призовой фонд: **1 000 000 ₽**, по 250 000 ₽ на 4 зачёта, включая НДФЛ 13%; получает капитан.
- Scoring: initial 1000, minimum 100, decay 50; `score = ceil(1000 − 0.36 × n²)`.
- 2025: 24 задачи, cutoff топ-10 ≈3810; цель 4000+.
- Ключевые техники 2025: cve-rs lifetime, kernel heap OOB, TOCTOU/mmap OOB, Windows TLS callback, fileless malware, SSRF через headless PDF, NoSQLi.
- AD 2025: veladora (IDOR/предсказуемый payment ID/инъекция в диалог), archive (CVE-2023-34399), warehouse (UUIDv1 API key + SSRF), prototype (MinIO CVE-2025-62506 + переполнение соли HMAC).
- Superfinal 2025: machine-1 Telegram webhook → Bot API `file://` → SSH → `vim.nox cap_setuid`; machine-2 TOCTOU/UAF → `HWMonitor.sys` OOB → MEMORY.DMP → NT hash → PTH; machine-3 LFI → `sip.conf` → Asterisk overflow → SUID `time` → pickle; machine-4 crypto/PPC/OSINT → архив → Turing machine → `su flaguser` → SUID `update_validator`.
- Timepad академического зачёта показывает `31 октября 23:00 — 1 ноября 12:00` и финал `5–7 декабря 2026`; это противоречит официальному положению и требует письменного подтверждения.

**A** (msg_16ddb908e0): Готово. Пакет подготовки сверен с официальным положением 2026 и обновлён.

## 1. Самое срочное — сегодня

Регистрация закрывается **25.10.2026 в 12:00 МСК**. По времени вашей машины (UTC+6) это **25.10 в 15:00**, то есть осталось около **20,5 часов**.

- [ ] Подать заявку: <https://aciso.timepad.ru/event/4167286/> (академический зачёт).
- [ ] Сохранить номер заявки и письмо-подтверждение.
- [ ] Проверить состав: **5–7 человек**, все студенты **одного вуза**, возраст **до 27 лет** включительно; на финале — **до 28**.
- [ ] Отправить письмо в оргкомитет по готовому шаблону: `ctf-prep/templates/email_orgcommittee.md`.
- [ ] Зафиксировать в командном чате, как делится приз: **250 000 ₽** на зачёт, включая НДФЛ 13%, получает капитан.

## 2. Расхождение, которое нельзя игнорировать

| Источник | Отбор | Финал |
|---|---|---|
| Официальное положение | `12:00 31.10 — 12:00 01.11` | `04–06.12.2026` |
| Timepad академического зачёта | `23:00 31.10 — 12:00 01.11` | `5–7 декабря 2026` |

Что делать:

1. Письменно подтвердить у оргкомитета оба пункта — шаблон уже готов.
2. Не покупать невозвратные билеты на 04.12 до ответа.
3. Держать вечер 31.10 свободным: если старт действительно в 23:00, график сна сдвигается на 11 часов (это уже учтено в `03_qualifier_playbook.md` и `00_urgent_checklist.md`).

Контакты: `info@aciso.ru`, `zoi@aciso.ru`, `+7 (495) 640-53-30`, `@zoi345`.

## 3. Что обновлено в документации

- Официальные окна финала:
  - **04.12** — школьный и СПО, финал 2.5: день `09:00–19:30`, игра `10:00–19:00`;
  - **05.12** — академический и смешанный, полуфинал 2.0: день `09:00–19:30`, игра `10:00–18:00`;
  - **06.12** — секретный финал 3.0: день `09:00–20:00`, игра `10:00–19:00`, награждение `19:00–20:00`.
- Во все ключевые документы добавлено предупреждение о расхождении с Timepad.
- Добавлен готовый шаблон письма в оргкомитет.
- Проверены ссылки, кодировка UTF-8 и блоки кода.

## 4. Ключевые файлы

| Файл | Зачем |
|---|---|
| `ctf-prep/README.md` | Главный хаб: календарь, цели, карта документов |
| `ctf-prep/00_urgent_checklist.md` | Пошагово на сегодня: регистрация, состав, связь |
| `ctf-prep/01_regulations_2026.md` | Положение: зачёты, квоты, приз, спорные места |
| `ctf-prep/04_seven_day_plan.md` | План 24–31.10 с конкретными задачами |
| `ctf-prep/03_qualifier_playbook.md` | Стратегия 24-часового отбора |
| `ctf-prep/07_cheatsheets/README.md` | Индекс 8 шпаргалок и порядок использования |
| `ctf-prep/11_training_targets.md` | Конкретные задачи из репозиториев с оценкой времени |
| `ctf-prep/templates/email_orgcommittee.md` | Письмо в оргкомитет |
| `ctf-prep/analysis/2025_summary.md` | Разбор задач 2025 |

## 5. План на ближайшие дни

- **24.10:** заявка, письмо в оргкомитет, созвон команды, старт настройки окружения.
- **25.10 после 12:00:** beginners 2025, проверка инструментов, первый короткий mock.
- **26–30.10:** идти по `04_seven_day_plan.md`: web/pwn/crypto/reverse/forensics, один mock-контест 3–4 часа, разбор ошибок.
- **31.10 12:00:** отбор. Цель — **4000+ очков** и топ-10 зачёта; для топ-3 — **6000+**.

## 6. Фокус отбора

1. **Web:** IDOR, SSRF, NoSQLi, prototype pollution, LFI, десериализация.
2. **Pwn:** ret2libc/ROP, heap, форматные строки, kernel OOB, Rust lifetime.
3. **Crypto:** RSA-атаки, LLL, MT19937, padding oracle, ECC.
4. **Forensics:** pcap, память Windows, реестр, вложенные архивы, fileless malware.
5. **Reverse:** TLS callbacks, антидебаг, VM, Rust/Go, Android.
6. **Misc/PPC:** автоматизация nc, парсинг, OSINT, pyjail.

Главное правило отбора: **сначала ширина, потом глубина**. За первые 90 минут прочитать все задачи и снять всё, что решается за 10–20 минут. Флаг отправлять сразу.

Если хотите, следующим шагом могу собрать таблицу для заполнения заявки по вашему составу или проверить конкретные тренировочные задачи под сильные/слабые места команды.


#### [idle] msg_16ddc4170001Xus7KcBnD1jW8H
{"id": "msg_16ddc4170001Xus7KcBnD1jW8H", "time": {"created": 1792844513648}, "type": "idle", "outcome": "succeeded"}


#### [model-switched] msg_16de5f34a0010AP2dyzS2y3mcI
switch: max -> None


#### [user] msg_16de5f2e1001Q7JtO0mtFQkO8E
я учусь в октс, в команде 4 человека, сколько я получу и на каких заданиях сделать акцент? мне очень важно победить и забрать призовой фонд

**A** (msg_16de8c7630): Важная поправка: если ОКТС — это колледж/техникум (СПО), а в команде **4 человека**, ваш зачёт — **СПО**, не академический. Академический требует **5–7 студентов одного вуза**, поэтому с 4 участниками он не подходит.

## 1. Сколько вы получите

Призовой фонд — **1 000 000 ₽**, но он делится по **250 000 ₽ на каждый из 4 зачётов**. Деньги получает **только команда, занявшая 1-е место в своём зачёте**. За 2–3 места гарантированного денежного приза нет.

Если вы выигрываете **СПО-зачёт**:

```text
250 000 ₽ − НДФЛ 13% (32 500 ₽) = 217 500 ₽
217 500 ₽ / 4 человека = 54 375 ₽ на человека
```

| Состав | На человека при равном делении |
|---:|---:|
| 3 | 72 500 ₽ |
| **4** | **54 375 ₽** |
| 5 | 43 500 ₽ |

Нюансы:

- Приз перечисляют **на банковский счёт капитана**, а не каждому отдельно. Дальше капитан распределяет по договорённости.
- Договоритесь о делении **письменно до старта**: кто капитан, как делим, что если кто-то не едет на финал.
- Капитан должен будет предоставить паспорт, ИНН, банковские реквизиты; участники — паспорт и подтверждение учёбы/регистрации. Это стоит подготовить заранее.
- 4 человека — допустимый минимум для СПО. Пятый имеет смысл только если он реально закрывает отдельную роль; иначе он снижает долю каждого и усложняет координацию.

## 2. Что сделать сегодня

Регистрация закрывается **25.10.2026 в 12:00 МСК**. По Омску это **15:00**, осталось около **20 часов**.

- [ ] Регистрироваться в **СПО-зачёте**: <https://aciso.timepad.ru/event/4167329/>.
- [ ] Проверить, что **все 4 — учащиеся одного колледжа (ОКТС)**. Если кто-то из другого учебного заведения — СПО-зачёт нельзя, нужен смешанный 5–7 человек.
- [ ] Проверить возраст: на странице СПО написано «до 27 лет», в положении — «на дату финала не более 28». Если кому-то 27–28, уточнить письменно.
- [ ] Сохранить подтверждение заявки.
- [ ] Отправить письмо в оргкомитет: `ctf-prep/templates/email_orgcommittee.md`. Главный вопрос — **дата финала СПО**: официально **04.12.2026**, а Timepad показывает **5–7 декабря**. Не покупайте невозвратные билеты до ответа.

Для СПО страница Timepad показывает корректное начало отбора — **12:00–12:00**, проблемы с `23:00` касаются академической страницы. Но дату финала всё равно подтвердите.

## 3. На каких заданиях сделать акцент

### Отбор: 31.10 12:00 — 01.11 12:00

Цель для СПО: **10–14 задач, 3500–4000+ очков**. Этого с запасом хватает для топ-10, но для победы в финале нужно ещё AD.

**P0 — обязательный минимум:**

| Блок | Задачи | Кто |
|---|---|---|
| Beginners 2025 | `babyweb`, `babypwn`, `babycrypto`, `babyrev`, `babyfor`, `babymisc`, `babyppc`, `babyosint` | все 4, по 2 задачи |
| Web | `goose`, `goose-revenge` | web-человек |
| Crypto | `miracle`, `stolen_blueprints` | crypto-человек |
| Forensics | `Funeral`, `zion` | forensics-человек |
| Pwn | `safelang`, `babystack` | pwn-человек |

**P1 — если остаётся время:**

| Блок | Задачи |
|---|---|
| Web | `trustmebroker` (SSRF через headless PDF), `mistakes` (prototype pollution), `waf` |
| Crypto | `important_task` (CRC), `geometry`, `murdata` |
| Reverse | `annabelle`, `Wincrack` |
| Forensics | `zion-revenge`, `gamer` |
| Pwn | `safelang-revenge`, `shellyha` |
| Misc/PPC | `checkpoint`, `slons`, `gamer` |

Пути к задачам — в `ctf-prep/11_training_targets.md`. Начинайте с 8 beginners: они дают быстрые очки и разогревают команду.

**Чего не делать на отборе:** не лезть в kernel pwn (`play_with_ker`, `watcher`), тяжёлую крипту (`dinosaurs`) и задачи на 4–5 часов, пока не сняты все дешёвые. Одна сложная задача не стоит восьми лёгких.

### Финал СПО: 04.12.2026, Attack-Defense

Это ключевое отличие от академического пути: **ваш финал — AD 04.12**, а не multi-machine pentest 06.12. Секретный финал 3.0 — только для академического и смешанного зачётов. Не тратьте время на `06_final_secret_pentest.md` и цепочки суперфинала.

Что тренировать:

| Сервис 2025 | Уязвимость | Что отработать |
|---|---|---|
| `veladora` | IDOR, предсказуемый payment ID, инъекция в диалог | чтение Go-кода, проверка владельца объекта, брут ID |
| `archive` | boost serialization, CVE-2023-34399 | разбор C++, отрицательные индексы, heap feng shui |
| `warehouse` | UUIDv1 как API key, SSRF в gateway | микросервисы, заголовки, brute времени, прокси |
| `prototype` | MinIO CVE-2025-62506, переполнение соли HMAC | S3-подпись, service-account, права, `latest`-образы |

На AD с 4 людьми:

- **1 человек = 1 сервис**: аудит, патч, восстановление.
- Капитан дополнительно координирует, следит за SLA и отправкой флагов.
- Все атаки автоматизировать: один скрипт на сервис, таймауты 3–5 секунд, 10–20 потоков, логирование флагов.
- Главное правило: **сначала стабильность, потом атака**. Патч, который ломает checker, хуже уязвимости.
- Провести минимум **2–3 mock AD** по 3–4 часа до 04.12.

## 4. Реалистичная оценка

Шанс есть, но с 4 людьми запаса нет:

- Нужно пройти **топ-10 СПО** на отборе.
- В финале СПО — **20 команд** (10 школьных + 10 СПО), и только **1-е место** даёт 250 000 ₽.
- 4 человека должны закрывать web, pwn, crypto, reverse/forensics и AD-защиту одновременно. Если одна категория провисает — ищите сильного пятого или перераспределяйте роли.

Практический план на 7 дней:

1. **24.10:** регистрация в СПО, письмо в оргкомитет, созвон, распределение ролей.
2. **25.10:** все 8 beginners, проверить инструменты.
3. **26–27.10:** web + crypto P0.
4. **28–29.10:** forensics + reverse + pwn P0.
5. **30.10:** mock-контест 4 часа, разбор.
6. **31.10:** отбор.

После отбора — сразу переходить на `05_final_attack_defense.md` и `07_cheatsheets/ad.md`, а не на суперфинал.

Если хотите, я могу собрать под вас **точный 7-дневный график на 4 человека** — с распределением задач по именам/ролям и чек-листом на каждый день. Для этого напишите, кто в команде сильнее: web, pwn, crypto, reverse или forensics.


#### [idle] msg_16de9827f001eftsq6RMCzY7TR
{"id": "msg_16de9827f001eftsq6RMCzY7TR", "time": {"created": 1792845382271}, "type": "idle", "outcome": "succeeded"}


#### [user] msg_16df91e7b001rDU4tR148RO3Xi
так, ладно, тогда нужно пока что сделать МАКСИМАЛЬНЫЙ фокус на отборочных задач, переходя от детального рассмотрения и изучения легких заданий и заканчивая самыми реальными из сложных задач для моей категории


#### [compaction] msg_16df970660021wbN2wnydU1IPH
## Objective
- Подготовить команду из 4 человек от ОКТС (СПО) к X Кубку CTF России 2026: пройти отбор, выиграть СПО-зачёт 04.12 и получить 250 000 ₽.
- Сейчас максимально сфокусироваться на отборочных задачах: от детального разбора лёгких до реалистичных сложных задач уровня СПО.

## Requirements
- Приоритет — отбор; затем победа в СПО Attack-Defense 04.12.
- Нужен прогресс от простых задач к сложным, а не хаотичный список.
- Ответы и документация — на русском.
- Команда: 4 человека, ОКТС.

## Decisions
- Зачёт — СПО, не академический: академический требует 5–7 студентов одного вуза.
- Цель отбора: 3500–4000+ очков, 10–14 задач; ориентир общего топ-10 2025 — 3810.
- Для СПО финал — только AD 04.12; multi-machine pentest 06.12 не готовить.
- Пропускать kernel pwn, тяжёлую крипту и задачи с низким шансом решения.
- Приз: только 1-е место в СПО; 250 000 ₽ gross → 217 500 ₽ net → 54 375 ₽ на человека при составе 4.
- Создать отдельный документ по отборочному фокусу СПО.

## Work State

### Completed
- Изучены `ctfcup.ru`, официальное положение 2026 и репозитории `acisoru` 2020–2025.
- Созданы `ctf-prep/README.md`, документы `00`–`12`, `07_cheatsheets/`, `templates/`, `analysis/`.
- Обновлены официальные окна финала: 04.12 `09:00–19:30` (игра `10:00–19:00`), 05.12 `09:00–19:30` (игра `10:00–18:00`), 06.12 `09:00–20:00` (игра `10:00–19:00`, награждение `19:00–20:00`).
- Во все ключевые документы добавлено предупреждение о расхождении Timepad.
- Добавлен `ctf-prep/templates/email_orgcommittee.md`.
- В `01_regulations_2026.md` добавлены расчёт для 4 человек и явное условие «250 000 ₽ только за 1-е место».
- В `00_urgent_checklist.md` добавлено правило «колледж + 4 человека = только СПО».
- Проверены UTF-8, BOM, `U+FFFD`, блоки кода и ссылки в основных документах.
- Пользователю дан ответ: СПО-зачёт, ссылка регистрации, расчёт приза, список приоритетных задач и AD-фокус.

### Active
- Собирается максимальный план подготовки к отбору для СПО: tier-прогрессия от beginners до реалистичных сложных задач.
- Изучаются README/writeup задач 2025, 2023 и 2022 для точных техник, таймбоксов и типичных ошибок.
- Подтверждён состав каталогов 2025: beginners — 8, web — 3, crypto — 2, reverse — 4, pwn — 5, forensic — 3.

### Blocked
- Нет письменного подтверждения оргкомитета по датам финала: Timepad показывает `5–7 декабря`, официальное положение — `04–06.12`; для СПО официально `04.12`.
- Академическая страница Timepad показывает старт `31.10 23:00`; страница СПО — корректные `12:00–12:00`.
- `analysis/2025_tasks.md` содержит нечётное число code fences (121); пока не исправлено.

## Next Move
1. Прочитать README/writeup выбранных задач 2025/2023/2022 и выписать точные техники, таймбоксы и подводные камни.
2. Создать `ctf-prep/13_spo_qualifier_focus.md`: tier-прогрессия, карточки задач, роли на 4 человека, 7-дневный график, mock-контест, score-стратегия и skip-list.
3. Добавить ссылку на новый документ в `README.md`, `04_seven_day_plan.md` и `11_training_targets.md`.
4. При необходимости исправить code fences в `analysis/2025_tasks.md`.
5. Выдать пользователю сжатый план: что решать сегодня, что завтра, что после 25.10.

## Relevant Files
- `ctf-prep/11_training_targets.md`: пути, техники и оценки времени по задачам.
- `ctf-prep/analysis/2025_tasks.md`: сырой разбор задач 2025; основа для карточек.
- `ctf-prep/analysis/2025_summary.md`: сводка техник и цепочек 2025.
- `ctf-prep/repos/ctfcup2025-quals/tasks`: исходники и writeup задач 2025.
- `ctf-prep/repos/ctfcup2023-quals/tasks`: задачи 2023 для среднего уровня.
- `ctf-prep/repos/ctfcup22-quals/tasks`: задачи 2022 для среднего уровня.
- `ctf-prep/README.md`: главный хаб; сюда добавить новый документ.
- `ctf-prep/04_seven_day_plan.md`: план 24–31.10; переписать под СПО-фокус.
- `ctf-prep/00_urgent_checklist.md`: регистрация, дедлайн, СПО-зачёт.
- `ctf-prep/01_regulations_2026.md`: даты, приз, условие 1-го места, расчёт на 4.
- `ctf-prep/05_final_attack_defense.md`: AD-финал 04.12; использовать после отбора.
- `ctf-prep/07_cheatsheets/ad.md`: таймлайн и AD-playbook.
- `ctf-prep/07_cheatsheets/README.md`: индекс шпаргалок.
- `ctf-prep/templates/email_orgcommittee.md`: письмо для подтверждения дат.
- `C:\Users\Eugene\AppData\Local\Temp\polozhenie2026.txt`: извлечённый текст официального положения.

## Important Context
- Отбор: `31.10.2026 12:00 — 01.11.2026 12:00 МСК`, 24 часа, jeopardy.
- СПО-финал: `04.12.2026`, день `09:00–19:30`, игра `10:00–19:00`, Москва.
- Регистрация до `25.10.2026 12:00 МСК`; локально Омск UTC+6 — до `15:00`, на 24.10 18:19 оставалось около 20 часов.
- Ссылка СПО: `https://aciso.timepad.ru/event/4167329/`; академический: `4167286`; смешанный: `4167370`; школьный: `4167419`.
- Все 4 участника должны быть из одной организации СПО; возраст на странице — до 27, в положении — не более 28 на дату финала.
- Приз: 1 000 000 ₽ на 4 зачёта; 250 000 ₽ только победителю зачёта; НДФЛ 13%; капитан получает на счёт.
- 4 человека: 54 375 ₽ каждому; 5: 43 500 ₽; 3: 72 500 ₽.
- 2025: общий топ-10 заканчивался на 3810 очках, первое место — 7707.
- Приоритет отбора: 8 beginners; web `goose`, `goose-revenge`, `trustmebroker`; crypto `miracle`, `stolen_blueprints`, `important_task`; forensics `Funeral`, `zion`, `zion-revenge`, `gamer`; reverse `annabelle`, `Wincrack`; pwn `safelang`, `safelang-revenge`, `babystack`; misc `checkpoint`, `slons`, `gamer`.
- Пропускать: `play_with_ker`, `watcher`, `dinosaurs`, `nanomachines`, `BimboIncident` на первом проходе.
- AD 2025 для тренировки: `veladora` (IDOR/payment ID/диалог), `archive` (boost serialization CVE-2023-34399), `warehouse` (UUIDv1/SSRF), `prototype` (MinIO CVE-2025-62506/HMAC).
- На AD с 4 людьми: 1 сервис = 1 владелец, капитан координирует SLA и флаги, обязательна автоматизация и 2–3 mock-сессии.
- QA основных документов: 25 `.md` проверены, UTF-8 без BOM, без `U+FFFD`, fences сбалансированы; ссылки в `README.md` и `07_cheatsheets/README.md` рабочие.
- Глобальный link-check даёт ложные срабатывания в `analysis/*` из-за путей, относительных к репозиториям задач.


#### [compaction] msg_16e0721b9001FfCYnPxDyKZ9tv
## Objective
- Подготовить команду из 4 человек от ОКТС (СПО) к X Кубку CTF России 2026: пройти отбор, выиграть СПО-зачёт 04.12 и получить 250 000 ₽.
- Сейчас максимальный фокус — на отборочных задачах: от детального разбора лёгких до реалистичных сложных задач уровня СПО.

## Requirements
- Приоритет — отбор; затем победа в СПО Attack-Defense 04.12.
- Нужен прогресс от простых задач к сложным, а не хаотичный список.
- Ответы и документация — на русском.
- Команда: 4 человека, ОКТС.

## Decisions
- Зачёт — СПО, не академический: академический требует 5–7 студентов одного вуза.
- Цель отбора: 3500–4000+ очков, 10–14 задач; ориентир общего топ-10 2025 — 3810.
- Для СПО финал — только AD 04.12; multi-machine pentest 06.12 не готовить.
- Пропускать kernel pwn, тяжёлую крипту и задачи с низким шансом решения.
- Приз: только 1-е место в СПО; 250 000 ₽ gross → 217 500 ₽ net → 54 375 ₽ на человека при составе 4.
- Создан отдельный документ по отборочному фокусу СПО: `13_spo_qualifier_focus.md`.

## Work State

### Completed
- Изучены `ctfcup.ru`, официальное положение 2026 и репозитории `acisoru` 2020–2025.
- Созданы `ctf-prep/README.md`, документы `00`–`12`, `07_cheatsheets/`, `templates/`, `analysis/`.
- Обновлены официальные окна финала: 04.12 `09:00–19:30` (игра `10:00–19:00`), 05.12 `09:00–19:30` (игра `10:00–18:00`), 06.12 `09:00–20:00` (игра `10:00–19:00`, награждение `19:00–20:00`).
- Во все ключевые документы добавлено предупреждение о расхождении Timepad.
- Добавлен `ctf-prep/templates/email_orgcommittee.md`.
- В `01_regulations_2026.md` добавлены расчёт для 4 человек и явное условие «250 000 ₽ только за 1-е место».
- В `00_urgent_checklist.md` добавлено правило «колледж + 4 человека = только СПО».
- Проверены UTF-8, BOM, `U+FFFD`, блоки кода и ссылки в основных документах.
- Создан `ctf-prep/13_spo_qualifier_focus.md` (~59 КБ, 1026 строк): tier-прогрессия T0–T4, 30+ карточек задач, роли на 4 человека, график 24–31.10, mock-контесты, score-стратегия, skip-list, чек-листы готовности и матрица навыков.
- В `README.md` добавлены СПО-баннер, строка `13_spo_qualifier_focus.md` в карте документов и обновлён режим «осталось 2 дня».
- В `04_seven_day_plan.md` добавлен баннер: для СПО основной документ — `13_spo_qualifier_focus.md`.
- В `11_training_targets.md` добавлен аналогичный СПО-баннер.
- Новый документ проверен: UTF-8 без BOM, без `U+FFFD`, 4 code fence (2 блока) сбалансированы.
- Выявлена фактическая ошибка: `babystack` (2022) — kernel ROP с ликом KASLR и `commit_creds(prepare_kernel_cred(0))`, а не простой stack overflow; в `11_training_targets.md` ещё не исправлено.
- Выявлен лишний code fence в `analysis/2025_tasks.md` около строки 3079 перед `### solve\exploit.py`; чётность fences — 119, ещё не исправлено.

### Active
- Завершается QA-проход: исправить `babystack` и `zion-revenge` в `11_training_targets.md`, убрать лишний fence в `analysis/2025_tasks.md`, перепроверить ссылки и кодировки.
- Готовится сжатый ответ пользователю: что решать сегодня, что завтра, что после 25.10.

### Blocked
- Нет письменного подтверждения оргкомитета по датам финала: Timepad показывает `5–7 декабря`, официальное положение — `04–06.12`; для СПО официально `04.12`.
- Академическая страница Timepad показывает старт `31.10 23:00`; страница СПО — корректные `12:00–12:00`.
- Регистрация закрывается `25.10.2026 12:00 МСК`; на 24.10 18:19 оставалось около 20 часов.

## Next Move
1. В `11_training_targets.md` исправить строку `babystack`: `kernel ROP (KASLR leak + commit_creds)`, время `240 мин`, приоритет `P3`.
2. В `11_training_targets.md` понизить `zion-revenge` до `P3` и указать `120–180 мин` (Go core dump + TLS 1.3).
3. В `analysis/2025_tasks.md` удалить лишний fence перед `### solve\exploit.py` и перепроверить чётность.
4. Проверить ссылки в `README.md` и `13_spo_qualifier_focus.md`, UTF-8/BOM/`U+FFFD` в изменённых файлах.
5. Выдать пользователю сжатый план: сегодня, завтра до 12:00, 26–30.10 и 31.10.

## Relevant Files
- `ctf-prep/13_spo_qualifier_focus.md`: главный новый документ СПО-фокуса; tier-прогрессия, карточки, роли, график, mock, score-стратегия.
- `ctf-prep/README.md`: главный хаб; добавлены СПО-баннер и ссылка на 13.
- `ctf-prep/04_seven_day_plan.md`: общий план 24–31.10; добавлен баннер о приоритете 13.
- `ctf-prep/11_training_targets.md`: меню задач; добавлен баннер, ещё нужны правки `babystack`/`zion-revenge`.
- `ctf-prep/analysis/2025_tasks.md`: сырой разбор 2025; остался лишний fence около строки 3079.
- `ctf-prep/analysis/2025_summary.md`: сводка техник и цепочек 2025.
- `ctf-prep/analysis/repo_inventory.md`: таблица баллов и числа решений 2025.
- `ctf-prep/repos/ctfcup2025-quals/tasks`: исходники и writeup задач 2025.
- `ctf-prep/repos/ctfcup2023-quals/tasks`: задачи 2023 для среднего уровня.
- `ctf-prep/repos/ctfcup22-quals/tasks`: задачи 2022 для среднего уровня.
- `ctf-prep/03_qualifier_playbook.md`: 24-часовой таймлайн и правила отбора.
- `ctf-prep/00_urgent_checklist.md`: регистрация, дедлайн, СПО-зачёт.
- `ctf-prep/01_regulations_2026.md`: даты, приз, условие 1-го места, расчёт на 4.
- `ctf-prep/05_final_attack_defense.md`: AD-финал 04.12; использовать после отбора.
- `ctf-prep/07_cheatsheets/ad.md`: таймлайн и AD-playbook.

## Important Context
- Отбор: `31.10.2026 12:00 — 01.11.2026 12:00 МСК`, 24 часа, jeopardy.
- СПО-финал: `04.12.2026`, день `09:00–19:30`, игра `10:00–19:00`, Москва.
- Регистрация до `25.10.2026 12:00 МСК`; локально Омск UTC+6 — до `15:00`.
- Ссылка СПО: `https://aciso.timepad.ru/event/4167329/`; академический: `4167286`; смешанный: `4167370`; школьный: `4167419`.
- Все 4 участника должны быть из одной организации СПО; возраст на странице — до 27, в положении — не более 28 на дату финала.
- Приз: 1 000 000 ₽ на 4 зачёта; 250 000 ₽ только победителю зачёта; НДФЛ 13%; капитан получает на счёт.
- 4 человека: 54 375 ₽ каждому; 5: 43 500 ₽; 3: 72 500 ₽.
- 2025: 24 задачи, суммарно ~9704 финальных балла, общий топ-10 заканчивался на ~3810, первое место — 7707.
- Траектории: база `8 beginners + 6×100 + Funeral + cursed + annabelle + trustmebroker = 3810`; + Wincrack или brokilon — `4729–4793`; + оба — `5712`; + bad_parser — `6709`.
- Приоритет отбора: 8 beginners; web `goose`, `goose-revenge`, `trustmebroker`; crypto `miracle`, `stolen_blueprints`, `important_task`; forensics `Funeral`, `zion`, `gamer`; reverse `annabelle`, `Wincrack`; pwn `safelang`, `safelang-revenge`, `babystack`; misc `checkpoint`, `slons`, `gamer`.
- Пропускать на первом проходе: `play_with_ker`, `watcher`, `dinosaurs`, `nanomachines`, `BimboIncident`, `zion-revenge`, `babystack` (kernel ROP).
- AD 2025 для тренировки: `veladora` (IDOR/payment ID/диалог), `archive` (boost serialization CVE-2023-34399), `warehouse` (UUIDv1/SSRF), `prototype` (MinIO CVE-2025-62506/HMAC).
- На AD с 4 людьми: 1 сервис = 1 владелец, капитан координирует SLA и флаги, обязательна автоматизация и 2–3 mock-сессии.
- Глобальный link-check даёт ложные срабатывания в `analysis/*` из-за путей, относительных к репозиториям задач.

**A** (msg_16e0cea380): Готово. Ниже — итог QA и сжатый план до старта отбора.

## Что исправлено в пакете

| Файл | Правка |
|---|---|
| `11_training_targets.md` | `babystack` (2022) переописан как kernel ROP: лик KASLR + `commit_creds(prepare_kernel_cred(0))`, 240 мин, P3 (было «stack overflow, 45 мин, P0») |
| `11_training_targets.md` | `zion-revenge` понижен до P3, 120–180 мин, уточнено: Go core dump + TLS 1.3 через `delve` |
| `13_spo_qualifier_focus.md` | `murdata` перенесён из `web/` в `crypto/` (и в Mock A) — это крипто-задача про Murmur3 + HLE |
| `analysis/2025_tasks.md` | Исправлена вложенность code fence: внешние блоки «дамп файла» переведены на 4 бэктика, добавлены 3 пропущенных закрывающих fence в секциях safelang. Теперь чётность и вложенность корректны |
| `README.md`, `04_seven_day_plan.md`, `11_training_targets.md` | Добавлены СПО-баннеры и ссылки на `13_spo_qualifier_focus.md` |

Проверено: UTF-8 без BOM, без `U+FFFD`, все локальные ссылки на документы и все `repos/...`-пути существуют (кроме `ctfcup2025-superfinals/machines/*` — репозиторий не чекаутится на Windows, это уже описано в документе).

## План: сегодня, 24.10

| Время | Действие |
|---|---|
| Сейчас | **Регистрация на Timepad** (`aciso.timepad.ru/event/4167329/`), зачёт СПО, 4 человека. Дедлайн — 25.10 12:00 МСК = **15:00 по Омску** |
| +30 мин | Скриншот заявки, письмо оргкомитету по шаблону `templates/email_orgcommittee.md` (расхождение дат Timepad/положение) |
| 2 часа | Созвон: роли (A web, B pwn/reverse, C crypto/forensics, D forensics/misc), каналы `#flags` / `#help`, таблица задач |
| 2–3 часа | Окружение: WSL/Kali, pwntools, gdb, Burp, Ghidra, Wireshark, binwalk, Docker, Sage |
| Вечер | `babyweb` + `babypwn` + `babycrypto` + `babyfor` — 4 флага и первые writeup'ы |

## Завтра, 25.10 — до 12:00 МСК

1. **Регистрация, если ещё не подана** — это задача №1.
2. Добить оставшиеся beginners: `babyrev`, `babymisc`, `babyppc`, `babyosint` → критерий 8/8 без подсказок, каждая ≤ 20 мин.
3. После 12:00: `goose` (NoSQLi через подделанную Flask-сессию) + разбор `solve.py`.
4. Вечер: `safelang` только до примитива (lifetime → heap leak), `miracle` (meet-in-the-middle).
5. Заполнить матрицу навыков в разделе 13.

## 26–30.10 (будни 3–4 часа)

| День | Фокус |
|---|---|
| 26.10 | `goose-revenge`, `trustmebroker` (шаги 1–2), `cursed` в Sage |
| 27.10 | `safelang-revenge` ×2, `annabelle` (дамп стадий) |
| 28.10 | `Funeral` (firmware → ext4 → AES), `zion`, `gamer` (misc), `slons` |
| 29.10 | Две T3 на выбор: `trustmebroker` / `Wincrack` / `brokilon` / `bad_parser` |
| 30.10 | Mock 4 часа, разбор, сборы, **сон до 01:00**. Новые инструменты не ставить |

## 31.10 — отбор

- 11:00 все онлайн, 11:30 роли зафиксированы, 12:00 старт.
- Первые 90 минут — «косилка»: beginners + все 100-балльные, цель 8–12 флагов.
- 3–12 ч — T2: `Funeral`, `zion`, `gamer`, `cursed`.
- 12–24 ч — максимум две T3 с владельцем и таймбоксом 2–3 часа.
- Цель: **4000+, 10–14 задач** (топ-10 2025 — ≈3810).

**Главное правило:** 100 баллов за 15 минут почти всегда лучше 900 за 4 часа с шансом 20%. Флаг сдан — задача закрыта.

Читать сейчас: `ctf-prep/13_spo_qualifier_focus.md` (разделы 3–5, 8–9) и `ctf-prep/00_urgent_checklist.md`.


#### [idle] msg_16e0d2315001S1SPA69ROjBmAs
{"id": "msg_16e0d2315001S1SPA69ROjBmAs", "time": {"created": 1792847717141}, "type": "idle", "outcome": "succeeded"}
