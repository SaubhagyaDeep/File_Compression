# do again
# video 7 encoded text
# video 9 on padding 

import heapq , os

class BinaryTree:
  def __init__(self,value,frequ):
    self.value=value
    self.frequ=frequ
    self.left=None
    self.right=None

  def __lt__(self,other):
    #less than operator orverloading
    return self.frequ< other.frequ
  
  def __eq__(self,other):
    #equal to operator overloading
    return self.frequ == other.frequ  

class Huffmancode:

  def __init__(self,path):
    self.path=path
    self.__heap=[]
    self.__code={} # contains code for each letter
    self.__reversecode={}

  def __frequency_from_text_(self,text):
    freq_dict={}
    for char in text:
      if char not in freq_dict:
        freq_dict[char]=0
      freq_dict[char]+=1
    return freq_dict

  

  def __Build_heap(self,frequency_dict):
    #creating heap to collect min 2 elements

    for key in frequency_dict:

      frequency=frequency_dict[key]
      binary_tree_node=BinaryTree(key,frequency)
      heapq.heappush(self.__heap,binary_tree_node)

  def __Build_Binary_Tree(self):
    while len(self.__heap)>1:

      binary_tree_node1 = heapq.heappop(self.__heap)
      binary_tree_node2 = heapq.heappop(self.__heap)
      sum_of_freq=binary_tree_node1.frequ+ binary_tree_node2.frequ
      newnode=BinaryTree(None,sum_of_freq)
      newnode.left=binary_tree_node1
      newnode.right=binary_tree_node2
      heapq.heappush(self.__heap,newnode)
    return 

  def __Build_Binary_Tree_Helper(self,root,curr_bits):
    if not root:
      return 
    
    if root.value:  
      # mapping leaf nodes to its bits (a --> 0010)
      self.__code[root.value]=curr_bits 
      self.__reversecode[curr_bits]=root.value
      return

    self.__Build_Binary_Tree_Helper(root.left,curr_bits+'0')
    self.__Build_Binary_Tree_Helper(root.right,curr_bits+'1')
      
  def __Build_Tree_Code(self):
    root=heapq.heappop(self.__heap)
    self.__Build_Binary_Tree_Helper(root,'')

  def __Build_Encoded_Text(self,text):
    encoded_text=''
    for char in text:
      encoded_text+=self.__code[char]
    return encoded_text
  
  def Build_Padded_Text(self,encoded_text):
    padding_value=8- len(encoded_text)%8
    for i in range(padding_value):
      encoded_text+='0'

    padded_info="{0:08b}".format(padding_value)
    padded_text=padded_info+encoded_text
    return padded_text
  
  def __Build_Byte_Array(self,padded_text):
    array=[]
    for i in range(0,len(padded_text),8):
      byte=padded_text[i:i+8]
      array.append(int(byte,2))
    return array
  

  def compression(self):
    print("Compressing the file ...")
# Access the file and extract the text from it 
    filename,file_extension=os.path.splitext(self.path)
    output_path=filename+'.bin'
    with open(self.path, 'r+') as file ,open(output_path,'wb') as output:
      #wb--write in binary
      text=file.read()
      text=text.rstrip()
# calculate the frequency of each text and store it in frequency dict
      frequency_dict=self.__frequency_from_text_(text)

      build_heap=self.__Build_heap(frequency_dict)
# Min heap for 2 minimum frequency
# Construct binary tree from that 

      self.__Build_Binary_Tree()

  # from binary tree Construct code and store in dict 
      self.__Build_Tree_Code()

# Construct encoded text made of 0s and 1s 

      encoded_text=self.__Build_Encoded_Text(text)
#padding of encoded text
      padded_text=self.Build_Padded_Text(encoded_text)

# return the binary file as output
      bytes_array=self.__Build_Byte_Array(padded_text)
      final_bytes=bytes(bytes_array)
      output.write(final_bytes)
    print("the file has been compressed sucessfully :)")
    return output_path

  def __Remove_padding(self,text):
    padded_info=text[:8]
    padding_value= int(padded_info,2)
    text=text[8:]
    text=text[:-1*padding_value]
    return text

  def __Decoded_Text(self,text):
    cur_bits=''
    decoded_text=''
    for char in text:
      cur_bits+=char
      if cur_bits in self.__reversecode:
        decoded_text+=self.__reversecode[cur_bits]
        cur_bits=''
    return decoded_text
  def decompress(self,input_path):
    filename,fileextension= os.path.splitext(input_path)
    output_path= filename+ '_decompressed'+'.txt'
    with open(input_path,'rb') as file, open(output_path,'w') as output:
      bit_string=''
      byte=file.read(1)
      while byte:
        byte=ord(byte)
        bits=bin(byte)[2:].rjust(8,'0')
        bit_string+= bits
        byte=file.read(1)

      text_after_removing_padding=self.__Remove_padding(bit_string)
      actual_text=self.__Decoded_Text(text_after_removing_padding)
      output.write(actual_text)
    return output_path

path=input("enter the path of the file you wanna compress : ")
h = Huffmancode(path)
compressed_file=h.compression()
h.decompress(compressed_file)


