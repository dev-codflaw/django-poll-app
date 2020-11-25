from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from import_export.models import DataSheetFromCommonNinja, Email_Dump


class Dashboard(View):
    def get(self, request, *args, **kwargs):
        context = {
            'total_votes':DataSheetFromCommonNinja.objects.filter(round='Semifinals').count(),
            'total_voters':DataSheetFromCommonNinja.objects.order_by().values('email').distinct().count(),
            'auth_votes':'0',
            'auth_voters':Email_Dump.objects.filter(email_confirmed=True).count(),
            'varification_pending':Email_Dump.objects.filter(email_confirmed=False, varification_pending=True).count(),
            'invalid_voters':Email_Dump.objects.filter(invalid=True).count(),

            'g25_harvard_total_votes': DataSheetFromCommonNinja.objects.filter(game='25', voted_for='#2 Harvard - Opportunes').values('email').count(),
            'g25_harvard_total_voters': DataSheetFromCommonNinja.objects.filter(game='25', voted_for='#2 Harvard - Opportunes').values('email').distinct().count(),
            'g25_harvard_auth_votes': '0',
            'g25_harvard_auth_voters': '0',

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

        ds_obj_list = list(DataSheetFromCommonNinja.objects.all())

        voter_obj_list = list(Email_Dump.objects.filter(email_confirmed=True))




        # context['data'] = ds_obj_list
        # context['data1'] = voter_obj_list

        return render(request, 'index.html', context)
