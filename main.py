from math import floor 
class STable:
    def init_table(self):
        self.Table=self.copyTable(self.A)
        self.column_names=[]
        self.raw_names=[]
        f_table=[0]
        for i in range(len(self.c)):
            f_table.append(-self.c[i] if self.orientation else self.c[i])
        self.Table.append(f_table)
        for i in range(len(self.b)):
            self.Table[i].insert(0,self.b[i])
        self.column_names=["S0"]
        for i in range(len(self.c)):
            self.column_names.append("x"+str(i+1))
        for i in range(len(self.b)):
            self.raw_names.append("x"+str(len(self.c)+i+1))
        self.raw_names.append("F")
        print("F=",end="")
        for i in range(len(self.c)):
             print(self.c[i],"*",self.column_names[i+1],"+",end="",sep="")
        print("0",end='');
        print(" => ", "min" if self.orientation else "max")
        
    def update_table(self,newTable,newB,newC,newTomin):
        self.orientation=newTomin 
        self.b=self.copyList(newB)
        self.c=self.copyList(newC)
        self.A=self.copyTable(newTable)
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
    def __init__(self):
        self.c=[]
        self.b=[]
        self.cannon_form=[]
        self.Table=[]
        self.A=[]
        self.column_names=[]
        self.raw_names=[]
        self.orientation=True
    def copyList(self, _list, minus=False):
        result=[]
        for i in range(len(_list)):
            if not minus:
               result.append(_list[i])
            else:
               result.append(-_list[i])
        return result
    def transpon(self,_Table,minus=False):
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
    def init_from_file(self,f,dvoy=False):
        dir_line_no_split=f.readline()
        while(dir_line_no_split=='\n'):
                dir_line_no_split=f.readline()
        dir_line=dir_line_no_split.split()
        if(dir_line[0]=="max"):
            self.orientation=False
        if(dir_line[0]=="min"):
            self.orientation=True
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
            self.A=self.transpon(temp,minus=True)
            self.orientation=not self.orientation
        self.init_table()    
    def printTable(self):
        print("      |",end="");
        for i in self.column_names:
            print("%-6s"%i+"|",end="")
        print("")
        for i in range(len(self.column_names)+1):
            print("%-6s"%"------"+"|",end="")
        print("")
        for i in range(len(self.raw_names)):
            for j in range(len(self.column_names)+1):
                if(j==0):
                    print("%-6s"%self.raw_names[i]+"|",end="")
                else:
                    print("%-6s"%str(round(self.Table[i][j-1],2))+"|",end="")
            print("")
            for i in range(len(self.column_names)+1):
                print("%-6s"%"------"+"|",end="")
            print("")  
    def jardan(self,r,k):
        newTable=self.copyTable(self.Table)
        srk=self.Table[r][k]
        for i in range(len(self.raw_names)):
            for j in range(len(self.column_names)):
                newTable[i][j]=self.Table[i][j]-self.Table[i][k]*self.Table[r][j]/srk
        for j in range(len(self.column_names)):
            newTable[r][j]=self.Table[r][j]/srk
        for j in range(len(self.raw_names)):
            newTable[j][k]=-self.Table[j][k]/srk
        newTable[r][k]=1/srk
        
        tmp=self.raw_names[r]
        self.raw_names[r]=self.column_names[k]
        self.column_names[k]=tmp
        self.Table=self.copyTable(newTable)
    def gomori_method(self,notInteger):
        raw_ind=0
        for h in range(len(self.raw_names)-1):
            if notInteger==self.raw_names[h]:
                  raw_ind=h
        newLine=[]
        for i in range(len(self.column_names)):
            newLine.append(-(self.Table[raw_ind][i]-floor(self.Table[raw_ind][i])))
        self.Table.insert(len(self.raw_names)-1,newLine)
       
        self.raw_names.insert(len(self.raw_names)-1,"x"+str(len(self.raw_names)+len(self.column_names)-1))        
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
    def get_simpl_result(self):
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
        result=self.Table[len(self.Table)-1][0]if self.orientation else -self.Table[len(self.Table)-1][0]
        print("F=",round(result,7))
        isInteger=True
        notInteger=0
        LineNum=0
        Value=0
        for h in range(len(self.raw_names)-1):
            if(getIntegerIndex(self.raw_names[h])<=len(self.c)):
               if not int(round(self.Table[h][0],7))==float(round(self.Table[h][0],7)) and abs(round(self.Table[h][0],7)-floor(round(self.Table[h][0],7)))>Value-floor(Value):
                  isInteger=False
                  notInteger=self.raw_names[h]
                  Value=round(self.Table[h][0],7)
               print(self.raw_names[h],"=",round(self.Table[h][0],7),end=" ")
        for h in range(1,len(self.column_names),1):
          if(getIntegerIndex(self.column_names[h])<=len(self.c)):
               print(self.column_names[h],"=0",end=" ")
        print("")
        return result,isInteger,notInteger,Value
    def printAnswer(self):
        print("Ответ:")
        result=self.Table[len(self.Table)-1][0]if self.orientation else -self.Table[len(self.Table)-1][0]
        print("F=",round(result,13))
        for h in range(len(self.raw_names)-1):
            if(getIntegerIndex(self.raw_names[h])<=len(self.c)):
               print(self.raw_names[h],"=",round(self.Table[h][0],7),end=" ")
        for h in range(1,len(self.column_names),1):
          if(getIntegerIndex(self.column_names[h])<=len(self.c)):
               print(self.column_names[h],"=0",end=" ")
        print("")

   def getIntegerIndex(notInteger):
       str_result=notInteger[1:]
       result=int(str_result)
       return result

f=open("input.txt",'r')
ST=STable()
ST.init_from_file(f)

result,isInteger,notInteger,Value=ST.get_simpl_result()
while not isInteger and result!=None:
   ST.gomori_method(notInteger)
   result,isInteger,notInteger,Value=ST.get_simpl_result()
ST.printAnswer()

