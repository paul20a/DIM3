from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from extras.models import Production, Role, Director, Actor, Application
from extras.forms import ProductionForm, UserForm, DirectorProfileForm, RoleForm, ActorProfileForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from extras.bing_search import run_query
from datetime import datetime


@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect('/extras/')

def accept(request, production_name_url, role_name_url,username):
    context = RequestContext(request)
    actor=Actor.objects.get(user=User.objects.get(username=username))
    role_name=decode_url(role_name_url)
    pro_name=decode_url(production_name_url)
    pro=Production.objects.get(title=pro_name)
    a=Application.objects.get(role=Role.objects.get(name=role_name,production=pro),actor=actor)
    a.outcome='accepted'
    a.save()
    return HttpResponseRedirect('/extras/production/'+production_name_url+'/role/'+role_name_url+'/view_application/', context)

def decline(request, production_name_url, role_name_url,username):
    context = RequestContext(request)
    actor=Actor.objects.get(user=User.objects.get(username=username))
    role_name=decode_url(role_name_url)
    pro_name=decode_url(production_name_url)
    pro=Production.objects.get(title=pro_name)
    a=Application.objects.get(role=Role.objects.get(name=role_name,production=pro),actor=actor)
    a.outcome='declined'
    a.save()
    return HttpResponseRedirect('/extras/production/'+production_name_url+'/role/'+role_name_url+'/view_application/', context)

def view_application(request, production_name_url, role_name_url):
    context = RequestContext(request)
    if request.user.is_staff:
        production_name=decode_url(production_name_url)
        role_name=decode_url(role_name_url)
        role=Role.objects.get(name=role_name, production=Production.objects.get(title=production_name))

        apps=Application.objects.filter(role=role, outcome='undecided')
        for app in apps:
            app.url=encode_url(app.actor.user.username)

        context_dict = {'apps': apps}
        context_dict['role'] = role
        context_dict['role_url'] = role_name_url
        context_dict['pro_url'] = production_name_url
    if request.method == 'POST':
        print "post:"
        if 'accept' in request.POST:
            print "accept:"
        if 'decline' in request.POST:
           print "decline:"


    return render_to_response('extras/view_application.html', context_dict, context)


def message(request, production_name_url, role_name_url):
    context = RequestContext(request)
    actor=Actor.objects.get(user=request.user)
    production_name=decode_url(production_name_url)
    role_name=decode_url(role_name_url)
    role=Role.objects.get(name=role_name,production=Production.objects.get( title = production_name))
    try:
        app=Application.objects.get(role=role,actor=actor)
    except Application.DoesNotExist:
       text='undecided'
       app=Application.objects.create(role=role,actor=actor, outcome=text, date=datetime.now().date())
    context_dict = {'app': app}
    context_dict['production_name_url'] = production_name_url
    context_dict['role_name_url'] = role_name_url
    return render_to_response('extras/send.html', context_dict, context)


def decode_url(name_url):
    return name_url.replace('_', ' ')


def encode_url(name):
    return name.replace(' ', '_')


def index(request):
    context = RequestContext(request)

    production_dict = {}
    for production in Production.objects.order_by('-title'):
        production_dict[production] = 0
    for application in Application.objects.order_by('-role'):
        production_dict[application.role.production]  += 1
    production_list_popular = sorted(production_dict, key = production_dict.get, reverse = True)

    context_dict = {}
    context_dict['productions_popular'] = production_list_popular[:5]
    context_dict['productions_closing'] = Production.objects.order_by('-closingDate')[:5]
    context_dict['roles'] = Role.objects.order_by('-name')
    context_dict['hpaid'] = Production.objects.order_by('-cost')[:5]

    for production in context_dict['productions_popular']:
        production.url = encode_url(production.title)
    for production in context_dict['productions_closing']:
        production.url = encode_url(production.title)
    for role in context_dict['roles']:
        role.url = encode_url(role.name)
        role.production.url = encode_url(role.production.title)

    return render_to_response('extras/index.html', context_dict, context)


def production(request, production_name_url):
    context = RequestContext(request)
    production_name = decode_url(production_name_url)

    context_dict = {'production_name': production_name}
    context_dict['production_name_url'] = production_name_url

    try:
        production = Production.objects.get(title=production_name)
        roles = Role.objects.filter(production=production)
        for role in roles:
            role.url = encode_url(role.name)
        context_dict['roles'] = roles
        context_dict['production'] = production
    except Production.DoesNotExist:
        pass

    # Go render the response and return it to the client.
    return render_to_response('extras/production.html', context_dict, context)


def role(request, production_name_url, role_name_url):
    context = RequestContext(request)
    role_name = decode_url(role_name_url)
    production_name=decode_url(production_name_url)

    context_dict = {'role_name': role_name}
    context_dict['role_name_url'] = role_name_url
    context_dict['production_name'] = production_name
    context_dict['production_name_url'] = production_name_url	
    
    
    if request.user.is_authenticated():
        context_dict['actorDetails'] = Actor.objects.filter(user = request.user)

    try:
        role = Role.objects.get(name = role_name)
        role.url=encode_url(role_name)
        context_dict['role']=role
        context_dict['picture'] = role.picture
        context_dict['production'] = Production.objects.get(title = production_name)
    except Role.DoesNotExist:
        pass

    # Go render the response and return it to the client.
    return render_to_response('extras/role.html', context_dict, context)

def actor(request, actor_name_url):
    context = RequestContext(request)
    actor_name = decode_url(actor_name_url)

    context_dict = {'actor_name': actor_name}
    context_dict['actor_name_url'] = actor_name_url

    # find the actor and add their details
    for actor in Actor.objects.order_by('-dateOfBirth'):
        if actor.user.username == actor_name:
            context_dict['actor'] = actor
            break
    # in addition to the details, add the productions that actor has played in
    context_dict['pastProductions'] = []
    for production in Production.objects.order_by('-title'):
        for application in Application.objects.order_by('-role'):
            if (application.role.production == production and
                application.actor.user == context_dict['actor'].user and
                application.outcome == 'Accepted'):
                context_dict['pastProductions'].append(production)
    for production in context_dict['pastProductions']:
        production.url = encode_url(production.title)

    # Go render the response and return it to the client.
    return render_to_response('extras/actor.html', context_dict, context)


def add_production(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/extras/login/')
    else:

        context = RequestContext(request)

        if request.method == 'POST':
            form = ProductionForm(request.POST)

            if form.is_valid():

                production= form.save(commit=False)
                production.productionID=Production.objects.count()

                director= Director.objects.get(user=request.user)
                production.director = director
         
                production.save()
                return index(request)
            else:

                print form.errors

        else:

            form = ProductionForm()

        return render_to_response('extras/add_production.html', {'form': form}, context)


def add_role(request, production_name_url):

    production_name = decode_url(production_name_url)
    context = RequestContext(request)
    try:
        pro = Production.objects.get(title=production_name)
    except Production.DoesNotExist:
        return render_to_response('extras/add_production.html', {}, context)

    director = Director.objects.get(user=request.user)
    print(director.user.username)
    print(pro.director.user.username)
    if director == pro.director:

        if request.method == 'POST':
            form = RoleForm(request.POST)

            if form.is_valid():

                role = form.save(commit=False)
                role.production = pro

                role.save()

                return production(request, production_name_url)
            else:
                print form.errors
        else:
            form = RoleForm()

        return render_to_response( 'extras/add_role.html',
                {'production_name_url': production_name_url,
                    'production_name': production_name, 'form': form}, context)
    else:
        return HttpResponseRedirect('/extras/login/')


def directorRegister(request):
    context = RequestContext(request)
    url = 'director_register'
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = DirectorProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = DirectorProfileForm()

    return render_to_response(
        'extras/register.html',
{'user_form': user_form, 'url': url, 'profile_form': profile_form, 'registered': registered},
          context)


def actorRegister(request):
    context = RequestContext(request)
    url = 'actor_register'
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = ActorProfileForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

        # Ideally picture upload for questionnaire form

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = ActorProfileForm()

    return render_to_response(
        'extras/register.html',
{'user_form': user_form, 'url': url, 'profile_form': profile_form, 'registered': registered}, context)


def user_login(request):

    context = RequestContext(request)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:

                login(request, user)
                return HttpResponseRedirect('/extras/')
            else:

                return HttpResponse("Your Extras account is disabled.")
        else:

            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:

        return render_to_response('extras/login.html', {}, context)


def about(request):
    context = RequestContext(request)

    context_dict = {'boldmessage': "About Extras Wanted"}

    return render_to_response('extras/about.html', context_dict, context)


def jobs(request):
    context = RequestContext(request)

    roles_list = Role.objects.order_by('-name')
    context_dict = {'roles': roles_list}
    for role in context_dict['roles']:
        role.url = encode_url(role.name)
        role.production.url = encode_url(role.production.title)

    return render_to_response('extras/jobs.html', context_dict, context)


def actors(request):
    context = RequestContext(request)

    actors_list = Actor.objects.order_by('-user')
    context_dict = {'actors': actors_list}
    for actor in context_dict['actors']:
        actor.url = encode_url(actor.user.username)

    return render_to_response('extras/actors.html', context_dict, context)


def profile(request):
    context = RequestContext(request)

    if request.user.is_authenticated():
        # add the user details
        rUser = request.user
        context_dict = {'userID': User.objects.order_by('-first_name')}
        context_dict['actorDetails'] = Actor.objects.filter(user=rUser)
        context_dict['directorDetails'] = Director.objects.filter(user=rUser)
        context_dict['pastCastings'] = []
        context_dict['currentCasts'] = []
     # add the past castings (depending on the user type)
        if context_dict['directorDetails']:  # director -> add all productions with the same director
            for production in Production.objects.order_by('-title'):
                production.url=encode_url(production.title)
                if production.director.user == rUser:
                    context_dict['pastCastings'].append(production)
        else:  # actor -> add all productions for which this actor has successfully applied
            actor = Actor.objects.get(user=rUser)
            roles =[]
            for ap in Application.objects.order_by('-date'):
                if ap.actor.user == rUser:
                    ap.rurl=encode_url(ap.role.name)
                    ap.purl=encode_url(ap.role.production.title)
                    context_dict['currentCasts'].append(ap)
                    roles.append(ap.role)

            for cast in context_dict['currentCasts']:
                cast.url = encode_url(cast.role.name)
                cast.purl = encode_url(cast.role.production.title)

        # add the available items (actors or roles) that are used for the list on the right side of the template
            context_dict['availableItems'] = []

            possible_roles= Role.objects.filter(gender=actor.gender,country =actor.country)
            for role in possible_roles.order_by('-name'):
                role.url = encode_url(role.name)
                role.purl = encode_url(role.production.title)
                if role not in roles:
                    context_dict['availableItems'].append(role)
    else:
        context_dict={}
    return render_to_response('extras/profile.html', context_dict, context)

def search(request):
    context = RequestContext(request)
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render_to_response('extras/search.html', {'result_list': result_list}, context)
