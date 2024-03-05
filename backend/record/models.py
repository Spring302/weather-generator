from django.db import models
from django.utils import timezone
from datetime import date

from enum import Enum

class TagChoices(Enum):
    IN = 'IN'
    OUT = 'OUT'

class User(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)    

class DailyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=date.today)
    go_time = models.DateTimeField(default=timezone.now)
    leave_time = models.DateTimeField(null=True, default=None)  # Manually define default value
    working_time = models.IntegerField(default=0)
    break_time = models.IntegerField(default=0)

class LoginAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    tag = models.CharField(max_length=10, choices=[(tag.value, tag.name) for tag in TagChoices], default=TagChoices.IN.value)
    check_time = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # 태그가 OUT일 경우 처리
        if self.tag == TagChoices.OUT.value:
            last_login_in = LoginAccess.objects.filter(user=self.user, tag=TagChoices.IN.value).order_by('-check_time').first()
            # 오늘 출근한 적이 있으면 출석기록을 가져와서 leave_time, working_time 계산 후 저장한다.
            if last_login_in:
                last_daily_record = DailyRecord.objects.filter(user=self.user, date=last_login_in.check_time.date()).first()
                if last_daily_record:
                    last_daily_record.leave_time = self.check_time
                    last_daily_record.save()
                    last_daily_record.working_time = (last_daily_record.leave_time - last_daily_record.go_time).seconds // 3600
                    last_daily_record.save()
                else:
                    # Handle case if no previous DailyRecord is found
                    pass
            else:
                # Handle case if no previous LoginAccess with tag IN is found
                pass
        super(LoginAccess, self).save(*args, **kwargs)