==================
 MetPX-Sarracenia
==================

[ Français_ ]

Overview
--------

MetPX-Sarracenia is a data duplication or distribution pump that leverages 
existing standard technologies (web servers and the `AMQP <http://www.amqp.org>`_ 
brokers) to achieve real-time message delivery and end to end transparency 
in file transfers.  Data sources establish a directory structure which is carried 
through any number of intervening pumps until they arrive at a client.  The 
client can provide explicit acknowledgement that propagates back through the 
network to the source.  Whereas traditional file switching is a point-to-point 
affair where knowledge is only between each segment, in Sarracenia, information 
flows from end to end in both directions.

At it's heart, sarracenia exposes a tree of web accessible folders (WAF), using 
any standard HTTP server (tested with apache).  Weather applications are soft 
real-time, where data should be delivered as quickly as possible to the next
hop, and minutes, perhaps seconds, count.  The standard web push technologies, 
ATOM, RSS, etc... are actually polling technologies that when used in low latency 
applications consume a great deal of bandwidth an overhead.  For exactly these 
reasons, those standards stipulate a minimum polling interval of five minutes.
Advanced Message Queueing Protocol (AMQP) messaging brings true push to 
notifications, and makes real-time sending far more efficient.

homepage: http://metpx.sf.net

Man Pages online: http://metpx.sourceforge.net/#sarracenia-documentation


Sarracenia is an initiative of Shared Services Canada ( http://ssc-spc.gc.ca )
in response to internal needs of the Government of Canada.


.. _Français:

Survol
------

MetPX-Sarracenia est un engin de copie et de distribution de données qui utilise 
des technologies standards (tel que les services web et le courtier de messages 
AMQP) afin d'effectuer des transferts de données en temps réel tout en permettant 
une transparence de bout en bout. Alors que chaque commutateur Sundew est unique 
en soit, offrant des configurations sur mesure et permutations de données multiples, 
Sarracenia cherche à maintenir l'intégrité de la structure des données, tel que 
proposée et organisée par la source, à travers tous les noeuds de la chaîne, 
jusqu'à destination. Le client peut fournir des accusés de réception qui se 
propagent en sens inverse jusqu'à la source. Tandis qu'un commutateur traditionnel 
échange les données de point à point, Sarracenia permet le passage des données 
d'un bout à l'autre du réseau, tant dans une direction que dans l'autre.

Sarracenia, à sa plus simple expression, expose une arborescence de dossiers disponibles 
sur la toile ("Web Accessible Folders"). Le temps de latence est une composante 
névralgique des applications météo: les minutes, et parfois les secondes, sont comptées. 
Les technologies standards, telles que ATOM et RSS, sont des technologies qui consomment 
beaucoup de bande passante et de ressouces lorsqu'elles doivent répondre à ces contraintes. 
Les standards limitent la fréquence maximale de vérification de serveur à cinq minutes. 
Le protocol de séquencement de messages avancés (Advanced Message Queuing Protocol, 
AMQP) est une approche beaucoup plus efficace pour la livraison d'annonces de 
nouveaux produits.

Sarracenia est une initiative de Services Partagés Canada ( http://ssc-spc.gc.ca ) en réponse à des besoins interne du gouvernement du Canada.

portail: http://metpx.sf.net




**2.16.08a1**

* Major Change: Changed "log" to "report" in all components.
* Added test case for sr_sender
* Documentation Update

**2.16.07a3**

* Ian's fix for sr_sender borked with post_exchange_split.
* Jun's fix for chmod and chmod_dir to be octal.

**2.16.07a2**

* Fixed typos that broke the package install in debian

**2.16.07a1**

* Added post_exchange_split config option (allows multiple cooperating sr_winnow instances) code, test suite mode, and documentation.
* fix logger output to file (bug #39 on sf)
* sr_amqp: Modified truncated exponential backoff to use multiplication instead of a table. So can modify max interval far more easily.  Also values are better.
* nicer formatting of sleep debug print.
* sr_post/sr_watch: added atime and mtime to post. (FR #41)
* sr_watch: handle file rename in watch directory (addresses bug #40)
* sr_watch: fix for on_post trigger to be called after filtering events.
* sr_sender: Added chmod_dir support (bug #28)
* plugin work: Made 'script incorrect' message more explicit about what is wrong in the script.
* plugin work: word smithery, replaced 'script' by 'plugin' in execfile. so the messages refer to 'plugin' errors.
* Added plugin part_check, which verbosely checks checksums,
* plugin work: Added dmf_renamers, modified for current convention, and word smithery in programmers guide.
* Tested (de-bugged) the missing file_rxpipe plugin, added it to the default list.
* Documentation improvements: sundew compatibility options to sr_subscribe.  
* Documentation improvements: moving code from subscriber to programming guide.  
* Added a note for documenting difference between senders and subscription clients in the message plugins.  
* Made reference to credentials.conf more explicit in all the command line component man pages. (Ian didn't understand he needed it... was not obvious.)
* Moved information about how to access credentials from plugin code from subscriber guide to programming guide.
* Turned a bit of the sr_watch man page into a CAVEAT section.
* Added a note about how file renaming is (poorly) handled at the moment.
* Test suite: removing overwrites of config files from test_sr_watch.sh
* Test suite: Continuing the quest:  getting rid of passwords in debug output,
* Test suite: adding explicit mention of exchange wherever possible.
* Fixed self-test to authenticate to broker as tfeed, but look for messages from tsource.

**0.0.1**


* Initial release


Michel Grenier <michel.grenier@IamRetiredNow.ca> (Retired)
  dd_subscribe, sr_subscribe, sr_sarra, sr_post, 
  All of the code, really.  

Jun Hu <jun.hu3@canada.ca>
  Documentation Diagrams, lead on deployments (head tester!)

Peter Silva <peter.silva@canada.ca>
  Project Manager & Evangelist. A lot of Documentation, and Review of Docs.
  Architect?  Much discussion with Michel.  Small bug fixes.

Khosrow Ebrahimpour <khosrow.ebrahimpour@canada.ca>
  Packaging & Process (Debian, Launchpad, some pypi, the vagrant self-test)

Daluma Sen <Daluma.Sen@canada.ca>
  sr_watch, and worked on sr_post as well for caching.

Murray Rennie <Murray.Rennie@canada.ca>
  sr_winnow, worked on that with Michel.



