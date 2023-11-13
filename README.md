<h1 align="center">Welcome to Tendances et opportunités 👋</h1>
<p>
  <a href="TODO doc" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://twitter.com/Riduidel" target="_blank">
    <img alt="Twitter: Riduidel" src="https://img.shields.io/twitter/follow/Riduidel.svg?style=social" />
  </a>
</p>

> A tool to observe IT tendencies based upon data extracted from various public websites.

## ✨ Useful links

* [Public dashboard](https://lookerstudio.google.com/reporting/742da15c-8d95-492c-8b9b-77e82d71d6a9/page/MYsbD/edit)

## Architecture

### How does it works

A Google BigQuery project contains some Dataform processes which extract data from the public datasets of the given websites.
When no public dataset exists, dataform will invoke remote cloud functions which will fetch dta from the web, push it into Google Cloud Storage Buckets, which are in turn ingested into dataform. 

The following table explains for each website how information is ingested.

| Website         | Informations processed<br/>💡 when envisonned, 🚧 when being worked on (an issue is associated), ✅ when ok | Processing method |
|--------------|-----------|-|
| Stackoverflow | Questions ✅ with popularity 🚧 ([see #8](https://github.com/Zenika/tendances-et-opportunites/issues/8))<br/>Answers [🚧 (see #9](https://github.com/Zenika/tendances-et-opportunites/issues/9))      | Dataform (public dataset) |
| GitHub      | Projects 🚧 ([see #10](https://github.com/Zenika/tendances-et-opportunites/issues/10))  | Dataform (public dataset) |
| TechEmpower      | 🚧 ([see #12](https://github.com/Zenika/tendances-et-opportunites/issues/12))  | Cloud Function ➡️ GCS Bucket ➡️ Dataform

As much as posisble, we use Google Cloud Function to inject data into Google Big Query when no source exists.

### Dataform
Contains the vaious data transformation table

### Google Cloud Function
Transform data coming from the outer world into Big Query tables.
Currently deployed functions are

* [extract_framework_categories_from_techempower](functions/extract_framework_categories_from_techempower/README.md)

### Google Secret Manager
Contains GitHub connection secret

### Looker Studio
Provides data vizualisation

## Author

👤 **Nicolas Delsaux**

* Website: http://riduidel.wordpress.com
* Twitter: [@Riduidel](https://twitter.com/Riduidel)
* Github: [@Riduidel](https://github.com/Riduidel)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_