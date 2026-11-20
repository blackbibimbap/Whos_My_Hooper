import streamlit as st
import io
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.patches import Circle, Rectangle, Arc
import plotly.express as px
from PIL import Image

st.set_page_config(layout="wide")
st.markdown("<style>div[data-testid='stSelectbox'] [data-testid='stWidgetLabel'] p {font-size: 1.5rem; font-weight: 700;}</style>", unsafe_allow_html=True)
st.title("Interactive NBA Shot Chart")

# Import data
COLS = ['PLAYER_NAME', 'EVENT_TYPE', 'LOC_X', 'LOC_Y', 'ACTION_TYPE', 'SHOT_TYPE']

def load_season_data(file_path):
    return pd.read_csv(file_path, usecols=COLS)

csv_files = sorted([f for f in os.listdir('.') if f.endswith('.csv')], reverse=True)

if not csv_files:
    st.error("No CSV files found in this folder. Please place your season files here.")
    st.stop()

season_options = {file.replace('.csv', ''): file for file in csv_files}


def player_seasons():
    m = {}
    for label, f in season_options.items():
        for p in pd.read_csv(f, usecols=['PLAYER_NAME'])['PLAYER_NAME'].dropna().unique():
            m.setdefault(p, []).append(label)
    return m

ps = player_seasons()

if 'season' not in st.session_state:
    st.session_state.season = list(season_options)[0]
if st.session_state.get('player') not in ps:
    st.session_state.player = next(p for p in sorted(ps) if st.session_state.season in ps[p])

col1, col2 = st.columns(2)

with col1:
    player_list = [p for p in sorted(ps) if st.session_state.season in ps[p]]
    selected_player = st.selectbox("Select a Player:", player_list, key='player')

with col2:
    selected_season_label = st.selectbox("Select Season:", ps[selected_player], key='season')

df = load_season_data(season_options[selected_season_label])

player_df = df[df['PLAYER_NAME'] == selected_player]


# Draw Court
def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    if ax is None:
        ax = plt.gca()

    floor = Rectangle((-250, -40), 500, 400, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=1, color=color)
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    outer_box = Rectangle((-80, -40), 160, 190, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-60.1, -40), 120.2, 190, linewidth=lw, color=color, fill=False)

    top_free_throw = Arc((0, 150), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    bottom_free_throw = Arc((0, 150), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle=(0, (6, 4)))

    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    corner_three_a = Rectangle((-220, -40), 0, 129.48, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -40), 0, 129.48, linewidth=lw, color=color)
    three_arc = Arc((0.7, 0), 475, 475, theta1=22.1, theta2=158.2, linewidth=lw, color=color)

    ax.plot([-84, -80], [10, 10], color=color, linewidth=lw)
    ax.plot([-84, -80], [30, 30], color=color, linewidth=lw)
    ax.plot([-84, -80], [65, 65], color=color, linewidth=lw)
    ax.plot([-84, -80], [100, 100], color=color, linewidth=lw)

    ax.plot([80, 84], [10, 10], color=color, linewidth=lw)
    ax.plot([80, 84], [30, 30], color=color, linewidth=lw)
    ax.plot([80, 84], [65, 65], color=color, linewidth=lw)
    ax.plot([80, 84], [100, 100], color=color, linewidth=lw)

    ax.set_aspect('equal')

    court_elements = [floor, hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc]

    for element in court_elements:
        ax.add_patch(element)

    return ax


def court_image():
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='none')
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_facecolor('none')
    ax.axis('off')
    draw_court(ax, color='#4A5568', lw=2)
    ax.set_xlim(-300, 300)
    ax.set_ylim(500, -100)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", transparent=True, dpi=120)
    plt.close(fig)
    return Image.open(buf)

court_img = court_image()


plot_df = player_df[player_df['EVENT_TYPE'].isin(["Made Shot", "Missed Shot"])].copy()
plot_df = plot_df[plot_df['LOC_Y'] <= 360]

dist = ((plot_df['LOC_X']**2 + plot_df['LOC_Y']**2) ** 0.5 / 10).round(0).astype(int)

def make_label(row):
    words = row['ACTION_TYPE'].split()
    return ' '.join(words[:-2] + [row['SHOT_TYPE'][:3]] + words[-2:])

plot_df['TOOLTIP'] = dist.astype(str) + "' " + plot_df.apply(make_label, axis=1)

pfig = px.scatter(
    plot_df, x='LOC_X', y='LOC_Y', color='EVENT_TYPE',
    color_discrete_map={'Made Shot': '#4ADE80', 'Missed Shot': 'red'},
    symbol='EVENT_TYPE', symbol_map={'Made Shot': 'circle', 'Missed Shot': 'x'},
    hover_name='TOOLTIP',
    hover_data={'EVENT_TYPE': False, 'LOC_X': False, 'LOC_Y': False},
)
pfig.update_traces(marker_size=7.5, opacity=0.7)
pfig.update_traces(marker=dict(size=9, line=dict(width=0.5)), selector=dict(name='Missed Shot'))
pfig.update_traces(hoverlabel=dict(bgcolor='#1f2937', font_color='#4ADE80'), selector=dict(name='Made Shot'))
pfig.update_traces(hoverlabel=dict(bgcolor='#1f2937', font_color='red'), selector=dict(name='Missed Shot'))

pfig.add_layout_image(source=court_img, xref="x", yref="y", x=-300, y=-100,
                      sizex=600, sizey=600, xanchor="left", yanchor="top", layer="below")
pfig.update_xaxes(range=[-300, 300], visible=False, constrain="domain")
pfig.update_yaxes(range=[540, -60], visible=False, scaleanchor="x")
pfig.update_layout(height=1000, margin=dict(l=0, r=0, t=0, b=0),
                   plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                   legend_title_text='',
                   legend=dict(x=0.01, y=0.99, xanchor='left', yanchor='top'))


st.plotly_chart(pfig, use_container_width=True)