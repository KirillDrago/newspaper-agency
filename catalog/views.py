from django.shortcuts import render
from django.views import generic

from catalog.models import Redactor, Topic, Newspaper


def index(request):
    """View function for the home page of the site."""

    num_redactors = Redactor.objects.count()
    num_newspaper = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    context = {
        "num_redactors": num_redactors,
        "num_newspaper": num_newspaper,
        "num_topics": num_topics,
    }

    return render(request, "catalog/index.html", context=context)


class TopicListView(generic.ListView):
    model = Topic
    template_name = "catalog/topic_list.html"
    context_object_name = "topic_list"
    paginate_by = 5
    queryset = Topic.objects.order_by("name")


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 5
    queryset = Newspaper.objects.select_related("topic")


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 5


class RedactorDetailView(generic.DetailView):
    model = Redactor
    # queryset = Redactor.objects.prefetch_related("newspapers")
