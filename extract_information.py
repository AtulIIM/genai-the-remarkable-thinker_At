import re


def extract_information(given_string):
    # Define regular expressions
    topic_regex = re.compile(r'Topic:(.*?)(?=(Sentiment|$))', re.DOTALL)
    sentiment_regex = re.compile(r'Sentiment:(.*?)(?=(Conclusion|$))', re.DOTALL)
    conclusion_regex = re.compile(r'Conclusion:(.*?)(?=(Summary|$))', re.DOTALL)
    summary_regex = re.compile(r'Summary:(.*)', re.DOTALL)

    # Find matches
    topic_match = topic_regex.search(given_string)
    sentiment_match = sentiment_regex.search(given_string)
    conclusion_match = conclusion_regex.search(given_string)
    summary_match = summary_regex.search(given_string)

    # Extract content for each variable
    topic = topic_match.group(1).strip() if topic_match else ""
    sentiment = sentiment_match.group(1).strip() if sentiment_match else ""
    conclusion = conclusion_match.group(1).strip() if conclusion_match else ""
    summary = summary_match.group(1).strip() if summary_match else ""

    return topic, sentiment, conclusion, summary

