# Jive Content Extractor
The purpose of this Python script is to extract all content from the Jive Community site in preparation for Blackboard's migration to Personify. 

## Pre-Requisites
* Python 3
* Requests package (to install, simply run ```pip install requests``` from the commandline in the project directory.)
* A [Blackboard Community](https://community.blackboard.com) account with sufficient privileges

## Usage
Usage of this script is fairly straight forward:

```python getContents.py --user <jive username> --password <jive password>```

This will pull all content, 100 records at a time. There are a number of command-line configuration items available as well.

| Argument | Description | Comments |
| --- | --- | --- | --- |
| -h/--help | Display usage information | Optional: --help |
| -u/--user | Your Jive username | **Required**: -u myUserName |
| -p/--password | Your Jive password | **Required**: -p myPassword |
| -t/--tags | Comma-delimeted list of tags | Optional: -t developer,developers |
| -d/--doctypes | Comma-delimeted list of document types | Optional: -d document,post,video,idea,discussion. A post is a blog |
| -f/--fields | Comma-delimited list of fields to include | Optional: --f content.text,subject,categories |
| -i/--includeBlogs | Flag to specify inclusion of blogs | Optional: --includeBlogs |
| -c/--count | Number of records to return. Default is 100 | Optional: -c 25 |
| -x/--developers | Use developer community settings | Optional: -x |

If you specify -x, you will bypass all other fields besides username and password. This will get all content with the tags 'developer' or 'developers'. It will pull all documents, blogs, videos, ideas, and discussions. It will return batches of 100 records.

## What You Get
The script builds a folder structure in the project directory. It looks like this:

* content
* content/documents
* content/documents/\<doc title\>
* content/documents/\<doc title\>/\<doc title\>.md
* content/documents/\<doc title\>/metadata.txt
* content/documents/\<doc title\>/comments
* content/documents/\<doc title\>/comments/\<comment id\>.md
* content/documents/\<doc title\>/comments/metadata.txt
* content/documents/\<doc title\>/comments/\<comment id\>/<comment id\>.md
* content/documents/\<doc title\>/attachments/
* content/documents/\<doc title\>/attachments/\<filename\>.\<ext\>
* content/documents/\<doc title\>/images/
* content/documents/\<doc title\>/images/\<image id\>

The comments are nested in directories by their parent id, thus allowing us to maintain nesting of comments and replies. The images don't specify type, so there is no extension. The images do open, though.

## For More Information
For more information on document types, fields available, and information related to Jive's API, visit their [documentation](https://developers.jivesoftware.com/api/v3/cloud/rest/index.html).
