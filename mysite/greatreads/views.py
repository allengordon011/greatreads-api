from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Search, Input

class IndexView(generic.ListView):
    template_name = 'greatreads/index.html'
    context_object_name = 'latest_search_list'

    def get_queryset(self):
        """Return the last five published searches. (not including those set to be published in the future)."""
        return Search.objects.filter(
            pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Search
    template_name = 'greatreads/search.html'


class ResultsView(generic.DetailView):
    model = Search
    template_name = 'greatreads/results.html'

def searchpage(request, search_id):
    search = get_object_or_404(Search, pk=search_id)
    try:
        selected_input = search.input_set.get(pk=request.POST['input'])
    except (KeyError, Input.DoesNotExist):
        # Redisplay the search voting form.
        return render(request, 'greatreads/searchpage.html', {
            'search': search,
            'error_message': "You didn't submit anything.",
        })
    else:
        selected_input.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('greatreads:results', args=(search.id,)))

# #the 'hard way'
# def index(request):
#     latest_search_list = Search.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_search_list': latest_search_list,
#     }
#     return render(request, 'greatreads/index.html', context)
#
# def detail(request, search_id):
#     search = get_object_or_404(Search, pk=search_id)
#     return render(request, 'greatreads/detail.html', {'search': search})
#
# def results(request, search_id):
#     search = get_object_or_404(Search, pk=search_id)
#     return render(request, 'greatreads/results.html', {'search': search})
#
# def vote(request, search_id):
#     search = get_object_or_404(Search, pk=search_id)
#     try:
#         selected_choice = search.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the search voting form.
#         return render(request, 'greatreads/detail.html', {
#             'search': search,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('greatreads:results', args=(search.id,)))
