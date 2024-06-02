from functools import wraps
from flask import Flask, render_template, request, session, flash, redirect


def logged_in(f):
    @wraps(f)
    def dec_func(*args, **kwargs):
        if session.get("loggin_in"):
            return f(*args, **kwargs)
        else:
            return redirect("/login")