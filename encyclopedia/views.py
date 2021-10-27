#
#TODO
# - [X] Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an 
#      encyclopedia entry, should render a page that displays the contents of 
#      that encyclopedia entry. 
#       [X] The view should get the content of the encyclopedia entry by calling 
#           the appropriate util function.
#       [X] If an entry is requested that does not exist, the user should be 
#           presented with an error page indicating that their requested page was not found.
#       [X] If the entry does exist, the user should be presented with a page that 
#           displays the content of the entry. The title of the page should 
#           include the name of the entry.
# - [X] Index Page: Update index.html such that, instead of merely listing the names of all 
#       pages in the encyclopedia, user can click on any entry name to be taken directly 
#       to that entry page.
# - [X] Search: Allow the user to type a query into the search box in the sidebar to search 
#       for an encyclopedia entry.
#       [X] If the query matches the name of an encyclopedia entry, the user should be 
#           redirected to that entry’s page.
#       [X] If the query does not match the name of an encyclopedia entry, the user should 
#           instead be taken to a search results page that displays a list of all encyclopedia 
#           entries that have the query as a substring. For example, if the search query were 
#           ytho, then Python should appear in the search results.
#       [X] Clicking on any of the entry names on the search results page should take the 
#           user to that entry’s page.
# - [X] New Page: Clicking “Create New Page” in the sidebar should take the user to a page 
#       where they can create a new encyclopedia entry.
#       [X] Users should be able to enter a title for the page and, in a textarea, 
#           should be able to enter the Markdown content for the page.
#       [X] Users should be able to click a button to save their new page.
#       [] When the page is saved, if an encyclopedia entry already exists with the provided 
#           title, the user should be presented with an error message.
#       [] Otherwise, the encyclopedia entry should be saved to disk, and the user should be 
#           taken to the new entry’s page.
# - [X] Edit Page: On each entry page, the user should be able to click a link to be taken to 
#       a page where the us
# .0er can edit that entry’s Markdown content in a textarea.
#   |    [X] The textarea should be pre-populated with the existing Markdown content of the page. 
#           (i.e., the existing content should be the initial value of the textarea).
#       [X] The user should be able to click a button to save the changes made to the entry.
#       [X] Once the entry is saved, the user should be redirected back to that entry’s page.
# - [X] Random Page: Clicking “Random Page” in the sidebar should take user to a random 
#       encyclopedia entry.
#    
#       [X] Markdown to HTML Conversion: On each entry’s page, any Markdown content in the entry 
#           file should be converted to HTML before being displayed to the user. You may use 
#           the python-markdown2 package to perform this conversion, installable via pip3 
#           install markdown2.
#    d:
#    cd D:\Programacion\wp_cs50_js_py\project_1\main\wiki
#    python manage.py runserver

from django.http.response import HttpResponseRedirect
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from .forms import AddEntry, EditEntry
from django.urls import reverse
from re import search
from . import util
import markdown2
import logging
import random

logger = logging.getLogger(__name__)

def topic(request, title):
    entry = util.get_entry(title)
    
    if entry:
        content = markdown2.markdown(entry)
        context = {'title': title, 'content': content}
        return render(request, 'encyclopedia/entry.html', context)
    else:
        context = {'message': f'Oops! {title} Wiki Page Not Be Found'}
        return render(request, 'encyclopedia/notFoundPage.html', context)

def index(request):

    if request.GET.get('q'):
        return search(request, request.GET['q'])
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def addEntry(request):
    if request.method == 'POST': #Si el método de request es POST
        form = AddEntry(request.POST) # Extrae la información del formulario

        if form.is_valid():
            title = form.cleaned_data['title'] #Sacar el título del form
            content = form.cleaned_data['content'] #Sacar el contendio del form
            entries = util.list_entries() #Sacar todas las entradas de la wiki

            for entry in entries:
                if entry.lower() in title.lower():
                    context = { 'form': form, 'title': title, 'message': 'already Exists'}
                    return render(request, 'encyclopedia/addEntry.html', context)
            
            util.save_entry(title, content) # Guardar la nueva entrada 
            entry = util.get_entry(title)
            content = markdown2.markdown(entry)
            context = {'title': title, 'content': content}
            return render(request, 'encyclopedia/entry.html', context)
    else:
        form = AddEntry()
    
    context = {'form': form}
    return render(request, 'encyclopedia/addEntry.html', context)

def search(request, query):
    matches = []
    entries = util.list_entries()

    for entry in entries:
        if query.lower() == entry.lower():
            title = entry
            entry = util.get_entry(title)
            return HttpResponseRedirect(reverse('topic', args=[title]))
        
        if query.lower() in entry.lower():
            matches.append(entry)

    context = {'matches': matches, 'query': query}
    return render(request, 'encyclopedia/searchResults.html', context)

def editEntry(request, title):

    entry = util.get_entry(title)

    if entry:
        form = EditEntry(initial={'title':title, 'content': entry})
        context = {'title': title, 'form': form}
        return render(request, 'encyclopedia/editEntry.html', context)
    else:
        context = {'message': f'Oops! {title} Wiki Page Not Be Found'}
        return render(request, 'encyclopedia/notFoundPage.html', context)

def submitEditedEntry(request, title):
    if request.method == 'POST':
        form = EditEntry(request.POST)
                
        if form.is_valid():
            content = form.cleaned_data['content']
            editedTitle = form.cleaned_data['title']

            if editedTitle != title:
                fileName = f'entries/{title}.md'

                if default_storage.exists(fileName):
                    default_storage.delete(fileName)

            util.save_entry(editedTitle, content)
            entry = util.get_entry(editedTitle)
            
        else:
            form = EditEntry()
        
        context = {'title': editedTitle, 'content': markdown2.markdown(entry)}
        return render(request, 'encyclopedia/entry.html', context)

def randomEntry(request):
    entries = util.list_entries()
    title = random.choice(entries)
    entry = util.get_entry(title)
    return HttpResponseRedirect(reverse('topic', args=[title]))