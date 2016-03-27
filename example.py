from corenlp import StanfordCoreNLP
import pprint

if __name__ == '__main__':
    nlp = StanfordCoreNLP('http://localhost:9000')
    text = ('I went to the Pita Pit restaurant yesterday.The food was delicious but serving was horrible there.')
    # text = ('London is good at studies but bad at sports.')
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,ner',
        'outputFormat': 'json'
    })
    pprint.pprint(output)
    x = output['sentences'][0]['basic-dependencies']
    pprint.pprint(x)
    print '-------------------------------------------------'
    for i in range(len(x)):
        print x[i]['dep'] + '-->' + x[i]['governorGloss'] + '-' + str(x[i]['governor']) + ' ' + x[i]['dependentGloss'] + '-' + str(x[i]['dependent'])
    # print(output['sentences'][0]['parse'])
    # output = nlp.tokensregex(text, pattern='/Pusheen|Smitha/', filter=False)
    # print(output)
    # output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False)
    # print(output)
