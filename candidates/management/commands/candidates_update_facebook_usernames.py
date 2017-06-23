from __future__ import print_function, unicode_literals

from datetime import datetime
from random import randint
import sys

from django.db import transaction
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from candidates.models import MultipleFacebookProfileIdentifiers
from popolo.models import Person

import requests
from bs4 import BeautifulSoup
import re


VERBOSE = False


def verbose(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


class Command(BaseCommand):

    help = "Use the Facebook API to check / fix Faceook user IDs"

    def record_new_version(self, person, msg=None):
        if msg is None:
            msg = 'Updated by the automated Faceook account checker ' \
                  '(candidates_update_facebook_usernames)'
        person.extra.record_version(
            {
                'information_source': msg,
                'version_id': "{0:016x}".format(randint(0, sys.maxsize)),
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        person.extra.save()

    # def remove_twitter_screen_name(self, person, twitter_screen_name):
    #     person.contact_details.get(
    #         contact_type='twitter',
    #         value=twitter_screen_name,
    #     ).delete()
    #     self.record_new_version(
    #         person,
    #         msg="This Twitter screen name no longer exists; removing it " \
    #         "(candidates_update_twitter_usernames)"
    #     )

    # def remove_twitter_user_id(self, person, twitter_user_id):
    #     person.identifiers.get(
    #         scheme='twitter',
    #         identifier=twitter_user_id,
    #     ).delete()
    #     self.record_new_version(
    #         person,
    #         msg="This Twitter user ID no longer exists; removing it " \
    #         "(candidates_update_twitter_usernames)",
    #     )

    def handle_person(self, person):
        try:
            user_id, profile_url = person.extra.facebook_profile_identifiers
        except MultipleFacebookProfileIdentifiers as e:
            print(u"WARNING: {message}, skipping".format(message=e))
            return

        # If they have a profile_url, then check to see if we
        # need to update the screen name from that; if so, update
        # the screen name.  Skip to the next person. This catches
        # people who have changed their profile_url, or
        # anyone who had a user ID set but not a profile_url
        # (which should be rare).  If the profile_url is not valid
        # it is deleted.
        if user_id:
            verbose(_("{person} has a Facebook user ID: {user_id}").format(
                person=person, user_id=user_id
            ))
            # TODO
            # if user_id not in self.twitter_data.user_id_to_screen_name:
            #     print(_("Removing user ID {user_id} for {person_name} as it is not a valid Twitter user ID. {person_url}").format(
            #         user_id=user_id,
            #         person_name=person.name,
            #         person_url=person.extra.get_absolute_url(),
            #     ))
            #     self.remove_twitter_user_id(person, user_id)
            #     return
            # correct_screen_name = self.twitter_data.user_id_to_screen_name[user_id]
            # if (screen_name is None) or (screen_name != correct_screen_name):
            #     print(_("Correcting the screen name from {old_screen_name} to {correct_screen_name}").format(
            #         old_screen_name=screen_name,
            #         correct_screen_name=correct_screen_name
            #     ))
            #
            #     person.contact_details.update_or_create(
            #         contact_type='twitter',
            #         defaults={'value': correct_screen_name},
            #     )
            #     self.record_new_version(person)
            # else:
            #     verbose(_("The screen name ({screen_name}) was already correct").format(
            #         screen_name=screen_name
            #     ))

        # Otherwise, if they have a profile_url name (but no
        # user ID, since we already dealt with that case) then
        # find their Twitter user ID and set that as an identifier.
        # If the screen name is not a valid Twitter screen name, it
        # is deleted.
        elif profile_url and not user_id:
            verbose(_("{person} has profile_url ({profile_url}) but no user ID").format(
                person=person, profile_url=profile_url
            ))

            req = requests.get(profile_url)
            if req.status_code == 404:
                print(profile_url)
                # TODO remove URL?
                return
            match = re.search(r'\"entity_id\"\:\"([^\"]+)\"', req.content)
            if match:
                print(match.group(1))

                person.identifiers.create(
                    scheme='facebook_profile',
                    identifier=match.group(1)
                )
                self.record_new_version(person)


    def handle(self, *args, **options):
        global VERBOSE
        VERBOSE = int(options['verbosity']) > 1

        qs = Person.objects.select_related('extra')
        qs = qs.filter(links__note__contains="facebook personal")

        for person in qs:
            with transaction.atomic():
                self.handle_person(person)
