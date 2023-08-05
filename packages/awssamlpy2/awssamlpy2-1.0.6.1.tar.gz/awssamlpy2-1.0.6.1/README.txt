As part of AWS Governance to enhance the security with the accounts and IAM users, Federated API access is recommended for AWS resources instead of hard-coded IAM AcessID and SecretKeys in the config file.

# Steps:

- If this is the first time install of this python package, use below command:

		For Python2.x version, pip install awssamlpy2
		For Python3.x version, pip install awssamlpy3

- To upgrade this python package to latest version, use below command:

		For Python2.x version, pip install awssamlpy2 --upgrade
		For Python3.x version, pip install awssamlpy3 --upgrade

- Create a 'awssaml.properties' (~/awssaml.properties) file under your user home directory like below -
		
		[UserProp]
		aws-region=us-east-1
		aws-outputformat=json
		idpurl=https://<Your Company AWS SAML Domain>/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices
	
	Please refer to Mesh DOC-111675 for the idpurl
		
- Create a 'configure' file under ~/.aws directory without providing the values for access and secret keys. Dont worry if haven't yet; the package will automatically create one if this file is not present. You may just choose the output and region fields as per your need.
 
		[default]
		output = json
		region = us-east-1
		aws_access_key_id =
		aws_secret_access_key =

- We have taken care to package the required modules. But if there are any additional packages required, install the missing modules based on the error encountered like below:

        On Linux, pip install <module>
            Eg: pip install requests
			
        On Windows, easy_install <module>
            Eg: easy_install requests
 
- Whenever you need SAML access to your AWS services, just the command:

		aws-saml 

- This does the following:
        
        - Verifies your ~/.aws/configure file to set the approriate region; OR creates one if its not present
		
		- Prompts the user for AD username/password and does SAML auth with our ADFS
                    NOTE: Username has to be in the format <domain>\<networkID>
		
		- Based on SAML response, prompts the user to choose the roles available on AWS for that user
		
		- Then, stores the temporarily created credentials (using Amazon STS service) for the user in the ~/.aws/credentials file along with STS token
		
		- Use API calls to work on AWS resources
		
		- Sample API call used in the script is for listing the S3 buckets, which is in Boto2.x format