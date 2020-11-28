## Test Scraping - Datagram
Il s'agit d'un projet de scraping de la page  https://www.norauto.fr/t/pneu/w-205-h-55-r-16/ete-s.html/1/
 contenant une liste de produits
Les principales fonctionnalités sont:

* Création d'un fichier json contenant le nom ,le prix et l'url de chaque produit. 
* Création d'un fichier json contenant le rang, le keyword et l'url de chaque produit.
### Cloner le repo
```bash
git https://github.com/pathToProject
cd projectname
```
### Install Dependencies
```bash
pip install .
```
### Run script
```bash
python -m scrap
```
