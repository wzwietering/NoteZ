import string
from tkinter import simpledialog, messagebox

import gensim
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import sentiment
from tools import toolbox
from ui import settings

text_language = 'english'


class Analyzer:
    def statistics(self, data: str) -> None:
        """Provides easy statistics
        :param data: text to analyze
        :type data: str"""
        tokenized_text = nltk.tokenize.word_tokenize(data)
        nltk_text = nltk.Text(tokenized_text)
        unique_words = len(set(nltk_text))
        length = len(nltk_text)
        diversity = unique_words / length

        # Use cleaned data for more useful results
        nltk_text = nltk.Text(self.clean_text(data))
        most_frequent = nltk.FreqDist(nltk_text)
        most_common_word = most_frequent.most_common(1)
        sentimenter = sentiment.Sentiment()
        global text_language
        messagebox.askokcancel("Statistics",
                               (f"Unique words: {unique_words}\n"
                                f"Word count: {length}\n"
                                f"Diversity: {diversity}\n"
                                f"Most common word: '{most_common_word[0][0]}'"
                                f", used {most_common_word[0][1]} times\n"
                                f"Topics of the text: "
                                f"{self.determine_topic(data)}\n"
                                f"Language: {text_language.capitalize()}\n"
                                f"Sentiment: {sentimenter.determine_sentiment(nltk_text, text_language)}"
                                ))

    def plot_dispersion(self, text: str) -> None:
        """Shows a dispersion plot of any amount of words
        :param text: text to plot
        :type text: str"""
        response = simpledialog.askstring('Plot dispersion',
                                          'Plot dispersion of what? You can'
                                          ' use commas to enter multiple'
                                          ' arguments.')
        if response:
            response = response.replace(" ", "")
            response = response.lower()
            arguments = response.split(',')
            tokenized_text = nltk.tokenize.word_tokenize(text.lower())
            nltk_text = nltk.Text(tokenized_text)
            nltk_text.dispersion_plot(arguments)

    def plot_characters(self, data: str) -> None:
        """Plot the use of characters
        :param data: text to plot
        :type data: str"""
        nltk_text = nltk.Text(data)
        nltk_text.plot()

    def plot_words(self, text: str) -> None:
        """Plot the use of words, without stopwords and numbers
        :param text: text to plot
        :type text: str"""
        tokenized_text = self.clean_text(text)
        nltk_text = nltk.Text(tokenized_text)
        most_frequent = nltk.FreqDist(nltk_text)
        most_frequent.plot(50)
        nltk_text.plot()

    @toolbox.timeit
    def determine_topic(self, data: str) -> None:
        """Uses advanced model to determine topic
        :param data: text to determine topic of
        :type data: str
        :return result: the topics of the text
        :rtype result: str"""
        tokenized_text = self.clean_text(data)
        dictionary = gensim.corpora.Dictionary([tokenized_text])
        corpus = [dictionary.doc2bow(tokenized_text)]
        lda = gensim.models.LdaModel(corpus, num_topics=1, id2word=dictionary,
                                     passes=2)
        topics = lda.print_topics()
        print(topics)

        # Create nice output string
        topics = topics[0][1].split("\"")
        parts = []
        i = 0
        for part in topics:
            if i % 2 != 0:
                parts.append(part)
            i += 1
        result = str(parts).strip('[]').replace("'", "")
        return result

    @toolbox.timeit
    def determine_language(self, data: list) -> str:
        """Determines the language of a text. The parameter can be a string
        or a tokenized text. Only the first 1000 words are used because it
        is faster.
        :param data: text to determine language of
        :type data: str or list[str]
        :return text_language: language of the text
        :rtype: str"""
        if type(data) is str:
            tokenized_text = nltk.tokenize.word_tokenize(data)
            tokenized_text = tokenized_text[0:1000]
        else:
            tokenized_text = data[0:1000]
        language_count = {}
        for language in stopwords.fileids():
            stopwords_set = set(stopwords.words(language))
            words = set(tokenized_text)
            common_words = words.intersection(stopwords_set)
            language_count[language] = len(common_words)
        print(language_count)
        global text_language
        text_language = max(language_count, key=language_count.get)
        return text_language

    def clean_text(self, data: str) -> list:
        """Removes all punctation, stop words and stems all words
        :param data: text to clean
        :type data: str
        :return tokenized_text: cleaned and tokenized text
        :rtype tokenized_text: list[str]"""
        data = data.lower()
        tokenized_text = nltk.tokenize.word_tokenize(data)
        language = self.determine_language(tokenized_text)
        if language == 'dutch':
            tokenized_text = self.modernize_dutch(tokenized_text)
        tokenized_text = self.remove_punctation(tokenized_text)
        if settings.stop_checked.get() == 0:
            tokenized_text = self.remove_stop_words(tokenized_text)
        if settings.stop_checked.get() == 0:
            tokenized_text = self.lemmatize_words(tokenized_text)
        return tokenized_text

    def remove_punctation(self, data: list) -> list:
        """Removes punctation
        :param data: text to remove punctation of
        :type data: list[str]
        :return: text without punctation
        :rtype: list[str]"""
        punctation = list(set(string.punctuation)) + [r'`', r'‘', r'’', '--',
                                                      '...', '"', '``', '\'\'']
        return filter(lambda x: x not in punctation, data)

    def remove_stop_words(self, data: list) -> list:
        """Removes stop words and numbers. Also includes additional stop words
        for English and Dutch to support older texts.
        :param data: text to remove the stopwords of
        :type data: list[str]
        :return: text without stopwords
        :rtype: list[str]"""
        global text_language
        stop_words = set(stopwords.words(text_language))
        more_stop_words_en = {'shall', 'unto', 'thou', 'ye', 'thy', 'thee',
                              'upon', 'hath', '‘i'}
        more_stop_words_nl = {'den', 'zoo', 'gij', 'the', 'dien', '\'t', '\'s',
                              'wij', 'de', '\'n'}
        numbers = set(map(str, range(0, 10)))
        stop_words = stop_words | more_stop_words_en | more_stop_words_nl | \
                     numbers
        return filter(lambda x: x not in stop_words, data)

    def lemmatize_words(self, data: list) -> list:
        """Lemmatize words
        :param data: text to remove punctation of
        :type data: list[str]
        :return: lemmatized text
        :rtype: list[str]"""
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(i) for i in data]

    def modernize_dutch(self, data: list) -> list:
        """In old Dutch, the 'y' is often used on places where the modern
        Dutch uses 'ij'. By replacing the characters, old stop words are
        detected by the remove_stop_words method
        :param data: text to modernize
        :type data: list[str]
        :return: modernized Dutch
        :rtype: list[str]"""
        return [word.replace('y', 'ij') for word in data]
