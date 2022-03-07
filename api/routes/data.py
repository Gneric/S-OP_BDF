import sys
from os import getcwd
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename, send_from_directory
from api.utils.dataLoader import createFileProductosOtros
from api.utils.functions import *
from flask_restful import Resource, abort
from datetime import datetime
from flask import request







