# Python_GUI
[BodyPass](https://www.bodypass.eu/) aims to break barriers between health sector and consumer goods sector and eliminate the current data silos.

The main objective of BodyPass is to foster exchange, linking and re-use, as well as to integrate 3D data assets from the two sectors. For this, BodyPass has to adapt and create tools that allow a secure exchange of information between data owners, companies and subjects (patients and customers).

This repository contains simple GUI examples for querying through the private blockchain network (HYPERLEDGER) developed by BodyPass. The use of GUIs requires having a wallet and an identity card at HYPERLEDGER.

* **GUI_Q01D3D**: GUI for Query type 0-1D3D. The GUI makes the query to HYPERLDEGER and access the services offered by the [Institute of Biomechanics of Valencia (IBV)](https://www.ibv.org/). You receive a 3D avatar that adjusts to the individual, and the requested measures.This query generates a full 3D the following fields are mandatory when submitting a transaction using the POST method:
  * Height : height in mm
  *	Weight : weight in kg
  *	Gender : male/female
  *	Age : age in years
  * Country Code : see ISO 3166 Alpha-2 
  
  Other metrics from the resource catalogue are optional.

* **GUI_Q03DHR**: GUI for Query type 0-3DHR. With this GUI you can enter a 3D scan with artifacts. The GUI makes the query to HYPERLDEGER and access the services offered by the [IBV](https://www.ibv.org/) and you receive a clean watertight 3D avatar that adjusts to the individual. The following fields are mandatory when submitting a transaction using the POST method:
  *	Height : height in mm
  *	Weight : weight in kg
  *	Gender : male/female
  *	Age : age in years
  *	CountryCode : see ISO 3166 Alpha-2
  *	file : the file storing the 3d triangular mesh. Pose: aeroplane. Extension : obj, ply, stl, zip

* **GUI_QA**: GUI for Query type A. This transaction queries a 3D model that is accessible by the participant. The GUI makes the query to HYPERLDEGER and access the services offered by the [IBV](https://www.ibv.org/) and you receive a clean waterthigh 3D avatar that adjusts to the individual and the measurements requested. You can also request measures included in the measurements catalague. The following field is mandatory when submitting a transaction using the POST method:
  *	data_code : The code of the 3D reconstruction that you want to obtain.

* **BODYPASScatalog.json**: Metrics included in the dictionary and stored by the system to well-define a metric. For any metric, the system stores the following:

  * ID: code that identifies the metric.
  * Designation: name of the metric.
  * Source: source of the metric. It usually refers to a standard definition.
  * Other std.: other standard definitions that can be compatible with the metric as defined here.
  * Definition: full and unambiguous description of the metric.
  * PartnerCodes: list of tuples “partner-code” where partner represents one of the project’s partners and code is the internal ID used on the partner’s database to identify the metric.
  * Media: urls to media files (images, 3Ds or videos) that facilitate the metric understanding.
  * Units: metric units employed.

