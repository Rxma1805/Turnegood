import re
import os
import jieba
from collections import  Counter

class DataTools:

    def __init__(self):
        self.one_gram_counts="0"
        self.two_gram_counts = "0"
        self.three_gram_counts = "0"
        self.raw_data_path = './database/data/AA/wiki_chs_little'
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
                    dic[line_spli[0]] = line_spli[1]

        return (count,dic)


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
