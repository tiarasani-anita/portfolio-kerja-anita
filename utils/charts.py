"""
GRAFIK INTERAKTIF PLOTLY
==========================
Berisi fungsi pembuat grafik interaktif untuk dashboard portfolio:
bar chart, pie chart, line chart, dan area chart dengan styling premium.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Palet warna premium sesuai tema portfolio
COLORS = {
    'cyan': '#00f0ff',
    'magenta': '#ff2ec4',
    'purple': '#8b5cf6',
    'green': '#00ffa3',
    'blue': '#3b82f6',
    'orange': '#f97316',
    'yellow': '#fbbf24',
    'red': '#ef4444',
    'pink': '#ec4899',
    'dark': '#070b16',
    'card': '#0d1428',
    'text': '#eef4ff',
    'muted': '#93a4c3'
}

# Template layout dasar dengan tema gelap modern
BASE_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, Arial, sans-serif', color=COLORS['text'], size=12),
    title_font=dict(family='Sora, Arial, sans-serif', color=COLORS['text'], size=16),
    margin=dict(l=40, r=20, t=50, b=40),
    hoverlabel=dict(
        bgcolor=COLORS['card'],
        font_size=12,
        font_color=COLORS['text'],
        bordercolor=COLORS['cyan']
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=11),
        bgcolor='rgba(0,0,0,0)'
    )
)

# Gradient untuk chart
def _gradient_colors(n):
    """Menghasilkan n warna gradient neon."""
    from matplotlib import colormaps
    cmap = colormaps['viridis']
    return [f'rgb({int(r*255)},{int(g*255)},{int(b*255)})' for r, g, b, _ in [cmap(i/(n-1)) if n > 1 else cmap(0.5) for i in range(n)]]


# ============================================================
# 1. BAR CHART
# ============================================================
def bar_chart(df, x_col, y_col, title='', color=None, horizontal=False, colors=None):
    """Membuat bar chart interaktif."""
    fig = go.Figure()
    
    if colors is None:
        colors = [COLORS['cyan'], COLORS['magenta'], COLORS['purple']]
    
    # Jika ada kolom kategori (multi series)
    if color and color in df.columns:
        for i, cat in enumerate(df[color].unique()):
            sub = df[df[color] == cat]
            fig.add_trace(go.Bar(
                x=sub[x_col] if not horizontal else sub[y_col],
                y=sub[y_col] if not horizontal else sub[x_col],
                name=str(cat),
                text=sub[y_col].apply(lambda v: f'{v:,.0f}'),
                textposition='outside',
                marker=dict(color=colors[i % len(colors)], line=dict(color='rgba(255,255,255,0.2)', width=1)),
                hovertemplate=f'{x_col}: %{{x}}<br>{y_col}: %{{y:,.0f}}<extra></extra>'
            ))
    else:
        fig.add_trace(go.Bar(
            x=df[x_col] if not horizontal else df[y_col],
            y=df[y_col] if not horizontal else df[x_col],
            text=df[y_col].apply(lambda v: f'{v:,.0f}'),
            textposition='outside',
            marker=dict(color=colors[0], line=dict(color='rgba(255,255,255,0.2)', width=1)),
            hovertemplate=f'{x_col}: %{{x}}<br>{y_col}: %{{y:,.0f}}<extra></extra>'
        ))
    
    layout = dict(BASE_LAYOUT)
    layout['title'] = title
    layout['yaxis'] = dict(gridcolor='rgba(255,255,255,0.08)', zerolinecolor='rgba(255,255,255,0.1)')
    layout['xaxis'] = dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)')
    
    fig.update_layout(**layout)
    fig.update_xaxes(tickangle=-30 if not horizontal else 0)
    return fig


# ============================================================
# 2. PIE / DONUT CHART
# ============================================================
def pie_chart(df, names_col, values_col, title='', hole=0.5):
    """Membuat pie/donut chart interaktif."""
    # Gunakan palet warna neon
    palette = [COLORS['cyan'], COLORS['magenta'], COLORS['purple'], COLORS['green'],
               COLORS['blue'], COLORS['orange'], COLORS['yellow'], COLORS['pink']]
    
    fig = go.Figure(go.Pie(
        labels=df[names_col],
        values=df[values_col],
        hole=hole,
        marker=dict(colors=palette[:len(df)], line=dict(color=COLORS['dark'], width=2)),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Nilai: %{value:,.0f} (%{percent})<extra></extra>'
    ))
    
    layout = dict(BASE_LAYOUT)
    layout['title'] = title
    fig.update_layout(**layout)
    return fig


# ============================================================
# 3. LINE / AREA CHART
# ============================================================
def line_chart(df, x_col, y_col, title='', mode='lines+markers', area=False, color=None):
    """Membuat line chart atau area chart."""
    fig = go.Figure()
    
    if area:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y_col],
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color=COLORS['cyan'], width=2.5),
            marker=dict(size=6, color=COLORS['magenta'], line=dict(color='white', width=1)),
            hovertemplate=f'{x_col}: %{{x}}<br>{y_col}: %{{y:,.0f}}<extra></extra>'
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y_col],
            mode=mode,
            line=dict(color=COLORS['cyan'], width=2.5),
            marker=dict(size=7, color=COLORS['magenta'], line=dict(color='white', width=1.5)),
            hovertemplate=f'{x_col}: %{{x}}<br>{y_col}: %{{y:,.0f}}<extra></extra>'
        ))
    
    layout = dict(BASE_LAYOUT)
    layout['title'] = title
    layout['yaxis'] = dict(gridcolor='rgba(255,255,255,0.08)', zerolinecolor='rgba(255,255,255,0.1)')
    layout['xaxis'] = dict(gridcolor='rgba(255,255,255,0.05)')
    fig.update_layout(**layout)
    return fig


def multi_line_chart(df, x_col, y_cols, title='', labels=None):
    """Membuat multi-line chart."""
    fig = go.Figure()
    palette = [COLORS['cyan'], COLORS['magenta'], COLORS['green'], COLORS['yellow']]
    
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[col],
            mode='lines+markers',
            name=labels[col] if labels and col in labels else col,
            line=dict(color=palette[i % len(palette)], width=2.5),
            marker=dict(size=6),
            hovertemplate=f'{x_col}: %{{x}}<br>{col}: %{{y:,.2f}}<extra></extra>'
        ))
    
    layout = dict(BASE_LAYOUT)
    layout['title'] = title
    layout['yaxis'] = dict(gridcolor='rgba(255,255,255,0.08)', zerolinecolor='rgba(255,255,255,0.1)')
    layout['xaxis'] = dict(gridcolor='rgba(255,255,255,0.05)')
    fig.update_layout(**layout)
    return fig


# ============================================================
# 4. HISTOGRAM / DISTRIBUSI
# ============================================================
def histogram(df, x_col, title='', nbins=20):
    """Membuat histogram distribusi data."""
    fig = go.Figure(go.Histogram(
        x=df[x_col],
        nbinsx=nbins,
        marker=dict(color=COLORS['cyan'], line=dict(color='rgba(255,255,255,0.3)', width=1)),
        hovertemplate=f'{x_col}: %{{x}}<br>Frekuensi: %{{y}}<extra></extra>'
    ))
    
    layout = dict(BASE_LAYOUT)
    layout['title'] = title
    layout['yaxis'] = dict(gridcolor='rgba(255,255,255,0.08)')
    layout['xaxis'] = dict(gridcolor='rgba(255,255,255,0.05)')
    fig.update_layout(**layout)
    return fig


# ============================================================
# 5. GAUGE / PROGRESS CHART
# ============================================================
def gauge_chart(value, title='', max_value=100, color=None):
    """Membuat gauge chart untuk KPI."""
    if color is None:
        color = COLORS['cyan']
    
    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=value,
        number=dict(font=dict(size=28, color=color), suffix=''),
        title=dict(text=title, font=dict(size=14, color=COLORS['text'])),
        gauge=dict(
            axis=dict(range=[0, max_value], tickcolor=COLORS['muted']),
            bar=dict(color=color, thickness=0.25),
            bgcolor='rgba(255,255,255,0.05)',
            borderwidth=0,
            steps=[
                dict(range=[0, max_value*0.5], color='rgba(255,46,196,0.1)'),
                dict(range=[max_value*0.5, max_value*0.8], color='rgba(0,255,163,0.1)'),
                dict(range=[max_value*0.8, max_value], color='rgba(0,240,255,0.15)')
            ]
        )
    ))
    
    layout = dict(BASE_LAYOUT)
    layout['height'] = 260
    layout['margin'] = dict(l=40, r=40, t=60, b=30)
    fig.update_layout(**layout)
    return fig


# ============================================================
# 6. SCATTER / BUBBLE CHART
# ============================================================
def scatter_chart(df, x_col, y_col, title='', color_col=None, size_col=None):
    """Membuat scatter chart."""
    fig = px.scatter(
        df, x=x_col, y=y_col,
        color=color_col, size=size_col if size_col else None,
        title=title,
        template='plotly_dark',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(**BASE_LAYOUT)
    return fig


# ============================================================
# 7. TREEMAP (Hierarki)
# ============================================================
def treemap(df, path_cols, values_col, title=''):
    """Membuat treemap untuk visualisasi hierarki data."""
    fig = px.treemap(
        df, path=path_cols, values=values_col,
        title=title, template='plotly_dark'
    )
    fig.update_traces(marker=dict(cornerradius=5))
    fig.update_layout(**BASE_LAYOUT)
    return fig


# ============================================================
# 8. WATERFALL CHART (Laba Rugi)
# ============================================================
def waterfall_chart(labels, values, title='', measure=None):
    """
    Membuat waterfall chart untuk laporan laba rugi.
    
    Parameters:
    - labels: list nama tahap
    - values: list nilai
    - measure: list tipe ('relative'/'total')
    """
    if measure is None:
        measure = ['relative'] * (len(values) - 1) + ['total']
    
    fig = go.Figure(go.Waterfall(
        name='Laba Rugi',
        orientation='v',
        measure=measure,
        x=labels,
        y=values,
        text=[f'{v:,.0f}' for v in values],
        textposition='outside',
        connector=dict(line=dict(color='rgba(255,255,255,0.3)', width=1)),
        increasing=dict(marker=dict(color=COLORS['green'])),
        decreasing=dict(marker=dict(color=COLORS['red'])),
        totals=dict(marker=dict(color=COLORS['cyan']))
    ))
    
    layout = dict(BASE_LAYOUT)
    layout['title'] = title
    layout['yaxis'] = dict(gridcolor='rgba(255,255,255,0.08)', zerolinecolor='rgba(255,255,255,0.1)')
    layout['xaxis'] = dict(gridcolor='rgba(255,255,255,0.05)')
    fig.update_layout(**layout)
    return fig


# ============================================================
# 9. STACKED BAR CHART
# ============================================================
def stacked_bar_chart(df, x_col, y_col, color_col, title='', colors=None):
    """Membuat stacked bar chart."""
    if colors is None:
        colors = [COLORS['cyan'], COLORS['magenta'], COLORS['purple'], COLORS['green'],
                  COLORS['blue'], COLORS['orange']]
    
    fig = go.Figure()
    cats = df[color_col].unique()
    
    for i, cat in enumerate(cats):
        sub = df[df[color_col] == cat]
        fig.add_trace(go.Bar(
            x=sub[x_col], y=sub[y_col],
            name=str(cat),
            marker=dict(color=colors[i % len(colors)], line=dict(color='rgba(255,255,255,0.2)', width=1)),
            hovertemplate=f'{x_col}: %{{x}}<br>{cat}: %{{y:,.0f}}<extra></extra>'
        ))
    
    layout = dict(BASE_LAYOUT)
    layout['title'] = title
    layout['barmode'] = 'stack'
    layout['yaxis'] = dict(gridcolor='rgba(255,255,255,0.08)', zerolinecolor='rgba(255,255,255,0.1)')
    layout['xaxis'] = dict(gridcolor='rgba(255,255,255,0.05)')
    fig.update_layout(**layout)
    return fig


# ============================================================
# 10. KPI CARD VALUE
# ============================================================
def kpi_card(title, value, delta=None, delta_color='normal', prefix='', suffix=''):
    """Membuat kartu KPI sederhana."""
    fig = go.Figure(go.Indicator(
        mode='number+delta',
        value=value,
        number=dict(font=dict(size=32, color=COLORS['cyan']), prefix=prefix, suffix=suffix),
        delta=dict(
            reference=0,
            relative=False,
            position='top-right',
            font=dict(size=14),
            increasing=dict(color=COLORS['green']),
            decreasing=dict(color=COLORS['red'])
        ),
        title=dict(text=title, font=dict(size=14, color=COLORS['text']))
    ))
    layout = dict(BASE_LAYOUT)
    layout['height'] = 160
    layout['margin'] = dict(l=30, r=30, t=50, b=20)
    fig.update_layout(**layout)
    return fig

