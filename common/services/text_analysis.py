# import json
# import six
# import sys
# from google.cloud import language
# from google.cloud.language import enums
# from google.cloud.language import types

# def serialize_entities(entities):
#     result = []
#     for entity in entities:
#         e = {
#             'aspect': entity.name,
#             'type': entity.type,
#             'salience': entity.salience,
#             'sentiment': {
#                 'magnitude': entity.sentiment.magnitude,
#                 'score': entity.sentiment.score,
#             },
#             'mentions': [],
#         }
#         for mention in entity.mentions:
#             e['mentions'].append({
#                 'text': {
#                     'content': mention.text.content,
#                     'begin_offset': mention.text.begin_offset,
#                 },
#                 'type': mention.type,
#                 'sentiment': {
#                     'magnitude': mention.sentiment.magnitude,
#                     'score': mention.sentiment.score,
#                 },
#             })
#         result.append(e)
#     return json.dumps(result)

# class TextAnalysis:
#     client = language.LanguageServiceClient()
#     text = ""
#     sentiment_analysis = ""
#     aspects = []

#     def __init__(self, text):
#         self.text = text
#         self.set_sentiment_analysis_from_text()
#         self.set_aspects_from_sentiment_analysis()

#     def set_sentiment_analysis_from_text(self):
#         text = self.text

#         if isinstance(text, six.binary_type):
#             text = text.decode('utf-8')

#         document = types.Document(
#             content=text.encode('utf-8'),
#             type=enums.Document.Type.PLAIN_TEXT)

#         # Detect and send native Python encoding to receive correct word offsets.
#         encoding = enums.EncodingType.UTF32
#         if sys.maxunicode == 65535:
#             encoding = enums.EncodingType.UTF16

#         result = self.client.analyze_entity_sentiment(document, encoding)

#         self.sentiment_analysis = serialize_entities(result.entities)
#         return self.sentiment_analysis

#     def set_aspects_from_sentiment_analysis(self):
#         print(self.sentiment_analysis)
#         sa = json.loads(self.sentiment_analysis)
#         print(sa)
#         aspects = []
#         for entity in sa:
#             print(entity)
#             aspects.append(entity['aspect'])
#         self.aspects = aspects
#         return self.aspects
