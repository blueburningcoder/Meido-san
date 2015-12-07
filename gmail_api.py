"""
Google Gmail API collected in one File. TODO: look at namespaces
or the like in python
basically everything needed to access one's E-mail.
(gotta find a way for getting the secret too ...)
"""
from apiclient import errors
from apiclient.discovery import build
from oauth2client import tools
import httplib2
import os
import oauth2client
import base64
import email

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.labels',
          'https://www.googleapis.com/auth/gmail.modify']

CLIENT_SECRET_FILE = '../../Downloads/client_secret.json'
APPLICATION_NAME = 'Meido-san'


def ListMessagesMatchingQuery(service, user_id='me', query=''):
    """List all Messages of the user's mailbox matching the query.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.
    Returns:
        List of Messages that match the criteria of the query. Note that the
        appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                                                       q=query,
                                                       pageToken=page_token
                                                       ).execute()
            messages.extend(response['messages'])
        return messages
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def ListMessagesWithLabels(service, user_id='me', label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Messages with these labelIds applied.
    Returns:
        List of Messages that have all required Labels applied. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate id to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids
                                                   ).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                                                       labelIds=label_ids,
                                                       pageToken=page_token
                                                       ).execute()
            messages.extend(response['messages'])
        return messages
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def getCredentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
    return credentials


def getMessage(service, user_id='me', msg_id):
    """ Get a Message with the given ID
    Args:
        service: Authorized Gmail API service instance
        user_id: User's email address or 'me'
        msg_id: The Id D of the message required
    Returns:
        A Message
    """
    try:
        message = service.users().messages().get(userId=user_id,
                                                 id=msg_id).execute()
        print 'Message snippet: %s' % message['snippet']
        return message
    except errors.HttpError, error:
        print 'An error ocurred: %s' % error


def getMimeMessage(service, user_id='me', msg_id):
    """ Get a Message and use it to create a MIME Message
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.
    Returns:
        A MIME Message, consisting of data from the Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()
        print 'Message snippet: %s' % message['snippet']
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        mime_msg = email.message_from_string(msg_str)
        return mime_msg
    except errors.HttpError, error:
        print 'An error ocurred: %s' % error


def getThread(service, user_id='me', thread_id):
    """ Get a Thread.
    Args:
        service: Authorized Gmaiil API service instance.
        user_id: User's email address.
        thread_id: The ID of the Thread required.
    Returns:
        Thread with matching ID.
    """
    try:
        thread = service.users().threads().get(userId=user_id,
                                               id=thread_id).execute()
        messages = thread['messages']
        print('thread id: %s - number of messages '
              'in this thread: %d') % (thread['id'], len(messages))
        return thread
    except errors.HttpError, error:
        print 'An error occured: %s' % error


def ListThreadsMatchingQuery(service, user_id='me', query=''):
    """ List all Threads of the user's mailbox matching the query.
    Args:
        service: Authorized Gmail API serivce instance.
        user_id: User's email address or "me".
        query: String used to filter messages returned.
            Eg.- 'label:UNREAD' for unread messages only.
    Returns:
        List of threads that match the criteria of the query. Note that the
        returned list contains Thread IDs, you must use get with the
        appropriate ID to get the details for a Thread.
    """
    try:
        response = service.users().threads().list(userId=user_id,
                                                  q=query).execute()
        threads = []
        if 'threads' in response:
            threads.extend(response['threads'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().threads().list(userId=user_id,
                                                      q=query,
                                                      pageToken=page_token
                                                      ).execute()
            threads.extend(response['threads'])
            return threads
    except errors.HttpError, error:
        print 'An error occured: %s' % error


def ListThreadsWithLabels(service, user_id='me', label_ids=[]):
    """List all Threads of the user's mailbox with label_ids applied.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Threads with these labelIds applied.
    Returns:
        List of threads that match the criteria of the query. Note that the
        returned list contains Thread IDs, you must use get with the
        appropriate ID to get the details for a Thread.
    """
    try:
        response = service.users().threads().list(userId=user_id,
                                                  labelIds=label_ids).execute()
        threads = []
        if 'threads' in response:
            threads.extend(response['threads'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().threads().list(userId=user_id,
                                                      labelIds=label_ids,
                                                      pageToken=page_token
                                                      ).execute()
            threads.extend(response['threads'])
        return threads
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


credentials = getCredentials()
http = credentials.authorize(httplib2.Http())
service = build('gmail', 'v1', http=http, credentials=credentials)
userId = 'meido.info@gmail.com'
# mes = ListMessagesMatchingQuery(service, 'me')
