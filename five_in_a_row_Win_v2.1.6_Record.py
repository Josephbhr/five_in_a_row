import tkinter as tk 
from tkinter import ttk  
import random
import re 
import time
import copy
import os
import ast
import sys
import numpy
import math

def center(windowwidth,windowheight,window):
        screenwidth=window.winfo_screenwidth()
        screenheight=window.winfo_screenheight()
        return "{0:}x{1:}+{2:}+{3:}".format(windowwidth\
                ,windowheight,(screenwidth-windowwidth)//2,\
                (screenheight-windowheight)//2)


def start():
        global start_window,modeflag,chess_record_file
        if getattr(sys, 'frozen', False):
                chess_record_path=os.path.dirname(sys.executable)+"/Chess_Record.txt"

        elif __file__:
                chess_record_path=os.path.dirname(__file__)+"/Chess_Record.txt"
        
        
        chess_record_file=open(chess_record_path,mode="a+")
        

        start_window=tk.Tk()
        start_window.title("五子棋")
        start_window.geometry(center(710,500,window=start_window))
        #start_window.config(background="#FFCC99")
        start_label=tk.Label(start_window,text="五子棋",font=("Times New Roman",32),fg="#FF9900",width=15,height=2)
        start_label.grid(column=1,row=0)
        
        modeflag=0
        h_vs_h_button=tk.Button(start_window,text="双人模式",font=("Times New Roman",17),command=lambda: [start_window.destroy(),start_h_vs_h()]\
                ,width=11,height=3)
        h_vs_h_button.grid(column=0,row=1,padx=7,pady=50)
        h_vs_c_button=tk.Button(start_window,text="人机模式",font=("Times New Roman",17),command=lambda: start_h_vs_c_config(start_window)\
                ,width=11,height=3)
        h_vs_c_button.grid(column=2,row=1,padx=7,pady=50)
        review_mode_button=tk.Button(start_window,text="棋谱记录",font=("Times New Roman",17),command=lambda: [start_window.destroy(),start_record_review()]\
                ,width=11,height=3)
        review_mode_button.grid(column=1,row=2,padx=7,pady=50)
        
        start_window.mainloop()
        


        ##############################双人模式主窗口#####################################################   
                  
def start_h_vs_h():
        global BoardCanvas,root_window
        global winnersign,turnsign,ChessPosition
        global retrieve_button,Re_Position
        global modeflag,chess_record_sign
        
        chess_record_sign=""
        modeflag="hh"
        winnersign=0
        turnsign=1
        ChessPosition=[]
        Re_Position=[]
       
       
        
        for i in range(15):
                ChessPosition.append([0]*15)

                
        root_window=tk.Tk()
        root_window.protocol("WM_DELETE_WINDOW",root_window_state)

        BoardCanvas=tk.Canvas(root_window,width=500,height=500,bg="Sandy Brown")
        BoardCanvas.grid(row=0,column=0,rowspan=10)

        for i in range (15):
                BoardCanvas.create_line(26,32*i+26,474,32*i+26)
        for j in range (15):
                BoardCanvas.create_line(32*j+26,26,32*j+26,474)
        #draw the board lines
        pointlist=[(3,3),(11,3),(7,7),(3,11),(11,11)]
        for i in range(5):
                for j in pointlist:
                        BoardCanvas.create_oval(26+j[0]*32-3,26+j[1]*32-3,26+j[0]*32+3,26+j[1]*32+3,fill="black")   
        #draw the black points  
          
        root_window.title("五子棋 双人模式")
        root_window.geometry(center(710,500,window=root_window))
        
        BoardCanvas.bind("<Button-1>",clickmonitor)
        retrieve_button=tk.Button(root_window,text="悔棋",font=("Times New Roman",20),\
                width=12,height=3,command=lambda: retrieve_correct())
        retrieve_button.grid(row=3,column=1,padx=8) 
        Again_button=tk.Button(root_window,text="再来一局",font=("Times New Roman",20),\
                width=12,height=3,command=lambda: [root_window.destroy(),start_h_vs_h()])
        Again_button.grid(row=5,column=1,padx=8)
        root_window.mainloop()

        
def start_record_review():
        global modeflag,review_BoardCanvas,root_window,review_turnsign,last_button,next_button,review_BoardCanvas,review_turnsign,record_select_combobox\
        ,chess_record_reader,winner_label

        modeflag="review"
        chess_record_reader={} 
        # define a dictionary to create the key-value pair of time-chess_record(One line in the txt file)
        chess_record_file.seek(0,0)

        # point to the first line of .txt file
        for i in chess_record_file.readlines():
                chess_record_reader[i[0:24]]=[i[25:28]]
                for j in ast.literal_eval(i[29:]):
                        if type(j)==int:
                                chess_record_reader[i[0:24]].append(ast.literal_eval(i[29:]))
                                break
                        # avoid the exception: only one position (7,7) -> for j in (7,7): -> 7 and 7
                        
                        chess_record_reader[i[0:24]].append(j)
        
        # ast.literal_eval convert the strings in .txt into list[tuple] safely 
        # print(chess_record_reader)
        root_window=tk.Tk()
        root_window.title("五子棋 棋谱记录")
        root_window.geometry(center(710,500,window=root_window))
        
        review_BoardCanvas=tk.Canvas(root_window,width=500,height=500,bg="Sandy Brown")
        review_BoardCanvas.grid(row=0,column=0,rowspan=10)

        for i in range (15):
                review_BoardCanvas.create_line(26,32*i+26,474,32*i+26)
        for j in range (15):
                review_BoardCanvas.create_line(32*j+26,26,32*j+26,474)
        #draw the board lines

        pointlist=[(3,3),(11,3),(7,7),(3,11),(11,11)]
        for i in range(5):
                for j in pointlist:
                        review_BoardCanvas.create_oval(26+j[0]*32-3,26+j[1]*32-3,26+j[0]*32+3,26+j[1]*32+3,fill="black")   
        #draw the black points  
        

        winner_label=tk.Label(root_window,text="胜者",font=("Times New Roman",20),\
                width=14,height=3)
        winner_label.grid(row=1,column=1,padx=8,pady=8) 
        
        last_button=tk.Button(root_window,text="上一步",font=("Times New Roman",20),\
                width=12,height=3,command=lambda: review_last(Re_Position),state="disabled")
        last_button.grid(row=2,column=1,padx=8,pady=8) 
        next_button=tk.Button(root_window,text="下一步",font=("Times New Roman",20),\
                width=12,height=3,command=lambda: review_next(Re_Position))
        next_button.grid(row=3,column=1,padx=8,pady=8) 

        return_main_button=tk.Button(root_window,text="回到主页面",font=("Times New Roman",20),\
                width=12,height=3,command=lambda: [root_window.destroy(),start()])
        return_main_button.grid(row=4,column=1,padx=8,pady=8)

        record_select_combobox=ttk.Combobox(root_window)
        record_select_combobox.grid(row=0,column=1,padx=8,pady=8)
        record_select_combobox["state"]="readonly"
        record_select_combobox["value"]=list(chess_record_reader.keys())
        record_select_combobox.current(len(chess_record_reader)-1)
        refresh_key=record_select_combobox.get()
        review_winner=chess_record_reader[refresh_key][0]       # [chess_record_reader[refresh_key][0] refers to the winner of the searched record
        
        if review_winner[0:2]=="hh":
                if review_winner[2]=="0":
                        winner_label["text"]="未结束(双人)"     
                elif review_winner[2]=="1":
                        winner_label["text"]="黑棋胜局(双人)"
                elif review_winner[2]=="2":
                        winner_label["text"]="白棋胜局(双人)"
        elif review_winner[0:2]=="hc":
                if review_winner[2]=="0":
                        winner_label["text"]="未结束(人机)"
                elif review_winner[2]=="1":
                        winner_label["text"]="黑棋胜局(人机)"
                elif review_winner[2]=="2":
                        winner_label["text"]="白棋胜局(人机)"

        
        
        Re_Position=chess_record_reader[refresh_key][1:]
        
        review_turnsign=-1     # set the index to the beginning of Re_Position 


        
        record_select_combobox.bind('<<ComboboxSelected>>',record_find)
        root_window.mainloop()

def record_find(event):

        global review_turnsign,review_BoardCanvas,Re_Position,last_button,next_button
        review_BoardCanvas.delete("chess") # clear the chess in a previous record
        review_turnsign=-1  

        refresh_key=record_select_combobox.get()
        review_winner=chess_record_reader[refresh_key][0]       # [chess_record_reader[refresh_key][0] refers to the winner of the searched record
        
        if review_winner[0:2]=="hh":
                if review_winner[2]=="0":
                        winner_label["text"]="未结束(双人)"     
                elif review_winner[2]=="1":
                        winner_label["text"]="黑棋胜局(双人)"
                elif review_winner[2]=="2":
                        winner_label["text"]="白棋胜局(双人)"
        elif review_winner[0:2]=="hc":
                if review_winner[2]=="0":
                        winner_label["text"]="未结束(人机)"
                elif review_winner[2]=="1":
                        winner_label["text"]="黑棋胜局(人机)"
                elif review_winner[2]=="2":
                        winner_label["text"]="白棋胜局(人机)"


        Re_Position=chess_record_reader[refresh_key][1:]        # regain the time stamp of the target record

        last_button=tk.Button(root_window,text="上一步",font=("Times New Roman",20),\
                width=12,height=3,command=lambda: review_last(Re_Position),state="disabled")
        last_button.grid(row=2,column=1,padx=8,pady=8) 
        next_button=tk.Button(root_window,text="下一步",font=("Times New Roman",20),\
                width=12,height=3,command=lambda: review_next(Re_Position))
        next_button.grid(row=3,column=1,padx=8,pady=8) 
        
        
        
########################人机主窗口################################        
def start_h_vs_c_config(window):

        global chess_select,modeflag,chess_record_sign
        chess_record_sign=""
        modeflag="hc"
        chess_select=tk.Toplevel(window)
        chess_select.grab_set()
        # modelling the configuration window
        chess_select.title("执方选择")
        chess_select.attributes("-topmost",True)
        chess_select.protocol("WM_DELETE_WINDOW",callback)
        chess_select.geometry(center(300,200,window=chess_select))
        chess_select_label=tk.Label(chess_select,text="请选择你的执方",font=("Times New Roman",30))
        chess_select_label.grid(row=0)
        gamersign=tk.IntVar()
        gamersign.set(1)
        Black_h=tk.Radiobutton(chess_select,text="黑方",font=("Times New Roman",20),variable=gamersign,value=1)
        Black_h.grid()
        White_h=tk.Radiobutton(chess_select,text="白方",font=("Times New Roman",20),variable=gamersign,value=2)
        White_h.grid()
        chess_select_confirm=tk.Button(chess_select,text="确认",font=("Times New Roman",20),command=lambda: [window.destroy(),\
                start_h_vs_c(gamersign.get())])
        chess_select_confirm.grid()
        chess_select.mainloop()



def start_h_vs_c(gamersign):
        
        '''
        Method: fundamental rules of five_in_a_row

        '''
        global BoardCanvas,root_window
        global winnersign,turnsign,ChessPosition
        global retrieve_button,Re_Position
        global compsign
        global root_window_open
        global time_AI_label,time_list
        
        time_AI=0
        root_window_open=1
        compsign=3-gamersign
        

        
        
        winnersign=0
        turnsign=1
        ChessPosition=[]
        Re_Position=[]
        time_list=[]

        #compsign represents the color of chess 
        # that the computer should hold
       
        
        for i in range(15):
                ChessPosition.append([0]*15)
      

        root_window=tk.Tk()
        root_window.protocol("WM_DELETE_WINDOW",root_window_state)
        

        BoardCanvas=tk.Canvas(root_window,width=500,height=500,bg="Sandy Brown")
        BoardCanvas.grid(row=0,column=0,rowspan=10)

        for i in range (15):
                BoardCanvas.create_line(26,32*i+26,474,32*i+26)
        for j in range (15):
                BoardCanvas.create_line(32*j+26,26,32*j+26,474)
        #draw the board lines
        pointlist=[(3,3),(11,3),(7,7),(3,11),(11,11)]
        for i in range(5):
                for j in pointlist:
                        BoardCanvas.create_oval(26+j[0]*32-3,26+j[1]*32-3,26+j[0]*32+3,26+j[1]*32+3,fill="black")   
        #draw the black points  
          
        root_window.title("五子棋 人机模式")
        root_window.geometry(center(710,500,window=root_window))
        
        BoardCanvas.bind("<Button-1>",clickmonitor)
        
        time_AI_label=tk.Label(root_window,text="运算时间为{}".format(time_AI),font=("Times New Roman",20),\
                width=14,height=3)
        time_AI_label.grid(row=1,column=1,padx=8)
       
        retrieve_button=tk.Button(root_window,text="悔棋",font=("Times New Roman",20),\
               width=12,height=3,command=lambda: retrieve_correct())
        retrieve_button.grid(row=3,column=1,padx=8) 

        '''
        人机悔棋待定
        '''
        Again_button=tk.Button(root_window,text="再来一局",font=("Times New Roman",20),\
                width=12,height=3,command=lambda: start_h_vs_c_config(root_window))
        Again_button.grid(row=5,column=1,padx=8)
        
        ######################################
        
        while(root_window_open):
                
                try:

                        comp_ruledriven()
                        root_window.update()
                except:
                        break
                        
             
                         

        ######################################
        
        
        
                
def comp_ruledriven():
        
        '''
        Attempt to find the better position for comp
        '''


        
        #print("Optimization begins now!")



        global turnsign,ChessPosition,Re_Position,BoardCanvas,retrieve_button,Pruns,leaf_node_count,total_node
        



        openrandx=0
        openrandy=0
        
        if turnsign!=compsign:
                return 
        else:   
                start_time=time.time()
                Pruns=0
                leaf_node_count=0
                total_node=0
                #BoardCanvas.unbind("<Button-1>")
                #retrieve_button.config(state="disabled")
                
                
                if len(Re_Position)==0 and compsign==1:  
                        #openrandx=random.randint(-1,1)
                        #openrandy=random.randint(-1,1)
                        
                        ChessPosition[7][7]=1
                        Re_Position.append((7,7))
                        drawchess(7,7)

                elif len(Re_Position)==1 and compsign==2:
                        openrandx=random.randint(Re_Position[0][0]-1,Re_Position[0][0]+1)
                        openrandy=random.randint(Re_Position[0][1]-1,Re_Position[0][1]+1)

                        while (openrandx,openrandy)==Re_Position[0] or openrandx<0 or openrandx>14 or openrandy<0 or openrandy>14:
                            openrandx=random.randint(Re_Position[0][0]-1,Re_Position[0][0]+1)
                            openrandy=random.randint(Re_Position[0][1]-1,Re_Position[0][1]+1)          
                                
                                
                        ChessPosition[openrandx][openrandy]=2
                        Re_Position.append((openrandx,openrandy))
                        drawchess(openrandx,openrandy)
                              
                else:   
                        
                        

                        optimalx,optimaly=treebuild(tree_depth=3)

                        print("AI puts chess on: ({},{})".format(optimalx,optimaly))

                        ChessPosition[optimalx][optimaly]=compsign
                        Re_Position.append((optimalx,optimaly))
                        drawchess(optimalx,optimaly)
                
                
                end_time=time.time()
                print("Pruning times:",Pruns)
                print("Number of leaf_nodes:",leaf_node_count)
                print("Number of total_nodes:",total_node)
                print("Number of non_leaf_nodes:",total_node-leaf_node_count)

                time_AI=end_time-start_time
                time_list.append((float(format(time_AI,".2f")),float(format((1000*time_AI+1)/(total_node+1),".2f"))))
                
                #record the entire time for one step(s)
                #record the frequency (ms/number of leaf_node)

                time_AI_label.config(text="运算时间:{:.2f}s".format(time_AI))

                if len(Re_Position)>=9:    
                        winnersign=winnerjudge(judge_x=optimalx,judge_y=optimaly)        
                        result_report(winnersign)


                turnsign=3-compsign 

                #retrieve_button.config(state="normal")
                #BoardCanvas.bind("<Button-1>",clickmonitor)
                
                #BoardCanvas.bind("<Button-1>",clickmonitor)
        



def treebuild(tree_depth=3):

          
        # the root node is one possible position for COMPUTER
        # In this case（odd number of depth）, the leaf nodes are still computer(i.e. MAX layer) 

        search_square()
        # obtain the search square
        alarm_dict={"huosi_AI":[],"chongsi_AI":[],"huosi_human":[],"chongsi_human":[],"danhuosan_AI":[],"tiaohuosan_AI":[],"danhuosan_human":[],"tiaohuosan_human":[]}
        # ordered based on priority(decreasing
        


        for all_position in warning_list: 
                temp_key,alarm_shift=chess_slicing(break_list=[all_position],slicing_flag="alarm")
                if temp_key!="ORDINARY":
                        alarm_dict[temp_key].append([all_position,alarm_shift])
        
        
        for alarms in alarm_dict.keys():

                if len(alarm_dict[alarms])>0:
                        print("Alarm Type(First priority): ",alarms)
                        
                        if alarms=="chongsi_AI" or alarms=="chongsi_human" or alarms=="tiaohuosan_AI" or alarms=="tiaohuosan_human"\
                                or alarms=="danhuosan_AI" or alarms=="danhuosan_human":
                               
                                alarm_dir=((alarm_dict[alarms][0])[1])[0]
                                offset=((alarm_dict[alarms][0])[1])[1]
                                alarm_x=((alarm_dict[alarms][0])[0])[0]
                                alarm_y=((alarm_dict[alarms][0])[0])[1]
                                
                                if alarm_dir=="left":
                                        return (alarm_x-offset,alarm_y)
                                elif alarm_dir=="right":
                                        return (alarm_x+offset,alarm_y)
                                elif alarm_dir=="up":
                                        return (alarm_x,alarm_y-offset)
                                elif alarm_dir=="down":
                                        return (alarm_x,alarm_y+offset)
                                elif alarm_dir=="topleft":
                                        return (alarm_x-offset,alarm_y-offset)
                                elif alarm_dir=="bottomright":
                                        return (alarm_x+offset,alarm_y+offset)
                                elif alarm_dir=="topright":
                                        return (alarm_x+offset,alarm_y-offset)
                                elif alarm_dir=="bottomleft":
                                        return (alarm_x-offset,alarm_y+offset)
                                
                        else:    
                                return (alarm_dict[alarms][0])[0]
                        
                        #use the first one that is of the first priority(alarm_dict[alarms][0]): [(alarm_x,alarm_y),["direction",offset]]
                        #(alarm_x,alarm_y) is (alarm_dict[alarms][0])[0]
        

        ## warning mechanism ##
        ## first priority ##

        target_dict={}
        # record the trees based on root node(unique)

        #mock_Position=copy.deepcopy(ChessPosition)
        #must use DEEPCOPY
        for legal_position in legal_list:  
                target_dict[legal_position]=treeviewer(depth=tree_depth-1,alpha=-50000000,beta=50000000,mock_list=[legal_position])
        print("AI待选落子位置:",target_dict)

        temp_max=max(target_dict.values())
        break_list=[]
        for targets in target_dict.keys():
                if temp_max-target_dict[targets]<=1000:
                        break_list.append(targets)


        return chess_slicing(break_list)




def treeviewer(depth,mock_list,alpha,beta):
        global Pruns,leaf_node_count,total_node
        if depth==0:
                leaf_node_count+=1
                return board_slicing(mock_list)
        
        
        '''
        if depth%2!=0:    #Max Layer for comp
                mock_Position[x][y]=compsign
        else:                      #Min Layer for human(mock)
                mock_Position[x][y]=3-compsign
        '''
        
        if depth%2!=0:    #Max Layer for comp(Not the leaf layer)
                
                node_value=-500000000 

        else:                      #Min Layer for human(mock)
               
                node_value=500000000

        
        #legal_list=search_square(flag="position")
        
        for legal_position in legal_list:   
                if legal_position not in mock_list:
                        
                        mock_list.append(legal_position)
                        total_node+=1
                        if depth%2!=0:  #Max Layer for comp(Not the leaf layer)
                                
                                temp_score=treeviewer(depth-1,mock_list,max(node_value,alpha),beta)
                        
                        else:
                                temp_score=treeviewer(depth-1,mock_list,alpha,min(node_value,beta))
                        
                        
                else:
                        continue 

                del mock_list[-1]
                
#################################An test for pruning#################################

                if depth%2!=0:    #Max Layer for comp(Not the leaf layer)
                
                        if temp_score>node_value:
                                
                                node_value=temp_score
                                
                        if int(math.exp(min(node_value/10000,10)))+7000>abs(beta):
                                Pruns+=1
                                break
                        

                else:                      #Min Layer for human(mock)
                        
                        if temp_score<node_value:
                                
                                node_value=temp_score
                                
                        if int(numpy.log(abs(node_value)+1))-7000<abs(alpha):
                                Pruns+=1
                                #print("Prun successfully!")
                                break
                
        return node_value
               
        

def search_square():
        '''
        process the legal positions as a list for AI
        '''
        
        global pivot_min,scope,legal_list,warning_list
        
        legal_list=[]
        warning_list=[]
        mock_Re_Position=Re_Position[:]
        x_max=max(mock_Re_Position,key= lambda x:x[0])[0]
        x_min=min(mock_Re_Position,key= lambda x:x[0])[0]
        y_max=max(mock_Re_Position,key= lambda y:y[1])[1]
        y_min=min(mock_Re_Position,key= lambda y:y[1])[1]
        scope=max(x_max-x_min+2,y_max-y_min+2)

    
        
        if x_min<1:
                x_min=1
        if y_min<1:
                y_min=1

        pivot_min=(x_min-1,y_min-1)


        if pivot_min[0]+scope>14 or pivot_min[1]+scope>14:
                scope=min(14-pivot_min[0],14-pivot_min[1])
                
        # in case of the range out of board    
        
        


        
        for x in range(pivot_min[0],pivot_min[0]+scope+1):
                for y in range(pivot_min[1],pivot_min[1]+scope+1):
                        
                        if ChessPosition[x][y]==0: 
                                        
                # check if the surrounding chesses of target root node(AI's first Chess) are empty
                # check radius: 1
                                
                                surrounding_check=0
                                for r in range(1,2):
                                        if x-r>=0:
                                                if ChessPosition[x-r][y]!=0:
                                                        surrounding_check+=1
                                                        break
                                        if x+r<=14:
                                                if ChessPosition[x+r][y]!=0:
                                                        surrounding_check+=1
                                                        break
                                        if y-r>=0:
                                                if ChessPosition[x][y-r]!=0:
                                                        surrounding_check+=1 
                                                        break
                                        if y+r<=14:
                                                if ChessPosition[x][y+r]!=0:
                                                        surrounding_check+=1 
                                                        break
                                        if x-r>=0 and y-r>=0:
                                                if ChessPosition[x-r][y-r]!=0:
                                                        surrounding_check+=1 
                                                        break
                                        if x+r<=14 and y+r<=14:
                                                if ChessPosition[x+r][y+r]!=0:
                                                        surrounding_check+=1 
                                                        break
                                        if x+r<=14 and y-r>=0:
                                                if ChessPosition[x+r][y-r]!=0:
                                                        surrounding_check+=1 
                                                        break
                                        if x-r>=0 and y+r<=14:
                                                if ChessPosition[x-r][y+r]!=0:
                                                        surrounding_check+=1 
                                                        break
                                
                                if surrounding_check>0:    
                          
                                        legal_list.append((x,y))

        for x in range(0,15):
                for y in range(0,15):  
                        if ChessPosition[x][y]==0:        
                                warning_list.append((x,y))             
        
        
def board_slicing(mock_list):
        #search_square(flag="square")

        '''
        The method used for slicing is not the same for row/column and diagonal
                #slicing_flag: "normal"->put the mock chesses (used in tree)
                #slicing_flag: "alarm" ->without mock chesses
        
        '''
        
       
        chess_slice={"left":[],"right":[],"up":[],"down":[],"topleft":[],"bottomright":[],"topright":[],"bottomleft":[]}
        # record the slices in four directions



        mock_Position=copy.deepcopy(ChessPosition)
        # deepcopy must be used in case of the "mock chess" is recorded in the "real" board

        # mock the process of putting chess
        

        for pos in range(len(mock_list)):

                if pos%2==0:  # chess for comp
                        mock_Position[(mock_list[pos])[0]][(mock_list[pos])[1]]=compsign
                else: 
                        mock_Position[(mock_list[pos])[0]][(mock_list[pos])[1]]=3-compsign
        
        

        for x in range(len(mock_Position)):
                for y in range(len(mock_Position[x])):
                        mock_Position[x][y]=str(mock_Position[x][y])

        ## format: [((x1,x2),(y1,y2)),((x2,x3),(y2,y3)),((x3,x4),(y3,y4))] 
        #  left side included but right side excluded

        if scope//6==2: # 12<=scope<=14
                cut_point=[((pivot_min[0],pivot_min[0]+6),(pivot_min[1],pivot_min[1]+6)),\
                        ((pivot_min[0]+6,pivot_min[0]+12),(pivot_min[1]+6,pivot_min[1]+12))]
               
                if (scope+1)%6>1:
                        cut_point.append(((pivot_min[0]+12,pivot_min[0]+12+((scope+1)%6)),\
                                (pivot_min[1]+12,pivot_min[1]+12+((scope+1)%6))))
                       
        elif scope//6==1:# 6<=scope<12
                cut_point=[((pivot_min[0],pivot_min[0]+6),(pivot_min[1],pivot_min[1]+6))]
                
                if (scope+1)%6>1:
                        cut_point.append(((pivot_min[0]+6,pivot_min[0]+6+((scope+1)%6)),\
                                (pivot_min[1]+6,pivot_min[1]+6+((scope+1)%6))))
                      
        elif scope//6==0: # 2<=scope<6
                cut_point=[((pivot_min[0],pivot_min[0]+scope+1),(pivot_min[1],pivot_min[1]+scope+1))]
              
        
        
        for points in cut_point:
                ## format: [((x1,x2),(y1,y2)),((x2,x3),(y2,y3)),((x3,x4),(y3,y4))] 
                #  left side included but right side excluded
                temp_slice=[]
                for y_row in range(pivot_min[1],pivot_min[1]+scope+1):
                        for x_row in range((points[0])[0],(points[0])[1]):
                                temp_slice.append(mock_Position[x_row][y_row])
                        if len(temp_slice)>=2:
                                chess_slice["right"].append("".join(temp_slice))
                        temp_slice=[]
                ## cut by row ##
                for x_column in range(pivot_min[0],pivot_min[0]+scope+1):
                        for y_column in range((points[1])[0],(points[1])[1]):
                                temp_slice.append(mock_Position[x_column][y_column])
                        if len(temp_slice)>=2:
                                chess_slice["down"].append("".join(temp_slice))
                        temp_slice=[]
                
                ## cut by column ##
                    
                        
                #else:
                #    print("Error: The cut-sign in cut_point list is illegal.")
        
        temp_slice=[]
        for offset in range(-(scope-1),scope): 
                if offset<=0:
                        
                        for i in range(scope+1-abs(offset)):
                                if i==6 or i==12:
                                        chess_slice["bottomright"].append("".join(temp_slice))
                                        temp_slice.clear()       
                                else:
                                        temp_slice.append(mock_Position[pivot_min[0]+abs(offset)+i][pivot_min[1]+i])
                
                else:
                        for j in range(scope+1-(offset)):
                                
                                if j==6 or j==12:
                                        chess_slice["bottomright"].append("".join(temp_slice))
                                        temp_slice.clear()       
                                else:
                                        temp_slice.append(mock_Position[pivot_min[0]+j][pivot_min[1]+j+offset])
                
                if len(temp_slice)>=2:
                        chess_slice["bottomright"].append("".join(temp_slice))
                
                temp_slice.clear()
        
        temp_slice=[]
        for offset in range(-(scope-1),scope): 
                if offset<=0:
                        
                        for i in range(scope+1-abs(offset)):
                                if i==6 or i==12:
                                        chess_slice["bottomleft"].append("".join(temp_slice))
                                        temp_slice.clear()       
                                else:
                                        temp_slice.append(mock_Position[pivot_min[0]+scope-abs(offset)-i][pivot_min[1]+i])
                
                else:
                        for j in range(scope+1-(offset)):
                                
                                if j==6 or j==12:
                                        chess_slice["bottomleft"].append("".join(temp_slice))
                                        temp_slice.clear() 
                                      
                                else:
                                        temp_slice.append(mock_Position[pivot_min[0]+scope-j][pivot_min[1]+j+offset])
                
                if len(temp_slice)>=2:
                        chess_slice["bottomleft"].append("".join(temp_slice))
                
                
                temp_slice.clear()



        return evaluation_normal(chess_slice,mock_chess_color=compsign)

def chess_slicing(break_list,slicing_flag="normal"):
        '''
        slicing_flag: "normal"
        slicing_flag: "alarm"
        
        '''
        

        chess_slice={"left":[],"right":[],"up":[],"down":[],"topleft":[],"bottomright":[],"topright":[],"bottomleft":[]}
        
        mock_Position=copy.deepcopy(ChessPosition)
        
        if slicing_flag=="normal":
                max_for_max=[(),float("-inf")]
        
        for x in range(len(mock_Position)):
                for y in range(len(mock_Position[x])):
                        mock_Position[x][y]=str(mock_Position[x][y])
        
        for break_target in break_list:

                mock_x=break_target[0]
                mock_y=break_target[1]
                
                if slicing_flag=="normal":
                        mock_Position[mock_x][mock_y]=str(compsign)
                elif slicing_flag=="alarm":
                        mock_Position[mock_x][mock_y]="0"
                        

                
                

                #score_direction={"direction":[int,[str]]} 
                #This "int" refers to the length of the following str 
                

                #####################   HERE IS A PROBLEM ####################
                # The issue about the boundary of searched square # 

                ## 1. fill with 0 (empty positions)
                ## 2. fill with self chess
                ## 3. fill with opponent chess (The problem is (0,0) will be regarded as opponents' wulian immediately and return -5000000000000)

                for dir in chess_slice.keys():
                        
                        temp_list=[]
                        if dir=="left":
                                length=min(mock_x+1-0,6)
                                if length<=1:
                                        continue
                                for j in range(length):
                                        temp_list.append(mock_Position[mock_x-j][mock_y])
                                chess_slice[dir].append("".join(temp_list))

                        elif dir=="right":
                                length=min(14-(mock_x-1),6)
                                if length<=1:
                                        continue
                                for j in range(length):
                                        temp_list.append(mock_Position[mock_x+j][mock_y])
                                chess_slice[dir].append("".join(temp_list))
                        elif dir=="up":
                                length=min(mock_y+1-0,6)
                                if length<=1:
                                        continue
                                for j in range(length):
                                        temp_list.append(mock_Position[mock_x][mock_y-j])
                                chess_slice[dir].append("".join(temp_list))
                        elif dir=="down":
                                length=min(14-(mock_y-1),6)
                                if length<=1:
                                        continue
                                for j in range(length):
                                        temp_list.append(mock_Position[mock_x][mock_y+j])
                                chess_slice[dir].append("".join(temp_list))
                        elif dir=="topleft":
                                length=min(min(mock_x+1-0,mock_y+1-0),6)
                                if length<=1:
                                        continue
                                for j in range(length):
                                        temp_list.append(mock_Position[mock_x-j][mock_y-j])
                                chess_slice[dir].append("".join(temp_list))
                        elif dir=="bottomright":
                                length=min(min(14-(mock_x-1),14-(mock_y-1)),6)
                                if length<=1:
                                        continue
                                for j in range(length):
                                        temp_list.append(mock_Position[mock_x+j][mock_y+j])
                                chess_slice[dir].append("".join(temp_list))
                        elif dir=="topright":
                                length=min(min(14-(mock_x-1),mock_y+1-0),6)
                                if length<=1:
                                        continue
                                for j in range(length):
                                        temp_list.append(mock_Position[mock_x+j][mock_y-j])
                                chess_slice[dir].append("".join(temp_list))
                        elif dir=="bottomleft":
                                length=min(min(mock_x+1-0,14-(mock_y-1)),6)
                                if length<=1:
                                        continue
                                for j in range(length):
                                        temp_list.append(mock_Position[mock_x-j][mock_y+j])
                                chess_slice[dir].append("".join(temp_list))
                

                if slicing_flag=="normal":
                        temp_max_max=evaluation_normal(chess_slice,mock_chess_color=compsign)
                        #############################################################
                        #-evaluation_normal(chess_slice,mock_chess_color=3-compsign)#
                        #############################################################
                        
                        if temp_max_max>max_for_max[1]:
                                max_for_max[0]=break_target
                                max_for_max[1]=temp_max_max
            
        
        if slicing_flag=="normal":
                "Normal: chess-base double check"
                return max_for_max[0]
        elif slicing_flag=="alarm":
                return evaluation_alarm(chess_slice)


def evaluation_alarm(chess_slice):
        '''
        calculate the score simply for the emergency situations
                i.e., PRIORITY:
                        1.AI(活四) 2.AI(冲四)     # 1、2平级
                        3.human(冲四) 4.AI (单活三/跳活三) 5.human(单活三/跳活三)


        '''
        if root_window_open==0 or winnersign!=0: 
                return
        alarm_shift=["",0]

        #e.g. ["up",2] means that (alarm_x,alarm_y-2) should be put on chess

        huosi_AI="huosi_AI"
        chongsi_AI="chongsi_AI"
        danhuosan_AI="danhuosan_AI"
        tiaohuosan_AI="tiaohuosan_AI"
        huosi_human="huosi_human"
        chongsi_human="chongsi_human"
        danhuosan_human="danhuosan_human"
        tiaohuosan_human="tiaohuosan_human"

        for c_slices in chess_slice.items():
                
                if len(c_slices[1])==0:
                        continue
                
                
                for target_str in c_slices[1]:

                        if len(target_str)!=6:
                                target_str=target_str.ljust(6,"0")
                        
                        if target_str=="000000":
                                continue
                        # 完全空白
                        
                        if (target_str=="011110" and compsign==1) or (target_str=="022220" and compsign==2):
                                
                                print ("我方活四_ALARM")
                                return huosi_AI,alarm_shift
                                  
                        elif ((target_str=="011112" or target_str=="211110"\
                                or target_str=="010111" or target_str=="101110" or target_str=="011101" or target_str=="111010"\
                                or target_str=="011011" or target_str=="110110") and compsign==1)\
                                or\
                                ((target_str=="022221" or target_str=="122220"\
                                or target_str=="020222" or target_str=="202220" or target_str=="022202" or target_str=="222020"\
                                or target_str=="022022" or target_str=="220220") and compsign==2):
                                
                                alarm_offset=target_str.find("0",1)
                                if alarm_offset==-1:
                                        alarm_offset=0
                                alarm_shift=[c_slices[0],alarm_offset]

                                
                                print ("我方冲四_ALARM")                
                                return chongsi_AI,alarm_shift
                        
                        elif ((target_str=="011110") and compsign==2) or ((target_str=="022220") and compsign==1):
                                
                                print ("对方活四_ALARM")
                                return huosi_human,alarm_shift
                        
                        elif ((target_str=="011112" or target_str=="211110"\
                                or target_str=="010111" or target_str=="101110" or target_str=="011101" or target_str=="111010"\
                                or target_str=="011011" or target_str=="110110")  and compsign==2) \
                                or \
                                ((target_str=="022221" or target_str=="122220"\
                                or target_str=="020222" or target_str=="202220" or target_str=="022202" or target_str=="222020"\
                                or target_str=="022022" or target_str=="220220")  and compsign==1):
                                
                                alarm_offset=target_str.find("0",1)
                                if alarm_offset==-1:
                                        alarm_offset=0
                                alarm_shift=[c_slices[0],alarm_offset]
                                
                                print ("对方冲四_ALARM")
                                return chongsi_human,alarm_shift
                        
                        elif ((target_str=="001110" or target_str=="011100") and compsign==1) or ((target_str=="002220" or target_str=="022200") and compsign==2):
                                print ("我方单活三_ALARM")
                                if compsign==1:
                                        alarm_shift=[c_slices[0],target_str.find("01",0)]
                                else:
                                        alarm_shift=[c_slices[0],target_str.find("02",0)]
        
                                return danhuosan_AI,alarm_shift
                        

                        elif ((target_str=="010110" or target_str=="101100" or target_str=="011010" or target_str=="110100") and compsign==1) \
                                or ((target_str=="020220" or target_str=="202200" or target_str=="022020" or target_str=="220200") and compsign==2):
                                print("我方跳活三_ALARM")
                                if compsign==1:
                                        alarm_shift=[c_slices[0],target_str.find("101",1)+1]
                                else:
                                        alarm_shift=[c_slices[0],target_str.find("202",1)+1]
                                        
                                return tiaohuosan_AI,alarm_shift
                        
                        elif ((target_str=="001110" or target_str=="011100") and compsign==2) or ((target_str=="002220" or target_str=="022200") and compsign==1):
                                print ("对方单活三_ALARM")
                                if compsign==2:
                                        alarm_shift=[c_slices[0],target_str.find("01",0)]
                                else:
                                        alarm_shift=[c_slices[0],target_str.find("02",0)]
                                return danhuosan_human,alarm_shift
                        
                        elif ((target_str=="010110" or target_str=="011010") and compsign==2) or ((target_str=="020220" or target_str=="022020") and compsign==1):
                                print("对方跳活三_ALARM")
                                
                                if compsign==2:
                                        alarm_shift=[c_slices[0],target_str.find("101",1)+1]
                                
                                else:
                                        alarm_shift=[c_slices[0],target_str.find("202",1)+1]
                                return tiaohuosan_human,alarm_shift


        '''              
        for i in range(5):
                if judge_x-(4-i)>=0 and judge_x+i<=14:
                        for j in range(5):
                                if ChessPosition[judge_x-(4-j)+i][judge_y]!=turnsign:
                                        break
                                elif(j==4):
                                        return turnsign
                        
        
        # judge on rows

        for i in range(5):
                if judge_y-(4-i)>=0 and judge_y+i<=14:
                        for j in range(5):
                                if ChessPosition[judge_x][judge_y-(4-j)+i]!=turnsign:
                                        break
                                elif(j==4):
                                        return turnsign
        
        # judge on columns

        
       

        for i in range(5):
                if judge_x-(4-i)>=0 and judge_y-(4-i)>=0 \
                and  judge_x+i<=14 and judge_y+i<=14:
                        for j in range(5):
                                if ChessPosition[judge_x-(4-j)+i][judge_y-(4-j)+i]!=turnsign:
                                        break
                                elif(j==4):
                                        return turnsign
        # judge y=x+m(m is the intercept)
        
        for i in range(5):
                if judge_x+(4-i)<=14 and judge_y-(4-i)>=0 \
                and  judge_x-i>=0 and judge_y+i<=14:
                        for j in range(5):
                                if ChessPosition[judge_x+(4-j)-i][judge_y-(4-j)+i]!=turnsign:
                                        break
                                elif(j==4):
                                        return turnsign
        # judge y=-x+m(m is the intercept)
        '''  
        return "ORDINARY",alarm_shift
                        
        
def evaluation_warning():
        '''
        Warning based on pre-search (before the decision tree)
                for each legal position, put one chess for both sides and check the feasibility
                1. AI five 2. Human five 3. AI open four 4. Human open four 5. AI double four(open or closed) 6. Human double four(open or closed)
                7. AI four-three 8.human four-three 9. AI double open three 10.human double open three
                
                Input: list [legal positions] (from the square_search)
                Output: the issue identifier or keyword
        '''
        


        pass 

        
        



def evaluation_normal(chess_slice,mock_chess_color):
                
        
        '''

        calculate the score for a target situation 
        refer to the target scale after assigning this chess 
        
        '''
        if root_window_open==0 or winnersign!=0:
                return
        
        root_score=0
        # Initialize the score for a root node as 0


        

        ## as a parameter used for calculation
        ## e.g. the attack ratio for white agency should be lower than black agency
        ## fall in (0,1]
      
        if compsign==1: ## black agency
                attack_ratio=1
        elif compsign==2:
                attack_ratio=0.7

        five=5000000
        huosi=500000
        chongsi=200000 
        danhuosan=10000
        tiaohuosan=8000
        miansan=4000
        huoer=200
        mianer=100
        

        

        for c_slices in chess_slice.items():
                if len(c_slices[1])==0:
                        continue
                
                
                for target_str in c_slices[1]:
                        if len(target_str)!=6:
                                target_str=target_str.ljust(6,"0")
                        
                        if target_str=="000000" or target_str=="100000" or target_str=="200000":
                                continue
                        # 完全空白
                        if re.search("11111",target_str):
                                if mock_chess_color==1:
                                        print ("我方五连")
                                        return  five                # 五连 或 长连
                                else:
                                        print("警告:对方五连")
                                        return  five*(-1)//attack_ratio
                        elif re.search("011110",target_str):
                                if mock_chess_color==1:
                                        print ("我方活四")
                                        return  huosi                       # 活四
                                else:
                                        print ("警告:对方活四")
                                        return  huosi*(-1)//attack_ratio
                        elif target_str=="011112" or target_str=="211110"\
                                or re.search("10111",target_str) or re.search("11101",target_str)\
                                or re.search("11011",target_str):
                                if mock_chess_color==1:
                                        print ("我方冲四")
                                        return  chongsi             # 冲四
                                else:
                                        print ("警告:对方冲四")
                                        return  chongsi*(-1)//attack_ratio
                        
                        elif re.search("01110",target_str):
                                if mock_chess_color==1:
                                        root_score+=danhuosan
                                                                # 单活三
                                else:
                                        root_score+=danhuosan*(-1)//attack_ratio

                        elif target_str=="010110" or target_str=="011010":
                                if mock_chess_color==1:
                                        root_score+=tiaohuosan
                                else:
                                        root_score+=tiaohuosan*(-1)//attack_ratio
                                                                # 跳活三

                        elif target_str=="001112" or target_str=="211100" or target_str=="010112" \
                        or target_str=="211010" or target_str=="011012" or target_str=="210110"\
                        or target_str=="011102" or target_str=="201110" or re.search("10011",target_str) \
                        or  re.search("11001",target_str) or  re.search("10101",target_str) :
                                
                                if mock_chess_color==1:
                                        
                                        root_score+=miansan            
                                else:
                                        root_score+=miansan*(-1)//attack_ratio      # 眠三
                                 
                        elif target_str=="001100" or re.search("01010",target_str) or re.search("1001",target_str)\
                        or   target_str=="011000" or target_str=="000110":
                                
                                if mock_chess_color==1:
                                        root_score+=huoer           
                                else:
                                        root_score+=huoer*(-1)//attack_ratio         # 活二
                                
                        elif target_str=="010012" or target_str=="210010" or re.search("10001",target_str):
                                if mock_chess_color==1:
                                        root_score+=mianer          
                                else:
                                        root_score+=mianer*(-1)//attack_ratio      # 眠二



                        elif re.search("22222",target_str):
                                if mock_chess_color==2:
                                        print ("我方五连")
                                        return  five*attack_ratio                # 五连 或 长连
                                else:
                                        print ("警告:对方五连")
                                        return  five*(-1)
                        elif re.search("022220",target_str):
                                if mock_chess_color==2:
                                        print ("我方活四")
                                        return  huosi*attack_ratio                       # 活四
                                else:
                                        print ("警告:对方活四")
                                        return  huosi*(-1)
                        elif target_str=="022221" or target_str=="122220"\
                                or re.search("20222",target_str) or re.search("22202",target_str)\
                                or re.search("22022",target_str):
                                if mock_chess_color==2:
                                        print ("我方冲四")
                                        return  chongsi*attack_ratio             # 冲四
                                else:
                                        print ("警告:对方冲四")
                                        return  chongsi*(-1)
                        elif re.search("02220",target_str):
                                if mock_chess_color==2:
                                        root_score+=danhuosan*attack_ratio
                                                                # 单活三
                                else:
                                        root_score+=danhuosan*(-1)
                        
                        elif target_str=="020220" or target_str=="022020":
                                if mock_chess_color==2:
                                        root_score+=tiaohuosan*attack_ratio
                                else:
                                        root_score+=tiaohuosan*(-1)
                                                                # 跳活三

                        elif target_str=="002221" or target_str=="122200" or target_str=="020221" \
                        or target_str=="122020" or target_str=="022021" or target_str=="120220"\
                        or target_str=="022201" or target_str=="102220" or re.search("20022",target_str) \
                        or  re.search("22002",target_str) or  re.search("20202",target_str) :
                                
                                if mock_chess_color==2:
                                        root_score+=miansan*attack_ratio            
                                else:
                                        root_score+=miansan*(-1)        # 眠三
                                
                        elif target_str=="002200" or re.search("02020",target_str) or re.search("2002",target_str)\
                        or   target_str=="022000" or target_str=="000220" :
                                
                                if mock_chess_color==2:
                                        root_score+=huoer*attack_ratio           
                                else:
                                        root_score+=huoer*(-1)          # 活二
                                
                        elif target_str=="020021" or target_str=="120020" or re.search("20002",target_str):
                                if mock_chess_color==2:
                                        root_score+=mianer*attack_ratio          
                                else:
                                        root_score+=mianer*(-1)          # 眠二

                                        

        # print("One root score for {:} tree is {:}".format(mock_list[0],root_score))
        #if root_score is None:
        #        print("PAY ATTENTION: ERROR for unrecognized chess situation!")

        return root_score


                        


                                
               
             


def clickmonitor(event):
        '''
        monitor the click event
        '''
        x_position=event.x
        y_position=event.y
        if modeflag=="hc":
                if compsign==1:
                        if len(Re_Position)%2==0:
                                return
                else:     
                        if len(Re_Position)%2!=0:
                                return
        clickjudge(x_position,y_position)
                

def clickjudge(x_position,y_position):
        global ChessPosition,retrieve_button,turnsign
        '''
        judge the final point in a approximate and coordinate way 
        '''
        judge_x=round((x_position-26)/32)
        judge_y=round((y_position-26)/32)

        print("judge_x:{},judge_y:{}".format(judge_x,judge_y))
        if modeflag=="hh":        
                if judge_x>=0 and judge_x<=14\
                        and judge_y>=0 and judge_y<=14:
                        if (ChessPosition[judge_x][judge_y]==0):
                                turnjudge(judge_x,judge_y)
                
                else:
                        print("Error: This chess position is beyond our board")       
        elif modeflag=="hc":
                if compsign==1:
                    if turnsign==3-compsign and len(Re_Position)%2==1:
                            if judge_x>=0 and judge_x<=14\
                                    and judge_y>=0 and judge_y<=14:
                                    if (ChessPosition[judge_x][judge_y]==0):
                                            turnjudge(judge_x,judge_y)
                    else:
                            print("Error: Please wait until computer finished its turn")
                elif compsign==2:
                    if turnsign==3-compsign and len(Re_Position)%2==0:
                            if judge_x>=0 and judge_x<=14\
                                    and judge_y>=0 and judge_y<=14:
                                    if (ChessPosition[judge_x][judge_y]==0):
                                            turnjudge(judge_x,judge_y)
                    else:
                            print("Error: Please wait until computer finished its turn")
                    

def turnjudge(judge_x,judge_y):
        global winnersign,turnsign,ChessPosition,Re_Position
        '''
        Ensure that the black and white agencies put in turn 
        ### ONLY FOR HUMAN ###
        '''
        global turnsign


        ChessPosition[judge_x][judge_y]=turnsign
        Re_Position.append((judge_x,judge_y))
        retrieve_button["state"]=tk.NORMAL    


        drawchess(judge_x,judge_y)
        if len(Re_Position)>=9:
                winnersign=winnerjudge(judge_x,judge_y)
                result_report(winnersign)
        #retrieve(judge_x,judge_y)
        turnsign=3-turnsign
        
        
        
        
        
        
        
def drawchess(judge_x,judge_y):
        global BoardCanvas,ChessPosition,turnsign
        
        if turnsign==1:
                BoardCanvas.create_oval(judge_x*32+26-10,\
                judge_y*32+26-10,judge_x*32+26+10,
                judge_y*32+26+10,fill="black",tags="chess")
        elif turnsign==2:
                BoardCanvas.create_oval(judge_x*32+26-10,\
                judge_y*32+26-10,judge_x*32+26+10,
                judge_y*32+26+10,fill="white",tags="chess")

def winnerjudge(judge_x,judge_y):
        '''
        "米" character search to judge the turnsign based on the updated chess
                four loops for four directions
                '''
        
        global ChessPosition,turnsign,winnersign
        
        for i in range(5):
                if judge_x-(4-i)>=0 and judge_x+i<=14:
                        for j in range(5):
                                if ChessPosition[judge_x-(4-j)+i][judge_y]!=turnsign:
                                        break
                                elif(j==4):
                                        return turnsign
                        
        
        # judge on rows

        for i in range(5):
                if judge_y-(4-i)>=0 and judge_y+i<=14:
                        for j in range(5):
                                if ChessPosition[judge_x][judge_y-(4-j)+i]!=turnsign:
                                        break
                                elif(j==4):
                                        return turnsign
        
        # judge on columns

        
       

        for i in range(5):
                if judge_x-(4-i)>=0 and judge_y-(4-i)>=0 \
                and  judge_x+i<=14 and judge_y+i<=14:
                        for j in range(5):
                                if ChessPosition[judge_x-(4-j)+i][judge_y-(4-j)+i]!=turnsign:
                                        break
                                elif(j==4):
                                        return turnsign
        # judge y=x+m(m is the intercept)
        
        for i in range(5):
                if judge_x+(4-i)<=14 and judge_y-(4-i)>=0 \
                and  judge_x-i>=0 and judge_y+i<=14:
                        for j in range(5):
                                if ChessPosition[judge_x+(4-j)-i][judge_y-(4-j)+i]!=turnsign:
                                        break
                                elif(j==4):
                                        return turnsign
        # judge y=-x+m(m is the intercept)
       
        if winnersign==1:
                print("Black Win")
        elif winnersign==2:
                print("White win")
        else:
                return 0

def callback():
        pass

def root_window_state():
        global root_window_open,root_window

        root_window_open=0
        root_window.destroy()
        record_write()
        time_analysis()

def result_report(winnersign):
        global root_window,winner_report,ChessPosition,chess_record_sign
        #root_window.quit()
        print("winner is ",winnersign)
        if winnersign==0:
                return 
        record_write(winnersign=winnersign)
        time_analysis()

        winner_report=tk.Toplevel(root_window)
        winner_report.grab_set() #modelling this window
        winner_report.title("赛果")
        winner_report.attributes("-topmost",True)
        winner_report.protocol("WM_DELETE_WINDOW",callback)
        winner_report.geometry(center(250,330,window=winner_report))
        
        if winnersign==1:
                winner_label=tk.Label(winner_report,text="黑方胜",font=("Times New Roman",30))
                winner_label.grid(row=1,ipadx=50)
        elif winnersign==2:
                winner_label=tk.Label(winner_report,text="白方胜",font=("Times New Roman",30))
                winner_label.grid(row=1,ipadx=50)
       
        
        if modeflag=="hh":
                hh_Again_button=tk.Button(winner_report,text="再来一局",font=("Times New Roman",30),command=lambda: [winner_report.destroy(),root_window.destroy(),start_h_vs_h()])
                hh_Again_button.grid(row=2,ipadx=25)
        elif modeflag=="hc":
                hc_Again_button=tk.Button(winner_report,text="再来一局",font=("Times New Roman",30),command=lambda: [winner_report.destroy(),start_h_vs_c_config(root_window)])
                hc_Again_button.grid(row=2,ipadx=25)

        

        review_button=tk.Button(winner_report,text="复盘此局",font=("Times New Roman",30),command=lambda: [winner_report.destroy(),root_window.destroy(),review(Re_Position)])
        review_button.grid(row=4,pady=10,ipadx=25)
        quit_button=tk.Button(winner_report,text="退出游戏",font=("Times New Roman",30),command=lambda: root_window_state())
        quit_button.grid(row=6,pady=10,ipadx=25)
        
        
        winner_report.mainloop()
        





def record_write(winnersign=0):
        global chess_record_sign
        if chess_record_sign=="f":
                return 
        Writing_Re_Position=Re_Position[:]
        # replace Re_Posiiton with a shallow copy, avoid the [int]->[str] convertion covering the Re_Position, which is used for the review for the last game
        chess_record_file.write(time.asctime(time.localtime(time.time())))
        chess_record_file.write(" ")
        chess_record_file.write(modeflag+str(winnersign))
        chess_record_file.write(" ")
        for re_po in range(len(Writing_Re_Position)):
                Writing_Re_Position[re_po]=str(Writing_Re_Position[re_po])
        chess_record_file.write(",".join(Writing_Re_Position))
        chess_record_file.write("\n")
        chess_record_file.close()
        chess_record_sign="f"
        # record the finished game into "Chess_record.txt"

def retrieve_correct(): 
        global ChessPosition,BoardCanvas,turnsign,retrieve_button,Re_Position
        
        if len(Re_Position)<1 or (len(Re_Position)==1 and compsign==1):
                return
       
        if modeflag=="hh":
                retrieve_list=[Re_Position[-1]]
                del Re_Position[-1]
                turnsign=3-turnsign
        elif modeflag=="hc":
                if (len(Re_Position)%2==0 and compsign==1) or (len(Re_Position)%2==1 and compsign==2):
                        return
                retrieve_list=[Re_Position[-1],Re_Position[-2]]
                del Re_Position[-1]
                del Re_Position[-1]
        for target in retrieve_list:
                ChessPosition[target[0]][target[1]]=0
                

        ######################################################
        
        
        
        BoardCanvas.delete("chess")

        #ChessPosition[judge_x][judge_y]=(0,0)  
        
        for i in range(len(Re_Position)):
            
               
            if i%2==0:

                BoardCanvas.create_oval(Re_Position[i][0]*32+26-10,\
                                Re_Position[i][1]*32+26-10,Re_Position[i][0]*32+26+10,
                                Re_Position[i][1]*32+26+10,fill="black",tags="chess")

            else:

                BoardCanvas.create_oval(Re_Position[i][0]*32+26-10,\
                                Re_Position[i][1]*32+26-10,Re_Position[i][0]*32+26+10,
                                Re_Position[i][1]*32+26+10,fill="white",tags="chess")



        retrieve_button["state"]=tk.DISABLED


def review(Re_Position):

        global review_BoardCanvas,review_turnsign,last_button,next_button
        review_turnsign=-1
        review_window=tk.Tk()
        review_BoardCanvas=tk.Canvas(review_window,width=500,height=500,bg="Sandy Brown")
        review_BoardCanvas.grid(row=0,column=0,rowspan=10)

        for i in range (15):
                review_BoardCanvas.create_line(26,32*i+26,474,32*i+26)
        for j in range (15):
                review_BoardCanvas.create_line(32*j+26,26,32*j+26,474)
        #draw the board lines
        pointlist=[(3,3),(11,3),(7,7),(3,11),(11,11)]
        for i in range(5):
                for j in pointlist:
                        review_BoardCanvas.create_oval(26+j[0]*32-3,26+j[1]*32-3,26+j[0]*32+3,26+j[1]*32+3,fill="black")   
        #draw the black points 
                
        last_button=tk.Button(review_window,text="上一步",font=("Times New Roman",20),\
                width=12,height=3,command=lambda: review_last(Re_Position),state="disabled")
        last_button.grid(row=3,column=1,padx=8) 
        next_button=tk.Button(review_window,text="下一步",font=("Times New Roman",20),\
                width=12,height=3,command=lambda: review_next(Re_Position))
        next_button.grid(row=5,column=1,padx=8) 

        review_window.title("五子棋复盘")
        review_window.geometry(center(710,500,window=review_window))
      
        
        if modeflag=="hh":
                hh_Again_button=tk.Button(review_window,text="再来一局",font=("Times New Roman",20),width=12,height=3,command=lambda: [review_window.destroy(),start_h_vs_h()])
                hh_Again_button.grid(row=7,column=1,padx=8)
        elif modeflag=="hc":
                hc_Again_button=tk.Button(review_window,text="再来一局",font=("Times New Roman",20),width=12,height=3,command=lambda: start_h_vs_c_config(review_window))
                hc_Again_button.grid(row=7,column=1,padx=8)
        elif modeflag=="review":
                hc_Again_button=tk.Button(review_window,text="返回主菜单",font=("Times New Roman",20),width=12,height=3,command=lambda: [review_window.destroy(),start()])
                hc_Again_button.grid(row=7,column=1,padx=8)
        review_window.mainloop()
        
def review_next(Re_Position):
       
        
        global review_BoardCanvas,review_turnsign,last_button,next_button
        
        print("review_turnsign is: ",review_turnsign)
        review_turnsign+=1
        
        
        
        if review_turnsign>=len(Re_Position)-1:
                next_button["state"]=tk.DISABLED
        
         
        elif review_turnsign>=0 and review_turnsign<len(Re_Position)-1:
                last_button["state"]=tk.NORMAL
                next_button["state"]=tk.NORMAL

        elif review_turnsign<0:
                last_button["state"]=tk.DISABLED

        
        if review_turnsign==0 and len(Re_Position)==1:
                last_button["state"]=tk.NORMAL
                next_button["state"]=tk.DISABLED
         
        ###############2023.1.1###############
        
        if review_turnsign%2==0:
                
                review_BoardCanvas.create_oval(Re_Position[review_turnsign][0]*32+26-10,\
                                Re_Position[review_turnsign][1]*32+26-10,Re_Position[review_turnsign][0]*32+26+10,
                                Re_Position[review_turnsign][1]*32+26+10,fill="black",tags="chess")
        else:
                review_BoardCanvas.create_oval(Re_Position[review_turnsign][0]*32+26-10,\
                                Re_Position[review_turnsign][1]*32+26-10,Re_Position[review_turnsign][0]*32+26+10,
                                Re_Position[review_turnsign][1]*32+26+10,fill="white",tags="chess")

        
def review_last(Re_Position):
        
        global review_BoardCanvas,review_turnsign,last_button,next_button
        print("review_turnsign is: ",review_turnsign)
        review_turnsign-=1
                
        
        if review_turnsign>=len(Re_Position)-1:
                next_button["state"]=tk.DISABLED
         
        elif review_turnsign>=0 and review_turnsign<len(Re_Position)-1:
                last_button["state"]=tk.NORMAL
                next_button["state"]=tk.NORMAL
        elif review_turnsign<0:
                last_button["state"]=tk.DISABLED

        if review_turnsign==-1 and len(Re_Position)==1:
                last_button["state"]=tk.DISABLED
                next_button["state"]=tk.NORMAL

        review_BoardCanvas.delete("chess")

        for i in range(review_turnsign+1):
                if i%2==0:
                        review_BoardCanvas.create_oval(Re_Position[i][0]*32+26-10,\
                                        Re_Position[i][1]*32+26-10,Re_Position[i][0]*32+26+10,
                                        Re_Position[i][1]*32+26+10,fill="black",tags="chess")
                else:   
                        review_BoardCanvas.create_oval(Re_Position[i][0]*32+26-10,\
                                        Re_Position[i][1]*32+26-10,Re_Position[i][0]*32+26+10,
                                        Re_Position[i][1]*32+26+10,fill="white",tags="chess")

def time_analysis():
        '''
        temp function used for analysing the time cost
                based on average, max, standard deviation of both time(s) and frequency (ms/node) 
        '''
        print(time_list)
        print("Average time {:.2f} (s)".format(sum(map(lambda x:x[0],time_list))/len(time_list)))
        print("Average frequency {:.2f} (ms/node)".format(sum(map(lambda x:x[1],time_list))/len(time_list)))
        print("Max time {:.2f} (s)".format(max(time_list,key= lambda x:x[0])[0]))
        print("Max frequency {:.2f} (ms/node)".format(max(time_list,key= lambda x:x[1])[1]))
        print("std time {:.2f} (s)".format(numpy.std(list(map(lambda x:x[0],time_list)))))
        print("std frequency {:.2f} (ms/node)".format(numpy.std(list(map(lambda x:x[1],time_list)))))


                

                
start()

        