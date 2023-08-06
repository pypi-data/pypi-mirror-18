import pymysql

class RoleServ(object):

    """
    RoleServ: Server tools for MysqlRoles.
        Functions for intializing the mysql source of truth server
        and functions associated with using it.
        This class should only manage the server.

        Input:
            serv: Address of source of Truth server (default: 127.0.0.1)
    """

    @staticmethod
    def sanitize(input, allowable_list=[], default="''"):
        """
        Sanitize inputs to avoid issues with pymysql.

        Takes in an input to sanitize.
        Optionally takes in an list of allowable values and a default.
        The default is returned if the input is not in the list.
        Returns a sanizized result.
        """
        # add general sanitization
        if (input in allowable_list or allowable_list == []):
            return input
        else:
            return default

    def __init__(self, server="127.0.0.1"):
        """
        Get input and set up connection to be used with contexts (with) later.

        Standard dunder/magic method; returns nothing special.
        No special input validation.
        """
        self.server = server
        tmp_connection = pymysql.connect(host=self.server,
                                          autocommit=True)
        tmp_connection.cursor().execute("create schema if not exists _MysqlRoles;")
        self.connection = pymysql.connect(host=self.server,
                                          db='_MysqlRoles',
                                          autocommit=True)

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close mysql connections on destruction.

        This method may not be necessary, but is here for good practice.
        """
        self.connection.close()

    def create_tables(self):
        """
        Create tables using the table_create.sql file in the create folder.

        Returns nothing.
        """
        with self.connection.cursor() as cursor:
            create_stmt = open('create/table_create.sql', 'r').read()
            cursor.execute(create_stmt)

    def test_seed_tables(self):
        """
        Seed table for testing, using the seed.sql file in the create folder.

        Returns nothing.
        """
        # TODO check if tables exist first
        with self.connection.cursor() as cursor:
            seed_table_stmt = open('create/seed.sql', 'r').read()
            cursor.execute(seed_table_stmt)

    """
    These next functions exist with the intent of use after everything has been
    set up.
    """

    def add_user(self, name, fromhost="%", plugin="mysql_native_password",
                 auth_str="*7ACE763ED393514FE0C162B93996ECD195FFC4F5"):
        """
        Add a user to the server if it does not yet exist.

        Raises a RuntimeError if the user already exists.
        Returns nothing.
        """
        name = RoleServ.sanitize(name)
        fromhost = RoleServ.sanitize(fromhost)
        plugin = RoleServ.sanitize(plugin)
        auth_str = RoleServ.sanitize(auth_str)
        # Note that the auth_str default is generated from password('changeme')
        with self.connection.cursor() as cursor:
            # check if user exists
            if cursor.execute("select (1) from user where UserName = %s",
                              (name)):
                # if so, error
                raise RuntimeError("User with username {0}\
                                   already exists.".format(name))
            # if not, add
            user_add_stmt = "insert into user values (%s, %s, %s, %s)"
            cursor.execute(user_add_stmt, (fromhost, name, plugin, auth_str))

    def add_host(self, address, name="", comments=""):
        """
        Add a host to the server if it does not yet exist.

        Raises a RuntimeError if the host already exists.
        Returns nothing.
        """
        address = RoleServ.sanitize(address)
        name = RoleServ.sanitize(name)
        comments = RoleServ.sanitize(comments)
        if name == "":
            name = address
        with self.connection.cursor() as cursor:
            # check if host exists
            if cursor.execute("select (1) from host where Name = %s",
                              (name)):
                # if so, error
                raise RuntimeError("Host with Name {0}\
                                   already exists.".format(name))
            # if not, add
            else:
                host_add_stmt = "insert into host values (%s, %s, %s)"
            cursor.execute(host_add_stmt, (name, address, comments))

    def add_host_group(self, name, description=""):
        """
        Add a host group to the server if it does not yet exist.

        Raises a RuntimeError if the host group already exists.
        Returns nothing.
        """
        name = RoleServ.sanitize(name)
        description = RoleServ.sanitize(description)
        with self.connection.cursor() as cursor:
            # check if host group exists
            if cursor.execute("select (1) from host_group where Name = %s",
                              (name)):
                # if so, error
                raise RuntimeError("Host group with Name {0}\
                                   already exists.".format(name))
            # if not, add
            hg_add_stmt = "insert into host_group values (%s, %s)"
            cursor.execute(hg_add_stmt, (name, description))

    def add_user_group(self, name, description=""):
        """
        Add a user group to the server if it does not yet exist.

        Raises a RuntimeError if the user group already exists.
        Returns nothing.
        """
        name = RoleServ.sanitize(name)
        description = RoleServ.sanitize(description)
        # Note that the auth_str default is generated from password('changeme')
        with self.connection.cursor() as cursor:
            # check if user group exists
            if cursor.execute("select (1) from user_group where Name = %s",
                              (name)):
                # if so, error
                raise RuntimeError("User group with Name {0}\
                                   already exists.".format(name))
            # if not, add
            ug_add_stmt = "insert into user_group values (%s, %s)"
            cursor.execute(ug_add_stmt, (name, description))

    def add_user_group_membership(self, username, groupname):
        """
        Add a user to a user group.

        Raises a RuntimeError if the user is already a member of the group.
        Raises a ValueError if the user does not exist.
        Raises a ValueError if the group does not exist.
        Returns nothing.
        """
        username = RoleServ.sanitize(username)
        groupname = RoleServ.sanitize(groupname)
        with self.connection.cursor() as cursor:
            # check if user exists
            if not cursor.execute("select (1) from user where UserName = %s",
                                  (username)):
                # if not, error
                raise ValueError("User with Name {0}\
                                   does not exist.".format(username))
            # check if user group exists
            if not cursor.execute("select (1) from user_group where Name = %s",
                                  (groupname)):
                # if not, error
                raise ValueError("User group with Name {0}\
                                   does not exist.".format(groupname))
            # if so, check if the membership exists already
            if cursor.execute("select (1) from user_group_membership\
                               where UserName = %s and GroupName = %s",
                              (username, groupname)):
                raise RuntimeError("{1} is already a member of\
                                   {2}".format(username, groupname))
            # if not, add it
            umem_add_stmt = "insert into user_group_membership\
                 values (%s, %s)"
            cursor.execute(umem_add_stmt, (username, groupname))

    def add_host_group_membership(self, hostname, groupname):
        """
        Add a host to a host group.

        Raises a RuntimeError if the host is already a member of the group.
        Raises a ValueError if the host does not exist.
        Raises a ValueError if the group does not exist.
        Returns nothing.
        """
        hostname = RoleServ.sanitize(hostname)
        groupname = RoleServ.sanitize(groupname)
        # Note that the auth_str default is generated from password('changeme')
        with self.connection.cursor() as cursor:
            # check if host exists
            if not cursor.execute("select (1) from host where Name = %s",
                                  (hostname)):
                # if not, error
                raise ValueError("Host with Name {0}\
                                   does not exist.".format(hostname))
            # check if host group exists
            if not cursor.execute("select (1) from host_group where Name = %s",
                                  (groupname)):
                # if not, error
                raise ValueError("Host group with Name {0}\
                                   does not exist.".format(groupname))
            # if so, check if the membership exists already
            if cursor.execute("select (1) from host_group_membership\
                               where HostName = %s and GroupName = %s",
                              (hostname, groupname)):
                raise RuntimeError("{1} is already a member of\
                                   {2}".format(hostname, groupname))
            # if not, add it
            hmem_add_stmt = "insert into host_group_membership\
             values (%s, %s)"
            cursor.execute(hmem_add_stmt, (hostname, groupname))

    def create_permission(self, name,  allgrant=False):
        """
        Create a permission type if it does not exist yet.

        Raises a RuntimeError if the permission already exists
        Does not check for duplicates.
        Returns nothing.
        """
        name = RoleServ.sanitize(name)
        # Note that the auth_str default is generated from password('changeme')
        allyes = ('"Y",'*29)[:-1]
        allno = ('"N",'*29)[:-1]
        if allgrant:
            allperm = allyes
        else:
            allperm = allno
        with self.connection.cursor() as cursor:
            # check if host group exists
            if cursor.execute("select (1) from permission_type where\
                                  Name = %s", (name)):
                # if not, error
                raise ValueError("Permission type with Name {0}\
                                   already exists.".format(name))
            ptype_add_stmt = "insert into permission_type values (%s, " + allperm + ")"
            cursor.execute(ptype_add_stmt, (name))

    def add_permission(self, name, grant, value="Y"):
        """
        Add a permission to a named permission group.
        Takes in the name of the permission to modify, which grant to perform.
        Optionally takes in a value, so that it can be used to revoke.
        grant should be a permission column name for user.
        Run for each permission desired to change

        Raises a ValueError if the permission type does not exist.
        Does not check for duplicates.
        Returns nothing.
        """
        name = RoleServ.sanitize(name)
        grant = RoleServ.sanitize(grant)
        value = RoleServ.sanitize(value, ["Y","N"], "N")
        # Note that the auth_str default is generated from password('changeme')
        with self.connection.cursor() as cursor:
            # check if permission type exists
            if not cursor.execute("select (1) from permission_type where\
                                  Name = %s", (name)):
                # if not, error
                raise ValueError("Permission type with Name {0}\
                                   does not exist.".format(name))
            perm_add_stmt = "update permission_type set " + grant + " =\
             %s where Name = %s limit 1"
            cursor.execute(perm_add_stmt, (value, name))

    def add_access(self, name, usergroup, hostgroup, permission, schema=""):
        """
        Give a user group access to a host group.

        Supports schema-level access, which defaults to empty.
        Empty Schema parameter means all schemas.
        Nonempty schema is treated like "grant (privs) on (schema) to (user)"

        Raises a RuntimeError if the the access grant exists by name.
        Raises a RuntimeError if the user access grant would be duplicated.
        Raises a ValueError if the host group does not exist.
        Raises a ValueError if the user group does not exist.
        Raises a ValueError if the permission type does not exist.
        Returns nothing.
        """
        name = RoleServ.sanitize(name)
        usergroup = RoleServ.sanitize(usergroup)
        hostgroup = RoleServ.sanitize(hostgroup)
        permission = RoleServ.sanitize(permission)
        schema = RoleServ.sanitize(schema)
        with self.connection.cursor() as cursor:
            # check if grant exists by name
            if cursor.execute("select (1) from access where Name = %s",
                              (name)):
                # if so, error
                raise RuntimeError("Access grant with Name {0}\
                                   already exists.".format(name))
            # check if grant exists by function
            if cursor.execute("select (1) from access where UserGroup = %s\
                              and HostGroup = %s",
                              (usergroup, hostgroup)):
                # if so, error
                raise RuntimeError("Access for {0} to {1} already\
                                   exists.".format(usergroup, hostgroup))
            # check if user group exists
            if not cursor.execute("select (1) from user_group where Name = %s",
                                  (usergroup)):
                # if not, error
                raise ValueError("User group with Name {0}\
                                   does not exist.".format(usergroup))
            # check if host group exists
            if not cursor.execute("select (1) from host_group where Name = %s",
                                  (hostgroup)):
                # if not, error
                raise ValueError("Host group with Name {0}\
                                   does not exist.".format(hostgroup))
            # check if permission type exists
            if not cursor.execute("select (1) from permission_type where\
                                  Name = %s",
                                  (permission)):
                # if not, error
                raise ValueError("Permission type with Name {0}\
                                   does not exist.".format(permission))
            # if all OK, add
            ag_add_stmt = "insert into access values (%s, %s, %s, %s, %s)"
            cursor.execute(ag_add_stmt, (name, usergroup, hostgroup,
                                         permission, schema))
