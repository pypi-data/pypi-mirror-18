from ejabberdctl import ejabberdctl


class ejabberdctl_tests(object):
    '''
    ejabberdctl.py testing suite.
    '''

    def __init__(self, server, username, password):
        '''
        Initialise the testing suite for
        Ejabberd XML-RPC Administration API client.
        '''
        self.server = server
        self.username = username
        self.password = password
        self.ctl = ejabberdctl(server, username, password)

    def run_all(self):
        '''
        Run all tests.
        '''
        print('\nRunning all implemented ejabberdctl.py tests:')
        print('---------------------------------------------\n\n')
        self.test_add_rosteritem()
        self.test_check_account()
        self.test_connected_users()
        self.test_connected_users_info()
        self.test_connected_users_number()
        self.test_connected_users_vhost()
        self.test_delete_rosteritem()
        self.test_get_cookie()
        self.test_get_last()
        self.test_get_loglevel()
        self.test_get_roster()
        self.test_kick_session()
        self.test_kick_user()
        self.test_list_cluster()
        self.test_num_active_users()
        self.test_num_resources()
        self.test_reload_config()
        self.test_reopen_log()
        self.test_resource_num()
        self.test_set_loglevel()
        self.test_stats()
        self.test_stats_host()
        self.test_status()
        self.test_status_list()
        self.test_status_list_host()
        self.test_status_num()
        self.test_status_num_host()
        self.test_user_resources()
        self.test_user_sessions_info()
        # self.test_restart()
        # self.test_stop()

    def test_add_rosteritem(self):
        '''
        Test ``add_rosteritem``.
        '''
        print('add_rosteritem(localuser,localserver,user,server,nick,group,subs)')
        response = self.ctl.add_rosteritem(self.username, self.server,
                                           'test2', self.server,
                                           'test2', 'Contacts', 'both')
        print(response)
        print('')
        assert response['res'] == 0

    # TODO def backup(self, file): Store the database to backup file

    # TODO def ban_account(user, host, reason)

    # TODO def change_password(user, host, newpass)

    # TODO def change_room_option(self, name, service, option, value) - Change an option in a MUC room

    def test_check_account(self):
        '''
        Test ``check_account``.
        '''
        print('check_account(user, host)')
        response = self.ctl.check_account(self.username, self.server)
        print(response)
        print('')
        assert response['res'] == 0

    # TODO def check_password(user, host, password)

    # check_password_hash(user, host, passwordhash, hashmethod)

    # TODO def compile(self, file): Recompile and reload Erlang source code file

    def test_connected_users(self):
        print('connected_users()')
        response = self.ctl.connected_users()
        print(response)
        print('')
        assert isinstance(response['connected_users'], list)

    def test_connected_users_info(self):
        '''
        Test ``connected_users_info``.
        '''
        print('connected_users_info()')
        response = self.ctl.connected_users_info()
        print(response)
        print('')
        assert isinstance(response['connected_users_info'], list)

    def test_connected_users_number(self):
        '''
        Test ``connected_users_number``.
        '''
        print('connected_users_number()')
        response = self.ctl.connected_users_number()
        print(response)
        print('')
        assert isinstance(response['num_sessions'], int)

    def test_connected_users_vhost(self):
        '''
        Test ``connected_users_vhost``.
        '''
        print('connected_users_vhost(host)')
        response = self.ctl.connected_users_vhost(self.server)
        print(response)
        print('')
        assert isinstance(response['connected_users_vhost'], list)

    # TODO def convert_to_scram(self, host): Convert the passwords in ‘users’ SQL table to SCRAM

    # TODO def convert_to_yaml(self, in, out): Convert the input file from Erlang to YAML format

    # TODO def create_room(self, name, service, host): Create a MUC room name@service in host

    # TODO def create_room_with_opts(self, name, service, host, options): Create a MUC room name@service in host with given options

    # TODO def create_rooms_file(self, file): Create the rooms indicated in file

    # TODO def delete_expired_messages()

    # TODO def delete_mnesia(self, host): Export all tables as SQL queries to a file

    # TODO def delete_old_mam_messages(self, type, days): Delete MAM messages older than DAYS

    # TODO def delete_old_messages(days)

    # TODO def delete_old_users(days)

    # TODO def delete_old_users_vhost(host, days)

    def test_delete_rosteritem(self):
        '''
        Test ``delete_rosteritem``.
        '''
        print('delete_rosteritem(localuser, localserver, user, server)')
        response = self.ctl.delete_rosteritem(self.username, self.server, 'test2', self.server)
        print(response)
        print('')
        assert response['res'] == 0

    # TODO def destroy_room(self, name, service): Destroy a MUC room

    # TODO def destroy_rooms_file(self, file): Destroy the rooms indicated in file. Provide one room JID per line.

    # TODO def dump(self, file): Dump the database to text file

    # TODO def dump_table(self, file, table): Dump a table to text file

    # TODO def export2sql(self, host, file): Export virtual host information from Mnesia tables to SQL files

    # TODO def export_piefxis(self, dir): Export data of all users in the server to PIEFXIS files (XEP-0227)

    # TODO def export_piefxis_host(self, dir, host): Export data of users in a host to PIEFXIS files (XEP-0227)

    # TODO def gen_html_doc_for_commands(self, file, regexp, examples): Generates html documentation for ejabberd_commands

    # TODO def gen_markdown_doc_for_commands(self, file, regexp, examples): Generates markdown documentation for ejabberd_commands

    def test_get_cookie(self):
        '''
        Test ``get_cookie``.
        '''
        print('get_cookie()')
        response = self.ctl.get_cookie()
        print(response)
        print('')
        assert isinstance(response['cookie'], str)

    def test_get_last(self):
        '''
        Test ``get_last``.

        15.07 - call won't throw an exception when user does not exist, or has no activity recorded

        16.09 - call throws an exception and the process crashes in ejabberd
        '''
        print('get_last(user, host)')
        try:
            response = self.ctl.get_last(self.username, self.server)
            print(response)
            print('')
            assert isinstance(response['last_activity'], str)
        except Exception, e:
            print(e)

    def test_get_loglevel(self):
        '''
        Test ``get_loglevel``.
        '''
        print('get_loglevel()')
        response = self.ctl.get_loglevel()
        print(response)
        print('')
        assert isinstance(response['leveltuple'], list)

    # TODO def get_offline_count(self): Get the number of unread offline messages

    # TODO def get_room_affiliations(self, name, service): Get the list of affiliations of a MUC room

    # TODO def get_room_occupants(self, name, service): Get the list of occupants of a MUC room

    # TODO def get_room_occupants_number(self, name, service): Get the number of occupants of a MUC room

    # TODO def get_room_options(self, name, service): Get options from a MUC room

    def test_get_roster(self):
        '''
        Test ``get_roster``.

        15.07 - call won't throw an exception when user does not exist

        16.09 - call throws an exception and the process crashes in ejabberd
        '''
        print('get_roster(user, host)')
        try:
            response = self.ctl.get_roster(self.username, self.server)
            print(response)
            print('')
            assert isinstance(response['contacts'], list)
        except Exception, e:
            print(e)

    # TODO def get_subscribers(self, name, service): List subscribers of a MUC conference

    # TODO def get_user_rooms(self, user, host): Get the list of rooms where this user is occupant

    # TODO def get_vcard(user, host, name)

    # TODO def get_vcard2(user, host, name, subname)

    # TODO def get_vcard2_multi(user, host, name, subname)

    # TODO def import_dir(self, file): Import users data from jabberd14 spool dir

    # TODO def import_file(self, file): Import users data from jabberd14 spool file

    # TODO def import_piefxis(self, file): Import users data from a PIEFXIS file (XEP-0227)

    # TODO def import_prosody(self, dir) Import data from Prosody

    # TODO incoming_s2s_number()

    # TODO def install_fallback(self, file): Install the database from a fallback file

    # TODO def join_cluster(self, node): Join this node into the cluster handled by Node

    def test_kick_session(self):
        '''
        Test ``kick_session``.
        '''
        print('kick_session(user, host, resource, reason)')
        response = self.ctl.kick_session(self.username, self.server, 'test', 'test')
        print(response)
        print('')
        assert response['res'] == 0

    def test_kick_user(self):
        '''
        Test ``kick_user``.
        '''
        print('kick_user(user, host)')
        response = self.ctl.kick_user(self.username, self.server)
        print(response)
        print('')
        assert isinstance(response['num_resources'], int)

    # TODO def leave_cluster(self, node): Remove node handled by Node from the cluster

    def test_list_cluster(self):
        '''
        Test ``list_cluster``.

        Test listing nodes that are part of the cluster handled by Node.
        '''
        print('list_cluster()')
        try:
            response = self.ctl.list_cluster()
            print(response)
            print('')
            assert isinstance(response['nodes'], list)
        except Exception, e:
            print(e)
            print('')

    # TODO def load(self, file): Restore the database from text file

    # TODO def mnesia_change_nodename(self, oldnodename, newnodename, oldbackup, newbackup): Change the erlang node name in a backup file

    # TODO def module_check(self, module):

    # TODO def module_install(self, module):

    # TODO def module_uninstall(self, module):

    # TODO def module_upgrade(self, module):

    # TODO def modules_available()

    # TODO def modules_installed()

    # TODO def modules_update_specs(self):

    # TODO def muc_online_rooms(self, host): List existing rooms (‘global’ to get all vhosts)

    # TODO def muc_unregister_nick(self, nick): Unregister the nick in the MUC service

    def test_num_active_users(self):
        '''
        Test ``num_active_users``.

        Get number of users active in the last days.

        Arguments:

        host :: binary

            Name of host to check

        days :: integer

            Number of days to calculate sum

        Result:

        {users,integer}

        Number of users active on given server in last n days
        '''
        print('num_active_users(host, days)')
        response = self.ctl.num_active_users(self.server, 1)
        print(response)
        print('')
        try:
            assert isinstance(response['users'], int)
        except:
            assert response['users'] == ''

    def test_num_resources(self):
        '''
        Test ``num_resources``.

        Get the number of resources of a user.

        Arguments:

        user :: binary

            User name
        host :: binary

            Server name

        Result:

        {resources,integer}

            Number of active resources for a user

        '''
        print('num_resources(user, host)')
        response = self.ctl.num_resources(self.username, self.server)
        print(response)
        print('')
        assert isinstance(response['resources'], int)

    # TODO def outgoing_s2s_number()

    # TODO def privacy_set(self, user, host, xmlquery): Send a IQ set privacy stanza for a local account

    # TODO def private_get(self, user, host, element, ns): Get some information from a user private storage

    # TODO def private_set(self, user, host, element): Set to the user private storage

    # TODO def process_rosteritems(action, subs, asks, users, contacts)

    # TODO def push_alltoall(host, group)

    # TODO def push_roster(self, file, user, host): Push template roster from file to a user

    # TODO def push_roster_all(self, file): Push template roster from file to all those users

    # TODO def register(user, host, password)

    # TODO def registered_users(host)

    # TODO def registered_vhosts()

    def test_reload_config(self):
        '''
        Test ``reload_config``.

        Reload config file in memory (only affects ACL and Access).

        Result:

        {res,rescode}

        '''
        print('reload_config()')
        response = self.ctl.reload_config()
        print(response)
        print('')
        assert response['res'] == 0
        assert isinstance(response['res'], int)

    # TODO def remove_node(node)

    def test_reopen_log(self):
        '''
        Test ``reopen_log``.

        Reopen the log files.

        Result:

        {res,rescode}

        '''
        print('reopen_log()')
        response = self.ctl.reopen_log()
        print(response)
        print('')
        assert response['res'] == 0
        assert isinstance(response['res'], int)

    def test_resource_num(self):
        '''
        Test ``resource_num``.

        Resource string of a session number.

        Arguments:

        user :: binary

            User name

        host :: binary

            Server name

        num :: integer

            ID of resource to return

        Result:

        {resource,string}

            Name of user resource

        '''
        print('resource_num(user, host, num)')
        try:
            response = self.ctl.resource_num(self.username, self.server, 1)
            print(response)
            print('')
            assert isinstance(response['resource'], str)
        except Exception, e:
            print('{}\n'.format(e))

    def test_restart(self):
        '''
        Test ``restart``.

        Restart ejabberd gracefully.

        Result:

        {res,rescode}

        '''
        print('restart()')
        response = self.ctl.restart()
        print(response)
        print('')
        assert response['res'] == 0
        assert isinstance(response['res'], int)

    # TODO def restore(self, file): Restore the database from backup file

    # TODO def rooms_unused_destroy(self, host, days): Destroy the rooms that are unused for many days in host

    # TODO def rooms_unused_list(self, host, days): List the rooms that are unused for many days in host

    # TODO def rotate_log(self): Rotate the log files

    # TODO def send_direct_invitation(self, name, service, password, reason, users): Send a direct invitation to several destinations

    # TODO def send_message(type, from_jid, to, subject, body)

    # TODO def send_stanza(self, from, to, stanza): Send a stanza; provide From JID and valid To JID

    # TODO def send_stanza_c2s(user, host, resource, stanza)

    # TODO def set_last(user, host, timestamp, status)

    def test_set_loglevel(self):
        '''
        Test ``set_loglevel``.
        Set the loglevel (0 to 5)

        Arguments:

            loglevel :: integer

        Result:

        {logger,atom}

        '''
        print('set_loglevel(loglevel)')
        try:
            response = self.ctl.set_loglevel(5)
            print(response)
            print('')
            assert isinstance(response['logger'], str)
        except Exception, e:
            print(e)
            print('')

    # TODO def set_master(nodename)

    # TODO def set_nickname(user, host, nickname)

    # TODO def set_presence(user, host, resource, type, show, status, priority)

    # TODO def set_room_affiliation(self, name, service, jid, affiliation): Change an affiliation in a MUC room

    # TODO def set_vcard(user, host, name, content)

    # TODO def set_vcard2(user, host, name, subname, content)

    # TODO def set_vcard2_multi(user, host, name, subname, contents)

    # TODO def srg_create(group, host, name, description, display)

    # TODO def srg_delete(group, host)

    # TODO def srg_get_info(group, host)

    # TODO def srg_get_members(group, host)

    # TODO def srg_list(host)

    # TODO def srg_user_add(user, host, group, grouphost)

    # TODO def srg_user_del(user, host, group, grouphost)

    def test_stats(self):
        '''
        Test ``stats``.

        Get statistical value: registeredusers onlineusers onlineusersnode uptimeseconds processes

        Arguments:

            name :: binary

        Result:

        {stat,integer}

        '''
        print('stats(\'registeredusers\')')
        response = self.ctl.stats('registeredusers')
        print(response)
        print('')
        assert isinstance(response['stat'], int)
        print('stats(\'onlineusers\')')
        response = self.ctl.stats('onlineusers')
        print(response)
        print('')
        assert isinstance(response['stat'], int)
        print('stats(\'onlineusersnode\')')
        response = self.ctl.stats('onlineusersnode')
        print(response)
        print('')
        assert isinstance(response['stat'], int)
        print('stats(\'uptimeseconds\')')
        response = self.ctl.stats('uptimeseconds')
        print(response)
        print('')
        assert isinstance(response['stat'], int)
        print('stats(\'processes\')')
        try:
            response = self.ctl.stats('processes')
            print(response)
            print('')
            assert isinstance(response['stat'], int)
        except Exception, e:
            print(e)
            print('')

    def test_stats_host(self):
        '''
        Test ``stats_host``.

        Get statistical value for this host: registeredusers onlineusers

        Arguments:

            name :: binary
            host :: binary

        Result:

        {stat,integer}

        '''
        print('stats_host(\'registeredusers\', host)')
        response = self.ctl.stats_host('registeredusers', self.server)
        print(response)
        print('')
        assert isinstance(response['stat'], int)
        print('stats_host(\'onlineusers\', host)')
        response = self.ctl.stats_host('onlineusers', self.server)
        print(response)
        print('')
        assert isinstance(response['stat'], int)

    def test_status(self):
        '''
        Test ``status``.
        '''
        print('status()')
        response = self.ctl.status()
        print(response)
        print('')
        assert response['res'] == 0

    def test_status_list(self):
        '''
        Test ``status_list``.

        List of logged users with this status.

        Arguments:

            status :: binary

        Result:

        {users,{list,{userstatus,{tuple,[{user,string}, {host,string}, {resource,string}, {priority,integer}, {status,string}]}}}}

        '''
        print('status_list(\'all\')')
        response = self.ctl.status_list('all')
        print(response)
        print('')
        assert isinstance(response['users'], list)

    def test_status_list_host(self):
        '''
        Test ``status_list_host``.
        '''
        print('status_list_host(host, \'all\')')
        response = self.ctl.status_list_host(self.server, 'all')
        print(response)
        print('')
        assert isinstance(response['users'], list)

    def test_status_num(self):
        '''
        Test ``status_num``.

        Number of logged users with this status

        Arguments:

        status :: binary

            Status type to check

        Result:

        {users,integer}

        Number of connected sessions with given status type

        '''
        print('status_num(status)')
        response = self.ctl.status_num('chat')
        print(response)
        print('')
        assert isinstance(response['users'], int)

    def test_status_num_host(self):
        '''
        Test ``status_num_host``.

        Number of logged users with this status in host

        Arguments:

        host :: binary

            Server name

        status :: binary

            Status type to check

        Result:

        {users,integer}

            Number of connected sessions with given status type

        '''
        print('status_num_host(host, status)')
        response = self.ctl.status_num_host(self.server, 'all')
        print(response)
        print('')
        assert isinstance(response['users'], int)

    def test_stop(self):
        '''
        Test ``stop``.

        Stop ejabberd gracefully

        Result:

        {res,rescode}

        '''
        print('stop()')
        response = self.ctl.stop()
        print(response)
        print('')
        assert response['res'] == 0
        assert isinstance(response['res'], int)

    # TODO def stop_kindly(delay, announcement)

    # TODO def subscribe_room(self, user, nick, room, nodes): Subscribe to a MUC conference

    # TODO def unregister(user, host)

    # TODO def unsubscribe_room(self, user, room): Unsubscribe from a MUC conference

    # TODO def update(module)

    # TODO def update_list()

    def test_user_resources(self):
        '''
        Test ``user_resources``.

        List user's connected resources.

        Result:

        {resources,{list,{resource,string}}}

        '''
        print('user_resources(user, host)')
        response = self.ctl.user_resources(self.username, self.server)
        print(response)
        print('')
        assert isinstance(response['resources'], list)

    def test_user_sessions_info(self):
        '''
        Test ``user_sessions_info``.

        Get information about all sessions of a user.

        Arguments:

            user :: binary
            host :: binary

        Result:

        {sessions_info,{list,{session,{tuple,[{connection,string},
                                              {ip,string},
                                              {port,integer},
                                              {priority,integer},
                                              {node,string},
                                              {uptime,integer},
                                              {status,string},
                                              {resource,string},
                                              {statustext,string}]}}}}
        '''
        print('user_sessions_info(user, host)')
        response = self.ctl.user_sessions_info(self.username, self.server)
        print(response)
        print('')
        assert isinstance(response['sessions_info'], list)

if __name__ == '__main__':
    # Setup
    server = 'example.com'
    username = 'admin'
    password = 'admin'

    # Run all Python Ejabberd XML-RPC Administration API client tests
    tests = ejabberdctl_tests(server, username, password)
    tests.run_all()
