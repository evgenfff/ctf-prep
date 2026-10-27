# 02. Анализ задач Кубка CTF России 2020–2025

Цель этого файла — не пересказать writeup'ы, а ответить на три вопроса:
1. **Что организаторы спрашивают из года в год?**
2. **Какие техники дают очки быстрее всего?**
3. **Что тренировать в оставшиеся дни, а что осознанно пропустить?**

Источники: публичные репозитории `github.com/acisoru` (`ctfcup2025-quals`, `ctfcup2025-ad`, `ctfcup2025-superfinals`, `ctfcup2023-quals`, `ctfcup22-quals`, `ctfcup-21-quals`, `ctfcup-2020-quals`), а также разборы в `analysis/`.

---

## 1. Сводка по годам

| Год | Задач в отборе | Категории | Что определяло год |
|---|---:|---|---|
| 2020 | 25 | web, pwn, crypto, reverse, forensics, misc | Классический jeopardy, много «школьных» техник |
| 2021 | 30 | web, pwn, crypto, reverse, forensics, osint, misc | SSRF, PHP, PDF, JSON-конфиги; heap и kernel pwn; padding oracle, ECC |
| 2022 | 23 | crypto, web, pwn, reverse, forensics, warmup | Bleichenbacher, CRC-preimage, timing; SSRF→Redis→Celery; kernel ROP |
| 2023 | 21 + 3 PT | crypto, web, pwn, reverse, forensics, misc, ppc + LDAP/NFS/stealer | DH на группе симметрий, HLE, prototype pollution, 2free, Bun/JS, Android |
| 2025 | 24 | beginners, web, pwn, crypto, reverse, forensics | Rust lifetime (cve-rs), kernel heap OOB, Windows anti-debug, fileless malware, SSRF через PDF |

**Тренд:** от «широкого набора классики» к **глубоким, многоступенчатым задачам** и **отдельной линейке beginners**. В 2025 появились серии `safelang` и `goose`, то есть организаторы сознательно дают несколько задач на одну технику с ростом сложности. Это выгодно команде: одна освоенная техника приносит 2–3 флага.

---

## 2. Частота категорий и стоимость

| Категория | 2020 | 2021 | 2022 | 2023 | 2025 | Вывод |
|---|---:|---:|---:|---:|---:|---|
| Web | 5 | 6 | 4 | 4 | 3 | Стабильно 3–6 задач, часто самые дешёвые и самые дорогие одновременно |
| Pwn | 4 | 5 | 4 | 3 | 5 | Ядро сложности; в 2025 — 5 задач (3 safelang + kernel + userspace) |
| Crypto | 5 | 5 | 5 | 3 | 2 | Мало задач, но дорогие; математика решает |
| Reverse | 4 | 4 | 4 | 4 | 3 | Стабильно 3–4; Windows/anti-debug и VM |
| Forensics | 4 | 4 | 4 | 3 | 3 | Стабильно 3–4; память, реестр, прошивки, pcap |
| Misc/PPC/OSINT | 3 | 6 | 3 | 4 | 3 | Дешёвые очки, часто недооценивают |

**Практический вывод:** нельзя быть командой «только web» или «только pwn». Для топ-10 нужны минимум **4 сильные категории** и закрытие beginners.

---

## 3. Матрица повторяющихся техник

| Техника | Годы | Примеры задач | Вероятность в 2026 | Приоритет |
|---|---|---|---|---|
| IDOR / broken access control | 2021–2025 | babyweb, veladora, warehouse | Очень высокая | P0 |
| SSRF (в т.ч. через PDF/headless) | 2021, 2022, 2023, 2025 | trustmebroker, scanner, legacy | Очень высокая | P0 |
| NoSQL injection | 2025 | goose, goose-revenge | Высокая | P0 |
| SQLi + WAF bypass | 2022, 2023 | waf, simple | Высокая | P1 |
| Prototype pollution | 2022, 2023 | mistakes, warmup | Средняя | P1 |
| LFI / path traversal | 2021, 2025 | machine-3, murdata | Высокая | P0 |
| Deserialization | 2021–2023, 2025 | archive (boost), prototype (MinIO) | Высокая | P1 |
| JWT/OAuth/сессии | 2021–2025 | veladora, babyweb | Высокая | P1 |
| ret2libc / ROP | 2020–2023, 2025 | babypwn, safelang | Очень высокая | P0 |
| Heap: tcache/2free/UAF | 2021–2023, 2025 | more_heap, bad_parser | Высокая | P1 |
| Kernel OOB / modprobe_path | 2021, 2022, 2025 | play_with_ker, watcher | Средняя | P2 |
| Rust lifetime / safe-language abuse | 2025 | safelang ×3 | Средняя (мода) | P1 |
| Windows anti-debug / TLS callback | 2025 | Wincrack, machine-2 | Высокая | P1 |
| Self-modifying / VM / nanomites | 2022, 2023, 2025 | annabelle, nanomachines, time_capsule | Высокая | P1 |
| RSA-атаки (Bleichenbacher, Hastad, Wiener) | 2021–2023 | good_pad_bad_pad | Высокая | P0 |
| LLL / subset sum / knapsack | 2025 | cursed, miracle | Средняя | P1 |
| p-адики / матричный DLP | 2025 | cursed | Низкая | P2 |
| MT19937 / LCG / seed brute | 2020–2025 | babycrypto | Высокая | P0 |
| Padding oracle / CBC bit flip | 2021, 2022 | good_pad_bad_pad | Средняя | P1 |
| ECC (invalid curve, small subgroup) | 2021, 2025 | nanomachines | Средняя | P1 |
| Pcap + вложенные архивы | 2020–2025 | babyfor, Funeral | Очень высокая | P0 |
| Windows memory forensics | 2022, 2023, 2025 | BimboIncident, zion | Высокая | P0 |
| Registry / fileless malware | 2025 | brokilon | Средняя | P1 |
| Firmware / IoT | 2022, 2025 | Funeral, Red_firmware_I | Средняя | P1 |
| Linux privesc (SUID/capabilities) | 2021–2025 | machine-1/3/4 | Очень высокая | P0 |
| Windows privesc (TOCTOU/UAF/driver) | 2025 | machine-2 | Средняя | P2 |
| OSINT | 2021, 2025 | babyosint, machine-4 | Высокая | P1 |
| PPC/автоматизация nc | 2020–2025 | babyppc, checkpoint, slons | Очень высокая | P0 |

---

## 4. Отбор 2025: полная таблица

Очки — ориентир по опубликованному скорборду/динамике; к концу контеста значения меняются.

| # | Задача | Категория | Очки | Техника | Оценка времени | Приоритет |
|---:|---|---|---:|---|---:|---|
| 1 | babycrypto | crypto | 100 | кастомный алгоритм + brute seed 100k | 20 мин | P0 |
| 2 | babyfor | forensics | 100 | pcap → битый ZIP → PPTX → скрытая картинка | 30 мин | P0 |
| 3 | babymisc | misc | 100 | integer overflow | 15 мин | P0 |
| 4 | babyosint | osint | 100 | поиск по AADHAAR, Google/Yandex | 10 мин | P0 |
| 5 | babyppc | ppc | 100 | автоматизация nc | 20 мин | P0 |
| 6 | babypwn | pwn | 100 | перезапись младшего байта адреса возврата на `win` | 25 мин | P0 |
| 7 | babyrev | reverse | 100 | IDA, дамп таблицы, XOR 0x42 | 30 мин | P0 |
| 8 | babyweb | web | 100 | доверие `X-Forwarded-For` + закомментированный код | 15 мин | P0 |
| 9 | safelang | pwn | 100 | Rust lifetime extension (cve-rs) | 90 мин | P1 |
| 10 | safelang-revenge | pwn | 100 | та же техника, другой рантайм | 60 мин | P1 |
| 11 | safelang-revenge-revenge | pwn | 100 | та же техника, третий вариант | 45 мин | P1 |
| 12 | goose | web | 100 | NoSQLi `$regex` + слепая экстракция | 60 мин | P1 |
| 13 | goose-revenge | web | 100 | NoSQLi, обход фильтра | 45 мин | P1 |
| 14 | miracle | crypto | 100 | рюкзачная криптосистема, meet-in-the-middle | 90 мин | P1 |
| 15 | Funeral | forensics | 239 | firmware, binwalk, ext4, cron, AES-ECB, UDP | 90 мин | P1 |
| 16 | cursed | crypto | 395 | p-адики, матричный DLP, LLL/BKZ | 180 мин | P2 |
| 17 | annabelle | reverse | 793 | self-modifying code, ARC4, обратный проход | 120 мин | P1 |
| 18 | Wincrack | reverse | 919 | TLS callback, антидебаг, PEB seed, кастомное шифрование | 150 мин | P2 |
| 19 | bad_parser | pwn | 997 | TOCTOU → mmap OOB → libc leak → TLS/printf | 240 мин | P2 |
| 20 | play_with_ker | pwn | 995 | kernel heap OOB → file spray → KASLR leak → `modprobe_path` | 300 мин | P3 |
| 21 | trustmebroker | web | 983 | SSRF через headless PDF + обход HTML-фильтра | 120 мин | P1 |
| 22 | BimboIncident | forensics | 1000 | память + руткит + инжект + шифровальщик | 180 мин | P2 |
| 23 | brokilon | forensics | 983 | реестр, fileless malware, расшифровка конфига | 150 мин | P2 |
| 24 | nanomachines | reverse | — | ECC + наномиты + отладка форка | 180 мин | P2 |

### Что это значит для стратегии

- **8 beginners + 3 safelang + 2 goose = 1300 очков** при относительно низком пороге входа. Это база, которую обязана взять любая команда, претендующая на топ-10.
- **Funeral + trustmebroker + annabelle = 2015 очков** — три задачи средней сложности, которые реально решить за 5–6 часов команде из 5 человек. Вместе с базой — **3315**.
- **Одна задача из «тяжёлых»** (cursed, Wincrack, BimboIncident, brokilon, bad_parser) добавляет 400–1000 и выводит на **3700–4300**, то есть в зону прохода.
- **Две тяжёлые** — уверенный топ-10 и заявка на топ-3.

---

## 5. Отбор 2023: 21 задача + 3 PT

| Задача | Категория | Техника | Чему учит |
|---|---|---|---|
| geometry | crypto | DH над группой симметрий 1337-угольника, brute | не бояться экзотических групп |
| lateralus | crypto | Fibonacci mod p², дискретный лог, трюк Пайе | p-адики и модульная арифметика |
| murdata | crypto/web | Murmur3 preimage + Hash Length Extension + path traversal | хеши и «магия» пустой строки |
| gamer | forensics | RAM dump, MPEG-TS из `firefox.exe` | память + медиа |
| zion | forensics | `strings` по core dump | базовый форензик |
| zion-revenge | forensics | TLS key из дампа → расшифровка pcap | память + сеть |
| gamer (misc) | misc | восстановление доски Minesweeper из XML | внимательность |
| checkpoint | ppc | интерактивная автоматизация | скорость написания скриптов |
| floating_in_delirium | ppc | эмуляция XOR 42 только арифметикой | нестандартные ограничения |
| slons | ppc | brute force | простой перебор |
| Mystery_ldap | pt | LDAP | AD-разведка |
| NFS | pt | NFS | сетевые шары |
| stealer | pt | stealer-артефакты | malware forensics |
| more_heap | pwn | 2free → arbitrary write → GOT/`_IO_2_1_stdout_` | heap |
| some_storage | pwn | overflow → vtable → shellcode | C++ объекты |
| spy | pwn | arbitrary write в GOT и `_fini_array` | современные митигации |
| 2fac | reverse | Android-приложение, алгоритм 2FA | мобильный реверс |
| magick_lock | reverse | полиномиальные остатки, GCD | математика в реверсе |
| monitoring | reverse | Bun/JS, деобфускация, обход sandbox | JS-рантаймы |
| time_capsule | reverse | кастомная VM, модифицированный MD5 | VM-реверс |
| mistakes | web | prototype pollution через `window.name` | клиентская логика |
| novosti | web | XSS + CSP bypass через iframe без CSP | CSP |
| scanner | web | SSRF + CRLF → Redis → Celery RCE | цепочки |
| waf | web | дублирующийся `Content-Type` → SQLi → RCE | парсеры и WAF |

**Вывод:** 2023 — «энциклопедия». Если у команды есть время только на один год для тренировки, берите 2023: он покрывает максимум техник.

---

## 6. Отбор 2022: 23 задачи

| Задача | Категория | Техника |
|---|---|---|
| dinosaurs | crypto | корреляционная атака на фильтрующий генератор |
| good_pad_bad_pad | crypto | Bleichenbacher / PKCS#1 v1.5 |
| important_task | crypto | восстановление прообраза CRC |
| stolen_blueprints | crypto | шифр Тритемиуса (self-XOR) по известному заголовку JPEG |
| the_time_has_come | crypto | timing-атака на возведение в степень |
| Red_firmware_I | forensics | UEFI/AMD PSP, модуль `$FTD` |
| fallen_angel | forensics | E01-образ дрона, геолокация |
| french_connection | forensics | сеть/артефакты (см. writeup) |
| malware_autopsy | forensics | анализ malware |
| babystack | pwn | классический stack overflow |
| ozne | pwn | heap |
| shellyha | pwn | shellcode |
| watcher | pwn | kernel ROP |
| bebrus | reverse | нестандартный бинарь |
| crackme2077 | reverse | crackme |
| simple_encoder | reverse | кодировщик |
| unicorn_plc | reverse | PLC/промышленный протокол |
| classic_matreshka | warmup | матрёшка |
| math_pong | warmup | математика |
| legacy | web | SSRF/цепочка |
| onlytweets | web | CSP/XSS |
| simple | web | SQLi/WAF |
| warmup | web | prototype pollution |

**Вывод:** 2022 даёт лучшую базу по crypto (5 разных атак) и forensics (образы, прошивка, память).

---

## 7. 2020–2021: что оттуда до сих пор актуально

Точные названия задач менее важны, чем набор техник:

- **Web:** SSRF, PHP include/wrappers, PDF-генераторы, JSON-конфиги, SQLi, XSS, обход фильтров.
- **Pwn:** ret2libc, heap (tcache/fastbin), kernel module OOB, format string.
- **Crypto:** padding oracle, ECC, RSA с малой экспонентой, MT19937.
- **Forensics:** pcap, память, файловые системы, стеганография.
- **OSINT:** геолокация, соцсети, метаданные.

Этот набор — «гигиена». Если он не закрыт, новые задачи 2025–2026 всё равно не решатся.

---

## 8. Десять закономерностей Кубка

1. **Beginners — это не разминка, а 1/3 очков.** В 2025 восемь задач по 100 = 800 очков, почти 21% от cutoff. Их пропуск — гарантированный вылет.
2. **Организаторы любят серии.** `safelang` ×3, `goose` ×2, `zion` ×2. Решил одну — решай остальные, пока техника в голове.
3. **Revenge-задачи меняют один барьер, а не всю задачу.** Не начинайте с нуля: берите прошлый эксплойт и меняйте обход.
4. **Сложность часто в обвязке, а не в идее.** TOCTOU, гонки, парсеры, нестандартные протоколы.
5. **Windows становится важнее.** Wincrack, BimboIncident, machine-2: TLS callbacks, драйверы, дампы, PTH.
6. **Реальные CVE в AD.** archive — CVE-2023-34399, prototype — CVE-2025-62506. Нужно уметь быстро гуглить и адаптировать PoC.
7. **Исходники и деплой почти всегда в репозитории.** Локальный запуск экономит часы.
8. **Флаги авторов лежат в репозиториях.** Для тренировки это нормально; на контесте флаги другие.
9. **Unintended solutions бывают.** Если задача кажется слишком простой — возможно, вы нашли unintended, и это нормально.
10. **Инфраструктура решает.** Падение сервиса, потеря флага, неверный формат — самые обидные потери.

---

## 9. Прогноз на 2026

На основе 2025 и общего тренда:

### Почти наверняка
- 6–8 beginners-задач (web, pwn, crypto, reverse, forensics, misc).
- 1–2 web-задачи на авторизацию/IDOR и 1 на SSRF.
- 1 pwn на ret2libc/ROP и 1 на heap.
- 1–2 crypto на RSA/LLL/PRNG.
- 1–2 forensics на pcap/память.
- 1 reverse с антидебагом или VM.
- 1–2 misc/PPC на автоматизацию.

### Вероятно
- NoSQLi или другая инъекция в не-SQL хранилище.
- Rust/Go unsafe/lifetime.
- Задача на supply chain / зависимость с CVE.
- Windows-артефакты (реестр, дамп, драйвер).
- LLM-обвязка (prompt injection, агент с инструментами) — тренд 2025–2026.
- Задача на контейнеры/k3s.

### Маловероятно, но возможно
- Полноценный kernel pwn (был в 2025, могут повторить).
- Аппаратная криптография/побочные каналы.
- Мобильный реверс (был в 2023).

---

## 10. Лестница сложности: что решать в первую очередь

### Уровень 0 — «не потерять очки» (20–30 минут каждая)
`babycrypto`, `babyfor`, `babymisc`, `babyosint`, `babyppc`, `babypwn`, `babyrev`, `babyweb`.
Цель: 8/8 за первые 90 минут.

### Уровень 1 — «проход в топ-10» (45–120 минут)
`safelang` ×3, `goose` ×2, `miracle`, `Funeral`, `annabelle`, `trustmebroker`.
Цель: 9/9 или максимум, что успеваете.

### Уровень 2 — «топ-3» (2–5 часов)
`cursed`, `Wincrack`, `brokilon`, `BimboIncident`, `bad_parser`, `nanomachines`.
Цель: 2–3 задачи.

### Уровень 3 — «победа» (4–6 часов, часто не берётся вообще)
`play_with_ker`, самые злые revenge-версии.
Цель: не начинать, пока не закрыты уровни 0–2.

---

## 11. Что тренировать: приоритеты по времени

Если у вас **10 часов** до отбора:
1. Beginners 2025 — 4 часа.
2. Web: goose + trustmebroker — 3 часа.
3. Pwn: babypwn + safelang — 2 часа.
4. Регламент и логистика — 1 час.

Если **30 часов**:
1. Beginners — 5 часов.
2. Web (goose ×2, trustmebroker, babyweb, mistakes) — 7 часов.
3. Pwn (babypwn, safelang ×3, more_heap) — 8 часов.
4. Crypto (babycrypto, miracle, good_pad_bad_pad) — 4 часа.
5. Forensics (babyfor, Funeral, zion) — 4 часа.
6. Mock-контест — 2 часа.

Если **неделя** — идите по `04_seven_day_plan.md`, но каждый день заканчивайте writeup'ом.

---

## 12. Главные выводы

1. **База важнее героизма.** 8 beginners + 5 средних задач дают проход. Погоня за одним kernel pwn вместо этого — путь вниз.
2. **Одна техника — несколько флагов.** Серии задач надо добивать.
3. **Исходники — ваше преимущество.** Локальный деплой и чтение кода экономят больше времени, чем любой эксплойт-шаблон.
4. **Динамика очков наказывает медлительность.** Лёгкие задачи надо брать в первые 3 часа.
5. **Финал — это другая игра.** После отбора переключайтесь на AD и multi-machine, а не продолжайте решать jeopardy.
