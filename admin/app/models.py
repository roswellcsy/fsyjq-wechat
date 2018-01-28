from django.db import models
from django.utils import timezone
import datetime

# Create your models here.


class User(models.Model):
    # 用户信息
    # pass
    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name_plural = '用户信息'
    # 微信可获取的信息
    # 是否关注公众号
    subscribe = models.CharField(max_length=1,default='1')
    # 记录关注者的微信号ID
    openid = models.CharField(max_length=255)
    # 昵称
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    # 姓名
    name = models.CharField(max_length=50, verbose_name='姓名', blank=True, null=True)
    # 手机号
    cellphone = models.CharField(max_length=11, verbose_name='手机号', blank=True, null=True)
    # 性别,值为1时是男性，值为2时是女性，值为0时是未知
    SEX = (
        ('1', '男'),
        ('2', '女'),
    )
    user_sex = models.CharField(max_length=1, choices=SEX, verbose_name='性别')
    # 城市
    user_city = models.CharField(max_length=10, blank=True, verbose_name='城市', null=True)
    # 国家
    user_country = models.CharField(
        max_length=10, blank=True, verbose_name='国家', null=True)
    # 省份
    user_province = models.CharField(
        max_length=10, blank=True, verbose_name='省份', null=True)
    # 语言，简体中文为zh_CN
    user_language = models.CharField(
        max_length=10, default='zh_CN', verbose_name='语言')
    # 关注时间
    user_subscribe_time = models.CharField(max_length=10, null=True, blank=True, verbose_name='关注公众号时间')
    # 网页访问access_token
    user_access_token = models.CharField(max_length=255)
    # access_token过期时间
    user_access_time = models.CharField(max_length=10, blank=True, null=True)
    # 网页访问refresh_token
    user_refresh_token = models.CharField(max_length=255)
    # refresh_token过期时间
    user_refresh_time = models.CharField(max_length=10, blank=True, null=True)
    # 是否志愿者
    user_volunteer_or_not = models.BooleanField(
        default=False, verbose_name='是否志愿者')

    def is_volunteer(self):
        if self.user_volunteer_or_not == False:
            return '否'
        elif self.user_volunteer_or_not == True:
            return '是'
    is_volunteer.short_description = '是否志愿者'
    # 公益活动报名
    # charity_campaign_list = models.ManyToManyField(CharityCampaign, blank=True, verbose_name='活动报名')

    # def signup_campaign(self):
    #     return ','.join([i.campaign_name for i in self.charitycampaign_set.all()])
    # signup_campaign.short_description = '报名活动清单'

# 单个图片上传


class SingleUploadImg(models.Model):
    def __str__(self):
        return self.photo_name

    class Meta:
        verbose_name_plural = '单图片上传'
    campaign_or_service_name = models.CharField(
        max_length=50, verbose_name='活动名称')
    photo_name = models.CharField(max_length=10, verbose_name='照片名字')
    photo = models.ImageField('图片', upload_to='media')


class CharityCampaign(models.Model):
    # 公益活动
    # pass
    def __str__(self):
        return self.campaign_name

    class Meta:
        verbose_name_plural = '公益活动发布列表'
    # 活动名称
    campaign_name = models.CharField(max_length=50, verbose_name='活动名称')
    # 活动分类,青少儿服务、青年服务、中年服务、长者服务、订餐服务、家政服务、公益服务、公共服务
    TYPE = (
        ('1', '青少儿服务'),
        ('2', '青年服务'),
        ('3', '中年服务'),
        ('4', '长者服务'),
        ('5', '订餐服务'),
        ('6', '家政服务'),
        ('7', '公益服务'),
        ('8', '公共服务'),
        ('9', '志愿者服务'),
    )
    campaign_type = models.CharField(
        max_length=50, choices=TYPE, verbose_name='活动分类')
    # 活动时间
    campaign_date = models.DateTimeField('活动时间')
    # 服务对象
    campaign_client = models.CharField(max_length=50, verbose_name='服务对象')
    # 活动地点
    campaign_address = models.CharField(max_length=50, verbose_name='活动地点')
    # 活动内容
    campaign_content = models.CharField(max_length=255, verbose_name='活动内容')
    # 服务费用
    campaign_paid = models.CharField(max_length=50, verbose_name='服务费用')
    # 活动图片
    photos = models.ManyToManyField(
        SingleUploadImg, blank=True, verbose_name='活动图片')
    # 报名截止日期
    campaign_signup_deadline = models.DateTimeField('报名截止时间')
    # 联系方式
    campaign_contact = models.CharField(max_length=50, verbose_name='活动联系方式')
    # 可报名人数
    campaign_counts = models.PositiveSmallIntegerField(verbose_name='可报名总人数')
    # 报名人员
    signup_user_list = models.ManyToManyField(
        User, blank=True, verbose_name='报名人员名单')

    def user_list(self):
        return ','.join(['姓名:' + i.name + ',联系方式:' + i.cellphone for i in self.signup_user_list.all()])
    user_list.short_description = '报名人员名单'
    # campaign_members = models.ManyToManyField(
    #     User,
    #     through='CharityCampaignSignUp',
    #     through_fields=('CharityCampaign','User'),
    # )
    # 需要加上上传图片，多图片前端使用vux的swiper自动轮播，参考祖庙微服务

# class CharityCampaignSignUp(models.Model):
#     # 公益活动报名
#     class Meta:
#         verbose_name_plural = '公益活动报名清单'
#     # 活动信息
#     CharityCampaignSignUp = models.ForeignKey(CharityCampaign)
#     # 报名人员
#     User = models.ForeignKey(User)
#     # 报名
#     signup = models.ForeignKey(
#         User,
#         related_name='charitycampaign_signup',
#     )


class ProServ(models.Model):
    # 专业服务信息/个案
    class Meta:
        verbose_name_plural = '专业服务登记列表'
    # pass
    # 关联微信用户
    proserv_user = models.ForeignKey(User, verbose_name='微信用户')

    def __str__(self):
        return self.sw_name + self.case_id
    # 初始信息
    proserv_question_title = models.CharField(
        max_length=255, verbose_name='咨询问题')

    proserv_question_content = models.CharField(
        max_length=255, verbose_name='咨询内容')
    # 个案服务登记表内容
    # 服务中心信息
    # 社工姓名
    sw_name = models.CharField(max_length=50, verbose_name='社工姓名')
    # 个案编号
    case_id = models.CharField(max_length=50, verbose_name='个案编号')
    # 咨询日期
    counseling_date = models.DateField('咨询日期')
    # 咨询对象信息
    # (1)姓名
    proserv_name = models.CharField(
        max_length=20, verbose_name='姓名')
    # def proserv_name(self):
    #     return self.proserv_user.name
    # proserv_name.short_description = '姓名'
    # (2)性别
    SEX = (
        ('1', '男'),
        ('2', '女'),
    )
    proserv_sex = models.CharField(
        max_length=1, choices=SEX, verbose_name='性别')
    # def proserv_sex(self):
    #     if self.proserv_user.user_sex == '1':
    #         return '男'
    #     elif self.proserv_user.user_sex == '2':
    #         return '女'
    # proserv_sex.short_description='性别'
    # (3)年龄
    proserv_age = models.CharField(
        max_length=20, blank=True, verbose_name='年龄')
    # (4)籍贯
    proserv_jiguan = models.CharField(
        max_length=50, blank=True, verbose_name='籍贯')
    # (5)户籍所在地
    proserv_house_hold = models.CharField(
        max_length=50, blank=True, verbose_name='户籍所在地')
    # (6)身份证明
    proserv_id_num = models.CharField(
        max_length=50, blank=True, verbose_name='身份证明')
    # (7)民族
    proserv_ethnic = models.CharField(
        max_length=50, blank=True, verbose_name='民族')
    # (8)政治面貌
    proserv_political_status = models.CharField(
        max_length=50, blank=True, verbose_name='政治面貌')
    # (9)宗教
    proserv_religion = models.CharField(
        max_length=50, blank=True, verbose_name='宗教')
    # (10)职业
    proserv_occupation = models.CharField(
        max_length=50, blank=True, verbose_name='职业')
    # (11)就读年级
    proserv_studying_grade = models.CharField(
        max_length=50, blank=True, verbose_name='就读年级')
    # (12)文化程度
    proserv_degree_of_education = models.CharField(
        max_length=50, blank=True, verbose_name='文化程度')
    # (13)所在社区
    proserv_community = models.CharField(
        max_length=50, blank=True, verbose_name='所在社区')
    # (14)联系方式
    proserv_contact = models.CharField(
        max_length=50, blank=True, verbose_name='联系方式')
    # def proserv_contact(self):
    #     return self.proserv_user.cellphone
    # proserv_contact.short_description = '联系方式'
    # (15)家庭住址
    proserv_live_address = models.CharField(
        max_length=50, blank=True, verbose_name='家庭住址')
    # (16)婚姻状况
    marriage_status = (
        ('1', '单身'),
        ('2', '同居'),
        ('3', '已婚'),
        ('4', '分居'),
        ('5', '离婚'),
        ('6', '丧偶'),
        ('7', '其它'),
    )
    proserv_married = models.CharField(
        max_length=1, choices=marriage_status, blank=True, verbose_name='婚姻状况')
    # (17)咨询问题(选项)
    question_type = (
        ('1', '亲子关系问题'),
        ('2', '婚姻问题'),
        ('3', '家庭纠纷'),
        ('4', '经济问题'),
        ('5', '职业问题'),
        ('6', '住屋问题'),
        ('7', '家庭暴力致伤/死(受害对象: 子女 / 配偶 / 老人 / 其它______)'),
        ('8', '个人精神/情绪问题'),
        ('9', '个人行为问题(吸毒/酒/赌博)'),
        ('10', '恋爱/交友问题'),
        ('11', '患病/复康问题(病类)'),
        ('12', '未婚怀孕'),
        ('13', '收养'),
        ('14', '其它'),
    )
    proserv_counseling = models.CharField(
        max_length=50, choices=question_type, blank=True, verbose_name='咨询问题类型')
    assistance_type = (
        ('1', '医疗救助'),
        ('2', '教育救助'),
        ('3', '住房救助'),
        ('4', '临时救助'),
        ('5', '最低生活保障救助'),
        ('6', '其它'),
    )
    social_assistance = models.CharField(
        max_length=1, choices=assistance_type, blank=True, verbose_name='社会救助')
    COUNSELING_RESULTS = (
        ('1', '问题改善/解决结案'),
        ('2', '转为辅导个案'),
        ('3', '转介'),
    )
    counseling_results = models.CharField(
        max_length=1, choices=COUNSELING_RESULTS, blank=True, verbose_name='咨询结果')


class VolunteerInfo(models.Model):
    class Meta:
        verbose_name_plural = '志愿者信息'

    def __str__(self):
        return self.volinfo_user.name
    # 志愿者信息
    volinfo_user = models.ForeignKey(User, verbose_name='微信用户')
    #(1)姓名
    volinfo_name = models.CharField(max_length=20, verbose_name='姓名')
    # def volinfo_name(self):
    #     return self.volinfo_user.name
    # volinfo_name.short_description = '姓名'
    #(2)性别 值为1时是男性，值为2时是女性，值为0时是未知
    SEX = (
        ('1', '男'),
        ('2', '女'),
    )
    volinfo_sex = models.CharField(
        max_length=1, choices=SEX, verbose_name='性别')

    # def volinfo_sex(self):
    #     if self.volinfo_user.user_sex == '1':
    #         return '男'
    #     elif self.volinfo_user.user_sex == '2':
    #         return '女'
    # volinfo_sex.short_description = '性别'
    volinfo_age = models.CharField(
        max_length=2, blank=True, verbose_name='年龄')

    #(3)籍贯
    volinfo_jiguan = models.CharField(
        max_length=100, blank=True, verbose_name='籍贯')
    #(4)住址
    volinfo_live_address = models.CharField(
        max_length=100, blank=True, verbose_name='住址')
    #(5)婚姻状况(已婚未婚)
    marriage_status = (
        ('1', '单身'),
        ('2', '同居'),
        ('3', '已婚'),
        ('4', '分居'),
        ('5', '离婚'),
        ('6', '丧偶'),
        ('7', '其它'),
    )
    volinfo_married = models.CharField(
        max_length=1, choices=marriage_status, blank=True, verbose_name='婚姻状况')
    #(6)证件类型(身份证、护照、警官证、军官证)
    id_card_type = (
        ('1', '身份证'),
        ('2', '护照'),
        ('3', '警官证'),
        ('4', '军官证'),
    )
    volinfo_idcard_type = models.CharField(
        max_length=10, choices=id_card_type, default='1', blank=True, verbose_name='证件类型')
    #(7)证件号码
    volinfo_id_num = models.CharField(
        max_length=18, blank=True, verbose_name='证件号码')
    #(8)出生日期(年月日)
    volinfo_birthday = models.DateField(
        blank=True, null=True, verbose_name='出生日期')
    #(9)Email
    volinfo_email = models.CharField(
        max_length=50, blank=True, verbose_name='电子邮箱')
    #(10)毕业院校
    volinfo_graduate_school = models.CharField(
        max_length=50, blank=True, verbose_name='毕业院校')
    #(11)毕业时间
    volinfo_graduate_date = models.DateField(
        blank=True, null=True, verbose_name='毕业时间')
    #(12)学历
    volinfo_education = models.CharField(
        max_length=5, blank=True, verbose_name='学历')
    #(13)专业
    volinfo_profession = models.CharField(
        max_length=50, blank=True, verbose_name='专业')
    #(14)工作单位
    volinfo_employer = models.CharField(
        max_length=50, blank=True, verbose_name='工作单位')
    #(15)职务
    volinfo_position = models.CharField(
        max_length=50, blank=True, verbose_name='职务')
    #(16)通讯地址
    volinfo_mail_address = models.CharField(
        max_length=50, blank=True, verbose_name='通讯地址')
    #(17)邮编
    volinfo_zipcode = models.CharField(
        max_length=10, blank=True, verbose_name='邮编')
    #(18)联系电话
    volinfo_contact_number = models.CharField(
        max_length=50, blank=True, verbose_name='固定电话')
    #(19)移动电话
    volinfo_cell_number = models.CharField(max_length=11, verbose_name='移动电话')
    # def volinfo_cell_number(self):
    #     return self.volinfo_user.cellphone
    # volinfo_cell_number.short_description = '移动电话'
    #(20)志愿服务区(禅城 - 社区)
    volinfo_service_area = models.CharField(
        max_length=50, blank=True, verbose_name='志愿服务区')
    #(21)志愿服务时间(法定休息日、工作日、不限)
    service_date_options = (
        ('1', '法定休息日'),
        ('2', '工作日'),
        ('3', '不限'),
    )
    volinfo_service_date = models.CharField(
        max_length=50, choices=service_date_options, verbose_name='志愿服务时间')
    #(22)技能
    volinfo_skills = models.CharField(
        max_length=50, blank=True, verbose_name='技能')


class VolServ(models.Model):
    # 志愿服务信息
    class Meta:
        verbose_name_plural = '志愿者服务清单'
    # 志愿服务
    # pass
    # 服务主题
    volserv_title = models.CharField(max_length=100, verbose_name='服务主题')
    # 服务内容
    volserv_content = models.CharField(max_length=200, verbose_name='服务内容')
    # 服务对象
    volserv_client = models.CharField(max_length=100, verbose_name='服务对象')
    # 服务时间
    volserv_date = models.DateTimeField('服务时间')
    # 服务地址
    volserv_address = models.CharField(max_length=100, verbose_name='服务地址')
    # 服务报名截止时间
    volserv_signup_deadline = models.DateField('服务报名截止时间')
    # 联系方式
    volserv_contact = models.CharField(max_length=100, verbose_name='服务联系方式')
    # 可报名人数
    volserv_counts = models.PositiveSmallIntegerField(verbose_name='可报名人数')
    # 报名人员
    signup_user_list = models.ManyToManyField(
        VolunteerInfo, blank=True, verbose_name='报名志愿者名单')

    def user_list(self):
        return ','.join(['姓名:' + i.volinfo_name + ',联系方式:' + i.volinfo_cell_number for i in self.signup_user_list.all()])
    user_list.short_description = '报名志愿者名单'


class VolTraining(models.Model):
    # 志愿者培训课程信息
    class Meta:
        verbose_name_plural = '志愿者培训清单'
    # 志愿者培训
    # 主讲人
    voltraining_zhu_jiang_ren = models.CharField(
        max_length=50, verbose_name='主讲人')
    # 培训主题
    voltraining_theme = models.CharField(max_length=100, verbose_name='培训主题')
    # 培训时间
    voltraining_date = models.DateTimeField('培训时间')
    # 培训内容
    voltraining_content = models.CharField(max_length=100, verbose_name='培训内容')
    # 培训地址
    voltraining_address = models.CharField(max_length=100, verbose_name='培训地址')
    # 可报名人数
    voltraining_counts = models.PositiveSmallIntegerField(verbose_name='可报名人数')
    # 培训报名截止日期
    voltraining_sign_up_deadline = models.DateField('服务报名截止时间')
    # pass
    # 报名人员
    signup_user_list = models.ManyToManyField(
        VolunteerInfo, blank=True, verbose_name='报名志愿者名单')

    def user_list(self):
        return ','.join(['姓名:' + i.volinfo_name + ',联系方式:' + i.volinfo_cell_number for i in self.signup_user_list.all()])
    user_list.short_description = '报名志愿者名单'


class PolicyQA(models.Model):
    class Meta:
        verbose_name_plural = '政策问答'
    qa_title = models.CharField(max_length=255, verbose_name='标题')
    qa_content = models.CharField(max_length=255, verbose_name='内容')
    qa_answer = models.CharField(max_length=255, verbose_name='回答')
    qa_ask_date = models.DateTimeField(
        verbose_name='提问时间', null=True, blank=True)
    qa_answer_date = models.DateTimeField(
        verbose_name='提问时间', null=True, blank=True)
    qa_user = models.ForeignKey(User, verbose_name='微信用户', blank=True)
    # def user(self):


# 微信API相关
class AccessToken(models.Model):
    class Meta:
        verbose_name_plural = '核心token'
    access_token = models.CharField(max_length=255)
    expire_in = models.IntegerField()
