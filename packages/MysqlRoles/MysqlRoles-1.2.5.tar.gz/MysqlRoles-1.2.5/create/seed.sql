-- user creation
insert into user values ("%","Alan","mysql_native_password", password("Alan"));
insert into user values ("%","Danice","mysql_native_password", password("Danice"));
insert into user values ("%","Terry","mysql_native_password", password("Terry"));
insert into user values ("%","Rachel","mysql_native_password", password("Rachel"));
insert into user values ("%","Sam","mysql_native_password", password("Sam"));

-- db hosts
insert into host values ("report", "report", "main report host");
insert into host values ("staging", "staging", "main staging host");
insert into host values ("testing", "testing", "main testing host");
insert into host values ("cert", "cert", "main cert host");
insert into host values ("prod", "prod", "main prod host");
insert into host values ("ops", "ops", "main ops host");
insert into host values ("localhost", "127.0.0.1", "this server");

-- user groups
insert into user_group (Name) values ("Audit");
insert into user_group (Name) values ("Development");
insert into user_group (Name) values ("Testing");
insert into user_group (Name) values ("Reporting");
insert into user_group (Name) values ("Admin");

-- host groups
insert into host_group (Name) values ("all");
insert into host_group (Name) values ("dev_stack");
insert into host_group (Name) values ("preprod");
insert into host_group (Name) values ("prod");
insert into host_group (Name) values ("report");
insert into host_group (Name) values ("localhost");

-- permission types
insert into permission_type (Name, Select_priv, Show_db_priv) values ("read", "Y", "Y");
insert into permission_type (Name, Select_priv, File_priv, Show_db_priv) values ("readfile", "Y", "Y", "Y");
insert into permission_type (Name, Select_priv, Insert_priv, Update_priv, Delete_priv, Show_db_priv) values ("readwrite", "Y", "Y", "Y", "Y", "Y");
insert into permission_type (Name, Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv, Drop_priv, References_priv, Index_priv, Alter_priv, Show_db_priv) values
("schemachange", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y");
insert into permission_type (Name, Lock_tables_priv, Execute_priv, Repl_slave_priv, Repl_client_priv, Create_routine_priv, Alter_routine_priv, Create_user_priv, Event_priv, Trigger_priv, Create_tablespace_priv, Drop_priv, Show_db_priv) values
("admin", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y");
insert into permission_type values ("ALL", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y");

-- user group memberships
insert into user_group_membership values ("Alan", "Audit"), ("Danice", "Development"), ("Terry", "Testing"), ("Rachel", "Reporting"), ("Sam", "Admin");

-- insert into host groups
--  -- dev_stack
insert into host_group_membership values ("staging", "dev_stack"), ("testing", "dev_stack"), ("cert", "dev_stack"), ("prod", "dev_stack");
-- -- preprod
insert into host_group_membership values ("staging", "preprod"), ("testing", "preprod"), ("cert", "preprod");
-- -- prod
insert into host_group_membership values ("prod", "prod");
-- -- report
insert into host_group_membership values ("report", "report"), ("ops", "report");
-- -- all
insert into host_group_membership values ("report", "all"), ("staging", "all"), ("testing", "all"), ("cert", "all"), ("prod", "all"), ("ops", "all");
-- -- localhost
insert into host_group_membership values ("localhost", "localhost");


-- access grants
insert into access values ("Audit", "Audit", "all", "read", "");
insert into access values ("Development", "Development", "dev_stack", "schemachange", "");
insert into access values ("Testing", "Testing", "dev_stack", "readwrite", "");
insert into access values ("Reporting", "Reporting", "all", "readfile", "");
insert into access values ("Admin", "Admin", "all", "ALL", "");
insert into access values ("Testing_localhost", "Testing", "localhost", "readwrite", "");
