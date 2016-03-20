from pycorenlp import StanfordCoreNLP
import pprint

if __name__ == '__main__':
    nlp = StanfordCoreNLP('http://localhost:9000')
    text = ('I went to the Pita Pit restaurant yesterday.The food was delicious but serving was horrible there.')
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,ner',
        'outputFormat': 'json'
    })
    pprint.pprint(output)
    print(output['sentences'][0]['parse'])
    output = nlp.tokensregex(text, pattern='/Pusheen|Smitha/', filter=False)
    print(output)
    output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False)
    print(output)
