from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px

df = pd.read_csv('BlackFriday.csv')

app = Dash(__name__)

# 按User_ID分类并计算每个User_ID对应的Purchase总和
purchase_by_user = df.groupby(['User_ID','Age','Gender','Marital_Status','Occupation','City_Category'])['Purchase'].sum().reset_index()
# 按照合并后的数据集中的Purchase列进行降序排序
top_10_users = purchase_by_user.sort_values(by='Purchase', ascending=False).head(10)
# 将 User_ID 列的数据类型更改为字符串
top_10_users['User_ID'] = top_10_users['User_ID'].astype(str)
#按从大到小的顺序显示
top_10_users = top_10_users.iloc[::-1]

#Purchase按年龄Age分类
age = df.groupby('Age')['Purchase'].sum().reset_index()
#Purchase按在城市居住时间分类
duration = df.groupby('Stay_In_Current_City_Years')['Purchase'].sum().reset_index()


#页面布局
app.layout = html.Div(
    [
        #标题栏：黑色星期五
        html.H1("Black Friday Sales Dashboard", style={'textAlign': 'center'}),
        #图表栏
        html.Div(
            [
                #饼状图：查看各因素购买量占比
                html.Div(
                    [
                        html.H4("Proportion of Purchase by Factors"),
                        dcc.RadioItems(
                            id="pie",
                            options=[
                                {'label': 'City Category', 'value': 'City_Category'},
                                {'label': 'Occupation', 'value': 'Occupation'},
                                {'label': 'Gender', 'value': 'Gender'},
                                {'label': 'Marital Status', 'value': 'Marital_Status'}
                            ],
                            value='City_Category',
                            labelStyle={'display': 'inline-block'}
                        ),
                        dcc.Graph(id='PieChart')
                    ],
                    className="six columns",
                    style={'margin': '10px'}
                ),
                # 用户购买量前十柱状图
                html.Div(
                    [
                        html.H4("Top 10 Users by Purchase"),
                        dcc.Graph(
                            id="user-top10",
                            figure=px.bar(
                                top_10_users,
                                x='Purchase',
                                y='User_ID',
                                orientation='h',
                                # hover显示值
                                hover_data=['Age', 'Gender', 'Marital_Status', 'Occupation', 'City_Category'],
                                title='Top 10 Users'
                            )
                        )
                    ],
                    className="six columns",
                    style={'margin': '10px'}
                ),
            ],
            className="row"
        ),
        #折线图：购买量随年龄/居住时长变化
        html.Div(
            [
                html.H4("Purchase Quantity by Factors"),
                dcc.RadioItems(
                    id="line",
                    options=[
                        {'label': 'Age', 'value': 'Age'},
                        {'label': 'Stay in Current City Years', 'value': 'Stay_In_Current_City_Years'}
                    ],
                    value='Age',
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Graph(id='LineChart', style={'height': '400px'})
            ],
            style={'margin': '10px'}
        )
    ],
    style={'font-family': 'Arial, sans-serif', 'max-width': '900px', 'margin': 'auto'}
)

# 饼图
@app.callback(
    Output('PieChart', 'figure'),
    Input('pie', 'value'),
)
def updatePieChart(selected_factor):
    fig = px.pie(df, values='Purchase', names=selected_factor, title=f"Proportion of Purchase by {selected_factor}")
    return fig

# 折线图
@app.callback(
    Output('LineChart', 'figure'),
    Input('line', 'value'),
)
def updateLineChart(selected_factor):
    if selected_factor == 'Age':
        fig = px.line(age, x=selected_factor, y='Purchase', title=f"Purchase Quantity by {selected_factor}")
    else:
        fig = px.line(duration, x=selected_factor, y='Purchase', title=f"Purchase Quantity by {selected_factor}")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
