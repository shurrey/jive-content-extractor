import argparse
import os
import requests

parser = argparse.ArgumentParser(description="This script allows you to pull all specified content types from Jive with the specified tags")
parser.add_argument("-u", "--user", type=str, required=True, help="Your Jive username *required")
parser.add_argument("-p", "--password", type=str, required=True, help="Your Jive password *required")
parser.add_argument("-t", "--tags", type=str, default="developer,developers", help="An optional comma-delimited list of tags, i.e. --t developer,developers <- This is the default")
parser.add_argument("-d", "--doctypes", type=str, default="document,post,video,idea", help="An optional comma-delimited list of document types, i.e. --d document,post,video,idea <- This is the default. This also accepts discussions, poll, and file. A post is a blog")
parser.add_argument("-f", "--fields", type=str, default="content.text,subject,categories", help="An optional comma-delimited list of fields to include, i.e. --f content.text,subject,categories <- This is the default.")
parser.add_argument("-i", "--includeblogs", action="store_true", default=True, help="Flag to determine whether to include blogs. Default is True")
parser.add_argument("-c", "--count", type=int, default=100, help="Number of records to return. Default is 100")

args = parser.parse_args()

username = args.user
password = args.password
tags = args.tags
doctypes = args.doctypes
fields = args.fields
includeBlogs = args.includeblogs
count = args.count

endpoint = 'https://community.blackboard.com/api/core/v3/contents?filter=tag(' + tags + ')&filter=type(' + doctypes + ')&includeBlogs=' + str(includeBlogs) + '&count=' + str(count) #+ '&fields=' + fields
print('{}'.format(endpoint))

if not os.path.exists('content'):
    os.mkdir('content')

for doctype in doctypes.split(','):
    if not os.path.exists('content/' + doctype):
        os.mkdir('content/' + doctype)


while True:
    resp = requests.get(endpoint, auth=(username,password))

    if resp.status_code != 200:
        # This means something went wrong.
        print('GET /contents/ {}'.format(resp.status_code))
        break
    
    fullbodyfn = 'fullbody.txt'

    if os.path.exists(fullbodyfn):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    fbody= open(fullbodyfn, append_write)

    if append_write == 'a':
        fbody.write("\r\n\r\n")

    fbody.write('{}'.format(resp.status_code))
    fbody.write("\r\n\r\n")
    fbody.write('{}'.format(resp.headers))
    fbody.write("\r\n\r\n")
    fbody.write('{}'.format(resp.text))

    fbody.close()

    for content_item in resp.json()['list']:
        print('{} {}'.format(content_item['content']['text'], content_item['subject']))
        filename=content_item['subject'] + '.html'
        filename = filename.replace('/', ' ')
        f= open('content/' + content_item['type'] + '/' + filename,"w+")
        f.write(content_item['content']['text'])
        f.close()
    
    try:
        endpoint = resp.json()['links']['next']
    except KeyError:						# If there is no "next" link
        break