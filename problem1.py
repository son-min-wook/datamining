import glob
import os
root = "Corpus/Input_Data/*"
folders = glob.glob(root)
datas = dict()
n = dict()
for folder in folders:
    file_list = os.listdir(folder)
    file_list_py=[file for file in file_list if file.endswith(".txt")]
    #print(file_list_py)
    for file in glob.glob(folder+"\*.txt"):
        f=open(file,"r",encoding="UTF8")
        file = open("output.txt",'w')
        context = f.read()
        datas[file]=context
for key in datas.keys():
    searching = datas[key].split()
    for txt in searching:
        words= txt.split("+")
        for word in words:
            if "NNP" in word or "NNG" in word:
                if word in n.keys():
                    n[word]+=1
                else:
                    n[word]=1
result = sorted(n.items(), key=lambda x: (-x[1], x[0]))
for i in range (5009):
    print(result[i][0] +"\t"+ str(result[i][1]))
    file.write(str(result[i][0]) +"\t"+ str(result[i][1])+"\n")