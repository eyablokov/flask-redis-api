provider "google" {
  credentials = file("account-auth.json")
  project = "alien-trainer-269910"
  region = "europe-west1"
}
