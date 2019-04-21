import glob
import os
import math
root = ["Corpus\\Input_Data/*","Corpus\\Test_Data/*","Corpus\\Val_Data/*"]
saveroot = ["201433688손민욱/input_Data","201433688손민욱/Test_Feature_Data","201433688손민욱/Val_Feature_Data"]
result_ss=[]  #5000개만 저장
for qwe in range(3):
    save = []
    folders = glob.glob(root[qwe])
    datas = dict()
    for folder in folders:                             #결과 저장할 파일들 경로 저장은 save에 , datas안에는 모든 파일들의 텍스트값들 저장
        file_list = os.listdir(folder)
        file_list_py=[file for file in file_list if file.endswith(".txt")]
        a=0
        for file in glob.glob(folder+"/*.txt"):
            path=file.split('\\')
            path[0]=saveroot[qwe]
            save.append(path[0]+"/"+path[2]+"/"+path[3])
            f=open(file,"r",encoding="UTF8")
            context = f.read()
            datas[file]=context
    n = dict()
    tf=[]
    for key in datas.keys():
        searching = datas[key].split()
        for txt in searching:
            words= txt.split("+")
            for word in words:
                if "NNP" in word or "NNG" in word:
                    if word in n.keys():                              # 모오오오든 텍스트의 몽오옹든 형태소 카운트 및 리스트생성
                        n[word]+=1                                  #형태소가 n에 있으면 카운트1 올리고 ㅇ벗으면 새로 만들고 카운트 1
                    else:                                             #상위 5000개 뽑기위해서 하는 작업
                        n[word]=1
    if(qwe==0):
        result_semi = sorted(n.items(), key=lambda x: (-x[1], x[0]))         #모든 단어의 빈도리스트를 빈도수 기준으로 내림차순 정렬
        for kw in range(5000):
            result_ss.append(result_semi[kw])
        result_ss.sort()                                #상위5000개만 뽑아서 걔네를 다시 가나다 순으로 정렬

    result=dict()                            #이 단어가 몇개의 파일ㄴ=에서 나왔는지를 위한 result
    for k in range(len(result_ss)):
        result[result_ss[k][0]]=0              #0으로 초기화
    sample=result.copy()

    for key in datas.keys():             #idf구하기
        searching = datas[key].split()
        nn = dict()
        for txt in searching:
            words= txt.split("+")
            for word in words:
                if "NNP" in word or "NNG" in word:
                    if word in result.keys():
                        if word in nn.keys():                    #해당문서에서 이미 나온적이 있는단어면 스킵
                            continue
                        else:
                            result[word] +=1                        #해당문서에서 나온적없는단어면 result에서 카운트 올리고 현재 문서에서 나왔던 단어들 저장해놓는 리스트에 저장해서 중복피하기
                            nn[word]=1
    idf=[]
    for j in range(len(result)):
        idf.append(math.log10(1607/(1+int(result[result_ss[j][0]]))))        #연산 끝

    for key in datas.keys():                         #tf
        nnn = sample.copy()
        searching = datas[key].split()
        for txt in searching:
            words= txt.split("+")
            for word in words:
                if "NNP" in word or "NNG" in word:
                    if word in nnn.keys():
                        nnn[word]+=1                                         #5000개 리스트에서 해당 단어가 나오면 그 단어 카운트 1업
        result_tf = nnn.copy()             #
        tf=[]
        for qq in range(len(result_tf)):
            tf.append(math.log10(1+int(result_tf[result_ss[qq][0]])))    #딕셔너리라서 0번째 값 불러오는게 안되서 이렇게 불러옴..

        tf_idf=[]
        print("result_tf: ",result_tf)
        print("idf: ",idf)
        print("tf: ",tf)
        sum=0
        for qq in range(len(tf)):
            tf_idf.append(tf[qq]*idf[qq])
            sum=sum+(tf[qq]*idf[qq])**2    #제곱
        sum=sum**0.5                      #루트
        for qq in range(len(tf_idf)):
            tf_idf[qq]=tf_idf[qq]/sum     #정규화 끝
        print("tf_idf: ",tf_idf)
        file_t = open(save[a], 'w')
        for zz in range(len(tf_idf)):
            file_t.write(str(tf_idf[zz]) + "\t")
        print("a: ",a)
        a+=1