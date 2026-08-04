"""Kumpulan grafik Plotly yang dipakai di semua halaman dashboard."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# warna senada dengan tema gelap neon portfolio
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

# palet gradient neon yang selalu dipakai
GRADIENT = ['#00f0ff', '#ff2ec4', '#8b5cf6', '#00ffa3', '#f97316', '#fbbf24', '#3b82f6', '#ec4899']

# layout dasar biar semua grafik rapi dan konsisten
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


def bar_chart(df, x_col, y_col, title='', color=None, horizontal=False, colors=None):
    """Bar chart support, bisa multi-series kalau kolom color diisi."""
    fig = go.Figure()

    if colors is None:
        colors = GRADIENT

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


def pie_chart(df, names_col, values_col, title='', hole=0.5):
    """Pie/donut chart dengan palet neon."""
    fig = go.Figure(go.Pie(
        labels=df[names_col],
        values=df[values_col],
        hole=hole,
        marker=dict(colors=GRADIENT[:len(df)], line=dict(color=COLORS['dark'], width=2)),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Nilai: %{value:,.0f} (%{percent})<extra></extra>'
    ))

    layout = dict(BASE_LAYOUT)
    layout['title'] = title
    fig.update_layout(**layout)
    return fig


def line_chart(df, x_col, y_col, title='', mode='lines+markers', area=False, color=None):
    """Line chart, bisa jadi area chart kalau area=True."""
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
    """Multi-line chart untuk bandingin beberapa seri data."""
    fig = go.Figure()

    for i, col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[col],
            mode='lines+markers',
            name=labels[col] if labels and col in labels else col,
            line=dict(color=GRADIENT[i % len(GRADIENT)], width=2.5),
            marker=dict(size=6),
            hovertemplate=f'{x_col}: %{{x}}<br>{col}: %{{y:,.2f}}<extra></extra>'
        ))

    layout = dict(BASE_LAYOUT)
    layout['title'] = title
    layout['yaxis'] = dict(gridcolor='rgba(255,255,255,0.08)', zerolinecolor='rgba(255,255,255,0.1)')
    layout['xaxis'] = dict(gridcolor='rgba(255,255,255,0.05)')
    fig.update_layout(**layout)
    return fig


def histogram(df, x_col, title='', nbins=20):
    """Histogram buat lihat distribusi data."""
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


def gauge_chart(value, title='', max_value=100, color=None):
    """Gauge chart buat nampilin capaian target."""
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


def scatter_chart(df, x_col, y_col, title='', color_col=None, size_col=None):
    """Scatter chart buat korelasi antar data."""
    fig = px.scatter(
        df, x=x_col, y=y_col,
        color=color_col, size=size_col if size_col else None,
        title=title,
        template='plotly_dark',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(**BASE_LAYOUT)
    return fig


def treemap(df, path_cols, values_col, title=''):
    """Treemap buat hirarki data."""
    fig = px.treemap(
        df, path=path_cols, values=values_col,
        title=title, template='plotly_dark'
    )
    fig.update_traces(marker=dict(cornerradius=5))
    fig.update_layout(**BASE_LAYOUT)
    return fig


def waterfall_chart(labels, values, title='', measure=None):
    """Waterfall chart, cocok buat laporan laba rugi."""
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


def stacked_bar_chart(df, x_col, y_col, color_col, title='', colors=None):
    """Stacked bar chart buat breakdown per kategori."""
    if colors is None:
        colors = GRADIENT

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


def kpi_card(title, value, delta=None, delta_color='normal', prefix='', suffix=''):
    """Kartu KPI dengan angka besar."""
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
