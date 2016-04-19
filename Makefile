all : probablepeople/generic_learned_settings.crfsuite \
      probablepeople/company_learned_settings.crfsuite \
      person_learned_settings.crfsuite

probablepeople/generic_learned_settings.crfsuite : name_data/labeled/company_labeled.xml name_data/labeled/person_labeled.xml
	parserator train $<,$(word 2,$^) probablepeople --modelfile $@

probablepeople/%_learned_settings.crfsuite : name_data/labeled/%_labeled.xml
	parserator train $< probablepeople --modelfile $@
