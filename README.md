<h1 align="center">Welcome to Tendances et opportunités 👋</h1>
<p>
  <a href="TODO doc" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://twitter.com/Riduidel" target="_blank">
    <img alt="Twitter: Riduidel" src="https://img.shields.io/twitter/follow/Riduidel.svg?style=social" />
  </a>
</p>

> Un outil d'observation des tendances de l'IT basé sur des données issues de sites publics (StackOverflow, GitHub, TechEmpower, ...

### Architecture

Autant que possible, les différentes données sont injectées dans BigQuery par des Google Cloud Function, puis aggrégées grâce à dataform.

Les différents éléments sont

### Dataform
Contient les différentes tables de transformation des données

### Google Cloud Function
Transforme les données venues "du monde extérieur" en tables BiGQuery.
Les fonctions actuellement déployées sont

* [extract_framework_categories_from_techempower](functions/extract_framework_categories_from_techempower/README.md)

### Google Secret Manager
Contient le token de connexion à GitHub

### Looker Studio

Fournit la visualisation des données

## Author

👤 **Nicolas Delsaux**

* Website: http://riduidel.wordpress.com
* Twitter: [@Riduidel](https://twitter.com/Riduidel)
* Github: [@Riduidel](https://github.com/Riduidel)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_