import sys

import meaningcloud
from django.conf import settings

def serialize_entities(entities):
    result = []
    for entity in entities:
        e = {
            'aspect': entity.name,
            'type': entity.type,
            'salience': entity.salience,
            'sentiment': {
                'magnitude': entity.sentiment.magnitude,
                'score': entity.sentiment.score,
            },
            'mentions': [],
        }
        for mention in entity.mentions:
            e['mentions'].append({
                'text': {
                    'content': mention.text.content,
                    'begin_offset': mention.text.begin_offset,
                },
                'type': mention.type,
                'sentiment': {
                    'magnitude': mention.sentiment.magnitude,
                    'score': mention.sentiment.score,
                },
            })
        result.append(e)
    return json.dumps(result)

class TextAnalysis:
    model = 'IAB_en'
    license_key = settings.MEANINGCLOUD_API_KEY
    text = ''
    language = ''
    sentiment_analysis = ''
    topic_extraction = ''
    categorization = ''

    def __init__(self, text, language='en'):
        self.text = text
        self.language = language

    def get_topic_extraction(self):
        topics_response =  meaningcloud.TopicsResponse(meaningcloud.TopicsRequest(
            self.license_key,
            txt=self.text,
            lang=self.language,
            topicType='ec',
        ).sendReq())
        self.topic_extraction = topics_response.getResults()
        return self.topic_extraction

    def get_sentiment_analysis(self):
        sentiment_response = meaningcloud.SentimentResponse(meaningcloud.SentimentRequest(
            self.license_key,
            lang=self.language,
            txt=self.text,
            txtf='plain',
        ).sendReq())
        self.sentiment_analysis = sentiment_response.getResults()
        return self.sentiment_analysis

    def get_categorization(self):
        class_response = meaningcloud.ClassResponse(meaningcloud.ClassRequest(
            self.license_key,
            txt=self.text,
            model=self.model,
        ).sendReq())
        self.categorization = class_response.getResults()
        return self.categorization
