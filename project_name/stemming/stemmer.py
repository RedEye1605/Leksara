import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class FlexibleStemmer:
    
    def __init__(self):
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()
        
    def stem_text(self, text: str, word_list = None, mode: str = 'keep') -> str:
        if not isinstance(text, str):
            return text

        if word_list is None:
            word_list = []
            
        word_set = {word.lower() for word in word_list}
        words = text.split()
        stemmed_words = []

        if mode == 'keep':
            for word in words:
                if word.lower() in word_set:
                    stemmed_words.append(word)
                else:
                    stemmed_words.append(self.stemmer.stem(word))
        elif mode == 'only':
            for word in words:
                if word.lower() in word_set:
                    stemmed_words.append(self.stemmer.stem(word))
                else:
                    stemmed_words.append(word)
        else:
            raise ValueError("Mode tidak valid. Gunakan 'keep' atau 'only'.")
            
        return ' '.join(stemmed_words)
    
    def stem_column(self, series: pd.Series, stemming: list = None, mode: str = 'keep') -> pd.Series:

        if stemming is None:
            stemming = []
        return series.apply(lambda x: self.stem_text(x, word_list=stemming, mode=mode))
