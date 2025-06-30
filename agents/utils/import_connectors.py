import os
import zipfile
import subprocess
import requests
import tempfile
from agents.utils.logger import get_logger

logger = get_logger("ImportConnectors")

def import_zip_file(zip_path, extract_to="workspace/imported_zip"):
    """Dézippe un projet ZIP vers le dossier cible."""
    logger.info(f"Début import ZIP: {zip_path} → {extract_to}")
    if not os.path.exists(zip_path) or not zip_path.endswith('.zip'):
        logger.error("Fichier ZIP non trouvé ou extension incorrecte.")
        return False, "Fichier ZIP non trouvé."
    try:
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        logger.info(f"Import ZIP réussi: {extract_to}")
        return True, extract_to
    except Exception as e:
        logger.error(f"Erreur lors de l’extraction ZIP : {e}")
        return False, f"Erreur lors de l’extraction ZIP : {e}"

def import_local_folder(folder_path):
    """Vérifie qu’un dossier local existe et le rend utilisable."""
    logger.info(f"Début import dossier local: {folder_path}")
    if os.path.isdir(folder_path):
        logger.info(f"Dossier local importé: {folder_path}")
        return True, folder_path
    logger.error(f"Chemin local invalide ou inaccessible: {folder_path}")
    return False, "Chemin local invalide ou inaccessible."

def import_from_github(github_url, dest_folder="workspace/imported_github", token=None):
    """Clone un repo Github (public ou privé si token donné)"""
    logger.info(f"Début import GitHub: {github_url} → {dest_folder}")
    if not github_url.startswith("https://github.com/"):
        logger.error("URL Github invalide.")
        return False, "URL Github invalide."
    try:
        clone_url = github_url
        if token:
            # Authentification https (token personnel)
            user = "x-access-token"
            clone_url = github_url.replace("https://", f"https://{user}:***@")  # on ne log pas le token !
        if os.path.exists(dest_folder):
            subprocess.call(["rm", "-rf", dest_folder])
        os.system(f'git clone "{clone_url}" "{dest_folder}"')
        if os.path.exists(dest_folder):
            logger.info(f"Clonage GitHub réussi: {dest_folder}")
            return True, dest_folder
        logger.error("Échec du clonage Github.")
        return False, "Échec du clonage Github."
    except Exception as e:
        logger.error(f"Erreur Github : {e}")
        return False, f"Erreur Github : {e}"

def import_from_gdrive(gdrive_id, dest_folder="workspace/imported_gdrive", gdrive_token=None):
    """
    Télécharge un fichier/dossier depuis Google Drive.
    Requiert la lib 'gdown' installée (pip install gdown)
    """
    logger.info(f"Début import Google Drive: {gdrive_id} → {dest_folder}")
    try:
        import gdown
    except ImportError:
        logger.error("Le module gdown est requis (pip install gdown).")
        return False, "Le module gdown est requis (pip install gdown)."
    if not gdrive_id:
        logger.error("ID Google Drive requis.")
        return False, "ID Google Drive requis."
    os.makedirs(dest_folder, exist_ok=True)
    try:
        output = os.path.join(dest_folder, gdrive_id)
        url = f"https://drive.google.com/uc?id={gdrive_id}"
        gdown.download(url, output, quiet=False)
        logger.info(f"Fichier Google Drive téléchargé: {output}")
        return True, output
    except Exception as e:
        logger.error(f"Erreur Google Drive : {e}")
        return False, f"Erreur Google Drive : {e}"

def import_from_dropbox(dropbox_link, dest_folder="workspace/imported_dropbox", dropbox_token=None):
    """
    Télécharge un fichier partagé Dropbox via l'API Dropbox.
    Requiert 'dropbox' SDK (pip install dropbox)
    """
    logger.info(f"Début import Dropbox: {dropbox_link} → {dest_folder}")
    try:
        import dropbox
    except ImportError:
        logger.error("Le module dropbox est requis (pip install dropbox).")
        return False, "Le module dropbox est requis (pip install dropbox)."
    if not dropbox_token:
        logger.error("Clé API Dropbox requise.")
        return False, "Clé API Dropbox requise."
    try:
        dbx = dropbox.Dropbox(dropbox_token)
        shared_link_metadata = dbx.sharing_get_shared_link_metadata(dropbox_link)
        download_path = os.path.join(dest_folder, shared_link_metadata.name)
        os.makedirs(dest_folder, exist_ok=True)
        with open(download_path, "wb") as f:
            metadata, res = dbx.sharing_get_shared_link_file(url=dropbox_link)
            f.write(res.content)
        logger.info(f"Fichier Dropbox téléchargé: {download_path}")
        return True, download_path
    except Exception as e:
        logger.error(f"Erreur Dropbox : {e}")
        return False, f"Erreur Dropbox : {e}"

def import_from_icloud(icloud_url, dest_folder="workspace/imported_icloud", icloud_token=None):
    """
    (BETA) iCloud n'a pas d'API publique officielle pour le download direct.
    Nécessite icloudpd (https://github.com/icloud-photos-downloader/icloud_photos_downloader)
    """
    logger.warning("Import iCloud non supporté en standard.")
    return False, "Import iCloud non supporté en standard. Voir icloudpd pour solution avancée."

def import_from_s3(s3_url, dest_folder="workspace/imported_s3", aws_access_key=None, aws_secret_key=None):
    """
    Télécharge un fichier depuis AWS S3. Requiert 'boto3'.
    """
    logger.info(f"Début import S3: {s3_url} → {dest_folder}")
    try:
        import boto3
    except ImportError:
        logger.error("Le module boto3 est requis (pip install boto3).")
        return False, "Le module boto3 est requis (pip install boto3)."
    if not s3_url or not aws_access_key or not aws_secret_key:
        logger.error("URL S3 et clés AWS requises.")
        return False, "URL S3 et clés AWS requises."
    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        bucket_name = s3_url.split('/')[2]
        object_key = '/'.join(s3_url.split('/')[3:])
        file_name = os.path.basename(object_key)
        download_path = os.path.join(dest_folder, file_name)
        os.makedirs(dest_folder, exist_ok=True)
        s3.download_file(bucket_name, object_key, download_path)
        logger.info(f"Fichier S3 téléchargé: {download_path}")
        return True, download_path
    except Exception as e:
        logger.error(f"Erreur S3 : {e}")
        return False, f"Erreur S3 : {e}"

def import_from_http(http_url, dest_folder="workspace/imported_http"):
    """
    Télécharge un fichier depuis une URL HTTP. Requiert 'requests'.
    """
    logger.info(f"Début import HTTP: {http_url} → {dest_folder}")
    try:
        import requests
    except ImportError:
        logger.error("Le module requests est requis (pip install requests).")
        return False, "Le module requests est requis (pip install requests)."
    if not http_url:
        logger.error("URL HTTP requise.")
        return False, "URL HTTP requise."
    try:
        response = requests.get(http_url)
        response.raise_for_status()
        os.makedirs(dest_folder, exist_ok=True)
        file_name = os.path.basename(http_url)
        download_path = os.path.join(dest_folder, file_name)
        with open(download_path, 'wb') as f:
            f.write(response.content)
        logger.info(f"Fichier HTTP téléchargé: {download_path}")
        return True, download_path
    except Exception as e:
        logger.error(f"Erreur HTTP : {e}")
        return False, f"Erreur HTTP : {e}"

def import_from_ftp(ftp_url, dest_folder="workspace/imported_ftp", ftp_user=None, ftp_pass=None):
    """
    Télécharge un fichier depuis un serveur FTP.
    """
    logger.info(f"Début import FTP: {ftp_url} → {dest_folder}")
    from ftplib import FTP, error_perm
    if not ftp_url:
        logger.error("URL FTP requise.")
        return False, "URL FTP requise."
    try:
        ftp = FTP(ftp_url)
        if ftp_user and ftp_pass:
            ftp.login(user=ftp_user, passwd=ftp_pass)
        else:
            ftp.login()
        os.makedirs(dest_folder, exist_ok=True)
        file_name = os.path.basename(ftp_url)
        download_path = os.path.join(dest_folder, file_name)
        with open(download_path, 'wb') as f:
            ftp.retrbinary(f'RETR {file_name}', f.write)
        ftp.quit()
        logger.info(f"Fichier FTP téléchargé: {download_path}")
        return True, download_path
    except error_perm as e:
        logger.error(f"Erreur FTP (permission) : {e}")
        return False, f"Erreur FTP : {e}"
    except Exception as e:
        logger.error(f"Erreur de connexion FTP : {e}")
        return False, f"Erreur de connexion FTP : {e}"

def import_from_svn(svn_url, dest_folder="workspace/imported_svn"):
    """
    Clone un dépôt SVN.
    """
    logger.info(f"Début import SVN: {svn_url} → {dest_folder}")
    if not svn_url:
        logger.error("URL SVN requise.")
        return False, "URL SVN requise."
    try:
        if os.path.exists(dest_folder):
            subprocess.call(["rm", "-rf", dest_folder])
        os.makedirs(dest_folder, exist_ok=True)
        subprocess.check_call(['svn', 'checkout', svn_url, dest_folder])
        logger.info(f"Clonage SVN réussi: {dest_folder}")
        return True, dest_folder
    except subprocess.CalledProcessError as e:
        logger.error(f"Erreur SVN (commande): {e}")
        return False, f"Erreur SVN : {e}"
    except Exception as e:
        logger.error(f"Erreur de connexion SVN : {e}")
        return False, f"Erreur de connexion SVN : {e}"

def import_from_bitbucket(bitbucket_url, dest_folder="workspace/imported_bitbucket", token=None):
    """
    Clone un dépôt Bitbucket (public ou privé si token donné).
    """
    logger.info(f"Début import Bitbucket: {bitbucket_url} → {dest_folder}")
    if not bitbucket_url.startswith("https://bitbucket.org/"):
        logger.error("URL Bitbucket invalide.")
        return False, "URL Bitbucket invalide."
    try:
        clone_url = bitbucket_url
        if token:
            user = "x-token-auth"
            clone_url = bitbucket_url.replace("https://", f"https://{user}:***@")
        if os.path.exists(dest_folder):
            subprocess.call(["rm", "-rf", dest_folder])
        os.system(f'git clone "{clone_url}" "{dest_folder}"')
        if os.path.exists(dest_folder):
            logger.info(f"Clonage Bitbucket réussi: {dest_folder}")
            return True, dest_folder
        logger.error("Échec du clonage Bitbucket.")
        return False, "Échec du clonage Bitbucket."
    except Exception as e:
        logger.error(f"Erreur Bitbucket : {e}")
        return False, f"Erreur Bitbucket : {e}"

def import_from_gitlab(gitlab_url, dest_folder="workspace/imported_gitlab", token=None):
    """
    Clone un dépôt GitLab (public ou privé si token donné).
    """
    logger.info(f"Début import GitLab: {gitlab_url} → {dest_folder}")
    if not gitlab_url.startswith("https://gitlab.com/"):
        logger.error("URL GitLab invalide.")
        return False, "URL GitLab invalide."
    try:
        clone_url = gitlab_url
        if token:
            user = "oauth2"
            clone_url = gitlab_url.replace("https://", f"https://{user}:***@")
        if os.path.exists(dest_folder):
            subprocess.call(["rm", "-rf", dest_folder])
        os.system(f'git clone "{clone_url}" "{dest_folder}"')
        if os.path.exists(dest_folder):
            logger.info(f"Clonage GitLab réussi: {dest_folder}")
            return True, dest_folder
        logger.error("Échec du clonage GitLab.")
        return False, "Échec du clonage GitLab."
    except Exception as e:
        logger.error(f"Erreur GitLab : {e}")
        return False, f"Erreur GitLab : {e}"
