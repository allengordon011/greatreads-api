import datetime

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Search

class SearchMethodTests(TestCase):

    def test_was_published_recently_with_future_search(self):
        """
        was_published_recently() should return False for searchs whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_search = Search(pub_date=time)
        self.assertIs(future_search.was_published_recently(), False)

    def test_was_published_recently_with_old_search(self):
        """
        was_published_recently() should return False for searchs whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_search = Search(pub_date=time)
        self.assertIs(old_search.was_published_recently(), False)

    def test_was_published_recently_with_recent_search(self):
        """
        was_published_recently() should return True for searchs whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_search = Search(pub_date=time)
        self.assertIs(recent_search.was_published_recently(), True)

    def create_search(search_text, days):
        """
        Creates a search with the given `search_text` and published the
        given number of `days` offset to now (negative for searchs published
        in the past, positive for searchs that have yet to be published).
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Search.objects.create(search_text=search_text, pub_date=time)


class SearchViewTests(TestCase):
    def test_index_view_with_no_searchs(self):
        """
        If no searchs exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_search_list'], [])

    def test_index_view_with_a_past_search(self):
        """
        Searchs with a pub_date in the past should be displayed on the
        index page.
        """
        create_search(search_text="Past search.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_search_list'],
            ['<Search: Past search.>']
        )

    def test_index_view_with_a_future_search(self):
        """
        Searchs with a pub_date in the future should not be displayed on
        the index page.
        """
        create_search(search_text="Future search.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_search_list'], [])

    def test_index_view_with_future_search_and_past_search(self):
        """
        Even if both past and future searchs exist, only past searchs
        should be displayed.
        """
        create_search(search_text="Past search.", days=-30)
        create_search(search_text="Future search.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_search_list'],
            ['<Search: Past search.>']
        )

    def test_index_view_with_two_past_searchs(self):
        """
        The searchs index page may display multiple searchs.
        """
        create_search(search_text="Past search 1.", days=-30)
        create_search(search_text="Past search 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_search_list'],
            ['<Search: Past search 2.>', '<Search: Past search 1.>']
        )
