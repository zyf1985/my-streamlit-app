import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 设置 SimHei 字体以支持中文显示
font_path = 'C:\\Windows\\Fonts\\simhei.ttf'  # Windows 系统的 SimHei 字体路径
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用 SimHei 字体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

# 设置页面标题
st.title('中国福利彩票历史数据分析')

# 上传文件
uploaded_file = st.file_uploader("上传 Excel 文件", type=["xlsx"])

# 确认已上传文件
if uploaded_file:
    # 读取 Excel 数据
    df = pd.read_excel(uploaded_file)

    # 显示数据预览
    st.write("数据预览：", df.head())

    # 检查数据列名
    st.write("数据列名：", df.columns)

    # 定义红球和蓝球的列
    red_ball_columns = ['红球1', '红球2', '红球3', '红球4', '红球5', '红球6']
    blue_ball_column = '篮球'  # 使用“篮球”作为蓝球的列名

    try:
        # 检查列是否存在
        if all(col in df.columns for col in red_ball_columns) and blue_ball_column in df.columns:
            # 将红球数据合并为一个长的数组
            red_balls = df[red_ball_columns].values.flatten()
            blue_balls = df[blue_ball_column].values

            # 统计红球和蓝球的频率
            red_ball_freq = pd.Series(red_balls).value_counts().sort_index()
            blue_ball_freq = pd.Series(blue_balls).value_counts().sort_index()

            # 可视化红球和蓝球的频率分布
            fig, ax = plt.subplots(1, 2, figsize=(14, 6))

            # 红球频率分布图
            ax[0].bar(red_ball_freq.index, red_ball_freq.values, color='red')
            ax[0].set_title('红球号码的频率分布')
            ax[0].set_xlabel('红球号码')
            ax[0].set_ylabel('出现频率')

            # 蓝球频率分布图
            ax[1].bar(blue_ball_freq.index, blue_ball_freq.values, color='blue')
            ax[1].set_title('蓝球号码的频率分布')
            ax[1].set_xlabel('蓝球号码')
            ax[1].set_ylabel('出现频率')

            st.pyplot(fig)

            # 显示热号和冷号
            top_red_balls = red_ball_freq.nlargest(5)
            bottom_red_balls = red_ball_freq.nsmallest(5)
            st.write("热号（出现频率最高的红球号码）：", top_red_balls)
            st.write("冷号（出现频率最低的红球号码）：", bottom_red_balls)

        else:
            st.error("Excel中没有正确的红球和篮球数据列，请检查列名。")

    except Exception as e:
        st.error(f"发生错误：{e}")
else:
    st.info("请上传包含历史数据的Excel文件。")
