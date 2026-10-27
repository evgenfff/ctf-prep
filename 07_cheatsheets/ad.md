# Attack-Defense — шпаргалка к X Кубку CTF России 2026

Рабочий документ команды. `$H` — хост атакуемой команды, `$S` — свой хост, `$J` — жюри/чекер-система, `$T` — team token. Все команды и эндпоинты проверяй в правилах и на своей инфраструктуре: в AD нет «универсального» API жюри, но есть повторяемый цикл.

## Формат и главное правило

- AD — это не «взять один флаг», а **удерживать SLA и забирать флаги каждый раунд**. Флаг живёт ограниченное время, его нужно отправлять до ротации.
- Свои сервисы должны отвечать чекеру **всегда**. Патч, который ломает checker, хуже уязвимости: минус SLA и потеря всех флагов.
- Флаги чужих команд обычно лежат в данных сервиса: комментарий счёта, название книги, domain IOC, `secret_ingredient` рецепта, email пользователя.
- Формат флага в репозитории 2025: `TEAM\d{3}_[A-Z0-9]{32}` (иногда base64 с `=`). Проверяй regex на конкретной игре.
- Не делай destructive-действий: `DROP TABLE`, `rm -rf`, массовые блокировки и флуд жюри — это минус SLA и дисквалификация.

## Роли на 5–6 человек

| Роль | Ответственность |
|---|---|
| Капитан/координатор | Тайминг, приоритеты, общение с жюри, финальное решение о патчах, контроль отправки флагов |
| Defense lead | Бэкапы, патчи, рестарты, проверка checker-контракта, откат |
| Attack web | veladora, warehouse, prototype: auth/IDOR/SSRF/десериализация |
| Attack binary | archive: протокол, boost serialization, ROP |
| Infra/monitoring | VPN, доступы, `ss`/`docker`/`kubectl`, логи, SLA, сеть |
| Scribe | Журнал: время, хост, сервис, payload, результат, отправленный флаг, патч |

Если людей меньше — совмещай: капитан + defense, два атакующих, один infra/scribe. **Никто не патчит в одиночку без второго глаза**: цена ошибки — потеря сервиса.

## Таймлайн 10:00–18:00 (день 09:00–19:30)

> 05.12 — академический/смешанный: день `09:00–19:30`, задания `10:00–18:00`. 04.12 — школьный/СПО: день `09:00–19:30`, задания `10:00–19:00`.

| Время | Что делать |
|---|---|
| 09:00–09:30 | Сбор на площадке, подключить VPN, проверить SSH/доступы, получить team token, список сервисов и service ID. Снять snapshot, собрать инвентарь, прогнать checker baseline |
| 09:30–10:00 | Финальная проверка: свои сервисы, checker, логи, бэкапы. Зафиксировать `flag_ids` |
| 10:00–10:15 | Старт раундов. Проверить свои сервисы, зафиксировать `flag_ids`, запустить первые атаки (по одному потоку на сервис) |
| 10:15–10:30 | Первые патчи критичных дыр, которые уже видны; не трогать API-контракты. Собрать очередь атак на 4 сервиса |
| 10:30–12:30 | Циклы по 15 минут: defense → attack → submit → log. Каждый патч проверять чекером |
| 12:30–12:50 | Синхронизация: что сломали, что не работает, какие флаги не дошли. Ротация секретов, если была утечка |
| 12:50–16:30 | Основная фаза: автоматизация эксплойтов, покрытие всех чужих хостов, точечные патчи |
| 16:30–17:30 | Последний агрессивный проход по всем целям; не начинать рискованные патчи своих сервисов |
| 17:30–18:00 | Freeze: только отправка уже добытых флагов, проверка SLA, фиксация результатов, короткое retro |

Раунд обычно 1–3 минуты; **не жди конца раунда**, чтобы отправить флаг. Проверяй, не истёк ли флаг, и не отправляй дубликаты.

## 15-минутный цикл

| Минута | Defense | Attack |
|---|---|---|
| 0–2 | Health/checker по всем своим сервисам; `curl`/`nc` ключевых эндпоинтов | Забрать свежие `flag_ids`, обновить очередь целей |
| 2–5 | Просмотреть логи, 4xx/5xx, новые запросы; проверить, жив ли патч | Прогнать готовые эксплойты по новым ID/хостам |
| 5–10 | Минимальный патч или rollback; проверить контракт | Дожать одну уязвимость, не распыляться на четыре |
| 10–13 | Повторный checker, замер latency, проверка ответов | Собрать флаги, дедуп, отправить |
| 13–15 | Записать патч/откат и его эффект | Записать payload, ошибки, следующий шаг |

## Первые 30 минут

### Доступ и инвентарь

```bash
wg-quick up team.conf                 # или openvpn/ WireGuard по правилам
ssh -i ~/.ssh/ad_key user@$S
sudo -i
ip -br a; ip route; ss -lntup
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
kubectl get pods,svc,ingress -A -o wide
systemctl list-units --type=service --state=running --no-pager
```

- Проверь `sudo -l`, ключи, доступ к `/service`, `/opt`, `/app`, `docker`, `kubectl`, `psql`.
- Найди чекер и его конфиг: `find / -maxdepth 4 -iname '*checker*' 2>/dev/null`; не запускай чужой checker без понимания аргументов.
- Сними snapshot **до** любых изменений:

```bash
mkdir -p /root/ad-backup
tar czf /root/ad-backup/service-$(date +%H%M).tgz /service /app /opt 2>/dev/null
cp -a /service /root/ad-backup/service.orig 2>/dev/null
```

- Запиши внешние URL, порты, TLS/SNI, service ID и team token в общий файл. Проверь, что ты видишь **свои** сервисы и `flag_ids` жюри.

### Проверка checker-контракта

```bash
curl -sk https://$S/health; curl -sk https://$S/api/health
curl -sk -o /dev/null -w '%{http_code} %{time_total}\n' https://$S/
```

- Для TCP-сервиса (archive) — `openssl s_client -connect $S:PORT -servername $S` и баннер.
- Запусти checker/локальный аналог, если он есть. Зафиксируй **точные** ожидаемые коды, поля JSON, тексты ошибок.
- Проверяй не «200 OK», а полный сценарий: регистрация → логин → создание сущности → чтение → удаление/повтор.

## Аудит своего сервиса

- **Маршруты.** Собери все endpoints: `flask routes`, grep роутеров Go/Express, OpenAPI/Swagger, JS, `robots.txt`. Отметь методы, роли, админские пути.
- **Authz/IDOR.** Два аккаунта: A не должен читать/менять B. Меняй ID, UUID, slug, `user_id`, `realm_id`, `payment_id`; пробуй `GET/POST/PUT/PATCH/HEAD/OPTIONS`.
- **SQLi.** `'`, `''`, `\`, time-based, `UNION`; проверь `ORDER BY`, `LIKE`, JSON-поля, хранимые процедуры. `sqlmap -r req.txt --batch --level=3`.
- **NoSQLi.** `{"$ne":null}`, `{"$regex":"^a"}`, `$where`; особенно login/поиск.
- **SSTI.** `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`; проверь PDF/письма/шаблоны.
- **Command injection.** `; id`, `| id`, `$(id)`, `%0a`; аргументы `--config`, `-o`, `git --upload-pack`.
- **SSRF.** Все поля с URL: webhook, импорт, preview, backend, avatar. Проверь `127.0.0.1`, metadata, внутренние k8s-имена, redirect, DNS rebinding.
- **Path traversal/LFI.** `../../`, абсолютный путь, `%2e%2e`, `....//`, symlink, `php://filter`, `file://`.
- **Upload.** Расширения, magic bytes, `.htaccess`, ZIP slip, SVG/XXE, пережатие.
- **Десериализация.** PHP `O:`, Python pickle, Java `rO0AB`, Node `_$$ND_FUNC$$_`, boost archive.
- **Секреты.** `.env`, `docker-compose`, git, ConfigMap/Secret, `/proc/*/environ`, history, логи, образы.
- **Конфиги.** Debug, CORS `*`, default creds, открытые порты, лишние методы, directory listing.
- **Зависимости/CVE.** `pip-audit`, `npm audit`, `trivy fs`, `nuclei -tags cve`, версии в заголовках.
- **Флаги у себя.** `grep -RaoE 'TEAM[0-9]{3}_[A-Z0-9]{32}' /service /app /tmp 2>/dev/null` — чужие флаги у себя тоже проверяй, но не удаляй данные чекера.

## Защита без потери SLA

### Порядок патча

1. Сделай backup файла/образа и запиши исходный hash.
2. Внеси **минимальный** diff: проверка владельца, валидация входа, отключение опасного поля.
3. Собери/перезапусти только затронутый сервис; не перезапускай весь кластер.
4. Прогони checker-сценарий и сравни коды/JSON с baseline.
5. Смотри логи 2–3 минуты; при 5xx — немедленный rollback.
6. Запиши патч в журнал: файл, строки, эффект, кто проверял.

### Типовые безопасные патчи

- **IDOR/ownership.** Добавить `WHERE id=$1 AND user_id=$2`; для `/bill/{payment_id}` — `bill.UserID == authUserID`. Не менять формат `payment_id`, если на него завязан checker.
- **Подмена username.** В `/talk` и `/remember` брать username только из токена; если поле передано — сравнивать с авторизованным.
- **Предсказуемый ID.** Генерировать `payment_id` через `crypto/rand`/UUIDv4; старые ID оставить читаемыми для checker.
- **UUIDv1 API key.** `md5(gen_random_uuid())` или 32 байта `crypto/rand`, не `uuid.NewUUID()`.
- **SSRF.** Allowlist схем/хостов, резолвить DNS и проверять IP, запрещать redirect, не пропускать `X-Forwarded-Host` внутрь. Для gateway — не затирать все заголовки, а allowlist + проверять источник.
- **Path traversal.** `filepath.Clean`, затем `strings.HasPrefix(abs, base+separator)`; для upload — случайное имя и белый список расширений.
- **Boost negative index.** До десериализации проверить, что индекс в архиве не отрицательный; обернуть `load` в try/catch и лимит размера.
- **MinIO.** Пин образа `RELEASE.2025-10-15T17-29-55Z`, закрыть `/admin` на nginx, отозвать старые service accounts.
- **Десериализация.** Подпись/шифрование блоба, allowlist классов, запрет native-форматов; не «чинить» regex-ом.

### Секреты и сессии

- Ротируй `SECRET_KEY`, JWT-ключ, пароли БД, MinIO-ключи **только** если утечка подтверждена; предупреди infra и проверь зависимости.
- После ротации инвалидируй старые сессии/токены; checker может перелогиниваться — проверь.
- Не храни секреты в git/образе; для k8s — Secret + `envFrom`, не ConfigMap.
- Пароли БД и JWT-ключи не меняй одновременно с патчем кода: сначала код, потом секрет, потом checker.

### WAF и логи

- WAF/nginx: блокируй явные `../`, `$regex`, `${jndi`, `php://`, длинные base64-архивы; **allowlist checker IP/UA**.
- Не блокируй `X-Forwarded-Host` глобально: ingress сам его ставит; фильтруй на app-уровне.
- Логи: nginx access/error, app stderr, `kubectl logs -f`, `journalctl -u`, `tcpdump -i any -w /root/ad.pcap`.
- Алерты: 5xx > N, latency > 2s, резкий рост 401/403, повторяющиеся `payment_id`, `../`, `$where`, большие POST.
- Храни логи локально: жюри может не дать доступ к централизованному стеку.

### Rollback

```bash
cp /service/app/handler.go.bak /service/app/handler.go
docker build -f utils/docker/app.Dockerfile -t service-app:latest .
kubectl delete pod -l app=service-app
kubectl rollout undo deployment/service-app
```

- Держи старый образ `:prev` и digest; не удаляй его до конца игры.
- Если патч не проверен — лучше откатить, чем оставить сервис DOWN.

## Эксплуатация

### Получение целей

```bash
curl -s -H "X-Team-Token: $T" "$J/flag_ids?service=4" | jq .
```

- Ответ обычно содержит `host` и список `flag_ids`/`username`/`feed_id`. Сопоставь свой `$H` с записью.
- Service ID смотри в правилах; в репозитории veladora — `4`, у остальных сервисов ID может отличаться.
- Если `flag_ids` нет — работай по списку хостов команд и общим ID/именам из checker-контракта.

### Шаблон threaded-эксплойта

```python
import re, sys, time, threading, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

FLAG = re.compile(r"TEAM\d{3}_[A-Z0-9]{32}")
JURY, TOKEN, SERVICE = "https://jury.example", "TEAM_TOKEN", 4
seen, lock = set(), threading.Lock()

def flag_ids():
    r = requests.get(f"{JURY}/flag_ids", params={"service": SERVICE},
                     headers={"X-Team-Token": TOKEN}, timeout=10, verify=False)
    r.raise_for_status()
    return r.json()

def submit(flag):
    with lock:
        if flag in seen:
            return
        seen.add(flag)
    for attempt in range(3):
        try:
            r = requests.post(f"{JURY}/submit", json={"flag": flag},
                              headers={"X-Team-Token": TOKEN}, timeout=10, verify=False)
            if r.status_code in (200, 201, 409):
                print("SUBMIT", r.status_code, flag, flush=True)
                return
            if r.status_code == 429:
                time.sleep(2 ** attempt)
        except requests.RequestException:
            time.sleep(1 + attempt)

def attack(host, target):
    s = requests.Session()
    s.headers["User-Agent"] = "ad-client/1.0"
    try:
        # ... конкретный эксплойт; вернуть список флагов ...
        text = ""
        for m in FLAG.findall(text):
            submit(m)
    except Exception as e:
        print("ERR", host, target, repr(e), flush=True)

def main():
    data = flag_ids()
    jobs = []
    for host, info in data.items():
        for target in info.get("flag_ids", []):
            jobs.append((host, target))
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(attack, h, t) for h, t in jobs]
        for f in as_completed(futs):
            f.result()

if __name__ == "__main__":
    main()
```

- Один `Session` на поток, не общий: requests не гарантирует потокобезопасность.
- `timeout` везде; `verify=False` только в игровой сети; не логируй токены/пароли.
- Ограничивай параллелизм: 5–10 потоков на сервис, иначе 429/5xx и минус SLA.
- Дедуп флагов и отправки; сохраняй `flag -> time -> host -> exploit` в CSV.
- При 401/403 обнови токен/сессию; при 404 — цель удалена/сменился ID; при 429 — backoff, не retry storm.

### Отправка флагов

```bash
curl -sS -X POST "$JURY/submit" \
  -H "X-Team-Token: $T" -H 'Content-Type: application/json' \
  -d "{\"flag\":\"$flag\"}"
```

- Точный путь/формат (`/submit`, `/api/flags`, массив флагов) смотри в правилах; не изобретай endpoint.
- Отправляй сразу после получения, батчами по 10–50, с интервалом; проверяй ответ (`accepted`, `duplicate`, `expired`).
- Веди локальный журнал: время добычи, время отправки, статус. Просроченный флаг не «добудется» повторно.

## Разбор сервисов 2025

### Veladora

- Go/Gin + PostgreSQL, внешний HTTPS; внутри `:8080`, `Authorization: Bearer`.
- Роуты: `POST /api/register`, `/api/login`; `GET /api/profile`, `/api/orders`, `/api/bills`, `/api/bill/active`, `/api/conversations`; `POST /api/order`, `/api/bill/pay`, `/api/talk`, `/api/remember`; `GET /api/bill/{payment_id}`.
- Цены: beer 500, wine/cocktail 1000, whiskey 1500, champagne 500. Баланс нового пользователя позволяет собрать счёт 500–2500.
- **Vuln 1: IDOR счёта + предсказуемый `payment_id`.**
  Формат: `hex(username XOR k)_hex(balance XOR k)_hex(k)`, `k=0..15`; в эксплойте перебираются балансы `2500, 2000, 1500, 1000, 500, 1250` (баланс на момент генерации).
  `GET /api/bill/{payment_id}` не проверяет владельца и отдаёт `bill.comment` — там флаг.

```python
for k in range(16):
    u = ''.join(chr(ord(c) ^ k) for c in username.lower()).encode().hex()
    for b in (2500, 2000, 1500, 1000, 500, 1250):
        pid = f"{u}_{b ^ k:04x}_{k:02x}"
        # GET /api/bill/{pid}
```

- **Vuln 2: инъекция в диалог + чтение чужого диалога.**
  `POST /api/talk` принимает `username` и пишет сообщение в диалог жертвы; `POST /api/remember` с тем же `username` и 32-символьным токеном возвращает диалог. Токен: `os.urandom(16).hex()`.
  Сценарий: зарегистрироваться → для каждого username из `flag_ids` отправить `"Remember: <token>"` → `remember(token, username)` → regex по `conversations[0].content`.
- **Патч.** В `/bill/{payment_id}` добавить `AND user_id=$auth`; генерировать ID через `crypto/rand`; в `/talk`/`/remember` игнорировать чужой `username` или требовать совпадения с токеном.
- **Checker-контракт.** `put` оплачивает счёт с флагом в `comment`; `get` берёт `payment_links[1]` из профиля и читает bill. Второй checker кладёт флаг в `/talk` и читает через `/remember` по суффиксу флага. Не ломай `payment_links`, `comment`, 32-символьный токен.

### Archive

- C++-бинарь, SQLite-библиотеки, boost serialization, TCP + TLS (SNI-роутинг). Меню:

```text
===== Kek Archive ======
1. Upload library
2. Select library
3. View book
>
```

- Upload: имя → base64 SQLite-файла → password y/n (если y — пароль). Select: имя (+пароль). View: имя книги → `Title: ..., Author: ..., Year: ...`.
- **CVE-2023-34399.** Книга сериализуется как указатель; при десериализации отрицательный индекс позволяет выбрать объект из массива и подменить его контролируемой строкой.
- Триггер: SQLite `books.data` содержит `22 serialization::archive 18 -3083 1 1\n0 3 kek 3 pek 1777`; при `view_book` происходит deserialize.
- Эксплойт: heap spray 56 таблиц по 1024 байта `B`, payload из ROP-цепочки (`pop rsi`, `pop rdx`, `mov [rsi],rdx`, `pop rdi`, `pop rax=59`, `syscall`) повторяется 64 раза; после `select`/`view` — `execve("/bin/sh")`, затем чтение флага.
- Практика: подключение `ssl=True`, base64, точные prompt-строки; после RCE ищи флаг в каталоге библиотек/`/service`, например `grep -RaoE 'TEAM[0-9]{3}_[A-Z0-9]{32}' /service /tmp /app`.
- **Патч.** Проверять индекс до `load` (не отрицательный, в пределах массива), лимит размера, try/catch. Быстрый вариант — отклонять архивы с отрицательным числом после версии `serialization::archive`, не ломая валидные библиотеки. Кардинально — обновить boost или переписать сервис.
- **Checker-контракт.** `put` создаёт библиотеку с флагом в title, загружает с паролем, затем `get` выбирает её и ищет книгу с title=флаг. Не меняй prompt-строки и формат `Title: ..., Author: ..., Year: ...`.

### Warehouse

- 4 микросервиса в k3s: `auth-server` (`:8081`), `warehouse` (`:8080`), `ti-server` (`:8082`), `gateway-server` (`:8000`); ingress: `/auth`, `/warehouse`, `/ti`, `/gateway`. Один PostgreSQL, у каждого своя БД.
- **Vuln 1: UUIDv1 → API key приватного TI-фида.**
  `POST /ti/feeds` создаёт фид; для private API key = `md5(uuid_v1)`. UUIDv1 содержит время и статичный suffix; ID фида и ключ генерируются почти одновременно.
  `GET /ti/feeds?is_public=false` отдаёт `id`; brute первых 8 hex **вперёд** (`prefix + 0..49`), suffix не меняется, ключ — `md5(candidate)`, запрос `GET /ti/feeds/{id}/iocs` с `X-API-Key`. Флаг лежит в domain IOC (`<flag>.malicious.local`).
- **Vuln 2: SSRF в gateway → `/users/search` auth-server.**
  Зарегистрироваться/залогиниться: `POST /auth/auth/register`, `/auth/auth/login` (двойной префикс из-за ingress). Создать VS:
  `POST /gateway/api/virtual-services` с `backend_url: "http://warehouse-auth-server:8081/users"`, `require_auth:false`, `ti_mode:"disabled"`.
  Затем `GET /gateway/vs/{slug}/search?query={user_id}`; gateway прокидывает путь `/search` к `/users/search`. `auth-server` возвращает email с флагом; `InternalOnly` пускает только запросы **без** `X-Forwarded-Host`, а gateway затирает все заголовки, кроме `Authorization`, — поэтому запрос выглядит внутренним.
- Список пользователей: `GET /auth/users?limit=20&offset=0` (или `/warehouse`-эндпоинт поиска).
- **Патч.** `auth-server`: не отдавать `email` в `/users/search`; gateway: не затирать `X-Forwarded-Host` слепо, allowlist заголовков и проверка источника; API key: `md5(random_bytes(16))` или `crypto/rand`.
- **Checker-контракт.** Проверяет public/private feed + IOC, realm/asset/roles, gateway auth 401, TI block 403, auth register/login/profile/logout/public-key. Патч не должен менять коды 401/403 и структуру JSON.

### Prototype

- Flask + MinIO (S3) за nginx; внешний HTTPS `:30081`, MinIO доступен через `/s3`; образ `minio/minio:latest` уязвим.
- Роуты: `GET /obtain_account` → base64url JSON `[access:secret, hmac]`; `POST /upload` (multipart `file`, `X-Token`); `POST /publish_recipe` (`recipe_text`, `secret_ingredient`, `preview_location`); `GET /recipes`; `PUT /like_recipe`; `GET /salt_hash`.
- **CVE-2025-62506.** Создание service account без policy через admin API даёт права администратора. Сценарий: получить временные ключи из `/obtain_account`; создать service account без policy; list buckets; найти `pvc*`; читать `*.json`; забрать `secret_ingredient`.
- **SigV4.** Подпись считается для внутреннего `prototype-s3.prototype.svc.cluster.local:9000`, а запрос отправляется на внешний `/s3`; обычный SDK так не умеет — нужен кастомный клиент (в репо `minioClient.py`).
- **Unintended: переполнение HMAC-соли.** `SALT = token_urlsafe(64)` длиннее 64 байт, HMAC-SHA256 хэширует ключ → эффективный ключ `sha256(SALT)`. `/salt_hash` отдаёт его; можно подписать любой `[data, hmac]`, например `victim:any`, и читать чужие рецепты с флагом.
- **Патч.** Пин MinIO-релиза, закрыть `/admin` на nginx, отозвать service accounts; убрать `/salt_hash`, ротировать соль, использовать `hmac.new(SALT[:64].encode(), ...)` или HKDF.
- **Checker-контракт.** `put`: `/obtain_account` → `/upload` → `/publish_recipe` с флагом в `secret_ingredient`; `get`: `/recipes` с токеном ищет `secret_ingredient == flag`. Не ломай base64url-токен, `/upload`, превью и `/recipes`.

## Чек-лист 15 минут: defense

- [ ] Все свои сервисы отвечают; health/checker — OK.
- [ ] В логах нет 5xx/таймаутов; latency в норме.
- [ ] Патч применён только к одному сервису; есть backup и план отката.
- [ ] Checker-сценарий пройден после патча, коды/JSON совпадают.
- [ ] Секреты не засветились в ответах/логах; сессии не сломаны.
- [ ] WAF не блокирует checker; allowlist проверен.
- [ ] Записаны патч, время, эффект, кто проверял.

## Чек-лист 15 минут: attack

- [ ] Свежие `flag_ids` получены и сопоставлены с хостами.
- [ ] По каждому сервису есть рабочий эксплойт или понятная причина, почему нет.
- [ ] Проверены alternate-пути: IDOR, SSRF, deserialize, auth bypass.
- [ ] Флаги дедуплицированы и отправлены; ответы жюри залогированы.
- [ ] Ошибки 401/403/404/429 разобраны, не retry storm.
- [ ] Payload и результат записаны; следующий шаг понятен.

## Типовые ошибки

- **Патч ломает checker.** Меняешь формат `payment_id`, коды 401/403, поля JSON или prompt-строки — теряешь SLA. Сначала контракт, потом безопасность.
- **Слишком широкий WAF.** Блокирует checker/legit-трафик; всегда allowlist и тест.
- **Ротация всех секретов сразу.** Ломает межсервисную аутентификацию; меняй по одному и проверяй.
- **Нет backup/rollback.** Патч в спешке → сервис DOWN до конца игры.
- **Один поток на все цели.** 429/5xx, бан, пропущенные флаги; ограничивай concurrency.
- **Повторная отправка.** Дубликаты и expired; дедуп и журнал обязательны.
- **Игнор `flag_ids`.** Ручной перебор ID медленный; используй данные жюри.
- **200 OK = успех.** Проверяй тело, флаг, формат, что это не заглушка.
- **Забыл TLS/SNI.** Archive и внешние API требуют `servername`/`verify=False`; иначе таймаут.
- **Атака «в лоб» по чужому сервису.** Сначала свои логи/патчи, потом чужие; не теряй SLA.
- **Флаг не тот.** `TEAM\d{3}_[A-Z0-9]{32}`, иногда base64; проверяй regex и контекст.
- **Паника и распыление.** Один сервис → один эксплойт → один флаг; фиксируй результат.
