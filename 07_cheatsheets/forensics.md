# Форензика — шпаргалка к X Кубку CTF России 2026

> Формат: артефакт → инструмент → команда. Все действия — на копии; оригинал не монтировать rw.
> Обозначения: `[B]` beginners, `[M]` medium, `[H]` hard.

## Когда открывать

| Видишь | Открывай раздел |
|---|---|
| `.E01`, `.dd`, `.raw`, `.vmdk`, `.vhd`, `.iso` | 1. Диск / образ |
| `.raw`, `.mem`, `.lime`, `MEMORY.DMP`, `hiberfil.sys` | 2. Память |
| `.pcap`, `.pcapng`, `tls`, `http2`, `usb` | 3. Сеть |
| `NTUSER.DAT`, `SAM`, `SYSTEM`, `SECURITY`, `NTDS.dit`, `.evtx` | 4. Windows |
| `auth.log`, `journal`, `cron`, `/proc`, `docker`, прошивка | 5. Linux |
| `.exe`, `.dll`, shellcode, `powershell -enc`, C2 | 6. Malware |
| PNG/JPEG/WAV/MP3/ZIP/PDF, «слишком большой файл» | 7. Стеганография |
| `.ab`, `.apk`, `.ipa`, `Manifest.db` | 8. Мобильные |
| «дамп памяти + трафик», «прошивка», «реестр» | 9. Разбор задач Кубка |

## 0. Триаж за 3 минуты

```bash
sha256sum *; file *; wc -c *
strings -n 8 -el file | head -100          # UTF-16LE для Windows
binwalk -Me file                            # сигнатуры и распаковка
exiftool -a -G1 file
```

1. Зафиксируй хэши и время (`stat`, `date -u`), чтобы не потерять таймлайн.
2. Определи тип: образ, дамп, pcap, реестр, бинарь, контейнер, прошивка.
3. Сразу ищи флаг/строки: `grep -a -i "ctfcup\|flag\|secret"`, `strings`.
4. Дальше иди по артефакту, а не по условию: условие часто врёт про «удалено».

## 1. Диск / образ

```bash
file disk.img; fdisk -l disk.img; mmls disk.img
ewfinfo image.E01
ewfmount image.E01 /mnt/ewf && ls /mnt/ewf        # появится ewf1
mmls /mnt/ewf/ewf1
fls -r -o 2048 /mnt/ewf/ewf1
icat -o 2048 /mnt/ewf/ewf1 1357829 > recovered.bin
```

Монтирование по offset (offset = start_sector × 512):

```bash
mount -o ro,loop,offset=$((2048*512)) disk.img /mnt/img
losetup -Pf --show disk.img                         # все разделы
qemu-nbd --connect=/dev/nbd0 disk.vmdk && mount /dev/nbd0p1 /mnt/vm
vmdkmount disk.vmdk /mnt/vmdk
guestmount -a disk.vmdk -i /mnt/vm                  # libguestfs
xmount --in ewf image.E01 --out vdi /mnt/x
```

SleuthKit:

```bash
mmls image.dd                 # таблица разделов
fls -r -p image.dd            # дерево файлов, включая удалённые
istat image.dd 12345          # метаданные inode/MFT
icat image.dd 12345 > file    # извлечь содержимое
tsk_recover -e image.dd out/  # все файлы
```

Восстановление:

```bash
testdisk image.dd             # разделы, загрузочные записи
photorec image.dd             # карвинг по сигнатурам
foremost -i image.dd -o out   # jpg, png, pdf, zip, doc
scalpel -c scalpel.conf image.dd -o out
bulk_extractor -o out image.dd
```

- E01 разбит на `.E01..E99` — `ewfmount` берёт первый, остальные подхватывает.
- VMDK: `qemu-img convert -f vmdk -O raw disk.vmdk disk.img`.
- VHD/VHDX: `qemu-img convert -f vhdx -O raw disk.vhdx disk.img`.
- ISO: `7z x`, `mount -o loop`, `isoinfo -R -f`.
- BitLocker: `dislocker`, ключ из памяти/реестра.
- Удалённые файлы: `fls -d`, `icat`, `tsk_recover`; в NTFS смотри `$MFT`, `$UsnJrnl`, `$LogFile`.

## 2. Память

Volatility 3:

```bash
vol -f mem.raw windows.info
vol -f mem.raw windows.pslist
vol -f mem.raw windows.psscan
vol -f mem.raw windows.pstree
vol -f mem.raw windows.cmdline
vol -f mem.raw windows.netscan
vol -f mem.raw windows.malfind
vol -f mem.raw windows.modules
vol -f mem.raw windows.dlllist --pid 1992
vol -f mem.raw windows.filescan
vol -f mem.raw windows.dumpfiles --physaddr 0x...
vol -f mem.raw windows.dumpfiles --pid 4440
vol -f mem.raw windows.memmap --pid 4440 --dump
vol -f mem.raw windows.vadinfo --pid 4440
vol -f mem.raw windows.handles --pid 4440
vol -f mem.raw windows.svcscan
vol -f mem.raw windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"
vol -f mem.raw windows.userassist
vol -f mem.raw windows.shimcaches
vol -f mem.raw windows.scheduled_tasks
vol -f mem.raw windows.hashdump
vol -f mem.raw windows.lsadump
vol -f mem.raw volshell
```

Символы: Vol3 сам скачивает Windows PDB; офлайн — `--symbols /path` или `--symbol-dirs`.
Linux-дамп:

```bash
vol -f mem.lime banners.Banners
vol -f mem.lime linux.pslist
vol -f mem.lime linux.pstree
vol -f mem.lime linux.bash
vol -f mem.lime linux.lsmod
vol -f mem.lime linux.sockstat
vol -f mem.lime linux.malfind
vol -f mem.lime linux.proc.Maps
vol -f mem.lime linux.pagecache.InodePages
```

Нужен ISF-символ-файл: `dwarf2json linux --elf vmlinux > linux.json`, затем `--symbol-dirs`.
Снятие дампа:

```bash
insmod lime.ko "path=/mnt/dump.lime format=lime"
avml /mnt/dump.raw
```

Windows crash dump:

```bash
vol -f MEMORY.DMP windows.info       # Vol3 умеет crash dump
```

`hiberfil.sys` — Volatility2 (`imagecopy`) или отдельные hibernation-плагины.

Дополнительно:

```bash
strings -n 8 -el mem.raw | grep -i "ctfcup\|flag"
bulk_extractor -o out mem.raw
memprocfs -device mem.raw -mount /mnt/mem
```

- `pslist` показывает активные процессы; `psscan` — в том числе скрытые/завершённые.
- Скрытый процесс ищи по `psscan`, `vadinfo`, `malfind`, `handles`; rootkit может занулить `ImageFileName` и выкинуть процесс из `ActiveProcessLinks`.
- `malfind` — RWX-страницы и инъекции; проверяй `MZ`/shellcode, но ложные срабатывания нормальны.
- `filescan` + `dumpfiles` — вытащить файл из кэша; `memmap` — дамп всего адресного пространства процесса.
- `hashdump`/`lsadump` — хэши и LSA-секреты; дальше hashcat.
- Пароли браузеров: ищи `Login Data`, `Local State`, `key4.db`, `logins.json` в дампе/образе.

## 3. Сеть

```bash
capinfos capture.pcapng
tshark -r capture.pcapng -q -z io,phs
tshark -r capture.pcapng -q -z endpoints,ip
tshark -r capture.pcapng -q -z conversations,tcp
tshark -r capture.pcapng -Y 'http.request' -T fields -e http.host -e http.request.uri
tshark -r capture.pcapng -Y 'dns' -T fields -e dns.qry.name
tshark -r capture.pcapng -Y 'smb2.filename' -T fields -e smb2.filename
tshark -r capture.pcapng -Y 'usbhid.data' -T fields -e usbhid.data
tshark -r capture.pcapng --export-objects http,out
```

Wireshark-фильтры:

```text
ip.addr == 10.0.0.5
tcp.stream eq 7
http.request || http.response
tls.handshake.type == 1
http2 || quic
dns.qry.name contains "exfil"
smb2 || smb || kerberos || ldap
usb.capdata || usbhid.data
frame contains "ctfcup"
```

TLS:

- `SSLKEYLOGFILE=keys.log` у клиента → Wireshark: Preferences → Protocols → TLS → `(Pre)-Master-Secret log filename`.
- TLS 1.3: нужен `trafficSecret`/keylog; в дампе ищи `CLIENT_RANDOM`, `SSLKEYLOGFILE`, `trafficSecret`.
- `tshark -r cap.pcapng -o tls.keylog_file:keys.log -Y http`.
- HTTP/2: Wireshark декодирует `http2`; при HPACK-ошибках смотри `http2.headers` и reassembly.
- QUIC: `quic` + keylog; иначе только метаданные.

DNS/SMB/USB:

```bash
tshark -r cap.pcapng -Y 'dns.flags.response == 0' -T fields -e dns.qry.name | sort -u
tshark -r cap.pcapng -Y 'smb2.cmd == 5' -T fields -e smb2.filename -e smb2.filesize
tshark -r cap.pcapng -Y 'usbhid.data' -T fields -e usbhid.data > hid.txt
```

- DNS-туннель: длинные поддомены, TXT, высокая энтропия, `-z dns,tree`.
- SMB: имена файлов, `smb2.filename`, `smb2.filesize`; вытаскивай через `NetworkMiner`/`smbclient`/reassembly.
- USB HID: 8 байт на событие; байт 0 — модификаторы, байты 2–7 — коды клавиш (нумерация с нуля). Декодируй таблицей HID→ASCII; мышь — относительные dx/dy.
- pcapng → pcap: `editcap -F pcap in.pcapng out.pcap`; объединить: `mergecap -w out.pcap a.pcap b.pcap`.
- VLAN/MPLS: `vlan`, `mpls`; checksum offload может ломать TCP — `-o tcp.check_checksum:FALSE`.
- Объекты: `--export-objects http,out`, `--export-objects smb,out`, `--export-objects tftp,out`.

## 4. Windows

Реестр:

```bash
regripper -r NTUSER.DAT -f all
regripper -r SYSTEM -f all
hivexsh NTUSER.DAT
regipy-dump NTUSER.DAT -o out
```

Кусты: `C:\Windows\System32\config\{SAM,SYSTEM,SECURITY,SOFTWARE,DEFAULT}`, `C:\Users\<user>\NTUSER.DAT`, `UsrClass.dat`.
Автозапуск: `Run`, `RunOnce`, `RunServices`, `Winlogon\Shell/Userinit`, `AppInit_DLLs`, `IFEO`, `Image File Execution Options`, `LSA Packages`, `Boot Execute`, `Startup` folder.

Учётки:

```bash
secretsdump.py -sam SAM -system SYSTEM -security SECURITY local
secretsdump.py -ntds ntds.dit -system SYSTEM LOCAL
hashcat -m 1000 hashes.txt rockyou.txt
```

`NTDS.dit` также: `esedbexport -t out ntds.dit`, затем таблицы `datatable`.

События:

```bash
evtx_dump.py Security.evtx > security.xml
chainsaw hunt evtx/ --sigma sigma/ --mapping mappings/sigma-event-logs-all.yml
hayabusa csv-timeline -d evtx/ -o timeline.csv
```

Ключевые Event ID: `4624` вход, `4625` неудача, `4672` admin, `4688` процесс, `4720` создан пользователь, `4698` задача, `7045` служба, `4104` script block, `1102` очистка лога, `5140` доступ к шаре.

Артефакты:

```bash
PECmd.exe -f "C:\Windows\Prefetch\CMD.EXE-*.pf" --csv out
AmcacheParser.exe -f Amcache.hve --csv out
AppCompatCacheParser.exe -f SYSTEM --csv out
MFTECmd.exe -f '$MFT' --csv out
MFTECmd.exe -f '$J' --csv out
```

- Prefetch: имя, путь, время запуска, счётчик; `SRUM` — отдельно через `SrumECmd`.
- Amcache: установленные/запущенные бинари, хэши.
- Shimcache/AppCompat: следы запуска, даже удалённых файлов.
- `$MFT`: таймстампы `$STANDARD_INFORMATION` и `$FILE_NAME`; расхождение — timestomping.
- `$UsnJrnl:$J`: переименования/удаления; `$LogFile` — журнал транзакций.
- PowerShell: `%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`, транскрипты, `4104`.
- Fileless: WMI `__EventFilter` + `CommandLineEventConsumer`/`ActiveScriptEventConsumer`, `powershell -enc`, `mshta`, `rundll32`, `regsvr32`, `certutil -urlcache`.
- Планировщик: `C:\Windows\System32\Tasks\*`, `schtasks /query /fo LIST /v`.
- Службы: `HKLM\SYSTEM\CurrentControlSet\Services`, `sc qc`.
- Браузеры: `History`, `Cookies`, `Login Data`, `Web Data`, `Local Storage`, `IndexedDB`.

## 5. Linux

```bash
cat ~/.bash_history ~/.zsh_history ~/.python_history
cat /etc/crontab; ls -la /etc/cron.* /var/spool/cron/crontabs
systemctl list-timers --all; systemctl list-unit-files --state=enabled
journalctl --directory=/var/log/journal -o json
last -aiF; lastb; lastlog; who -a; w
```

- `auth.log`/`secure`: sudo, ssh, su, новые пользователи.
- `journald`: `journalctl -u ssh`, `_COMM`, `_EXE`, `_PID`; бинарный формат — `journalctl --file`.
- `/proc/<pid>/{cmdline,environ,maps,fd,exe,cwd,root}`; удалённый бинарь: `ls -l /proc/*/exe | grep deleted`.
- Rootkit: `chkrootkit`, `rkhunter --check`, `debsums -c`, `dpkg -V`, `rpm -Va`, `lsmod`, `/etc/ld.so.preload`, `LD_PRELOAD`, `unhide`.
- Persistence: `~/.config/systemd/user`, `/etc/systemd/system`, `.bashrc`, `.profile`, `/etc/rc.local`, `authorized_keys`, `sudoers`.
- Docker: `/var/lib/docker/overlay2`, `docker ps -a`, `docker history --no-trunc`, `docker inspect`, `docker save`, `dive`, `docker diff`.
- Прошивка: `binwalk -Me fw.bin`, `unsquashfs`, `jefferson` (JFFS2), `ubireader_extract_images`/`ubireader_extract_files` (UBI), `debugfs -R "ls -l"` (ext4), `strings -n 8`, `xxd`.
- U-Boot: `binwalk`, `dumpimage -l`, `fw_printenv`, `uboot-mkimage`; ищи заголовок `0x27051956` и переменные окружения.
- UEFI/BIOS: `UEFITool`, `uefi-firmware-parser`, `PSPTool`, `chipsec`; ищи `$PSP`, `$FTD`, `FET` по `0x020000`.
- Хвосты прошивки: ключи/IV могут лежать за пределами rootfs — проверяй весь файл, а не только распакованную ФС.

## 6. Malware

```bash
file sample.exe; diec sample.exe; pestudio sample.exe
strings -n 6 -el sample.exe
floss sample.exe
capa -r rules/ sample.exe
pefile sample.exe
yara -r rules.yar sample.exe
upx -d sample.exe -o unpacked.exe
```

- Packer/compiler: Detect It Easy, PEiD, `upx`; распаковка — x64dbg + Scylla, `pe-sieve /pid`.
- .NET: `dnSpy`, `ILSpy`, `dotPeek`; ищи `Assembly.Load`, `FromBase64String`, `Aes`, `MkAddr`.
- Shellcode: `scdbg`, `speakeasy`, `CAPA`; карвинг PE из памяти по `MZ...PE\0\0`.
- `PE2shc`: PE-заголовок в дампе, код с 0-го оффсета; вырежи и открой в IDA/Ghidra.
- API hashing: восстанови имена функций перебором экспортов и той же хэш-функции (см. `brokilon`).
- Инъекции: `CreateProcessReflection`, `QueueUserAPC`, `NtMapViewOfSection`; ищи в `malfind`/`vadinfo`.
- C2: строки, конфиг, `CobaltStrikeParser`, `1768.py`; DNS/HTTP beaconing, JA3, периодичность.
- Anti-forensics: `IsDebuggerPresent`, VM-проверки, `Sleep`, `GetTickCount`, обфускация строк XOR/RC4.
- YARA: семейство, строки, импорты; проверь ложные срабатывания.

## 7. Стеганография

```bash
exiftool -a -G1 file
binwalk -Me file
foremost -i file -o out
zsteg -a file.png
stegseek file.jpg rockyou.txt
steghide extract -sf file.jpg -p password
pngcheck -v file.png
identify -verbose file.png
```

- PNG: chunks `tEXt/zTXt/iTXt`, LSB в `IDAT`, палитра, `zsteg -a`; `pngcheck` покажет аномалии. Визуально — `stegsolve` (каналы, битовые плоскости, frame browser).
- JPEG: EXIF, комментарии, appended data после `FFD9`, `jsteg`, `outguess`, `steghide`.
- Аудио: спектрограмма `sox in.wav -n spectrogram -o spec.png` или `ffmpeg -i in.wav -lavfi showspectrumpic spec.png`; DTMF, Morse, SSTV.
- ZIP: `zip2john` + john, `bkcrack` при known plaintext, `7z l -slt`, `unzip -l`; битый архив — `zip -FF`.
- PDF: `pdfinfo`, `pdftotext`, `pdfimages -all`, `pdfdetach -saveall`, `qpdf --qdf`, `mutool clean`.
- Office: `unzip` (docx/xlsx/pptx — ZIP), `olevba`, `oletools`, `msoffcrypto-tool`; скрытые слайды/картинки.
- Видео: `ffmpeg -i in.mp4 frames/%04d.png`, `exiftool`, `mkvinfo`.
- QR/штрихкод: `zbarimg`, `qrdecode`.
- Whitespace: `stegsnow -C`, `stegdetect`.
- Файл «слишком большой» — почти всегда appended data: `binwalk`, `tail -c`, `xxd`.

## 8. Мобильные

Android:

```bash
adb backup -apk -shared -all -f backup.ab
abe unpack backup.ab backup.tar
tar xf backup.tar
jadx -d out app.apk
apktool d app.apk -o apk_out
aapt dump badging app.apk
sqlite3 databases/app.db ".tables"
```

- Смотри `AndroidManifest.xml`, `shared_prefs/*.xml`, `databases/*.db`, `files/`, `cache/`.
- Шифрование/ключи — в `SharedPreferences`, native `.so`, `strings`.
- Frida/objection — динамический обход root/SSL pinning.

iOS:

```bash
idevicebackup2 backup --full ./backup
plutil -p Info.plist
sqlite3 Manifest.db "select * from Files;"
```

- iTunes backup: `Manifest.db`, файлы по SHA1-именам; `plist` — бинарный (`plistutil -i`).
- `class-dump`, `frida-ios-dump`, `objection` — для приложений.

## 9. Разбор задач Кубка

| Задача | Год | Артефакт | Техника / ключевая идея |
|---|---|---|---|
| babyfor | 2025 | pcapng + blob | HTTP-скачивание → `binwalk` находит ZIP без первого байта `P` → восстанови `PK\x03\x04` → PPTX → скрытая картинка |
| Funeral | 2025 | прошивка + pcapng | `binwalk` → ядро/rootfs/хвост 48 байт; `unsquashfs`; crontab → подменённый `egrep`; AES-ECB ключ из хвоста → UDP 1337 → картинка |
| BimboIncident | 2025 | дамп памяти | руткит-драйвер `WinCrypt.sys` скрыл процесс (unlink `ActiveProcessLinks`, zero `ImageFileName`); патч Vol3 → `psscan`/`memmap`; PE2shc shellcode; строки XOR 13; ключ = `"SNEZHANAMALVAREV"` xor первые 16 байт PNG |
| brokilon | 2025 | `HKCU.hiv` | автозапуск Group Policy Logon → PowerShell loader → инъекция в `explorer.exe` через `CreateProcessReflection` (+0x2a70) → API hashing → RC4-конфиг из SID → расшифровка файла → сетевой клиент PE2shc → скачать и расшифровать |
| gamer | 2023 | дамп памяти | `firefox.exe` → фрагменты MPEG-TS (Twitch) → `binwalk`/карвинг; альтернатива — скриншот; часть 1 — XML-сейв Minesweeper |
| zion | 2023 | core dump | `strings core` → `grep ctfcup`; zion-revenge — TLS 1.3 `trafficSecret` из Go-дампа через delve → расшифровка записей → `binwalk` gRPC |
| Red_firmware_I | 2022 | UEFI AMD PSP | `FET` по `0x020000`; модуль `$FTD`; 16-байтный заголовок + 7 записей по 16 байт; собрать куски флага по физическим адресам |
| fallen_angel | 2022 | E01 | `ewfmount` → `fls`/`icat` → MP4 → `exiftool` GPS → населённый пункт |
| french_connection | 2022 | дамп Win8.1 | Vol3 `pstree`/`cmdline`/`netscan`/`malfind` → DLL hijack в `spoolsv` → `ualapi.dll` → base64 payload → `certreq` exfil |
| malware_autopsy | 2022 | pcap | SMTP-вложение ISO → LNK → `regasm.exe` → .NET DLL → ILSpy → `MkAddr` → второй stage AES → расшифровать `flag.encrypted` |

## 10. Чек-лист «20 минут на форензику»

1. **0–2 мин.** `sha256sum`, `file`, `strings`, `binwalk -Me`, `exiftool`. Зафиксируй тип и время.
2. **2–5 мин.** Определи артефакт: образ / память / pcap / реестр / бинарь / прошивка. Открой нужный раздел.
3. **5–9 мин.** Собери базовый контекст: процессы, файлы, соединения, автозапуск, таймлайн.
4. **9–13 мин.** Ищи аномалию: скрытый процесс, неизвестный DLL, лишний автозапуск, подозрительный домен, appended data.
5. **13–17 мин.** Извлеки и расшифруй: `dumpfiles`/`icat`/`export-objects`, ключи из памяти/реестра, XOR/RC4/AES.
6. **17–20 мин.** Проверь флаг на формат, посмотри таймзону и кодировку, сохрани команды/хэши для отчёта.

## 11. Грабли

- **Timezone.** Windows-артефакты часто в UTC, условия — в локальном; `date -u`, `TZ=UTC`, проверяй смещение.
- **Кодировки.** `strings` по умолчанию ищет ASCII; для Windows — `-el` (UTF-16LE), для русского — cp1251.
- **Anti-forensics.** Очистка логов, timestomping, удаление файлов, `vssadmin delete shadows`; смотри `$MFT`, `$J`, `$LogFile`, Volume Shadow Copies.
- **Повреждённые архивы.** ZIP без `PK`, обрезанный EOCD, битый central directory: чини байты, `zip -FF`, `7z x`, `binwalk`.
- **Не весь файл — ФС.** В прошивке ключ/IV может лежать в хвосте за rootfs; проверяй `binwalk` и `tail`.
- **Скрытые процессы.** `psscan` может не показать процесс с занулённым `ImageFileName`; патчь парсер или ищи `_EPROCESS` вручную.
- **Volatility.** Проверь версию (2 vs 3), профиль/символы, битый дамп; `windows.info` должен отработать первым.
- **E01 split.** Монтируй первый сегмент, но проверь наличие всех `.E01..E99`.
- **pcapng.** Не все инструменты читают pcapng; конвертируй `editcap -F pcap`.
- **TLS.** Без keylog TLS 1.3 не расшифровать; ищи ключ в памяти, `SSLKEYLOGFILE`, `trafficSecret`.
- **HTTP/2.** HPACK сжимает заголовки; смотри reassembled stream, а не отдельные кадры.
- **USB HID.** Не путай boot protocol и report protocol; проверь раскладку и модификаторы.
- **Ложные срабатывания.** `malfind`, YARA, `strings "flag"` — проверяй контекст, не тащи первый попавшийся флаг.
- **Не выдумывай флаг.** Если артефакт даёт мусор — вернись к шагу 3 и проверь, тот ли это процесс/файл/поток.
