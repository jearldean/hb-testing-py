"""Testsq for Balloonicorn's Flask app."""

import unittest
import party


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"having a party", result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        result = self.client.get("/")
        self.assertIn(b"Please RSVP", result.data)
        self.assertNotIn(b"123 Magic Unicorn Way", result.data)


    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        self.assertIn(b"123 Magic Unicorn Way", result.data)
        self.assertNotIn(b"Please RSVP", result.data)
 

    def test_rsvp_mel(self):
        """Can we keep Mel out?"""

        """
            >>> is_mel(name="Mel Melitpolski", email="mel@ubermelon.com")
            True
            >>> is_mel(name="Swell Melitpolski", email="swell@ubermelon.com")
            False
        """
        rsvp_info = {'name': "Mel Melitpolski", 'email': "mel@ubermelon.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        self.assertIn(b"Sorry, Mel. This is kind of awkward.", result.data)

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        self.assertNotIn(b"Sorry, Mel. This is kind of awkward.", result.data)


        rsvp_info = {'name': "Mel", 'email': "mel@ubermelon.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        self.assertIn(b"Sorry, Mel. This is kind of awkward.", result.data)

        # mel_imposters = ["Mel", "Melitpolski", "Mel Melitpolski", 
        # "mel", "melitpolski", "mel melitpolski",
        # "Mel melitpolski", "mel Melitpolski"]
        rsvp_info = {'name': "mel", 'email': ""}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        self.assertIn(b"Hey, fill out the form.", result.data)




if __name__ == "__main__":
    unittest.main()
