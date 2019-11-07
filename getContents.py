import argparse
import os
import requests
import json

def buildUri(paramType,value):
    global queryParamCount

    print(value)

    if value == None:
        return ''
    elif value == False and paramType == 'includeBlogs':
        return ''
    else:
        if queryParamCount == 0:
            param = '?'
        else: 
            param = '&'

        if paramType == 'tag' or paramType == 'type':
            param += 'filter=' + paramType + '(' + str(value) + ')'
        else:
            param += paramType + '=' + str(value)
        queryParamCount += 1
        return param

def createStructure():
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

    if not os.path.exists('content'):
        os.mkdir('content')

    for doctype in doctypes.split(','):
        if not os.path.exists('content/' + doctype):
            os.mkdir('content/' + doctype)

def getContent(content_item,path):
    
    #print('{} {}'.format(content_item['content']['text'], content_item['subject']))
    
    filename=content_item['subject'] + '.md'
    filename = filename.replace('/', ' ')

    f= open(path + '/' + filename,"w+")
    
    f.write(json.dumps(content_item['content']['text'],indent=4, separators=(',', ': ')))
    
    f.close()

def buildMetadata(content_item,path):
    filename='metadata.txt'

    f= open(path + '/' + filename,"w+")

    f.write('Id: ' + content_item['id'] + '\r\n')
    f.write('Title: ' + content_item['subject'] + '\r\n')
    f.write('Status: ' + content_item['status'] + '\r\n')
    f.write('Created: ' + content_item['published'] + '\r\n')
    f.write('Tags: ' + str(content_item['tags']) + '\r\n')
    f.write('Space: ' + content_item['parentPlace']['name'] + '\r\n')
    f.write('Content Id: ' + content_item['contentID'] + '\r\n')
    f.write('Author: ' + content_item['author']['displayName'] + '\r\n')
    f.write('Status: ' + content_item['status'] + '\r\n')
    f.write('Categories: ' + str(content_item['categories']) + '\r\n')
    f.write('Status: ' + content_item['status'])

    f.close()

def getComments(url,basePath,username,password):

    basePath += '/comments'

    print('URL: ' + url + ' Path: ' + basePath + '\r\n')
    
    r = requests.get(url, auth=(username,password))

    topId = 0
    ids = []

    for comment in r.json()['list']:

        if comment.get('id') == None:
            break

        if not os.path.exists(basePath):
            os.mkdir(basePath)
        
        if comment['parentContent']['type'] != 'comment':
            topId = comment['id']
            path = basePath + '/' + topId
            ids = []
        else: 
            parentId = comment['parentContent']['id']
            if ids.count(parentId) <= 0:
                ids.append(parentId)
            path = basePath + '/' + topId
            for id in ids:
                path += '/' + id
            print(path)

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                print ("OSError: Creation of the directory %s failed" % path)
            except Exception:
                print ("Error: Creation of the directory %s failed" % path)

        print(json.dumps(comment,indent=4, separators=(',', ': ')))
        
        commentFileName = path  + '/' + comment['id'] + '.md'

        print('\r\nFilename' + commentFileName + '\r\n')

        f = open(commentFileName, 'w+')
        
        f.write(str(comment['content']['text']) + '\r\n')
        f.write('Author: ' + comment['author']['displayName'] + '\r\n')

        if comment['replyCount'] <= 0:
            continue
        
        print(str(comment['replyCount']) + '\r\n')

        f.close()

def getAttachments(content_item,path,username,password):
    
    if content_item.get('attachments') != None:
        path += '/attachments'

        if not os.path.exists(path):
            os.mkdir(path)

        for attachment in content_item['attachments']:
            #print(str(attachment))

            url = attachment['url']
            
            r = requests.get(url, auth=(username,password))

            attachmentFileName = path + '/' + attachment['name']

            #print(attachmentFileName)

            f = open(attachmentFileName, 'wb')
            
            f.write(r.content)

            f.close()


def getImages(content_item,path,username,password):
    if content_item.get('contentImages') != None:
        path += '/images'

        if not os.path.exists(path):
            os.mkdir(path)

        for image in content_item['contentImages']:
            #print(str(image))

            url = image['ref']
            
            r = requests.get(url, auth=(username,password))

            imageFileName = path + '/' + image['id']

            #print(imageFileName)

            f = open(imageFileName, 'wb')
            
            f.write(r.content)

            f.close()

parser = argparse.ArgumentParser(description="This script allows you to pull all specified content types from Jive with the specified tags")
parser.add_argument("-u", "--user", type=str, required=True, help="Your Jive username *required")
parser.add_argument("-p", "--password", type=str, required=True, help="Your Jive password *required")
parser.add_argument("-t", "--tags", type=str, default=None, help="An optional comma-delimited list of tags, i.e. --t developer,developers")
parser.add_argument("-d", "--doctypes", type=str, default=None, help="An optional comma-delimited list of document types, i.e. --d document,post,video,idea,discussion. A post is a blog")
parser.add_argument("-f", "--fields", type=str, default=None, help="An optional comma-delimited list of fields to include, i.e. --f content.text,subject,categories")
parser.add_argument("-i", "--includeblogs", action="store_true", default=False, help="Flag to determine whether to include blogs. Default is True")
parser.add_argument("-c", "--count", type=int, default=100, help="Number of records to return. Default is 100")
parser.add_argument("-x", "--developers", action="store_true", default=False, help="Developer Community use case")

args = parser.parse_args()

jiveFQDN = 'mycommunity.jiveon.com'
apiUri = 'https://' + jiveFQDN + '/api/core/v3/'

endpoint = apiUri + 'content'
queryParamCount = 0

username = args.user
password = args.password

if args.developers == True:
    endpoint += '?filter=tag(developer,developers)&filter=type(document,post,video,idea,discussion)&includeBlogs=True&count=100'
else:
    endpoint += buildUri('tag', args.tags)
    endpoint += buildUri('type', args.doctypes)
    endpoint += buildUri('fields', args.fields)
    endpoint += buildUri('includeBlogs', args.includeblogs)
    endpoint += buildUri('count', args.count)

print('{}'.format(endpoint))

while True:
    resp = requests.get(endpoint, auth=(username,password))

    if resp.status_code != 200:
        # This means something went wrong.
        print('GET /contents/ {}'.format(resp.status_code))
        print(resp.text)
        break
    
    createStructure()

    for content_item in resp.json()['list']:
        title = content_item['subject']
        title = title.replace('/', '-')

        print(title)
        if not os.path.exists('content/' + content_item['type'] + '/' + title):
            os.mkdir('content/' + content_item['type'] + '/' + title)

        path = 'content/' + content_item['type'] + '/' + title

        getContent(content_item,path)
        buildMetadata(content_item,path)
        
        if 'comments' in content_item['resources']:
            getComments(content_item['resources']['comments']['ref'],path,username,password)
        
        if 'attachments' in content_item:
            getAttachments(content_item,path,username,password)
        
        if 'contentImages' in content_item:
            getImages(content_item,path,username,password)
    
    try:
        endpoint = resp.json()['links']['next']
    except KeyError:						# If there is no "next" link
        break