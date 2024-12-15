#!/usr/bin/env python3
"""
Familiarize yourself with the client.GithubOrgClient class
"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from typing import Dict
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    declare the TestGithubOrgClient(unittest.TestCase) class
    """

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
        implement method test_org with test org
        """
        url = "https://api.github.com/orgs/{}".format(org_name)
        org_client = GithubOrgClient(org_name)
        org_client.org()
        mock_get_json.assert_called_once_with(url)

    def test_public_repos_url(self) -> None:
        """
        Implement the test_public_repos_url method to unit-test
        GithubOrgClient._public_repos_url
        """
        mock_payload = {"repos_url": "https://api.github.com/orgs/google/"}

        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_payload
            org_client = GithubOrgClient("google")
            result = org_client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/google/")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json) -> None:
        """
        Implement TestGithubOrgClient.test_public_repos to
        unit-test GithubOrgClient.public_repos
        """
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = mock_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "http://fakeurl.com"
            org_client = GithubOrgClient("fake_org")
            result = org_client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Dict[str, Dict],
                         license_key: str, expected: bool) -> None:
        """
        Implement TestGithubOrgClient.test_has_license to
        unit-test GithubOrgClient.has_license
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(['org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'], TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Create the TestIntegrationGithubOrgClient(unittest.TestCase)
    class and implement the setUpClass and tearDownClass which are
    part of the unittest.TestCase API
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        implement the setUpClass
        """
        mock_config = {"return_value.json.side_effect":
                       [cls.org_payload, cls.repos_payload,
                        cls.org_payload, cls.repos_payload]
                       }
        cls.get_patcher = patch("requests.get", **mock_config)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        implement the tearDownClass
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Implement the test_public_repos method to test
        GithubOrgClient.public_repos
        """
        org_client = GithubOrgClient("google")
        self.assertEqual(org_client.org, self.org_payload)
        self.assertEqual(org_client.repos_payload, self.repos_payload)

    def test_public_repos_with_license(self) -> None:
        """
        Implement test_public_repos_with_license to test the
        public_repos with the argument license="apache-2.0" and make
        sure the result matches the expected value from the fixtures
        """
        test_class = GithubOrgClient("google")
        assert True


if __name__ == "__main__":
    unittest.main()
