"""
    This module uses ibm watson apis to translate strings
    from english to other languages
"""
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

URL_LT = 'https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/c30a554c-e273-43ba-b15c-d3eb4bcf6993'
APIKEY_LT = 'idrwla-RfY7fJzIH8YpJu2Y3XxnjSbYMQTTC3AeC7YNZ'
VERSION_LT = '2018-05-01'
authenticator = IAMAuthenticator(APIKEY_LT)
language_translator = LanguageTranslatorV3(version=VERSION_LT,authenticator=authenticator)
language_translator.set_service_url(URL_LT)

def englishtofrench(en_text):
    """
    This function translates an english input string
    to a french output string using ibm watson apis
    """
    if en_text:
        translation_response = language_translator.translate(\
            text=en_text, model_id='en-fr')
        translation = translation_response.get_result()
        translation = list(translation.items())
        french_translation = \
            translation[0][1][0]['translation']
        return french_translation
    return ''

def englishtogerman(en_text):
    """
    This function translates an english input string
    to a german output string using ibm watson apis
    """
    if en_text:
        translation_response = language_translator.translate(\
            text=en_text, model_id='en-de')
        translation = translation_response.get_result()
        translation = list(translation.items())
        german_translation = \
            translation[0][1][0]['translation']
        return german_translation
    return ''
