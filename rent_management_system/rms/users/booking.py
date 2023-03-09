from flask import render_template, flash, redirect, url_for
from rms import app, db
from rms.models import Room, Booking
from datetime import datetime

