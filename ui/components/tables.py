from __future__ import annotations
import pandas as pd
import streamlit as st


def render_top100_table(rows: list[dict]):
    if not rows:
        st.info("No data to display")
        return

    df = pd.DataFrame(rows)
    display_cols = [c for c in ["rank", "candidate_id", "final_score", "jd_coverage",
                                  "retrieval_intelligence", "evidence_score",
                                  "ownership_score", "career_alignment_score",
                                  "behavior_super_score", "availability", "profile_title"]
                    if c in df.columns]

    if "rank" in df.columns:
        df["rank"] = df["rank"].astype(int)

    for c in display_cols:
        if c not in ("rank", "candidate_id", "profile_title"):
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").round(4)

    st.dataframe(
        df[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "final_score": st.column_config.NumberColumn("Score", format="%.2f"),
        },
    )
