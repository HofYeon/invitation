from django.db import models
from django.conf import settings

# Create your models here
class Invitation(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_invitations" )
    groom_lastname = models.CharField("신랑 성", max_length=100)
    groom_firstname = models.CharField("신랑 이름", max_length=100)
    bride_lastname = models.CharField("신부 성", max_length=100)
    bride_firstname = models.CharField("신부 이름", max_length=100)
    wedding_datetime = models.DateTimeField("결혼식 날짜")
    weddinghall_name = models.CharField("결혼식장 이름", max_length=100)
    weddinghall_info = models.CharField("웨딩홀 정보", max_length=200)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    update_at = models.DateTimeField("수정일", auto_now = True)

    class Meta:
        db_table = "app_invitation"


# ---------------------------
# 모시는 글 (1:1)
# ---------------------------
class InvitationGreeting(models.Model):
    invitation = models.OneToOneField(
        Invitation,
        on_delete=models.CASCADE,
        related_name="greeting",
    )
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)

    def __str__(self):
        return f"Greeting for Invitation {self.invitation_id}"

    class Meta:
        db_table = "app_invitationgreeting"
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
    father_last_name = models.CharField(max_length=50, blank=True)
    father_first_name = models.CharField(max_length=50, blank=True)
    father_is_baptismal = models.BooleanField(default=False)
    father_baptismal_name = models.CharField(max_length=100, blank=True)
    father_is_renamed = models.BooleanField(default=False)
    father_renamed_name = models.CharField(max_length=100, blank=True)
    father_is_deceased = models.BooleanField(default=False)

    # 어머님 정보
    mother_last_name = models.CharField(max_length=50, blank=True)
    mother_first_name = models.CharField(max_length=50, blank=True)
    mother_is_baptismal = models.BooleanField(default=False)
    mother_baptismal_name = models.CharField(max_length=100, blank=True)
    mother_is_renamed = models.BooleanField(default=False)
    mother_renamed_name = models.CharField(max_length=100, blank=True)
    mother_is_deceased = models.BooleanField(default=False)

    # 자유 입력
    free_input = models.CharField(max_length=200, blank=True) #자유 입력이 있을 시 값 우선 

    order = models.PositiveIntegerField(default=0)     # 출력 순서


    def __str__(self):
        return f"{self.get_side_display()} - {self.invitation.user.last_name}{self.invitation.user.first_name}"

    class Meta:
        db_table = "app_invitationfamily"

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

# ---------------------------
# 갤러리 (1:N)
#   - 사진 1장 = 레코드 1개
#   - (invitation, order) 인덱스 + 유니크로 순서/메인 안정화
# ---------------------------
class InvitationGallery(models.Model):
    invitation = models.ForeignKey(
        Invitation,
        on_delete=models.CASCADE,
        related_name="gallery",
    )
    image = models.ImageField(  # ✅ CharField 대신 ImageField
        upload_to="invitation/gallery/",
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
        return f"{self.invitation_id} - {self.image_path} ({self.order})"
    
    class Meta:
        db_table = "app_invitationgallery"


# ---------------------------
# 지도/주소 (1:1)
#   - 카카오(다음) 주소/우편번호 API 응답 필드에 맞춰 구성
#   - ERD에 보이는 다수의 문자열 필드들을 CharField/BooleanField로 매핑
# ---------------------------
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
    # lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # map_url = models.CharField(max_length=500, blank=True)

    createdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Map for Invitation {self.invitation_id}"
    
    class Meta:
        db_table = "app_invitationmap"