import logging

import meaningcloud
from django.conf import settings

logger = logging.getLogger(__name__)

class TextAnalysis:
    model = 'IAB_en'
    license_key = settings.MEANINGCLOUD_API_KEY
    text = ''
    language = 'en'
    topic_extraction = None
    sentiment_analysis = None
    categorization = None

    def __init__(self, text, language='en'):
        self.text = text
        self.language = language

    def get_topic_extraction(self):
        logger.debug('TextAnalysis.get_topic_extraction()')
        if self.topic_extraction is None:
            topics_response =  meaningcloud.TopicsResponse(meaningcloud.TopicsRequest(
                self.license_key,
                txt=self.text,
                lang=self.language,
                topicType='ec',
            ).sendReq())
            self.topic_extraction = topics_response.getResults()
        return self.topic_extraction

    def get_sentiment_analysis(self):
        logger.debug('TextAnalysis.get_sentiment_analysis()')
        if self.sentiment_analysis is None:
            logger.debug('sentiment_analysis not set')
            logger.debug('setting sentiment_analysis')
            sentiment_response = meaningcloud.SentimentResponse(meaningcloud.SentimentRequest(
                self.license_key,
                lang=self.language,
                txt=self.text,
                txtf='plain',
            ).sendReq())
            self.sentiment_analysis = sentiment_response.getResults()
        logger.debug(self.sentiment_analysis)
        return self.sentiment_analysis

    def get_categorization(self):
        logger.debug('TextAnalysis.get_categorization()')
        if self.categorization is None:
            class_response = meaningcloud.ClassResponse(meaningcloud.ClassRequest(
                self.license_key,
                txt=self.text,
                model=self.model,
            ).sendReq())
            self.categorization = class_response.getResults()
        return self.categorization
