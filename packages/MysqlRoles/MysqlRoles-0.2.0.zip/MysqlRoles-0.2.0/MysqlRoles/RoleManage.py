import pymysql
from MysqlRoles.RoleServ import RoleServ

class RoleManage(object):

    """
    RolePush:
        Functions to, from a source of truth, check a DB and make
        the mysql user table match.
        This class should only manage the client.

        Input:
            client: Address of server to make match the source of truth
            server: Address of source of Truth server (default: localhost)
    """

    # we need permission names by order
    permission_order = ["Select_priv", "Insert_priv", "Update_priv",
                        "Delete_priv", "Create_priv", "Drop_priv",
                        "Reload_priv", "Shutdown_priv", "Process_priv",
                        "File_priv", "Grant_priv", "References_priv",
                        "Index_priv", "Alter_priv", "Super_priv",
                        "Create_tmp_table_priv", "Lock_tables_priv",
                        "Execute_priv", "Repl_slave_priv",
                        "Repl_client_priv", "Create_view_priv",
                        "Show_view_priv", "Create_routine_priv",
                        "Alter_routine_priv", "Create_user_priv",
                        "Event_priv", "Trigger_priv", "Create_tablespace_priv"]

    def __init__(self, client, server="localhost"):
        """
        Get input and set up connections to be used with contexts (with) later.

        Standard dunder/magic method; returns nothing special.
        No special input validation.
        """
        self.server = server
        self.client = client
        self.central_con = pymysql.connect(host=self.server,
                                          db='_MysqlRoles',
                                          autocommit=True)
        self.client_con = pymysql.connect(host=self.client,
                                          db='mysql',
                                          autocommit=True)

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close mysql connections on destruction.
        """
        self.client_con.close()
        self.central_con.close()

    def get_users(self):
        """
        Get a list of users managed by this service.

        Returns a list of usernames managed by the service.
        """
        with self.central_con.cursor() as cursor:
            get_users = "select Name from user"
            cursor.execute(get_users)
            result = list(cursor.fetchall())
            return result

    def get_servers(self):
        """
        Get a list of servers managed by this service.

        Returns a list of server addresses managed by the service.
        """
        with self.central_con.cursor() as cursor:
            get_addresses = "select Address from host"
            cursor.execute(get_users)
            result = list(cursor.fetchall())
            return result

    def user_check(self):
        """
        Run a check against the host for consistency, reporting differences.
        """
        server = self.client
        should_users=None
        there_users=None
        # get list of users that should be on this host
        with self.central_con.cursor() as cursor:
            should_query = "select distinct(u.UserName) \
            from User u inner join \
            user_group_membership as ug on u.Name=ug.UserName \
            join access a on a.UserGroup=ug.GroupName inner join \
            host_group_membership as hg on \
            hg.HostName=a.HostGroup \
            where hg.HostName=%s"
            cursor.execute(should_query, (server))
            should_users = list(cursor.fetchall())
        # get list of users actually on the host
        with self.client_con.cursor() as cursor:
            there_query = "select distinct(User) from \
            mysql.user"
            cursor.execute(there_query)
            there_users = list(cursor.fetchall())
        missing_client = list(set(should_users) -
                              set(there_users) )
        missing_server = list(set(there_users) -
                              set(should_users) )
        okay_user = list(set(there_users)\
                         .intersection(should_users)_
        return [missing_client, missing_server , okay_user]

    def user_change(self, name, new_user=False):
        """
        Creates and/or updates a user.
        """
        with self.client_con.cursor() as cursor:
            if new_user:
                user_stmt = "create user if not exists %s"
                cursor.execute(user_stmt, (name))
            # May need to check if user exists, even though it should.
            perm_vals = [x=="Y" for x in self.get_privs(name)]
            perm_cols = self.permission_order
            user_priv_stmt = "update user set (%s)"
            for perm, col in zip(perm_vals, perm_cols):
                if perm:
                    cursor.execute("grant %s on *.* to %s", (col, name))
                else:
                    cursor.execute("revoke %s on *.* from %s", (col, name))

    def remove_user(self, name):
        """
        Removes a user from a database.
        Returns nothing.
        """
        with self.client_con.cursor() as cursor:
            cursor.execute("remove user %s", (name))


    def get_privs(self, user):
        """
        Get the privs of the user on the specified host.
        Returns a list of "Y" or "N" for each permission.
        Should return an empty list if no results.
        """
        host = self.client
        with self.central_con.cursor() as cursor:
            # get host groups that touch this host
            hg_query = "select GroupName from \
            host_group_membership where \
            HostName=%s"
            cursor.execute(hg_query, (host))
            hostgroups = list(cursor.fetchall())
            # get user groups that touch this user
            ug_query = "select GroupName from \
            user_group_membership where \
            UserName=%s"
            cursor.execute(ug_query, (user))
            usergroups = list(cursor.fetchall())
            # find all access that maps them
            ug_query = "select PermissionType from \
            access where UserGroup in (%s) and \
            HostGroup in (%s)"
            cursor.execute(ug_query,
                           (",".join(usergroups),
                            ",".join(hostgroups)))
            permissiontypes = list(cursor.fetchall())
            # logical or for each permission
            # return a list for each permission in order
            perm_query = "select \
            max(Select_priv) ,\
            max(Insert_priv) ,\
            max(Update_priv) ,\
            max(Delete_priv) ,\
            max(Create_priv) ,\
            max(Drop_priv) ,\
            max(Reload_priv) ,\
            max(Shutdown_priv) ,\
            max(Process_priv) ,\
            max(File_priv) ,\
            max(Grant_priv) ,\
            max(References_priv) ,\
            max(Index_priv) ,\
            max(Alter_priv) ,\
            max(Show_db_priv) ,\
            max(Super_priv) ,\
            max(Create_tmp_table_priv) ,\
            max(Lock_tables_priv) ,\
            max(Execute_priv) ,\
            max(Repl_slave_priv) ,\
            max(Repl_client_priv) ,\
            max(Create_view_priv) ,\
            max(Show_view_priv) ,\
            max(Create_routine_priv) ,\
            max(Alter_routine_priv) ,\
            max(Create_user_priv) ,\
            max(Event_priv) ,\
            max(Trigger_priv) ,\
            max(Create_tablespace_priv) \
            from permision_type where \
            Name in (%s)"
            cursor.execute(perm_query,
                           (",".join(permissiontypes))
            permissions = list(cursor.fetchall()[0])
            return permissions

    def update_users(self, remove=False):
        """
        Make the user inserts to add to the client, and add them.
        """
        for server in self.get_servers():
            users=self.user_check(server)
            for add_usr in users[0]:
                # add users missing on client
                self.user_change(add_usr, True)
            for update_usr in users[2]:
                # update permissions
                self.user_change(update_usr, False)
            if remove:
                # remove users on client but not server
                for rem_usr in users[1]:
                    self.remove_user(rem_usr)

    def cli(self):
        """
        Interact with command line.
        """
        pass
