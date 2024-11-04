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
    engine = 'ArophaBiodegEngine_v1.0',
    address_to_spreadsheet = 'path/to/your/spreadsheet.xlsm'
)
```

### Current AI engines
We currently offer the **ArophaBiodegEngine_v1.0**, a comprehensive digital twin solution that simulates the biodegradation of both macromolecular polymers and small molecules.

Our development team continues to advance our AI engines, and updates to this repository will include additional solutions for broader biodegradation challenges.

### Contact
For a copy of the data entry spreadsheet template or any business inquiries, please contact our [business team](https://www.aropha.com/contact.html).