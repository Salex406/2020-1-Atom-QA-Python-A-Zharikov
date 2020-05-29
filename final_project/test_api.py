import pytest
from base import BaseCase
from fixtures import *
from sqlalchemy.orm.exc import ObjectDeletedError
import time


class TestAPI(BaseCase):

    @pytest.mark.API
    def test_status(self, api):
        """
        CHECK STATUS CODE

        Step 1:
        Try connect to server and check status
        for 200

        EXPECT: status_code == 200
        """
        assert api.get_status().status_code == 200

    @pytest.mark.API
    def test_access_negative(self, api):
        """
        CHECK BLOCK USER API COMMAND

        Step 1:
        Add user to db
        Step 2:
        Block access via api request
        Step 3:
        Check access in db
        Check request answer

        EXPECT: status_code == 200, access == 0
        """
        self.builder.add_user(api.get_user())
        r1 = api.access_user(api.get_user(), False)
        access_false = self.builder.get_access(api.get_user())
        self.builder.del_user(api.get_user())
        assert access_false == 0
        assert r1.status_code == 200

    @pytest.mark.API
    def test_access_positive(self, api):
        """
        CHECK UNLOCK USER API COMMAND

        Step 1:
        Add user to db, update access to 0
        Step 2:
        Unlock access via api request
        Step 3:
        Check access in db
        Check request answer

        EXPECT: status_code == 200, access == 1
        """
        self.builder.add_user(api.get_user())
        self.builder.upd_access(api.get_user(), False)
        r1 = api.access_user(api.get_user(), True)
        access_true = self.builder.get_access(api.get_user())
        self.builder.del_user(api.get_user())
        assert access_true == 1
        assert r1.status_code == 200

    @pytest.mark.API
    def test_del_user(self, api):
        """
        CHECK DELETE USER API COMMAND

        Step 1:
        Add user to db
        Step 2:
        Delete user via api request
        Step 3:
        Check user in db
        Check request answer

        EXPECT: status_code == 204, user not in db(ObjectDeletedError)
        """
        self.builder.add_user(api.get_user())
        resp = api.del_user(api.get_user())
        assert resp.status_code == 204
        with pytest.raises(ObjectDeletedError):
            assert self.builder.check_user(api.get_user()) is False

    @pytest.mark.API
    def test_add_user(self, api):
        """
        CHECK ADD USER API COMMAND

        Step 1:
        Add user via api request
        Step 2:
        Delete user from db

        EXPECT: status_code == 201, no ObjectDeletedError
        """
        resp = api.add_user(api.get_user())
        self.builder.delete_user(api.get_user())
        assert resp.status_code == 201

    @pytest.mark.API
    def test_add_duplicate(self, api):
        """
        CHECK DUPLICATE SITUATION IN API REQUESTS

        Step 1:
        Add user to db
        Step 2:
        Try to add this user via api request

        EXPECT: status_code == 304
        """
        self.builder.add_user(api.get_user())
        resp = api.add_user(api.get_user())
        self.builder.del_user(api.get_user())
        assert resp.status_code == 304

    @pytest.mark.API
    def test_reg_duplicate_name(self, api):
        """
        CHECK DUPLICATE USERNAMES

        Step 1:
        Add user to db
        Step 2:
        Try to add user with same name via register page

        EXPECT: status_code == 304
        """
        self.builder.add_user(api.get_user())
        resp = api.reg_user(api.get_user().username, "E47gN@er.ty", "3", "3" )
        self.builder.del_user(api.get_user())
        assert resp.status_code == 304

    @pytest.mark.API
    def test_reg_duplicate_eml(self, api):
        """
        CHECK DUPLICATE EMAIL

        Step 1:
        Add user to db
        Step 2:
        Try to add user with same email via register page

        EXPECT: status_code == 304
        """
        self.builder.add_user(api.get_user())
        time.sleep(0.3)
        resp = api.reg_user("E47gN5R3", api.get_user().email, "3", "3")
        self.builder.del_user(api.get_user())
        assert resp.status_code == 304

    @pytest.mark.API
    def test_auth_code_positive(self, api):
        """
        CHECK LOGIN PAGE RSPONSE CODE IF LOGIN IS SUCCESS

        Step 1:
        Add user to db
        Step 2:
        Try to login via login page

        EXPECT: status_code == 200
        """
        self.builder.add_user(api.get_user())
        resp = api.login_user(api.get_user().username, api.get_user().password)
        self.builder.del_user(api.get_user())
        assert resp.status_code == 200

    @pytest.mark.API
    def test_auth_code_negative(self, api):
        """
        CHECK LOGIN PAGE RSPONSE CODE IF LOGIN IS FAIL

        Step 1:
        Try to login via login page

        EXPECT: status_code == 400
        """
        resp = api.login_user("QWERTY", "QWERTY")
        assert resp.status_code == 400
