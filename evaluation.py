from sacrebleu.metrics import BLEU, CHRF

bleu = BLEU()
bleu_chrf = CHRF()

with open('Final Project/Data/target/hy_test.txt', 'r') as hy_test, open('Final Project/translations/hy.txt', 'r') as hy_translations:
    test_set = hy_test.read().split('\n')
    translations = hy_translations.read().split('\n')

print('ARMENIAN TRANSLATIONS')
print(bleu.corpus_score(test_set, [translations]))
print(bleu_chrf.corpus_score(test_set, [translations]))
print()

with open('Final Project/Data/target/en_test.txt', 'r') as en_test, open('Final Project/translations/en.txt', 'r') as en_translations:
    test_set = en_test.read().split('\n')
    translations = en_translations.read().split('\n')

print('ENGLISH TRANSLATIONS')
print(bleu.corpus_score(test_set, [translations]))
print(bleu_chrf.corpus_score(test_set, [translations]))
print()