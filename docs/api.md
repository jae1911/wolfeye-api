# Wolfeye API Docs

```
GET /api/ping
```
This will return a JSON response containing
```
{
	"status": "ok"
}
```

---

```
GET /api/total_db
```
Will return the total count of URLs contained in the database.
```
{
	"cache-hit":true,
	"count":2
}
```
`cache-hit` indicates the result is cached. Cached results are updated every 30 minutes for this endpoint.

---

```
POST /api/search

{
	"query": "query to be searched"
}
```
Will return a JSON response of matched URLs:
```
{
	"cache-hit": true,
	"res": [
		{
			"title": "Jae's website - Main page",
			"url": "https://jae.fi"
		},
		{
			"title": "Minteck's space",
			"url": "https://minteck.org/"
		}
	]
}
```
`cache-hit` indicates the result is cached. Cached results are cleaned every 15 minutes for this endpoint.

---

```
GET /api/admin/get_all

{
	"token": "admin_token"
}
```
Will return a JSON response containing all URLs contained in the database.
```
[
	{
		"last_fetched": "Sun, 12 Dec 2021 15:08:01 GMT",
		"title": "Jae's website - Main page",
		"url": "https://jae.fi"
	},
	{
		"last_fetched": "Sun, 12 Dec 2021 15:56:24 GMT",
		"title": "Minteck's space",
		"url": "https://minteck.org/"
	}
]
```

---

```
POST /api/crawler/add

{
	"url": "https://minteck.org/",
	"title": "Minteck's space",
	"token": "crawler_token"
}
```
Will add the URL and title to the database. To be used by crawlers.
```
{
	"success": "ok"
}
```
