# IGCrawlerService

Questo repository contiene il servizio di crawling per il progetto di SWE 2021/22: Guida Michelin @Social proposto da Zero12. 

## Requires

- [instagrapi](https://github.com/adw0rd/instagrapi) :  `pip install instagrapi`, unofficial Instagram API for Python
- [boto3](https://github.com/boto/boto3) : `pip install boto3`, Amazon Web Services (AWS) SDK for Python

## Changes

- La prima versione del crawler usava Selenium per fare web scraping su Instagram, basandosi sui tag HTML e gli attributi CSS. Questo metodo, seppur funzionante, era poco elegante e 
  potenzialmente inaffidabile in caso qualcosa fosse cambiato nell'HTML e CSS delle pagine analizzate.
- La seconda versione del crawler utilizza [instagrapi](https://github.com/adw0rd/instagrapi), un'API non ufficiale per Instagram, che offre più funzionalità e affidabilità.



