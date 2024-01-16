import re

twitter_regex = re.compile(
    r"https?://(?:www\.)?(?:twitter\.com|x\.com)/([\w]+)?/?status/(\d+)(?:[\S]+)?"
)
pixiv_regex = re.compile(
    r"https?://(?:www\.)?pixiv\.net(?:/[\w]+)?/artworks/(\d+)(?:[\S]+)?")
fx_domain = "https://fxtwitter.com"
phixiv_domain = "https://phixiv.net"

urlStr = 'https://www.pixiv.net/artworks/115016839\n\
https://www.pixiv.net/en/artworks/112355796\n\
https://x.com/sora72iro_art/status/1743914172864454825?s=20\n\
https://x.com/sora72iro_art/status/1743914172864454825\n\
https://twitter.com/latebirdwakeup/status/1744454638555017453?t=GaCFD4UyW5RU-KJIQ1iPQw&s=19'

urlList = urlStr.split('\n')

matchList = []

for url in urlList:
    matchItem = re.match(pixiv_regex, url)
    if matchItem is not None:
        matchList.append(matchItem)

for case in matchList:
    print(case.groups())
