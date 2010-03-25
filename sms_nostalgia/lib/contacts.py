import logging
log = logging.getLogger(__name__)



import evolution



class ContactsAPI(object):

    
    #python evolution - not all phone numbers show up 
    #http://talk.maemo.org/showthread.php?p=581204
    name_attributes = [
        "full-name",
        "given-name",
        "family-name",
        "nickname"
    ]

    phone_attributes = [
        "assistant-phone",
        "business-phone",
        "business-phone-2",
        "business-fax",
        "callback-phone",
        "car-phone",
        "company-phone",
        "home-phone",
        "home-phone-2",
        "home-fax",
        "isdn-phone",
        "mobile-phone",
        "other-phone",
        "other-fax",
        "pager",
        "primary-phone",
        "radio",
        "telex",
        "tty",
    ]



    @classmethod
    def get_all(cls):
        from sms_nostalgia.model.contact import Contact
        log.debug('get_all')
        abook = evolution.ebook.open_addressbook("default")
        all_contacts = abook.get_all_contacts()

        contacts = []
        for econtact in all_contacts:
            contacts.append(Contact(econtact))
        log.debug('got %s contacts' % len(contacts))
        return contacts
            

    @classmethod
    def sort_by_phone(cls, contacts=None):
        log.debug('sort_by_phone')
        if not contacts:
            contacts = cls.get_all()

        by_phone = {} #dict by phone number
        for c in contacts:
            for phone in c.phones():
                if phone in by_phone:
                    log.warning('duplicated phone: %s: %s' % (phone, c.uuid()))
                by_phone[phone] = c

        return by_phone
        
