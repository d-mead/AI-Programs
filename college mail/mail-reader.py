#!/usr/bin/python
# -*- coding: utf-8 -*-
import appscript
mail = appscript.app(u'Mail')
mailbox = mail.mailboxes[u'Inbox'].mailboxes[u'David']
messages = mailbox.messages
unPublishedMessages = messages.get()
#loop through all unread messages
for message in unPublishedMessages:
    print(message.subject.get())