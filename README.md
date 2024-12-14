# FlaskBlog | فلَسک‌بلاگ  

**یک پروژه وبلاگ ساده با استفاده از Flask**  
**A simple blog project implemented with Flask.**  

---

## 🎯 درباره پروژه | About the Project  

**FlaskBlog** یک پروژه وبلاگ ساده است که برای نمایش مهارت‌های برنامه‌نویسی و مدیریت پروژه طراحی شده است.  
**FlaskBlog** is a simple blogging project designed to showcase programming and project management skills.  

---

## ✨ ویژگی‌ها | Features  

- **مدیریت کاربران | User Management:** ثبت‌نام، ورود و خروج کاربران.  
  User registration, login, and logout.  

- **پنل مدیریت | Admin Panel:** مدیریت کاربران، دسته‌بندی‌ها و مقالات.  
  Admin panel for managing users, categories, and posts.  

- **مدیریت مقالات | Post Management:** ارسال، ویرایش، تأیید و حذف مقالات.  
  Create, edit, approve, and delete posts.  

- **جستجوی مقالات | Article Search:** جستجو در محتوای مقالات.  
  Search through article content.  

- **پاسخ به پیام‌ها | Respond to Messages:** پاسخ به پیام‌های کاربران از طریق وبسایت.  
  Respond to user inquiries through the website.  

- **دسته‌بندی‌ها | Categories:** مدیریت دسته‌بندی‌ها توسط ادمین.  
  Admin-managed categories.  

- **رابط کاربری ساده | Simple Interface:** طراحی کاربرپسند برای استفاده آسان.  
  User-friendly interface for easy navigation.  

---

## 🛠 پیش‌نیازها | Prerequisites  

برای اجرای این پروژه به موارد زیر نیاز دارید:  
You need the following to run this project:  

- **Python 3.12**  
- **pip** (مدیریت بسته‌های Python | Python package manager)  
- **virtualenv** (توصیه می‌شود | Recommended)  

---

## 🚀 نصب و راه‌اندازی | Installation & Setup  

### 1️⃣ کلون کردن مخزن | Clone the Repository  
```bash  
git clone https://github.com/your-username/FlaskBlog.git  
cd FlaskBlog  
```  

### 2️⃣ ایجاد و فعال‌سازی محیط مجازی | Create and Activate a Virtual Environment  
```bash  
python -m venv venv  
source venv/bin/activate  # Linux/Mac  
venv\Scripts\activate  # Windows  
```  

### 3️⃣ نصب وابستگی‌ها | Install Dependencies  
```bash  
pip install -r requirements.txt  
```  

### 4️⃣ تنظیم فایل محیطی | Configure Environment File  
```bash  
cp .env_file .env  
```  
سپس فایل `.env` را باز کرده و متغیرهای محیطی لازم را تنظیم کنید.  
Then open the `.env` file and set the required environment variables.  

### 5️⃣ اجرای برنامه | Run the Application  
```bash  
python run.py  
```  
برنامه در آدرس `http://localhost:5000` قابل دسترسی خواهد بود.  
The app will be accessible at `http://localhost:5000`.  

---

## 👤 حساب کاربری ادمین | Admin Account  

پس از راه‌اندازی اولیه، یک حساب کاربری ادمین ایجاد می‌شود:  
An admin account will be created after the initial setup:  

- **نام کاربری | Username:** `admin`  
- **رمز عبور | Password:** `admin123`  

لطفاً پس از اولین ورود، رمز عبور را تغییر دهید.  
Please change the password after the first login.  

---

## 💡 نکات | Notes  

- **پایگاه داده | Database:**  
  SQLite3 به صورت پیش‌فرض استفاده می‌شود که برای توسعه مناسب است. برای محیط تولید از دیتابیس‌های قدرتمندتری مانند PostgreSQL استفاده کنید.  
  SQLite3 is used by default for development. For production, use a more robust database like PostgreSQL.  

- **بهینه‌سازی | Optimization:**  
  سیستم‌ها به صورت ساده پیاده‌سازی شده‌اند و ممکن است برای استفاده در مقیاس بزرگ نیاز به بهینه‌سازی داشته باشند.  
  Features are implemented simply and may require optimization for large-scale usage.  

---

## 📄 لایسنس | License  

این پروژه تحت دو لایسنس است:  
This project is dual-licensed under:  

- **بخش بک‌اند | Backend:** [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)  
- **بخش فرانت‌اند (قالب) | Frontend (Template):** [MIT License](https://opensource.org/licenses/MIT)  