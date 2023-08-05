#!/usr/bin/python

import sys
import boto.sts
import boto.s3
import requests
import getpass
import ConfigParser
import base64
import logging
import xml.etree.ElementTree as ET
import re
import os
from bs4 import BeautifulSoup
from os.path import expanduser
from urlparse import urlparse, urlunparse

##########################################################################
# Variables

sslverification = True

homedir = expanduser("~")

# awscredsfile: The file where this script will store the temp credentials under the saml profile
# awscredsfile = '~/.aws/credentials'
awscredsfile = os.path.join(os.path.expanduser('~'), '.aws', 'credentials')

# propfile: The properties file containing user and company specific properties.
# propfile = '~/awssaml.properties'
propfile = os.path.join(os.path.expanduser('~'), 'awssaml.properties')

if (os.path.isfile(propfile)):
	propfile = os.path.join(os.path.expanduser('~'), 'awssaml.properties')
	print('The AWS SAML property file considered is : %s' %(propfile))
	config = ConfigParser.RawConfigParser()
	config.read(propfile)
	# region: The default AWS region that this script will connect to for all API calls.
	region = config.get('UserProp', 'aws-region')
	#print(region)
	# output format: The AWS CLI output format that will be configured in the saml profile (affects subsequent CLI calls).
	outputformat = config.get('UserProp', 'aws-outputformat')
	# idpentryurl: The initial url that starts the authentication process.
	idpentryurl = config.get('UserProp', 'idpurl')
	#print(idpentryurl)

	if not (os.path.isfile(awscredsfile)):
	        print('The AWS credentials file ~/.aws/credentials is not present user\'s home directory %s. Creating it now.' %(awscredsfile))
        	file = open(awscredsfile,'w')
	        file.write('[default]\nregion = %s\noutput = %s\naws_access_key_id = \naws_secret_access_key = \n' %(region, outputformat))
        	file.close()
else:
	print('The awssaml.properties file doesn\'t exist in user\'s home directory %s. Please create it and try again.' %(homedir))
	exit()
# Uncomment to enable low level debugging
#logging.basicConfig(level=logging.DEBUG)

##########################################################################

# Get the federated credentials from the user
print('Username:'),
username = raw_input()
password = getpass.getpass()
#print('')

# Initiate session handler
session = requests.Session()

# Programmatically get the SAML assertion
# Opens the initial IdP url and follows all of the HTTP302 redirects, and
# gets the resulting login page
formresponse = session.get(idpentryurl, verify=sslverification)
# Capture the idpauthformsubmiturl, which is the final url after all the 302s
idpauthformsubmiturl = formresponse.url

# Parse the response and extract all the necessary values
# in order to build a dictionary of all of the form values the IdP expects
formsoup = BeautifulSoup(formresponse.text.decode('utf8'), "html5lib")
payload = {}

for inputtag in formsoup.find_all(re.compile('(INPUT|input)')):
    name = inputtag.get('name','')
    value = inputtag.get('value','')
    if "user" in name.lower():
        #Make an educated guess that this is the right field for the username
        payload[name] = username
    elif "email" in name.lower():
        #Some IdPs also label the username field as 'email'
        payload[name] = username
    elif "pass" in name.lower():
        #Make an educated guess that this is the right field for the password
        payload[name] = password
    else:
        #Simply populate the parameter with the existing value (picks up hidden fields in the login form)
        payload[name] = value

# Debug the parameter payload if needed
# Use with caution since this will print sensitive output to the screen
#print payload

# Some IdPs don't explicitly set a form action, but if one is set we should
# build the idpauthformsubmiturl by combining the scheme and hostname 
# from the entry url with the form action target
# If the action tag doesn't exist, we just stick with the 
# idpauthformsubmiturl above
for inputtag in formsoup.find_all(re.compile('(FORM|form)')):
    action = inputtag.get('action')
    loginid = inputtag.get('id')
    if action:
	if loginid == "loginForm":
	        parsedurl = urlparse(idpentryurl)
        	idpauthformsubmiturl = parsedurl.scheme + "://" + parsedurl.netloc + action

# Performs the submission of the IdP login form with the above post data
response = session.post(
    idpauthformsubmiturl, data=payload, verify=sslverification)

# Debug the response if needed
#print (response.text)
f = open('response', 'w')
f.write(response.text)
f.close()

# Overwrite and delete the credential variables, just for safety
username = '##############################################'
password = '##############################################'
del username
del password

# Decode the response and extract the SAML assertion
soup = BeautifulSoup(response.text.decode('utf8'), "html5lib")
assertion = ''

# Look for the SAMLResponse attribute of the input tag (determined by
# analyzing the debug print lines above)
for inputtag in soup.find_all('input'):
    if(inputtag.get('name') == 'SAMLResponse'):
        #print(inputtag.get('value'))
        assertion = inputtag.get('value')

# Better error handling is required for production use.
if (assertion == ''):
    #TODO: Insert valid error checking/handling
    print('Response did not contain a valid SAML assertion')
    sys.exit(0)

# Debug only
# print(base64.b64decode(assertion))

# Parse the returned assertion and extract the authorized roles
awsroles = []
root = ET.fromstring(base64.b64decode(assertion))
for saml2attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
    if (saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role'):
        for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
            awsroles.append(saml2attributevalue.text)

# Note the format of the attribute value should be role_arn,principal_arn
# but lots of blogs list it as principal_arn,role_arn so let's reverse
# them if needed
for awsrole in awsroles:
    chunks = awsrole.split(',')
    if'saml-provider' in chunks[0]:
        newawsrole = chunks[1] + ',' + chunks[0]
        index = awsroles.index(awsrole)
        awsroles.insert(index, newawsrole)
        awsroles.remove(awsrole)

# If I have more than one role, ask the user which one they want,
# otherwise just proceed
print ('')
if len(awsroles) > 1:
    i = 0
    print('Please choose the role you would like to assume:')
    for awsrole in awsroles:
        print('[', i, ']: ', awsrole.split(',')[0])
        i += 1
    print('Selection: '),
    selectedroleindex = raw_input()

    # Basic sanity check of input
    if int(selectedroleindex) > (len(awsroles) - 1):
        print('You selected an invalid role index, please try again')
        sys.exit(0)

    role_arn = awsroles[int(selectedroleindex)].split(',')[0]
    principal_arn = awsroles[int(selectedroleindex)].split(',')[1]
else:
    role_arn = awsroles[0].split(',')[0]
    principal_arn = awsroles[0].split(',')[1]

# Use the assertion to get an AWS STS token using Assume Role with SAML
conn = boto.sts.connect_to_region(region)
token = conn.assume_role_with_saml(role_arn, principal_arn, assertion)

# Write the AWS STS token into the AWS credential file
# Read in the existing config file
config = ConfigParser.RawConfigParser()
config.read(awscredsfile)

# Put the credentials into a saml specific section instead of clobbering
# the default credentials
if not config.has_section('saml'):
    config.add_section('saml')

config.set('saml', 'output', outputformat)
config.set('saml', 'region', region)
config.set('saml', 'aws_access_key_id', token.credentials.access_key)
config.set('saml', 'aws_secret_access_key', token.credentials.secret_key)
config.set('saml', 'aws_session_token', token.credentials.session_token)

# Write the updated config file
with open(awscredsfile, 'w+') as configfile:
    config.write(configfile)

# Give the user some basic info as to what has just happened
print('\n\n----------------------------------------------------------------')
print('Your new access key pair has been stored in the AWS configuration file {0} under the saml profile.'.format(awscredsfile))
print('Note that it will expire at {0}.'.format(token.credentials.expiration))
print('After this time, you may safely rerun this script to refresh your access key pair.')
print('To use this credential, call the AWS CLI with the --profile option (e.g. aws --profile saml ec2 describe-instances).')
print('----------------------------------------------------------------\n\n')

# Use the AWS STS token to list all of the S3 buckets
s3conn = boto.s3.connect_to_region(region,
                     aws_access_key_id=token.credentials.access_key,
                     aws_secret_access_key=token.credentials.secret_key,
                     security_token=token.credentials.session_token)

buckets = s3conn.get_all_buckets()

print('Simple API example listing all S3 buckets:')
print(buckets)
