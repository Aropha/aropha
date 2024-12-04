# Aropha Digital Twin Solutions
<!-- badges: start -->
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Ypmo0l414TZhx4JTFwuT1bduYs0iRqgw?usp=drive_link)
<!-- badges: end -->

At [Aropha](https://www.aropha.com/), we deliver high-precision digital twin solutions that simulate the biodegradation of macromolecular polymers and small molecules with exceptional scalability. For a demonstration, you can explore this [Google Colab notebook](https://colab.research.google.com/drive/1Ypmo0l414TZhx4JTFwuT1bduYs0iRqgw?usp=drive_link) which provides a command-line interface (CLI) to our inference pipelines.

## Overview
This repository, **aropha**, provides a CLI that connects to Aropha’s simulation inference pipelines. The CLI reads in-silico biodegradation experiment data from a spreadsheet template, submits it to Aropha’s servers for processing, and retrieves the results directly to your computer. Designed with privacy at its core, the pipeline ensures zero visibility into your data: no data is printed, stored on hard drives, or retained on persistent storage — even temporarily. All computations performed entirely in RAM and results are securely delivered back to you.

### Installation
Aropha clients can install this CLI locally for connecting to our inference pipelines:
```
pip install git+https://github.com/aropha/aropha.git
```

### Biodegradation Simulation
Aropha provides a streamlined spreadsheet template for clients to design their biodegradation experiments. After purchasing simulation credits, clients can use the following command to process their simulations. The retrieved results will be saved automatically in the same folder as the spreadsheet template.

```
from aropha import Aropha

Aropha(
    email = 'your_email',
    password = 'your_password',
    address_to_spreadsheet = 'path/to/your/spreadsheet.xlsx'
)
```

### AI engines
We currently offer a suite of comprehensive digital twin solutions that simulates the biodegradation of both macromolecular polymers and small molecules.

Our development team continues to advance our AI engines, and updates to this repository will include additional solutions for broader biodegradation challenges.

| AI Engines        | Version (Release Date) | Chemical Space   | Notes                                    |
|--------------------|-------------------------|------------------|------------------------------------------|
| ArophaFormer      | v1.0 (Sep/23/2024)     | Comprehensive    | `Degree of Polymerization` ≤ 100                                 |
| ArophaGrapher     | v1.0 (Jan/31/2025)     | Comprehensive    | `Degree of Polymerization` ≤ 2000                               |
| ArophaPolyFormer  | v1.0 (Dec/31/2024)     | Polymer          | No limit for `Degree of Polymerization`, can take both SMILES string and monomer units |


### Contact
For a copy of the data entry spreadsheet template or any business inquiries, please contact our [business team](https://www.aropha.com/contact.html).