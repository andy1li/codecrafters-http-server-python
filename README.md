# Build your own HTTP server (Python)
https://app.codecrafters.io/courses/http-server/overview

---

### Start server

`python -m app.main --directory files`

---

### Test manually with HTTPie 

**Stage 2: Respond with 200**

`http localhost:4221`

> HTTP/1.1 200 OK

---
**Stage 3: Respond with 404**

`http localhost:4221/404`

> HTTP/1.1 404 Not Found

---
**Stage 4: Respond with content**

`http localhost:4221/echo/abc`

```
http localhost:4221/
HTTP/1.1 200 OK
Content-Length: 3
Content-Type: text/plain

abc
```

---
**Stage 5: Parse headers**

`http localhost:4221/user-agent`

```
HTTP/1.1 200 OK
Content-Length: 12
Content-Type: text/plain

HTTPie/3.2.2
```

---
**Stage 6: Concurrent connections**

`nc localhost 4221`

---
**Stage 6: Get a file**

`http localhost:4221/files/foo.txt`

```
HTTP/1.1 200 OK
Content-Length: 3
Content-Type: application/octet-stream

bar
```

---
**Stage 7: Post a file**

`cat files/foo.txt | http POST localhost:4221/files/bar.txt`

> HTTP/1.1 201 Created
