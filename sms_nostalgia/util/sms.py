import logging
log = logging.getLogger(__name__)



def import_smses():
    """
    @returns all smses (Inbox + Sent)
    """
    from sms_nostalgia.model.sms import Sms

    log.debug('importing sms...')
    
    result = []
    for x in range(400):
        sms = Sms('+480%d' % x, 
                  'sms...', 'Inbox', 
                  display_name='Tomasz Nazar %s' % x)
        result.append(sms)

    return result

