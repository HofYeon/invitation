from django import forms
from .models import Guestbook


class GuestbookForm(forms.ModelForm):
    raw_password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 입력'}),
        strip=False
    )

    class Meta:
        model = Guestbook
        fields = ['author_name', 'content', 'raw_password']

    def save(self, commit=True, invitation=None):
        """
        GuestbookEntry 저장 시 비밀번호를 해시로 변환하고,
        invitation 객체(ForeignKey)를 연결합니다.
        """
        entry: Guestbook = super().save(commit=False)
        if invitation is not None:
            entry.invitation = invitation
        entry.set_password(self.cleaned_data['raw_password'])  # 해시 저장
        if commit:
            entry.save()
        return entry