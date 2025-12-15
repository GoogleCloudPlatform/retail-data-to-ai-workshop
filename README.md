# Demystifying Google Cloud Products for Retail & Supply Chain - Data & AI applications

This repository hosts `tutorials for LLM powered data & AI products` that can be leveraged in a Data-to-AI estate on Google Cloud. 

## Features <br>
(1) **Learning modules** - each covering a practical problem to be solved, architecture & considerations, code and configuration, and comprehensive instruction manuals, links to product documentation, and best practices for an immersive learning experience. <br> 

(2) **Primer on creating custom agents** with Agent Development Kit (ADK), hosting on Agent Engine with UI on Gemini Enterprise and leveraging MCP toolbox for databases <br> 

(3) **Fully functional multi-agent, autonomous agent `retail supply chain solution` (with public/synthetic data) for preventing stockouts** featuring the best of breed data and agent development techncial stack on Google Cloud. <br><br>
In some cases, the latest features are showcased, in public preview, and may also include features in private preview.<br>

Note: This repository will be kept current and new features will be steadily added, you can stay tuned by following the [roadmap](ROADMAP.md).

<hr>

## Objective
The objective is to demystify Google Cloud products and services for data and agentic development through a fully scripted hands-on and immersive learning experience with a relatable use case.<br>

<hr>

##  Disclaimer
1. This repository and its contents are not an official Google Product.
2. The code in this repository ***is intended for educational purposes***. While it can be used to quickstart development by enterprises, due diligence and hardening of the code is required for deployment to higher environments
3. The architecture showcased ***does not dictate*** retail and supply chain architecture, but merely how to use Google Cloud products to solve business problems.

<hr>

## Audience
The intended audience is anyone with interest in learning Google Cloud products. 

<hr>

## Format & Duration
The tutorials are fully scripted (no research needed), with (fully automated) environment setup (coming soon), data, code, commands, notebooks, orchestration, and configuration.<br>

**Option 1 - DIY:** <br> 
Clone the repo and follow the step by step instructions for an end to end developer experience.<br>

**Option 2 - Instructor-led workshop:** <br>
If you are a Google Cloud customer, you can reach out to your Google account team, and ask for an (no-cost) instructor-led workshop running on your GCP project (you will be responsible for GCP consumption).<br>

**Option 3 - Strapped for time / no GCP environment / dont need to try out but interested in knowing:** <br>
Just read the content like a book, there are pictorial overviews and screenshots of exactly what each module covers.

**Time commitment:** <br>
Expect to spend ~12 hours to fully understand, read product documentation and execute the tutorials.<br>

<hr>

## Dependencies

1. A Google Cloud project
2. IAM permissions to provision services, and grant IAM permissions
3. Basic knowledge of Google Cloud is useful, as is knowledge of comparabale platforms and techical stacks, but not required as comprehensive instructions are included
4. If a feature showcased is not accessible by you, it is likely a private preview feature and needs explicit allow-listing by the responsible product team. Reach out to your Google Cloud account team for help with allow-listing.

<hr>

## Level

L200 - L300

<hr>

## Technical Stack

| # | Purpose  | Product/Service/Technology |
| -- | :-- |  :--- |
| 1. | Operational database | AlloyDB |
| 2. | Analytical database | BigQuery |
| 3. | LLM-powered agenting grounding - metadata and golden dataset generation (no-code)| Dataplex `Data Insights API` |
| 4. | LLM-powered Data warehouse dimensional model code generation with just prompts (no-code)| `Data Engineering Agent` |
| 5. | LLM-powered Reporting Data Mart code generation with just prompts (no-code) | `Data Engineering Agent` |
| 6. | Workflow management and orchestration of BigQuery jobs | `Dataform` |
| 7. | Out of the box (no-code) Data QnA agent | BigQuery `Conversational Analytics API` |
| 8. | Out of the box (no-code) Exploratory Data Analysis & visualization with just prompts on Colab Enterprise | `Data Science Agent` |
| 9. | Generative AI functions with SQL | BigQuery `*.GENERATE*` functions |
| 10. | Time series forecasting | `TimesFM` and `Arima Plus` in BigQuery |
| 11. | Image generation | Gemini |
| 12. | Multimodal embedding generation with SQL | BigQuery `AI.EMBED` and `AI.GENERATE_EMBEDDING` |
| 13. | Multimodal search with SQL | Bigquery `VECTOR_SEARCH` abd `AI.SEARCH` |
| 14. | Apache Iceberg Lakehouse | BigQuery `Managed Iceberg Tables`<br>BigLake managed REST Catalog |
| 15. | Managed Apache Spark compute | `Dataproc Serverless` |
| 16. | Agent Development SDK* | Google Agent Development Kit (`ADK`) |
| 17. | Agent runtime* | `Agent Engine`  |
| 18. | Agent UI* | Agentspace on `Gemini Enterprise` |
| 19. | Standardized and secure database access tooling* | `MCP toolbox for databases` |
| 20. | Agent-to-Agent secure discovery, communication, and collaboration* | `A2A`  |
| 21. | Event driven orchestration* | Cloud Run Functions<br>Cloud Pub/Sub  |
| 22. | Time-based scheduling orchestration* | Cloud composer<br>  |
| 23. | Serverless compute* | Cloud Run |
| 24. | Secret store* | Secret Manager |
| 25. | Provisioning automation* | Terraform |

`*` - Coming soon

<hr>

## Learning Modules

| Module # | Focus  |
| -- | :-- | 
|   0. | [**Provisioning**](03-lab-manuals/Module-00-Provisioning.md) <br>gcloud commands<br>Terraform - coming soon | 
|   1. | [**BigQuery and AlloyDB interoperability**](03-lab-manuals/Module-01-AlloyDB-BQ-Interop.md) <br>BigQuery federation into AlloyDB<br>AlloyDB foriegn Data Wrapper for BigQuery  | 
|  2a. | [**Data profiling with Dataplex**](03-lab-manuals/Module-02a-Data-Insights-API.md) <br> Summary statistics generation and persistence| 
|  2b. | [**Data Insights at a table level for agentic grounding**](03-lab-manuals/Module-02b-Data-Insights-API.md) <br> LLM-powered table description generation<br> LLM-powered table column description generation <br> LLM-powered golden query generation (question and SQL pairs) | 
|  2c. | [**Data Insights at a dataset level for agentic grounding**](03-lab-manuals/Module-02c-Data-Insights-API.md) <br> LLM-powered dataset description generation<br> LLM-powered table relationships inference <br> LLM-powered cross table golden query generation (question and SQL pairs) | 
|   3. | [**(No code) Data Warehouse star schema code generation with BigQuery Data Engineering Agent**](03-lab-manuals/Module-03-Data-Engineering-Agent-For-Warehousing.md) <br>Have the Data Engineering Agent generate baseline Data Warehouse star schema with just prompts. Then run the same on Dataform and validate.  |
|   4. | [**(No code) Reporting Data Mart code generation with BigQuery Data Engineering Agent**](03-lab-manuals/Module-04-Data-Engineering-Agent-For-Reporting.md) <br>Have the Data Engineering Agent generate baseline Reporting Data Mart reports with just prompts. Then run the same on Dataform and validate.  | 
|   5. | [**(No code) Data QnA Agent standup in a minute with Conversational Analytics API**](03-lab-manuals/Module-05-Conversational-Analytics.md) <br> Zero code data QnA agent standup in the BigQuery UI with just instructions.  | 
|   6. | [**(No code) Exploratory Data Analysis with just prompts powered by BigQuery Data Science Agent on Colab Enterprise notebooks**](03-lab-manuals/Module-06-EDA-with-Data-Science-Agent.md) <br>Have the Data Science Agent on Colab Enterprise run Exploratory Data Analytics just prompts. You can then enhance this as needed, include update data with code generated by Data Science Agent.  | 
|   7. | [**Time series forecasting with TimesFM and ArimaPlus in BigQuery**](03-lab-manuals/Module-07-Forecasting-WithTimesFM.md) <br>Zero shot forecasting with TimesFM in BigQuery SQL and comparing with ArimaPlus in BigQuery. We will forecast retail sales and also item sales.  | 
|   8. | [**Generate content with SQL with Generative AI functions in BigQuery**](03-lab-manuals/Module-08-GenAI-Functions-In-BQ.md) <br>Using Generative AI functions in BigQuery - we will generate product descriptions and user manuals. We will learn to do keyword extraction, play with knobs for te same, then do sentiment analysis of product reviews   | 
|   9. | [**Embedding generation and vector search in BigQuery with just SQL**](03-lab-manuals/Module-09-Embedding-Gen-And-Vector-Search-In-BQ.md) <br> We will generate product images based on descriptions. We will then generate embeddings for the product description and images and learn to do text-to-text search as well as text-to-image search - all from within BigQuery with SQL  | 
| 10a. | [**Apache Iceberg Lakehouse in BigQuery with managed Iceberg tables**](https://github.com/anagha-google/retail-supply-chain-workshop/blob/main/03-lab-manuals/Module-10a-Apache-Iceberg-Lakehouse.md)   | 
|  11. | **Primer on Custom Agent Development on GCP with a data QnA chat application** (coming soon)   | 
|  12. | **Multi-agent, autonomous agent solution with best of breed Google Cloud agentic stack for preventing retail stockouts** (coming soon)   | 

<hr>



## Getting started

1. Review the dependencies and ensure they are met
2. Proceed to the [provisioning module](03-lab-manuals/Module-00-Provisioning.md).
3. Follow along each page of the user manual

<hr>

## Roadmap

If you would like additional features to be showcased, log an issue with details.<br>
To see what is coming, click [here](ROADMAP.md).

<hr>


## Issues

Share you feedback, and issues encountered, by logging issues.

<hr>

## Cleanup

If you provisioned a GCP project to run through this content, you can simply shut down the project to stop spend. Alternately, you can delete instances, shut down individual services. Terraform for cleanup is on the roadmap and will be made available.

<hr>

## Contributing

Contributions to this library are always welcome and highly encouraged.

See [CONTRIBUTING](CONTRIBUTING.md) for more information on how to get started.

Please note that this project is released with a Contributor Code of Conduct. By participating in
this project you agree to abide by its terms. See [Code of Conduct](CODE_OF_CONDUCT.md) for more
information.

<hr>

## Authors

This repository and content is maintained by the Google AI Ready Data Cloud Solution Architect team.

| # | Contributor  | Role |
| -- | :-- |  :--- |
| 1. | Anagha Khanolkar | Primary author|
| 2. | Ashwin Sridhar | Industry subject matter expertise - Supply Chain |
| 3. | Ryan Price | Industry subject matter expertise - Retail |

<hr>



## License

Apache 2.0 - See [LICENSE](LICENSE) for more information.

<hr>




