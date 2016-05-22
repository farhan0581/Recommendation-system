from corenlp import StanfordCoreNLP
import pprint

if __name__ == '__main__':
    nlp = StanfordCoreNLP('http://localhost:9000')
    # text = "Non tolerance was gandhijis weapon."
    # text = ("We went to pitapit,it can be expensive but not hygienic.")
    # text = ("The dishes at Alkareem are highly recommended.")
    text = ("The sitting which is mostly outdoor is the prettiest you can come across in CP")
    # text = ('I loved The Crispy Vegetables but found the Wontons to be devoid of any flavor')
    # text = ("delicious veg manchurian.")
    # text = ('London is good at studies but bad at sports.')
    # text = ("The tiger prawns here,it doesn't get better.")
    # text = ('Check out the pics to find out who greeted me on my first visit to Bercos CP branch, it can be expensive but not hygienic.')
    
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,ner',
        'outputFormat': 'json'
    })
    # pprint.pprint(output)
    tree = output['sentences'][0]['parse']
    print tree
    x = output['sentences'][0]['collapsed-dependencies']
    # pprint.pprint(x)
    print '-------------------------------------------------'
    for i in range(len(x)):
        print x[i]['dep'] + '-->' + x[i]['governorGloss'] + '-' + str(x[i]['governor']) + ' ' + x[i]['dependentGloss'] + '-' + str(x[i]['dependent'])
    # print(output['sentences'][0]['parse'])
    # output = nlp.tokensregex(text, pattern='/Pusheen|Smitha/', filter=False)
    # print(output)
    # output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False)
    # print(output)
    print '-------------------------------------------------'
    y = output['sentences'][0]['tokens']
    for k in range(len(y)):
        print y[k]['lemma'] + ' --> ' + y[k]['pos']
