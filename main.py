
class SimplexTable:
    c=[]
    b=[]
    cannon_form=[]
    Table=[]
    A=[]
    column_indexes=[]
    raw_indexes=[]
    to_min=True
    def init_table(self):
        self.Table=self.copyTable(self.A)
        self.column_indexes=[]
        self.raw_indexes=[]
        f_table=[0]
        for i in range(len(self.c)):
            f_table.append(-self.c[i] if self.to_min else self.c[i])
        self.Table.append(f_table)
        for i in range(len(self.b)):
            self.Table[i].insert(0,self.b[i])
        self.column_indexes=["S0"]
        for i in range(len(self.c)):
            self.column_indexes.append("x"+str(i+1))
        for i in range(len(self.b)):
            self.raw_indexes.append("x"+str(len(self.c)+i+1))
        self.raw_indexes.append("F")
        print("F=",end="")
        for i in range(len(self.c)):
             print(self.c[i],"*",self.column_indexes[i+1],"+",end="",sep="")
        print("0",end='');
        print(" => ", "min" if self.to_min else "max")
        
    def update_table(self,newTable,newB,newC,newTomin):
        self.to_min=newTomin 
        self.b=self.copyList(newB)
        self.c=self.copyList(newC)
        self.A=self.copyTable(newTable)
        self.init_table()
    def __init__(self):
        c=[]
        b=[]
        cannon_form=[]
        Table=[]
        A=[]
        column_indexes=[]
        raw_indexes=[]
        to_min=True
    def init_from_file(self,f,dvoy=False):
        dir_line_no_split=f.readline()
        while(dir_line_no_split=='\n'):
                dir_line_no_split=f.readline()
        dir_line=dir_line_no_split.split()
        if(dir_line[0]=="max"):
            self.to_min=False
        if(dir_line[0]=="min"):
            self.to_min=True
        c_line=f.readline();
        while(c_line=='\n'):
                c_line=f.readline()
        self.c=[float(x) for x in c_line.split()];
        b_line=f.readline();
        while(b_line=='\n'):
                b_line=f.readline()
        self.b=[float(x) for x in b_line.split()];
        for i in range(len(self.b)):
            line=f.readline()
            while(line=='\n'):
                line=f.readline()
            self.A.append([float(x) for x in line.split()])
        
        if dvoy:        
            temp=self.copyList(self.b)
            self.b=self.copyList(self.c,minus=True)
            self.c=self.copyList(temp)
            temp=self.copyTable(self.A)
            self.A=self.Transport(temp,minus=True)
            self.to_min=not self.to_min
        self.init_table()
    def copyTable(self,_Table, minus=False):
       result=[]
       result_line=[]
       for i in range(len(_Table)):
            for j in range(len(_Table[0])):
                if not minus:
                   result_line.append(_Table[i][j])
                else:
                    result_line.append(-_Table[i][j])
            result.append(result_line)
            result_line=[]
       return result
    def copyList(self, _list, minus=False):
        result=[]
        for i in range(len(_list)):
            if not minus:
               result.append(_list[i])
            else:
               result.append(-_list[i])
        return result
    def Transport(self,_Table,minus=False):
       result=[]
       result_line=[]
       for i in range(len(_Table[0])):
            for j in range(len(_Table)):
                if not minus:
                   result_line.append(_Table[j][i])
                else:
                    result_line.append(-_Table[j][i])
            result.append(result_line)
            result_line=[]
       return result
    def printTable(self):
        print("      |",end="");
        for i in self.column_indexes:
            print("%-6s"%i+"|",end="")
        print("")
        for i in range(len(self.column_indexes)+1):
            print("%-6s"%"------"+"|",end="")
        print("")
        for i in range(len(self.raw_indexes)):
            for j in range(len(self.column_indexes)+1):
                if(j==0):
                    print("%-6s"%self.raw_indexes[i]+"|",end="")
                else:
                    print("%-6s"%str(round(self.Table[i][j-1],2))+"|",end="")
            print("")
            for i in range(len(self.column_indexes)+1):
                print("%-6s"%"------"+"|",end="")
            print("")  
    def jardan(self,r,k):
        newTable=self.copyTable(self.Table)
        srk=self.Table[r][k]
        for i in range(len(self.raw_indexes)):
            for j in range(len(self.column_indexes)):
                newTable[i][j]=self.Table[i][j]-self.Table[i][k]*self.Table[r][j]/srk
        for j in range(len(self.column_indexes)):
            newTable[r][j]=self.Table[r][j]/srk
        for j in range(len(self.raw_indexes)):
            newTable[j][k]=-self.Table[j][k]/srk
        newTable[r][k]=1/srk
        
        tmp=self.raw_indexes[r]
        self.raw_indexes[r]=self.column_indexes[k]
        self.column_indexes[k]=tmp
        self.Table=self.copyTable(newTable)
    def isOpornoe(self):
        for i in range(len(self.Table)-1):
            if(self.Table[i][0]<0): 
                return i
        return -1
    def isOptimal(self):
        for i in range(1,len(self.Table[0]),1):
            if self.Table[len(self.Table)-1][i]>0:
                return i
        return -1
    def findRawCol(self,i,raw_col):
        if raw_col=="raw":
            for k in range(1,len(self.Table[i]),1):     
                if self.Table[i][k]<0:
                    min_r=self.Table[i][0]/self.Table[i][k]
                    min_ind=i
                    for l in range(len(self.Table)-1):
                        if self.Table[l][k]>0 and self.Table[l][0]/self.Table[l][k]>=0 and self.Table[l][0]/self.Table[l][k]<min_r:
                            min_r=self.Table[l][0]/self.Table[l][k]
                            min_ind=l
                    return min_ind,k
            return -1,-1
        if raw_col=="col":
            for k in range(len(self.Table)-1):
                if self.Table[k][i]>0:
                    min_r=self.Table[k][0]/self.Table[k][i]
                    min_ind=k
                    for l in range(len(self.Table)-1):
                        if self.Table[l][i]>0 and self.Table[l][0]/self.Table[l][i]>=0 and self.Table[l][0]/self.Table[l][i]<min_r:
                            min_r=self.Table[l][0]/self.Table[l][i]
                            min_ind=l
                    return min_ind,i
                    
            return -1,-1
    def doSimplex(self):
        self.printTable()
        print("")
        Opor=self.isOpornoe()
        while(Opor>=0):
           r,k=self.findRawCol(Opor,"raw")
           if(r>=0):
              self.jardan(r,k)
              
           else:
              print("Нет допустимых решений")
              return None,False,0,0
           Opor=self.isOpornoe()
        Optim=self.isOptimal()
        while(Optim>=0):
          r,k=self.findRawCol(Optim,"col")
          if(r>=0):
                self.jardan(r,k)
                
          else:
                print("Функция не органичена сверху")
                return None,False,0,0
          Optim=self.isOptimal()
        self.printTable()
        print("Найдено оптимальное решение")
        result=self.Table[len(self.Table)-1][0]if self.to_min else -self.Table[len(self.Table)-1][0]
        print("F=",result)
        isInteger=True
        notInteger=0
        LineNum=0
        Value=0
        for h in range(len(self.raw_indexes)-1):
            if(getIntegerIndex(self.raw_indexes[h])<=len(self.c)):
               if not int(self.Table[h][0])==float(self.Table[h][0]):
                  isInteger=False
                  notInteger=self.raw_indexes[h]
                  Value=self.Table[h][0]
               print(self.raw_indexes[h],"=",self.Table[h][0],end=" ")
        for h in range(1,len(self.column_indexes),1):
          if(getIntegerIndex(self.column_indexes[h])<=len(self.c)):
               print(self.column_indexes[h],"=0",end=" ")
        print("")
        return result,isInteger,notInteger,Value
    def printAnswer(self):
        print("Ответ:")
        result=self.Table[len(self.Table)-1][0]if self.to_min else -self.Table[len(self.Table)-1][0]
        print("F=",result)
        for h in range(len(self.raw_indexes)-1):
            if(getIntegerIndex(self.raw_indexes[h])<=len(self.c)):
               print(self.raw_indexes[h],"=",self.Table[h][0],end=" ")
        for h in range(1,len(self.column_indexes),1):
          if(getIntegerIndex(self.column_indexes[h])<=len(self.c)):
               print(self.column_indexes[h],"=0",end=" ")
        print("")
    def check_var_list(self,var):
        result=True
        _sum=0
        for j in range(len(self.A)):
          _sum=0
          for i in range(len(var)):
              _sum+=var[i]*self.A[j][i]
          if _sum>self.b[j]:
              result=False
        return result
    def f(self,var):
        result=0
        for i in range(len(var)):
            result+=self.c[i]*var[i]
        return result
        
    def brute_force(self):
        var=[0 for i in range(len(self.c))]
        result=self.f(var)
        digit=0
        while digit!=-1:
           digit=len(self.c)-2
           while self.check_var_list(var):
                   print(var," F=", self.f(var))
                   if (result<self.f(var) and  not self.to_min) or (result>self.f(var) and  self.to_min):
                        result=self.f(var)
                   var[len(self.c)-1]+=1
                   
           var[len(self.c)-1]=0
           var[digit]+=1
           while not self.check_var_list(var):
                  var[digit]=0
                  digit-=1
                  if digit==-1:
                     break
                  var[digit]+=1
        return result          
             
             
        
def getIntegerIndex(notInteger):
    str_result=notInteger[1:]
    result=int(str_result)
    return result
def Tree(ST):
    global BestF
    global BestST
    result,isInteger,notInteger,Value=ST.doSimplex()
    if(isInteger):
        print("Оптимальное целочисленное решение найдено.")
        exit()
    if(result==None):
        exit()
    print("\n",notInteger,"<=",int(Value))
    niIndex=getIntegerIndex(notInteger)
    newTable=ST.copyTable(ST.A)
    newB=ST.copyList(ST.b)
    newLine=[]
    for i in range(len(ST.c)):
       if (i+1)==niIndex:
          newLine.append(1)
       else:
          newLine.append(0)
    newB.append(int(Value))
    newTable.append(newLine)
    ChildSTleft=SimplexTable()
    ChildSTleft.update_table(newTable,newB,ST.c,ST.to_min)
    
    recurseTree(ChildSTleft)
    newTable=ST.copyTable(ST.A)
    newB=ST.copyList(ST.b)
    newLine=[]
    print("\n",notInteger,">=",int(Value)+1)
    niIndex=getIntegerIndex(notInteger)
    newTable=ST.copyTable(ST.A)
    newB=ST.copyList(ST.b)
    newLine=[]
    for i in range(len(ST.c)):
       if (i+1)==niIndex:
          newLine.append(-1)
       else:
          newLine.append(0)
    newB.append(-int(Value)-1)
    newTable.append(newLine)
    ChildSTRight=SimplexTable()
    ChildSTRight.update_table(newTable,newB,ST.c,ST.to_min)
    recurseTree(ChildSTRight)
def recurseTree(ST):
    global BestF
    global BestST
    result,isInteger,notInteger,Value=ST.doSimplex()
    if(isInteger):
        if (BestF==None):
            BestF=result
            BestST=ST
        if (BestF<result and  not ST.to_min) or (BestF>result and  ST.to_min):
            BestF=result
            BestST=ST
        return
    if(result==None):
        return
    print("\n",notInteger,"<=",int(Value))
    niIndex=getIntegerIndex(notInteger)
    newTable=ST.copyTable(ST.A)
    newB=ST.copyList(ST.b)
    newLine=[]
    for i in range(len(ST.c)):
       if (i+1)==niIndex:
          newLine.append(1)
       else:
          newLine.append(0)
    newB.append(int(Value))
    newTable.append(newLine)
    ChildSTleft=SimplexTable()
    ChildSTleft.update_table(newTable,newB,ST.c,ST.to_min)
    recurseTree(ChildSTleft)
    newTable=ST.copyTable(ST.A)
    newB=ST.copyList(ST.b)
    newLine=[]
    print("\n",notInteger,">=",int(Value)+1)
    newTable=ST.copyTable(ST.A)
    newB=ST.copyList(ST.b)
    newLine=[]
    for i in range(len(ST.c)):
       if (i+1)==niIndex:
          newLine.append(-1)
       else:
          newLine.append(0)
    newB.append(-int(Value)-1)
    newTable.append(newLine)
    ChildSTRight=SimplexTable()
    ChildSTRight.update_table(newTable,newB,ST.c,ST.to_min)
    recurseTree(ChildSTRight)
    
BestST=None
BestF=None
f=open("input.txt",'r')
ST=SimplexTable()
ST.init_from_file(f)
print(str(ST.brute_force()))
Tree(ST)
BestST.printAnswer()
