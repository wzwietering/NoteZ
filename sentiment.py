import nltk


class Sentiment:
    """A class with methods to analyze the sentiment of a text"""

    def determine_sentiment(self, data: nltk.Text, language: str) -> str:
        """This method determines sentiment based on word count
        :param data: The data to analyze
        :param language: The language of the text
        :return: Returns a formatted string to inform the user
        :type data: nltk.Text
        :type language: str
        :rtype: str
        """
        if language == 'english':
            prefix = 'en'
        elif language == 'dutch':
            prefix = 'nl'
        else:
            return 'Language not supported'

        with open(f'data/{prefix}_positive.txt') as file:
            positive = file.read().splitlines()
        with open(f'data/{prefix}_negative.txt') as file:
            negative = file.read().splitlines()

        frequency = nltk.FreqDist(data)
        positive_words, negative_words = 0, 0
        for word in positive:
            match = frequency.get(word)
            if match:
                positive_words += match

        for word in negative:
            match = frequency.get(word)
            if match:
                negative_words += match

        print(positive_words, negative_words)
        if positive_words != 0 or negative_words != 0:
            if positive_words >= negative_words:
                ratio = positive_words / (
                    positive_words + negative_words) * 100 * (
                        len(positive) / len(negative))
                result = f"The data is {ratio}% positive"
            else:
                ratio = negative_words / (
                    positive_words + negative_words) * 100 * (
                        len(negative) / len(positive))
                result = f"The data is {ratio}% negative"
            return result
        else:
            return 'No sentiment found'
