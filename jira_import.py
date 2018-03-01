import logging
import csv


def read_jira_issues(filename, jira_base_url):
    epics = {}
    issues = {}
    with open(filename) as jira_export_file:
        issue_reader = csv.DictReader(jira_export_file)
        for issue in issue_reader:
            issue_type = issue['Issue Type']
            issue_key = issue['Issue key']
            issue_summary = issue['Summary']
            issue_link = jira_base_url + issue_key + "/"
            if issue_type == 'Epic':
                epic_name = issue['Custom field (Epic Name)']
                epics[issue_key] = (issue_summary, epic_name, issue_link)
            if issue_type == 'Task' or issue_type == 'Unplanned Task':
                epic_link = issue['Custom field (Epic Link)']
                story_points = issue['Custom field (Story Points)']
                if story_points.endswith(".0"):
                    story_points = story_points[:-2]
                issues[issue_key] = (issue_summary, epic_link, issue_link,
                                     story_points)
    return epics, issues
