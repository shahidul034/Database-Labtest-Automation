import cx_Oracle
import re
con = cx_Oracle.connect('ss/ss@localhost')
mycursor = con.cursor()
Ques=open("data/ques.txt","r").read().split("\n")
temp=open("data/radio.txt","r").read().split("\n")
radio_ques=[]
for x in temp:
    xx=x.split("||")
    radio_ques.append(
        {
            "question":xx[0],
            "mcq":xx[1].split(";"),
            "ans":xx[2]
        }
    )
def question_show(number):
    if number>=(len(Ques)+1) and number<=(len(Ques)+len(temp)):
        q_num=number-len(Ques)-1
        return {
            rad:gr.Radio(radio_ques[q_num]["mcq"], label=radio_ques[q_num]["question"], visible=True,interactive=True),
            out: gr.Textbox(visible=False),
            inp:gr.Code(label="SQL code",lines=10,visible=False,interactive=True),
            lab: gr.Label(visible=False)
        }
    return {
        rad:gr.Radio(visible=False),
        out: gr.Textbox(label="Question description",lines=2,visible=True,value=f"{Ques[int(number)-1]}"),
        inp:gr.Code(label="SQL code",lines=10,visible=True,interactive=True, value=""),
        lab: gr.Label(visible=False)
    } 
def sql_check_fun(sql_code):
    try:
        mycursor.execute(sql_code)
        return True
    except:
        return False
def answer_check2(roll,number,sql_code):
    ch=sql_check_fun(sql_code)
    if not ch:
            return False
    if number==1:
        pattern = r'create\s+table\s+(\w+)'
        match = re.search(pattern, sql_code)
        table_name = match.group(1)
        t=[(x[0],x[1]) for x in ((mycursor.execute(f"select * from {table_name}")).description)]
        t2=[(x[0],x[1]) for x in ((mycursor.execute("select * from shakib")).description)]
        return t==t2
    if number==2:
        table_name=sql_code.split(" ")[2]
        t=([x for x in mycursor.execute("select * from shakib")])[0]
        t2=([x for x in mycursor.execute(f"select * from {table_name}")])[0]
        return t==t2
    if number==3 and sql_code.split(" ")[3]!="rename":
        pattern = r'\balter\s+table\s+\w+\s+rename\s+column\s+\w+\s+to\s+\w+\b'
        match = re.search(pattern, sql_code, re.IGNORECASE)
        print(match)
        return match is not None
    if number==4 and sql_code.split(" ")[3]!='modify':
        pattern = r'\balter table\b\s+\w+\s+\bmodify\b\s+\w+\s+\w+\(\d+\)'
        return bool(re.search(pattern, sql_code, re.IGNORECASE))

    if number==5 and sql_code.split( )[3]!='add':
        return False
    if number==6 and sql_code.split( )[3]!='drop':
        return False

    
def check_duplicate(roll,number):
    temp2=open("data/result.txt","r").read().split("\n")
    for x in temp2:
        xx=x.split(";")
        if str(roll)==str(xx[0]) and str(number)==str(xx[1]):
            return True
    return False
def answer_check(roll,number,rad,inp):
    print(roll,number,rad,inp)
    if check_duplicate(roll,number):
        return {
                lab: gr.Label(visible=True,elem_id="already",value="Already submitted or accepted!!!")
            }
    result=open("data/result.txt","a")
    if number>=(len(Ques)+1) and number<=(len(Ques)+len(temp)):
        q_num=number-len(Ques)-1
        if radio_ques[q_num]["ans"]==rad:
            st=f"{roll};{number};AC\n"
            result.write(st)
            return {
                lab: gr.Label(visible=True,elem_id="accepted",value="Submitted")
            }
        else:
            st=f"{roll};{number};NAC\n"
            result.write(st)
            return {
                lab: gr.Label(visible=True,elem_id="accepted",value="Submitted")
            }
       
        
    else:
        sql_check=answer_check2(roll,number,inp)
        if sql_check:
            st=f"{roll};{number};AC\n"
            result.write(st)
            return {
                lab: gr.Label(visible=True,elem_id="accepted",value="Accepted")
            }
        else:
            return {
                lab: gr.Label(visible=True,elem_id="wrong",value="Wrong")
            }
    result.close()
        
import gradio as gr
css = """
#accepted {background-color: green;align-content: center;font: 30px Arial, sans-serif;}
#wrong {background-color: red;align-content: center;font: 30px Arial, sans-serif;}
#already {background-color: blue;align-content: center;font: 30px Arial, sans-serif;}
"""
with gr.Blocks(css=css) as demo:
    gr.Markdown(
    """
    # Database Quiz and Lab test
    """)
    with gr.Row():
        roll = gr.Number(label="Roll number")
    with gr.Row():
        ques_show=gr.Dropdown(
            [x+1 for x in range(len(Ques)+len(temp))], label="Question number", info="Enter your question number")
    with gr.Row():
        out = gr.Textbox(label="Question description",lines=1,visible=False)
    with gr.Row():
        inp=gr.Code(label="SQL code",lines=10,visible=False)
        rad=gr.Radio(visible=False)
    with gr.Row():    
        button = gr.Button("Submit")
        lab=gr.Label(visible=False)
        ques_show.change(question_show, ques_show, [rad,out,inp,lab])
    button.click(answer_check,[roll,ques_show,rad,inp],lab)

demo.launch()


