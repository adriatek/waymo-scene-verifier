import streamlit as st 
import pandas as pd




st.title("Waymo Scene Verifier")
st.caption("Mini V&V tool covering scenario coverage + automated checks on Waymo Open Dataset segments")


segments = pd.read_csv("segment_metadata.csv")
findings = pd.read_csv("findings.csv")

st.header("Segment Metadata")
st.dataframe(segments)

st.header("Defect Report")
st.dataframe(findings)

st.metric("Segments analyzed", len(segments))
st.metric("Findings", len(findings))
