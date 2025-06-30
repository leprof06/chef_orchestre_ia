# agents/utils/import_connectors.py

import os
import zipfile
import subprocess
import requests

def import_zip_file(zip_path, extract_to="workspace/imported_zip"):
    """Dézippe un projet ZIP vers le dossier cible."""
    if not os.path.exists(zip_path) or not zip_path.endswith('.zip'):
        return False, "Fichier ZIP non trouvé."
    try:
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True, extract_to
    except Exception as e:
        return False, f"Erreur lors de l’extraction ZIP : {e}"

def import_local_folder(folder_path):
    """Vérifie qu’un dossier local existe et le rend utilisable."""
    if os.path.isdir(folder_path):
        return True, folder_path
    return False, "Chemin local invalide ou inaccessible."

def import_from_github(github_url, dest_folder="workspace/imported_github", token=None):
    """Clone un repo Github (public ou privé si token donné)"""
    if not github_url.startswith("https://github.com/"):
        return False, "URL Github invalide."
    try:
        clone_url = github_url
        if token:
            # Authentification https (token personnel)
            user = "x-access-token"
            clone_url = github_url.replace("https://", f"https://{user}:{token}@")
        # Utilise git clone (nécessite git installé)
        if os.path.exists(dest_folder):
            subprocess.call(["rm", "-rf", dest_folder])  # Nettoie avant de cloner
        os.system(f'git clone "{clone_url}" "{dest_folder}"')
        if os.path.exists(dest_folder):
            return True, dest_folder
        return False, "Échec du clonage Github."
    except Exception as e:
        return False, f"Erreur Github : {e}"

def import_from_gdrive(gdrive_id, dest_folder="workspace/imported_gdrive", gdrive_token=None):
    """
    Télécharge un fichier/dossier depuis Google Drive.
    gdrive_id : identifiant du fichier/dossier
    Requiert la lib 'gdown' installée (pip install gdown)
    """
    try:
        import gdown
    except ImportError:
        return False, "Le module gdown est requis (pip install gdown)."
    if not gdrive_id:
        return False, "ID Google Drive requis."
    os.makedirs(dest_folder, exist_ok=True)
    try:
        output = os.path.join(dest_folder, gdrive_id)
        url = f"https://drive.google.com/uc?id={gdrive_id}"
        gdown.download(url, output, quiet=False)
        return True, output
    except Exception as e:
        return False, f"Erreur Google Drive : {e}"

def import_from_dropbox(dropbox_link, dest_folder="workspace/imported_dropbox", dropbox_token=None):
    """
    Télécharge un fichier partagé Dropbox (lien partage) via l'API Dropbox.
    Requiert 'dropbox' SDK (pip install dropbox)
    """
    try:
        import dropbox
    except ImportError:
        return False, "Le module dropbox est requis (pip install dropbox)."
    if not dropbox_token:
        return False, "Clé API Dropbox requise."
    try:
        dbx = dropbox.Dropbox(dropbox_token)
        shared_link_metadata = dbx.sharing_get_shared_link_metadata(dropbox_link)
        # Télécharge le fichier partagé
        download_path = os.path.join(dest_folder, shared_link_metadata.name)
        os.makedirs(dest_folder, exist_ok=True)
        with open(download_path, "wb") as f:
            metadata, res = dbx.sharing_get_shared_link_file(url=dropbox_link)
            f.write(res.content)
        return True, download_path
    except Exception as e:
        return False, f"Erreur Dropbox : {e}"

def import_from_icloud(icloud_url, dest_folder="workspace/imported_icloud", icloud_token=None):
    """
    (BETA) iCloud n'a pas d'API publique officielle pour le download direct.
    Nécessite icloudpd (https://github.com/icloud-photos-downloader/icloud_photos_downloader)
    et une authentification utilisateur.
    """
    return False, "Import iCloud non supporté en standard. Voir icloudpd pour solution avancée."

# TODO: Ajouter GitLab, Bitbucket, AWS S3, HuggingFace, etc.
def import_from_s3(s3_url, dest_folder="workspace/imported_s3", aws_access_key=None, aws_secret_key=None):
    """
    Télécharge un fichier depuis AWS S3.
    Requiert 'boto3' (pip install boto3)
    """
    try:
        import boto3
    except ImportError:
        return False, "Le module boto3 est requis (pip install boto3)."
    
    if not s3_url or not aws_access_key or not aws_secret_key:
        return False, "URL S3 et clés AWS requises."
    
    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        bucket_name = s3_url.split('/')[2]
        object_key = '/'.join(s3_url.split('/')[3:])
        file_name = os.path.basename(object_key)
        download_path = os.path.join(dest_folder, file_name)
        
        os.makedirs(dest_folder, exist_ok=True)
        s3.download_file(bucket_name, object_key, download_path)
        
        return True, download_path
    except Exception as e:
        return False, f"Erreur S3 : {e}"

def import_from_http(http_url, dest_folder="workspace/imported_http"):
    """
    Télécharge un fichier depuis une URL HTTP.
    Requiert 'requests' (pip install requests)
    """
    try:
        import requests
    except ImportError:
        return False, "Le module requests est requis (pip install requests)."
    
    if not http_url:
        return False, "URL HTTP requise."
    
    try:
        response = requests.get(http_url)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        
        os.makedirs(dest_folder, exist_ok=True)
        file_name = os.path.basename(http_url)
        download_path = os.path.join(dest_folder, file_name)
        
        with open(download_path, 'wb') as f:
            f.write(response.content)
        
        return True, download_path
    except Exception as e:
        return False, f"Erreur HTTP : {e}"

def import_from_ftp(ftp_url, dest_folder="workspace/imported_ftp", ftp_user=None, ftp_pass=None):
    """
    Télécharge un fichier depuis un serveur FTP.
    Requiert 'ftplib' (inclus dans la bibliothèque standard Python)
    """
    from ftplib import FTP, error_perm
    
    if not ftp_url:
        return False, "URL FTP requise."
    
    try:
        ftp = FTP(ftp_url)
        if ftp_user and ftp_pass:
            ftp.login(user=ftp_user, passwd=ftp_pass)
        else:
            ftp.login()  # Anonyme
        
        os.makedirs(dest_folder, exist_ok=True)
        file_name = os.path.basename(ftp_url)
        download_path = os.path.join(dest_folder, file_name)
        
        with open(download_path, 'wb') as f:
            ftp.retrbinary(f'RETR {file_name}', f.write)
        
        ftp.quit()
        return True, download_path
    except error_perm as e:
        return False, f"Erreur FTP : {e}"
    except Exception as e:
        return False, f"Erreur de connexion FTP : {e}"

def import_from_svn(svn_url, dest_folder="workspace/imported_svn"):
    """
    Clone un dépôt SVN.
    Requiert 'subversion' (svn) installé sur le système.
    """
    if not svn_url:
        return False, "URL SVN requise."
    
    try:
        if os.path.exists(dest_folder):
            subprocess.call(["rm", "-rf", dest_folder])  # Nettoie avant de cloner
        os.makedirs(dest_folder, exist_ok=True)
        subprocess.check_call(['svn', 'checkout', svn_url, dest_folder])
        return True, dest_folder
    except subprocess.CalledProcessError as e:
        return False, f"Erreur SVN : {e}"
    except Exception as e:
        return False, f"Erreur de connexion SVN : {e}"

def import_from_bitbucket(bitbucket_url, dest_folder="workspace/imported_bitbucket", token=None):
    """
    Clone un dépôt Bitbucket (public ou privé si token donné).
    Requiert 'git' installé sur le système.
    """
    if not bitbucket_url.startswith("https://bitbucket.org/"):
        return False, "URL Bitbucket invalide."
    
    try:
        clone_url = bitbucket_url
        if token:
            # Authentification https (token personnel)
            user = "x-token-auth"
            clone_url = bitbucket_url.replace("https://", f"https://{user}:{token}@")
        
        if os.path.exists(dest_folder):
            subprocess.call(["rm", "-rf", dest_folder])  # Nettoie avant de cloner
        os.system(f'git clone "{clone_url}" "{dest_folder}"')
        
        if os.path.exists(dest_folder):
            return True, dest_folder
        return False, "Échec du clonage Bitbucket."
    except Exception as e:
        return False, f"Erreur Bitbucket : {e}"

def import_from_gitlab(gitlab_url, dest_folder="workspace/imported_gitlab", token=None):
    """
    Clone un dépôt GitLab (public ou privé si token donné).
    Requiert 'git' installé sur le système.
    """
    if not gitlab_url.startswith("https://gitlab.com/"):
        return False, "URL GitLab invalide."
    
    try:
        clone_url = gitlab_url
        if token:
            # Authentification https (token personnel)
            user = "oauth2"
            clone_url = gitlab_url.replace("https://", f"https://{user}:{token}@")
        
        if os.path.exists(dest_folder):
            subprocess.call(["rm", "-rf", dest_folder])  # Nettoie avant de cloner
        os.system(f'git clone "{clone_url}" "{dest_folder}"')
        
        if os.path.exists(dest_folder):
            return True, dest_folder
        return False, "Échec du clonage GitLab."
    except Exception as e:
        return False, f"Erreur GitLab : {e}"
