from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from import_export.models import DataSheetFromCommonNinja, Email_Dump
from django.db import connection



def find_valid_votes_team_wise(game_number, voted_for):

        p = ("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "\
            +"JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "\
                +"WHERE import_export_email_dump.email_confirmed=1 "\
                    +"AND import_export_datasheetfromcommonninja.game='%s' AND import_export_datasheetfromcommonninja.voted_for='%s' AND import_export_datasheetfromcommonninja.round='Semifinals'" % (game_number, voted_for))

        cursor = connection.cursor().execute(p)      
        return cursor.fetchall()[0][0]


def find_invalid_votes_team_wise(game_number, voted_for):

        p = ("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "\
            +"JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "\
                +"WHERE import_export_email_dump.invalid=1 "\
                    +"AND import_export_datasheetfromcommonninja.game='%s' AND import_export_datasheetfromcommonninja.voted_for='%s' AND import_export_datasheetfromcommonninja.round='Semifinals'" % (game_number, voted_for))

        cursor = connection.cursor().execute(p)      
        return cursor.fetchall()[0][0]

def find_pending_votes_team_wise(game_number, voted_for):

        p = ("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "\
            +"JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "\
                +"WHERE import_export_email_dump.varification_pending=1 AND import_export_email_dump.email_confirmed=0 "\
                    +"AND import_export_datasheetfromcommonninja.game='%s' AND import_export_datasheetfromcommonninja.voted_for='%s' AND import_export_datasheetfromcommonninja.round='Semifinals'" % (game_number, voted_for))

        cursor = connection.cursor().execute(p)      
        return cursor.fetchall()[0][0]

class Dashboard(View):

    def get(self, request, *args, **kwargs):

        cursor = connection.cursor().execute("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "+
        "JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "+
        "where import_export_email_dump.email_confirmed=1 "+
        "AND import_export_datasheetfromcommonninja.round='Semifinals'")
        # cursor.execute("SELECT COUNT(*) FROM import_export_email_dump")
        auth_votes = cursor.fetchall()
        # print(result[0][0])



        context = {
            'total_votes':DataSheetFromCommonNinja.objects.filter(round='Semifinals').count(),
            'total_voters':Email_Dump.objects.all().count(),
            'auth_votes': auth_votes[0][0],
            'auth_voters':Email_Dump.objects.filter(email_confirmed=True).count(),
            'varification_pending':Email_Dump.objects.filter(email_confirmed=False, varification_pending=True, invalid=False).count(),
            'invalid_voters':Email_Dump.objects.filter(invalid=True).count(),

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


        return render(request, 'index.html', context)
