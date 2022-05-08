#%%
#read a file and count tokens
import os
import re
import plotly.express as px
import pandas as pd
os.chdir("/mnt/d/Mega/Documents/CS/TLoB/")
FILES = {
    "example1": ["quatusExamples2/simpleFifo_hw.tcl","quatusExamples2/Example1.qsys"],
    "example1B": ["quatusExamples2/simpleFifo_hw.tcl","quatusExamples2/Example1B.qsys"],
    "example2": ["quatusExamples2/fake16550_hw.tcl","quatusExamples2/fluteCore_hw.tcl","quatusExamples2/Example2.qsys"],
    "example3": ["quatusExamples2/axi4Master1_hw.tcl","quatusExamples2/axi4Master2_hw.tcl","quatusExamples2/axi4Slave5_hw.tcl","quatusExamples2/axi4Slave7_hw.tcl","quatusExamples2/Example3.qsys"]
}
FILESMyTOOL = {
    "example1":["exampleFIFOs.json"],
    "example1B":["exampleFIFOs3.json"],
    "example2": ["exampleFlute.json"],
    "example3": ["example3.json"]
}

regex = "(\w|\.)+"

def count(FILES):
    Lines = {}
    Tokens = {}
    #compute number of tokes and lines for each groups of files in FILES
    for exampleName,group in FILES.items():
        Lines[exampleName] = 0
        Tokens[exampleName] = 0
        for file in group:
            with open(os.path.join(".",file)) as f:
                content = f.readlines()
                Lines[exampleName] += len(content)
                #flatten
                content = "".join(content)
                #find all words matching regex
                content = [m.group() for m in re.finditer(regex,content)]
                
                #remove empty strings
                content = [x for x in content if x != '']
                #count
                Tokens[exampleName] += len(content)
    return Lines,Tokens

results ={"IQP":count(FILES), "My":count(FILESMyTOOL)}

#create a dataframe Tool:["IQP","My"], Example, Lines, Tokens
df = pd.DataFrame(columns=["Tool","Example","Lines","Tokens"])
for tool,(lines,tokens) in results.items():
    for example,l in lines.items():
        df = df.append({"Tool":tool,"Example":example,"Lines":l,"Tokens":tokens[example]},ignore_index=True)

#display(df)
        
# %%
#chart1 stacked bar chart of IQP and My example1, example1B 
dfC1 = df[df["Example"].isin(["example1","example1B"])]
#subtract line and token count in example1 from example1B
for tool in ["IQP","My"]:
    torLines = dfC1[(dfC1["Example"] == "example1") & (dfC1["Tool"] == tool)]["Lines"]
    torTokens = dfC1[(dfC1["Example"] == "example1") & (dfC1["Tool"] == tool)]["Tokens"]
    dfC1.loc[(dfC1["Example"] == "example1B") & (dfC1["Tool"] == tool),"Lines"] -= list(torLines)[0]
    dfC1.loc[(dfC1["Example"] == "example1B") & (dfC1["Tool"] == tool),"Tokens"] -= list(torTokens)[0]


fig1 = px.bar(dfC1, x="Tool", y="Tokens", color="Example", barmode="stack")
#chart2 same but with lines
fig2 = px.bar(dfC1, x="Tool", y="Lines", color="Example", barmode="stack")
#increase font size
fig1.update_layout(font_size=18)
fig2.update_layout(font_size=18)
#save charts as pdf in ../Latex/charts
fig1.write_image("Latex/charts/example1_tokens.pdf")
fig2.write_image("Latex/charts/example1_lines.pdf")
# %%
#grouped bar chart of tokens for each example
dfC2 =df
fig3 = px.bar(dfC2, x="Tool", y="Tokens", color="Example", barmode="group")
# same for lines
fig4 = px.bar(dfC2, x="Tool", y="Lines", color="Example", barmode="group")
fig3.update_layout(font_size=18)
fig4.update_layout(font_size=18)
#save charts as pdf in ../Latex/charts
fig3.write_image("Latex/charts/all_tokens.pdf")
fig4.write_image("Latex/charts/all_lines.pdf")

# %%
