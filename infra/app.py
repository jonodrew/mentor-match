#!/usr/bin/env python3

from aws_cdk import App

from infra.infra_stack import MentorMatchStack


app = App()
MentorMatchStack(app, "infra")

app.synth()
