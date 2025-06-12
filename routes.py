from flask import render_template, url_for, flash, redirect, request, send_from_directory
from app import app, db
from models import User, File, SharedFile
from forms import RegistrationForm, LoginForm, UploadFileForm, ShareFileForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
import uuid # For generating unique filenames

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login Successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def dashboard():
    user_files = File.query.filter_by(user_id=current_user.id).all()
    # Files shared with the current user
    shared_files_with_me = current_user.can_access_files.all()
    return render_template('dashboard.html', title='Dashboard', files=user_files, shared_files_with_me=shared_files_with_me)

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadFileForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file:
            original_filename = secure_filename(file.filename)
            unique_filename = str(uuid.uuid4()) + '_' + original_filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            new_file = File(
                filename=unique_filename,
                original_filename=original_filename,
                file_path=file_path,
                user_id=current_user.id
            )
            db.session.add(new_file)
            db.session.commit()
            flash('Your file has been uploaded!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('upload.html', title='Upload File', form=form)

@app.route("/download/<int:file_id>")
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    # Check if the current user is the owner of the file OR
    # if the file is shared with the current user
    if file.user_id != current_user.id and current_user not in file.shared_with.all():
        flash('You do not have permission to download this file.', 'danger')
        return redirect(url_for('dashboard'))

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        file.filename,
        as_attachment=True,
        download_name=file.original_filename
    )

@app.route("/share/<int:file_id>", methods=['GET', 'POST'])
@login_required
def share_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        flash('You do not have permission to share this file.', 'danger')
        return redirect(url_for('dashboard'))

    form = ShareFileForm()
    if form.validate_on_submit():
        recipient = User.query.filter_by(username=form.recipient_username.data).first()
        if not recipient:
            flash('User not found.', 'danger')
            return redirect(url_for('share_file', file_id=file.id))

        if recipient == current_user:
            flash('You cannot share a file with yourself.', 'warning')
            return redirect(url_for('share_file', file_id=file.id))

        # Check if already shared
        if recipient in file.shared_with.all():
            flash(f'File already shared with {recipient.username}.', 'info')
            return redirect(url_for('dashboard'))

        file.shared_with.append(recipient)
        db.session.commit()
        flash(f'File "{file.original_filename}" shared with {recipient.username} successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    # List of users this file is already shared with
    already_shared_with = file.shared_with.all()
    return render_template('share_file.html', title='Share File', form=form, file=file, already_shared_with=already_shared_with)

@app.route("/delete/<int:file_id>", methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        flash('You do not have permission to delete this file.', 'danger')
        return redirect(url_for('dashboard'))

    try:
        os.remove(file.file_path) # Delete file from file system
        db.session.delete(file)
        db.session.commit()
        flash('File deleted successfully!', 'success')
    except OSError as e:
        flash(f'Error deleting file: {e}', 'danger')
    return redirect(url_for('dashboard'))

# Optional: Publicly shareable link (be cautious with this)
@app.route("/public_share/<int:file_id>")
@login_required
def generate_public_link(file_id):
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        flash('You do not have permission to generate a public link for this file.', 'danger')
        return redirect(url_for('dashboard'))

    if not file.is_shared:
        file.share_link = str(uuid.uuid4())
        file.is_shared = True
        db.session.commit()
        flash('Public share link generated!', 'success')
    return render_template('share_file.html', title='Share File', file=file) # Display the link on the share page

@app.route("/shared/<string:share_link>")
def access_shared_file(share_link):
    file = File.query.filter_by(share_link=share_link, is_shared=True).first_or_404()
    # No login_required for public links, but you might want to add rate limiting
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        file.filename,
        as_attachment=True,
        download_name=file.original_filename
    )
