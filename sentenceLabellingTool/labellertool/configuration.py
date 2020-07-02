import os

ROOT = os.path.dirname(os.path.abspath(__file__))

'''<----- Data Files Path --------->'''
resume_data_path = os.path.join(ROOT, 'resume')
job_descriptions_data_path = os.path.join(ROOT, 'job description')
other_data_path = os.path.join(ROOT, 'other')

# '''<------- Model and Tokenizers -------->'''
# tokenizer_path = os.path.join(ROOT, 'models/new_tokenizer.pickle')
# model_path = os.path.join(ROOT, 'models/resume_identifier.sav')

'''<----------NER Model Files --------->'''
jarPath = os.path.join(ROOT,'models/stanford-ner.jar')
NerModelPath = os.path.join(ROOT,'models/NER_model.ser.gz')


'''<--------- Document Classification Model------>'''
tfidf_vec_path = os.path.join(ROOT, 'models/tfidf1.pkl')
SVC_classifier = os.path.join(ROOT,"models/new_model_svc.pkl")

'''<-----Segementation Model ---->'''
ResumeSegmentationModelPath = os.path.join(ROOT,'models/segment_identifier.pkl')

'''<-------Pool Parser files--------->'''
technical_skills_pool = os.path.join(ROOT,'data/technical_skills.csv')
soft_skills_pool = os.path.join(ROOT,'data/soft_skills_resume.csv')
languages_pool = os.path.join(ROOT,'data/languages.csv')
nationality_pool = os.path.join(ROOT,'data/nationality_data.csv')