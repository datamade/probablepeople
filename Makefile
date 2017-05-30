all : probablepeople/generic_learned_settings.crfsuite \
      probablepeople/company_learned_settings.crfsuite \
      probablepeople/person_learned_settings.crfsuite

probablepeople/generic_learned_settings.crfsuite: name_data/labeled/company_labeled.xml name_data/labeled/person_labeled.xml
	parserator train $^ probablepeople --modelfile=generic

probablepeople/company_learned_settings.crfsuite: name_data/labeled/company_labeled.xml
	parserator train $< probablepeople --modelfile=company

probablepeople/person_learned_settings.crfsuite: name_data/labeled/person_labeled.xml
	parserator train $< probablepeople --modelfile=person

