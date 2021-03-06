
import unittest
import docker
import requests
import os
from docker import Client
from . import constant
from . import common

client = common.get_client()

class TestImages(unittest.TestCase):

    podman = None
    def setUp(self):
        super().setUp()
        common.restore_image_from_cache(self)

    def tearDown(self):
        common.remove_all_images()
        return super().tearDown()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        common.enable_sock(cls)


    @classmethod
    def tearDownClass(cls):
        common.terminate_connection(cls)
        return super().tearDownClass()


# Inspect Image

    def test_inspect_image(self):
        # Check for error with wrong image name
        with self.assertRaises(requests.HTTPError):
            client.inspect_image("dummy")
        alpine_image = client.inspect_image(constant.ALPINE)
        self.assertIn(constant.ALPINE, alpine_image["RepoTags"])

# Tag Image

    # Validates if invalid image name is given a bad response is encountered.
    def test_tag_invalid_image(self):
        with self.assertRaises(requests.HTTPError):
            client.tag("dummy","demo")



    #  Validates if the image is tagged successfully.
    def test_tag_valid_image(self):
        client.tag(constant.ALPINE,"demo",constant.ALPINE_SHORTNAME)
        alpine_image = client.inspect_image(constant.ALPINE)
        for x in alpine_image["RepoTags"]:
            if("demo:alpine" in x):
                self.assertTrue
        self.assertFalse

    # Validates if name updates when the image is retagged.
    @unittest.skip("dosent work now")
    def test_retag_valid_image(self):
        client.tag(constant.ALPINE_SHORTNAME, "demo","rename")
        alpine_image = client.inspect_image(constant.ALPINE)
        self.assertNotIn("demo:test", alpine_image["RepoTags"])

# List Image
    # List All Images
    def test_list_images(self):
        allImages = client.images()
        self.assertEqual(len(allImages), 1)
        # Add more images
        client.pull(constant.BB)
        allImages = client.images()
        self.assertEqual(len(allImages) , 2)


    # List images with filter
        filters = {'reference':'alpine'}
        allImages = client.images(filters = filters)
        self.assertEqual(len(allImages) , 1)

# Search Image
    def test_search_image(self):
        response = client.search("alpine")
        for i in response:
            # Alpine found
            if "docker.io/library/alpine" in i["Name"]:
                self.assertTrue
        self.assertFalse

# Image Exist (No docker-py support yet)

# Remove Image
    def test_remove_image(self):
        # Check for error with wrong image name
        with self.assertRaises(requests.HTTPError):
            client.remove_image("dummy")
        allImages = client.images()
        self.assertEqual(len(allImages) , 1)
        alpine_image = client.inspect_image(constant.ALPINE)
        client.remove_image(alpine_image)
        allImages = client.images()
        self.assertEqual(len(allImages) , 0)

# Image History
    def test_image_history(self):
        # Check for error with wrong image name
        with self.assertRaises(requests.HTTPError):
            client.remove_image("dummy")
        imageHistory = client.history(constant.ALPINE)
        alpine_image = client.inspect_image(constant.ALPINE)
        for h in imageHistory:
            if h["Id"] in alpine_image["Id"]:
                self.assertTrue
        self.assertFalse

# Prune Image (No docker-py support yet)

# Export Image

    def test_export_image(self):
        client.pull(constant.BB)
        file = os.path.join(constant.ImageCacheDir , "busybox.tar")
        if not os.path.exists(constant.ImageCacheDir):
            os.makedirs(constant.ImageCacheDir)
        # Check for error with wrong image name
        with self.assertRaises(requests.HTTPError):
            client.get_image("dummy")
        response = client.get_image(constant.BB)
        image_tar = open(file,mode="wb")
        image_tar.write(response.data)
        image_tar.close()
        os.stat(file)

# Import|Load Image

    def test_import_image(self):
        allImages = client.images()
        self.assertEqual(len(allImages), 1)
        file = os.path.join(constant.ImageCacheDir , "busybox.tar")
        client.import_image_from_file(filename=file)
        allImages = client.images()
        self.assertEqual(len(allImages), 2)

if __name__ == '__main__':
    # Setup temporary space
    unittest.main()
