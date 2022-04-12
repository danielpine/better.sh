import logging
import sys

from tools.PySqlTemplate import PySqlTemplate
sys.path.append("..")
sys.path.append(".")

log = logging.getLogger(__name__)


class LoginService(object):

    def findUser(self, user, passwd):
        return PySqlTemplate.findOne('select * from user where username=? and passwd=?', user, passwd)

    def findUserByPhone(self, phone):
        return PySqlTemplate.findOne('select * from user where phone=?', phone)
