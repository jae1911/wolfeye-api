# Wolfeye API Docs

All API endpoints are rate limited to 20 requests per minutes. Different rate limits are described on the endpoints.

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
Will return the total count of URLs contained in the database. Rate limit is 2 per minute.
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
	"token": "crawler_token",
	"description": "page description"
}
```
Will add the URL and title to the database. To be used by crawlers.
```
{
	"success": "ok"
}
```

---

```
POST /api/instant

{
	"query": "reddit"
}
```
Will return a JSON response of the instant search. Rate limit is 3 per minute.
```
{
	"cache-hit": true,
	"res": {
		"Abstract": "Reddit is an American social news aggregation, web content rating, and discussion website. Registered members submit content to the site such as links, text posts, images, and videos, which are then voted up or down by other members. Posts are organized by subject into user-created boards called \"communities\" or \"subreddits\", which cover a variety of topics such as news, politics, religion, science, movies, video games, music, books, sports, fitness, cooking, pets, and image-sharing. Submissions with more upvotes appear towards the top of their subreddit and, if they receive enough upvotes, ultimately on the site's front page. Although there are strict rules prohibiting harassment, it still occurs, and Reddit administrators moderate the communities and close or restrict them on occasion. Moderation is also conducted by community-specific moderators, who are not considered Reddit employees.",
		"AbstractSource": "Wikipedia",
		"AbstractText": "Reddit is an American social news aggregation, web content rating, and discussion website. Registered members submit content to the site such as links, text posts, images, and videos, which are then voted up or down by other members. Posts are organized by subject into user-created boards called \"communities\" or \"subreddits\", which cover a variety of topics such as news, politics, religion, science, movies, video games, music, books, sports, fitness, cooking, pets, and image-sharing. Submissions with more upvotes appear towards the top of their subreddit and, if they receive enough upvotes, ultimately on the site's front page. Although there are strict rules prohibiting harassment, it still occurs, and Reddit administrators moderate the communities and close or restrict them on occasion. Moderation is also conducted by community-specific moderators, who are not considered Reddit employees.",
		"AbstractURL": "https://en.wikipedia.org/wiki/Reddit",
		"Answer": "",
		"AnswerType": "",
		"Definition": "",
		"DefinitionSource": "",
		"DefinitionURL": "",
		"Entity": "infobox",
		"Heading": "Reddit",
		"Image": "/i/0d32099f.png",
		"ImageHeight": 270,
		"ImageIsLogo": 1,
		"ImageWidth": 711,
		"Infobox": {
			"content": [
				{
					"data_type": "string",
					"label": "Type of business",
					"value": "Private",
					"wiki_order": 0
				},
				{
					"data_type": "string",
					"label": "Available in",
					"value": "English, Multilingual",
					"wiki_order": 1
				},
				{
					"data_type": "string",
					"label": "Founded",
					"value": "June 23, 2005",
					"wiki_order": 2
				},
				{
					"data_type": "string",
					"label": "Area served",
					"value": "Worldwide",
					"wiki_order": 3
				},
				{
					"data_type": "string",
					"label": "Owner",
					"value": "Advance Publications (majority shareholder)",
					"wiki_order": 4
				},
				{
					"data_type": "string",
					"label": "Founder(s)",
					"value": "Steve Huffman, Aaron Swartz, Alexis Ohanian",
					"wiki_order": 5
				},
				{
					"data_type": "string",
					"label": "Key people",
					"value": "Alexis Ohanian, Aaron Swartz, Steve Huffman (co-founder and CEO), Jen Wong COO, Drew Vollero CFO, Christopher Slowe CTO",
					"wiki_order": 6
				},
				{
					"data_type": "string",
					"label": "Industry",
					"value": "Social media, Advertising",
					"wiki_order": 7
				},
				{
					"data_type": "string",
					"label": "Revenue",
					"value": ">US$100 million (Q2 2021)",
					"wiki_order": 8
				},
				{
					"data_type": "string",
					"label": "Employees",
					"value": "700 (February 2021)",
					"wiki_order": 9
				},
				{
					"data_type": "string",
					"label": "Website",
					"value": "reddit.com",
					"wiki_order": 10
				},
				{
					"data_type": "string",
					"label": "Advertising",
					"value": "Banner ads and promoted links",
					"wiki_order": 11
				},
				{
					"data_type": "string",
					"label": "Commercial",
					"value": "Yes",
					"wiki_order": 12
				},
				{
					"data_type": "string",
					"label": "Registration",
					"value": "Optional",
					"wiki_order": 13
				},
				{
					"data_type": "string",
					"label": "Current status",
					"value": "Active",
					"wiki_order": 14
				},
				{
					"data_type": "string",
					"label": "Written in",
					"value": "Python, JavaScript",
					"wiki_order": 15
				},
				{
					"data_type": "github_profile",
					"label": "GitHub profile",
					"value": "reddit",
					"wiki_order": "101"
				},
				{
					"data_type": "twitter_profile",
					"label": "Twitter profile",
					"value": "reddit",
					"wiki_order": "102"
				},
				{
					"data_type": "instagram_profile",
					"label": "Instagram profile",
					"value": "reddit",
					"wiki_order": "103"
				},
				{
					"data_type": "facebook_profile",
					"label": "Facebook profile",
					"value": "reddit",
					"wiki_order": "104"
				},
				{
					"data_type": "instance",
					"label": "Instance of",
					"value": {
						"entity-type": "item",
						"id": "Q3220391",
						"numeric-id": 3220391
					},
					"wiki_order": "207"
				}
			],
			"meta": [
				{
					"data_type": "string",
					"label": "article_title",
					"value": "Reddit"
				},
				{
					"data_type": "string",
					"label": "template_name",
					"value": "infobox"
				}
			]
		},
		"Redirect": "",
		"RelatedTopics": [
			{
				"FirstURL": "https://duckduckgo.com/c/Reddit",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Reddit\">Reddit Category</a>",
				"Text": "Reddit Category"
			},
			{
				"FirstURL": "https://duckduckgo.com/Baidu_Tieba",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/Baidu_Tieba\">Baidu Tieba</a> - Baidu Tieba is the most used Chinese communication platform, hosted by the Chinese web services company Baidu. Baidu Tieba was established on December 3, 2003. It is an online community that heavily integrates Baidu's search engine.",
				"Text": "Baidu Tieba - Baidu Tieba is the most used Chinese communication platform, hosted by the Chinese web services company Baidu. Baidu Tieba was established on December 3, 2003. It is an online community that heavily integrates Baidu's search engine."
			},
			{
				"FirstURL": "https://duckduckgo.com/Delicious_(website)",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/Delicious_(website)\">Delicious (del.icio.us)</a> - Delicious was a social bookmarking web service for storing, sharing, and discovering web bookmarks. The site was founded by Joshua Schachter and Peter Gadjokov in 2003 and acquired by Yahoo!.",
				"Text": "Delicious (del.icio.us) - Delicious was a social bookmarking web service for storing, sharing, and discovering web bookmarks. The site was founded by Joshua Schachter and Peter Gadjokov in 2003 and acquired by Yahoo!."
			},
			{
				"FirstURL": "https://duckduckgo.com/Digg",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/Digg\">Digg</a> - Digg, stylized in lowercase as digg, is an American news aggregator with a curated front page, aiming to select stories specifically for the Internet audience such as science, trending political issues, and viral Internet issues.",
				"Text": "Digg - Digg, stylized in lowercase as digg, is an American news aggregator with a curated front page, aiming to select stories specifically for the Internet audience such as science, trending political issues, and viral Internet issues."
			},
			{
				"FirstURL": "https://duckduckgo.com/Diigo",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/Diigo\">Diigo</a> - Diigo is a social bookmarking website that allows signed-up users to bookmark and tag Web pages. Additionally, it allows users to highlight any part of a webpage and attach sticky notes to specific highlights or to a whole page.",
				"Text": "Diigo - Diigo is a social bookmarking website that allows signed-up users to bookmark and tag Web pages. Additionally, it allows users to highlight any part of a webpage and attach sticky notes to specific highlights or to a whole page."
			},
			{
				"FirstURL": "https://duckduckgo.com/Fark",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/Fark\">Fark</a> - Fark is a community website created by Drew Curtis that allows members to comment on a daily batch of news articles and other items from various websites.",
				"Text": "Fark - Fark is a community website created by Drew Curtis that allows members to comment on a daily batch of news articles and other items from various websites."
			},
			{
				"FirstURL": "https://duckduckgo.com/Hacker_News",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/Hacker_News\">Hacker News</a> - Hacker News is a social news website focusing on computer science and entrepreneurship. It is run by Paul Graham's investment fund and startup incubator, Y Combinator. In general, content that can be submitted is defined as \"anything that gratifies one's intellectual curiosity.\"",
				"Text": "Hacker News - Hacker News is a social news website focusing on computer science and entrepreneurship. It is run by Paul Graham's investment fund and startup incubator, Y Combinator. In general, content that can be submitted is defined as \"anything that gratifies one's intellectual curiosity.\""
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Economy_of_San_Francisco",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Economy_of_San_Francisco\">Economy of San Francisco</a>",
				"Text": "Economy of San Francisco"
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Aggregation_websites",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Aggregation_websites\">Aggregation websites</a>",
				"Text": "Aggregation websites"
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Cond%C3%A9_Nast_websites",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Cond%C3%A9_Nast_websites\">Condé Nast websites</a>",
				"Text": "Condé Nast websites"
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Media_sharing",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Media_sharing\">Media sharing</a>",
				"Text": "Media sharing"
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Free_wiki_software",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Free_wiki_software\">Free wiki software</a>",
				"Text": "Free wiki software"
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Question-and-answer_websites",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Question-and-answer_websites\">Question-and-answer websites</a>",
				"Text": "Question-and-answer websites"
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Wikis",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Wikis\">Wikis</a>",
				"Text": "Wikis"
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Y_Combinator_companies",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Y_Combinator_companies\">Y Combinator companies</a>",
				"Text": "Y Combinator companies"
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Free_content_management_systems",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Free_content_management_systems\">Free content management systems</a>",
				"Text": "Free content management systems"
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Free_software_programmed_in_Python",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Free_software_programmed_in_Python\">Free software programmed in Python</a>",
				"Text": "Free software programmed in Python"
			},
			{
				"FirstURL": "https://duckduckgo.com/c/Community_websites",
				"Icon": {
					"Height": "",
					"URL": "",
					"Width": ""
				},
				"Result": "<a href=\"https://duckduckgo.com/c/Community_websites\">Community websites</a>",
				"Text": "Community websites"
			}
		],
		"Results": [
			{
				"FirstURL": "https://www.reddit.com/",
				"Icon": {
					"Height": 16,
					"URL": "/i/reddit.com.ico",
					"Width": 16
				},
				"Result": "<a href=\"https://www.reddit.com/\"><b>Official site</b></a><a href=\"https://www.reddit.com/\"></a>",
				"Text": "Official site"
			}
		],
		"Type": "A",
		"meta": {
			"attribution": null,
			"blockgroup": null,
			"created_date": null,
			"description": "Wikipedia",
			"designer": null,
			"dev_date": null,
			"dev_milestone": "live",
			"developer": [
				{
					"name": "DDG Team",
					"type": "ddg",
					"url": "http://www.duckduckhack.com"
				}
			],
			"example_query": "nikola tesla",
			"id": "wikipedia_fathead",
			"is_stackexchange": null,
			"js_callback_name": "wikipedia",
			"live_date": null,
			"maintainer": {
				"github": "duckduckgo"
			},
			"name": "Wikipedia",
			"perl_module": "DDG::Fathead::Wikipedia",
			"producer": null,
			"production_state": "online",
			"repo": "fathead",
			"signal_from": "wikipedia_fathead",
			"src_domain": "en.wikipedia.org",
			"src_id": 1,
			"src_name": "Wikipedia",
			"src_options": {
				"directory": "",
				"is_fanon": 0,
				"is_mediawiki": 1,
				"is_wikipedia": 1,
				"language": "en",
				"min_abstract_length": "20",
				"skip_abstract": 0,
				"skip_abstract_paren": 0,
				"skip_end": "0",
				"skip_icon": 0,
				"skip_image_name": 0,
				"skip_qr": "",
				"source_skip": "",
				"src_info": ""
			},
			"src_url": null,
			"status": "live",
			"tab": "About",
			"topic": [
				"productivity"
			],
			"unsafe": 0
		}
	}
}
```
`cache-hit` indicates the result is cached. Cached results are cleaned every hour for this endpoint.
