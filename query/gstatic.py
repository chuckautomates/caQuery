import requests
import boto3
import sys


def gstaticIpRanges():
    url = 'https://www.gstatic.com/ipranges/goog.json'
    response = requests.request("GET", url)
    # Blank list
    ipV4List = []
    # Loop through all returned entries
    for x in range(0,len(response.json()['prefixes'])):
        try:
            # Append IPv4 addresses to IP List
            ipV4List.append(response.json()['prefixes'][x]['ipv4Prefix'])
        except:
            # If it hits an entry other then ipv4 it will skip and continue
            continue
    # Return IPv4 list
    return(ipV4List)


def awsRegionalWafIpSet(ipv4List, aws_access_key, aws_secret_key, region):
    # This function will create a new IP Set List for an AWS WAF,
    # will fail if it set list already exists. (Need to create another Fn)
    # Create client connection to AWS WAFv2
    try:
        client = boto3.client('wafv2',
            aws_access_key_id = aws_access_key,
            aws_secret_access_key = aws_secret_key,
            region_name = region)
        # Send config to Create new IP set list
        response = client.create_ip_set(
            Name= 'GSTATIC-IPs',
            Scope= 'REGIONAL',
            Description= 'IP Ranges recieved from gstatic',
            IPAddressVersion='IPV4',
            Addresses= ipv4List,
        )
        # Check for 200 return response
        if int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
            return(response)
        else:
            returnDict = {'Error': 'Recieved non 200 Status Code while creating Rule Set'}
            return(returnDict)
    # If fails on creating it will check if an existing one will need to be updated
    except:
        returnDict = {'Error': 'Connecting to client'}
        return(returnDict)



if __name__ == '__main__':
    aws_access_key = sys.argv[1]
    aws_secret_key = sys.argv[2]
    region = sys.argv[3]
    ipv4List = gstaticIpRanges()
    print(ipv4List)
    awsRegionalWafIpSet(ipv4List, aws_access_key, aws_secret_key, region)
