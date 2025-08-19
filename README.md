# Experiment05-Docker

## بررسی داکرفایل پروژه backend

داکرفایل نوشته شده برای پروژه backend به صورت زیر است:

```dockerfile
FROM docker.arvancloud.ir/python:3.13

WORKDIR /app

COPY . .

RUN python -m pip install -i https://mirror-pypi.runflare.com/simple --upgrade pip

RUN pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

توضیح داکرفایل:

این داکرفایل برای ساخت یک تصویر داکر برای پروژه Django استفاده می‌شود. در اینجا مراحل مختلفی که در داکرفایل انجام می‌شود توضیح داده شده است:

1. **انتخاب تصویر پایه**: در خط اول، یک تصویر پایه از Python 3.13 انتخاب می‌شود که از مخزن ArvanCloud بارگیری می‌شود.

2. **تنظیم دایرکتوری کاری**: با استفاده از دستور `WORKDIR /app`، دایرکتوری کاری به `/app` تغییر می‌کند. این بدان معناست که تمام دستورات بعدی در این دایرکتوری اجرا خواهند شد.

3. **کپی فایل‌ها**: با استفاده از دستور `COPY . .`، تمام فایل‌های موجود در دایرکتوری فعلی به دایرکتوری کاری در تصویر داکر کپی می‌شوند.

4. **نصب pip**: در این مرحله، pip به‌روز می‌شود تا از آخرین نسخه آن استفاده شود.

5. **نصب وابستگی‌ها**: با استفاده از دستور `RUN pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt`، تمام وابستگی‌های پروژه که در فایل `requirements.txt` مشخص شده‌اند، نصب می‌شوند.

6. **باز کردن پورت**: با استفاده از دستور `EXPOSE 8000`، پورت 8000 برای دسترسی به برنامه در حال اجرا باز می‌شود.

7. **اجرای سرور**: در نهایت، با استفاده از دستور `CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]`، سرور Django در آدرس `0.0.0.0:8000` راه‌اندازی می‌شود.

## پیاده‌سازی load balancer

چون در ادامه نیاز داریم تا چند اینستنس از اپلیکیشن Django را مدیریت کنیم، از Nginx به عنوان لود بالانسر استفاده می‌کنیم. برای این کار، باید Nginx را پیکربندی کنیم.

در فولدر `nginx` یک فایل جدید به نام `nginx.conf` ایجاد کردیم و تنظیمات زیر را در آن قرار دادیم:

```nginx
events {}

http {
    upstream backend_pool {

        server backend1:8000 max_fails=3 fail_timeout=30s weight=1;
        server backend2:8000 max_fails=3 fail_timeout=30s weight=1;
        server backend3:8000 max_fails=3 fail_timeout=30s weight=1;

    }

    server {
        listen 80;

        location / {
            proxy_pass http://backend_pool;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $server_name;

        }
    }
}
```

توضیح:

1. **events {}**

   - بخش مربوط به تنظیمات رویدادها و کار با کانکشن‌ها. در اینجا خالی است و از تنظیمات پیش‌فرض استفاده می‌کند.

2. **http { … }**

   - بخش اصلی برای تنظیمات HTTP در NGINX. شامل تعریف upstream و server.

3. **upstream backend_pool { … }**

   - تعریف یک **گروه سرور** (Load Balancing Pool) به نام `backend_pool`.
   - سه سرور backend اضافه شده‌اند: `backend1`, `backend2`, `backend3` هر کدام روی پورت ۸۰۰۰.
   - `max_fails=3 fail_timeout=30s`: اگر یک سرور سه بار متوالی fail کند، به مدت ۳۰ ثانیه از دسترس خارج در نظر گرفته می‌شود.
   - `weight=1`: وزن سرور برای Load Balancing (در اینجا همه مساوی هستند).

4. **server { … }**

   - تعریف یک Virtual Host که به پورت ۸۰ گوش می‌دهد.

5. **location / { … }**

   - درخواست‌های مسیر `/` به `backend_pool` هدایت می‌شوند.
   - `proxy_pass http://backend_pool;`: درخواست‌ها به سرورهای backend ارسال می‌شوند.
   - `proxy_set_header …`: اضافه کردن هدرهایی به درخواست‌های پراکسی برای حفظ اطلاعات اصلی کلاینت و دامنه.

     - `Host`: نام میزبان اصلی
     - `X-Real-IP`: آی‌پی واقعی کلاینت
     - `X-Forwarded-For`: لیست آی‌پی‌های پراکسی شده
     - `X-Forwarded-Proto`: پروتکل اصلی (http/https)
     - `X-Forwarded-Host`: نام سرور NGINX
