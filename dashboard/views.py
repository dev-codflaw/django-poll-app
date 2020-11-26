from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from import_export.models import DataSheetFromCommonNinja, Email_Dump
from django.db import connection



# def find_valid_votes_team_wise(game_number, voted_for):

#         cursor = connection.cursor().execute("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "+
#         "LEFT JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "+
#         "WHERE import_export_email_dump.email_confirmed=1 "+
#         "AND import_export_datasheetfromcommonninja.game="+game_number+
#         " AND import_export_datasheetfromcommonninja.voted_for='#2 Harvard - Opportunes'"+
#         " AND import_export_datasheetfromcommonninja.round='Semifinals'")        
#         return cursor.fetchall()[0][0]


class Dashboard(View):

    def get(self, request, *args, **kwargs):

        cursor = connection.cursor().execute("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "+
        "JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "+
        "where import_export_email_dump.email_confirmed=1 "+
        "AND import_export_datasheetfromcommonninja.round='Semifinals'")
        # cursor.execute("SELECT COUNT(*) FROM import_export_email_dump")
        auth_votes = cursor.fetchall()
        # print(result[0][0])

        cursor = connection.cursor().execute("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "+
        "LEFT JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "+
        "where import_export_email_dump.email_confirmed=1 "+
        "AND import_export_datasheetfromcommonninja.round='Semifinals' AND import_export_datasheetfromcommonninja.game='25' AND import_export_datasheetfromcommonninja.voted_for='#2 Harvard - Opportunes'")
        g25_harvard_auth_votes = cursor.fetchall()[0][0]

        cursor = connection.cursor().execute("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "+
        "LEFT JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "+
        "where import_export_email_dump.invalid=1 "+
        "AND import_export_datasheetfromcommonninja.round='Semifinals' AND import_export_datasheetfromcommonninja.game='25' AND import_export_datasheetfromcommonninja.voted_for='#2 Harvard - Opportunes'")
        g25_harvard_dis_votes = cursor.fetchall()[0][0]

        cursor = connection.cursor().execute("SELECT COUNT (*) FROM import_export_datasheetfromcommonninja "+
        "JOIN import_export_email_dump ON import_export_datasheetfromcommonninja.email = import_export_email_dump.email "+
        "WHERE import_export_email_dump.varification_pending=1 AND import_export_email_dump.email_confirmed=0 AND import_export_email_dump.invalid=0 "+
        "AND import_export_datasheetfromcommonninja.round='Semifinals' AND import_export_datasheetfromcommonninja.game='25' AND import_export_datasheetfromcommonninja.voted_for='#2 Harvard - Opportunes'")
        g25_harvard_pending_votes = cursor.fetchall()[0][0]


        context = {
            'total_votes':DataSheetFromCommonNinja.objects.filter(round='Semifinals').count(),
            'total_voters':DataSheetFromCommonNinja.objects.order_by().values('email').distinct().count(),
            'auth_votes': auth_votes[0][0],
            'auth_voters':Email_Dump.objects.filter(email_confirmed=True).count(),
            'varification_pending':Email_Dump.objects.filter(email_confirmed=False, varification_pending=True, invalid=False).count(),
            'invalid_voters':Email_Dump.objects.filter(invalid=True).count(),

            'g25_harvard_total_votes': DataSheetFromCommonNinja.objects.filter(game='25', voted_for='#2 Harvard - Opportunes').count(),
            'g25_harvard_total_voters': DataSheetFromCommonNinja.objects.filter(game='25', voted_for='#2 Harvard - Opportunes').values('email').distinct().count(),
            'g25_harvard_auth_votes': g25_harvard_auth_votes,
            # 'g25_harvard_auth_votes': find_valid_votes_team_wise(game_number='25', voted_for='#2 Harvard - Opportunes'),
            'g25_harvard_dis_votes': g25_harvard_dis_votes,
            'g25_harvard_pending_votes': g25_harvard_pending_votes,

            'g25_rutgers_total_votes': DataSheetFromCommonNinja.objects.filter(game='25', voted_for='#2 Rutgers - Raag').values('email').count(),
            'g25_rutgers_total_voters': DataSheetFromCommonNinja.objects.filter(game='25', voted_for='#2 Rutgers - Raag').values('email').distinct().count(),
            'g25_rutgers_auth_votes': '0',
            'g25_rutgers_auth_voters': '0',

            'g26_penn_total_votes': DataSheetFromCommonNinja.objects.filter(game='26', voted_for='#2 U Penn - Penn Masala').values('email').count(),
            'g26_penn_total_voters': DataSheetFromCommonNinja.objects.filter(game='26', voted_for='#2 U Penn - Penn Masala').values('email').distinct().count(),
            'g26_penn_auth_votes': '0',
            'g26_penn_auth_voters': '0',
            
            'g26_illinois_total_votes': DataSheetFromCommonNinja.objects.filter(game='26', voted_for='#2 U Illinois - No Comment').values('email').count(),
            'g26_illinois_total_voters': DataSheetFromCommonNinja.objects.filter(game='26', voted_for='#2 U Illinois - No Comment').values('email').distinct().count(),
            'g26_illinois_auth_votes': '0',
            'g26_illinois_auth_voters': '0',

            'g27_vanderbilt_total_votes': DataSheetFromCommonNinja.objects.filter(game='27', voted_for='#1 Vanderbilt - Melodores').values('email').count(),
            'g27_vanderbilt_total_voters': DataSheetFromCommonNinja.objects.filter(game='27', voted_for='#1 Vanderbilt - Melodores').values('email').distinct().count(),
            'g27_vanderbilt_auth_votes': '0',
            'g27_vanderbilt_auth_voters': '0',

            'g27_florida_total_votes': DataSheetFromCommonNinja.objects.filter(game='27', voted_for='#3 Florida State - All-Night Yahtzee').values('email').count(),
            'g27_florida_total_voters': DataSheetFromCommonNinja.objects.filter(game='27', voted_for='#3 Florida State - All-Night Yahtzee').values('email').distinct().count(),
            'g27_florida_auth_votes': '0',
            'g27_florida_auth_voters': '0',


            'g28_bringham_total_votes': DataSheetFromCommonNinja.objects.filter(game='28', voted_for='#2 Brigham Young U - Vocal Point').values('email').count(),
            'g28_bringham_total_voters': DataSheetFromCommonNinja.objects.filter(game='28', voted_for='#2 Brigham Young U - Vocal Point').values('email').distinct().count(),
            'g28_bringham_auth_votes': '0',
            'g28_bringham_auth_voters': '0',

            'g28_ucla_total_votes': DataSheetFromCommonNinja.objects.filter(game='28', voted_for='#1 UCLA - Scattertones').values('email').count(),
            'g28_ucla_total_voters': DataSheetFromCommonNinja.objects.filter(game='28', voted_for='#1 UCLA - Scattertones').values('email').distinct().count(),
            'g28_ucla_auth_votes': '0',
            'g28_ucla_auth_voters': '0',

        }


        return render(request, 'index.html', context)
