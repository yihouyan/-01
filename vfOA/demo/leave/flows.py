#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2023-11-7
# software: PyCharm


from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.flow import views as flow_views

from .models import *
from .views import *

@frontend.register
class LeaveFlow(Flow):
    process_class = LeaveProcess
    summary_template = "{{ process.leave.req_by.user.username }}的请假"
    process_title = '请假'

    start = (
        flow.Start(
            LeaveStartView
        ).Permission(
            auto_create=True
        ).Next(this.dep_approve)
    )

    dep_approve = (
        flow.View(
            approve_check
        ).Assign(
            lambda act: act.process.leave.req_by.Manager.user
        ).Next(
            this.check_dep_approve)
    )

    check_dep_approve = (
        flow.If(lambda activation: activation.process.dep_approved==1)
            .Then(this.hr_approve)
            .Else(this.NG)
    )

    hr_approve = (
        flow.View(
            approve_check
        ).Permission(
            auto_create=True
        ).Next(
            this.check_hr_approve
        )
    )

    check_hr_approve = (
        flow.If(lambda activation: activation.process.hr_approved==1)
            .Then(this.OK)
            .Else(this.NG)
    )
    NG = (
        flow.Handler(
            this.send_NG_request
        ).Next(this.end)
    )
    OK = (
        flow.Handler(
            this.send_OK_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_NG_request(self, activation):
        print('dep_approved==>'+ str(activation.process.dep_approved))
        print('hr_approved==>' + str(activation.process.hr_approved))
        print('NG')

    def send_OK_request(self, activation):
        print('OK')