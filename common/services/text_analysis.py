import json
import logging

import meaningcloud
from django.conf import settings

logger = logging.getLogger(__name__)

class TextAnalysis:
    def __init__(self, text, language='en'):
        self.model          = 'IAB_en'
        self.license_key    = settings.MEANINGCLOUD_API_KEY
        self.text           = text
        self.language       = language

        self.topic_extraction       = None
        self.topic_extraction_raw   = None
        self.sentiment_analysis     = None
        self.sentiment_analysis_raw = None
        self.categorization         = None
        self.categorization_raw     = None

    def get_topic_extraction(self):
        logger.debug('TextAnalysis.get_topic_extraction()')
        if self.topic_extraction is None:
            logger.debug('topic_extraction not set')
            logger.debug('setting topic_extraction')

            topics_response =  meaningcloud.TopicsResponse(meaningcloud.TopicsRequest(
                self.license_key,
                txt=self.text,
                lang=self.language,
                topicType='ec',
            ).sendReq())

            # Save the raw and serialized topic extraction
            self.topic_extraction_raw   = topics_response.getResults()
            self.topic_extraction       = MeaningCloudResponse(self.topic_extraction_raw).topic()

        logger.debug(self.topic_extraction)
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

            # Save the raw and serialized sentiment analysis
            self.sentiment_analysis_raw = sentiment_response.getResults()
            print(self.sentiment_analysis_raw)
            self.sentiment_analysis     = MeaningCloudResponse(self.sentiment_analysis_raw).absa()

        logger.debug(self.sentiment_analysis)
        return self.sentiment_analysis

    def get_categorization(self):
        logger.debug('TextAnalysis.get_categorization()')
        if self.categorization is None:
            logger.debug('categorization not set')
            logger.debug('setting categorization')

            class_response = meaningcloud.ClassResponse(meaningcloud.ClassRequest(
                self.license_key,
                txt=self.text,
                model=self.model,
            ).sendReq())

            # Save the raw and serialized categorization
            self.categorization_raw = class_response.getResults()
            self.categorization     = MeaningCloudResponse(self.categorization_raw).categorization()

        logger.debug(self.categorization)
        return self.categorization


class MeaningCloudResponse:
    def __init__(self, response):
        self.response = response

    @staticmethod
    def letter_to_number_score(letter):
        """Get a number representation of Meaningcloud's letter score

        Args:
        - letter (string): One of P+, P, P-, N+, N, N-

        Returns:
        - (float): A float representation of Meaningcloud's letter score
        """
        score_map = {
            'P+':   0.9,
            'P':    0.5,
            'P-':   0.2,
            'N-':   -0.2,
            'N':    -0.5,
            'N+':   -0.9,
        }
        return score_map[letter] if letter in score_map else 0

    def absa(self):
        """Serializes a raw MeaningCloud Sentiment Analysis response

        Args:
        - mc_response (str): The raw meaningcloud response

        Returns:
        - (dict) - the serialized result with these fields:
            - text (str) - the raw text input
            - score (float) - the document-wide sentiment score
            - events (list) - individual sentiment events in the document
                - term (str)
                - variant (str)
                - type (str) - aspect or opinion
                - polarity (float)
                - start (int) - start point in the text string
                - end (int) - end point in the text string
        """
        data        = self.response
        result      = {}
        events      = []
        analysis    = data

        for sentence in analysis['sentence_list']:
            if 'segment_list' in sentence:
                for segment in sentence['segment_list']:
                    if 'polarity_term_list' in segment:
                        for p_term in segment['polarity_term_list']:
                            events.append({
                                'term': p_term['text'],
                                'variant': p_term['text'],
                                'type': 'opinion',
                                'polarity': MeaningCloudResponse.letter_to_number_score(p_term['score_tag']),
                                'start': p_term['inip'],
                                'end': p_term['endp'],
                            })
                            if 'sentimented_concept_list' in p_term:
                                for aspect in p_term['sentimented_concept_list']:
                                    events.append({
                                        'term': aspect['form'],
                                        'variant': aspect['variant'],
                                        'type': 'aspect',
                                        'polarity': MeaningCloudResponse.letter_to_number_score(aspect['score_tag']),
                                        'start': aspect['inip'],
                                        'end': aspect['endp'],
                                    })
                    if 'sentimented_concept_list' in segment:
                        for scl in segment['sentimented_concept_list']:
                            events.append({
                                'term': scl['form'],
                                'variant': scl['variant'],
                                'type': 'aspect',
                                'polarity': MeaningCloudResponse.letter_to_number_score(scl['score_tag']),
                                'start': scl['inip'],
                                'end': scl['endp'],
                            })

        result['score']     = MeaningCloudResponse.letter_to_number_score(analysis['score_tag'])
        result['events']    = events

        return result

    def topic(self):
        return self.response

    def categorization(self):
        return self.response
