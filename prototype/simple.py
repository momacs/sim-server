
'''
Several simple simulations testing various early-development aspects of PRAM.
'''

from pram.data   import GroupSizeProbe, ProbeMsgMode
from pram.entity import Group, GroupQry, GroupSplitSpec, Site
from pram.rule   import GoToRule, TimeInt
from pram.sim    import Simulation
from drule       import RuleDownloader

rd = RuleDownloader()
rd.downloadlocalrule("download.txt")

from pram.rule import DiscreteInvMarkovChain

#We are goint to donwload this rule and insert into the rule.py
# Then import it again
# ----------------------------------------------------------------------------------------------------------------------
# (0) Init:

progress_flu_rule = DiscreteInvMarkovChain('flu-status', { 's': [0.95, 0.05, 0.00], 'i': [0.00, 0.50, 0.50], 'r': [0.10, 0.00, 0.90] })
    # s - susceptible
    # i - infectious
    # r - recovered

sites = { 'home': Site('h'), 'work': Site('w') }

probe_grp_size_flu = GroupSizeProbe.by_attr('flu', 'flu-status', progress_flu_rule.get_states(), msg_mode=ProbeMsgMode.DISP, memo='Mass distribution across flu status')
probe_grp_size_site = GroupSizeProbe.by_rel('site', Site.AT, sites.values(), msg_mode=ProbeMsgMode.DISP, memo='Mass distribution across sites')


# ----------------------------------------------------------------------------------------------------------------------
# (1) Simulations testing the basic operations on groups and rules:

# (1.1) A single-group, single-rule (1g.1r) simulation:
s = Simulation()
s.add_rule(progress_flu_rule)
s.add_probe(probe_grp_size_flu)
s.add_group(Group('g0', 1000, { 'flu-status': 's' }))
s.run(24)

# (1.2) A single-group, two-rule (1g.2r) simulation:
# s = Simulation()
# s.add_rule(progress_flu_rule)
# s.add_rule(GoToRule(TimeInt(10,16), 0.4, 'home', 'work'))
# s.add_probe(probe_grp_size_flu)
# s.add_group(Group('g0', 1000, { 'flu-status': 's' }, { Site.AT: sites['home'], 'home': sites['home'], 'work': sites['work'] }))
# s.run(24)

# (1.3) As above (1g.2r), but with reversed rule order (which should not, and does not, change the results):
# s = Simulation()
# s.add_rule(GoToRule(TimeInt(10,16), 0.4, 'home', 'work'))
# s.add_rule(progress_flu_rule)
# s.add_probe(probe_grp_size_flu)
# s.add_group(Group('g0', 1000, { 'flu-status': 's' }, { Site.AT: sites['home'], 'home': sites['home'], 'work': sites['work'] }))
# s.run(24)

# (1.4) A two-group, two-rule (2g.2r) simulation (the groups don't interact via rules):
# s = Simulation()
# s.add_rule(progress_flu_rule)
# s.add_rule(GoToRule(TimeInt(10,16), 0.4, 'home', 'work'))
# s.add_probe(probe_grp_size_flu)
# s.add_group(Group('g0', 1000, attr={ 'flu-status': 's' }))
# s.add_group(Group('g1', 2000, rel={ Site.AT: sites['home'], 'home': sites['home'], 'work': sites['work'] }))
# s.run(24)

# (1.5) A two-group, two-rule (2g.2r) simulation (the groups do interact via one rule):
# s = Simulation()
# s.add_rule(progress_flu_rule)
# s.add_rule(GoToRule(TimeInt(10,16), 0.4, 'home', 'work'))
# s.add_probe(probe_grp_size_flu)
# s.add_group(Group('g0', 1000, { 'flu-status': 's' }, { Site.AT: sites['home'], 'home': sites['home'], 'work': sites['work'] }))
# s.add_group(Group('g1', 2000, { 'flu-status': 's' }))
# s.run(24)

# (1.6) A two-group, three-rule (2g.3r) simulation (same results, as expected):
# s = Simulation()
# s.add_rule(progress_flu_rule)
# s.add_rule(GoToRule(TimeInt(10,22), 0.4, 'home', 'work'))
# s.add_rule(GoToRule(TimeInt(10,22), 0.4, 'work', 'home'))
# s.add_probe(probe_grp_size_flu)
# s.add_group(Group('g0', 1000, { 'flu-status': 's' }, { Site.AT: sites['home'], 'home': sites['home'], 'work': sites['work'] }))
# s.add_group(Group('g1', 2000, { 'flu-status': 's' }, { Site.AT: sites['home'], 'home': sites['home'] }))
# s.run(24)


# ----------------------------------------------------------------------------------------------------------------------
# (2) Simulations testing rule interactions:

# (2.1) Antagonistic rules overlapping entirely in time (i.e., goto-home and goto-work; converges to a stable distribution):
# s = Simulation()
# s.add_rule(GoToRule(TimeInt(10,22), 0.4, 'home', 'work'))
# s.add_rule(GoToRule(TimeInt(10,22), 0.4, 'work', 'home'))
# s.add_probe(probe_grp_size_site)
# s.add_group(Group('g0', 1000, {}, { Site.AT: sites['home'], 'home': sites['home'], 'work': sites['work'] }))
# s.set_pragma_analyze(False)
# s.run(1).summary(False, end_line_cnt=(1,1))
# s.run(1).summary(False, end_line_cnt=(1,1))
# s.run(1).summary(False, end_line_cnt=(1,1))
# s.run(1).summary(False, end_line_cnt=(1,1))
# s.run(24)

# (2.2) Antagonistic rules overlapping mostly in time (i.e., goto-home and hoto-work; second rule "wins"):
# s = Simulation()
# s.add_rule(GoToRule(TimeInt(10,16), 0.4, 'home', 'work'))
# s.add_rule(GoToRule(TimeInt(10,22), 0.4, 'work', 'home'))
# s.add_probe(probe_grp_size_site)
# s.add_group(Group('g0', 1000, {}, { Site.AT: sites['home'], 'home': sites['home'], 'work': sites['work'] }))
# s.run(24)
