import Queue
import os
import ast

class Node:
    # A binary tree's node which include character, its frequency and the left and right node children
    def __init__(self,ch, freq, left = None, right = None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right

    def __cmp__(self, other):
        if other == None:
            return -1
        return cmp(self.freq,other.freq)


# Read file
def read_file(path):
    file = open(path,"r")
    result = file.read()
    file.close()
    return result

# Write file
def write_file(path,item):
    file = open(path,"w")
    file.write(item)
    file.close()

# Create a dictionary which contains the character as key, and its frequency as value.
def create_dictionary(s):
    dict = {}
    for ch in s:
        if ch in dict:
            freq = dict[ch]
            dict[ch] = freq + 1
        else:
            dict[ch] = 1
    return dict

# Build a binary tree based on the given dictionary
def build_tree(dict):
    q = Queue.PriorityQueue()
    for key,val in dict.iteritems():
        q.put(Node(key,val))
    while q.qsize() != 1:
        left = q.get()
        right = q.get()
        freq = left.freq + right.freq
        q.put(Node('\0',freq,left,right))
    return q.get()


# Reverse dictionary. Keys will be turned into value and vice versa
def reverse_dict(dict):
    return {value : key for key,value in dict.iteritems()}

# Given a tree and a string, create a dictionary based on Huffman Algorithm
def encode(tree,s,result_dict):
    if tree == None:
        return
    if tree.right == None and tree.left == None:
        result_dict[tree.ch] = s
    encode(tree.left, s + "0", result_dict)
    encode(tree.right,s+"1",result_dict)

# Given an encoded string, and Huffman dictionary, get back the original string
def decode(encode_str, reverse_dict):
    temp = ""
    decode_str = ""
    for ch in encode_str:
        temp = temp + ch
        if temp in reverse_dict:
            decode_str = decode_str + reverse_dict[temp]
            temp = ""
    return decode_str

# Convert a string to binary string
def convert_str_to_bin(s):
    return ''.join(['%08d' % int(bin(ord(i))[2:]) for i in s])


# Decode a string and store all the needed information 
def prepare_str_for_compress(file_str):
    dict = create_dictionary(file_str)
    tree = build_tree(dict)
    dict_new = {}
    encode(tree, "", dict_new)
    temp = ""
    for ch in file_str:
        temp = temp + dict_new[ch]
    num_of_additional_char = 8 - (len(temp) % 8)
    if num_of_additional_char != 8:
        for i in range(num_of_additional_char):
            temp = "0" + temp
    result = ""
    i = 0
    while i < len(temp):
        result = result + chr(int(temp[i:i+8],2))
        i = i + 8
    result = str(num_of_additional_char%8) + "\n" + result
    return str(dict_new) + ".endDictionary!" + result


# Decode a string and turn it back to its original content
def prepare_str_for_decompress(file_str):
    signal = ".endDictionary!"
    index_dict = file_str.find(signal)
    dict = file_str[:index_dict]
    dict = ast.literal_eval(dict)
    num_of_additional = int(file_str[index_dict + len(signal)])
    raw_str = file_str[index_dict+len(signal)+2:]
    raw_str = convert_str_to_bin(raw_str)
    if num_of_additional != 0:
        raw_str = raw_str[num_of_additional:]
    result = decode(raw_str,reverse_dict(dict))
    return result

# Make compression
def compress(target_path,result_path):
    if not os.path.exists(target_path):
        print "Cannot find the file!"
        return
    file_str = read_file(target_path)
    str_compress = prepare_str_for_compress(file_str)
    write_file(result_path,str_compress)


# Make decompression
def decompress(target_path,result_path):
    if not os.path.exists(target_path):
        print "Cannot find the file!"
        return
    file_str = read_file(target_path)
    str_decompress = prepare_str_for_decompress(file_str)
    write_file(result_path,str_decompress)

def displayMenu():
    option = raw_input("Enter 1 for compression and 2 for decompression: ")
    option = int(option)
    if option != 1 and option != 2:
        print "Invalid option."
        return

    target_path = raw_input("Enter file name or the target path: ")
    result_path = raw_input("Enter file name or result path: ")
    if option == 1:
        compress(target_path,result_path)
    else:
        decompress(target_path,result_path)

if __name__ == "__main__":
    displayMenu()
