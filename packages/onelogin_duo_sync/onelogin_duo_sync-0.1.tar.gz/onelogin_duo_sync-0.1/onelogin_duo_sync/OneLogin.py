import requests

class OneLogin(object):
    def __init__(self, shard='US'):
        """
        Specify the shard of the system being used (us or eu)
        :param shard: us or eu
        :return:
        """
        self.shard = shard.lower()
        if 'us' in self.shard:
            self.base_url = 'https://api.us.onelogin.com'
        elif 'eu' in self.shard:
            self.base_url = 'https://api.eu.onelogin.com'
        elif 'shadow01' in self.shard:
            self.base_url = 'https://oapi01-shadow01.use1.onlgn.net'

    def set_attributes(self, kwargs):
        for kwarg_key, kwarg_value in kwargs.iteritems():
            setattr(self, kwarg_key, kwarg_value)

    def handle_error(self, **kwargs):
        error = {}
        for k,v in kwargs.iteritems():
            error[k] = v
        return error


class Token(OneLogin):
    """
    Create the token object to be used for calling the OneLogin API.
    """
    def __init__(token, **kwargs):
        for key in ('client_id', 'client_secret', 'shard'):
            if key in kwargs:
                setattr(token, key, kwargs[key])
        token.session = requests.session()
        token.session.headers = {'Content-Type': 'application/json'}
        oauth_endpoint = '/auth/oauth2'
        try:
            OneLogin.__init__(token, token.shard)
        except:
            if token.client_id == '0':
                raise ValueError('Client_ID is required')
            elif token.client_secret == '0':
                raise ValueError('Client_Secret is required')
        token.target = token.base_url + oauth_endpoint
        token.get_token()

    def get_token(token):
        """
        Get a new OAUTH token
        :return: JSON response
        """
        authorization = 'client_id: %s, client_secret: %s' % (token.client_id,
                                                              token.client_secret)
        token.session.headers.update({'Authorization':authorization})
        r = token.session.post(token.target + '/token', verify=False,
                               json={'grant_type':'client_credentials'})
        if r.status_code != 200:
            print token.handle_error(**{'status_code':r.status_code,
                                       'message_body':r.text,
                                       'url': token.target + '/token',
                                       'headers':token.session.headers})
            return False
        else:
            token.set_attributes({
                'access_token':r.json()['data'][0]['access_token'],
                'refresh_token':r.json()['data'][0]['refresh_token'],
                'token_created_at':r.json()['data'][0]['created_at'],
                'token_expires_at':r.json()['data'][0]['expires_in']})
            return True

    def refresh_the_token(token):
        """
        Refresh the current OAUTH token
        :return: JSON response
        """
        r = token.session.post(token.target + '/token', verify=False,
                               json={
                                  'grant_type':'refresh_token',
                                  'refresh_token':token.refresh_token,
                                  'access_token':token.access_token})
        if r.status_code != 200:
            print token.handle_error(**{'status_code':r.status_code,
                                       'message_body':r.text,
                                       'url': token.target + '/token',
                                       'headers':token.session.headers})
            return False
        else:
            token.set_attributes({
                'access_token':r.json()['data'][0]['access_token'],
                'refresh_token':r.json()['data'][0]['refresh_token'],
                'created_at':r.json()['data'][0]['created_at'],
                'expires_in':r.json()['data'][0]['expires_in']
            })

            return True

    def revoke_the_token(token):
        """
        Revoke the current OAUTH token
        :return: JSON response
        """
        r = token.session.post(token.target + '/revoke', verify=False,
                               json={
                                  'grant_type':'revoke_token',
                                  'access_token':token.access_token,
                                  'client_id':token.client_id,
                                  'client_secret':token.client_secret
                              })
        if r.status_code != 200:
            print token.handle_error(**{'status_code':r.status_code,
                                       'message_body':r.text,
                                       'url': token.target + '/revoke',
                                       'headers':token.session.headers})
            return False
        else:
            return True

    def check_token_expiration(self):
        """
        TODO: Calculate expiration time of token, if expired, call refresh_token
        to update access_token
        :return:
        """

    def check_rate_limit(token):
        """
        check rate limit
        :return:
        """
        if token.access_token:
            authorization = 'Bearer:%s' % token.access_token
            token.session.headers.update({'Authorization':authorization})
        else:
            return 'Access Token not found'
        r = token.session.get(token.base_url + '/auth/rate_limit', verify=False)
        if r.status_code != 200:
            print token.handle_error(**{'status_code':r.status_code,
                                       'message_body':r.text,
                                       'url': token.target + '/revoke',
                                       'headers':token.session.headers})
            return False
        else:
            return r


class User(Token):
    """

    """

    def __init__(user, token):
        """
        Requires token to init
        :return:
        """
        # user.set_attributes(kwargs)
        user.session = requests.session()
        user.session.headers = {'Content-Type': 'application/json'}
        user.user_endpoint = '/api/1/users'
        try:
            user.base_url = token.base_url
            user.session.headers.update({'Authorization': 'Bearer:%s' %
                                                          token.access_token})
        except:
            raise ValueError('Token not found, have you initialized the Token yet?')


    def get_all_users(user, sort=False, fields=''):
        """
        Get all users, specify sort and fields to filter results
        :param sort: Sort results by ID, use 1 to sort asc, 2 for desc, default is no sort
        :param fields: specify fields to include in result 'lastname, firstname, email'
        :return: Dictionary of user's with each page of response corresponding to key,
        1,2,etc
        """
        count = 0
        next_page = 1
        response = {}
        while next_page != 0:
            if sort == 0:
                r = user.session.get(user.base_url + user.user_endpoint +
                                     '?&fields=%s' % str(fields), verify=False)
            elif sort == 1:
                r = user.session.get(user.base_url + user.user_endpoint +
                                     '?sort=id&fields=%s' % str(fields), verify=False)
            else:
                r = user.session.get(user.base_url + user.user_endpoint +
                                     '?sort=-id&fields=%s' % str(fields), verify=False)
            if r.status_code != 200:
                print user.handle_error(**{'status_code':r.status_code,
                                           'message_body':r.text,
                                           'url': user.base_url + user.user_endpoint,
                                           'headers':user.session.headers})
                next_page == 0
                return False
            else:
                if r.json()['pagination']['next_link'] == None:
                    next_page == 0
                    response[count] = r.json()
                    return response
                else:
                    user.user_endpoint = r.json()['pagination']['next_link'][28:]
                    response[count] = r.json()
                    count += 1

class Group(Token):
    """
    TODO: Call Group API to list, create, destory, update, and search Groups
    """

    def __init__(group, token):
        """
        Initialize the Group Object

        :return:
        """
        group.session = requests.session()
        group.session.headers = {'Content-Type': 'application/json'}
        group.groups_endpoint = '/api/1/groups'
        try:
            group.base_url = token.base_url
            group.session.headers.update({'Authorization': 'Bearer:%s' % token.access_token})
        except:
            raise ValueError('Token not found, have you initialized the Token yet?')

    def get_all_groups(group):
        """
        Just like it says on the tin.

        :return:
        """
        r = group.session.get(group.base_url + group.groups_endpoint)
        if r.status_code != 200:
            print group.handle_error(**{
                'status code':r.status_code,
                'message_body':r.text,
                'url':group.base_url + group.groups_endpoint,
                'headers':group.session.headers})
            exit()
        else:
            return r.json()
