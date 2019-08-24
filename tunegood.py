import re
import os
import jieba
from collections import  Counter

class DataTools:

    def __init__(self):
        self.one_gram_counts="0"
        self.two_gram_counts = "0"
        self.three_gram_counts = "0"
        self.raw_data_path = './database/data/AA/wiki_chs'
        self.chinese_clean_data='./database/data/AA/wiki_chs_clean_sign.txt'
        self.chinese_cut_data = './database/data/AA/wiki_chs_cuts.txt'
        self.wiki_one_gram = './database/data/AA/wiki_chs_one_gram.txt'
        self.wiki_2_gram = './database/data/AA/wiki_chs_2_gram.txt'
        self.wiki_3_gram = './database/data/AA/wiki_chs_3_gram.txt'
        self.error_file = './database/data/AA/error.txt'
        self.cut_list=[]
        self.one_gram_dic = {}
        self.two_gram_dic = {}
        self.three_gram_dic = {}

    def create_cut_file(self):
        count = 1
        with open(self.chinese_cut_data, 'w') as cut_file:
            with open(self.chinese_clean_data, 'w') as save_file:
                with open(self.raw_data_path, 'r') as file_raw_data:
                    while True:
                        try:
                            line = file_raw_data.readline()
                            if not line:
                                break
                            if not line.strip():
                                continue
                            else:
                                words = re.findall('[\u4E00-\u9FA5]', line)
                                if not words:
                                    continue
                                coach = ''.join(words)
                                save_file.writelines(coach)
                                cuts = list(jieba.cut(coach))
                                cut_file.write(' '.join(cuts))
                                self.cut_list += cuts
                                count += 1
                                if count % 100000 == 0:
                                    print(str(count) + ':' + ' '.join(cuts))
                                    count = 0

                        except Exception as e:
                            with open(self.error_file, 'w') as error:
                                error.write(str(e))
                                error.write('\n')

    def get_cut_words_list(self):
        with open(self.chinese_cut_data, 'r') as cut_file:
            while True:
                line = cut_file.readline().strip()
                if not line:
                    break
                if not line.strip():
                    continue
                else:
                    self.cut_list += [word.strip() for word in line.strip().split(' ') if word.strip()]

    def create_one_gram(self):
        count = 1
        with open(self.wiki_one_gram, 'w') as freque_write_file:
            word_counts = Counter(self.cut_list)
            word_len = len(word_counts)
            freque_write_file.write('ALL' + ':' + str(word_len))
            self.one_gram_counts = str(word_len)
            freque_write_file.write('\n')
            for word_count in word_counts.most_common():
                word, count = word_count
                self.one_gram_dic[word] = str(count)
                freque_write_file.write(word + ':' + str(count))
                freque_write_file.write('\n')
                count += 1
                if count % 100000 == 1:
                    print(word + ':' + str(count))
                    count = 1

    def create_2_gram(self):
        count = 1
        with open(self.wiki_2_gram, 'w') as freque_write_file:
            all_2_grams_words = [''.join(self.cut_list[i:i + 2]) for i in range(len(self.cut_list[:-1]))]
            word_counts = Counter(all_2_grams_words)
            word_len = len(word_counts)
            freque_write_file.write('ALL' + ':' + str(word_len))
            self.two_gram_counts = str(word_len)
            freque_write_file.write('\n')
            for word_count in word_counts.most_common():
                word, count = word_count
                self.two_gram_dic[word] = str(count)
                freque_write_file.write(word + ':' + str(count))
                freque_write_file.write('\n')
                count += 1
                if count % 100000 == 1:
                    print(word + ':' + str(count))
                    count = 1

    def create_3_gram(self):
        count = 1
        with open(self.wiki_3_gram, 'w') as freque_write_file:
            all_3_grams_words = [''.join(self.cut_list[i:i + 3]) for i in range(len(self.cut_list[:-2]))]
            word_counts = Counter(all_3_grams_words)
            word_len = len(word_counts)
            freque_write_file.write('ALL' + ':' + str(word_len))
            self.three_gram_counts = str(word_len)
            freque_write_file.write('\n')
            for word_count in word_counts.most_common():
                word, count = word_count
                self.three_gram_dic[word] = str(count)
                freque_write_file.write(word + ':' + str(count))
                freque_write_file.write('\n')
                count += 1
                if count % 100000 == 1:
                    print(word + ':' + str(count))
                    count = 1

    def Run(self):
        self.cut_list=[]
        print('loading')
        if not os.path.exists(self.chinese_cut_data):
            self.create_cut_file()
        print('create_cut_file  had done!')
        if not self.cut_list:
            print('get cut_list  is doing!')
            self.get_cut_words_list()
        print('get cut_list is done,getting wiki_one_gram')
        if not os.path.exists(self.wiki_one_gram):
            self.create_one_gram()
        if not self.one_gram_dic:
            self.one_gram_counts,self.one_gram_dic = self.get_n_gram_dic(self.wiki_one_gram)
        print('geting wiki_2_gram')
        if not os.path.exists(self.wiki_2_gram):
            self.create_2_gram()
        if not self.two_gram_dic:
            self.two_gram_counts, self.two_gram_dic = self.get_n_gram_dic(self.wiki_2_gram)
        print('geting wiki_3_gram')
        if not os.path.exists(self.wiki_3_gram):
            self.create_3_gram()
        if not self.three_gram_dic:
            self.three_gram_counts, self.three_gram_dic = self.get_n_gram_dic(self.wiki_3_gram)

        self.one_r_count_list = Counter(dataTool.one_gram_dic.values())
        self.one_N = sum([int(r) * self.ge_N_r(r,"1") for r in self.one_r_count_list])
        self.two_r_count_list = Counter(dataTool.two_gram_dic.values())
        self.two_N = sum([int(r) * self.ge_N_r(r, "2") for r in self.two_r_count_list])
        self.three_r_count_list = Counter(dataTool.three_gram_dic.values())
        self.three_N = sum([int(r) * self.ge_N_r(r, "3") for r in self.three_r_count_list])



        print('done')

    def get_n_gram_dic(self,file_name):
        dic={}
        count="0"
        with open(file_name,'r') as freque_file:
            while True:
                line = freque_file.readline()
                if not line:
                    break
                if not line.strip():
                    continue
                else:
                    line_spli = line.strip().split(':')
                    if line_spli[0] == 'ALL':
                        count = line_spli[1]
                        continue
                    dic[line_spli[0]] = line_spli[1]

        return (count,dic)

    def get_n_tuning_probability(self,word,n):
        if n == 1:
            if word in self.one_gram_dic:
                r = int(self.one_gram_dic[word])
                pb = (r+1) / self.one_N * self.ge_N_r(r+1,'1') /self.ge_N_r(r,'1')
                return pb if pb != 0 else self.ge_N_r(r,'1')/self.one_N
            else:
                #return self.ge_N_r(1,'1')/self.one_N
                return 1/len(self.one_gram_dic)

        elif n == 2:
            if word in self.two_gram_dic:
                r = int(self.two_gram_dic[word])
                pb = (r + 1) / self.two_N * self.ge_N_r(r + 1,'2') / self.ge_N_r(r,'2')
                return pb if pb != 0 else self.ge_N_r(r, '2') / self.two_N
            else:
                #return self.ge_N_r(1,'2')/self.two_N
                return 0

        elif n == 3:
            if word in self.three_gram_dic:
                r = int(self.three_gram_dic[word])
                pb = (r + 1) / self.three_N * self.ge_N_r(r + 1,'3') / self.ge_N_r(r,"3")
                return pb if pb != 0 else self.ge_N_r(r, '3') / self.three_N
            else:
                #return self.ge_N_r(1,'3')/self.three_N
                return 0


    def get_one_dic(self):
        return self.one_gram_dic

    def get_2_dic(self):
        return self.two_gram_dic

    def get_3_dic(self):
        return self.three_gram_dic

    def get_len_one_gram(self):
        return self.one_gram_counts

    def get_len_two_gram(self):
        return self.two_gram_counts

    def get_len_three_gram(self):
        return self.three_gram_counts


    def ge_N_r(self,r, n):
        if n == "1":
            #出现次数为r的个数
            if str(r) in self.one_r_count_list:
                return self.one_r_count_list[str(r)]
            else:
                return 0
        elif n == "2":
            if str(r) in self.two_r_count_list:
                return self.two_r_count_list[str(r)]
            else:
                return 0
        elif n == "3":
            if str(r) in self.three_r_count_list:
                return self.three_r_count_list[str(r)]
            else:
                return 0
        else:
            return


    def get_prob(self,word):  # P(w1)
        return self.get_n_tuning_probability(word,1)


    def get_combination_prob(self,w1, w2):
        pr = self.get_n_tuning_probability(w1+w2,2)
        #return pr
        return pr if pr != 0 else self.get_prob(w1)*self.get_prob(w2)

    def get_three_combination_prob(self,w1, w2, w3):
        pr = self.get_n_tuning_probability(w1 + w2+w3, 3)
        #return pr
        return pr if pr != 0 else self.get_n_tuning_probability(w3, 1) * self.get_combination_prob(w1, w2)

    def get_prob_2_gram(self,w1, w2):  # P(w2|w1)
        return self.get_combination_prob(w1, w2) / self.get_prob(w1)

    def get_prob_3_gram(self,w1, w2, w3):  # P(w3|w1w2)
        return self.get_three_combination_prob(w1, w2, w3) / self.get_combination_prob(w1, w2)

    def language_model_of_1(self,sentence):
        probability = 1
        word_list = list(jieba.cut(sentence))
        for i, word in enumerate(word_list):
            probability *= self.get_prob(word)
            print(word, probability)
        return probability


    def language_model_of_2(self,sentence):
        probability = 1
        word_list = list(jieba.cut(sentence))
        for i, word in enumerate(word_list):
            if i == 0:
                probability *= self.get_prob(word)
                print(word,probability)
            else:
                pre_word = word_list[i - 1]
                probability *= self.get_prob_2_gram(pre_word, word)
                print(pre_word,word, probability)

        return probability

    def language_model_of_3(self,sentence):
        probability = 1
        word_list = list(jieba.cut(sentence))
        for i, word in enumerate(word_list):
            if i == 0:
                probability *= self.get_prob(word)
                print(word,probability)
            elif i == 1:
                pre_word = word_list[i - 1]
                probability *= self.get_prob_2_gram(pre_word, word)
                print(pre_word,word, probability)
            else:
                pr_n_2_word = word_list[i - 2]
                pr_n_1_word = word_list[i - 1]
                probability *= self.get_prob_3_gram(pr_n_2_word, pr_n_1_word, word)
                print(pr_n_2_word, pr_n_1_word,word, probability)
        return probability

dataTool = DataTools()
dataTool.Run()

need_compared = [
    "明天晚上请你吃大餐 今天晚上请你吃大餐",
    "我们一起吃日料 我们一起吃苹果",
    "今天晚上请你吃大餐,我们一起吃日料 明天晚上请你吃大餐,我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "今晚我去吃火锅 今晚火锅去吃我",
    "洋葱奶昔来一杯 养乐多绿来一杯"
]

for s in need_compared:
    s1, s2 = s.split()

    print(list(jieba.cut(s1)))
    print(list(jieba.cut(s2)))

    p1, p2 = dataTool.language_model_of_3(s1), dataTool.language_model_of_3(s2)

    better = s1 if p1 > p2 else s2

    print('{} is more possible'.format(better))
    print('-' * 4 + ' {} with probility {}'.format(s1, p1))
    print('-' * 4 + ' {} with probility {}'.format(s2, p2))


