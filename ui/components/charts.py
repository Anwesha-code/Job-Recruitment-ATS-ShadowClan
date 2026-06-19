from __future__ import annotations
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def score_distribution(scores: list[float], title: str = "Score Distribution"):
    fig = px.histogram(
        x=scores, nbins=20,
        labels={"x": "Final Score"},
        title=title,
        color_discrete_sequence=["#1f77b4"],
    )
    fig.update_layout(bargap=0.05, height=300)
    st.plotly_chart(fig, use_container_width=True)


def feature_contribution_chart(row: dict):
    features = {
        "JD Coverage": float(row.get("jd_coverage", 0) or 0),
        "Evidence": float(row.get("evidence_score", 0) or 0),
        "Retrieval Intelligence": float(row.get("retrieval_intelligence", 0) or 0),
        "Behavior": float(row.get("behavior_super_score", 0) or 0),
        "Ownership": float(row.get("ownership_score", 0) or 0),
        "Career Alignment": float(row.get("career_alignment_score", 0) or 0),
        "Availability": float(row.get("availability", 0) or 0),
    }
    df = pd.DataFrame({
        "Feature": list(features.keys()),
        "Score (0-1)": list(features.values()),
    })
    df = df.sort_values("Score (0-1)", ascending=True)
    fig = px.bar(
        df, y="Feature", x="Score (0-1)",
        orientation="h", title="Feature Scores",
        color="Score (0-1)", color_continuous_scale="Blues",
        text_auto=".3f",
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)


def experience_distribution(rows: list[dict]):
    vals = [float(r.get("years_of_experience", 0) or 0) for r in rows]
    fig = px.histogram(
        x=vals, nbins=20,
        labels={"x": "Years of Experience"},
        title="Experience Distribution (Top-100)",
        color_discrete_sequence=["#ff7f0e"],
    )
    fig.update_layout(bargap=0.05, height=300)
    st.plotly_chart(fig, use_container_width=True)


def correlation_heatmap(rows: list[dict]):
    features = ["jd_coverage", "retrieval_intelligence", "evidence_score",
                "ownership_score", "career_alignment_score",
                "behavior_super_score", "honeypot_probability"]
    df = pd.DataFrame(rows)
    avail = [c for c in features if c in df.columns]
    if len(avail) < 2:
        st.info("Not enough feature columns for correlation heatmap")
        return
    corr = df[avail].corr()
    fig = px.imshow(
        corr.values,
        x=corr.columns,
        y=corr.columns,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        text_auto=".2f",
        title="Feature Correlation Heatmap (Top-100)",
        aspect="auto",
    )
    fig.update_layout(height=max(400, len(avail) * 60))
    st.plotly_chart(fig, use_container_width=True)


def honeypot_gauge(hp_prob: float):
    color = "#00cc66" if hp_prob <= 0.1 else ("#ffaa00" if hp_prob <= 0.3 else "#ff4444")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=hp_prob * 100,
        title={"text": "Honeypot Risk %"},
        number={"suffix": "%"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 10], "color": "#e8f5e9"},
                {"range": [10, 30], "color": "#fff3e0"},
                {"range": [30, 100], "color": "#ffebee"},
            ],
        },
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)
