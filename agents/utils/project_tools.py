import os
import shutil
import zipfile
import requests

# Dépendances externes nécessaires :
# pip install gitpython pydrive2 dropbox boto3 python-gitlab pysvn ftplib

from git import Repo
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import dropbox
import boto3
import gitlab
from ftplib import FTP

def get_existing_projects():
    projects_dir = "projects"
    if not os.path.exists(projects_dir):
        return []
    return [name for name in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, name))]

def save_project(project_name):
    return True  # À adapter si tu veux une logique avancée

def load_project(project_name):
    return True

def delete_project(project_name):
    projects_dir = "projects"
    path = os.path.join(projects_dir, project_name)
    if os.path.exists(path):
        shutil.rmtree(path)
        return True
    return False

def export_project(project_name):
    projects_dir = "projects"
    folder = os.path.join(projects_dir, project_name)
    zip_path = f"{folder}.zip"
    if os.path.exists(folder):
        shutil.make_archive(folder, 'zip', folder)
        return True, zip_path
    return False, "Projet inexistant"

def import_zip_file(zip_path):
    if not os.path.exists(zip_path):
        return False, "Fichier ZIP introuvable."
    try:
        extract_dir = os.path.splitext(zip_path)[0]
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        return True, f"Projet importé dans {extract_dir}"
    except Exception as e:
        return False, f"Erreur lors de l'import ZIP : {e}"

def import_local_folder(folder_path):
    projects_dir = "projects"
    if not os.path.exists(folder_path):
        return False, "Dossier local introuvable."
    project_name = os.path.basename(folder_path.rstrip('/\\'))
    dest = os.path.join(projects_dir, project_name)
    try:
        shutil.copytree(folder_path, dest)
        return True, f"Projet importé depuis {folder_path}"
    except Exception as e:
        return False, f"Erreur lors de l'import dossier local : {e}"

def import_from_github(github_url, token=None):
    """Clone un repo GitHub public ou privé dans projects/"""
    projects_dir = "projects"
    project_name = github_url.rstrip('/').split('/')[-1]
    dest = os.path.join(projects_dir, project_name)
    try:
        if token:
            # Token: https://<token>@github.com/...
            repo_url = github_url.replace('https://', f'https://{token}@')
        else:
            repo_url = github_url
        Repo.clone_from(repo_url, dest)
        return True, f"Projet GitHub cloné dans {dest}"
    except Exception as e:
        return False, f"Erreur import GitHub : {e}"

def import_from_gdrive(gdrive_id, gdrive_token=None):
    """Télécharge un fichier ou dossier Google Drive (avec Pydrive2, nécessite authentification)"""
    # Hypothèse : l'utilisateur s'est déjà authentifié et le token est dans gdrive_token.json
    projects_dir = "projects"
    dest = os.path.join(projects_dir, f"gdrive_{gdrive_id}")
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
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            # Téléchargement récursif (exemple simplifié)
            file.GetContentFile(os.path.join(dest, file['title']))
        else:
            file.GetContentFile(os.path.join(dest, file['title']))
        return True, f"Projet GDrive importé dans {dest}"
    except Exception as e:
        return False, f"Erreur import GDrive : {e}"

def import_from_dropbox(dropbox_link, dropbox_token=None):
    """Télécharge un dossier/fichier Dropbox"""
    projects_dir = "projects"
    dest = os.path.join(projects_dir, "dropbox_import")
    try:
        dbx = dropbox.Dropbox(dropbox_token)
        metadata, res = dbx.files_download(dropbox_link)
        os.makedirs(dest, exist_ok=True)
        with open(os.path.join(dest, metadata.name), "wb") as f:
            f.write(res.content)
        return True, f"Projet Dropbox importé dans {dest}"
    except Exception as e:
        return False, f"Erreur import Dropbox : {e}"

def import_from_icloud(icloud_url, icloud_token=None):
    # ⚠️ Pas d'API iCloud publique stable en Python, stub :
    return False, "Import iCloud non supporté automatiquement en Python (Apple limitation)"

def import_from_s3(s3_url, aws_access_key=None, aws_secret_key=None):
    """Télécharge un bucket S3 entier dans projects/"""
    import boto3
    from urllib.parse import urlparse
    projects_dir = "projects"
    parsed = urlparse(s3_url)
    bucket = parsed.netloc
    prefix = parsed.path.lstrip('/')
    dest = os.path.join(projects_dir, f"s3_{bucket}_{prefix.replace('/', '_')}")
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
        return True, f"Projet S3 importé dans {dest}"
    except Exception as e:
        return False, f"Erreur import S3 : {e}"

def import_from_http(http_url):
    """Télécharge un zip/code/file via HTTP (GET)"""
    projects_dir = "projects"
    local_name = http_url.split("/")[-1]
    dest = os.path.join(projects_dir, f"http_{local_name}")
    try:
        r = requests.get(http_url)
        os.makedirs(dest, exist_ok=True)
        path = os.path.join(dest, local_name)
        with open(path, "wb") as f:
            f.write(r.content)
        # Dézippe si c'est un zip
        if local_name.endswith(".zip"):
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(dest)
        return True, f"Projet HTTP importé dans {dest}"
    except Exception as e:
        return False, f"Erreur import HTTP : {e}"

def import_from_ftp(ftp_url, ftp_user=None, ftp_pass=None):
    """Télécharge tout un dossier/file FTP"""
    from urllib.parse import urlparse
    projects_dir = "projects"
    parsed = urlparse(ftp_url)
    dest = os.path.join(projects_dir, f"ftp_{parsed.hostname}")
    try:
        ftp = FTP(parsed.hostname)
        ftp.login(user=ftp_user, passwd=ftp_pass)
        # Pour simplifier, on ne télécharge que le dossier courant
        os.makedirs(dest, exist_ok=True)
        files = ftp.nlst()
        for fname in files:
            with open(os.path.join(dest, fname), "wb") as f:
                ftp.retrbinary("RETR " + fname, f.write)
        ftp.quit()
        return True, f"Projet FTP importé dans {dest}"
    except Exception as e:
        return False, f"Erreur import FTP : {e}"

def import_from_svn(svn_url):
    """Clone un repo SVN (nécessite pysvn ou commande svn installée)"""
    projects_dir = "projects"
    dest = os.path.join(projects_dir, svn_url.split('/')[-1])
    try:
        import subprocess
        subprocess.check_call(['svn', 'checkout', svn_url, dest])
        return True, f"Projet SVN importé dans {dest}"
    except Exception as e:
        return False, f"Erreur import SVN : {e}"

def import_from_bitbucket(bitbucket_url, token=None):
    """Clone Bitbucket (public/privé) comme GitHub (token HTTPS)"""
    return import_from_github(bitbucket_url, token=token)

def import_from_gitlab(gitlab_url, token=None):
    """Clone un repo GitLab"""
    projects_dir = "projects"
    project_name = gitlab_url.rstrip('/').split('/')[-1]
    dest = os.path.join(projects_dir, project_name)
    try:
        if token:
            repo_url = gitlab_url.replace('https://', f'https://oauth2:{token}@')
        else:
            repo_url = gitlab_url
        Repo.clone_from(repo_url, dest)
        return True, f"Projet GitLab cloné dans {dest}"
    except Exception as e:
        return False, f"Erreur import GitLab : {e}"
