import pandas as pd
import streamlit as st
import openai
import json
import itertools

user_api_key = st.sidebar.text_input(":round_pushpin: Your _OpenAI API key_ here:", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt1 = """         
            You will act as if you are an English teacher. And you will be given two types of data
            1. A Python dictionary with the following keys: 'key_word', 'english_level'
            For example: {'key_word': 'education', 'english_level': 'B2 Upper Intermediate'}
            2. A Python list of part of speech.
            For example: ['Noun', 'Noun', 'Noun']

            Then, make a word list that matches the structure and length of the parts of speech list. 
            Conditions for the elements of the list:
            - Must be a Python string.
            - Must be in English.
            - Must be in lowercase, unless a proper noun or something specific.
            - Should be easily categorize into one part of speech
            - Must be associated with 'key_word' and 'english_level'.
            - Should be unique and meaningful.

            Output list only, with no extra text or comments.   
            Do not say anything until the user says something. 
          """
prompt2 = """ Generate a JSON array of objects based on the given word list and the given dictionary. The following are the keys for the objects in the array:

            - Vocabulary - The word in the list in its original form
            - IPA - The word written in proper and correct International Phonetic Alphabet for the British pronunciation. (example: /ˈliːɡəl/)
            - Part of Speech - Part of speech of each words. Must only be in [noun, verb, adjective, idiom]. 
                             - Can be both at the same time (example: noun/verb, verb/idiom)
            - Definition: A definition of the word in English in one sentence, all lowercase. 
            The definition must also be suitable for the given 'english_level'. For example, if 'english_level' is A1 Beginner, the definition should be easy for A1 Beginner speakers to understand.
            - Example Sentence: A proper English sentence that contains the word. The sentence must also be suitable for the given 'english_level'. 
            For example, if 'english_level' is A1 Beginner, the sentence should be easy for A1 Beginner speakers to understand.
            - Translation: The translation of the word in the student's 'native_lang'.

            Output JSON array of objects only, with no extra text or comments.
            Do not say anything until the user says something.
          """
        
st.write('Peerapas Laisarn 6740173622 Year 1')
st.title(':scroll: :orange[_Associated Words_ Generator] :book:')
st.markdown("Type in an English word, and this Streamlit app will provide you with a number of words that are _related to_ or _associated with_ the word.")
st.divider()

st.subheader('Type in a word. :pencil:')
st.markdown('The word, or words, can literally be anything — from a word to a sentence, or from something very general to something extremely specific.')
with st.expander("_Out of ideas at the moment?_ [click here!]"):
   choices = st.radio("Here are some ideas that you can choose from if you don't have any ideas at the moment", 
                      ['education', 'clothing', 'love', 'water', 'ChatGPT', 'Thailand', 
                       'Basic Programming for Natural Language Processing', 'Taylor Swift','1960s', 'body', 
                       'the economy', 'biology'])
key_word = st.text_input("Or if you already have an idea, type it here!", choices)
with st.container(border=True):
  st.write(':orange[**Your word:**]', key_word)
st.divider()

st.subheader('Enter the number of words you want in your table, based on their part of speech. :abc:')

st.markdown('_How many NOUNS do you want in your table?_')
num_nouns = st.slider('**Nouns**', 1, 20, 1)
with st.container(border=True):
  st.write(':orange[**Nouns:**]', str(num_nouns))

st.markdown('_What about VERBS?_')
num_verbs = st.slider('**Verbs**', 1, 20, 1)
with st.container(border=True):
  st.write(':orange[**Verbs:**]', str(num_verbs))

st.markdown('_Do you want some ADJECTIVES?_')
num_adjs = st.slider('**Adjectives**', 1, 20, 1)
with st.container(border=True):
  st.write(':orange[**Adjectives:**]', str(num_adjs))

st.markdown('_And how about a few IDIOMS?_')
num_idioms = st.slider('**Idioms**', 1, 20, 1)
with st.container(border=True):
  st.write(':orange[**Idioms:**]', str(num_idioms))
st.divider()

st.subheader('Enter your English proficiency level. :school:')
st.markdown('We will use this information to generate a list of words, along with the definitions and the example sentences of those words, that is suitable for your current English proficiency level.')
with st.container(border=True):
  st.write(""":point_down: **Based on the Common European Framework of Reference for Languages (CEFR), which listed 6 levels of proficiency.**
              \nA1 Beginner | A2 Elementary | B1 Intermediate | B2 Upper Intermediate | C1 Advanced | C2 Proficient""")
proficiency_levels = ['A1 Beginner', 'A2 Elementary', 'B1 Intermediate', 'B2 Upper Intermediate', 'C1 Advanced', 'C2 Proficient']
english_level = st.select_slider("Slide from left to right:", options=proficiency_levels)
with st.container(border=True):
  st.write(':orange[**Your proficiency level:**]', english_level)
st.divider()

st.subheader('Enter another language. :earth_asia:')
st.markdown("This can be your native language, or a language of your interest.")
languages = ("Chinese (Simplified)", "Chinese (Traditional)", "French", "German", "Hindi", 
             "Japanese", "Korean", "Russian", "Spanish", "Thai", "Vietnamese")
native_lang = st.selectbox('Choose from the box down below:', languages, index=None, placeholder="Thai")
with st.container(border=True):
  st.write(':orange[**Your chosen language:**]', native_lang)
st.divider()

first_dictionary = {'key_word': key_word, 'english_level': english_level}
second_dictionary = {'key_word': key_word, 'english_level': english_level, 'native_lang': native_lang}
pos_list = [['Noun']*num_nouns] + [['Verb']*num_verbs] + [['Adjective']*num_adjs] + [['Idiom']*num_idioms]

st.subheader("When you are done filling in everything, choose how you want the associated words to be displayed. :computer:")
with st.container(border=True):
  st.markdown('**List of Lists** - You will receive a list of associated words categorized by their parts of speech.')
  st.markdown('**Pandas DataFrame** - You will receive a Pandas dataframe with information on vocabulary, IPA*, POS**, definition, example sentence, and a translation in a language that you had chosen.')
  st.markdown('**Table** - You will receive a table with information on vocabulary, IPA, POS, definition, example Sentence, and a translation in a language that you had chosen.')
  st.markdown('**JSON Array** - You will receive a JSON array of objects with information on vocabulary, IPA, POS, definition, example sentence, and a translation in a language that you had chosen.')
st.markdown('\* "IPA" stands for "International Phonetic Alphabet"')
st.markdown('** "POS" stands for "Part of Speech"')
st.divider()

st.subheader('**Click one of the buttons down below to get the results.** :pushpin:')
col1, col2, col3, col4 = st.columns(4)
if col1.button('List of Lists', use_container_width=True, type='primary'):
  list_of_word_lists = []
  for pos in pos_list:
      lists_match = False
      while not lists_match:
        messages_so_far = [{"role": "system", "content": prompt1}, 
                          {"role": "user", "content": json.dumps(first_dictionary)}, 
                          {"role": "user", "content": json.dumps(pos)}]
        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages_so_far)
        json_str = response.choices[0].message.content
        json_list = json.loads(json_str)
        if len(json_list) == len(pos):
          lists_match = True
          list_of_word_lists.append(json_list)
  st.write(list_of_word_lists)

elif col2.button('Pandas DataFrame', use_container_width=True, type='primary'):
  list_of_word_lists = []
  for pos in pos_list:
      lists_match = False
      while not lists_match:
        messages_so_far = [{"role": "system", "content": prompt1}, 
                          {"role": "user", "content": json.dumps(first_dictionary)}, 
                          {"role": "user", "content": json.dumps(pos)}]
        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages_so_far)
        json_str = response.choices[0].message.content
        json_list = json.loads(json_str)
        if len(json_list) == len(pos):
          lists_match = True
          list_of_word_lists.append(json_list)
  list_of_words = list(itertools.chain.from_iterable(list_of_word_lists))
  messages_so_far = [{"role": "system", "content": prompt2}, 
                    {"role": "user", "content": json.dumps(list_of_words)}, 
                    {"role": "user", "content": json.dumps(second_dictionary)}]
  response = client.chat.completions.create(model="gpt-4o-mini", messages=messages_so_far)
  json_str = response.choices[0].message.content
  json_list = json.loads(json_str)
  df = pd.DataFrame.from_dict(json_list)
  st.dataframe(df)

elif col3.button('Table', use_container_width=True, type='primary'):
  list_of_word_lists = []
  for pos in pos_list:
      lists_match = False
      while not lists_match:
        messages_so_far = [{"role": "system", "content": prompt1}, 
                          {"role": "user", "content": json.dumps(first_dictionary)}, 
                          {"role": "user", "content": json.dumps(pos)}]
        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages_so_far)
        json_str = response.choices[0].message.content
        json_list = json.loads(json_str)
        if len(json_list) == len(pos):
          lists_match = True
          list_of_word_lists.append(json_list)
  list_of_words = list(itertools.chain.from_iterable(list_of_word_lists))
  messages_so_far = [{"role": "system", "content": prompt2}, 
                    {"role": "user", "content": json.dumps(list_of_words)}, 
                    {"role": "user", "content": json.dumps(second_dictionary)}]
  response = client.chat.completions.create(model="gpt-4o-mini", messages=messages_so_far)
  json_str = response.choices[0].message.content
  json_list = json.loads(json_str)
  df = pd.DataFrame.from_dict(json_list)
  st.table(df)

elif col4.button('JSON Array', use_container_width=True, type='primary'):
  list_of_word_lists = []
  for pos in pos_list:
      lists_match = False
      while not lists_match:
        messages_so_far = [{"role": "system", "content": prompt1}, 
                          {"role": "user", "content": json.dumps(first_dictionary)}, 
                          {"role": "user", "content": json.dumps(pos)}]
        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages_so_far)
        json_str = response.choices[0].message.content
        json_list = json.loads(json_str)
        if len(json_list) == len(pos):
          lists_match = True
          list_of_word_lists.append(json_list)
  list_of_words = list(itertools.chain.from_iterable(list_of_word_lists))
  messages_so_far = [{"role": "system", "content": prompt2}, 
                    {"role": "user", "content": json.dumps(list_of_words)}, 
                    {"role": "user", "content": json.dumps(second_dictionary)}]
  response = client.chat.completions.create(model="gpt-4o-mini", messages=messages_so_far)
  json_str = response.choices[0].message.content
  json_list = json.loads(json_str)
  st.write(json_list)
