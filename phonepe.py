import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
import plotly
from PIL import Image
import base64

# Data Frame Creation
#SQL Connection
My_Database = psycopg2.connect(host = "localhost",
                               user = "postgres",
                               port = "5432",
                               database = "PhonePe_Data",
                               password = "admin123")
cursor = My_Database.cursor()

# Aggregated_Insurance
cursor.execute("SELECT * FROM Aggregated_Insurance")
My_Database.commit()
Table_1 = cursor.fetchall()

Aggregated_Insurance_DF = pd.DataFrame(Table_1,columns = ("States","Years","Quarter","Transaction_Type",
                                                          "Transaction_count","Transaction_amount"))

# Aggregated_Transaction
cursor.execute("SELECT * FROM Aggregated_Transaction")
My_Database.commit()
Table_2 = cursor.fetchall()

Aggregated_Transaction_DF = pd.DataFrame(Table_2,columns = ("States","Years","Quarter","Transaction_Type",
                                                          "Transaction_count","Transaction_amount"))

# Aggregated_User
cursor.execute("SELECT * FROM Aggregated_User")
My_Database.commit()
Table_3 = cursor.fetchall()

Aggregated_User_DF = pd.DataFrame(Table_3,columns = ("States","Years","Quarter","Brands",
                                                          "Transaction_count","Percentage"))

# Map_Insurance
cursor.execute("SELECT * FROM Map_Insurance")
My_Database.commit()
Table_4 = cursor.fetchall()

Map_Insurance_DF = pd.DataFrame(Table_4,columns = ("States","Years","Quarter","Districts",
                                                          "Transaction_count","Transaction_amount"))

# Map_Transaction
cursor.execute("SELECT * FROM Map_Transaction")
My_Database.commit()
Table_5 = cursor.fetchall()

Map_Transaction_DF = pd.DataFrame(Table_5,columns = ("States","Years","Quarter","Districts",
                                                          "Transaction_count","Transaction_amount"))

# Map_User
cursor.execute("SELECT * FROM Map_User")
My_Database.commit()
Table_6 = cursor.fetchall()

Map_User_DF = pd.DataFrame(Table_6,columns = ("States","Years","Quarter","Districts",
                                                          "RegisteredUsers","AppOpens"))

# Top_Insurance
cursor.execute("SELECT * FROM Top_Insurance")
My_Database.commit()
Table_7 = cursor.fetchall()

Top_Insurance_DF = pd.DataFrame(Table_7,columns = ("States","Years","Quarter","Pincodes",
                                                          "Transaction_count","Transaction_amount"))

# Top_Transaction
cursor.execute("SELECT * FROM Top_Transaction")
My_Database.commit()
Table_8 = cursor.fetchall()

Top_Transaction_DF = pd.DataFrame(Table_8,columns = ("States","Years","Quarter","Pincodes",
                                                          "Transaction_count","Transaction_amount"))

# Top_User
cursor.execute("SELECT * FROM Top_User")
My_Database.commit()
Table_9 = cursor.fetchall()

Top_User_DF = pd.DataFrame(Table_9,columns = ("States","Years","Quarter","Pincodes",
                                                          "RegisteredUsers"))



def Transaction_Amount_and_Count_Y(df,year):

    Trans_Count_Amt_Y = df[df["Years"] == year]
    Trans_Count_Amt_Y.reset_index(drop=True, inplace=True)

    Trans_Count_Amt_Y_Group = Trans_Count_Amt_Y.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Trans_Count_Amt_Y_Group.reset_index(inplace = True)

    col1,col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(Trans_Count_Amt_Y_Group, x = "States", y = "Transaction_amount", title = f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        

        fig_amount.update_layout(title={'text': f"{year} TRANSACTION AMOUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                 geo=dict(visible=False)
                                 )
        st.plotly_chart(fig_amount)   
    with col2:
        fig_count = px.bar(Trans_Count_Amt_Y_Group, x = "States", y = "Transaction_count", title = f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=650,width=600)
        fig_count.update_layout(title={'text': f"{year} TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                 geo=dict(visible=False)
                                 )
        st.plotly_chart(fig_count)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    Data_1 = json.loads(response.content)

    state_name = []

    for feature in Data_1["features"]:
        state_name.append((feature["properties"]["ST_NM"]))

    state_name.sort()

    with col1:

        fig_India_1 = px.choropleth(Trans_Count_Amt_Y_Group, geojson = Data_1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color = (Trans_Count_Amt_Y_Group["Transaction_amount"].min(), 
                                                Trans_Count_Amt_Y_Group["Transaction_amount"].max()),
                                    hover_name = "States", title = f"{year} TRANSACTION AMOUNT",fitbounds = "locations", height=600,width=600)
        
        fig_India_1.update_geos(visible = False)
        fig_India_1.update_layout(title={'text': f"{year} TRANSACTION AMOUNT",'font':{'family':"comic sans ms",'color':"yellow"},
                     # Center the title
        },
    geo=dict(visible=False)
    )

        st.plotly_chart(fig_India_1)

    with col2:

        fig_India_2 = px.choropleth(Trans_Count_Amt_Y_Group, geojson = Data_1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_count",color_continuous_scale="Rainbow",
                                    range_color = (Trans_Count_Amt_Y_Group["Transaction_count"].min(), 
                                                Trans_Count_Amt_Y_Group["Transaction_count"].max()),
                                    hover_name = "States", title = f"{year} TRANSACTION COUNT",fitbounds = "locations", height=600,width=600)
        
        fig_India_2.update_geos(visible = False)
        fig_India_2.update_layout(title={'text': f"{year} TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"},
                     # Center the title
        },
        geo=dict(visible=False)
        )

        st.plotly_chart(fig_India_2)

    return Trans_Count_Amt_Y

def Transaction_Amount_and_Count_Y_Q(df,quarter):

    Trans_Count_Amt_Y = df[df["Quarter"] == quarter]
    Trans_Count_Amt_Y.reset_index(drop=True, inplace=True)

    Trans_Count_Amt_Y_Group = Trans_Count_Amt_Y.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Trans_Count_Amt_Y_Group.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(Trans_Count_Amt_Y_Group, x = "States", y = "Transaction_amount", title = f"{Trans_Count_Amt_Y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=600,width=600)
        fig_amount.update_layout(title={'text':f"{Trans_Count_Amt_Y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                 geo=dict(visible=False)
                                 )
        st.plotly_chart(fig_amount)

    with col2:

        fig_count = px.bar(Trans_Count_Amt_Y_Group, x = "States", y = "Transaction_count", title = f"{Trans_Count_Amt_Y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=600,width=600)
        fig_count.update_layout(title={'text':f"{Trans_Count_Amt_Y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                 geo=dict(visible=False)
                                 )
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)

    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        Data_1 = json.loads(response.content)

        state_name = []

        for feature in Data_1["features"]:
            state_name.append((feature["properties"]["ST_NM"]))

        state_name.sort()

        fig_India_1 = px.choropleth(Trans_Count_Amt_Y_Group, geojson = Data_1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color = (Trans_Count_Amt_Y_Group["Transaction_amount"].min(), 
                                                Trans_Count_Amt_Y_Group["Transaction_amount"].max()),
                                    hover_name = "States", title = f"{Trans_Count_Amt_Y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                                    fitbounds = "locations", height=600,width=600)
        
        fig_India_1.update_geos(visible = False)
        fig_India_1.update_layout(title={'text': f"{Trans_Count_Amt_Y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",'font':{'family':"comic sans ms",'color':"yellow"},
                     # Center the title
        },
        geo=dict(visible=False)
        )


        st.plotly_chart(fig_India_1)

    with col2:


        fig_India_2 = px.choropleth(Trans_Count_Amt_Y_Group, geojson = Data_1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_count",color_continuous_scale="Rainbow",
                                    range_color = (Trans_Count_Amt_Y_Group["Transaction_count"].min(), 
                                                Trans_Count_Amt_Y_Group["Transaction_count"].max()),
                                    hover_name = "States", title = f"{Trans_Count_Amt_Y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                                    fitbounds = "locations", 
                                    height=600,width=600)
        
        fig_India_2.update_geos(visible = False)
        fig_India_2.update_layout(title={'text': f"{Trans_Count_Amt_Y['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"},
                     # Center the title
        },
        geo=dict(visible=False)
        )

        st.plotly_chart(fig_India_2)

    return Trans_Count_Amt_Y


def Aggre_tran_transaction_type(df,state):

    Trans_Count_Amt_Y = df[df["States"] == state]
    Trans_Count_Amt_Y.reset_index(drop=True, inplace=True)

    Trans_Count_Amt_Y_Group = Trans_Count_Amt_Y.groupby("Transaction_Type")[["Transaction_count","Transaction_amount"]].sum()
    Trans_Count_Amt_Y_Group.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:
        fig_piechart_1 = px.pie(data_frame = Trans_Count_Amt_Y_Group, names = "Transaction_Type", values = "Transaction_amount",
                             width= 600, title = f"{state.upper()} TRANSACTION AMOUNT", hole = 0.5)
        fig_piechart_1.update_layout(title={'text': f"{state.upper()} TRANSACTION AMOUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                     geo=dict(visible=False))
        st.plotly_chart(fig_piechart_1)

    with col2:

        fig_piechart_2 = px.pie(data_frame = Trans_Count_Amt_Y_Group, names = "Transaction_Type", values = "Transaction_count",
                             width=600, title = f"{state.upper()} TRANSACTION COUNT", hole = 0.5)
        fig_piechart_2.update_layout(title={'text': f"{state.upper()} TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                     geo=dict(visible=False))
        st.plotly_chart(fig_piechart_2)


# Aggregated User Analysis_1
def Aggregate_User_Plot_1(df,year):
    Aggre_User_Year = df[df["Years"]== year]
    Aggre_User_Year.reset_index(drop = True, inplace = True)

    Aggre_User_Year_GroupBy = pd.DataFrame(Aggre_User_Year.groupby("Brands")["Transaction_count"].sum())
    Aggre_User_Year_GroupBy.reset_index(inplace = True)

    fig_User_BarChart_1 =px.bar(Aggre_User_Year_GroupBy, x = "Brands", y = "Transaction_count", title = f"{year} BRANDS AND TRANSACTION COUNT",
                                width = 1000, color_discrete_sequence = px.colors.sequential.Oranges_r,hover_name="Brands") 
    fig_User_BarChart_1.update_layout(title={'text': f"{year} BRANDS AND TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                     geo=dict(visible=False))
    st.plotly_chart(fig_User_BarChart_1)
    
    return Aggre_User_Year


# Aggregated User Analaysis_2
def Aggregated_User_Plot_2(df,quarter):
    
    Aggre_User_Year_Quarter = df[df["Quarter"]== quarter]
    Aggre_User_Year_Quarter.reset_index(drop = True, inplace = True)

    Aggre_User_Year_Quarter_GroupBy = pd.DataFrame(Aggre_User_Year_Quarter.groupby("Brands")["Transaction_count"].sum())
    Aggre_User_Year_Quarter_GroupBy.reset_index(inplace= True)

    fig_User_BarChart_1 =px.bar(Aggre_User_Year_Quarter_GroupBy, x = "Brands", y = "Transaction_count", title = f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                                width = 1000, color_discrete_sequence = px.colors.sequential.Oranges_r, hover_name="Brands") 
    
    st.plotly_chart(fig_User_BarChart_1)

    return Aggre_User_Year_Quarter


# Aggregate User Analysis 3
def Aggregated_User_Plot_3(df,state):

    Aggre_User_Year_Quarter_State = df[df["States"] == state]
    Aggre_User_Year_Quarter_State.reset_index(drop=True,inplace= True)

    fig_line_1 = px.line(Aggre_User_Year_Quarter_State, x = "Brands", y = "Transaction_count", hover_data= "Percentage",
                        title = f"{state.upper()}'s  BRANDS,  TRANSACTION COUNT,  PERCENTAGE",width = 800,
                        markers=True)
    fig_line_1.update_layout(title={'text': f"{state.upper()}'s  BRANDS,  TRANSACTION COUNT,  PERCENTAGE",'font':{'family':"comic sans ms",'color':"yellow"}},
                             geo=dict(visible=False))
    st.plotly_chart(fig_line_1)


# Map Insurance Districts
def Map_Insurance_Districts(df,state):

    Trans_Count_Amt_Y = df[df["States"] == state]
    Trans_Count_Amt_Y.reset_index(drop=True, inplace=True)
    

    Trans_Count_Amt_Y_Group = Trans_Count_Amt_Y.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    Trans_Count_Amt_Y_Group.reset_index(inplace = True)

    col_1,col_2 = st.columns(2)

    with col_1:
        fig_Bar_1 = px.bar(Trans_Count_Amt_Y, x = "Transaction_amount", y = "Districts", orientation = "h",
                        title = f"{state}'s DISTRICTS AND TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Mint_r,
                        height = 600, width = 600)
        fig_Bar_1.update_layout(title = {'text':f"{state}'s DISTRICTS AND TRANSACTION AMOUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
            geo=dict(visible=False)
        )
        st.plotly_chart(fig_Bar_1)

    with col_2:
        fig_Bar_2 = px.bar(Trans_Count_Amt_Y, x = "Transaction_count", y = "Districts", orientation = "h",
                        title = f"{state}'s DISTRICTS AND TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r,
                        height = 600,width = 600)
        fig_Bar_2.update_layout(title = {'text': f"{state}'s DISTRICTS AND TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
            geo=dict(visible=False)
        )
        st.plotly_chart(fig_Bar_2)


# Map_User_Plot_1
def Map_User_Plot_1(df,year):

    Map_User_Year = df[df["Years"]== year]
    Map_User_Year.reset_index(drop = True, inplace = True)

    Map_User_Year_GroupBy = Map_User_Year.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    Map_User_Year_GroupBy.reset_index(inplace = True)

    fig_line_1 = px.line(Map_User_Year_GroupBy, x = "States", y = ["RegisteredUsers", "AppOpens"],
                        title = f"{year} REGISTERED USERS AND APP OPENS",width = 1000,height = 800,
                        markers=True)
    fig_line_1.update_layout(title={'text': f"{year} REGISTERED USERS AND APP OPENS",'font':{'family':"comic sans ms",'color':"yellow"}},
                             geo=dict(visible=False))
    st.plotly_chart(fig_line_1)

    return Map_User_Year

# Map_User_Plot_2
def Map_User_Plot_2(df,quarter):

    Map_User_Year_Quarter = df[df["Quarter"]== quarter]
    Map_User_Year_Quarter.reset_index(drop = True, inplace = True)

    Map_User_Year_GroupBy = Map_User_Year_Quarter.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    Map_User_Year_GroupBy.reset_index(inplace = True)

    fig_line_1 = px.line(Map_User_Year_GroupBy, x = "States", y = ["RegisteredUsers", "AppOpens"],
                        title = f"{df['Years'].min()} {quarter} QUARTER REGISTERED USERS AND APP OPENS",width = 1000,height = 800,
                        markers=True,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    fig_line_1.update_layout(title={'text': f"{df['Years'].min()} {quarter} QUARTER REGISTERED USERS AND APP OPENS",'font':{'family':"comic sans ms",'color':"yellow"}},
                             geo=dict(visible=False))
    st.plotly_chart(fig_line_1)

    return Map_User_Year_Quarter


# Map User Plot 3
def Map_User_Plot_3(df,states):
    Map_User_Year_Quarter_State = df[df["States"]== states]
    Map_User_Year_Quarter_State.reset_index(drop = True, inplace = True)


    col_1,col_2 = st.columns(2)
    with col_1:
            fig_Map_User_Bar_1 = px.bar(Map_User_Year_Quarter_State, x = "RegisteredUsers", y = "Districts", orientation= "h",
                                    title = f"{states.upper()} REGISTERED USERS", height= 800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
            fig_Map_User_Bar_1.update_layout(title={'text': f"{states.upper()} REGISTERED USERS",'font':{'family':"comic sans ms",'color':"yellow"}},
                                            geo=dict(visible=False))
            st.plotly_chart(fig_Map_User_Bar_1)


    with col_2:
        fig_Map_User_Bar_2 = px.bar(Map_User_Year_Quarter_State, x = "AppOpens", y = "Districts", orientation= "h",
                                    title = f"{states.upper()} APP OPENS", height= 800, color_discrete_sequence=px.colors.sequential.Rainbow)
        fig_Map_User_Bar_2.update_layout(title={'text': f"{states.upper()} APP OPENS",'font':{'family':"comic sans ms",'color':"yellow"}},
                                         geo=dict(visible=False))
        st.plotly_chart(fig_Map_User_Bar_2)


# Top Insurance Plot_1
def Top_Insurance_Plot_1(df,state):
    Top_Insurance_Year = df[df["States"]== state]
    Top_Insurance_Year.reset_index(drop = True, inplace = True)

    Top_Insurance_Year_GroupBy = Top_Insurance_Year.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    Top_Insurance_Year_GroupBy.reset_index(inplace = True)


    col_1,col_2 = st.columns(2)
    with col_1:
        fig_Top_Insurance_Bar_1 = px.bar(Top_Insurance_Year, x ="Quarter", y = "Transaction_amount",hover_data= "Pincodes",
                                        title = "TRANSACTION AMOUNT", height= 650, width=600, color_discrete_sequence=px.colors.sequential.Reds_r)
        fig_Top_Insurance_Bar_1.update_layout(title = {'text': "TRANSACTION AMOUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                              geo=dict(visible=False))
        st.plotly_chart(fig_Top_Insurance_Bar_1)
    with col_2:
        fig_Top_Insurance_Bar_2 = px.bar(Top_Insurance_Year, x ="Quarter", y = "Transaction_count",hover_data= "Pincodes",
                                    title = "TRANSACTION COUNT", height= 650, width=600, color_discrete_sequence=px.colors.sequential.Peach_r)
        fig_Top_Insurance_Bar_2.update_layout(title = {'text': "TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"}},geo=dict(visible=False))
        st.plotly_chart(fig_Top_Insurance_Bar_2)


def Top_User_Plot_1(df,year):
    Top_User_Year = df[df["Years"]== year]
    Top_User_Year.reset_index(drop = True, inplace = True)

    Top_User_Year_GroupBy = pd.DataFrame(Top_User_Year.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    Top_User_Year_GroupBy.reset_index(inplace = True)

    fig_Top_User_Plot_1 = px.bar(Top_User_Year_GroupBy, x = "States", y = "RegisteredUsers", color = "Quarter", width = 1000,
                                height = 800,color_discrete_sequence = px.colors.sequential.Burgyl, hover_name="States",
                                title = f"{year} REGISTERED USERS")
    fig_Top_User_Plot_1.update_layout(title={'text': f"{year} REGISTERED USERS",'font':{'family':"comic sans ms",'color':"yellow"}},
                                     geo=dict(visible=False))
    st.plotly_chart(fig_Top_User_Plot_1)

    return Top_User_Year


# Top User Plot_2
def Top_User_Plot_2(df,state):
    Top_User_Year_State = df[df["States"]== state]
    Top_User_Year_State.reset_index(drop = True, inplace = True)

    fig_Top_User_Plot_2 = px.bar(Top_User_Year_State, x = "Quarter", y = "RegisteredUsers", title = "REGISTERED USERS , PINCODES AND QUARTER",
                                width = 1000, height = 800, color = "RegisteredUsers", hover_data = "Pincodes",color_continuous_scale = px.colors.sequential.Magenta)
    fig_Top_User_Plot_2.update_layout(title={'text': "REGISTERED USERS , PINCODES AND QUARTER",'font':{'family':"comic sans ms",'color':"yellow"}},
                                      geo=dict(visible=False))
    st.plotly_chart(fig_Top_User_Plot_2)


#SQL Connection

def Top_Chart_Transaction_Amount(table_name):
    My_Database = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                port = "5432",
                                database = "PhonePe_Data",
                                password = "admin123")
    cursor = My_Database.cursor()


    # Plot_1
    query_1 = f'''select states, sum(transaction_amount) as transaction_amount
                    from {table_name}
                    group by states
                    order by transaction_amount desc
                    limit 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    My_Database.commit()

    df_1 = pd.DataFrame(table_1, columns=("states","transaction_amount"))

    col_1,col_2 = st.columns(2)
    with col_1:
        fig_amount_1 = px.bar(df_1, x = "states", y = "transaction_amount", title = "TOP 10 OF TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600,
                            hover_name="states")
        fig_amount_1.update_layout(title = {'text': "TOP 10 OF TRANSACTION AMOUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                   geo=dict(visible=False))
        st.plotly_chart(fig_amount_1)


    # Plot_2
    query_2 = f'''select states, sum(transaction_amount) as transaction_amount
                    from {table_name}
                    group by states
                    order by transaction_amount
                    limit 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    My_Database.commit()

    df_2 = pd.DataFrame(table_2, columns=("states","transaction_amount"))

    with col_2:
        fig_amount_2 = px.bar(df_2, x = "states", y = "transaction_amount", title = "LAST 10 OF TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650,width=600,
                            hover_name="states")
        fig_amount_2.update_layout(title = {'text': "LAST 10 OF TRANSACTION AMOUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                   geo=dict(visible=False))
        st.plotly_chart(fig_amount_2)


    # Plot_3
    query_3 = f'''select states, avg(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    My_Database.commit()

    df_3 = pd.DataFrame(table_3, columns=("states","transaction_amount"))

    fig_amount_3 = px.bar(df_3, x = "transaction_amount", y = "states", title = "AVERAGE OF TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Cividis, height=800,width=1000,
                        hover_name="states", orientation="h")
    fig_amount_3.update_layout(title = {'text': "AVERAGE OF TRANSACTION AMOUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                               geo=dict(visible=False))
    st.plotly_chart(fig_amount_3)


#SQL Connection

def Top_Chart_Transaction_Count(table_name):
    My_Database = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                port = "5432",
                                database = "PhonePe_Data",
                                password = "admin123")
    cursor = My_Database.cursor()


    # Plot_2
    query_1 = f'''select states, sum(transaction_count) as transaction_count
                    from {table_name}
                    group by states
                    order by transaction_count desc
                    limit 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    My_Database.commit()

    df_1 = pd.DataFrame(table_1, columns=("states","transaction_count"))

    col_1,col_2 = st.columns(2)
    with col_1:
        fig_amount = px.bar(df_1, x = "states", y = "transaction_count", title = "TOP 10 OF TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=600,width=600,
                            hover_name="states")
        fig_amount.update_layout(title = {'text': "TOP 10 OF TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                 geo=dict(visible=False))
        st.plotly_chart(fig_amount)


    # Plot_2
    query_2 = f'''select states, sum(transaction_count) as transaction_count
                    from {table_name}
                    group by states
                    order by transaction_count
                    limit 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    My_Database.commit()

    df_2 = pd.DataFrame(table_2, columns=("states","transaction_count"))

    with col_2:
        fig_amount_2 = px.bar(df_2, x = "states", y = "transaction_count", title = "LAST 10 OF TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600,width=600,
                            hover_name="states")
        fig_amount_2.update_layout(title = {'text': "LAST 10 OF TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                                 geo=dict(visible=False))
        st.plotly_chart(fig_amount_2)


    # Plot_3
    query_3 = f'''select states, avg(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    My_Database.commit()

    df_3 = pd.DataFrame(table_3, columns=("states","transaction_count"))

    fig_amount_3 = px.bar(df_3, x = "transaction_count", y = "states", title = "AVERAGE OF TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Cividis, height=800,width=1000,
                        hover_name="states", orientation="h")
    fig_amount_3.update_layout(title = {'text': "AVERAGE OF TRANSACTION COUNT",'font':{'family':"comic sans ms",'color':"yellow"}},
                               geo=dict(visible=False))
    st.plotly_chart(fig_amount_3)


#SQL Connection
#Top_Chart_Registered_Users
def Top_Chart_Registered_Users(table_name, state):
    My_Database = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                port = "5432",
                                database = "PhonePe_Data",
                                password = "admin123")
    cursor = My_Database.cursor()


    # Plot_1
    query_1 = f'''select districts,sum(registeredusers) as registeredusers
                from {table_name}
                where states = '{state}'
                group by districts
                order by registeredusers desc
                limit 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    My_Database.commit()

    df_1 = pd.DataFrame(table_1, columns=("districts","registeredusers"))
    col_1,col_2 = st.columns(2)
    with col_1:
        fig_amount = px.bar(df_1, x = "districts", y = "registeredusers", title = "TOP 10 OF REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=600,width=600,
                            hover_name="districts")
        fig_amount.update_layout(title = {'text': "TOP 10 OF REGISTERED USERS",'font':{'family':"comic sans ms",'color':"yellow"}},
                                 geo=dict(visible=False))
        st.plotly_chart(fig_amount)


    # Plot_2
    query_2 = f'''select districts,sum(registeredusers) as registeredusers
                from {table_name}
                where states = '{state}'
                group by districts
                order by registeredusers
                limit 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    My_Database.commit()

    df_2 = pd.DataFrame(table_2, columns=("districts","registeredusers"))

    with col_2:
        fig_amount_2 = px.bar(df_2, x = "districts", y = "registeredusers", title = "LAST 10 OF REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600,width=600,
                            hover_name="districts")
        fig_amount_2.update_layout(title = {'text': "LAST 10 OF REGISTERED USERS",'font':{'family':"comic sans ms",'color':"yellow"}},
                                 geo=dict(visible=False))
        st.plotly_chart(fig_amount_2)


    # Plot_3
    query_3 = f'''select districts,avg(registeredusers) as registeredusers
                from {table_name}
                where states = '{state}'
                group by districts
                order by registeredusers;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    My_Database.commit()

    df_3 = pd.DataFrame(table_3, columns=("districts","registeredusers"))

    fig_amount_3 = px.bar(df_3, x = "registeredusers", y = "districts", title = "AVERAGE OF REGISTERED USERS",
                        color_discrete_sequence=px.colors.sequential.Cividis, height=800,width=1000,
                        hover_name="districts", orientation="h")
    fig_amount_3.update_layout(title = {'text': "AVERAGE OF REGISTERED USERS",'font':{'family':"comic sans ms",'color':"yellow"}},
                               geo=dict(visible=False))
    st.plotly_chart(fig_amount_3)


#SQL Connection
# Top Charts App Opens
def Top_Chart_App_Opens(table_name, state):
    My_Database = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                port = "5432",
                                database = "PhonePe_Data",
                                password = "admin123")
    cursor = My_Database.cursor()


    # Plot_1
    query_1 = f'''select districts,sum(appopens) as appopens
                from {table_name}
                where states = '{state}'
                group by districts
                order by appopens desc
                limit 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    My_Database.commit()

    df_1 = pd.DataFrame(table_1, columns=("districts","appopens"))


    col_1,col_2 = st.columns(2)
    with col_1:
        fig_amount = px.bar(df_1, x = "districts", y = "appopens", title = "TOP 10 OF APP OPENS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=600,width=600,
                            hover_name="districts")
        fig_amount.update_layout(title = {'text': "TOP 10 OF APP OPENS",'font':{'family':"comic sans ms",'color':"yellow"}},
                                 geo=dict(visible=False))
        st.plotly_chart(fig_amount)


    # Plot_2
    query_2 = f'''select districts,sum(appopens) as appopens
                from {table_name}
                where states = '{state}'
                group by districts
                order by appopens
                limit 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    My_Database.commit()

    df_2 = pd.DataFrame(table_2, columns=("districts","appopens"))

    with col_2:
        fig_amount_2 = px.bar(df_2, x = "districts", y = "appopens", title = "LAST 10 OF APP OPENS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600,width=600,
                            hover_name="districts")
        fig_amount_2.update_layout(title = {'text': "LAST 10 OF APP OPENS",'font':{'family':"comic sans ms",'color':"yellow"}},
                                 geo=dict(visible=False))
        st.plotly_chart(fig_amount_2)


    # Plot_3
    query_3 = f'''select districts,avg(appopens) as appopens
                from {table_name}
                where states = '{state}'
                group by districts
                order by appopens;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    My_Database.commit()

    df_3 = pd.DataFrame(table_3, columns=("districts","appopens"))

    fig_amount_3 = px.bar(df_3, x = "appopens", y = "districts", title = "AVERAGE OF APP OPENS",
                        color_discrete_sequence=px.colors.sequential.Cividis, height=800,width=1000,
                        hover_name="districts", orientation="h")
    fig_amount_3.update_layout(title = {'text': "AVERAGE OF APP OPENS",'font':{'family':"comic sans ms",'color':"yellow"}},
                               geo=dict(visible=False))
    st.plotly_chart(fig_amount_3)


#SQL Connection
# Top user 10th Question

def Top_Chart_Registered_Users_of_Top_User(table_name):
    
    My_Database = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                port = "5432",
                                database = "PhonePe_Data",
                                password = "admin123")
    cursor = My_Database.cursor()


    # Plot_1
    query_1 = f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers desc
                limit 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    My_Database.commit()

    df_1 = pd.DataFrame(table_1, columns=("states","registeredusers"))

    col_1,col_2 = st.columns(2)
    with col_1:
        fig_amount = px.bar(df_1, x = "states", y = "registeredusers", title = "TOP 10 OF TOP REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=600,width=600,
                            hover_name="states")
        fig_amount.update_layout(title = {'text': "TOP 10 OF TOP REGISTERED USERS",'font':{'family':"comic sans ms",'color':"yellow"}})
        st.plotly_chart(fig_amount)


    # Plot_2
    query_2 = f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers
                limit 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    My_Database.commit()

    df_2 = pd.DataFrame(table_2, columns=("states","registeredusers"))

    with col_2:
        fig_amount_2 = px.bar(df_2, x = "states", y = "registeredusers", title = "LAST 10 OF TOP REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600,width=600,
                            hover_name="states")
        fig_amount_2.update_layout(title = {'text':"LAST 10 OF TOP REGISTERED USERS",'font':{'family':"comic sans ms",'color':"yellow"}},
                                   geo=dict(visible=False))
        st.plotly_chart(fig_amount_2)


    # Plot_3
    query_3 = f'''select states, avg(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    My_Database.commit()

    df_3 = pd.DataFrame(table_3, columns=("states","registeredusers"))

    fig_amount_3 = px.bar(df_3, x = "registeredusers", y = "states", title = "AVERAGE OF TOP REGISTERED USERS",
                        color_discrete_sequence=px.colors.sequential.Cividis, height=800,width=1000,
                        hover_name="states", orientation="h")
    fig_amount_3.update_layout(title = {'text': "AVERAGE OF TOP REGISTERED USERS",'font':{'family':"comic sans ms",'color':"yellow"}},
                               geo=dict(visible=False))
    st.plotly_chart(fig_amount_3)


# streamlit Part

st.set_page_config(layout="wide",page_title="Phonepe Pulse",page_icon="📊",initial_sidebar_state="expanded")
page_bg = '''
<style>
body {
    background-image: url("D:/python YT/New folder/.venv/phonepe_bg_img.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
'''

# Apply the background CSS
st.markdown(page_bg, unsafe_allow_html=True)
st.markdown("""
    <h1 style="font-family: 'Castellar', sans-serif; font-size: 36px; color: purple;">
        📊 PHONEPE DATA VISUALIZATION AND EXPLORATION
    </h1>
""", unsafe_allow_html=True)
#st.title("📊 PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    
    #select = option_menu("Main Menu",["Home","Data Exploration","Top Charts"])
    select = option_menu(
                        menu_title = "Manin Menu",
                        options = ["Home","Data Exploration","Top Charts","Profile"],
                        icons = ["house","book","book","person"],
                        menu_icon = "cast",
                        default_index = 0,
                        styles={
                            "container":{
                                "background-color":"purple",
                                "padding":"0px",
                                "margin":"0px",
                                "font-color":"black"
                            },
                            "icon":{
                                "color":"black",
                                "font-size":"25px"
                            },
                            "nav_link":{
                                "font-size":"16px",
                                "text-align":"left",
                                "margin":"0px",
                                "color":"black"
                                
                            }
                            }
                        )
    
    Skill_Box = st.selectbox("Skill Take Away",
                 ("1. Github Cloning",
                  "2. Python",
                  "3. Pandas",
                  "4. mysql-connector-python",
                  "5. Streamlit",
                  "6. Plotly"))
    if Skill_Box == "1. Github Cloning":
        pass
    elif Skill_Box == "2. Python":
        pass
    elif Skill_Box == "3. Pandas":
       pass
    elif Skill_Box == "4. Postgres-SQL-connector-python":
        pass
    elif Skill_Box == "5. Streamlit":
        pass

    elif Skill_Box == "5. Plotly":
        pass





if select == "Home":
    style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    background-i;
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)
    
    col1,col2= st.columns(2)

    with col1:
        st.markdown("""
    <h1 style="font-family: 'Castellar', sans-serif; font-size: 36px; color: #4CAF50;">
        PHONEPE
    </h1>
""", unsafe_allow_html=True)
        #st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
    st.markdown("""
        <h3 style="font-family: 'Castellar', sans-serif; font-size: 18px; color: #4CAF50;">
            FEATURES
        </h3>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h6 style="font-family: 'gaudy old style', sans-serif; font-size: 18px; color: #4CAF50;">
            
            Credit & Debit card linking\n
            Bank Balance check\n
            Money Storage\n
            PIN Authorization\n
        </h6>
    """, unsafe_allow_html=True)

        #st.write("****FEATURES****")
       # st.write("****Credit & Debit card linking****")
        #st.write("****Bank Balance check****")
        #st.write("****Money Storage****")
        #st.write("****PIN Authorization****")
        #st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        
        import streamlit as st

        video_path_1 = r'D:\python YT\New folder\.venv\PhonePe - Introduction.mp4'
        st.video(video_path_1)

        #st.video(Image.open('D:/python YT/New folder/.venv/Phone Pe Ad (1).mp4'))

    col3,col4= st.columns(2)

    with col3:
            video_path_2 = 'D:/python YT/New folder/.venv/Phone Pe Ad (1).mp4'
            st.video(video_path_2)
                #st.image(Image.open(r"D:\python YT\New folder\.venv\Phonepe_img_2.jpeg"),width=450)

    with col4:
            st.markdown("""
            <h6 style="font-family: 'Castellar', sans-serif; font-size: 18px; color: #4CAF50;, text-align: right;">
                        
                
            One App For All Your Payments\n
            Easy Transactions\n
            Your Bank Account Is All You Need\n
            Multiple Payment Modes\n
            PhonePe Merchants\n
            Multiple Ways To Pay\n
            1.Direct Transfer & More\n
            2.QR Code\n
            Earn Great Rewards
        </h6>
    """, unsafe_allow_html=True)

            #st.write("****Easy Transactions****")
            #st.write("****One App For All Your Payments****")
            #st.write("****Your Bank Account Is All You Need****")
            #st.write("****Multiple Payment Modes****")
            #st.write("****PhonePe Merchants****")
            #st.write("****Multiple Ways To Pay****")
            #st.write("****1.Direct Transfer & More****")
            #st.write("****2.QR Code****")
            #st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")

        st.markdown("""
        <h3 style="font-family: 'Castellar', sans-serif; font-size: 18px; color: #4CAF50;">
            
            No Wallet Top-Up Required\n
            Pay Directly From Any Bank To Any Bank A/C\n
            Instantly & Free
        </h3>
    """, unsafe_allow_html=True)
       # st.write("****No Wallet Top-Up Required****")
       # st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        #st.write("****Instantly & Free****")
        #st.markdown(" ")

    with col6:
        video_path_3 = r'D:\python YT\New folder\.venv\Phone Pe Motion Graphics Crop.mp4'
        st.video(video_path_3)
        #st.image(Image.open(r"D:\python YT\New folder\.venv\Phonepe_img_3.jpeg"),width=400)


elif select == "Data Exploration":

    tab_1,tab_2,tab_3 = st.tabs(["Aggregated Analysis", "Map Analysis","Top Analysis"])
    tab_style = '''
    <style>
    .stTabs [data-baseweb="tab"] {
        padding: 10px;
        margin: 5px;
        border: 2px solid black;
        border-radius: 5px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e0e0e0;
    }
    </style>
    '''

    # Apply the custom CSS
    st.markdown(tab_style, unsafe_allow_html=True)
    # Create tabs with boxes
    #tab_1, tab_2, tab_3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    #tab_1,tab_2,tab_3 = st.tabs(["Aggregated Analysis", "Map Analysis","Top Analysis"])
    

    with tab_1:
        method = st.radio("Select The Method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])


        if method == "Insurance Analysis":

            col1,col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Year</h4>", 
                    unsafe_allow_html=True
                )
                
                years = st.slider(
                    "",
                    Aggregated_Insurance_DF["Years"].min(),
                    Aggregated_Insurance_DF["Years"].max(),
                    Aggregated_Insurance_DF["Years"].min()
                )

            tac_Y = Transaction_Amount_and_Count_Y(Aggregated_Insurance_DF, years)

            col1,col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Quarter</h4>", 
                    unsafe_allow_html=True
                )
                
                quarters = st.slider(
                    "",
                    tac_Y["Quarter"].min(),
                    tac_Y["Quarter"].max(),
                    tac_Y["Quarter"].min()
                )
               # quarters = st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),
                                #tac_Y["Quarter"].min())
            Transaction_Amount_and_Count_Y_Q(tac_Y,quarters)


        elif method == "Transaction Analysis":
            
            col1,col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Year</h4>", 
                    unsafe_allow_html=True
                )
                
                years = st.slider(
                    "",
                    Aggregated_Transaction_DF["Years"].min(),
                    Aggregated_Transaction_DF["Years"].max(),
                    Aggregated_Transaction_DF["Years"].min()
                )
                #years = st.slider("Select The Year",Aggregated_Transaction_DF["Years"].min(),Aggregated_Transaction_DF["Years"].max(),
                               # Aggregated_Transaction_DF["Years"].min())
            
            Agg_trans_tac_Y = Transaction_Amount_and_Count_Y(Aggregated_Transaction_DF, years)

            col1,col2 = st.columns(2)
            with col1:
                # Add a styled label for the selectbox
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The States</h4>", 
                    unsafe_allow_html=True
                )

                states = st.selectbox("", Agg_trans_tac_Y["States"].unique())

            Aggre_tran_transaction_type(Agg_trans_tac_Y, states)
                #states = st.selectbox("Select The States", Agg_trans_tac_Y["States"].unique())

           # Aggre_tran_transaction_type(Agg_trans_tac_Y,states)

            col1,col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Quarter</h4>", 
                    unsafe_allow_html=True
                )
                
                quarters = st.slider(
                    "",
                    Agg_trans_tac_Y["Quarter"].min(),
                    Agg_trans_tac_Y["Quarter"].max(),
                    Agg_trans_tac_Y["Quarter"].min()
                )
                #quarters = st.slider("Select The Quarter",Agg_trans_tac_Y["Quarter"].min(),Agg_trans_tac_Y["Quarter"].max(),
                               # Agg_trans_tac_Y["Quarter"].min())
            Aggre_trans_tac_Q_Y = Transaction_Amount_and_Count_Y_Q(Agg_trans_tac_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:
                # Add a styled label for the selectbox
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The States Type</h4>", 
                    unsafe_allow_html=True
                )

                states = st.selectbox("", Aggre_trans_tac_Q_Y["States"].unique(),key = "unique_selectbox_key")

                #states = st.selectbox("Select The States Type", Aggre_trans_tac_Q_Y["States"].unique())

            Aggre_tran_transaction_type(Aggre_trans_tac_Q_Y,states)



        elif method == "User Analysis":
            
                col1,col2 = st.columns(2)
                
                with col1:
                    st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Year</h4>", 
                    unsafe_allow_html=True
                )
                
                years = st.slider(
                    "",
                    Aggregated_User_DF["Years"].min(),
                    Aggregated_User_DF["Years"].max(),
                    Aggregated_User_DF["Years"].min())
                    #years = st.slider("Select The Year",Aggregated_User_DF["Years"].min(),Aggregated_User_DF["Years"].max(),
                                    #Aggregated_User_DF["Years"].min())
                
                Agg_User_Year = Aggregate_User_Plot_1(Aggregated_User_DF,years)     


                col1,col2 = st.columns(2)   
                with col1:
                    st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Quarter</h4>",
                    unsafe_allow_html=True
                    )
                
                    #quarters = st.slider(
                       # "",
                        #Agg_User_Year["Quarter"].min(),
                        #Agg_User_Year["Quarter"].max(),
                        #Agg_User_Year["Quarter"].min(),
                       # key = "unique_quarters")

                    quarters = st.slider("",Agg_User_Year["Quarter"].min(),Agg_User_Year["Quarter"].max(),
                                    Agg_User_Year["Quarter"].min())

                    Agg_User_Year_Quarter = Aggregated_User_Plot_2(Agg_User_Year,quarters)
                #Agg_User_Year_Quarter = Aggregated_User_Plot_2(Agg_User_Year,quarters_value)

                col1,col2 = st.columns(2)
                with col1:
                    # Add a styled label for the selectbox
                    st.markdown(
                        "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The States</h4>", 
                        unsafe_allow_html=True
                    )
                    states = st.selectbox("", Agg_User_Year_Quarter["States"].unique())

                    #states = st.selectbox("Select The State", Agg_User_Year_Quarter["States"].unique())

                Aggregated_User_Plot_3(Agg_User_Year_Quarter,states)


    with tab_2:



        method_2 = st.radio("Select The Method",["Map Insurance", "Map Transaction","Map User"])

        if method_2 == "Map Insurance":
            
            col1,col2 = st.columns(2)
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Year For Map Insurance</h4>", 
                    unsafe_allow_html=True
                )
                years = st.slider("",
                    Map_Insurance_DF["Years"].min(),
                    Map_Insurance_DF["Years"].max(),
                    Map_Insurance_DF["Years"].min(),
                    key="unique_slider_key")
                
                #years = st.slider("Select The Year For Map Insurance",Map_Insurance_DF["Years"].min(),Map_Insurance_DF["Years"].max(),
                 #               Map_Insurance_DF["Years"].min())
            
            Map_Insurance_tac_Y = Transaction_Amount_and_Count_Y(Map_Insurance_DF, years)

            col1,col2 = st.columns(2)
            with col1:
                # Add a styled label for the selectbox
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The State Of Map Insurance</h4>", 
                    unsafe_allow_html=True
                )
                states = st.selectbox("", Map_Insurance_tac_Y["States"].unique(),key = "unique_state_key")

                #states = st.selectbox("Select The State Of Map Insurance", Map_Insurance_tac_Y["States"].unique())

            Map_Insurance_Districts(Map_Insurance_tac_Y,states)


            col1,col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Particular Quarter For Map Insurance</h4>", 
                    unsafe_allow_html=True
                )
                quarters = st.slider("",
                    Map_Insurance_tac_Y["Quarter"].min(),
                    Map_Insurance_tac_Y["Quarter"].max(),
                    Map_Insurance_tac_Y["Quarter"].min(),
                    key="unique_Quarter_key"
                )
                #quarters = st.slider("Select The Particular Quarter For Map Insurance",Map_Insurance_tac_Y["Quarter"].min(),Map_Insurance_tac_Y["Quarter"].max(),
                 #               Map_Insurance_tac_Y["Quarter"].min())
            Map_Insurance_tac_Year_Quarter = Transaction_Amount_and_Count_Y_Q(Map_Insurance_tac_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:

                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The States For Quarter Of Map Insurance</h4>", 
                    unsafe_allow_html=True
                )
                states = st.selectbox("", Map_Insurance_tac_Year_Quarter["States"].unique(), key = "unique_States_Map_Insurance_key")

                #states = st.selectbox("Select The States For Quarter Of Map Insurance", Map_Insurance_tac_Year_Quarter["States"].unique())

            Map_Insurance_Districts(Map_Insurance_tac_Year_Quarter, states)



        elif method_2 == "Map Transaction":
            
            col1,col2 = st.columns(2)
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Year For Map Insurance</h4>", 
                    unsafe_allow_html=True
                )
                years = st.slider("",
                    Map_Transaction_DF["Years"].min(),
                    Map_Transaction_DF["Years"].max(),
                    Map_Transaction_DF["Years"].min(),
                    key = "unique_slider_for_year_map_Insurance"
                )
                #years = st.slider("Select The Year For Map Insurance",Map_Transaction_DF["Years"].min(),Map_Transaction_DF["Years"].max(),
                         #       Map_Transaction_DF["Years"].min())
            
            Map_Transaction_tac_Y = Transaction_Amount_and_Count_Y(Map_Transaction_DF, years)

            col1,col2 = st.columns(2)
            with col1:

                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The States</h4>", 
                    unsafe_allow_html=True
                )
                states = st.selectbox("", Map_Transaction_tac_Y["States"].unique(),key = "unique_state_for_select_states")

                #states = st.selectbox("Select The States", Map_Transaction_tac_Y["States"].unique())

            Map_Insurance_Districts(Map_Transaction_tac_Y,states)


            col1,col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Particular Quarter For Map Transaction</h4>", 
                    unsafe_allow_html=True
                )
                quarters = st.slider("",
                    Map_Transaction_tac_Y["Quarter"].min(),
                    Map_Transaction_tac_Y["Quarter"].max(),
                    Map_Transaction_tac_Y["Quarter"].min(),
                    key = "unique_particular_Q_Map_T"
                )
                #quarters = st.slider("",Map_Transaction_tac_Y["Quarter"].min(),Map_Transaction_tac_Y["Quarter"].max(),
                                #Map_Transaction_tac_Y["Quarter"].min())
                #quarters = st.slider("Select The Particular Quarter For Map Transaction",Map_Transaction_tac_Y["Quarter"].min(),Map_Transaction_tac_Y["Quarter"].max(),
                               # Map_Transaction_tac_Y["Quarter"].min())
            Map_Transaction_tac_Year_Quarter = Transaction_Amount_and_Count_Y_Q(Map_Transaction_tac_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:

                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The States Type</h4>", 
                    unsafe_allow_html=True
                )
                states = st.selectbox("", Map_Transaction_tac_Year_Quarter["States"].unique(), key = "unique_state_type_key")
                #states = st.selectbox("Select The States Type", Map_Transaction_tac_Year_Quarter["States"].unique())

            Map_Insurance_Districts(Map_Transaction_tac_Year_Quarter, states)


        elif method_2 == "Map User":

            col1,col2 = st.columns(2)
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Year For Map Insurance</h4>", 
                    unsafe_allow_html=True
                )
                years = st.slider("",
                    Map_User_DF["Years"].min(),
                    Map_User_DF["Years"].max(),
                    Map_User_DF["Years"].min(),
                    key= "unique_slider_year_key"
                )
                #years = st.slider("",Map_User_DF["Years"].min(),Map_User_DF["Years"].max(),
                               # Map_User_DF["Years"].min())
                #years = st.slider("Select The Year For Map Insurance",Map_User_DF["Years"].min(),Map_User_DF["Years"].max(),
                                #Map_User_DF["Years"].min())
            
            Map_User_Y = Map_User_Plot_1(Map_User_DF,years)

            col1,col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Particular Quarter For Map Transaction</h4>", 
                    unsafe_allow_html=True
                )
                quarters = st.slider("",
                    Map_User_Y["Quarter"].min(),
                    Map_User_Y["Quarter"].max(),
                    Map_User_Y["Quarter"].min(),
                    key = "unique_particular_quarter_key_for_map_T"
                )
                #quarters = st.slider("",Map_User_Y["Quarter"].min(),Map_User_Y["Quarter"].max(),
                                #Map_User_Y["Quarter"].min())
                #quarters = st.slider("Select The Particular Quarter For Map Transaction",Map_User_Y["Quarter"].min(),Map_User_Y["Quarter"].max(),
                               # Map_User_Y["Quarter"].min())
            Map_User_Year_Quarter = Map_User_Plot_2(Map_User_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:

                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The States Of Map User</h4>", 
                    unsafe_allow_html=True
                )


                states = st.selectbox("", Map_User_Year_Quarter["States"].unique(),key = "unique_state_select_of_map_user ")

            Map_User_Plot_3(Map_User_Year_Quarter, states)


    with tab_3:
        method_3 = st.radio("Select The Method",["Top Insurance", "Top Transaction","Top User"])
        
        if method_3 == "Top Insurance":
            
            col1,col2 = st.columns(2)
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Year For Top Insurance</h4>", 
                    unsafe_allow_html=True
                )
                years = st.slider("",
                    Top_Insurance_DF["Years"].min(),
                    Top_Insurance_DF["Years"].max(),
                    Top_Insurance_DF["Years"].min(),
                    key = "select_unique_year_for_top_insurance"
                )
                #years = st.slider("",Top_Insurance_DF["Years"].min(),Top_Insurance_DF["Years"].max(),Top_Insurance_DF["Years"].min())
                #years = st.slider("Select The Year For Top Insurance",Top_Insurance_DF["Years"].min(),Top_Insurance_DF["Years"].max(),
                                #Top_Insurance_DF["Years"].min())
            
            Top_Insurance_tac_Y = Transaction_Amount_and_Count_Y(Top_Insurance_DF, years)

            col1,col2 = st.columns(2)
            with col1:

                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The States Of Top Insurance</h4>", 
                    unsafe_allow_html=True
                )
                states = st.selectbox("", Top_Insurance_tac_Y["States"].unique(),key = "uniqu_particular_Q_for_top_Ins")

            Top_Insurance_Plot_1(Top_Insurance_tac_Y,states)

            col1,col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Particular Quarter For Top Insurance</h4>", 
                    unsafe_allow_html=True
                )
                quarters = st.slider("",Top_Insurance_DF["Quarter"].min(),Top_Insurance_DF["Quarter"].max(),
                                Top_Insurance_DF["Quarter"].min(), key = "select_unique_states_for_top_ins")
            Top_Insurance_Year_Quarter = Transaction_Amount_and_Count_Y_Q(Top_Insurance_DF,quarters)

        
        elif method_3 == "Top Transaction":
            
            col1,col2 = st.columns(2)
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Year For Top Transaction</h4>", 
                    unsafe_allow_html=True
                )
                years = st.slider("",
                    Top_Transaction_DF["Years"].min(),
                    Top_Transaction_DF["Years"].max(),
                    Top_Transaction_DF["Years"].min(),
                    key = "select_unique_year_for_trans"
                )
                #years = st.slider("",Top_Transaction_DF["Years"].min(),Top_Transaction_DF["Years"].max(),
                                #Top_Transaction_DF["Years"].min(), )
            
            Top_Transaction_TAC_Y = Transaction_Amount_and_Count_Y(Top_Transaction_DF, years)

            col1,col2 = st.columns(2)
            with col1:

                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The States Of Top Transaction</h4>", 
                    unsafe_allow_html=True
                )

                states = st.selectbox("", Top_Transaction_TAC_Y["States"].unique(), key ="Select_unique_states_of_Top_TRANS")

            Top_Insurance_Plot_1(Top_Transaction_TAC_Y,states)

            col1,col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Particular Quarter For Top Transaction</h4>", 
                    unsafe_allow_html=True
                )
                quarters = st.slider("",Top_Transaction_TAC_Y["Quarter"].min(),Top_Transaction_TAC_Y["Quarter"].max(),
                                Top_Transaction_TAC_Y["Quarter"].min(),key = "unique_Select_paticular_quarter_for_top_trans")
            Top_Transaction_Year_Quarter = Transaction_Amount_and_Count_Y_Q(Top_Transaction_TAC_Y,quarters)
        
        elif method_3 == "Top User":
            
            col1,col2 = st.columns(2)
            with col1:
                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Year For Top User</h4>", 
                    unsafe_allow_html=True
                )
                years = st.slider("",Top_User_DF["Years"].min(),Top_User_DF["Years"].max(),
                                Top_User_DF["Years"].min(), key = "select_unique_year_for_top_user")
            
            Top_User_Y = Top_User_Plot_1(Top_User_DF, years)

            col1,col2 = st.columns(2)
            with col1:

                st.markdown(
                    "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The States Of Top User</h4>", 
                    unsafe_allow_html=True
                )
                states = st.selectbox("", Top_User_Y["States"].unique(),key = "unique_states_for_top_user")

            Top_User_Plot_2(Top_User_Y,states)

elif select == "Top Charts":
    st.markdown("<h1 style='font-family: castellar; font-size: 25px; color: mediumpurple;'>TOP CHARTS</h1>", unsafe_allow_html=True)
    #st.title("TOP CHARTS")
    st.markdown(
        "<h4 style='font-family: comic sans ms; font-size: 18px; color: white;'>Select The Question From Below:</h4>",
        unsafe_allow_html=True
    )
    
    question = st.selectbox("",["1. Transaction Amount and Count of Aggregated Insurance",

                                                    "2. Transaction Amount and Count of Map Insurance",

                                                    "3. Transaction Amount and Count of Top Insurance",

                                                    "4. Transaction Amount and Count of Aggregated Transaction",

                                                    "5. Transaction Amount and Count of Map Transaction",

                                                    "6. Transaction Amount and Count of Top Transaction",

                                                    "7. Transaction Count of Aggregated User",

                                                    "8. Registered users of Map User",

                                                    "9. App opens of Map User",

                                                    "10. Registered users of Top User"
                                                    ],key="unique_of_top_charts")
    

    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_Amount("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_Count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_Amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_Count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_Amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_Count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_Amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_Count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_Amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_Count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_Chart_Transaction_Amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_Count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        Top_Chart_Transaction_Count("aggregated_user")

    elif question == "8. Registered users of Map User":

        states = st.selectbox("Select The State", Map_User_DF["States"].unique())
        st.subheader("REGISTERED USERS")
        Top_Chart_Registered_Users("map_user",states)

    elif question == "9. App opens of Map User":

        states = st.selectbox("Select The State", Map_User_DF["States"].unique())
        st.subheader("REGISTERED USERS")
        Top_Chart_App_Opens("map_user",states)

    elif question == "10. Registered users of Top User":

        st.subheader("REGISTERED USERS")
        Top_Chart_Registered_Users_of_Top_User("top_user")


elif select == "Profile":
    st.markdown("""
    <style>
    /* Custom font style for links */
    a {
        font-family: "Arial", sans-serif;  /* Change to desired font */
        font-size: 18px;                  /* Adjust font size */
        font-weight: bold;                /* Make the font bold */
        color: #0073e6;                   /* Link color */
        text-decoration: none;            /* Remove underline */
    }
    a:hover {
        color: #005bb5;                   /* Hover color for links */
    }
    </style>
""", unsafe_allow_html=True)
    Links_of_mine = option_menu(
                        menu_title = "Connect Me",
                        options = ["Instagram","Email","LinkedIn","Git_Hub"],
                        icons = ["instagram","envelope","linkedin","github"],
                        menu_icon = "cast",
                        default_index = 0
                        )


        # Display the corresponding link based on selection
    if Links_of_mine == "Instagram":
        st.markdown('<a href="https://www.instagram.com/kishore_kumar_22/" target="_blank"><i class="fab fa-instagram"></i> Instagram</a>', unsafe_allow_html=True)
    elif Links_of_mine == "Email":
        st.markdown('<a href="mailto:kishorericardo026@gmail.com" target="_blank"><i class="fas fa-envelope"></i> Email</a>', unsafe_allow_html=True)
    elif Links_of_mine == "LinkedIn":
        st.markdown('<a href="https://www.linkedin.com/in/kishorekumar2002" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a>', unsafe_allow_html=True)
    elif Links_of_mine == "Git_Hub":
        st.markdown('<a href="https://github.com/KishoreKumar-J-22" target="_blank"><i class="fab fa-github"></i> GitHub</a>', unsafe_allow_html=True)
