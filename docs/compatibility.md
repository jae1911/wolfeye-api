# Feature Compatibility

This document compares features between the new WolfEye API and the proof-of-concept PHP-based API that.

| Feature | WolfEye API | PoC API |
| ------ | ------ | ------ |
| General-purpose Ping | `/api/ping` (GET) | - |
| Database contents information | `/api/total_db` (GET) | - |
| Search | `/api/search` (POST) | `/search` (GET) |
| Database dump | `/api/get_all` (POST) | - |
| Crawler management | `/api/crawler` (POST) | - |
| DuckDuckGo Instant Answers integration | - | `/ratelimited/instant.php` (GET) |
| WolframAlpha integration | *(won't be implemented)* | `/ratelimited/answer.php` (GET) |
