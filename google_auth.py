#!/usr/bin/env python

#設定環境變數 GOOGLE_APPLICATION_CREDENTIALS 來為應用程式程式碼提供驗證憑證
def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

#將路徑傳送至程式碼中的服務帳戶金鑰
def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        '/Users/dschen/gcp_keys/My First Project-7443813dd19f.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

#在 Compute Engine、Kubernetes Engine、App Engine 彈性環境和 Cloud Functions 上取得憑證
def explicit_compute_engine(project):
    from google.auth import compute_engine
    from google.cloud import storage

    # Explicitly use Compute Engine credentials. These credentials are
    # available on Compute Engine, App Engine Flexible, and Container Engine.
    credentials = compute_engine.Credentials()

    # Create the client using the credentials and specifying a project ID.
    storage_client = storage.Client(credentials=credentials, project=project)

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

#在 App Engine 標準環境中取得憑證
def explicit_app_engine(project):
    from google.auth import app_engine
    import googleapiclient.discovery

    # Explicitly use App Engine credentials. These credentials are
    # only available when running on App Engine Standard.
    credentials = app_engine.Credentials()

    # Explicitly pass the credentials to the client library.
    storage_client = googleapiclient.discovery.build(
        'storage', 'v1', credentials=credentials)

    # Make an authenticated API request
    buckets = storage_client.buckets().list(project=project).execute()
    print(buckets)

if __name__ == '__main__':

  implicit()
  explicit()
