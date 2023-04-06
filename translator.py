import re
from transformers import AutoModelWithLMHead,AutoTokenizer,pipeline
def split_text(text, max_len):
    pattern = re.compile('[.,:。？！；]')
    subtexts = []
    cur_subtext = ''
    for sentence in pattern.split(text):
        if len(cur_subtext) + len(sentence) + 1 > max_len:
            subtexts.append(cur_subtext)
            cur_subtext = sentence.strip()
        else:
            if cur_subtext:
                cur_subtext += ' '
            cur_subtext += sentence

    if cur_subtext:
        subtexts.append(cur_subtext)

    return subtexts
def translate(model_file,input_file,output_file,update_progress):
    text = ''
    with open(input_file, 'r',encoding="utf-8") as f:
        text = f.read()

    result = re.sub(r'\n(?!\n)', '', text)

    sentences = result.split('.')

    def handle_n(sentences):
        res = []
        for s in sentences:
            if s=='\n':
                res.append(s)
            elif s.strip():
                if s.startswith('\n'):
                    res.append('\n')
                res.append(s.strip()+'.')
        return res
    sentences = handle_n(sentences)



    handle_sentences = []
    for sentence in sentences:
        handle_sentences.extend(split_text(sentence, 2000))

    model = AutoModelWithLMHead.from_pretrained(model_file)
    tokenizer = AutoTokenizer.from_pretrained(model_file)
    translation = pipeline("translation_en_to_zh", model=model, tokenizer=tokenizer)

    result =[]

    for i,handle_sentence in enumerate(handle_sentences):
        if handle_sentence=='\n':
            result.append('\n\n')
        else:
            result.append(translation(handle_sentence, max_length=401)[0]['translation_text'])
        update_progress(i,len(handle_sentences))
    with open(output_file, 'w',encoding="utf-8") as f:
        f.write(''.join(result))
