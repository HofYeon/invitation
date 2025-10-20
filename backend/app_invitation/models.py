import uuid, os

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password, check_password

# Create your models here

def invitation_image_upload_to(instance, filename):
    """
    모든 이미지(main, middle, end)를 같은 main 폴더에 저장.
    경로 예시:
    invitation/<username>/<invitation_id>/main/<uuid>.jpg
    """
    base, ext = os.path.splitext(filename)
    username = slugify(getattr(instance.user, "username", "anon"))
    invitation_id = instance.pk or "temp"  # 아직 저장 안 된 객체는 temp로

    return f"invitation/{username}/{invitation_id}/main/{uuid.uuid4().hex}{ext.lower()}"



class Invitation(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_invitations" )
    invitationname = models.CharField("초대장 이름", max_length=150, unique=True)
    groom_lastname = models.CharField("신랑 성", max_length=100)
    groom_firstname = models.CharField("신랑 이름", max_length=100)
    groom_bankname = models.CharField("은행명", max_length=50, blank=True)
    groom_account = models.CharField("계좌번호", max_length=100, blank=True)
    groom_phone = models.CharField("휴대폰 번호", max_length=20, blank=True)
    bride_lastname = models.CharField("신부 성", max_length=100)
    bride_firstname = models.CharField("신부 이름", max_length=100)
    bride_bankname = models.CharField("은행명", max_length=50, blank=True)
    bride_account = models.CharField("계좌번호", max_length=100, blank=True)
    bride_phone = models.CharField("휴대폰 번호", max_length=20, blank=True)
    wedding_datetime = models.DateTimeField("결혼식 날짜")
    weddinghall_name = models.CharField("결혼식장 이름", max_length=100)
    weddinghall_info = models.CharField("웨딩홀 정보", max_length=200)
    # ✅ 이미지 3개 (모두 main 폴더에 저장)
    main_img = models.ImageField("메인 이미지", upload_to=invitation_image_upload_to, blank=True, null=True)
    middle_img = models.ImageField("중간 이미지", upload_to=invitation_image_upload_to, blank=True, null=True)
    end_img = models.ImageField("엔드 이미지", upload_to=invitation_image_upload_to, blank=True, null=True)

    created_at = models.DateTimeField("생성일", auto_now_add=True)
    update_at = models.DateTimeField("수정일", auto_now = True)


    class Meta:
        db_table = "app_invitation"
        verbose_name = "청첩장 기본 정보"
        verbose_name_plural = "청첩장 기본 정보"

    def __str__(self):
        return f"{self.groom_lastname}{self.groom_firstname} ♥ {self.bride_lastname}{self.bride_firstname}"


# ---------------------------
# 모시는 글 (1:1)
# ---------------------------

def greeting_image_upload_to(instance, filename):
    """
    모든 이미지(main, middle, end)를 같은 main 폴더에 저장.
    경로 예시:
    invitation/<username>/<invitation_id>/main/<uuid>.jpg
    """
    base, ext = os.path.splitext(filename)
    username = slugify(getattr(instance.invitation.user, "username", "anon"))
    invitation_id = instance.invitation.pk or "temp"  # 아직 저장 안 된 객체는 temp로

    return f"invitation/{username}/{invitation_id}/greeting/{uuid.uuid4().hex}{ext.lower()}"

class InvitationGreeting(models.Model):
    invitation = models.OneToOneField(
        Invitation,
        on_delete=models.CASCADE,
        related_name="greeting",
    )
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    greeting_img = models.ImageField("인사말 이미지", upload_to=greeting_image_upload_to, blank=True, null=True)

    def __str__(self):
        return f"Greeting for Invitation {self.invitation_id}"

    class Meta:
        db_table = "app_invitationgreeting"
        verbose_name = "인사말"
        verbose_name_plural = "인사말"
# ---------------------------
# 가족 소개 (1:N)
#   - ERD의 choice(신랑/신부, 아버님/어머님)를 SmallInteger로 반영
#   - 개명 여부/고인 여부/세례명 등 포함
# ---------------------------
class InvitationFamily(models.Model):
    class Side(models.IntegerChoices):
        GROOM = 1, "신랑측"
        BRIDE = 2, "신부측"

    invitation = models.ForeignKey(
        Invitation,
        on_delete=models.CASCADE,
        related_name="families",
    )

    side = models.SmallIntegerField(choices=Side.choices, unique=False)  # 신랑/신부측 구분

    # 아버님 정보
    father_last_name = models.CharField("아버님  성",max_length=50, blank=True)
    father_first_name = models.CharField("이름",max_length=50, blank=True)
    father_is_baptismal = models.BooleanField("세례 여부",default=False)
    father_baptismal_name = models.CharField("세례명",max_length=100, blank=True)
    father_is_renamed = models.BooleanField("개명 여부",default=False)
    father_renamed_name = models.CharField("개명",max_length=100, blank=True)
    father_is_deceased = models.BooleanField("고인 여부",default=False)
    father_bankname = models.CharField("은행명", max_length=50, blank=True)
    father_account = models.CharField("계좌번호", max_length=100, blank=True)
    father_phone = models.CharField("휴대폰 번호", max_length=20, blank=True)

    # 어머님 정보
    mother_last_name = models.CharField("어머님 성",max_length=50, blank=True)
    mother_first_name = models.CharField("이름",max_length=50, blank=True)
    mother_is_baptismal = models.BooleanField("세례 여부",default=False)
    mother_baptismal_name = models.CharField("세례 명",max_length=100, blank=True)
    mother_is_renamed = models.BooleanField("개명 여부",default=False)
    mother_renamed_name = models.CharField("개명",max_length=100, blank=True)
    mother_is_deceased = models.BooleanField("고인 여부",default=False)
    mother_bankname = models.CharField("은행명", max_length=50, blank=True)
    mother_account = models.CharField("계좌번호", max_length=100, blank=True)
    mother_phone = models.CharField("휴대폰 번호", max_length=20, blank=True)

    # 자유 입력
    free_input = models.CharField("자유 입력",max_length=200, blank=True) #자유 입력이 있을 시 값 우선

    order = models.PositiveIntegerField(default=0)     # 출력 순서


    def __str__(self):
        return f"{self.get_side_display()} - {self.invitation.user.last_name}{self.invitation.user.first_name}"

    class Meta:
        db_table = "app_invitationfamily"
        verbose_name = "혼주 정보"
        verbose_name_plural = "혼주 정보"

# ---------------------------
# 캘린더 (필요 시 확장; ERD에 맞춰 초대장 FK만)
# ---------------------------
class InvitationCalendar(models.Model):
    invitation = models.OneToOneField(
        Invitation,
        on_delete=models.CASCADE,
        related_name="calendar",
    )
    # 추후 iCal/외부 캘린더 연동 필드가 생기면 추가
    def __str__(self):
        return f"Calendar for Invitation {self.invitation_id}"

    class Meta:
        db_table = "app_invitationcalendar"
        verbose_name = "캘린더 - 건드릴 필요 없음"
        verbose_name_plural = "캘린더 - 건드릴 필요 없음"

# ---------------------------
# 갤러리 (1:N)
#   - 사진 1장 = 레코드 1개
#   - (invitation, order) 인덱스 + 유니크로 순서/메인 안정화
# ---------------------------

def gallery_upload_to(instance, filename):
    """
    초대(invitation)와 연결된 사용자별로 갤러리 이미지를 저장하는 경로를 동적으로 반환.
    결과 예시:
    media/invitation/<username>/<invitation_id>/gallery/<uuid>.jpg
    """
    base, ext = os.path.splitext(filename)
    invitation = getattr(instance, "invitation", None)

    # 사용자 이름 (slugify로 안전하게)
    user_slug = "anonymous"
    invitation_id = "temp"

    if invitation:
        if getattr(invitation, "user", None):
            username = getattr(invitation.user, "username", None) or str(invitation.user_id or "")
            user_slug = slugify(username) or str(invitation.user_id)
        invitation_id = str(invitation.pk or "temp")

    return f"invitation/{user_slug}/{invitation_id}/gallery/{uuid.uuid4().hex}{ext.lower()}"

class InvitationGallery(models.Model):
    invitation = models.ForeignKey(
        Invitation,
        on_delete=models.CASCADE,
        related_name="gallery",
    )
    image = models.ImageField(  # ✅ CharField 대신 ImageField
        upload_to=gallery_upload_to,
        blank=True,
        null=True,
        verbose_name="갤러리 이미지"
    )
    order = models.PositiveIntegerField(default=0)     # 가장 작은 값 = 메인
    createdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["invitation", "order"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["invitation", "order"],
                name="uniq_invitation_order",
            ),
            models.CheckConstraint(
                check=models.Q(order__gte=0),
                name="ck_gallery_order_non_negative",
            ),
        ]
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.invitation_id} - {self.image} ({self.order})"
    
    class Meta:
        db_table = "app_invitationgallery"
        verbose_name = "갤러리 사진 업로드"
        verbose_name_plural = "갤러리 사진 업로드"


# ---------------------------
# 지도/주소 (1:1)
#   - 카카오(다음) 주소/우편번호 API 응답 필드에 맞춰 구성
#   - ERD에 보이는 다수의 문자열 필드들을 CharField/BooleanField로 매핑
# ---------------------------

def map_image_upload_to(instance, filename):
    """
    모든 이미지(main, middle, end)를 같은 main 폴더에 저장.
    경로 예시:
    invitation/<username>/<invitation_id>/main/<uuid>.jpg
    """
    base, ext = os.path.splitext(filename)
    username = slugify(getattr(instance.invitation.user, "username", "anon"))
    invitation_id = instance.invitation.pk or "temp"  # 아직 저장 안 된 객체는 temp로

    return f"invitation/{username}/{invitation_id}/map/{uuid.uuid4().hex}{ext.lower()}"

class InvitationMap(models.Model):
    invitation = models.OneToOneField(
        Invitation,
        on_delete=models.CASCADE,
        related_name="map",
    ) 

    # 기본
    zonecode = models.CharField("우편번호", max_length=20, blank=True)
    address = models.CharField("지번/도로명 통합 주소", max_length=300, blank=True)
    e_address = models.CharField("영문 지번/도로명 통합 주소", max_length=300, blank=True)
    address_type = models.CharField("주소 타입", max_length=20, blank=True)
    bcode = models.CharField("법정동 코드", max_length=20, blank=True)

    # 동/법정동명
    bname = models.CharField("법정동/법정리", max_length=100, blank=True)
    bname1 = models.CharField("읍,면동 이름", max_length=100, blank=True)
    bname2 = models.CharField("법정동,리 이름", max_length=100, blank=True)

    e_bname = models.CharField("영문 법정동/법정리", max_length=100, blank=True)
    e_bname1 = models.CharField("영문 읍,면동 이름", max_length=100, blank=True)
    e_bname2 = models.CharField("영문 법정동,리 이름", max_length=100, blank=True)

    # 건물
    building_code = models.CharField("건물 코드", max_length=50, blank=True)
    building_name = models.CharField("건물명", max_length=200, blank=True)
    #apartment = models.CharField("공동주택 여부", max_length=10, blank=True)  # 'Y'/'N' 등 문자열 응답

    # 시/도/시군구/법정리
    sido = models.CharField("시도", max_length=50, blank=True)
    sigungu = models.CharField("시군구", max_length=50, blank=True)
    sigungu_code = models.CharField("시군구 코드", max_length=20, blank=True)

    e_sido = models.CharField(" 영문 시도", max_length=50, blank=True)
    e_sigungu = models.CharField("영문 시군구", max_length=50, blank=True)

    # 도로명
    roadname = models.CharField("도로명", max_length=200, blank=True)
    roadname_code = models.CharField("도로명 코드", max_length=50, blank=True)
    roadaddress = models.CharField("도로명 주소", max_length=300, blank=True)
    e_roadaddress = models.CharField("영문 도로명 주소", max_length=300, blank=True)
    
    #지번 주소
    jibunadress = models.CharField("지번 주소", max_length=300, blank=True)
    e_jibunadress = models.CharField(" 영문 지번 주소", max_length=300, blank=True)

    # 상세주소(사용자 입력)
    detail_address = models.CharField("상세 주소", max_length=200, blank=True)

    # 좌표(지오코딩 별도 시 채움)
    lat = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    lng = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    # map_url = models.CharField(max_length=500, blank=True)
    map_img = models.ImageField("약도 이미지", upload_to=map_image_upload_to, blank=True, null=True)

    createdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Map for Invitation {self.invitation_id}"
    
    class Meta:
        db_table = "app_invitationmap"
        verbose_name = "위치"
        verbose_name_plural = "위치"



#방명록 모델
class Guestbook(models.Model):
    invitation = models.ForeignKey(
        Invitation,
        related_name='guestbook_entries',
        on_delete=models.CASCADE
    )
    author_name = models.CharField('작성자', max_length=50)
    password = models.CharField('비밀번호(해시)', max_length=128)  # 평문 저장 금지!
    content = models.TextField('내용')  # 이모지 포함 텍스트
    created_at = models.DateTimeField('작성일시', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def set_password(self, raw_password: str):
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.author_name} - {self.created_at:%Y-%m-%d %H:%M}"

    class Meta:
        db_table = "app_guestbook"
        verbose_name = "방명록 - 건드릴 필요 없음"
        verbose_name_plural = "방멱록 - 건드릴 필요 없음"


#신랑, 신부측 계좌

