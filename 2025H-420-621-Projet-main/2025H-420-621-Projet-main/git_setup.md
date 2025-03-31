# Configuration Git et GitHub pour le projet

## **1. Création d'un dépôt GitHub**
1. Connectez-vous à votre compte GitHub.
2. Cliquez sur le bouton **New** dans la barre latérale gauche pour créer un nouveau dépôt.
3. Remplissez les informations :
   - **Repository name** : `420-621-projet-echecs`.
   - **Description** : Jeu d'échecs multi-joueurs développé dans le cadre du cours 420-621.
   - **Visibility** : Choisissez `Private`.
4. Cliquez sur **Create repository**.

---

## **2. Initialisation d'un dépôt Git local**
### **Windows/Linux**
1. Ouvrez un terminal ou PowerShell et naviguez dans le dossier de votre projet :
   ```bash
   cd CHEMIN/ACCES/DE/VOTRE/PROJET
   ```
2. Initialisez un dépôt Git local :
   ```bash
   git init
   ```
3. Ajoutez le dépôt GitHub comme dépôt distant :
   ```bash
   git remote add origin git@github.com:<votre-utilisateur>/420-621-projet-echecs.git
   ```

---

## **3. Configuration des clés SSH**
### **Générer une clé SSH**
1. Vérifiez si vous avez déjà une clé SSH :
   ```bash
   ls ~/.ssh/id_rsa.pub  # Linux/Mac
   dir %USERPROFILE%\.ssh\id_rsa.pub  # Windows
   ```
   Si une clé existe, passez à l'étape suivante. Sinon, générez-en une nouvelle.

2. Générer une nouvelle clé SSH :
   ```bash
   ssh-keygen -t rsa -b 4096 -C "votre-email@example.com"
   ```
   Appuyez sur **Entrée** pour accepter l'emplacement par défaut, puis définissez un mot de passe (optionnel).

3. Ajoutez la clé SSH à l'agent SSH :
   ```bash
   eval $(ssh-agent -s)  # Linux/Mac
   ssh-add ~/.ssh/id_rsa
   ```
   Sur Windows (PowerShell) :
   ```bash
   ssh-add %USERPROFILE%\.ssh\id_rsa
   ```

### **Ajouter la clé SSH à GitHub**
1. Copiez la clé SSH dans le presse-papier :
   ```bash
   cat ~/.ssh/id_rsa.pub  # Linux/Mac
   type %USERPROFILE%\.ssh\id_rsa.pub  # Windows
   ```
2. Connectez-vous à GitHub, allez dans **Settings > SSH and GPG keys**, puis cliquez sur **New SSH key**.
3. Collez la clé dans le champ **Key** et donnez-lui un titre (par exemple, "Clé SSH pour projet 420-621").
4. Cliquez sur **Add SSH key**.

---

## **4. Faire un commit et un push**
1. Ajoutez tous les fichiers au suivi Git :
   ```bash
   git add .
   ```
2. Créez un commit avec un message descriptif :
   ```bash
   git commit -m "Initialisation du projet"
   ```
3. Poussez les modifications vers le dépôt GitHub :
   ```bash
   git push -u origin main
   ```

---

## **5. Vérification**
1. Rendez-vous sur votre dépôt GitHub pour vérifier que les fichiers ont bien été poussés.
2. Si vous travaillez en équipe, partagez le lien du dépôt avec votre coéquipier et assurez-vous qu'il a accès.

---

## **6. Commandes utiles**
- **Vérifier l'état du dépôt** :
  ```bash
  git status
  ```
- **Voir l'historique des commits** :
  ```bash
  git log
  ```
- **Mettre à jour le dépôt local avec les modifications distantes** :
  ```bash
  git pull origin main
  ```
- **Pousser de nouvelles modifications** :
  ```bash
  git push
  ```

---