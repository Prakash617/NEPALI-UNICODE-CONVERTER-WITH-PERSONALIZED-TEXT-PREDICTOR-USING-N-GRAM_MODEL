import math
import random
import re
import json
import math

def split_to_sentences(data):
    #get stripped sentences in array removing empty sentences 
    sentences = re.sub(r'[^क-नःप-रलव-हा-ृेैोौ्ँंॐ‍ अ-ऌएऐओऔ।]', "",data)
    sentences = sentences.split('।')
    sentences = [s.strip() for s in sentences]
    sentences = [s for s in sentences if len(s) > 0]
    
    return sentences      

def tokenize_sentences(sentences):
    #get array of tokens/words for each of the sentences
    tokenized_sentences = []
    
    for sentence in sentences:

        tokenized =  sentence.split()

        tokenized_sentences.append(tokenized)
    
    return tokenized_sentences

def get_tokenized_data(data):
    #Combined effect of 
        # 1. Splitting into sentences 
        # 2. Tokenizeing sentences
    sentences = split_to_sentences(data)
    tokenized_sentences = tokenize_sentences(sentences)
    
    return tokenized_sentences



def get_words_ftable(tokenized_sentences):
   # get dictionary containing all tokens(words) with their frequecy
    word_counts = {}
    
    for sentence in tokenized_sentences: 

        for token in sentence: 


            if token not in word_counts :
                word_counts[token] = 1
            
            else:
                word_counts[token] += 1

    
    return word_counts

def get_vocab_above_threshold(tokenized_sentences, threshold):
    
    closed_vocab = []
    
    # Get the word couts of the tokenized sentences
    word_counts = get_words_ftable(tokenized_sentences)
    
    for word, cnt in word_counts.items(): 
        
        if cnt >= threshold  :
            closed_vocab.append(word)

    return closed_vocab

def replace_oov_words_by_unk(tokenized_sentences, vocabulary, unknown_token="<unk>"):
    # tokenized sentences with unk
    vocabulary = set(vocabulary)
    
    # Initialize a list that will hold the sentences after less frequent words are replaced by the unknown token
    replaced_tokenized_sentences = []
    
    for sentence in tokenized_sentences:
        
        # Initialize the list that will contain a single sentence with "unknown_token" replacements
        replaced_sentence = []

        for token in sentence: 

            if token in vocabulary: 

                replaced_sentence.append(token)
            else:

                replaced_sentence.append(unknown_token)
     
        # Append the list of tokens to the list of lists
        replaced_tokenized_sentences.append(replaced_sentence)
        
    return replaced_tokenized_sentences

def preprocess_data(train_data, test_data, threshold):

    # Get the closed vocabulary using the train data
    vocabulary = get_vocab_above_threshold (train_data, threshold)
    
    # For the train data, replace less common words with "<unk>"
    train_data_replaced = replace_oov_words_by_unk(train_data, vocabulary, unknown_token="<unk>")
    
    # For the test data, replace less common words with "<unk>"
    test_data_replaced = replace_oov_words_by_unk(test_data, vocabulary, unknown_token="<unk>")

    return train_data_replaced, test_data_replaced, vocabulary

def get_ngrams_ftable(tokenized_sentences, n):

    # Initialize dictionary of n-grams and their counts
    n_grams = {}
    
    # Go through each sentence in the data
    for sentence in tokenized_sentences: 
        sentence = tuple (sentence)
        
    #count frequency of each ngram
        for i in range(len(sentence) - n + 1 ): 

            # Get the n-gram from i to i+n
            n_gram =   sentence [i: i + n]

            if n_gram in n_grams : 

                n_grams[n_gram] += 1
            else:

                n_grams[n_gram] = 1
                
            #n_grams[n_gram]=n_grams.get(ngram,0)+1
    

    return n_grams

def estimate_probability(word, current_ngram_chunk, 
                         ngram_ftable, nplus1_gram_ftable, vocab_size, k=1.0):
    # for finding, given current_chunk what is the probability of the word...
    # convert list to tuple to use it as a dictionary key
    current_ngram_chunk = tuple(current_ngram_chunk)
    
    
    current_ngram_freq =  ngram_ftable.get(current_ngram_chunk, 0) 
    denominator = current_ngram_freq + (k * vocab_size)

    # current chunk with word
    nplus1_gram_chunk = current_ngram_chunk + (word,)

    nplus1_gram_freq = nplus1_gram_ftable.get(nplus1_gram_chunk, 0)
        
    numerator = nplus1_gram_freq + k

    probability = numerator / denominator
    
    return probability


def estimate_probabilities(current_ngram, ngram_ftable, nplus1_gram_ftable, vocabulary, k=1.0):

    # convert list to tuple to use it as a dictionary key
    current_ngram = tuple(current_ngram)
    
    # add <e> <unk> to the vocabulary
    # <s> is not needed since it should not appear as the next word
    vocabulary_size = len(vocabulary)
    
    probabilities = {}
    for word in vocabulary:
        probability = estimate_probability(word, current_ngram, 
                                           ngram_ftable, nplus1_gram_ftable, 
                                           vocabulary_size, k=k)
        probabilities[word] = probability

    return probabilities

import math

def suggest_a_word(previous_words, ngram_ftable, nplus1_gram_ftable, vocabulary, n, k=1.0, start_with=None):
       
    
    # get the most recent 'n' words from previous words as the previous n-gram
    previous_ngram = previous_words[-n:]

    # Estimate the probabilities that each word in the vocabulary is the next word
    
    probabilities = estimate_probabilities(previous_ngram,
                                           ngram_ftable, nplus1_gram_ftable,
                                           vocabulary, k=k)

    suggestion = None
    
    max_prob = 0

    for word, prob in probabilities.items(): 
        
        if start_with is not None:   
            if   not word.startswith(start_with):
                continue 
        
        if prob > max_prob :
            
            suggestion = word
            max_prob = prob
  
    return suggestion, max_prob

### Get multiple suggestions

def get_suggestions(previous_tokens, ngram_ftable_list, vocabulary, k=1.0, start_with=None):
    model_counts = len(previous_tokens)
    suggestions = []
    for i in range(model_counts):
        ngram_ftable = ngram_ftable_list[i]
        nplus1_gram_ftable = ngram_ftable_list[i+1]
        
        suggestion = suggest_a_word(previous_tokens, ngram_ftable,
                                    nplus1_gram_ftable, vocabulary,
                                    k=k,n=i+1, start_with=start_with)
        suggestions.append(suggestion)
    return suggestions

### Make N-Gram Frequency Table using train_data_processed
def get_ngram_ftable_list(train_data_processed):
    ngram_ftable_list = []
    for n in range(1, 6):
        ngram_ftable = get_ngrams_ftable(train_data_processed, n)
        ngram_ftable_list.append(ngram_ftable)
    return ngram_ftable_list


### Make Prediction List of 1,2,3,4 Gram

def make_prediction_table(ngram_ftable, nplus1_gram_ftable,n):
    temp_dic={}
    for key, freq in nplus1_gram_ftable.items():
        nk=key[:n]
        divider = ngram_ftable[nk]
        temp_dic[nk]=temp_dic.get(nk,None)
        if temp_dic[nk]:
            temp_dic[nk].update({key[n]:freq/divider})
        else:
            temp_dic[nk]={key[n]:freq/divider}

    nexttemp={}
    
    vc=len(list(temp_dic.keys())[0])
    if vc==1:
        for i,d in temp_dic.items():
            l=d.items()
            v=sorted(l,key=lambda x:x[1],reverse=True)
            r=0 #count number of predictin not <unk>
            t=[]
            for j in range(len(v)):
                if v[j][0]!='<unk>':
                    t.append(v[j])
                    r+=1
                if r==3 and i[0]!='<unk>' :break
            nexttemp[i]=t
    else:
        for i,d in temp_dic.items():
            l=d.items()
            v=sorted(l,key=lambda x:x[1],reverse=True)
            r=0 #count number of predictin not <unk>
            t=[]
            for j in range(len(v)):
                if v[j][0]!='<unk>':
                    t.append(v[j])
                    r+=1
                if r==3 :break
            nexttemp[i]=t
    return nexttemp

import time
def select_r(rvalues):
    a=[]
    while len(a)<3:
        random.seed(time.time())
        s=random.randint(0,len(rvalues)-1)
        if rvalues[s] not in a:a.append(rvalues[s])
    return a


def make_prediction_list(ngram_ftable_list):
    p_list=[]
    for i in range(1,len(ngram_ftable_list)):
        p_list.append(make_prediction_table(ngram_ftable_list[i-1],ngram_ftable_list[i],i))
    return p_list

### Calculating Perplexity

def calculate_perplexity(sentence, ngram_ftable, nplus1_gram_ftable, vocabulary_size,n, k=1.0):
   
    sentence = tuple(sentence)
    
    # length of sentence
    N = len(sentence)
    
    summation=0
    # Index t ranges from 0 to N - n, inclusive on both ends
    for t in range(0, N-n): # complete this line

        # get the n-gram preceding the word at position t
        ngram = sentence[t:t+n]
        
        # get the word at position t
        word = sentence[t+n]

        probability =estimate_probability(word, ngram, ngram_ftable, nplus1_gram_ftable, vocabulary_size, k=k)
        summation+=math.log(probability)
#         product_pi *=  (1 / probability)

#     perplexity = product_pi ** (1 / N)
#     perplexity = math.exp(-summation/ N)

    return summation, N

def calculate_pp(test_sentences, ngram_ftable_list, vocab_size, k=1.0):
    ngram_p_list=[]
    for i in range(4):
        count=0
        total=0
        for sentence in test_sentences:
            c,t=calculate_perplexity(sentence,ngram_ftable_list[i],ngram_ftable_list[i+1],vocab_size,n=i+1,k=k)
            count+=c
            total+=t
        ngram_p_list.append(math.exp(-count/total))
    return ngram_p_list

### Calculating Accuracy of Each Model

def calculate_prediction_values(sentence, prediction_list, n):
  
    sentence = tuple(sentence)
    
    # length of sentence 
    N = len(sentence)
    out=0
    count=0
    # Index t ranges from 0 to N - n, inclusive on both ends
    for t in range(n,N-1): # complete this line

        # get the n-gram preceding the word at position t
        ngram = sentence[t-n:t]
         
        e=0
        p=[]
        final=''
        word = sentence[t]
        predicted_word =prediction_list[n-1].get(ngram,[])
        if predicted_word: 
            final=[i[0] for i in predicted_word[:3]]
            out+=1
        if word in final:
            count += 1
#         print(final)
    total_prediction = count+out
    correct_prediction = count
    
    return correct_prediction , total_prediction

def calculate_accuracy(test_sentences, prediction_list):
    ngram_accuracy_list=[]
    for i in range(len(prediction_list)):
        count=0
        total=0
        for sentence in test_sentences:
            c,t=calculate_prediction_values(sentence,prediction_list,n=i+1)
            count+=c
            total+=t
        ngram_accuracy_list.append(count/total)
        
    return ngram_accuracy_list

### Saving the Prediction List


### Testing Suggestion from prediction list with STUPID BACK-OFF

def suggest(previous_tokens, prediction_list, n, rvalues=['']):
    ngram = tuple(previous_tokens)
    p=[]
    e=0
    final=''
    for j in range(n,0,-1):
        predicted_word =prediction_list[j-1].get(ngram,[])
        if predicted_word :
            if ngram==('<unk>',): return select_r(rvalues)
            return predicted_word
        ngram=ngram[1:]
    return select_r(rvalues)

def model_in_use(unicodeloc):
    location=unicodeloc
    # location="en_US.twitter.txt"
    # location="setopatiopinion.txt"
    with open(location, "r", encoding="utf-8") as f:
        data = f.read()


    #1. tokenize the data 
    #2. suffle
    #3. split data into train(80% data) and remaining 20% into test_data
    tokenized_data = get_tokenized_data(data)
    random.seed(87)
    random.shuffle(tokenized_data)
    # print(len(tokenized_data))
    train_size = int(len(tokenized_data) * 0.8)
    # print(train_size)
    train_data = tokenized_data 
    # train_data = tokenized_data[0:train_size]
    test_data = tokenized_data[train_size:]
    # print(train_data)

    # print("{} data are split into {} train and {} test set".format(
    #     len(tokenized_data), len(train_data), len(test_data)))

    # print("First training sample:")
    # print(train_data[0])
        
    # print("First test sample")
    # print(test_data[0])
    
    ### Preprocess the train and test data

    #gives vocabulary/ (closed vocabulary with threshold)
    #      train_data_replaced with <unk> using vocab
    #      test_data_replaced with <unk> using vocab
    train_data_processed, test_data_processed, vocabulary = preprocess_data(train_data, test_data, threshold=1)
    # print("First preprocessed training sample:")
    # print(train_data_processed[0], len(train_data_processed))
    # print()
    # print("First preprocessed test sample:")
    # print(test_data_processed[0],len(test_data_processed))
    # print()
    # print("First 10 vocabulary:")
    # print(vocabulary[0:10])
    # print()
    # print("Size of vocabulary:", len(vocabulary))

    ngram_ftable_list = get_ngram_ftable_list(train_data_processed)
    prediction_list=make_prediction_list(ngram_ftable_list)
    # print(calculate_accuracy(test_data_processed,prediction_list))
    # print(calculate_pp(test_data_processed, ngram_ftable_list, len(vocabulary), k=1.0))
    
    return prediction_list

import json

def generate_model(inputfileloc,ofileloc='user_model.json'):
    ofileloc=r'map\\'+ofileloc
    prediction_list=model_in_use(inputfileloc)
    json_list=[]
    for l in range(4):
        json_tuple_str={}
        for i,k in prediction_list[l].items():
            json_tuple_str[' '.join(i)]=k
        json_list.append(json_tuple_str)

    with open(ofileloc,'w') as f:
        json.dump(json_list,f)
    print('Trained successfully!')

if __name__=="__main__":
    pass
    # generate_model('scrappeddata.txt','pre_model.json')