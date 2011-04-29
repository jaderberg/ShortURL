from django.db import models
import datetime
import random
import string

class ShortURL(models.Model):
    code = models.CharField(max_length=10, unique=True)
    code_length = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField('expiry date')
    owner = models.CharField(max_length=250)
    url = models.URLField(verify_exists=False)
    clicks = models.IntegerField(default=0)
    def __unicode__(self):
        return self.code
    def has_expired(self):
        return not self.expiry_date >= datetime.datetime.now()
    def get_shortURL(self):
        return 'http://typ.so/' + self.code
    @staticmethod
    def create(url, code, owner):
        date_expires = datetime.datetime.now() + datetime.timedelta(2*7)
        newObj = ShortURL(code='', expiry_date=date_expires, owner=owner, url=url)
        if code and not ShortURL.code_taken(code):
            newObj.code = code
        else:
            worst_length = ShortURL.objects.count()/62 + 1
            # check if any codes below that length have expired
            current_length = 0
            shorter_length_found = False
            while current_length < worst_length and not shorter_length_found:
                current_length += 1
                codes = ShortURL.objects.filter(code_length=current_length).filter(expiry_date__lt=datetime.datetime.now()).order_by('expiry_date')
                if codes.count():
                    shorter_length_found = True
            code = ShortURL.generate_code(current_length)
            while ShortURL.code_taken(code):
                code = ShortURL.generate_code(current_length)
            newObj.code = code
        newObj.code_length = len(newObj.code)
        return newObj
    @staticmethod
    def generate_code(N):
        # Generate a code of length N
        return ''.join(random.choice(string.letters + string.digits) for x in range(N))
    @staticmethod
    def code_taken(code):
        s = ShortURL.objects.filter(code=code)
        if s.count():
            if s[0].has_expired():
                s[0].delete()
                return False
            else:
                return True
        else:
            return False
    
