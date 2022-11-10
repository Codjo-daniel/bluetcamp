from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'datalakecodjo' # Must be replaced by your <storage_account_name>
    account_key = 'qTf6G9d9PEQDEEs42CkiJLQu7fc6HG9SXugbR6qo8pIiFQC6e0/i6wiP5yxE3v+N7BziSlXDOsjL+AStP0bCDw==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None