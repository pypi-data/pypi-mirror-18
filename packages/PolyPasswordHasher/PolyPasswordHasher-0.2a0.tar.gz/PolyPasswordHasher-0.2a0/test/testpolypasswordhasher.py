import polypasswordhasher

from unittest import TestCase

import sys
THRESHOLD = 10

class TestPolyPasswordHasher(TestCase):

  def test_polypasswordhasher(self):

    # require knowledge of 10 shares to decode others.   Create a blank, new
    # password file...
    pph = polypasswordhasher.PolyPasswordHasher(threshold = THRESHOLD, passwordfile = None)

    # create three admins so that any two have the appropriate threshold
    pph.create_account('admin','correct horse',THRESHOLD/2)
    pph.create_account('root','battery staple',THRESHOLD/2)
    pph.create_account('superuser','purple monkey dishwasher',THRESHOLD/2)

    # make some normal user accounts...
    pph.create_account('alice','kitten',1)
    pph.create_account('bob','puppy',1)
    pph.create_account('charlie','velociraptor',1)
    pph.create_account('dennis','menace',0)
    pph.create_account('eve','iamevil',0)


    # try some logins and make sure we see what we expect...
    self.assertTrue(pph.is_valid_login('alice','kitten') == True)
    self.assertTrue(pph.is_valid_login('admin','correct horse') == True)
    self.assertTrue(pph.is_valid_login('alice','nyancat!') == False)
    self.assertTrue(pph.is_valid_login('dennis','menace') == True)
    self.assertTrue(pph.is_valid_login('dennis','password') == False)


    # persist the password file to disk
    pph.write_password_data('securepasswords')



     
    # If I remove this from memory, I can't use the data on disk to check 
    # passwords without a threshold
    pph = None

    # let's load it back in
    pph = polypasswordhasher.PolyPasswordHasher(threshold = THRESHOLD,passwordfile = 'securepasswords')

    # The password information is essentially useless alone.   You cannot know
    # if a password is valid without threshold or more other passwords!!!
    try: 
      pph.is_valid_login('alice','kitten')
    except ValueError:
      pass
    else:
      print "Can't get here!   It's still bootstrapping!!!"

    # with a threshold (or more) of correct passwords, it decodes and is usable.
    pph.unlock_password_data([('admin','correct horse'), ('root','battery staple'), ('bob','puppy'),('dennis','menace')])

    # now, I can do the usual operations with it...
    self.assertTrue(pph.is_valid_login('alice','kitten') == True)

    pph.create_account('moe','tadpole',1)
    pph.create_account('larry','fish',0)
       


    ##### TEST ISOLATED VALIDATION

    # require knowledge of 10 shares to decode others.   Create a blank, new
    # password file...
    pph = polypasswordhasher.PolyPasswordHasher(threshold = THRESHOLD, 
            passwordfile = None, isolated_check_bits = 2)

    # create three admins so that any two have the appropriate threshold
    pph.create_account('admin','correct horse',THRESHOLD/2)
    pph.create_account('root','battery staple',THRESHOLD/2)
    pph.create_account('superuser','purple monkey dishwasher',THRESHOLD/2)

    # make some normal user accounts...
    pph.create_account('alice','kitten',1)
    pph.create_account('bob','puppy',1)
    pph.create_account('charlie','velociraptor',1)
    pph.create_account('dennis','menace',0)
    pph.create_account('eve','iamevil',0)


    # try some logins and make sure we see what we expect...
    self.assertTrue(pph.is_valid_login('alice','kitten') == True)
    self.assertTrue(pph.is_valid_login('admin','correct horse') == True)
    self.assertTrue(pph.is_valid_login('alice','nyancat!') == False)
    self.assertTrue(pph.is_valid_login('dennis','menace') == True)
    self.assertTrue(pph.is_valid_login('dennis','password') == False)


    # persist the password file to disk
    pph.write_password_data('securepasswords')


    # If I remove this from memory, I can't use the data on disk to check 
    # passwords without a threshold
    pph = None


    # let's load it back in
    pph = polypasswordhasher.PolyPasswordHasher(threshold = THRESHOLD,
            passwordfile = 'securepasswords', isolated_check_bits=2)

    # create a bootstrap account
    pph.create_account("bootstrapper", 'password', 0)
    try:
      self.assertTrue(pph.is_valid_login("bootstrapper",'password') == True)
      self.assertTrue(pph.is_valid_login("bootstrapper",'nopassword') == False)
    except ValueError:
      print("Bootstrap account creation failed.")



    # The password threshold info should be useful now...
    try: 
      self.assertTrue(pph.is_valid_login('alice','kitten') == True)
      self.assertTrue(pph.is_valid_login('admin','correct horse') == True)
      self.assertTrue(pph.is_valid_login('alice','nyancat!') == False)
    except ValueError:
      print "Isolated validation but it is still bootstrapping!!!"

    try:
      pph.create_account('moe','tadpole',1)
    except ValueError:
      # Should be bootstrapping...
      pass
    else:
      print "Isolated validation does not allow account creation!"



    # with a threshold (or more) of correct passwords, it decodes and is usable.
    pph.unlock_password_data([('admin','correct horse'), ('root','battery staple'), ('bob','puppy'),('dennis','menace')])

    # now, I can do the usual operations with it...
    self.assertTrue(pph.is_valid_login('alice','kitten') == True)

    # including create accounts...
    pph.create_account('moe','tadpole',1)
    pph.create_account('larry','fish',0)
       
