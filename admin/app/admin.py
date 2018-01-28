from django.contrib import admin
from .models import User, SingleUploadImg, VolunteerInfo, CharityCampaign, ProServ, VolServ, VolTraining, PolicyQA
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['user_subscribe_time', 'nickname', 'user_city','user_sex',
                       'user_country', 'user_province', 'user_language',
                       'user_subscribe_time','user_volunteer_or_not']
    fieldsets = [
        ('个人信息', {'fields': ['nickname', 'name', 'cellphone', 'user_sex', 'user_city',
                             'user_country', 'user_province', 'user_language',
                             'user_subscribe_time', 'user_volunteer_or_not']}),
        # ('活动清单', {'fields': ('signup_user_list',)}),
        # ('访问信息', {'fields': readonly_fields})
        # ('访问信息',{'fields': ['user_access_token', 'user_access_time', 'user_refresh_token', 'user_refresh_time']}),
    ]
    list_display = ['nickname', 'name', 'cellphone', 'user_sex', 'user_city',
                    'user_country', 'user_province', 'is_volunteer', 'user_subscribe_time']

# class UserInfoInline(admin.TabularInline):
#     model = User
#     extra = 1


admin.site.register(User, UserAdmin)


class CharityCampaignAdmin(admin.ModelAdmin):
    # readonly_fields = ['user_subscribe_time', 'nickname', 'user_city',
    #                    'user_country', 'user_province', 'user_language',
    #                    'user_subscribe_time']
    fieldsets = [
        ('活动信息', {'fields': ['campaign_name', 'campaign_type', 'campaign_date', 'campaign_client', 'campaign_address',
                             'campaign_content', 'campaign_paid', 'campaign_signup_deadline',
                             'campaign_contact', 'campaign_counts','photos']}),
        ('报名人选', {'fields': ['signup_user_list']}),
        # ('活动清单', {'fields': ('signup_user_list',)}),
        # ('访问信息', {'fields': readonly_fields})
        # ('访问信息',{'fields': ['user_access_token', 'user_access_time', 'user_refresh_token', 'user_refresh_time']}),
    ]
    list_display = ('campaign_name', 'campaign_type', 'campaign_date',
                    'campaign_signup_deadline', 'campaign_counts', 'user_list')


admin.site.register(CharityCampaign, CharityCampaignAdmin)


class ProServAdmin(admin.ModelAdmin):
        # readonly_fields = ['user_subscribe_time', 'nickname', 'user_city',
    #                    'user_country', 'user_province', 'user_language',
    #                    'user_subscribe_time']
    readonly_fields = []
    fieldsets = [
        ('负责方信息', {'fields': ['sw_name', 'case_id', 'counseling_date']}),
        ('初始信息',{'fields':['proserv_counseling','proserv_question_title','proserv_question_content']}),
        ('客户信息', {'fields': ['proserv_name','proserv_sex','proserv_contact','proserv_age', 'proserv_jiguan',
                             'proserv_house_hold', 'proserv_id_num', 'proserv_ethnic', 'proserv_political_status',
                             'proserv_religion', 'proserv_occupation', 'proserv_studying_grade', 'proserv_degree_of_education',
                             'proserv_community', 'proserv_live_address', 'proserv_married',
                             ]}),
        ('服务信息', {'fields': ['social_assistance', 'counseling_results']})
        # ('活动清单', {'fields': ('signup_user_list',)}),
        # ('访问信息', {'fields': readonly_fields})
        # ('访问信息',{'fields': ['user_access_token', 'user_access_time', 'user_refresh_token', 'user_refresh_time']}),
    ]
    list_display = ('case_id', 'sw_name', 'counseling_date',
                    'proserv_name', 'proserv_sex', 'proserv_contact')
    # 遗留问题:想要在详细信息里列出姓名、性别和联系方式，因为不是field，会出错


admin.site.register(ProServ, ProServAdmin)


class VolunteerInfoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('基本信息', {'fields': ['volinfo_name',
                             'volinfo_sex', 'volinfo_cell_number']}),
        ('详细信息', {'fields': ['volinfo_age', 'volinfo_jiguan',
                             'volinfo_live_address', 'volinfo_married', 'volinfo_idcard_type', 'volinfo_id_num',
                             'volinfo_birthday', 'volinfo_email', 'volinfo_graduate_school', 'volinfo_graduate_date',
                             'volinfo_education', 'volinfo_profession', 'volinfo_employer', 'volinfo_position', 'volinfo_mail_address', 'volinfo_zipcode', 'volinfo_contact_number', 'volinfo_skills'
                             ],
                  'classes': ['collapse']}),
        ('志愿服务信息', {'fields': ['volinfo_service_area',
                               'volinfo_service_date']}),
        ('选择', {'fields': ['volinfo_user']}),
        # ('活动清单', {'fields': ('signup_user_list',)}),
        # ('访问信息', {'fields': readonly_fields})
        # ('访问信息',{'fields': ['user_access_token', 'user_access_time', 'user_refresh_token', 'user_refresh_time']}),
    ]
    list_display = ('volinfo_name', 'volinfo_sex', 'volinfo_cell_number',
                    'volinfo_service_area', 'volinfo_service_date')
    #'volinfo_name''volinfo_cell_number',
    # 遗留问题：只要是非field的都不能在详细中出现


admin.site.register(VolunteerInfo, VolunteerInfoAdmin)


class VolServAdmin(admin.ModelAdmin):
    fieldsets = [
        ('志愿服务信息', {'fields': ['volserv_title', 'volserv_content', 'volserv_client', 'volserv_date', 'volserv_address',
                             'volserv_signup_deadline', 'volserv_contact', 'volserv_counts']}),
        ('报名人选', {'fields': ['signup_user_list']}),
        # ('活动清单', {'fields': ('signup_user_list',)}),
        # ('访问信息', {'fields': readonly_fields})
        # ('访问信息',{'fields': ['user_access_token', 'user_access_time', 'user_refresh_token', 'user_refresh_time']}),
    ]
    list_display = ('volserv_title', 'volserv_client', 'volserv_date',
                    'volserv_address', 'volserv_counts', 'user_list')
    # list_display_links = ('user_list',)


admin.site.register(VolServ, VolServAdmin)


class VolTrainingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('志愿者培训课程信息', {'fields': ['voltraining_zhu_jiang_ren', 'voltraining_theme', 'voltraining_date', 'voltraining_content', 'voltraining_address',
                             'voltraining_counts', 'voltraining_sign_up_deadline']}),
        ('报名人选', {'fields': ['signup_user_list']}),
        # ('活动清单', {'fields': ('signup_user_list',)}),
        # ('访问信息', {'fields': readonly_fields})
        # ('访问信息',{'fields': ['user_access_token', 'user_access_time', 'user_refresh_token', 'user_refresh_time']}),
    ]
    list_display = ('voltraining_theme', 'voltraining_date', 'voltraining_zhu_jiang_ren',
                    'voltraining_sign_up_deadline', 'voltraining_counts', 'user_list')


admin.site.register(VolTraining, VolTrainingAdmin)


class PolicyQAAdmin(admin.ModelAdmin):
    readonly_fields = ('qa_ask_date', 'qa_title',
                       'qa_content', 'qa_answer_date')
    fieldsets = [
        ('问题', {'fields': ['qa_ask_date', 'qa_title', 'qa_content']}),
        ('答复', {'fields': ('qa_answer_date', 'qa_answer',)}),
        # ('访问信息', {'fields': readonly_fields})
        # ('访问信息',{'fields': ['user_access_token', 'user_access_time', 'user_refresh_token', 'user_refresh_time']}),
    ]

    list_display = ('qa_user', 'qa_title', 'qa_content',
                    'qa_answer', 'qa_ask_date', 'qa_answer_date')


admin.site.register(PolicyQA, PolicyQAAdmin)

admin.site.register(SingleUploadImg)
