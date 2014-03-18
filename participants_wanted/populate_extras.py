import os

def populate():
    # Actor Users
    new_actor_user1 = add_user('actorWannaB','Nicolas','Cage','nicCage@rage.com','1',False)
    new_actor_user2 = add_user('jnr','Robert','Downey Jnr','rdjnr@ironman.com','1',False)
    new_actor_user3 = add_user('bpitt','Brad','Pitt','achilles@troy.com','1',False)

    # Director Users
    new_director_user1 = add_user('steve','Steven','Spielberg','sup@hollywood.com','1',True)
    new_director_user2 = add_user('ridders','Ridley','Scott','maximus@gladiator.com','1',True)
    new_director_user3 = add_user('kiwi','Peter','Jackson','forGondor@lotr.com','1',True)
    new_director_user4 = add_user('god','George','Lucas','god@lucasfilm.com','1',True)	
    new_director_user5 = add_user('terminator_creator','Alan','Taylor','alan@terminate.com','1',True)
    new_director_user6 = add_user('baz','Baz','Luhrman','baz@musicfilms.com','1',True)

    # Actors
    new_actor1 = add_actor(new_actor_user1,'USA','1986-12-18','180','152','brown','brown','male','4.2')
    new_actor2 = add_actor(new_actor_user2,'USA','1986-12-18','180','152','brown','brown','male','4.2')
    new_actor3 = add_actor(new_actor_user3,'USA','1986-12-18','180','152','brown','brown','male','4.2')
    
    # Directors
    new_director1 = add_director(new_director_user1,'Hollywood','www.jaws.com','07701445267')
    new_director2 = add_director(new_director_user2,'Hollywood','www.gladiator.com','07701445267')
    new_director3 = add_director(new_director_user3,'Hollywood','www.kingkong.com','07701445267')
    new_director4 = add_director(new_director_user4,'California','www.lucasfilm.com','1194596960381')
    new_director5 = add_director(new_director_user5,'Hollywood','www.terminatorgenesis.com','93743588246')
    new_director6 = add_director(new_director_user6,'Hollywood','www.musicfilms.com','7686665789')

    # Productions
    new_production1 = add_production('1234',new_director1,'Avatar 2','Sequel to the sucky Avatar','Fantasy','2014-03-23','2014-03-24','8000000')
    new_production2 = add_production('1235',new_director2,'Prometheus Returns','Sequel to Prometheus','Sci-Fi','2014-03-23','2014-03-24','65000')
    new_production3 = add_production('1236',new_director3,'The Hobbit 3','Third part of The Hobbit ','Fantasy','2014-03-23','2014-03-24','80000')
    new_production4 = add_production('1237',new_director4,'Star Wars VII','Sequel to Star Wars','Sci-Fi','2014-03-17','2014-05-10','1000000')
    new_production5 = add_production('1238',new_director5,'Terminator: Genesis','Sequel to Terminator','Sci-Fi','2014-03-20','2014-04-20','75000')
    new_production6 = add_production('1239',new_director6,'Moulin Rouge','Romantic musical','Drama/Romance/Musical','2014-03-25','2014-05-24','30000')
    new_production7 = add_production('1240',new_director6,'The Great Gatsby','Remake of The Great Gatsby','Drama/Romance','2014-06-10','2014-07-10','60000')
    new_production8 = add_production('1241',new_director6,'Mamma Mia','Remake of the famous musical','Comedy/Romance/Musical','2014-06-10','2014-07-10','25000')

    # Role
    new_role1 = add_role(new_production1,'Male','Actor','Tail love','Umbeeba')
    new_role2 = add_role(new_production2,'Male','Actor','Alien killer, Male version of Ripley','Rips')
    new_role3 = add_role(new_production3,'Female','Actor','Female dwarf?','Wendy')
    new_role4 = add_role(new_production4,'Male','Actor', 'Handsome male actor, good at martial arts', 'Jedi')
    new_role5 = add_role(new_production4,'Male','Dwarf', 'Male dwarf to play the part of an ewok', 'Ewok')
    new_role6 = add_role(new_production4,'Male/Female','Actor', 'Must run fast', 'Stormtrooper')
    new_role7 = add_role(new_production5,'Female','Actor','Female aged 18 to 30 good looking and attractive.','Female Terminator')
    new_role8 = add_role(new_production8,'Female','Singer','Wanted female actor/singer - playing age - twenties/early thirties (younger looks are the important factor rather than age).  good singing voice is essential coupled with competent acting skills.','Mamma Mia Role')
    


    # Application
    new_application1 = add_application(new_role1,new_actor1,'2014-03-01','Accepted')
    new_application2 = add_application(new_role2,new_actor2,'2014-03-01','Accepted')
    new_application3 = add_application(new_role3,new_actor3,'2014-03-01','Accepted')
   

def add_user(username,fname,lname,email,password,is_staff):
    u = User.objects.get_or_create(username=username,first_name=fname,last_name=lname,email=email,password=password,is_staff=is_staff)[0]
    u.set_password(password)
    u.save()
    return u

def add_actor(user,country,dob,weight,height,hColour,eColour,gender,rating):
    #u = add_user(username,fname,lname,email,password)
    a = Actor.objects.get_or_create(user=user,country=country,
        dateOfBirth=dob,weight=weight,height=height,hairColour=hColour,eyeColour=eColour,gender=gender,rating=rating)[0]
    return a

def add_director(user,agency,website,phone):
    #u = add_user(username,fname,lname,email,password)
    d = Director.objects.get_or_create(user=user,agency=agency,website=website,phone=phone)[0]
    return d


def add_production(pID,director,title,description,genre,openingDate,closingDate,cost):
    p = Production.objects.get_or_create(productionID=pID,director=director,title=title,description=description,genre=genre,openingDate=openingDate,closingDate=closingDate,cost=cost)[0]
    return p

def add_role(production,gender,roleType,description,name):
    r = Role.objects.get_or_create(production=production,gender=gender,roleType=roleType,description=description,name=name)[0]
    return r

def add_application(role,actor,date,outcome):
    ap = Application.objects.get_or_create(role=role,actor=actor,date=date,outcome=outcome)[0]
    return ap	

# start execution here
if __name__=='__main__':
    print "Starting extras population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'participants_wanted.settings')
    from extras.models import Actor, Director, User, Production, Role, Application  
    populate()
    print "Populate complete"
