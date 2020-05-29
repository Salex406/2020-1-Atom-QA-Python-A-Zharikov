from db.orm_model import Base, User
from db.mysql_orm_client import MysqlOrmConnection


class MysqlOrmBuilder:

    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        #self.engine = connection.connection.engine

    def add_user(self, user):
        self.connection.session.add(user)
        self.connection.session.commit()

    def del_user(self, user):
        self.connection.session.delete(user)
        self.connection.session.commit()

    def upd_access(self, user, value):
        user.access = value
        self.connection.session.commit()

    def get_users(self):
        for instance in self.connection.session.query(User).order_by(User.id):
            print(instance.username, instance.password, instance.access)
 
    def check_user(self, user):
        self.connection.session.commit()
        exists = self.connection.session.query(User.id).filter_by(username=user.username).scalar() is not None
        return exists

    def check_user_by_name(self, username):
        self.connection.session.commit()
        exists = self.connection.session.query(User.id).filter_by(username=username).scalar() is not None
        return exists

    def delete_user(self, user):
        self.connection.session.query(User.id).filter(User.username==user.username).delete()
        self.connection.session.commit()

    def get_datetime(self, user):
        self.connection.session.commit()
        for obj in self.connection.session.query(User).filter(User.username==user.username):
            return obj.start_active_time
  
    def get_active(self, user):
        self.connection.session.commit()
        for obj in self.connection.session.query(User).filter(User.username==user.username):
            return obj.active

    def get_access(self, user):
        self.connection.session.commit()
        obj = self.connection.session.query(User).filter(User.username==user.username).first()
        return obj.access
