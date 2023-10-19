from django.core.mail import send_mail
from car_servise.celery import app


@app.task
def send_order_confirmation_email(email, sum_price):
    subject = 'Ваш заказ был принят!'
    message = f'Вы  создали заказ в нашем автосервисе. Его сумма составляет {sum_price}$.'
    mail = 'dima.kulaga5@gmail.com'
    from_email = email

    send_mail(subject, message, mail, [from_email], fail_silently=False)
