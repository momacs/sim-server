import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os, urllib, cv2

from pram.data   import GroupSizeProbe, ProbeMsgMode
from pram.entity import Group, GroupQry, GroupSplitSpec, Site
from pram.rule   import GoToRule, DiscreteInvMarkovChain, TimeInt
from pram.sim    import Simulation

# Streamlit encourages well-structured code, like starting execution in a main() function.
def main():
    # Render the readme as markdown using st.markdown.
    readme_text = st.markdown("#PRAM WEBSERVER v2")

    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("PRAM WEB v2")
    app_mode = st.sidebar.selectbox("Choose simulation",
        ["Show instructions", "01-simple", "Show the source code"])
    if app_mode == "Show instructions":
        st.sidebar.success('To continue select "Run the app".')
    elif app_mode == "Show the source code":
        readme_text.empty()
        st.code("# EMPTY")
    elif app_mode == "01-simple":
        readme_text.empty()
        run_the_app()

# This is the main app app itself, which appears when the user selects "Run the app".
def run_the_app():

    # Draw the UI elements to search for objects (pedestrians, cars, etc.)
    gsize, s1, s2, s3, i1, i2, i3, r1, r2, r3 = frame_selector_ui()

    progress_flu_rule = DiscreteInvMarkovChain('flu-status',
    { 's': [s1, s2, s3], 'i': [i1, i2, i3], 'r': [r1, r2, r3] })
    # s - susceptible
    # i - infectious
    # r - recovered

    sites = { 'home': Site('h'), 'work': Site('w') }

    probe_grp_size_flu = GroupSizeProbe.by_attr('flu', 'flu-status', progress_flu_rule.get_states(), msg_mode=ProbeMsgMode.DISP, memo='Mass distribution across flu status')
    probe_grp_size_site = GroupSizeProbe.by_rel('site', Site.AT, sites.values(), msg_mode=ProbeMsgMode.DISP, memo='Mass distribution across sites')

    data = ""
    s = Simulation()
    s.add_rule(progress_flu_rule)
    s.add_probe(probe_grp_size_flu)
    s.add_group(Group('g0', gsize, { 'flu-status': 's' }))
    sys.stdout = open('out.dat', 'w')
    s.run(24)
    sys.stdout.close()

    with open('out.dat') as file:
        data = file.readlines()
        data = str(self.data)
    st.write(data)

# This sidebar UI is a little search engine to find certain object types.
def frame_selector_ui():
    st.sidebar.markdown("# Paramaters")

    # Choose a frame out of the selected frames.
    gsize = st.sidebar.slider("Choose group size ", 1, 10000, 0)

    st.sidebar.markdown("### Susceptible")
    s1 = st.sidebar.number_input("[x,_, _]", key="s1")
    s2 = st.sidebar.number_input("[_,x,_]", key="s2")
    s3 = st.sidebar.number_input("[_,_,x]", key="s3")


    st.sidebar.markdown("### Infectious")
    i1 = st.sidebar.number_input("[x,_, _]", key="i1")
    i2 = st.sidebar.number_input("[_,x,_]", key="i2")
    i3 = st.sidebar.number_input("[_,_,x]", key="i3")


    st.sidebar.markdown("### Recovered")
    r1 = st.sidebar.number_input("[x,_, _]", key="r1")
    r2 = st.sidebar.number_input("[_,x,_]", key="r2")
    r3 = st.sidebar.number_input("[_,_,x]", key="r3")
    return gsize, s1, s2, s3, i1, i2, i3, r1, r2, r3

if __name__ == "__main__":
    main()
