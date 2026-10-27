# 11. Тренировочные цели: что решать и в каком порядке

Этот файл — «меню» задач из публичных репозиториев. Не пытайтесь решить всё. Выберите по 2–3 на навык и доведите до понимания.

**Пути указаны от `ctf-prep/repos/`.**

---

## 1. Отбор 2025: beginners (обязательно всем)

| Задача | Путь | Навык | Время | Цель |
|---|---|---|---:|---|
| babyweb | `ctfcup2025-quals/tasks/beginners/babyweb` | HTTP-заголовки, исходники | 15 мин | понять, как доверять `X-Forwarded-For` опасно |
| babypwn | `.../beginners/babypwn` | ret2win | 25 мин | переписать младший байт возврата |
| babycrypto | `.../beginners/babycrypto` | brute seed | 20 мин | обратить кастомный алгоритм |
| babyrev | `.../beginners/babyrev` | IDA, XOR | 30 мин | найти таблицу и декодировать |
| babyfor | `.../beginners/babyfor` | pcap → ZIP → PPTX | 30 мин | собрать «матрёшку» |
| babymisc | `.../beginners/babymisc` | integer overflow | 15 мин | обойти проверку |
| babyppc | `.../beginners/babyppc` | автоматизация | 20 мин | написать скрипт |
| babyosint | `.../beginners/babyosint` | OSINT | 10 мин | найти человека по данным |

**Критерий готовности:** решаете все 8 без writeup'а за 90 минут.

---

## 2. Web

| Задача | Путь | Техника | Время | Приоритет |
|---|---|---|---:|---|
| goose | `ctfcup2025-quals/tasks/web/goose` | NoSQLi `$regex`, blind | 60 мин | P0 |
| goose-revenge | `.../web/goose-revenge` | NoSQLi, обход фильтра | 45 мин | P0 |
| trustmebroker | `.../web/trustmebroker` | SSRF через headless PDF | 120 мин | P1 |
| mistakes (2023) | `ctfcup2023-quals/tasks/web/mistakes` | prototype pollution | 90 мин | P1 |
| novosti (2023) | `.../web/novosti` | XSS + CSP bypass | 60 мин | P1 |
| scanner (2023) | `.../web/scanner` | SSRF → Redis → Celery RCE | 120 мин | P2 |
| waf (2023) | `.../web/waf` | дублирующийся Content-Type | 90 мин | P1 |
| legacy (2022) | `ctfcup22-quals/tasks/web/legacy` | SSRF/цепочка | 90 мин | P2 |
| onlytweets (2022) | `.../web/onlytweets` | CSP/XSS | 60 мин | P2 |
| simple (2022) | `.../web/simple` | SQLi/WAF | 60 мин | P2 |
| warmup (2022) | `.../web/warmup` | prototype pollution | 45 мин | P1 |

**Что тренировать:** Burp Repeater, ffuf, анализ JS, чтение исходников, обход WAF, цепочки.

---

## 3. Pwn

| Задача | Путь | Техника | Время | Приоритет |
|---|---|---|---:|---|
| babypwn | `ctfcup2025-quals/tasks/beginners/babypwn` | ret2win | 25 мин | P0 |
| safelang | `.../pwn/safelang` | Rust lifetime (cve-rs) | 90 мин | P1 |
| safelang-revenge | `.../pwn/safelang-revenge` | та же техника | 60 мин | P1 |
| safelang-revenge-revenge | `.../pwn/safelang-revenge-revenge` | та же техника | 45 мин | P1 |
| bad_parser | `.../pwn/bad_parser` | TOCTOU, mmap OOB, TLS | 240 мин | P2 |
| play_with_ker | `.../pwn/play_with_ker` | kernel heap OOB | 300 мин | P3 |
| more_heap (2023) | `ctfcup2023-quals/tasks/pwn/more_heap` | 2free, arbitrary write | 180 мин | P1 |
| some_storage (2023) | `.../pwn/some_storage` | overflow, vtable, shellcode | 120 мин | P2 |
| spy (2023) | `.../pwn/spy` | GOT, `_fini_array` | 120 мин | P2 |
| babystack (2022) | `ctfcup22-quals/tasks/pwn/babystack` | stack overflow | 45 мин | P0 |
| shellyha (2022) | `.../pwn/shellyha` | shellcode | 60 мин | P1 |
| watcher (2022) | `.../pwn/watcher` | kernel ROP | 240 мин | P3 |

**Что тренировать:** checksec, offset, leak, ROP, heap, gdb, pwntools.

---

## 4. Crypto

| Задача | Путь | Техника | Время | Приоритет |
|---|---|---|---:|---|
| babycrypto | `ctfcup2025-quals/tasks/beginners/babycrypto` | brute seed | 20 мин | P0 |
| miracle | `.../crypto/miracle` | knapsack, meet-in-the-middle | 90 мин | P1 |
| cursed | `.../crypto/cursed` | p-адики, матричный DLP, LLL | 180 мин | P2 |
| geometry (2023) | `ctfcup2023-quals/tasks/crypto/geometry` | DH на группе симметрий | 60 мин | P1 |
| lateralus (2023) | `.../crypto/lateralus` | Fibonacci mod p² | 90 мин | P2 |
| murdata (2023) | `.../crypto/murdata` | Murmur3, HLE | 90 мин | P1 |
| dinosaurs (2022) | `ctfcup22-quals/tasks/crypto/dinosaurs` | корреляционная атака | 180 мин | P3 |
| good_pad_bad_pad (2022) | `.../crypto/good_pad_bad_pad` | Bleichenbacher | 120 мин | P1 |
| important_task (2022) | `.../crypto/important_task` | CRC preimage | 60 мин | P1 |
| stolen_blueprints (2022) | `.../crypto/stolen_blueprints` | Trithemius | 30 мин | P0 |
| the_time_has_come (2022) | `.../crypto/the_time_has_come` | timing attack | 120 мин | P2 |

**Что тренировать:** SageMath, LLL, RSA-атаки, PRNG, модульная арифметика.

---

## 5. Reverse

| Задача | Путь | Техника | Время | Приоритет |
|---|---|---|---:|---|
| babyrev | `ctfcup2025-quals/tasks/beginners/babyrev` | IDA, XOR | 30 мин | P0 |
| annabelle | `.../reverse/annabelle` | self-modifying, ARC4 | 120 мин | P1 |
| Wincrack | `.../reverse/Wincrack` | TLS callback, антидебаг | 150 мин | P2 |
| nanomachines | `.../reverse/nanomachines` | ECC, наномиты | 180 мин | P2 |
| 2fac (2023) | `ctfcup2023-quals/tasks/reverse/2fac` | Android | 90 мин | P2 |
| magick_lock (2023) | `.../reverse/magick_lock` | полиномы, GCD | 90 мин | P2 |
| monitoring (2023) | `.../reverse/monitoring` | Bun/JS, sandbox | 120 мин | P2 |
| time_capsule (2023) | `.../reverse/time_capsule` | кастомная VM | 150 мин | P2 |

**Что тренировать:** IDA/Ghidra, x64dbg, антидебаг, VM, скрипты IDAPython.

---

## 6. Forensics

| Задача | Путь | Техника | Время | Приоритет |
|---|---|---|---:|---|
| babyfor | `ctfcup2025-quals/tasks/beginners/babyfor` | pcap, ZIP, PPTX | 30 мин | P0 |
| Funeral | `.../forensic/Funeral` | firmware, ext4, AES | 90 мин | P1 |
| BimboIncident | `.../forensic/BimboIncident` | память, руткит, шифровальщик | 180 мин | P2 |
| brokilon | `.../forensic/brokilon` | реестр, fileless | 150 мин | P2 |
| gamer (2023) | `ctfcup2023-quals/tasks/forensic/gamer` | память, MPEG-TS | 90 мин | P1 |
| zion (2023) | `.../forensic/zion` | core dump | 30 мин | P0 |
| zion-revenge (2023) | `.../forensic/zion-revenge` | TLS key из дампа | 90 мин | P1 |
| Red_firmware_I (2022) | `ctfcup22-quals/tasks/forensics/Red_firmware_I` | UEFI/AMD PSP | 120 мин | P2 |
| fallen_angel (2022) | `.../forensics/fallen_angel` | E01, геолокация | 90 мин | P1 |

**Что тренировать:** Wireshark, Volatility, binwalk, registry, timelines.

---

## 7. Misc / PPC / OSINT

| Задача | Путь | Техника | Время |
|---|---|---|---:|
| babyppc | `ctfcup2025-quals/tasks/beginners/babyppc` | nc-автоматизация | 20 мин |
| babymisc | `.../beginners/babymisc` | overflow | 15 мин |
| babyosint | `.../beginners/babyosint` | OSINT | 10 мин |
| gamer (2023) | `ctfcup2023-quals/tasks/misc/gamer` | Minesweeper XML | 45 мин |
| checkpoint (2023) | `.../ppc/checkpoint` | автоматизация | 60 мин |
| floating_in_delirium (2023) | `.../ppc/floating_in_delirium` | арифметика без XOR | 60 мин |
| slons (2023) | `.../ppc/slons` | brute force | 30 мин |

---

## 8. AD 2025 (после отбора)

| Сервис | Путь | Что отработать |
|---|---|---|
| veladora | `ctfcup2025-ad/services/veladora` | IDOR, предсказуемый ID, инъекция в диалог |
| archive | `.../services/archive` | boost serialization, CVE-2023-34399 |
| warehouse | `.../services/warehouse` | UUIDv1, SSRF, микросервисы |
| prototype | `.../services/prototype` | MinIO CVE-2025-62506, подпись S3 |

**Задание:** поднять каждый сервис, пройти чек-лист аудита, написать эксплойт, накатить патч, прогнать checker.

---

## 9. Секретный финал 2025

| Машина | Путь | Цепочка |
|---|---|---|
| machine-1 | `ctfcup2025-superfinals/machines/machine-1` | Telegram webhook → Bot API `file://` → SSH → `vim cap_setuid` |
| machine-2 | `.../machine-2` | TOCTOU + UAF → драйвер → MEMORY.DMP → NT hash → PTH |
| machine-3 | `.../machine-3` | LFI → `sip.conf` → Asterisk → overflow → SUID → pickle |
| machine-4 | `.../machine-4` | crypto/PPC/OSINT → архив → Turing → `su flaguser` → SUID |

**Важно:** репозиторий может не чекаутиться на Windows из-за путей `C:\...`. Используйте `git show HEAD:<path>` или WSL.

---

## 10. Внешние тренировочные площадки

| Площадка | Что тренировать | Ссылка |
|---|---|---|
| PortSwigger Web Security Academy | web, SSRF, JWT, deserialization | portswigger.net/web-security |
| pwn.college | pwn, kernel, heap | pwn.college |
| picoCTF | beginners, все категории | picoctf.org |
| Cryptohack | crypto | cryptohack.org |
| OverTheWire | Linux, pwn | overthewire.org |
| Hack The Box | AD, pentest | hackthebox.com |
| TryHackMe | AD, Windows | tryhackme.com |
| Flare-On | reverse, malware | flare-on.com |
| Root-Me | все категории | root-me.org |
| CTFtime | архив задач и writeup'ов | ctftime.org |
| Malware Traffic Analysis | pcap, forensics | malware-traffic-analysis.net |
| Blue Team Labs Online | forensics, IR | blueteamlabs.online |

---

## 11. План после отбора: 4 недели до финала

Если прошли отбор, начинается другая подготовка. Отбор — это jeopardy, финал — AD и pentest.

### Неделя 1 (09–15.11): AD-фундамент
- Поднять `veladora` и `warehouse` локально.
- Пройти чек-лист аудита.
- Изучить checker и формат флагов.
- Тренировка: 2 вечера по 2 часа.

### Неделя 2 (16–22.11): AD-эксплуатация
- Эксплойт на IDOR Veladora.
- Эксплойт на SSRF Warehouse.
- Патчи для обоих.
- Mock AD 3 часа.

### Неделя 3 (23–29.11): Windows и multi-machine
- machine-2: TOCTOU/UAF/драйвер/дамп.
- machine-1 и machine-3: Linux-цепочки.
- Volatility, impacket, mimikatz.
- Mock pentest 4 часа.

### Неделя 4 (30.11–04.12): финальная репетиция
- Полный mock AD 6 часов.
- Полный mock pentest 6 часов.
- Разбор ошибок.
- Логистика Москвы.
- Сон и восстановление.
- 05.12 — AD-полуфинал (академический/смешанный), 06.12 — секретный финал 3.0.

---

## 12. Ежедневная рутина (90 минут)

Если нет времени на большие блоки:

1. **15 мин** — разминка на известной задаче.
2. **45 мин** — одна новая задача.
3. **20 мин** — разбор/подсказка.
4. **10 мин** — writeup.

Даже 90 минут в день в течение месяца дают больше, чем один 12-часовой марафон.

---

## 13. Как понять, что вы готовы

- [ ] Beginners 2025 — 8/8 без подсказок.
- [ ] Можете за 60 минут поднять задачу из репозитория и получить флаг.
- [ ] Знаете, где искать утечки/IDOR/SSRF в незнакомом веб-приложении.
- [ ] Можете собрать ROP-цепочку по шаблону.
- [ ] Понимаете LLL и можете запустить Sage.
- [ ] Разбираете pcap и дамп памяти по чек-листу.
- [ ] Можете провести Linux-привилегии по чек-листу.
- [ ] Знаете, как из Windows-дампа достать NT hash.
- [ ] Умеете писать эксплойт с потоками и таймаутами.
- [ ] Можете объяснить свой эксплойт другому человеку.
