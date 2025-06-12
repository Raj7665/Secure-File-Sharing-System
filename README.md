# Secure File Sharing System using Flask

A web application built with Flask for secure file sharing, allowing users to upload, download, and share files with authentication and access control. This project aims to provide a basic yet functional platform for managing digital assets securely.

---

## ✨ Features

* **User Authentication & Authorization**: Secure user registration, login, and access control powered by Flask-Login and Werkzeug for password hashing.
* **File Upload**: Users can securely upload files to the server.
* **File Download**: Users can download their own files or files shared with them.
* **File Sharing**: Share files with specific registered users.
* **Public Share Links (Optional)**: Generate unique, publicly accessible links for files (use with caution).
* **Database Integration**: Stores user and file metadata using SQLite (can be easily migrated to PostgreSQL/MySQL).
* **Flash Messages**: Provides user feedback for actions like login, upload, and sharing.

---

## 🛠️ Technologies Used

* **Backend Framework**: **Flask** (Python)
* **Database ORM**: **Flask-SQLAlchemy** (for SQLite by default)
* **User Management**: **Flask-Login**
* **Password Hashing**: **Werkzeug**
* **Forms**: **Flask-WTF**
* **Frontend**: HTML5, CSS3, JavaScript (Jinja2 templating)
* **File Handling**: `werkzeug.utils.secure_filename`, `uuid`

---

## 🚀 Setup and Installation

Follow these steps to get the project up and running on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/secure-file-sharing-flask.git](https://github.com/yourusername/secure-file-sharing-flask.git)
    cd secure-file-sharing-flask
    ```
    (Replace `yourusername/secure-file-sharing-flask.git` with your actual repository URL.)

2.  **Create a Python virtual environment (highly recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    * **On Windows:**
        ```bash
        venv\Scripts\activate
        ```

4.  **Install dependencies:**
    It's best practice to create a `requirements.txt` file after installing all packages.
    ```bash
    pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF python-dotenv
    # After installing, you can create a requirements.txt file:
    # pip freeze > requirements.txt
    ```

5.  **Set Environment Variables:**
    For security, **never hardcode your `SECRET_KEY`**. Create a file named `.env` in the root of your project directory (`secure_file_sharing/`) and add your secret key there.

    **`.env` file content:**
    ```dotenv
    SECRET_KEY='a_very_long_and_random_secret_key_for_production'
    # Optionally, for production, you might specify a different database:
    # DATABASE_URL='postgresql://user:password@host:port/database_name'
    ```
    *Replace `'a_very_long_and_random_secret_key_for_production'` with a strong, randomly generated string.*

6.  **Run the application:**
    ```bash
    python app.py
    ```

7.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

---

## 💡 Usage

Once the application is running:

1.  **Register** a new user account if you don't have one, or **Log In** with existing credentials.
2.  After logging in, you'll be redirected to your **Dashboard**.
3.  Click on the **Upload** link to upload new files from your computer.
4.  On the **Dashboard**, you'll see a list of your uploaded files.
    * **Download**: Click the "Download" link next to a file to retrieve it.
    * **Share**: Click "Share" to share a file with another registered user by entering their username.
    * **Delete**: Click "Delete" to remove a file from the system (requires confirmation).
    * **Generate Public Link**: If you choose to, you can create a public, shareable URL for your file (use with extreme caution).
5.  Files shared with you by other users will appear under the "Files Shared With You" section on your dashboard.

---

## 🔒 Security Notes (Important!)

This project provides a foundation for secure file sharing, but for a production environment, several critical security considerations must be addressed:

* **Secret Key**: The `SECRET_KEY` in `config.py` should **always be an environment variable** and never hardcoded in production. It's vital for session management and security.
* **HTTPS/SSL**: **Absolutely essential** for any public-facing application. Always deploy with HTTPS to encrypt all data transmitted between the client and server. Tools like Nginx with Let's Encrypt can help.
* **File Encryption at Rest**: The current implementation stores files as-is on the server's disk. For highly sensitive data, implement **server-side encryption** of files *before* storing them and decryption on download. Libraries like `cryptography` or `PyNaCl` can be used. This also requires secure key management.
* **Robust File Type Validation**: While `secure_filename` helps prevent path traversal, you should implement stricter **MIME type validation** to ensure only allowed file types are uploaded, preventing malicious script uploads.
* **File Size Limits**: While `MAX_CONTENT_LENGTH` is set, consider more granular checks and user feedback for large files.
* **Rate Limiting**: Implement **rate limiting** on routes like login, registration, and file uploads to mitigate brute-force attacks and prevent resource exhaustion. (e.g., using `Flask-Limiter`).
* **Error Handling and Logging**: Implement comprehensive error handling and logging to monitor application behavior and detect potential security incidents.
* **Database Security**: For production, move away from SQLite to a more robust and secure database like **PostgreSQL** or **MySQL**, and ensure proper database user permissions.
* **XSS Protection**: Jinja2 templates auto-escape HTML, but always be cautious when rendering any user-generated content directly.
* **Regular Security Audits**: Periodically review your code and dependencies for known vulnerabilities.
