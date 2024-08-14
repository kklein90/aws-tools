import boto3
from slack import WebClient
from slack.errors import SlackApiError
import os
import argparse
import json

def get_slack_token():
    client = boto3.client('secretsmanager')
    secret = client.get_secret_value(SecretId='/slack/pythonmessenger')['SecretString']

    return secret

def send_slack_msg(repo,tag,message):
    repo = repo.upper()
    tag = tag
    message = message
    secret = get_slack_token()
    client = WebClient(secret)
    try:
        response = client.chat_postMessage(
            channel='#image-builds',
            text=repo + ":" + tag + " scan results: \n" + message)
        assert response["ok"] 
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

def get_image_scan_results(repo, tag):
    client = boto3.client('ecr')
    distilled_findings = []
    try:
        scan_findings = client.describe_image_scan_findings(repositoryName=repo, imageId={'imageTag': tag})
    except client.exceptions.ScanNotFoundException as e:
        distilled_findings.append({"name": "no scans for this image", "severity": "", "uri": "", "package": ""})
        return distilled_findings

    for item in scan_findings['imageScanFindings']['findings']:
        for key in item:
            if key == 'name':
                if item['severity'] == "CRITICAL" or item['severity'] == "HIGH":
                    distilled_findings.append({"name": item['name'], "severity": item['severity'], "uri": item["uri"], "package": item["attributes"][2]['value']})

    return distilled_findings


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send container image scan results to Slack')
    parser.add_argument(
        "--repo", "-r",
        type=str,
        default="nginx-proxy",
        help="The repo name to fetch scan results from (nginx-prox, macro-api, readiness-ms)"
    )
    parser.add_argument(
        "--tag", "-t",
        type=str,
        help="The image tag to fetch image scan results from."
    )
    pargs = parser.parse_args()
    repo = pargs.repo
    tag = pargs.tag

    findings = get_image_scan_results(repo, tag)
    send_slack_msg(repo, tag, json.dumps(findings))