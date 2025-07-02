# 🔑 API Key Setup Guide

Ce guide explique où et comment obtenir toutes les clés API suggérées/utilisées dans le projet **Chef d'Orchestre IA**. Pour chaque clé, tu trouveras :

- Le lien d’inscription et d’activation
- La procédure détaillée
- La politique de gratuité / limitation / paiement
- Comment l’ajouter au fichier `.env`

---

## 1. OpenAI API Key

- **Lien** : [OpenAI API Keys](https://platform.openai.com/account/api-keys)
- **Procédure** :
  1. Crée un compte ou connecte-toi sur [https://platform.openai.com](https://platform.openai.com)
  2. Va dans “API Keys” (menu de gauche)
  3. Clique sur “Create new secret key”
  4. Copie la clé générée
  5. Ajoute-la à ton fichier `.env` :
     ```
     OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
     ```
- **Tarif** :
  - ⚠️ **Payant** au-delà d’un crédit de bienvenue (\~5\$)
  - Les requêtes IA OpenAI (GPT-3.5/4) sont facturées selon usage (token)
  - Les comptes gratuits ont une limite de crédit, puis doivent recharger

---

## 2. HuggingFace API Token

- **Lien** : [HuggingFace Tokens](https://huggingface.co/settings/tokens)
- **Procédure** :
  1. Connecte-toi ou crée un compte sur [https://huggingface.co](https://huggingface.co)
  2. Va dans “Settings” > “Access Tokens”
  3. Clique sur “New token”, donne-lui un nom, choisis le scope “Read”
  4. Copie la clé générée
  5. Ajoute-la dans le `.env` :
     ```
     HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxx
     ```
- **Tarif** :
  - ✅ **Gratuit** (mais certaines API sont payantes)
  - Les modèles publics de base sont gratuits, les gros modèles et endpoints avancés peuvent nécessiter un abonnement ou du “credits”

---

## 3. GitHub API Token (optionnel)

- **Lien** : [GitHub Personal Tokens](https://github.com/settings/tokens)
- **Procédure** :
  1. Va sur [https://github.com/settings/tokens](https://github.com/settings/tokens)
  2. Clique sur "Generate new token" (classic ou fine-grained)
  3. Choisis les scopes nécessaires (lecture privée/public)
  4. Copie le token généré
  5. Ajoute-le dans le `.env` si tu veux cloner des repo privés :
     ```
     GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxx
     ```
- **Tarif** :
  - ✅ **Gratuit** pour accès public / perso

---

## 4. Google Drive API (optionnel, import/export)

- **Lien** : [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- **Procédure** :
  1. Crée un projet sur Google Cloud
  2. Active l’API “Google Drive”
  3. Va dans “Identifiants”
  4. Crée des identifiants OAuth 2.0 (Desktop ou Web app)
  5. Télécharge le JSON (client\_secret.json)
  6. Utilise ce fichier/token pour te connecter avec la lib `pydrive2`
  7. Mets le chemin dans le `.env` (si utilisé dans le projet)
- **Tarif** :
  - ✅ **Gratuit** (usage personnel modéré)
  - ⚠️ Limites pour un trop gros volume ou usage pro

---

## 5. Dropbox API Token (optionnel)

- **Lien** : [Dropbox App Console](https://www.dropbox.com/developers/apps)
- **Procédure** :
  1. Connecte-toi sur [https://www.dropbox.com/developers/apps](https://www.dropbox.com/developers/apps)
  2. Crée une “App”
  3. Gère les permissions (lecture/écriture selon besoin)
  4. Récupère le “Generated token” dans la page de config de l’app
  5. Ajoute-le dans le `.env` :
     ```
     DROPBOX_TOKEN=sl.ABCDEFGH...
     ```
- **Tarif** :
  - ✅ **Gratuit** (avec limites Dropbox, voir quota)

---

## 6. AWS S3 Access Keys (optionnel)

- **Lien** : [AWS Console IAM](https://console.aws.amazon.com/iam/)
- **Procédure** :
  1. Crée un compte AWS (gratuit pour 12 mois puis payant)
  2. Va dans “IAM” > “Users” > Ajoute un utilisateur
  3. Donne-lui la permission “AmazonS3FullAccess” (ou limitée)
  4. Garde les “Access Key ID” et “Secret Access Key”
  5. Ajoute-les dans le `.env` :
     ```
     AWS_ACCESS_KEY=AKIAxxxxxxxxxx
     AWS_SECRET_KEY=xxxxxxxxxxxxxxxx
     ```
- **Tarif** :
  - ⚠️ **Payant** (mais "Free Tier" la première année et pour petits volumes)

---

## 7. Autres (Bitbucket, GitLab, etc.)

- Utilise la même logique : créer une "App" ou un "Token" dans les settings de la plateforme.
- Ajoute la clé dans le `.env` comme :
  ```
  BITBUCKET_TOKEN=xxxx
  GITLAB_TOKEN=xxxx
  ```
- Vérifie la politique de chaque service (souvent gratuit pour lecture repo publics)

---

## 🚨 Important

- **Ne partage jamais tes clés** ! Ne push jamais `.env` sur GitHub.
- Pour les besoins du projet, le `.env` n’est PAS versionné (`.gitignore`)
- En cas de problème de clé, se référer à la doc officielle du service.

---

*Si une API t’affiche une erreur ou une limitation, vérifie ton quota sur le site du service ou ajoute un moyen de paiement.*

