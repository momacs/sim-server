import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os, urllib
import sys

from pram.data   import GroupSizeProbe, ProbeMsgMode
from pram.entity import Group, GroupQry, GroupSplitSpec, Site
from pram.rule   import GoToRule, DiscreteInvMarkovChain, TimeInt
from pram.sim    import Simulation

class Test:
    def Run(self):
        # Render the readme as markdown using st.markdown.
        readme_text = st.markdown("#PRAM WEBSERVER v2")

        # Once we have the dependencies, add a selector for the app mode on the sidebar.
        st.sidebar.title("PRAM WEB v2")
        readme_text.empty()
        self.run_the_app()

    def run_the_app(self):
        st.write("Apple Sauce Test")


a = Test()
a.Run()

