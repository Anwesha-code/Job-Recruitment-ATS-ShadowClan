from __future__ import annotations
import streamlit as st


def metric_card(label: str, value: str | int | float, delta: str | None = None, help_text: str | None = None):
    st.metric(label=label, value=str(value), delta=delta, help=help_text)
