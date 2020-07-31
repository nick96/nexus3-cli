from nexuscli.api.repository.model import RawHostedRepository


def test_upload(upload_file_ensure_raises_api_error):
    """Ensure the method raises an exception when the API response is wrong"""
    upload_file_ensure_raises_api_error(RawHostedRepository)
