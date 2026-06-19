from __future__ import annotations
import streamlit as st


def page_header(title: str, subtitle: str | None = None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()


def info_box(text: str):
    st.info(text)


def warning_box(text: str):
    st.warning(text)


def success_box(text: str):
    st.success(text)


def error_box(text: str):
    st.error(text)
