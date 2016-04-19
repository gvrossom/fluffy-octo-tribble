# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Folder, Document
from .forms import FolderForm, DocumentForm

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('datahub.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'datahub/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


def folder_list(request):
    folders = Folder.public.all()
    context = {'folders': folders}
    return render(request, 'datahub/folder_list.html', context)


def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    documents = Document.public.filter(folder__id=folder_id)
    context = {'documents': documents, 'folder': folder}
    return render(request, 'datahub/folder_detail.html', context)


def document_list(request):
    documents = Document.public.all()
    if request.GET.get('tag'):##using a get method on a dictionary-like request.GET prevents a KeyError to be raised if tag is not present in the query string.
        documents = documents.filter(tags__name=request.GET['tag'])
    context = {'documents': documents}
    return render(request, 'datahub/document_list.html', context)


def document_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        documents = user.documents.all()
        folders = user.folders.all()
    else:
        documents = Document.public.filter(owner__username=username)
        folders = Folder.public.filter(owner__username=username)
    if request.GET.get('tag'):
        documents = documents.filter(tags__name=request.GET['tag'])
    context = {'folders': folders, 'documents': documents, 'owner': user}
    return render(request, 'datahub/document_user.html', context)


@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()
            form.save_m2m() #create the relationship to the tag model
            return redirect('datahub:document_user',
                username=request.user.username)
    else:
        form = DocumentForm()
    context = {'form': form, 'create': True}
    return render(request, 'datahub/form.html', context)

@login_required
def document_edit(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if document.owner != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = DocumentForm(instance=document, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('datahub:document_user',
                username=request.user.username)
    else:
        form = DocumentForm(instance=document)
    context = {'form': form, 'create': False} ## False because the document already exists
    return render(request, 'datahub/form.html', context)


@login_required
def folder_create(request):
    if request.method == 'POST':
        form = FolderForm(data=request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.save()
            form.save_m2m()
            return redirect('datahub:document_user',
                username=request.user.username)
    else:
        form = FolderForm()
    context = {'form': form, 'create': True}
    return render(request, 'datahub/folder_form.html', context)


@login_required
def folder_edit(request, pk):
    folder = get_object_or_404(Folder, pk=pk)
    if folder.owner != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = FolderForm(instance=folder, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('datahub:document_user',
                username=request.user.username)
    else:
        form = FolderForm(instance=folder)
    context = {'form': form, 'create': False}
    return render(request, 'datahub/folder_form.html', context)
