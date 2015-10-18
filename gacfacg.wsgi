activate_this = '/srv/http/gacfacg/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/srv/http/gacfacg/gacfacg')
from app import app as application
