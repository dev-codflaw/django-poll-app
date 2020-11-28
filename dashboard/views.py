from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from import_export.models import DataSheetFromCommonNinja, Email_Dump
from django.db import connection, transaction


def find_valid_votes_team_wise(game_number, voted_for):

        try:
            p = ("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "\
                +"JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "\
                    +"WHERE import_export_email_dump.email_confirmed=True "\
                        +"AND import_export_datasheetfromcommonninja.game='%s' AND import_export_datasheetfromcommonninja.voted_for='%s' AND import_export_datasheetfromcommonninja.round='Semifinals'" % (game_number, voted_for))
            
            cursor = connection.cursor()
            cursor.execute(p)
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print(e) 
            pass



def find_invalid_votes_team_wise(game_number, voted_for):
        try:
            p = ("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "\
                +"JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "\
                    +"WHERE import_export_email_dump.invalid=True "\
                        +"AND import_export_datasheetfromcommonninja.game='%s' AND import_export_datasheetfromcommonninja.voted_for='%s' AND import_export_datasheetfromcommonninja.round='Semifinals'" % (game_number, voted_for))
            cursor = connection.cursor()
            cursor.execute(p)
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print(e)
            pass

def find_pending_votes_team_wise(game_number, voted_for):

        try: 
            p = ("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "\
                +"JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "\
                    +"WHERE import_export_email_dump.verification_pending=True AND import_export_email_dump.email_confirmed=False AND import_export_email_dump.invalid=False "\
                        +"AND import_export_datasheetfromcommonninja.game='%s' AND import_export_datasheetfromcommonninja.voted_for='%s' AND import_export_datasheetfromcommonninja.round='Semifinals'" % (game_number, voted_for))
            
            cursor = connection.cursor()
            cursor.execute(p)
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print(e)           
            pass

def total_auth_votes():
        try: 
            p = ("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "\
                +"JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "\
                    +"WHERE import_export_email_dump.email_confirmed=True")
                        
            cursor = connection.cursor()
            cursor.execute(p)
            row = cursor.fetchone()
            return row[0]

        except Exception as e:
            print(e) 
            pass


class Dashboard(View):

    def get(self, request, *args, **kwargs):
        
        s = DataSheetFromCommonNinja.objects.values('updated_at').order_by('id')[0]
        total_voters = Email_Dump.objects.all().count()
        auth_voters = Email_Dump.objects.filter(email_confirmed=True).count()
        verification_pending = Email_Dump.objects.filter(email_confirmed=False, verification_pending=True, invalid=False).count()
        invalid_voters = Email_Dump.objects.filter(invalid=True).count()


        context = {

            'last_status_updated_dashboard':s['updated_at'],
            'total_votes':DataSheetFromCommonNinja.objects.filter(round='Semifinals').count(),
            'auth_votes': total_auth_votes(),
            'total_voters':total_voters ,
            'auth_voters':auth_voters,
            'verification_pending':verification_pending,
            'invalid_voters':invalid_voters,

            'g25_harvard_total_votes': DataSheetFromCommonNinja.objects.filter(game='25', voted_for='#2 Harvard - Opportunes').count(),
            'g25_harvard_auth_votes': find_valid_votes_team_wise(game_number='25', voted_for='#2 Harvard - Opportunes'),
            'g25_harvard_dis_votes': find_invalid_votes_team_wise(game_number='25', voted_for='#2 Harvard - Opportunes'),
            'g25_harvard_pending_votes': find_pending_votes_team_wise(game_number='25', voted_for='#2 Harvard - Opportunes'),

            'g25_rutgers_total_votes': DataSheetFromCommonNinja.objects.filter(game='25', voted_for='#2 Rutgers - Raag').values('email').count(),
            'g25_rutgers_auth_votes': find_valid_votes_team_wise(game_number='25', voted_for='#2 Rutgers - Raag'),
            'g25_rutgers_dis_votes': find_invalid_votes_team_wise(game_number='25', voted_for='#2 Rutgers - Raag'),
            'g25_rutgers_pending_votes': find_pending_votes_team_wise(game_number='25', voted_for='#2 Rutgers - Raag'),

            'g26_penn_total_votes': DataSheetFromCommonNinja.objects.filter(game='26', voted_for='#2 U Penn - Penn Masala').values('email').count(),
            'g26_penn_total_voters': DataSheetFromCommonNinja.objects.filter(game='26', voted_for='#2 U Penn - Penn Masala').values('email').distinct().count(),
            'g26_penn_auth_votes': find_valid_votes_team_wise(game_number='26', voted_for='#2 U Penn - Penn Masala'),
            'g26_penn_dis_votes': find_invalid_votes_team_wise(game_number='26', voted_for='#2 U Penn - Penn Masala'),
            'g26_penn_pending_votes': find_pending_votes_team_wise(game_number='26', voted_for='#2 U Penn - Penn Masala'),
            
            'g26_illinois_total_votes': DataSheetFromCommonNinja.objects.filter(game='26', voted_for='#2 U Illinois - No Comment').values('email').count(),
            'g26_illinois_total_voters': DataSheetFromCommonNinja.objects.filter(game='26', voted_for='#2 U Illinois - No Comment').values('email').distinct().count(),
            'g26_illinois_auth_votes': find_valid_votes_team_wise(game_number='26', voted_for='#2 U Illinois - No Comment'),
            'g26_illinois_dis_votes': find_invalid_votes_team_wise(game_number='26', voted_for='#2 U Illinois - No Comment'),
            'g26_illinois_pending_votes': find_pending_votes_team_wise(game_number='26', voted_for='#2 U Illinois - No Comment'),

            'g27_vanderbilt_total_votes': DataSheetFromCommonNinja.objects.filter(game='27', voted_for='#1 Vanderbilt - Melodores').values('email').count(),
            'g27_vanderbilt_total_voters': DataSheetFromCommonNinja.objects.filter(game='27', voted_for='#1 Vanderbilt - Melodores').values('email').distinct().count(),
            'g27_vanderbilt_auth_votes': find_valid_votes_team_wise(game_number='27', voted_for='#1 Vanderbilt - Melodores'),
            'g27_vanderbilt_dis_votes': find_invalid_votes_team_wise(game_number='27', voted_for='#1 Vanderbilt - Melodores'),
            'g27_vanderbilt_pending_votes': find_pending_votes_team_wise(game_number='27', voted_for='#1 Vanderbilt - Melodores'),

            'g27_florida_total_votes': DataSheetFromCommonNinja.objects.filter(game='27', voted_for='#3 Florida State - All-Night Yahtzee').values('email').count(),
            'g27_florida_total_voters': DataSheetFromCommonNinja.objects.filter(game='27', voted_for='#3 Florida State - All-Night Yahtzee').values('email').distinct().count(),
            'g27_florida_auth_votes': find_valid_votes_team_wise(game_number='27', voted_for='#3 Florida State - All-Night Yahtzee'),
            'g27_florida_dis_votes': find_invalid_votes_team_wise(game_number='27', voted_for='#3 Florida State - All-Night Yahtzee'),
            'g27_florida_pending_votes': find_pending_votes_team_wise(game_number='27', voted_for='#3 Florida State - All-Night Yahtzee'),


            'g28_bringham_total_votes': DataSheetFromCommonNinja.objects.filter(game='28', voted_for='#2 Brigham Young U - Vocal Point').values('email').count(),
            'g28_bringham_total_voters': DataSheetFromCommonNinja.objects.filter(game='28', voted_for='#2 Brigham Young U - Vocal Point').values('email').distinct().count(),
            'g28_bringham_auth_votes': find_valid_votes_team_wise(game_number='28', voted_for='#2 Brigham Young U - Vocal Point'),
            'g28_bringham_dis_votes': find_invalid_votes_team_wise(game_number='28', voted_for='#2 Brigham Young U - Vocal Point'),
            'g28_bringham_pending_votes': find_pending_votes_team_wise(game_number='28', voted_for='#2 Brigham Young U - Vocal Point'),

            'g28_ucla_total_votes': DataSheetFromCommonNinja.objects.filter(game='28', voted_for='#1 UCLA - Scattertones').values('email').count(),
            'g28_ucla_total_voters': DataSheetFromCommonNinja.objects.filter(game='28', voted_for='#1 UCLA - Scattertones').values('email').distinct().count(),
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


        return render(request, 'index.html', context)

