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


def listLabels(service, user_id='me'):
    """ Get a list of all Labels in the user's mailbox.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address or "me".
    Returns:
        A list with all labels in the user's mailbox.
    """
    try:
        response = service.users().labels().list(userId=user_id).execute()
        labels = response['labels']
        for label in labels:
            print 'Label id: %s - Label name: %s' % (label['id'], label['name'])
        return labels
    except errors.HttpError, error:
        print 'An error occured: %s' % error


def ListMessagesWithLabels(service, label_ids=[], user_id='me'):
    """List all Messages of the user's mailbox with label_ids applied.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address or "me".
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


def getMessage(service, msg_id, user_id='me'):
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


def getMimeMessage(service, msg_id, user_id='me'):
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


def getThread(service, thread_id, user_id='me'):
    """ Get a Thread.
    Args:
        service: Authorized Gmail API service instance.
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


def ListThreadsWithLabels(service, label_ids=[], user_id='me'):
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


def GetAttachments(service, msg_id, user_id='me', store_dir='/home/bez/Downloads/'):
    """Get and store attachment from Message with given id.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: ID of Message containing attachment.
        store_dir: The directory used to store attachments.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        for part in message['payload']['parts']:
            if part['filename']:
                print part
                file_data = base64.urlsafe_b64decode(part['body']['data']).encode('UTF-8')
#               file_data = base64.urlsafe_b64decode(part['body']['attachmentId'].encode('UTF-8') + '=')
                path = ''.join([store_dir, part['filename']])
                f = open(path, 'w')
                f.write(file_data)
                f.close()
                print 'Saved attachement %s to %s' % (part['filename'], store_dir)
            else:
                print 'Not an attachement'
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def UpdateLabel(service, label_id, updated_label_object, user_id='me'):
    """Update an existing Label.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address or 'me'.
        label_id: ID of the Label to update.
        updated_label_object: Updated label.
    Returns:
        Updated Label.
    """
    try:
        updated_label_object['id'] = label_id
        updated_label = (service.users().labels()
                .update(userId=user_id, id=label_id,
                        body=updated_label_object).execute())
        print 'label id: %s - label name: %s' % (updated_label['id'],
                                                 updated_label['name'])
        return updated_label
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def ListHistory(service, start_history_id='1', user_id='me'):
    """List History of all changes to the user's mailbox.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address or 'me'.
        start_history_id: Only return Histories at or after start_history_id.
    Returns:
        A list of mailbox changes that occured after the start_history_id.
    """
    try:
        history = service.users().history().list(userId=user_id, 
                                startHistoryId=start_history_id
                                ).execute()
        changes = history['history'] if 'history' in history else []
        while 'nextPageToken' in history:
            page_token = history['nextPageToken']
            history = service.users().history().list(userId=user_id,
                            startHistoryId=start_history_id, 
                            pageToken=page_token).execute()
            changes.extend(history['history'])
        return changes
    except errors.HttpError, error:
        print 'An error occurred: %s' % error



def ListUnreadMessages(service):
    """ Lists all unread messages.
    Args:
        service: Authorized Gmail API service instance.
    """
    return ListMessagesWithLabels(service, 'UNREAD')


def ListUnreadThreads(service):
    """ Lists all unread threads.
    Args:
        service: Authorized Gmail API service instance.
    """
    return ListThreadsWithLabels(service, 'UNREAD')


def MakeLabel(label_name, mlv='show', llv='labelShow'):
    """Create Label object.
    Args:
        label_name: The name of the Label.
        mlv: Message list visibility, show/hide.
        llv: Label list visibility, labelShow/labelHide.
    Returns:
        Created Label.
    """
    label = {'messageListVisibility': mlv,
             'name': label_name,
             'labelListVisibility': llv}
    return label


def ModifyThread(service, thread_id, msg_labels, user_id='me'):
    """ Add labels to a Thread.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email adress or 'me'.
        thread_id: The id of the thread to be modified.
        msg_labels: The change in labels.
    Returns:
        Thread with modified Labels.
    """
    try:
        thread = service.users().threads().modify(userId=user_id, id=thread_id,
                                                  body=msg_labels).execute()
        thread_id = thread['id']
        label_ids = thread['messages'][0]['labelIds']
        print 'Thread ID: %s - With Label IDs %s' % (thread_id, label_ids)
        return thread
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def CreateMsgLabels():
    """ Create object to update labels.
    Returns:
        A label update object.
    """
    return { 'removeLabelIds':[], 'addLabelIds':['UNREAD', 'Label_2']}


credentials = getCredentials()
http = credentials.authorize(httplib2.Http())
service = build('gmail', 'v1', http=http, credentials=credentials)
userId = 'meido.info@gmail.com'
mes = ListMessagesMatchingQuery(service)
