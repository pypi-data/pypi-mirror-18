== Install:

VCForPython27.msi (https://www.microsoft.com/en-us/download/details.aspx?id=44266)
lxml-3.5.0.win32-py2.7.exe (https://pypi.python.org/pypi/lxml/3.5.0)

$pip install crawlermaster

== write csslist.json:
example: techcrunch_news_csslist.json

{
    "rawdata-converter-name":"techcrunch_news",
    "local-html-file-pattern":{
        "strBasedir":"C:\\Users\\muchu\\Downloads",
        "strSuffixes":"news.html"
    },
    "csslist":[
        {
            "name": "techcrunch-news-title", 
            "sampleUrl": "https://techcrunch.com/2016/06/02/apple-app-store-goes-down/", 
            "cssRule": "header.page-title h1.tweet-title::text", 
            "sampleAns": [
                "Apple App Store goes down"
            ], 
            "ansType": "exact" 
        },
        {
            "name":"techcrunch-news-tags",
            "sampleUrl":"https://techcrunch.com/2016/06/02/apple-app-store-goes-down/",
            "cssRule":"div.tags a.tag::text",
            "sampleAns":[
                "Apps",
                "Apple",
                "iCloud",
                "iTunes",
                "app-store"
            ],
            "ansType":"exact"
        },
        {
            "name":"techcrunch-news-pubtime",
            "sampleUrl":"https://techcrunch.com/2016/06/02/apple-app-store-goes-down/",
            "cssRule":"header.article-header div.byline time.timestamp::text",
            "sampleAns":[
                "4 hours ago"
            ],
            "ansType":"exist"
        }
    ]
}

== run test:

$crawlermaster csslist.json

== Uninstall:

$pip uninstall crawlermaster

