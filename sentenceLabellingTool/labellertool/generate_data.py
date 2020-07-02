import csv
import pandas as pd
from os import walk
from labellertool import configuration as cfg
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
import string
import os

from labellertool.datareader import prepare_text

class sentencelabel:

    def __init__(self, resume_path):
        self.resume_path = resume_path

    def return_resume_files_path(self):
        resume_files = [filenames for (dirpath, dirnames, filenames) in walk(self.resume_path)][0]
        resume_files_path = [self.resume_path + '/' + filename for filename in resume_files]
        return resume_files_path

    # resume_path = "C:/Users/zerad/Desktop/dolphinlab-master/seven/resume"
    

    # resume_files = [filenames for (dirpath, dirnames, filenames) in walk(cfg.resume_data_path)][0]
    # resume_files_path = [cfg.resume_data_path + '/' + filename for filename in resume_files]

    def sent_tag(self,resume):
        new_texts = []
        pos_tag_text = []
        texts = prepare_text(resume,True)
        texts = [text.splitlines() for text in texts]
        
        for text in texts:
            for word in text:

                new_texts.append(word_tokenize(word.translate(str.maketrans('', '', string.punctuation))))
        # flat_list_sent = [item for sublist in new_texts for item in sublist]
        sent_pos_tags = [pos_tag(sent) for sent in new_texts]
        
        tag_text = ''
        for text in sent_pos_tags:
            for pos in text:
                if(text.index(pos)==0):
                    tag_text = pos[1]
                else:
                    tag_text = tag_text + ',' + pos[1]
            pos_tag_text.append(tag_text)
        
        return new_texts, pos_tag_text

    def labelit(self):
        chunk_sentence = []
        chunk_pos = []

        resume_files_path = self.return_resume_files_path()

        for resume in resume_files_path:
            val_new, val_pos = self.sent_tag(resume)
            chunk_sentence = chunk_sentence + val_new
            chunk_pos = chunk_pos + val_pos
            # break

        # print(len(chunk_sentence))
        # print(len(chunk_pos))    

        # finaldata = pd.DataFrame({'sentences':chunk_sentence, 'pos_tag':chunk_pos})
        # finaldata['category'] = ''

        return chunk_sentence, chunk_pos
        # print(finaldata)
        # exit()

        # finaldata.to_csv("sentence_classifier_data.csv")
