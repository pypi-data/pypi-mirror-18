# -*- coding: utf-8 -*-
from JapaneseTokenizer.common import text_preprocess
from JapaneseTokenizer.datamodels import FilteredObject, TokenizedResult, TokenizedSenetence
from JapaneseTokenizer.common import filter
from JapaneseTokenizer import init_logger
from typing import List, Tuple, Any, Union
from future.utils import string_types
import logging
import sys

logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
python_version = sys.version_info


try:
    import Mykytea
except ImportError:
    logger.error(msg='Mykytea is not ready to use yet. Install first')

__author__ = 'kensuke-mi'


class KyteaWrapper:
    def __init__(self, option_string=''):
        assert isinstance(option_string, (str, string_types))
        # option string is argument of Kytea.
        self.kytea = Mykytea.Mykytea(option_string)

    def __list_tags(self, t):
        def convert(t2): return (t2[0], t2[1])
        return [(word.surface, [[convert(t2) for t2 in t1] for t1 in word.tag]) for word in t]

    def __check_char_set(self, input_char):
        # type: (Union[str, unicode]) -> unicode
        if isinstance(input_char, str):
            return input_char.decode('utf-8')
        elif isinstance(input_char, unicode):
            return input_char
        else:
            raise Exception('nor unicode, str')

    def __extract_morphological_information(self, kytea_tags_tuple, is_feature):
        # type: (Tuple[str,List[Any]], bool) -> TokenizedResult
        """This method extracts morphlogical information from token object.
        """
        assert isinstance(kytea_tags_tuple, tuple)
        assert isinstance(is_feature, bool)

        surface = self.__check_char_set(kytea_tags_tuple[0])
        word_stem = u''

        pos_tuple = kytea_tags_tuple[1][0]
        pos = self.__check_char_set(pos_tuple[0][0])
        pos_score = float(pos_tuple[0][1])

        yomi_tuple = kytea_tags_tuple[1][1]
        yomi = self.__check_char_set(yomi_tuple[0][0])
        yomi_score = float(yomi_tuple[0][1])

        tuple_pos = (pos, )

        misc_info = {
            'pos_score': pos_score,
            'pos': pos,
            'yomi': yomi,
            'yomi_score': yomi_score
        }

        token_object = TokenizedResult(
            node_obj=None,
            tuple_pos=tuple_pos,
            word_stem=word_stem,
            word_surface=surface,
            is_feature=is_feature,
            is_surface=True,
            misc_info=misc_info
        )

        return token_object

    def call_kytea_tokenize_api(self, sentence):
        """
        """
        result = self.kytea.getTagsToString(sentence)
        assert isinstance(result, string_types)

        return result

    def tokenize(self, sentence, normalize=True, is_feature=False, return_list=True):
        # type: (Union[str,unicode], bool, bool, bool) -> Union[List[str], TokenizedSenetence]
        """This method returns tokenized result.
        If return_list==True(default), this method returns list whose element is tuple consisted with word_stem and POS.
        If return_list==False, this method returns TokenizedSenetence object.

        :param sentence: input sentence. unicode
        :param normalize: boolean flag to make string normalization before tokenization
        :param is_feature:
        :param is_surface:
        :param return_list:
        :return:
        """
        assert isinstance(normalize, bool)
        assert isinstance(sentence, string_types)
        if normalize:
            normalized_sentence = text_preprocess.normalize_text(sentence, dictionary_mode='ipadic')
        else:
            normalized_sentence = sentence

        normalized_sentence_utf_8 = normalized_sentence.encode('utf-8')
        result = self.__list_tags(self.kytea.getTags(normalized_sentence_utf_8))

        token_objects = [
            self.__extract_morphological_information(
                kytea_tags_tuple=kytea_tags,
                is_feature=is_feature
            )
            for kytea_tags in result]

        if return_list:
            tokenized_objects = TokenizedSenetence(
                sentence=sentence,
                tokenized_objects=token_objects
            )
            return tokenized_objects.convert_list_object()
        else:
            tokenized_objects = TokenizedSenetence(
                sentence=sentence,
                tokenized_objects=token_objects)

            return tokenized_objects

    def convert_str(self, p_c_tuple):
        converted = []
        for item in p_c_tuple:
            if isinstance(item, str): converted.append(item)
            else: converted.append(item)
        return converted

    def __check_pos_condition_str(self, pos_condistion):
        assert isinstance(pos_condistion, list)
        # [ ('', '', '') ]

        return [
            tuple(self.convert_str(p_c_tuple))
            for p_c_tuple
            in pos_condistion
        ]

    def filter(self, parsed_sentence, pos_condition=None, stopwords=None):
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        if isinstance(stopwords, type(None)):
            s_words = []
        else:
            s_words = stopwords

        if isinstance(pos_condition, type(None)):
            p_condition = []
        else:
            p_condition = self.__check_pos_condition_str(pos_condition)

        filtered_object = filter.filter_words(
            tokenized_obj=parsed_sentence,
            valid_pos=p_condition,
            stopwords=s_words
        )
        assert isinstance(filtered_object, FilteredObject)

        return filtered_object
