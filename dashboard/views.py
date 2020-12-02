from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from upstaged_data.models import Datasheet, Voter
from django.db import connection, transaction
from datetime import date, timedelta, datetime

def find_valid_votes_team_wise(game_number, voted_for):

        try:
            p = ("SELECT COUNT (*) FROM datasheet "\
                +"JOIN voter ON datasheet.email = voter.email "\
                    +"WHERE voter.email_confirmed=True "\
                        +"AND datasheet.game='%s' AND datasheet.voted_for='%s' AND datasheet.round='Semifinals'" % (game_number, voted_for))
            
            cursor = connection.cursor()
            cursor.execute(p)
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print(e) 
            pass


def find_invalid_votes_team_wise(game_number, voted_for):
        try:
            p = ("SELECT COUNT (*) FROM datasheet "\
                +"JOIN voter ON datasheet.email = voter.email "\
                    +"WHERE voter.invalid=True "\
                        +"AND datasheet.game='%s' AND datasheet.voted_for='%s' AND datasheet.round='Semifinals'" % (game_number, voted_for))
            cursor = connection.cursor()
            cursor.execute(p)
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print(e)
            pass

def find_pending_votes_team_wise(game_number, voted_for):

        try: 
            p = ("SELECT COUNT (*) FROM datasheet "\
                +"JOIN voter ON datasheet.email = voter.email "\
                    +"WHERE voter.verification_pending=True AND voter.email_confirmed=False AND voter.invalid=False "\
                        +"AND datasheet.game='%s' AND datasheet.voted_for='%s' AND datasheet.round='Semifinals'" % (game_number, voted_for))
            
            cursor = connection.cursor()
            cursor.execute(p)
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print(e)           
            pass

def total_auth_votes():
        try: 
            p = ("SELECT COUNT (*) FROM datasheet "\
                +"JOIN voter ON datasheet.email = voter.email "\
                    +"WHERE voter.email_confirmed=True")
                        
            cursor = connection.cursor()
            cursor.execute(p)
            row = cursor.fetchone()
            return row[0]

        except Exception as e:
            print(e) 
            pass

def total_invalid_votes():
        try: 
            p = ("SELECT COUNT (*) FROM datasheet "\
                +"JOIN voter ON datasheet.email = voter.email "\
                    +"WHERE voter.invalid=True")
                        
            cursor = connection.cursor()
            cursor.execute(p)
            row = cursor.fetchone()
            return row[0]

        except Exception as e:
            print(e) 
            pass
    

def total_pending_votes():
        try: 
            p = ("SELECT COUNT (*) FROM datasheet "\
                +"JOIN voter ON datasheet.email = voter.email "\
                    +"WHERE voter.verification_pending=True")
                        
            cursor = connection.cursor()
            cursor.execute(p)
            row = cursor.fetchone()
            return row[0]

        except Exception as e:
            print(e) 
            pass

def find_date_wise_votes(obj_list):
        try:
            date_wise_auth_votes = 0
            date_wise_dis_votes = 0
            date_wise_pending_votes = 0
            # ds_list = Datasheet.objects.filter(vote_time__contains=start_date)
            for ds in obj_list:
                if Voter.objects.get(email=ds.email):
                    vtr = Voter.objects.get(email=ds.email)
                    if vtr.email_confirmed:
                        date_wise_auth_votes = date_wise_auth_votes +1
                    if vtr.invalid:
                        date_wise_dis_votes = date_wise_dis_votes +1
                    if vtr.verification_pending:
                        date_wise_pending_votes = date_wise_pending_votes +1
                    
                else:
                    pass
            
            print(date_wise_auth_votes)
            print(date_wise_dis_votes)
            print(date_wise_pending_votes)
            date_wise_total_votes = date_wise_auth_votes + date_wise_dis_votes + date_wise_pending_votes
            date_wise_data_dict = {
                'date_wise_total_votes': date_wise_total_votes,
                'date_wise_auth_votes': date_wise_auth_votes,
                'date_wise_dis_votes': date_wise_dis_votes,
                'date_wise_pending_votes': date_wise_pending_votes,
            }
            return date_wise_data_dict
        except Exception as e:
            print(e) 
            pass

def dashboard_data():
    s = Datasheet.objects.latest('updated_at')
    total_voters = Voter.objects.all().count()
    auth_voters = Voter.objects.filter(email_confirmed=True).count()
    verification_pending = Voter.objects.filter(email_confirmed=False, verification_pending=True, invalid=False).count()
    invalid_voters = Voter.objects.filter(invalid=True).count()



    context = {

        'last_status_updated_dashboard':s.updated_at,
        'total_votes':Datasheet.objects.filter(round='Semifinals').count(),
        'auth_votes': total_auth_votes(),
        'invalid_votes': total_invalid_votes(),
        'dis_votes': total_pending_votes(),
        'total_voters':total_voters ,
        'auth_voters':auth_voters,
        'verification_pending':verification_pending,
        'invalid_voters':invalid_voters,

        'g25_harvard_total_votes': Datasheet.objects.filter(game='25', voted_for='#2 Harvard - Opportunes').count(),
        'g25_harvard_auth_votes': find_valid_votes_team_wise(game_number='25', voted_for='#2 Harvard - Opportunes'),
        'g25_harvard_dis_votes': find_invalid_votes_team_wise(game_number='25', voted_for='#2 Harvard - Opportunes'),
        'g25_harvard_pending_votes': find_pending_votes_team_wise(game_number='25', voted_for='#2 Harvard - Opportunes'),

        'g25_rutgers_total_votes': Datasheet.objects.filter(game='25', voted_for='#2 Rutgers - Raag').values('email').count(),
        'g25_rutgers_auth_votes': find_valid_votes_team_wise(game_number='25', voted_for='#2 Rutgers - Raag'),
        'g25_rutgers_dis_votes': find_invalid_votes_team_wise(game_number='25', voted_for='#2 Rutgers - Raag'),
        'g25_rutgers_pending_votes': find_pending_votes_team_wise(game_number='25', voted_for='#2 Rutgers - Raag'),

        'g26_penn_total_votes': Datasheet.objects.filter(game='26', voted_for='#2 U Penn - Penn Masala').values('email').count(),
        'g26_penn_total_voters': Datasheet.objects.filter(game='26', voted_for='#2 U Penn - Penn Masala').values('email').distinct().count(),
        'g26_penn_auth_votes': find_valid_votes_team_wise(game_number='26', voted_for='#2 U Penn - Penn Masala'),
        'g26_penn_dis_votes': find_invalid_votes_team_wise(game_number='26', voted_for='#2 U Penn - Penn Masala'),
        'g26_penn_pending_votes': find_pending_votes_team_wise(game_number='26', voted_for='#2 U Penn - Penn Masala'),
        
        'g26_illinois_total_votes': Datasheet.objects.filter(game='26', voted_for='#2 U Illinois - No Comment').values('email').count(),
        'g26_illinois_total_voters': Datasheet.objects.filter(game='26', voted_for='#2 U Illinois - No Comment').values('email').distinct().count(),
        'g26_illinois_auth_votes': find_valid_votes_team_wise(game_number='26', voted_for='#2 U Illinois - No Comment'),
        'g26_illinois_dis_votes': find_invalid_votes_team_wise(game_number='26', voted_for='#2 U Illinois - No Comment'),
        'g26_illinois_pending_votes': find_pending_votes_team_wise(game_number='26', voted_for='#2 U Illinois - No Comment'),

        'g27_vanderbilt_total_votes': Datasheet.objects.filter(game='27', voted_for='#1 Vanderbilt - Melodores').values('email').count(),
        'g27_vanderbilt_total_voters': Datasheet.objects.filter(game='27', voted_for='#1 Vanderbilt - Melodores').values('email').distinct().count(),
        'g27_vanderbilt_auth_votes': find_valid_votes_team_wise(game_number='27', voted_for='#1 Vanderbilt - Melodores'),
        'g27_vanderbilt_dis_votes': find_invalid_votes_team_wise(game_number='27', voted_for='#1 Vanderbilt - Melodores'),
        'g27_vanderbilt_pending_votes': find_pending_votes_team_wise(game_number='27', voted_for='#1 Vanderbilt - Melodores'),

        'g27_florida_total_votes': Datasheet.objects.filter(game='27', voted_for='#3 Florida State - All-Night Yahtzee').values('email').count(),
        'g27_florida_total_voters': Datasheet.objects.filter(game='27', voted_for='#3 Florida State - All-Night Yahtzee').values('email').distinct().count(),
        'g27_florida_auth_votes': find_valid_votes_team_wise(game_number='27', voted_for='#3 Florida State - All-Night Yahtzee'),
        'g27_florida_dis_votes': find_invalid_votes_team_wise(game_number='27', voted_for='#3 Florida State - All-Night Yahtzee'),
        'g27_florida_pending_votes': find_pending_votes_team_wise(game_number='27', voted_for='#3 Florida State - All-Night Yahtzee'),


        'g28_bringham_total_votes': Datasheet.objects.filter(game='28', voted_for='#2 Brigham Young U - Vocal Point').values('email').count(),
        'g28_bringham_total_voters': Datasheet.objects.filter(game='28', voted_for='#2 Brigham Young U - Vocal Point').values('email').distinct().count(),
        'g28_bringham_auth_votes': find_valid_votes_team_wise(game_number='28', voted_for='#2 Brigham Young U - Vocal Point'),
        'g28_bringham_dis_votes': find_invalid_votes_team_wise(game_number='28', voted_for='#2 Brigham Young U - Vocal Point'),
        'g28_bringham_pending_votes': find_pending_votes_team_wise(game_number='28', voted_for='#2 Brigham Young U - Vocal Point'),

        'g28_ucla_total_votes': Datasheet.objects.filter(game='28', voted_for='#1 UCLA - Scattertones').values('email').count(),
        'g28_ucla_total_voters': Datasheet.objects.filter(game='28', voted_for='#1 UCLA - Scattertones').values('email').distinct().count(),
        'g28_ucla_auth_votes': find_valid_votes_team_wise(game_number='28', voted_for='#1 UCLA - Scattertones'),
        'g28_ucla_dis_votes': find_invalid_votes_team_wise(game_number='28', voted_for='#1 UCLA - Scattertones'),
        'g28_ucla_pending_votes': find_pending_votes_team_wise(game_number='28', voted_for='#1 UCLA - Scattertones'),

    }

    context['auth_votes_percent'] = (total_auth_votes()/context['total_votes'])*100
    context['auth_voters_percent'] = (auth_voters/context['total_voters'])*100
    context['pending_voters_percent'] = (verification_pending/context['total_voters'])*100
    context['invalid_voters_percent'] = (invalid_voters/context['total_voters'])*100

    context['g25_p1_auth_prcnt'] = (context['g25_harvard_auth_votes']/context['g25_harvard_total_votes'])*100
    context['g25_p1_dis_prcnt'] = (context['g25_harvard_dis_votes']/context['g25_harvard_total_votes'])*100
    context['g25_p1_pending_prcnt'] = (context['g25_harvard_pending_votes']/context['g25_harvard_total_votes'])*100

    context['g25_p2_auth_prcnt'] = (context['g25_rutgers_auth_votes']/context['g25_rutgers_total_votes'])*100
    context['g25_p2_dis_prcnt'] = (context['g25_rutgers_dis_votes']/context['g25_rutgers_total_votes'])*100
    context['g25_p2_pending_prcnt'] = (context['g25_rutgers_pending_votes']/context['g25_rutgers_total_votes'])*100

    context['g26_p1_auth_prcnt'] = (context['g26_penn_auth_votes']/context['g26_penn_total_votes'])*100
    context['g26_p1_dis_prcnt'] = (context['g26_penn_dis_votes']/context['g26_penn_total_votes'])*100
    context['g26_p1_pending_prcnt'] = (context['g26_penn_pending_votes']/context['g26_penn_total_votes'])*100

    context['g26_p2_auth_prcnt'] = (context['g26_illinois_auth_votes']/context['g26_illinois_total_votes'])*100
    context['g26_p2_dis_prcnt'] = (context['g26_illinois_dis_votes']/context['g26_illinois_total_votes'])*100
    context['g26_p2_pending_prcnt'] = (context['g26_illinois_pending_votes']/context['g26_illinois_total_votes'])*100

    context['g27_p1_auth_prcnt'] = (context['g27_vanderbilt_auth_votes']/context['g27_vanderbilt_total_votes'])*100
    context['g27_p1_dis_prcnt'] = (context['g27_vanderbilt_dis_votes']/context['g27_vanderbilt_total_votes'])*100
    context['g27_p1_pending_prcnt'] = (context['g27_vanderbilt_pending_votes']/context['g27_vanderbilt_total_votes'])*100

    context['g27_p2_auth_prcnt'] = (context['g27_florida_auth_votes']/context['g27_florida_total_votes'])*100
    context['g27_p2_dis_prcnt'] = (context['g27_florida_dis_votes']/context['g27_florida_total_votes'])*100
    context['g27_p2_pending_prcnt'] = (context['g27_florida_pending_votes']/context['g27_florida_total_votes'])*100

    context['g28_p1_auth_prcnt'] = (context['g28_bringham_auth_votes']/context['g28_bringham_total_votes'])*100
    context['g28_p1_dis_prcnt'] = (context['g28_bringham_dis_votes']/context['g28_bringham_total_votes'])*100
    context['g28_p1_pending_prcnt'] = (context['g28_bringham_pending_votes']/context['g28_bringham_total_votes'])*100

    context['g28_p2_auth_prcnt'] = (context['g28_ucla_auth_votes']/context['g28_ucla_total_votes'])*100
    context['g28_p2_dis_prcnt'] = (context['g28_ucla_dis_votes']/context['g28_ucla_total_votes'])*100
    context['g28_p2_pending_prcnt'] = (context['g28_ucla_pending_votes']/context['g28_ucla_total_votes'])*100

    g25_all_auth_pending_vote = (context['g25_harvard_auth_votes'] + context['g25_harvard_pending_votes'] + context['g25_rutgers_auth_votes'] + context['g25_rutgers_pending_votes'] )
    g26_all_auth_pending_vote = (context['g26_penn_auth_votes'] + context['g26_penn_pending_votes'] + context['g26_illinois_auth_votes'] + context['g26_illinois_pending_votes'] )
    g27_all_auth_pending_vote = (context['g27_vanderbilt_auth_votes'] + context['g27_vanderbilt_pending_votes'] + context['g27_florida_auth_votes'] + context['g27_florida_pending_votes'] )
    g28_all_auth_pending_vote = (context['g28_bringham_auth_votes'] + context['g28_bringham_pending_votes'] + context['g28_ucla_auth_votes'] + context['g28_ucla_pending_votes'] )
    
    context['g25_p1_prcnt'] = ((context['g25_harvard_auth_votes'] + context['g25_harvard_pending_votes']) / g25_all_auth_pending_vote)*100
    context['g25_p2_prcnt'] = ((context['g25_rutgers_auth_votes'] + context['g25_rutgers_pending_votes']) / g25_all_auth_pending_vote)*100

    context['g26_p1_prcnt'] = ((context['g26_penn_auth_votes'] + context['g26_penn_pending_votes']) / g26_all_auth_pending_vote)*100
    context['g26_p2_prcnt'] = ((context['g26_illinois_auth_votes'] + context['g26_illinois_pending_votes']) / g26_all_auth_pending_vote)*100
    
    context['g27_p1_prcnt'] = ((context['g27_vanderbilt_auth_votes'] + context['g27_vanderbilt_pending_votes']) / g27_all_auth_pending_vote)*100
    context['g27_p2_prcnt'] = ((context['g27_florida_auth_votes'] + context['g27_florida_pending_votes']) / g27_all_auth_pending_vote)*100       
    
    context['g28_p1_prcnt'] = ((context['g28_bringham_auth_votes'] + context['g28_bringham_pending_votes']) / g28_all_auth_pending_vote)*100
    context['g28_p2_prcnt'] = ((context['g28_ucla_auth_votes'] + context['g28_ucla_pending_votes']) / g28_all_auth_pending_vote)*100

    return context

class Dashboard(View):

    def get(self, request, *args, **kwargs):
        context = dashboard_data()
        today = date.today()
        d = today.strftime("%Y-%m-%d")
        # print(d)
        vts_obj_list = []
        vts_obj_list.extend(Datasheet.objects.filter(vote_time__contains=d))
        context['date_wise_data_dict'] = find_date_wise_votes(vts_obj_list)

        return render(request, 'index.html', context)


    def post(self, request, *args, **kwargs):
        context = dashboard_data()

        is_private = request.POST.get('dates', False)
        x = is_private.split(" - ")
        
        # print(x)
        # print(type(x))
        # print(type(is_private))
        
        sd = str(x[0]).split("/")
        ed = str(x[1]).split("/")
        print(sd)
        start_date = sd[2]+'-'+sd[0]+'-'+sd[1]
        # print(type(str(x[0])))
        sdate = date(int(sd[2]), int(sd[0]), int(sd[1]))   # start date date format -  # 2020-11-23
        # print(sdate)
        edate = date(int(ed[2]), int(ed[0]), int(ed[1]))   # end date
        # print(edate)

        delta = edate - sdate       # as timedelta

        # print(delta.days)
        
        vts_obj_list = []
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            # print(day)
            vts_obj_list.extend(Datasheet.objects.filter(vote_time__contains=day.strftime('%Y-%m-%d')))

        context['date_wise_data_dict'] = find_date_wise_votes(vts_obj_list)
        # print(len(obj_list))


        return render(request, 'index.html', context )

    



def date_wise_vote_list(request):
    if request.method=="POST":
        is_private = request.POST.get('dates', False)
        x = is_private.split(" - ")
        
        # print(x)
        # print(type(x))
        # print(type(is_private))
        
        sd = str(x[0]).split("/")
        ed = str(x[1]).split("/")
        print(sd)
        start_date = sd[2]+'-'+sd[0]+'-'+sd[1]
        # print(type(str(x[0])))
        sdate = date(int(sd[2]), int(sd[0]), int(sd[1]))   # start date date format -  # 2020-11-23
        # print(sdate)
        edate = date(int(ed[2]), int(ed[0]), int(ed[1]))   # end date
        # print(edate)

        delta = edate - sdate       # as timedelta
    
        obj_list = []
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            obj_list.extend(Datasheet.objects.filter(vote_time__contains=day.strftime('%Y-%m-%d')))

        find_date_wise_votes(obj_list)
        # print(len(obj_list))
        context = {
            'object_list': obj_list
        }

        return render(request, 'dashboard/date_wise_votes_list.html', context)
    return render(request, 'dashboard/date_wise_votes_list.html', )