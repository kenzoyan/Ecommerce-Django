 
from django.contrib.sessions.models import Session

s = Session.objects.get(pk='7o28wjdztmfb97gnu21j2s2aha3p6eg1')

print(s.get_decoded())