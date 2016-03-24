activate_this = '/opt/gacfacg/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/opt/gacfacg/gacfacg')
from app import app as application
