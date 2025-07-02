import os
import shutil
import zipfile
import tempfile
import requests
import json

# External dependencies (pip install gitpython pydrive2 dropbox boto3 python-gitlab)
from git import Repo
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import dropbox
import boto3
from ftplib import FTP

PROJECTS_DIR = "projects"
IGNORED_FOLDERS = [
    'node_modules', '.venv', '.git', '__pycache__', 'dist', 'build', '.idea', '.mypy_cache', '.pytest_cache'
]
IGNORED_FILES = ['.DS_Store', 'Thumbs.db']
IGNORED_EXTENSIONS = ['.log', '.pyc', '.pyo']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 Mo

def should_ignore(path):
    parts = set(os.path.normpath(path).split(os.sep))
    if any(ignored in parts for ignored in IGNORED_FOLDERS):
        return True
    if os.path.basename(path) in IGNORED_FILES:
        return True
    if any(path.lower().endswith(ext) for ext in IGNORED_EXTENSIONS):
        return True
    try:
        if os.path.isfile(path) and os.path.getsize(path) > MAX_FILE_SIZE:
            return True
    except Exception:
        pass
    return False

# --- Core project management ---

def create_project(project_name):
    path = os.path.join(PROJECTS_DIR, project_name)
    if os.path.exists(path):
        return False, f"Project '{project_name}' already exists."
    try:
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "main.py"), "w", encoding="utf-8") as f:
            f.write("# New Python project\n")
        with open(os.path.join(path, "state.json"), "w", encoding="utf-8") as f:
            json.dump({}, f)
        return True, f"Project '{project_name}' created successfully."
    except Exception as e:
        return False, f"Error creating project: {e}"

def list_projects():
    if not os.path.exists(PROJECTS_DIR):
        return []
    return [name for name in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, name))]

def save_project_state(project_name, state):
    state_file = os.path.join(PROJECTS_DIR, project_name, "state.json")
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def load_project_state(project_name):
    state_file = os.path.join(PROJECTS_DIR, project_name, "state.json")
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def delete_project(project_name):
    path = os.path.join(PROJECTS_DIR, project_name)
    if os.path.exists(path):
        shutil.rmtree(path)
        return True
    return False

def export_project(project_name, export_path=None):
    """
    Zip a project folder and return zip path, en excluant dépendances et gros fichiers.
    """
    folder = os.path.join(PROJECTS_DIR, project_name)
    zip_path = export_path or f"{folder}.zip"
    if not os.path.exists(folder):
        return False, "Project does not exist."
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder):
                dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, folder)
                    if should_ignore(abs_path):
                        continue
                    zipf.write(abs_path, arcname=rel_path)
        return True, zip_path
    except Exception as e:
        return False, f"Error during export: {e}"

# --- Import Functions (zip, local folder, github, etc) ---

def import_project_from_zip(zip_path, project_name=None):
    """
    Import a project from a ZIP file, filtré.
    """
    if not os.path.exists(zip_path):
        return False, "ZIP file not found."
    base_name = project_name or os.path.splitext(os.path.basename(zip_path))[0]
    extract_dir = os.path.join(PROJECTS_DIR, base_name)
    if os.path.exists(extract_dir):
        return False, f"Project '{base_name}' already exists. Please choose another name or delete the existing one."
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
            for root, dirs, files in os.walk(tmpdir):
                dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]
                for file in files:
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, tmpdir)
                    dest_path = os.path.join(extract_dir, rel_path)
                    if should_ignore(src_path):
                        continue
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(src_path, dest_path)
        return True, f"Project imported into {extract_dir}"
    except Exception as e:
        return False, f"Error importing ZIP: {e}"

def import_project_from_local_folder(folder_path, project_name=None):
    dest = os.path.join(PROJECTS_DIR, project_name or os.path.basename(folder_path.rstrip('/\\')))
    try:
        os.makedirs(dest, exist_ok=True)
        for root, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]
            for f in files:
                src_path = os.path.join(root, f)
                rel_path = os.path.relpath(src_path, folder_path)
                dest_path = os.path.join(dest, rel_path)
                if should_ignore(src_path):
                    continue
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
        return True, f"Project imported from {folder_path}"
    except Exception as e:
        return False, f"Error importing local folder: {e}"

def import_project_from_github(github_url, token=None, project_name=None):
    base_name = project_name or github_url.rstrip('/').split('/')[-1]
    dest = os.path.join(PROJECTS_DIR, base_name)
    try:
        if token:
            repo_url = github_url.replace('https://', f'https://{token}@')
        else:
            repo_url = github_url
        Repo.clone_from(repo_url, dest)
        return True, f"GitHub project cloned to {dest}"
    except Exception as e:
        return False, f"Error importing from GitHub: {e}"

def import_project_from_gdrive(gdrive_id, gdrive_token=None, project_name=None):
    base_name = project_name or f"gdrive_{gdrive_id}"
    dest = os.path.join(PROJECTS_DIR, base_name)
    try:
        gauth = GoogleAuth()
        if gdrive_token:
            gauth.LoadCredentialsFile(gdrive_token)
        else:
            gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({'id': gdrive_id})
        file.FetchMetadata()
        os.makedirs(dest, exist_ok=True)
        file.GetContentFile(os.path.join(dest, file['title']))
        return True, f"GDrive project imported to {dest}"
    except Exception as e:
        return False, f"Error importing from GDrive: {e}"

def import_project_from_dropbox(dropbox_link, dropbox_token=None, project_name=None):
    base_name = project_name or "dropbox_import"
    dest = os.path.join(PROJECTS_DIR, base_name)
    try:
        dbx = dropbox.Dropbox(dropbox_token)
        metadata, res = dbx.files_download(dropbox_link)
        os.makedirs(dest, exist_ok=True)
        with open(os.path.join(dest, metadata.name), "wb") as f:
            f.write(res.content)
        return True, f"Dropbox project imported to {dest}"
    except Exception as e:
        return False, f"Error importing from Dropbox: {e}"

def import_project_from_icloud(icloud_url, icloud_token=None, project_name=None):
    return False, "iCloud import not supported in Python (Apple limitation)"

def import_project_from_s3(s3_url, aws_access_key=None, aws_secret_key=None, project_name=None):
    from urllib.parse import urlparse
    parsed = urlparse(s3_url)
    bucket = parsed.netloc
    prefix = parsed.path.lstrip('/')
    base_name = project_name or f"s3_{bucket}_{prefix.replace('/', '_')}"
    dest = os.path.join(PROJECTS_DIR, base_name)
    try:
        s3 = boto3.resource('s3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key)
        os.makedirs(dest, exist_ok=True)
        bucket_obj = s3.Bucket(bucket)
        for obj in bucket_obj.objects.filter(Prefix=prefix):
            target = os.path.join(dest, obj.key[len(prefix):].lstrip('/'))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            bucket_obj.download_file(obj.key, target)
        return True, f"S3 project imported to {dest}"
    except Exception as e:
        return False, f"Error importing from S3: {e}"

def import_project_from_http(http_url, project_name=None):
    local_name = project_name or http_url.split("/")[-1]
    dest = os.path.join(PROJECTS_DIR, f"http_{local_name}")
    try:
        r = requests.get(http_url)
        os.makedirs(dest, exist_ok=True)
        path = os.path.join(dest, local_name)
        with open(path, "wb") as f:
            f.write(r.content)
        if local_name.endswith(".zip"):
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(dest)
        return True, f"HTTP project imported to {dest}"
    except Exception as e:
        return False, f"Error importing from HTTP: {e}"

def import_project_from_ftp(ftp_url, ftp_user=None, ftp_pass=None, project_name=None):
    from urllib.parse import urlparse
    parsed = urlparse(ftp_url)
    base_name = project_name or f"ftp_{parsed.hostname}"
    dest = os.path.join(PROJECTS_DIR, base_name)
    try:
        ftp = FTP(parsed.hostname)
        ftp.login(user=ftp_user, passwd=ftp_pass)
        os.makedirs(dest, exist_ok=True)
        files = ftp.nlst()
        for fname in files:
            with open(os.path.join(dest, fname), "wb") as f:
                ftp.retrbinary("RETR " + fname, f.write)
        ftp.quit()
        return True, f"FTP project imported to {dest}"
    except Exception as e:
        return False, f"Error importing from FTP: {e}"

def import_project_from_svn(svn_url, project_name=None):
    base_name = project_name or svn_url.split('/')[-1]
    dest = os.path.join(PROJECTS_DIR, base_name)
    try:
        import subprocess
        subprocess.check_call(['svn', 'checkout', svn_url, dest])
        return True, f"SVN project imported to {dest}"
    except Exception as e:
        return False, f"Error importing from SVN: {e}"

def import_project_from_bitbucket(bitbucket_url, token=None, project_name=None):
    return import_project_from_github(bitbucket_url, token=token, project_name=project_name)

def import_project_from_gitlab(gitlab_url, token=None, project_name=None):
    base_name = project_name or gitlab_url.rstrip('/').split('/')[-1]
    dest = os.path.join(PROJECTS_DIR, base_name)
    try:
        if token:
            repo_url = gitlab_url.replace('https://', f'https://oauth2:{token}@')
        else:
            repo_url = gitlab_url
        Repo.clone_from(repo_url, dest)
        return True, f"GitLab project cloned to {dest}"
    except Exception as e:
        return False, f"Error importing from GitLab: {e}"
