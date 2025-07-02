# 🔑 API Key Setup Guide (EN)

This guide explains where and how to get every API key suggested/used in the **Chef d'Orchestre IA** project. For each key, you'll find:

- Official registration and activation link
- Step-by-step procedure
- Free/paid policy
- How to add it to your `.env` file

---

## 1. OpenAI API Key

- **Link**: [OpenAI API Keys](https://platform.openai.com/account/api-keys)
- **Procedure:**
  1. Create an account or sign in at [https://platform.openai.com](https://platform.openai.com)
  2. Go to “API Keys” (left menu)
  3. Click “Create new secret key”
  4. Copy the generated key
  5. Add it to your `.env` file:
     ```ini
     OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
     ```
- **Pricing:**
  - ⚠️ **Paid** after a small welcome credit (\~\$5)
  - OpenAI (GPT-3.5/4) requests are usage-billed (by token)
  - Free accounts have a credit cap, then require payment

---

## 2. HuggingFace API Token

- **Link**: [HuggingFace Tokens](https://huggingface.co/settings/tokens)
- **Procedure:**
  1. Sign up or log in at [https://huggingface.co](https://huggingface.co)
  2. Go to “Settings” > “Access Tokens”
  3. Click “New token,” give it a name, select “Read” scope
  4. Copy the generated token
  5. Add it to `.env`:
     ```ini
     HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxx
     ```
- **Pricing:**
  - ✅ **Free** (some advanced APIs are paid)
  - Public models are free, some advanced endpoints require “credits” or subscription

---

## 3. GitHub API Token (optional)

- **Link**: [GitHub Personal Tokens](https://github.com/settings/tokens)
- **Procedure:**
  1. Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
  2. Click “Generate new token” (classic or fine-grained)
  3. Choose needed scopes (read public/private repos)
  4. Copy the generated token
  5. Add to `.env` if you want to clone private repos:
     ```ini
     GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxx
     ```
- **Pricing:**
  - ✅ **Free** for public/personal access

---

## 4. Google Drive API (optional, import/export)

- **Link**: [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- **Procedure:**
  1. Create a project on Google Cloud
  2. Enable “Google Drive API”
  3. Go to “Credentials”
  4. Create OAuth 2.0 credentials (Desktop or Web app)
  5. Download the JSON file (`client_secret.json`)
  6. Use this file/token to connect with the `pydrive2` library
  7. Set the path in your `.env` (if needed by the project)
- **Pricing:**
  - ✅ **Free** (for moderate personal use)
  - ⚠️ Limits for high-volume or professional use

---

## 5. Dropbox API Token (optional)

- **Link**: [Dropbox App Console](https://www.dropbox.com/developers/apps)
- **Procedure:**
  1. Sign in at [https://www.dropbox.com/developers/apps](https://www.dropbox.com/developers/apps)
  2. Create an “App”
  3. Manage permissions (read/write as needed)
  4. Get your “Generated token” on the app config page
  5. Add to `.env`:
     ```ini
     DROPBOX_TOKEN=sl.ABCDEFGH...
     ```
- **Pricing:**
  - ✅ **Free** (Dropbox account quota applies)

---

## 6. AWS S3 Access Keys (optional)

- **Link**: [AWS Console IAM](https://console.aws.amazon.com/iam/)
- **Procedure:**
  1. Create an AWS account (free for 12 months, then paid)
  2. Go to “IAM” > “Users” > Add user
  3. Give “AmazonS3FullAccess” permissions (or limited)
  4. Copy the “Access Key ID” and “Secret Access Key”
  5. Add them to `.env`:
     ```ini
     AWS_ACCESS_KEY=AKIAxxxxxxxxxx
     AWS_SECRET_KEY=xxxxxxxxxxxxxxxx
     ```
- **Pricing:**
  - ⚠️ **Paid** (“Free Tier” for first year and small usage)

---

## 7. Others (Bitbucket, GitLab, etc.)

- Similar logic: create an "App" or "Token" in your account settings on each platform.
- Add the key in `.env` like:
  ```ini
  BITBUCKET_TOKEN=xxxx
  GITLAB_TOKEN=xxxx
  ```
- Check pricing for each (usually free for public repo read-only)

---

## 🚨 Important

- **Never share your keys!** Never push `.env` to GitHub.
- For this project, `.env` is **not** versioned (`.gitignore` protects it)
- If you have key/usage issues, refer to the official documentation of each service.

---

*If you see API errors or limits, check your quota on the service’s site or add a payment method if needed.*

