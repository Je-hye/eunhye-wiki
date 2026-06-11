import json
import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ComposeBoundaryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        result = subprocess.run(
            ["docker", "compose", "config", "--format", "json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        cls.compose = json.loads(result.stdout)

    def test_public_api_is_not_on_private_network(self) -> None:
        networks = self.compose["services"]["public-api"]["networks"]

        self.assertEqual({"public-tier"}, set(networks))

    def test_public_api_has_no_private_mounts(self) -> None:
        public_api = self.compose["services"]["public-api"]

        self.assertNotIn("volumes", public_api)
        self.assertNotIn("PRIVATE_DATABASE_URL", public_api["environment"])

    def test_web_is_not_a_bridge_between_trust_zones(self) -> None:
        networks = self.compose["services"]["web"]["networks"]

        self.assertEqual({"frontend-tier"}, set(networks))

    def test_private_api_is_bound_to_loopback(self) -> None:
        ports = self.compose["services"]["private-api"]["ports"]

        self.assertEqual("127.0.0.1", ports[0]["host_ip"])

    def test_databases_do_not_share_a_network(self) -> None:
        public_networks = set(self.compose["services"]["public-db"]["networks"])
        private_networks = set(self.compose["services"]["private-db"]["networks"])

        self.assertTrue(public_networks.isdisjoint(private_networks))


if __name__ == "__main__":
    unittest.main()
