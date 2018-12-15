'''
Created on 4 дек. 2018 г.

@author: al
'''
import sys
import re
import rus_preprocessing_udpipe
from ufal.udpipe import Model, Pipeline

def LemmatizaciaText(FileIsxText,FileLemma):
  output=["1","2"]
  inputput=["1","2"]
  listpusto=["1","2"]
  udpipe_model_url = '/home/al/eclipse-work_cpp/Lingvo/isxDate/udpipe_syntagrus.model'  # URL of the UDPipe model
  print('Loading the model...', file=sys.stderr)
  model = Model.load(udpipe_model_url)
  process_pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
  fileIsh = open(FileIsxText,'r')
  fileLem= open(FileLemma,'w')
  print(FileIsxText, file=sys.stderr)
  print(FileLemma, file=sys.stderr)
  print('Loading the text...', file=sys.stderr)
  
  ishText=fileIsh.read()
  print('Load the text...', file=sys.stderr)
  inputput.clear()
  inputput=ishText.split(" ")
  print(inputput[:30], file=sys.stderr)
  prstr=""
  sstt=""
  pusto=""
  listpusto.clear()
  for kk in inputput:
    output.clear()
    if (kk != pusto):
          res = kk.strip()
          output = rus_preprocessing_udpipe.tag_ud(process_pipeline, text=res)
          if (output != listpusto):
             sstt=output[-1]
            #sstt=re.sub(r'[','',sstt)
             print(sstt, file=sys.stderr)
             prstr += "{} ".format(sstt)  
  fileLem.write(prstr)
  fileLem.close()
  fileIsh.close()


