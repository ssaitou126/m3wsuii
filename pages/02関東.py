import streamlit as st
import lxml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import json

# 年月日時設定
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).replace(
    tzinfo=None
)
nowday = now.strftime("%Y%m01")
nowyear = now.strftime("%Y")
thismonth = datetime.datetime(now.year, now.month, 1)
lastmonth = thismonth + datetime.timedelta(days=-1)
lastday = lastmonth.strftime("%Y%m01")
diff = now - thismonth
difday = diff.days
difsec = diff.seconds
diftime = int((difday * 24) + (difsec / 60 / 60))
tmrw = now + datetime.timedelta(days=1)
mdngt = datetime.datetime(tmrw.year, tmrw.month, tmrw.day, 0, 0, 0)
difhr = int((mdngt - now).total_seconds() / 60 / 60)


# グラフ描画関数
def grfdrw(url):
    rivdict = json.load(open("urls.json", "r"))
    urll = rivdict[url].replace("datelabel", lastday).replace("yearlabel", nowyear)
    urln = rivdict[url].replace("datelabel", nowday).replace("yearlabel", nowyear)
    dfls = pd.read_html(urll)
    dfns = pd.read_html(urln)
    dfll = dfls[1].iloc[2:-1, :]
    dfnn = dfns[1].iloc[2 : difday + 3, :]
    dfc = pd.concat([dfll, dfnn])
    df3w = dfc.iloc[-21:, 1:]
    df3wd = dfc.iloc[-21:, 0]
    tiklist = df3wd.values.tolist()
    newtik = [_[5:10] for _ in tiklist]

    df = df3w.replace(["^(?![+-]?(?:\d+\.?\d*|\.\d+)).+$"], "NaN", regex=True)
    arr = np.array(df, dtype=float).ravel()
    grf = pd.Series(arr)
    smin = grf.min()
    smax = grf.max()
    idx = 504 - difhr - 2
    if np.isnan(grf[idx]):
        srct = grf[idx - 1]
    else:
        srct = grf[idx]
    rname = f"{dfns[0].iloc[1,3]}　{dfns[0].iloc[1,1]}"
    headertxt = f'{rname}　　　　最大=　{smax}m　　最小=　{smin}m　　直近=　{srct}m'
    st.write(headertxt)

    x = [*range(0, 504)]
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(grf)
    ax.fill_between(x, grf, smin - 0.2, color="c", alpha=0.2)
    ax.set_xticks(np.arange(0, 504, 24), newtik, rotation=45)
    ax.set_ylim(smin - 0.2, smax + 0.2)
    ax.grid()
    st.pyplot(fig)


# チェックボックスの設定
st.sidebar.write("### 関東河川")
riv1 = st.sidebar.checkbox("久慈川")
if riv1:
    grfdrw("kujigawa")
riv2 = st.sidebar.checkbox("那珂川黒羽")
if riv2:
    grfdrw("kurobane")
riv3 = st.sidebar.checkbox("那珂川小口")
if riv3:
    grfdrw("koguti")
riv4 = st.sidebar.checkbox("那珂川御前山")
if riv4:
    grfdrw("gozen")
riv5 = st.sidebar.checkbox("鬼怒川宝積寺")
if riv5:
    grfdrw("housyaku")
riv6 = st.sidebar.checkbox("鬼怒川石井")
if riv6:
    grfdrw("isii")
riv7 = st.sidebar.checkbox("秋川")
if riv7:
    grfdrw("akikawa")
riv8 = st.sidebar.checkbox("相模川")
if riv8:
    grfdrw("sagami")
riv9 = st.sidebar.checkbox("狩野川")
if riv9:
    grfdrw("kano")

st.text("※国土交通省水文水質データベースのデータを利用して表示します")

# ホームページへのリンク
link1 = "[AyuZyのホームページ](https://sites.google.com/view/ayuzy)"
st.sidebar.markdown(link1, unsafe_allow_html=True)
