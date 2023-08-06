# RestfulContentManager
A content manager for Jupyter that retrieves data from an external api

# Configuration
The most basic configuration takes a single parameter that provides the url for the api:

```python

from restfulContentManager import RestfulContentManager

c = get_config()

# ... other config ...

c.NotebookApp.contents_manager_class = RestfulContentManager
c.RestfulContentManager.api_endpoint = 'http:/myawesome.api/v1/"

```
